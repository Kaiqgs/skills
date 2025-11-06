import os
import time
import logging
from typing import Set, List, Optional
from urllib.parse import urlparse, urlunparse
from selenium.webdriver import Chrome
import markdownify
from selenium.webdriver.common.by import By

from app.folder_structure import PAGES_DIR, SKILLS_DIR
from app.url_to_name import url_to_name
from app.index import load_index, save_index
from app.markdown_llm import clean_markdown_with_llm, estimate_llm_cost

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


def main(url: str = "https://www.google.com", use_llm_cleaning: bool = False, use_batch: bool = False):
    logging.info(f"\n{'='*60}")
    logging.info(f"Starting crawl for: {url}")
    logging.info(f"{'='*60}\n")

    driver = Chrome()

    index = load_index()

    base_url = url
    base_name = url_to_name(base_url)

    page_directory = os.path.join(PAGES_DIR, base_name)
    os.makedirs(page_directory, exist_ok=True)

    index_entry = index.get(base_url, {
        "base_url": base_url,
        "base_name": base_name,
        "visited": [],
        "pages": []
    })

    visited_urls = set(index_entry.get("visited", []))

    crawl_and_save_pages(driver, base_url, page_directory, visited_urls, index_entry["pages"])

    logging.info(f"\n{'='*60}")
    logging.info(f"Crawl complete! Pages found: {len(index_entry['pages'])}")
    logging.info(f"{'='*60}\n")

    # Save index immediately after crawling (before potentially failing LLM step)
    index_entry["visited"] = list(visited_urls)
    index[base_url] = index_entry
    save_index(index)
    logging.info("  ✓ Index saved")

    logging.info("Concatenating markdown files...")
    concatenated_markdown = concatenate_markdown_files(index_entry["pages"])
    logging.info(f"  ✓ Concatenated {len(index_entry['pages'])} page(s)")

    # Save concatenated (uncleaned) version immediately
    skill_path = os.path.join(SKILLS_DIR, f"{base_name}.md")
    with open(skill_path, "w") as f:
        f.write(concatenated_markdown)
    logging.info(f"  ✓ Pre-cleanup version saved to: {skill_path}")

    if use_llm_cleaning:
        # Show cost estimate and ask for confirmation
        cost_estimate = estimate_llm_cost(concatenated_markdown, use_batch=use_batch)

        logging.info(f"\n{'='*60}")
        logging.info("LLM Cleaning Cost Estimate")
        logging.info(f"{'='*60}")
        logging.info(f"Mode: {cost_estimate['mode']}")
        logging.info(f"Estimated input tokens: {cost_estimate['estimated_input_tokens']:,}")
        logging.info(f"Estimated output tokens: {cost_estimate['estimated_output_tokens']:,}")
        logging.info(f"Estimated input cost: ${cost_estimate['input_cost']:.4f}")
        logging.info(f"Estimated output cost: ${cost_estimate['output_cost']:.4f}")
        logging.info(f"Total estimated cost: ${cost_estimate['total_cost']:.4f}")
        logging.info(f"{'='*60}\n")

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
            except Exception as e:
                logging.error(f"\n✗ LLM cleaning failed: {e}")
                logging.info(f"Pre-cleanup version is still available at: {skill_path}\n")
                raise

    logging.info(f"\n✓ Final skill file: {skill_path}\n")

    driver.quit()

    return skill_path


if __name__ == "__main__":
    main()
