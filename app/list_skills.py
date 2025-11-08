import os
import logging
from datetime import datetime
from app.folder_structure import SKILLS_DIR
from app.logging_util import log_centered_header


def list_skills():
     # TODO: update this to use folder_structure, visited, and queue
    return
    """List all crawled skills with statistics."""
    index = load_index()

    if not index:
        logging.info("No skills found. Run a crawl first!")
        return

    log_centered_header("SKILLMAKER - ALL SKILLS", width=80)

    # Sort by last crawled (most recent first)
    sorted_entries = sorted(
        index.items(),
        key=lambda x: x[1].get('statistics', {}).get('last_crawled', ''),
        reverse=True
    )

    for idx, (url, entry) in enumerate(sorted_entries, 1):
        base_name = entry.get('base_name', 'unknown')
        stats = entry.get('statistics', {})

        # Get basic info
        page_count = len(entry.get('pages', []))
        url_count = len(entry.get('visited', []))

        # Get statistics
        last_crawled = stats.get('last_crawled', 'Never')
        skill_file_size = stats.get('skill_file_size_bytes', 0)
        skill_file_lines = stats.get('skill_file_lines', 0)
        page_cleaned = entry.get('cleaning_metadata', {}).get('pages_cleaned', False)
        llm_cleaned = stats.get('llm_cleaned', False)

        # Format last crawled time
        if last_crawled != 'Never':
            try:
                dt = datetime.fromisoformat(last_crawled)
                last_crawled = dt.strftime('%Y-%m-%d %H:%M')
            except:
                pass

        # Format file size
        if skill_file_size > 1024 * 1024:
            size_str = f"{skill_file_size / (1024 * 1024):.2f} MB"
        elif skill_file_size > 1024:
            size_str = f"{skill_file_size / 1024:.2f} KB"
        else:
            size_str = f"{skill_file_size} bytes"

        # Cleaning status
        cleaning_status = []
        if page_cleaned:
            cleaning_status.append("Page-cleaned")
        if llm_cleaned:
            cleaning_status.append("LLM-cleaned")
        cleaning_str = ", ".join(cleaning_status) if cleaning_status else "No cleaning"

        # Print skill info
        logging.info(f"[{idx}] {base_name}")
        logging.info(f"    URL:          {url}")
        logging.info(f"    Pages:        {page_count} files ({url_count} URLs crawled)")
        logging.info(f"    Skill size:   {size_str} ({skill_file_lines:,} lines)")
        logging.info(f"    Last crawled: {last_crawled}")
        logging.info(f"    Cleaning:     {cleaning_str}")

        # Show skill file path
        skill_file = os.path.join(SKILLS_DIR, f"{base_name}.md")
        if os.path.exists(skill_file):
            logging.info(f"    Skill file:   {skill_file}")
        else:
            logging.info(f"    Skill file:   NOT FOUND")

        logging.info("")

    logging.info("=" * 80)
    logging.info(f"Total: {len(index)} skill(s)")
    logging.info("=" * 80)
    logging.info("")
