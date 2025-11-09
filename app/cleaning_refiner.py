import logging
import traceback
from typing import Dict, Tuple
from app.markdown_llm import get_anthropic_client, MODEL, MAX_OUTPUT_TOKENS
from app.cleaning_evaluator import evaluate_cleaning_quality_with_llm
from app.iteration_manager import save_iteration, save_best_iteration
from app.folder_structure import get_iterations_dir


def apply_cleaning_code_to_sample(sample: str, code: str) -> str:
    namespace = {}
    exec(code, namespace)

    clean_line_func = namespace['clean_line']
    clean_doc_func = namespace['clean_doc']

    lines = sample.split('\n')
    cleaned_lines = []

    for line in lines:
        try:
            cleaned_line = clean_line_func(line)
            if cleaned_line is not None and cleaned_line != "":
                cleaned_lines.append(cleaned_line)
        except Exception:
            cleaned_lines.append(line)

    line_cleaned = '\n'.join(cleaned_lines)

    try:
        final_cleaned = clean_doc_func(line_cleaned)
    except Exception:
        final_cleaned = line_cleaned

    return final_cleaned


def build_initial_generation_prompt(sampled_content: str) -> str:
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


def build_refinement_prompt(sampled_content: str, previous_iteration: Dict) -> str:
    evaluation = previous_iteration["evaluation"]

    quality_score = evaluation.get("quality_score", 0.0)
    assessment = evaluation.get("assessment", "No assessment provided")
    issues = evaluation.get("issues_found", [])
    improvements = evaluation.get("improvements_needed", [])
    patterns_removed = evaluation.get("patterns_removed", [])

    issues_text = "\n".join([f"  - {issue}" for issue in issues]) if issues else "  (No critical issues identified)"
    improvements_text = "\n".join([f"  - {imp}" for imp in improvements]) if improvements else "  (Focus on edge cases and minor refinements)"
    patterns_text = ", ".join(patterns_removed) if patterns_removed else "none identified"

    return f"""You are generating IMPROVED Python cleaning functions for documentation markdown based on feedback from a previous attempt.

**PREVIOUS ATTEMPT FEEDBACK:**
- Quality Score: {quality_score:.2f} / 1.00
- Assessment: {assessment}
- Patterns Successfully Removed: {patterns_text}

**Issues Found:**
{issues_text}

**Improvements Needed:**
{improvements_text}

**SAMPLE BEFORE CLEANING (first 4000 chars):**
```
{sampled_content[:4000]}
```

**SAMPLE AFTER PREVIOUS CLEANING ATTEMPT (first 4000 chars):**
```
{previous_iteration["sample_after"][:4000]}
```

**YOUR TASK:**
Generate COMPLETELY NEW clean_line() and clean_doc() functions that address the issues and improvements above.

DO NOT make incremental tweaks - rethink your approach based on the feedback.

Focus on:
1. Addressing the specific issues mentioned in the feedback
2. Implementing the improvements requested
3. Being more conservative or aggressive as needed based on the quality score and assessment

**REQUIREMENTS:**
- Return ONLY valid Python code (no markdown, no explanations)
- Both clean_line() and clean_doc() must be defined
- Use only Python standard library
- DO NOT wrap in code blocks (no ```python)

**YOUR NEW CODE:**"""


def generate_cleaning_code(prompt: str) -> Tuple[str, Dict]:
    client = get_anthropic_client()

    message = client.messages.create(
        model=MODEL,
        max_tokens=MAX_OUTPUT_TOKENS,
        messages=[{"role": "user", "content": prompt}]
    )

    code = message.content[0].text.strip()

    if code.startswith("```python"):
        code = code.replace("```python", "", 1)
    if code.startswith("```"):
        code = code.replace("```", "", 1)
    if code.endswith("```"):
        code = code[:-3]
    code = code.strip()

    token_usage = {
        "input_tokens": message.usage.input_tokens,
        "output_tokens": message.usage.output_tokens
    }

    return code, token_usage


def validate_cleaning_code(code: str) -> bool:
    try:
        namespace = {}
        exec(code, namespace)

        if 'clean_line' not in namespace:
            raise ValueError("Function 'clean_line' is not defined")
        if 'clean_doc' not in namespace:
            raise ValueError("Function 'clean_doc' is not defined")

        clean_line_func = namespace['clean_line']
        clean_doc_func = namespace['clean_doc']

        test_result = clean_line_func("Test line")
        if not isinstance(test_result, str):
            raise TypeError(f"clean_line() must return str, got {type(test_result)}")

        test_result = clean_doc_func("# Test\\n\\nContent")
        if not isinstance(test_result, str):
            raise TypeError(f"clean_doc() must return str, got {type(test_result)}")

        clean_line_func("")
        clean_doc_func("")

        return True

    except Exception as e:
        logging.warning(f"  ⚠ Validation failed: {e}")
        return False


def iterative_cleaning_generation(
    sampled_content: str,
    base_name: str,
    smooth_max_iterations: int = 3,
    error_max_iterations: int = 5
) -> Dict:
    iterations = []
    best_iteration = None
    best_quality_score = 0.0
    total_input_tokens = 0
    total_output_tokens = 0

    had_errors = False
    max_iterations = smooth_max_iterations

    logging.info(f"\n{'='*80}")
    logging.info(f"ITERATIVE CLEANING FUNCTION GENERATION")
    logging.info(f"{'='*80}\n")

    for i in range(max_iterations):
        logging.info(f"\n--- Iteration {i+1}/{max_iterations} ---\n")

        try:
            if i == 0:
                prompt = build_initial_generation_prompt(sampled_content)
                logging.info(f"  → Generating initial cleaning functions...")
            else:
                prompt = build_refinement_prompt(sampled_content, iterations[-1])
                logging.info(f"  → Refining based on previous evaluation...")

            code, code_tokens = generate_cleaning_code(prompt)
            total_input_tokens += code_tokens["input_tokens"]
            total_output_tokens += code_tokens["output_tokens"]

            logging.info(f"  → Validating generated code...")
            if not validate_cleaning_code(code):
                logging.warning(f"  ⚠ Code validation failed, skipping iteration")
                had_errors = True
                if max_iterations < error_max_iterations:
                    max_iterations = error_max_iterations
                    logging.info(f"  → Extending max iterations to {error_max_iterations} due to errors")
                continue

            logging.info(f"  ✓ Code validated successfully")

            logging.info(f"  → Applying to sample...")
            cleaned_sample = apply_cleaning_code_to_sample(sampled_content, code)

            logging.info(f"  → Evaluating quality with LLM...")
            evaluation = evaluate_cleaning_quality_with_llm(
                sampled_content,
                cleaned_sample,
                i + 1
            )

            total_input_tokens += evaluation["token_usage"]["input_tokens"]
            total_output_tokens += evaluation["token_usage"]["output_tokens"]

            if not evaluation.get("improvements_needed"):
                logging.warning(f"  ⚠ Empty improvements_needed in evaluation - LLM may not be providing actionable feedback")
            if not evaluation.get("issues_found"):
                logging.info(f"  ✓ No critical issues found")

            iteration_data = {
                "iteration_num": i + 1,
                "cleaning_code": code,
                "sample_before": sampled_content,
                "sample_after": cleaned_sample,
                "evaluation": evaluation,
                "code_generation_tokens": code_tokens,
                "total_tokens": {
                    "input_tokens": total_input_tokens,
                    "output_tokens": total_output_tokens
                }
            }

            save_iteration(base_name, i + 1, iteration_data)
            iterations.append(iteration_data)

            quality_score = evaluation.get("quality_score", 0.0)

            if quality_score > best_quality_score:
                best_quality_score = quality_score
                best_iteration = iteration_data
                logging.info(f"  ✓ NEW BEST QUALITY: {quality_score:.2f}")

            if quality_score >= 0.98:
                logging.info(f"  ✓ Excellent quality achieved ({quality_score:.2f})! Stopping early.")
                break

            if i > 0 and quality_score < iterations[-2]["evaluation"].get("quality_score", 0.0):
                logging.info(f"  ⚠ Quality regression detected ({quality_score:.2f} < {iterations[-2]['evaluation'].get('quality_score', 0.0):.2f})")
                logging.info(f"  → Stopping and using best iteration")
                break

        except Exception as e:
            logging.error(f"  ✗ Iteration {i+1} failed: {e}")
            logging.error(traceback.format_exc())
            had_errors = True
            if max_iterations < error_max_iterations:
                max_iterations = error_max_iterations
                logging.info(f"  → Extending max iterations to {error_max_iterations} due to errors")

    if best_iteration is None:
        raise Exception("Failed to generate any valid cleaning functions")

    save_best_iteration(base_name, best_iteration)

    logging.info(f"\n{'='*80}")
    logging.info(f"ITERATIVE GENERATION COMPLETE")
    logging.info(f"{'='*80}")
    logging.info(f"  Best quality score: {best_quality_score:.2f}")
    logging.info(f"  Total iterations: {len(iterations)}")
    logging.info(f"  Best iteration: {best_iteration['iteration_num']}")
    logging.info(f"  Total tokens: {total_input_tokens:,} input, {total_output_tokens:,} output")

    return {
        "iterations": iterations,
        "best_iteration": best_iteration,
        "best_quality_score": best_quality_score,
        "total_tokens": {
            "input_tokens": total_input_tokens,
            "output_tokens": total_output_tokens
        }
    }
