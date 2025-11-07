import os
import time
import logging
from typing import Set, List, Optional
from urllib.parse import urlparse, urlunparse
from selenium.webdriver import Chrome
import markdownify
from selenium.webdriver.common.by import By

from app.folder_structure import PAGES_DIR, SKILLS_DIR, CLEAN_DIR
from app.url_to_name import url_to_name
from app.markdown_llm import clean_markdown_with_llm, estimate_llm_cost
from app.page_sampler import sample_pages_for_analysis
from app.cleaning_function_generator import generate_cleaning_functions, estimate_page_cleaning_cost
from app.page_cleaner import apply_cleaning_functions, get_cleaned_page_paths
from app.logging_util import log_header, log_success, log_info, log_warning

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')


def strip_url_fragment(url: str) -> str:
    """Remove the fragment (#section) from a URL to avoid duplicate downloads of single-page docs."""
    parsed = urlparse(url)
    return urlunparse(parsed._replace(fragment=""))


def crawl_and_save_pages(driver: Chrome, base_url: str, page_directory: str, visited: Set[str], page_paths: List[str]) -> None:
    to_visit = [base_url]

    while to_visit:
        current_url = to_visit.pop(0)
        current_url_no_fragment = strip_url_fragment(current_url)

        if current_url_no_fragment in visited:
            continue

        visited.add(current_url_no_fragment)

        logging.info(f"[{len(to_visit)} left] Crawling: {current_url_no_fragment}")

        driver.get(current_url)
        time.sleep(2)

        html_content = driver.page_source
        markdown_content = markdownify.markdownify(html_content)

        page_name = url_to_name(current_url_no_fragment)
        page_path = os.path.join(page_directory, f"{page_name}.md")

        with open(page_path, "w") as f:
            f.write(markdown_content)

        page_paths.append(page_path)
        logging.info(f"  ✓ Saved to: {page_name}.md")

        all_links = [a.get_attribute("href") for a in driver.find_elements(By.TAG_NAME, "a")]
        same_domain_links = [link for link in all_links if link and base_url in link]
        # Strip fragments from links before checking visited/to_visit
        same_domain_links_no_fragment = [strip_url_fragment(link) for link in same_domain_links]
        new_links = [link for link in same_domain_links_no_fragment if link not in visited and link not in to_visit]

        if new_links:
            logging.info(f"  → Found {len(new_links)} new link(s)")

        to_visit.extend(new_links)



def concatenate_markdown_files(page_paths: List[str]) -> str:
    concatenated_content = []

    for page_path in sorted(page_paths):
        if os.path.exists(page_path):
            with open(page_path, "r") as f:
                page_content = f.read()
                concatenated_content.append(page_content)
                concatenated_content.append("\n\n---\n\n")

    return "".join(concatenated_content)


def main(url: str = "https://www.google.com", use_llm_cleaning: bool = False, use_batch: bool = False, use_page_cleaning: bool = False):
    log_header(f"Starting crawl for: {url}")

    driver = Chrome()


    base_url = url
    base_name = url_to_name(base_url)

    page_directory = os.path.join(PAGES_DIR, base_name)
    os.makedirs(page_directory, exist_ok=True)

    visited_urls = set([])


    crawl_and_save_pages(driver, base_url, page_directory, visited_urls, index_entry["pages"])

    log_header(f"Crawl complete! Pages found: {len(index_entry['pages'])}")

    # Save index immediately after crawling (before potentially failing LLM step)
    index_entry["visited"] = list(visited_urls)
    index[base_url] = index_entry
    save_index(index)
    log_success("Index saved")

    # INTERMEDIATE PAGE CLEANING STEP (optional)
    if use_page_cleaning:
        log_header("Intermediate Page Cleaning")

        cleaning_metadata = index_entry.get("cleaning_metadata", {})

        if cleaning_metadata.get("pages_cleaned"):
            # Pages already cleaned in a previous run - use cleaned versions
            log_info("Pages already cleaned in previous run")
            cleaned_dir = os.path.join(CLEAN_DIR, base_name)

            if os.path.exists(cleaned_dir):
                cleaned_paths = get_cleaned_page_paths(cleaned_dir)
                if cleaned_paths:
                    index_entry["pages"] = cleaned_paths
                    logging.info(f"  ✓ Using {len(cleaned_paths)} cleaned page(s) from: {cleaned_dir}\n")
                else:
                    logging.warning("  ⚠ No cleaned pages found, using original pages\n")
            else:
                logging.warning("  ⚠ Clean directory not found, using original pages\n")

            cleaned_paths = apply_cleaning_functions(
                index_entry["pages"],
                index_entry["cleaning_metadata"]["cleaning_function"],
                cleaned_dir
            )


        else:
            # First time cleaning - generate and apply cleaning functions
            try:
                # Step 1: Sample pages for analysis
                logging.info("Sampling markdown pages for analysis...")
                sampled_content = sample_pages_for_analysis(index_entry["pages"], sample_percentage=0.05)

                if not sampled_content:
                    logging.warning("  ⚠ No content sampled, skipping page cleaning\n")
                else:
                    # Step 2: Show cost estimate and get user confirmation
                    logging.info("Estimating cost for cleaning function generation...")
                    cost_estimate = estimate_page_cleaning_cost(sampled_content, max_retries=5)

                    log_header("Page Cleaning Cost Estimate", newline_before=True, newline_after=False)
                    logging.info(f"Sample size: {cost_estimate['sample_size_chars']:,} chars ({cost_estimate['estimated_sample_tokens']:,} tokens)")
                    logging.info(f"Max retry attempts: {cost_estimate['max_retries']}")
                    logging.info(f"")
                    logging.info(f"Best case (success on first try):")
                    logging.info(f"  Input tokens:  {cost_estimate['best_case']['input_tokens']:,}")
                    logging.info(f"  Output tokens: {cost_estimate['best_case']['output_tokens']:,}")
                    logging.info(f"  Input cost:    ${cost_estimate['best_case']['input_cost']:.4f}")
                    logging.info(f"  Output cost:   ${cost_estimate['best_case']['output_cost']:.4f}")
                    logging.info(f"  Total cost:    ${cost_estimate['best_case']['total_cost']:.4f}")
                    logging.info(f"")
                    logging.info(f"Worst case (all {cost_estimate['max_retries']} retries needed):")
                    logging.info(f"  Input tokens:  {cost_estimate['worst_case']['input_tokens']:,}")
                    logging.info(f"  Output tokens: {cost_estimate['worst_case']['output_tokens']:,}")
                    logging.info(f"  Input cost:    ${cost_estimate['worst_case']['input_cost']:.4f}")
                    logging.info(f"  Output cost:   ${cost_estimate['worst_case']['output_cost']:.4f}")
                    logging.info(f"  Total cost:    ${cost_estimate['worst_case']['total_cost']:.4f}")
                    logging.info("=" * 60)
                    logging.info("")

                    response = input("Proceed with page cleaning? (y/n): ").lower().strip()

                    if response != 'y':
                        logging.info("Page cleaning skipped by user.\n")
                    else:
                        # Step 3: Generate cleaning function with LLM (with retries)
                        logging.info("\nGenerating custom cleaning functions...")
                        cleaning_code = generate_cleaning_functions(sampled_content, max_retries=5)

                        # Step 4: Apply cleaning functions to all pages
                        logging.info("Applying cleaning functions to pages...")
                        cleaned_dir = os.path.join(CLEAN_DIR, base_name)
                        os.makedirs(cleaned_dir, exist_ok=True)

                        cleaned_paths = apply_cleaning_functions(
                            index_entry["pages"],
                            cleaning_code,
                            cleaned_dir
                        )

                        # Step 5: Store metadata in index for future runs
                        from datetime import datetime
                        index_entry["cleaning_metadata"] = {
                            "cleaning_function": cleaning_code,
                            "cleaned_at": datetime.now().isoformat(),
                            "pages_cleaned": True,
                            "cleaned_page_count": len(cleaned_paths)
                        }

                        # Step 6: Update page paths to use cleaned versions
                        index_entry["pages"] = cleaned_paths

                        # Step 7: Save updated index
                        index[base_url] = index_entry
                        save_index(index)
                        logging.info("  ✓ Index updated with cleaning metadata")
                        logging.info(f"  ✓ Page cleaning complete!\n")

            except Exception as e:
                logging.error(f"\n✗ Page cleaning failed: {e}")
                logging.info("  → Continuing with original (uncleaned) pages\n")
                # Continue with original pages - don't fail the entire process

    logging.info("Concatenating markdown files...")
    concatenated_markdown = concatenate_markdown_files(index_entry["pages"])
    logging.info(f"  ✓ Concatenated {len(index_entry['pages'])} page(s)")

    # Save concatenated (uncleaned) version immediately
    skill_path = os.path.join(SKILLS_DIR, f"{base_name}.md")
    with open(skill_path, "w") as f:
        f.write(concatenated_markdown)
    logging.info(f"  ✓ Pre-cleanup version saved to: {skill_path}")

    # Track if LLM cleaning was applied
    llm_cleaned = False

    if use_llm_cleaning:
        # Show cost estimate and ask for confirmation
        cost_estimate = estimate_llm_cost(concatenated_markdown, use_batch=use_batch)

        log_header("LLM Cleaning Cost Estimate", newline_before=True, newline_after=False)
        logging.info(f"Mode: {cost_estimate['mode']}")
        logging.info(f"Estimated input tokens: {cost_estimate['estimated_input_tokens']:,}")
        logging.info(f"Estimated output tokens: {cost_estimate['estimated_output_tokens']:,}")
        logging.info(f"Estimated input cost: ${cost_estimate['input_cost']:.4f}")
        logging.info(f"Estimated output cost: ${cost_estimate['output_cost']:.4f}")
        logging.info(f"Total estimated cost: ${cost_estimate['total_cost']:.4f}")
        logging.info("=" * 60)
        logging.info("")

        response = input("Proceed with LLM cleaning? (y/n): ").lower().strip()

        if response != 'y':
            logging.info("LLM cleaning skipped. Using pre-cleanup version.\n")
        else:
            logging.info("\nCleaning markdown with LLM...")
            try:
                concatenated_markdown = clean_markdown_with_llm(concatenated_markdown, use_batch=use_batch)
                logging.info("  ✓ LLM cleaning complete")

                # Overwrite with cleaned version
                with open(skill_path, "w") as f:
                    f.write(concatenated_markdown)
                logging.info(f"  ✓ Updated skill file with cleaned version: {skill_path}")
                llm_cleaned = True
            except Exception as e:
                logging.error(f"\n✗ LLM cleaning failed: {e}")
                logging.info(f"Pre-cleanup version is still available at: {skill_path}\n")
                raise

    # Collect statistics for the index
    from datetime import datetime

    # Get skill file statistics
    skill_file_size = os.path.getsize(skill_path) if os.path.exists(skill_path) else 0
    skill_file_lines = 0
    if os.path.exists(skill_path):
        with open(skill_path, "r") as f:
            skill_file_lines = sum(1 for _ in f)

    # Save statistics to index
    index_entry["statistics"] = {
        "last_crawled": datetime.now().isoformat(),
        "skill_file_size_bytes": skill_file_size,
        "skill_file_lines": skill_file_lines,
        "llm_cleaned": llm_cleaned,
        "page_count": len(index_entry["pages"]),
        "url_count": len(index_entry.get("visited", []))
    }

    index[base_url] = index_entry
    save_index(index)
    log_success("Statistics saved to index")

    logging.info(f"\n✓ Final skill file: {skill_path}\n")

    driver.quit()

    return skill_path


if __name__ == "__main__":
    main()
