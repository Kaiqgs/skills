import logging
import traceback
from anthropic import Anthropic
from app.markdown_llm import get_anthropic_client, MODEL, PRICING


def build_generation_prompt(sampled_content: str) -> str:
    """Build the prompt for generating cleaning functions."""
    return f"""You are a Python code generator. Based on the following samples from documentation markdown files, create TWO Python functions to clean the content:

1. **clean_line(line: str) -> str**
   - Takes a single line of markdown text
   - Returns the cleaned line (or empty string to remove the line entirely)
   - Use this for: removing navigation bars, footers, repeated headers, unnecessary whitespace
   - Should handle edge cases (None, empty strings)

2. **clean_doc(md: str) -> str**
   - Takes a full markdown document as a single string
   - Returns the cleaned document
   - Use this for: structural fixes, removing duplicate sections, fixing formatting issues
   - Should handle edge cases (None, empty strings)

**CRITICAL REQUIREMENTS:**
- Return ONLY valid Python code with NO explanations, comments, or markdown formatting
- Both functions MUST be defined
- Use only Python standard library (re, string, etc. are OK, but no external packages)
- Functions must be safe and handle edge cases gracefully
- DO NOT include any text before or after the Python code
- DO NOT wrap the code in markdown code blocks (no ```python)

**SAMPLES FROM DOCUMENTATION:**

{sampled_content}

**YOUR RESPONSE (Python code only):**"""


def estimate_page_cleaning_cost(sampled_content: str, max_retries: int = 5) -> dict:
    """
    Estimate the cost of generating and validating cleaning functions.

    Args:
        sampled_content: Sampled markdown content to inform function generation
        max_retries: Maximum number of retry attempts (worst case scenario)

    Returns:
        Dictionary with cost breakdown
    """
    client = get_anthropic_client()

    # Build the generation prompt to estimate initial cost
    generation_prompt = build_generation_prompt(sampled_content)

    # Count tokens for generation prompt
    token_count = client.messages.count_tokens(
        model=MODEL,
        messages=[{"role": "user", "content": generation_prompt}]
    )

    estimated_input_tokens = token_count.input_tokens

    # Estimate output tokens for code generation (typically 500-2000 tokens for functions)
    estimated_output_per_attempt = 1500

    # Worst case: max_retries attempts (each retry also needs input tokens for fix prompt)
    # Fix prompts include original sample + error context, so they're longer
    fix_prompt_multiplier = 1.3  # Fix prompts are ~30% longer due to error context

    # Calculate worst-case scenario
    worst_case_input = estimated_input_tokens  # Initial generation
    worst_case_input += int((estimated_input_tokens * fix_prompt_multiplier) * (max_retries - 1))  # Retries

    worst_case_output = estimated_output_per_attempt * max_retries

    # Calculate best-case scenario (success on first try)
    best_case_input = estimated_input_tokens
    best_case_output = estimated_output_per_attempt

    # Get pricing (regular API only, no batch for function generation due to retry needs)
    prices = PRICING["regular"]

    # Calculate costs
    best_input_cost = (best_case_input / 1_000_000) * prices["input"]
    best_output_cost = (best_case_output / 1_000_000) * prices["output"]
    best_total = best_input_cost + best_output_cost

    worst_input_cost = (worst_case_input / 1_000_000) * prices["input"]
    worst_output_cost = (worst_case_output / 1_000_000) * prices["output"]
    worst_total = worst_input_cost + worst_output_cost

    return {
        "sample_size_chars": len(sampled_content),
        "estimated_sample_tokens": estimated_input_tokens,
        "max_retries": max_retries,
        "best_case": {
            "input_tokens": best_case_input,
            "output_tokens": best_case_output,
            "input_cost": best_input_cost,
            "output_cost": best_output_cost,
            "total_cost": best_total
        },
        "worst_case": {
            "input_tokens": worst_case_input,
            "output_tokens": worst_case_output,
            "input_cost": worst_input_cost,
            "output_cost": worst_output_cost,
            "total_cost": worst_total
        }
    }


def build_fix_prompt(sampled_content: str, error_context: dict) -> str:
    """Build the prompt for fixing a broken cleaning function."""
    return f"""The Python cleaning functions you generated have an error. Please fix the code.

**ORIGINAL CODE THAT FAILED:**
```python
{error_context['code']}
```

**ERROR MESSAGE:**
{error_context['error']}

**FULL TRACEBACK:**
{error_context['traceback']}

**ATTEMPT NUMBER:** {error_context['attempt']}

**SAMPLES FROM DOCUMENTATION (for context):**
{sampled_content}

**REQUIREMENTS:**
- Return ONLY the corrected Python code
- NO explanations, comments, or markdown formatting
- Both clean_line() and clean_doc() must be defined
- Fix the specific error mentioned above
- DO NOT wrap in code blocks (no ```python)

**YOUR CORRECTED CODE:**"""


def generate_cleaning_functions(sampled_content: str, max_retries: int = 5) -> str:
    """
    Generate Python cleaning functions using Claude API with iterative retry.

    Args:
        sampled_content: Sampled markdown content to inform function generation
        max_retries: Maximum number of attempts to generate valid functions

    Returns:
        Valid Python code as a string defining clean_line() and clean_doc()

    Raises:
        Exception: If unable to generate valid functions after max_retries
    """
    client = get_anthropic_client()
    attempt = 0
    error_context = None

    logging.info(f"  → Generating cleaning functions with Claude API (max {max_retries} attempts)...")

    while attempt < max_retries:
        try:
            # Generate or fix the code
            if attempt == 0:
                prompt = build_generation_prompt(sampled_content)
                logging.info(f"  → Attempt {attempt + 1}/{max_retries}: Generating functions...")
            else:
                prompt = build_fix_prompt(sampled_content, error_context)
                logging.info(f"  → Attempt {attempt + 1}/{max_retries}: Fixing errors...")

            # Call Claude API
            message = client.messages.create(
                model=MODEL,
                max_tokens=4000,
                messages=[{"role": "user", "content": prompt}]
            )

            code = message.content[0].text.strip()

            # Remove markdown code blocks if LLM included them despite instructions
            if code.startswith("```python"):
                code = code.replace("```python", "", 1)
            if code.startswith("```"):
                code = code.replace("```", "", 1)
            if code.endswith("```"):
                code = code[:-3]
            code = code.strip()

            logging.info(f"  → Validating generated code ({len(code)} chars)...")

            # Test execution in isolated namespace
            namespace = {}
            exec(code, namespace)

            # Validate both functions exist
            if 'clean_line' not in namespace:
                raise ValueError("Function 'clean_line' is not defined in generated code")
            if 'clean_doc' not in namespace:
                raise ValueError("Function 'clean_doc' is not defined in generated code")

            # Test functions with dummy data
            clean_line_func = namespace['clean_line']
            clean_doc_func = namespace['clean_doc']

            # Test clean_line
            test_result = clean_line_func("Test line with content")
            if not isinstance(test_result, str):
                raise TypeError(f"clean_line() must return str, got {type(test_result)}")

            # Test clean_doc
            test_result = clean_doc_func("# Test Document\n\nSome content here.")
            if not isinstance(test_result, str):
                raise TypeError(f"clean_doc() must return str, got {type(test_result)}")

            # Test edge cases
            clean_line_func("")
            clean_line_func(None) if None else clean_line_func("")  # Handle None gracefully
            clean_doc_func("")

            # Success!
            logging.info(f"  ✓ Functions validated successfully on attempt {attempt + 1}")
            logging.info(f"  → Token usage - Input: {message.usage.input_tokens:,}, Output: {message.usage.output_tokens:,}")

            return code

        except Exception as e:
            error_context = {
                "code": code if 'code' in locals() else "No code generated",
                "error": str(e),
                "traceback": traceback.format_exc(),
                "attempt": attempt + 1
            }

            logging.warning(f"  ⚠ Validation failed on attempt {attempt + 1}/{max_retries}")
            logging.warning(f"     Error: {str(e)}")

            attempt += 1

    # Max retries exhausted
    raise Exception(
        f"Failed to generate valid cleaning functions after {max_retries} attempts.\n"
        f"Last error: {error_context['error']}\n"
        f"Last code:\n{error_context['code']}"
    )
