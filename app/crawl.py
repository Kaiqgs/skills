from collections import deque
import os
import time
import logging
from typing import  Set, List 
from urllib.parse import urlparse, urlunparse
from selenium.webdriver import Chrome
import markdownify
from selenium.webdriver.common.by import By

import app.folder_structure as folder_structure
import app.persist as persist
from app.folder_structure import PAGES_DIR, SKILLS_DIR, CLEAN_DIR, get_all_pages
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


def crawl_and_save_pages(driver: Chrome, base_url: str, page_directory: str, visited: Set[str], queue: set[str]) -> tuple[Set[str], set[str]]:

    while queue:
        current_url = queue.pop()
        current_url_no_fragment = strip_url_fragment(current_url)

        if current_url_no_fragment in visited:
            continue

        visited.add(current_url_no_fragment)

        logging.info(f"[{len(queue)} left] Crawling: {current_url_no_fragment}")

        driver.get(current_url)
        time.sleep(2)

        html_content = driver.page_source
        markdown_content = markdownify.markdownify(html_content)

        page_name = url_to_name(current_url_no_fragment)
        page_path = folder_structure.get_pages_filename
        page_path = os.path.join(page_directory, f"{page_name}.md")

        with open(page_path, "w") as f:
            f.write(markdown_content)
        persist.save_set(visited, folder_structure.get_pages_filename(page_directory))
        persist.save_set(queue, folder_structure.get_queue_filename(page_directory))
        logging.info(f"  ✓ Saved to: {page_name}.md")

        all_links = [a.get_attribute("href") for a in driver.find_elements(By.TAG_NAME, "a")]
        same_domain_links = [link for link in all_links if link and base_url in link]
        same_domain_links_no_fragment = set([strip_url_fragment(link) for link in same_domain_links])
        
        url_count_before_update = len(queue)
        queue.update(same_domain_links_no_fragment - visited)

        new_next_url_count = len(queue) - url_count_before_update

        if new_next_url_count > 0:
            logging.info(f"  → Found {new_next_url_count} new URLs(s)")

    return visited, queue



def concatenate_markdown_files(page_paths: List[str]) -> str:
    concatenated_content = []

    for page_path in sorted(page_paths):
        if os.path.exists(page_path):
            with open(page_path, "r") as f:
                page_content = f.read()
                concatenated_content.append(page_content)
                concatenated_content.append("\n\n---\n\n")

    return "".join(concatenated_content)


def crawl(url: str = "https://www.google.com", clean=False):
    log_header(f"Starting crawl for: {url}")

    driver = Chrome()


    base_url = url
    base_name = url_to_name(base_url)

    
    page_directory = os.path.join(PAGES_DIR, base_name)

    os.makedirs(page_directory, exist_ok=True)

    visited_urls = persist.load_set(folder_structure.get_pages_filename(page_directory))
    queue_urls = persist.load_set(folder_structure.get_queue_filename(page_directory), set([base_url]))


    try:
        visited_urls, queue_urls = crawl_and_save_pages(driver, base_url, page_directory, visited_urls, queue_urls)
    except KeyboardInterrupt:
        logging.info("Keyboard interrupt detected, exiting...")
        return

    log_header(f"Crawl complete! Pages found: {len(visited_urls)}")
    log_success("Index saved")

    driver.quit()

    if clean:
        clean_dir = os.path.join(PAGES_DIR, "clean")
        os.makedirs(clean_dir, exist_ok=True)
        sample = sample_pages_for_analysis(page_directory)
        with open("sample.md", "w") as f:
            f.write(sample)


        cleaning_function = generate_cleaning_functions(sample)





if __name__ == "__main__":
    crawl()
