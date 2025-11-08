import os
import shutil
import logging
from app.url_to_name import url_to_name
from app.folder_structure import PAGES_DIR, SKILLS_DIR, CLEAN_DIR
# from app.index import load_index, save_index
from app.logging_util import log_success


def delete_site(url: str):
    # TODO: update this to use folder_structure, visited, and queue
    return 
    """Delete all traces of a crawled site from index, pages, clean, and skills."""
    base_name = url_to_name(url)

    # Check what exists
    index = load_index()
    index_entry = index.get(url)
    pages_dir = os.path.join(PAGES_DIR, base_name)
    clean_dir = os.path.join(CLEAN_DIR, base_name)
    skill_file = os.path.join(SKILLS_DIR, f"{base_name}.md")

    items_to_delete = []

    if index_entry:
        items_to_delete.append(f"  - Index entry for: {url}")

    if os.path.exists(pages_dir):
        items_to_delete.append(f"  - Pages directory: {pages_dir}")

    if os.path.exists(clean_dir):
        items_to_delete.append(f"  - Clean directory: {clean_dir}")

    if os.path.exists(skill_file):
        items_to_delete.append(f"  - Skill file: {skill_file}")

    if not items_to_delete:
        logging.info(f"Nothing found for URL: {url}")
        return

    # Show what will be deleted
    logging.info(f"The following will be deleted for '{base_name}':")
    for item in items_to_delete:
        logging.info(item)

    # Ask for confirmation
    response = input("\nAre you sure you want to delete these items? (y/n): ").lower().strip()

    if response != 'y':
        logging.info("Deletion cancelled.")
        return

    # Perform deletion
    if index_entry:
        del index[url]
        save_index(index)
        log_success(f"Deleted index entry for: {url}")

    if os.path.exists(pages_dir):
        shutil.rmtree(pages_dir)
        log_success(f"Deleted pages directory: {pages_dir}")

    if os.path.exists(clean_dir):
        shutil.rmtree(clean_dir)
        log_success(f"Deleted clean directory: {clean_dir}")

    if os.path.exists(skill_file):
        os.remove(skill_file)
        log_success(f"Deleted skill file: {skill_file}")

    logging.info("\nDeletion complete!")
