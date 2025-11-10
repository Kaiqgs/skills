from collections import deque
import os
import time
import logging
import app.anthropic as app_anthropic
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
from app.marketplace_manager import add_skill_to_marketplace
from app.skill_validator import validate_skill

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



def copy_pages_to_references(page_paths: List[str], references_dir: str) -> List[str]:
    copied_files = []

    for page_path in sorted(page_paths):
        if os.path.exists(page_path):
            filename = os.path.basename(page_path)
            dest_path = os.path.join(references_dir, filename)

            with open(page_path, "r") as src:
                content = src.read()

            with open(dest_path, "w") as dst:
                dst.write(content)

            copied_files.append(dest_path)
            logging.info(f"  → Copied {filename}")

    return copied_files


def concatenate_markdown_files(page_paths: List[str]) -> str:
    concatenated_content = []

    for page_path in sorted(page_paths):
        if os.path.exists(page_path):
            with open(page_path, "r") as f:
                page_content = f.read()
                concatenated_content.append(page_content)
                concatenated_content.append("\n\n---\n\n")

    return "".join(concatenated_content)


def build_skill_md_prompt(sampled_content: str, skill_name: str, reference_files: List[str]) -> str:
    reference_list = "\n".join([f"- references/{os.path.basename(f)}" for f in sorted(reference_files)])

    skill_creator_path = os.path.join(os.path.dirname(__file__), "skill-creator", "SKILL.md")
    with open(skill_creator_path, "r") as f:
        skill_creator_guide = f.read()

    return f"""You are creating a SKILL.md file for a Claude Code skill based on documentation that has been crawled and cleaned.

The skill name is: {skill_name}

IMPORTANT: The following {len(reference_files)} reference files are available in the references/ directory.
You MUST reference ALL of these files in the SKILL.md using the format `references/filename.md`:
{reference_list}

Here is the skill-creator guide that explains what makes an effective skill:

<skill_creator_guide>
{skill_creator_guide}
</skill_creator_guide>

Here is a representative sample of the documentation content:

{sampled_content}

Generate a complete SKILL.md file following these requirements from the skill-creator guidelines:

1. **YAML Frontmatter** (required, at the very start of the file):
   ---
   name: {skill_name}
   description: Third-person description specifying WHEN to use this skill (be specific about scenarios, tasks, or contexts that should trigger it)
   ---

2. **Overview Section**: 1-2 sentences explaining what this skill enables

3. **Main Content**: Choose appropriate structure (workflow-based, task-based, or capabilities-based)
   - Use imperative/infinitive form (verb-first instructions), NOT second person
   - Reference ALL {len(reference_files)} documentation files from the references/ directory
   - Use the format `references/filename.md` when referencing files
   - For files >10k words, include grep search patterns to help find specific topics
   - Include concrete examples of how to use the skill
   - Organize references by topic/workflow to make them discoverable

4. **Writing Style**:
   - Objective, instructional language (e.g., "To accomplish X, do Y")
   - No second person ("you should")
   - Imperative/infinitive form throughout

5. **Progressive Disclosure**:
   - Keep SKILL.md lean and focused on workflow guidance
   - Detailed reference material stays in references/ files
   - Guide when to load which reference files

IMPORTANT: Return ONLY the complete SKILL.md content with proper YAML frontmatter. Do not include any explanations or conversational text. Your entire response will be saved directly as the SKILL.md file."""


def generate_skill_md(skill_name: str, reference_files: List[str], page_directory: str) -> tuple[str, dict]:
    from anthropic import Anthropic
    from app.markdown_llm import get_anthropic_client, MODEL

    log_header("Generating SKILL.md with LLM")

    sampled_content = sample_pages_for_analysis(page_directory, target_tokens=50000)

    log_info(f"Sampled {len(sampled_content):,} characters for analysis")

    client = get_anthropic_client()
    prompt = build_skill_md_prompt(sampled_content, skill_name, reference_files)

    token_count = client.messages.count_tokens(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}]
    )

    estimated_input_tokens = token_count.input_tokens
    estimated_output_tokens = app_anthropic.MAX_OUTPUT_TOKENS

    input_cost = (estimated_input_tokens / 1_000_000) * 3.00
    output_cost = (estimated_output_tokens / 1_000_000) * 15.00
    total_cost = input_cost + output_cost

    log_info(f"Estimated cost: ${total_cost:.4f} ({estimated_input_tokens:,} input + ~{estimated_output_tokens:,} output tokens)")

    message = client.messages.create(
        model=MODEL,
        max_tokens=app_anthropic.MAX_OUTPUT_TOKENS,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    skill_md_content = message.content[0].text

    usage = {
        "input_tokens": message.usage.input_tokens,
        "output_tokens": message.usage.output_tokens,
        "total_cost": (message.usage.input_tokens / 1_000_000) * 3.00 + (message.usage.output_tokens / 1_000_000) * 15.00
    }

    log_success(f"Generated SKILL.md ({message.usage.output_tokens:,} tokens, ${usage['total_cost']:.4f})")

    return skill_md_content, usage


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

    from app.iteration_manager import load_best_iteration
    best_iteration = load_best_iteration(base_name)

    if clean and not best_iteration:
        from app.cleaning_refiner import iterative_cleaning_generation

        log_header("Starting iterative page cleaning")

        sampled_content = sample_pages_for_analysis(page_directory)

        log_info(f"Sampled content size: {len(sampled_content):,} characters")

        result = iterative_cleaning_generation(
            sampled_content=sampled_content,
            base_name=base_name,
            smooth_max_iterations=5,
            error_max_iterations=7
        )

        best_code = result["best_iteration"]["cleaning_code"]

        clean_dir = os.path.join(CLEAN_DIR, base_name)
        os.makedirs(clean_dir, exist_ok=True)

        cleaning_function_path = folder_structure.get_cleaning_function_filename(clean_dir)
        with open(cleaning_function_path, "w") as f:
            f.write(best_code)

        log_success(f"Best quality score: {result['best_quality_score']:.2f}")
        log_success(f"Total iterations: {len(result['iterations'])}")
        log_success(f"Best iteration: #{result['best_iteration']['iteration_num']}")

        page_paths = folder_structure.get_all_pages(page_directory)
        cleaned_paths = apply_cleaning_functions(page_paths, best_code, clean_dir)

        log_success(f"Cleaned {len(cleaned_paths)} pages")

        pages_to_concatenate = cleaned_paths
    elif clean and best_iteration:
        log_header("Using existing best iteration for cleaning")

        best_code = best_iteration["cleaning_code"]

        clean_dir = os.path.join(CLEAN_DIR, base_name)
        os.makedirs(clean_dir, exist_ok=True)

        log_success(f"Best quality score: {best_iteration['evaluation']['quality_score']:.2f}")
        log_success(f"Best iteration: #{best_iteration['iteration_num']}")

        page_paths = folder_structure.get_all_pages(page_directory)
        cleaned_paths = apply_cleaning_functions(page_paths, best_code, clean_dir)

        log_success(f"Cleaned {len(cleaned_paths)} pages")

        pages_to_concatenate = cleaned_paths
    else:
        pages_to_concatenate = folder_structure.get_all_pages(page_directory)



    skill_paths = folder_structure.make_skill_dir(base_name)
    skill_file = skill_paths["skill_file"]
    references_dir = skill_paths["references_dir"]
    scripts_dir = skill_paths["scripts_dir"]
    assets_dir = skill_paths["assets_dir"]

    log_header("Creating skill structure")

    log_info(f"Copying {len(pages_to_concatenate)} pages to references/")
    reference_files = copy_pages_to_references(pages_to_concatenate, references_dir)
    log_success(f"Copied {len(reference_files)} reference files")

    skill_md_content, usage = generate_skill_md(base_name, reference_files, page_directory)

    with open(skill_file, "w") as f:
        f.write(skill_md_content)

    log_success(f"Skill created at: {skill_file}")
    log_info(f"References: {len(reference_files)} files in {references_dir}")
    log_info(f"Total tokens: {usage['input_tokens']:,} input + {usage['output_tokens']:,} output = ${usage['total_cost']:.4f}")

    is_valid, validation_message = validate_skill(skill_file)
    if is_valid:
        log_success(f"Validation passed: {validation_message}")
    else:
        log_warning(f"Validation failed: {validation_message}")

    add_skill_to_marketplace(base_name)





if __name__ == "__main__":
    crawl()
