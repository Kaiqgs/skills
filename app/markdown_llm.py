import os
import logging
import time
from anthropic import Anthropic

# Suppress verbose HTTP logs from the Anthropic client
logging.getLogger("httpx").setLevel(logging.WARNING)

# Constants
MODEL = "claude-sonnet-4-5-20250929"
MAX_OUTPUT_TOKENS = 16000

# Pricing per million tokens
PRICING = {
    "regular": {"input": 3.00, "output": 15.00},
    "batch": {"input": 1.50, "output": 7.50}  # 50% off
}


def get_anthropic_client() -> Anthropic:
    """Get initialized Anthropic client with API key from environment."""
    api_key = os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("AVANTE_ANTHROPIC_API_KEY")
    return Anthropic(api_key=api_key)


def build_cleaning_prompt(markdown_content: str) -> str:
    """Build the cleaning prompt for the LLM."""
    return f"""Clean up and improve this documentation markdown:

1. Remove duplicate sections and repeated content
2. Remove navigation artifacts, footers, headers that appear on every page
3. Remove broken links and fix formatting issues
4. Organize content logically with proper headings
5. Preserve all unique technical information and code examples
6. Keep the documentation clear and concise

IMPORTANT: Return ONLY the cleaned markdown. Do not include any explanations, comments, or conversational text. Your entire response will be saved directly as a markdown file.

Here's the markdown to clean:

{markdown_content}"""


def estimate_llm_cost(markdown_content: str, use_batch: bool = False, max_output_tokens: int = MAX_OUTPUT_TOKENS) -> dict:
    """Estimate the cost of LLM cleaning using the Anthropic API token counting."""
    client = get_anthropic_client()
    cleaning_prompt = build_cleaning_prompt(markdown_content)

    # Use Anthropic API to count tokens
    token_count = client.messages.count_tokens(
        model=MODEL,
        messages=[{"role": "user", "content": cleaning_prompt}]
    )

    estimated_input_tokens = token_count.input_tokens
    estimated_output_tokens = max_output_tokens

    # Get pricing
    pricing_mode = "batch" if use_batch else "regular"
    prices = PRICING[pricing_mode]

    # Calculate costs
    input_cost = (estimated_input_tokens / 1_000_000) * prices["input"]
    output_cost = (estimated_output_tokens / 1_000_000) * prices["output"]
    total_cost = input_cost + output_cost

    return {
        "estimated_input_tokens": estimated_input_tokens,
        "estimated_output_tokens": estimated_output_tokens,
        "input_cost": input_cost,
        "output_cost": output_cost,
        "total_cost": total_cost,
        "mode": "Batch API" if use_batch else "Regular API"
    }


def clean_markdown_with_llm(markdown_content: str, use_batch: bool = False) -> str:
    """Clean markdown using Claude API (regular or batch mode)."""
    client = get_anthropic_client()
    cleaning_prompt = build_cleaning_prompt(markdown_content)

    logging.info(f"  → Input size: {len(markdown_content):,} characters")

    # Check token count before processing
    try:
        token_count = client.messages.count_tokens(
            model=MODEL,
            messages=[{"role": "user", "content": cleaning_prompt}]
        )
        estimated_tokens = token_count.input_tokens
        logging.info(f"  → Estimated input tokens: {estimated_tokens:,}")

        # Claude has a 200k token limit
        if estimated_tokens > 200000:
            raise Exception(
                f"Content is too large: {estimated_tokens:,} tokens exceeds the 200,000 token limit.\n"
                f"Try processing a smaller documentation set or implement chunking."
            )
        elif estimated_tokens > 180000:
            logging.warning(f"  ⚠ Warning: Content is very large ({estimated_tokens:,} tokens). Approaching the 200k limit.")
    except Exception as e:
        if "too large" in str(e) or "exceeds" in str(e):
            raise
        logging.warning(f"  ⚠ Could not estimate token count: {e}")

    if use_batch:
        logging.info("  → Creating batch request (50% cost savings!)...")

        # Create batch request
        batch = client.messages.batches.create(
            requests=[{
                "custom_id": "cleanup-docs",
                "params": {
                    "model": MODEL,
                    "max_tokens": MAX_OUTPUT_TOKENS,
                    "messages": [
                        {"role": "user", "content": cleaning_prompt}
                    ]
                }
            }]
        )

        logging.info(f"  → Batch created: {batch.id}")
        logging.info(f"  → Status: {batch.processing_status}")
        logging.info("  → Waiting for batch to complete (this may take a few minutes)...")

        # Poll for completion
        while batch.processing_status in ["in_progress", "pending"]:
            time.sleep(10)  # Check every 10 seconds
            batch = client.messages.batches.retrieve(batch.id)
            logging.info(f"  → Status: {batch.processing_status}")

        if batch.processing_status != "ended":
            raise Exception(f"Batch processing failed with status: {batch.processing_status}")

        # Retrieve results
        logging.info("  → Retrieving batch results...")
        results = list(client.messages.batches.results(batch.id))

        if not results:
            raise Exception("No batch results returned")

        result = results[0].result

        # Check if the result is an error
        if result.type == "errored":
            error_info = result.error
            error_message = error_info.message if hasattr(error_info, 'message') else str(error_info)

            # Check if it's a token limit error
            if "too long" in error_message or "maximum" in error_message:
                raise Exception(
                    f"Content exceeds token limit: {error_message}\n"
                    "Try processing a smaller documentation set or implement chunking."
                )
            else:
                raise Exception(f"Batch processing error: {error_message}")

        message = result.message
        cleaned_content = message.content[0].text

        # Log usage information
        logging.info(f"  → Output size: {len(cleaned_content):,} characters")
        logging.info(f"  → Tokens used - Input: {message.usage.input_tokens:,}, Output: {message.usage.output_tokens:,}")
        logging.info(f"  → Batch stats - Processing: {batch.request_counts.processing}, Succeeded: {batch.request_counts.succeeded}, Errors: {batch.request_counts.errored}")

    else:
        logging.info("  → Calling Claude API (this may take a moment)...")

        message = client.messages.create(
            model=MODEL,
            max_tokens=MAX_OUTPUT_TOKENS,
            messages=[
                {"role": "user", "content": cleaning_prompt}
            ]
        )

        cleaned_content = message.content[0].text

        # Log usage information
        logging.info(f"  → Output size: {len(cleaned_content):,} characters")
        logging.info(f"  → Tokens used - Input: {message.usage.input_tokens:,}, Output: {message.usage.output_tokens:,}")

    return cleaned_content
