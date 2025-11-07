import os
import logging
import traceback
from typing import List


def apply_cleaning_functions(page_paths: List[str], cleaning_code: str, output_dir: str) -> List[str]:
    """
    Apply LLM-generated cleaning functions to all pages and save to output directory.

    Args:
        page_paths: List of absolute paths to original markdown files
        cleaning_code: Python code string defining clean_line() and clean_doc()
        output_dir: Directory to save cleaned markdown files

    Returns:
        List of absolute paths to cleaned markdown files

    Raises:
        Exception: If cleaning functions fail to execute properly
    """
    logging.info(f"  → Applying cleaning functions to {len(page_paths)} page(s)...")

    # Execute cleaning code to load functions into namespace
    namespace = {}
    try:
        exec(cleaning_code, namespace)
    except Exception as e:
        raise Exception(f"Failed to execute cleaning code: {e}\n{traceback.format_exc()}")

    # Verify functions exist
    if 'clean_line' not in namespace or 'clean_doc' not in namespace:
        raise Exception("Cleaning code must define both clean_line() and clean_doc() functions")

    clean_line_func = namespace['clean_line']
    clean_doc_func = namespace['clean_doc']

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    cleaned_paths = []
    success_count = 0
    error_count = 0
    total_chars_removed = 0

    for page_path in page_paths:
        if not os.path.exists(page_path):
            logging.warning(f"  ⚠ Page not found, skipping: {page_path}")
            error_count += 1
            continue

        page_name = os.path.basename(page_path)
        output_path = os.path.join(output_dir, page_name)


        try:
            # Read original page
            with open(page_path, "r", encoding="utf-8") as f:
                original_content = f.read()

            original_content_length = len(original_content)

            # Apply line-by-line cleaning
            lines = original_content.split('\n')
            cleaned_lines = []

            for line in lines:
                try:
                    cleaned_line = clean_line_func(line)
                    # Keep line if it returns non-empty string
                    if cleaned_line is not None and cleaned_line != "":
                        cleaned_lines.append(cleaned_line)
                except Exception as e:
                    # If clean_line fails, keep original line
                    logging.warning(f"  ⚠ clean_line() failed for line in {page_name}, keeping original: {e}")
                    cleaned_lines.append(line)

            # Reconstruct document
            line_cleaned_content = '\n'.join(cleaned_lines)

            # Apply document-level cleaning
            try:
                final_content = clean_doc_func(line_cleaned_content)
            except Exception as e:
                logging.warning(f"  ⚠ clean_doc() failed for {page_name}, using line-cleaned version: {e}")
                final_content = line_cleaned_content

            # Save cleaned page
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(final_content)

            final_content_length = len(final_content)
            delta_content_length = original_content_length - final_content_length
            logging.info(f"  ✓ Cleaned {page_name}, removed {delta_content_length} characters")
            total_chars_removed += delta_content_length

            cleaned_paths.append(output_path)
            success_count += 1

            # Log progress every 10 pages
            if success_count % 10 == 0:
                logging.info(f"     Processed {success_count}/{len(page_paths)} pages...")

        except Exception as e:
            logging.error(f"  ✗ Failed to clean {page_name}: {e}")
            error_count += 1
            # Continue with other pages even if one fails

    logging.info(f"  ✓ Cleaned {success_count} page(s), {error_count} error(s)")
    logging.info(f"  ✓ Cleaned {total_chars_removed} characters in total")

    if success_count == 0:
        raise Exception("Failed to clean any pages successfully")

    return cleaned_paths


def get_cleaned_page_paths(cleaned_dir: str) -> List[str]:
    """
    Get list of all markdown files in the cleaned directory.

    Args:
        cleaned_dir: Path to directory containing cleaned markdown files

    Returns:
        List of absolute paths to cleaned markdown files
    """
    if not os.path.exists(cleaned_dir):
        return []

    cleaned_paths = []
    for filename in sorted(os.listdir(cleaned_dir)):
        if filename.endswith('.md'):
            cleaned_paths.append(os.path.join(cleaned_dir, filename))

    return cleaned_paths
