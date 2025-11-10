import os
import shutil
import logging
from app.url_to_name import url_to_name
from app.folder_structure import PAGES_DIR, SKILLS_DIR, CLEAN_DIR, ITERATIONS_DIR, get_iterations_dir
from app.logging_util import log_success
from app.marketplace_manager import remove_skill_from_marketplace


def delete_site(url: str):
    base_name = url_to_name(url)

    pages_dir = os.path.join(PAGES_DIR, base_name)
    clean_dir = os.path.join(CLEAN_DIR, base_name)
    iterations_dir = get_iterations_dir(base_name)
    skill_dir = os.path.join(SKILLS_DIR, base_name)

    items_to_delete = []

    if os.path.exists(pages_dir):
        items_to_delete.append(f"  - Pages directory: {pages_dir}")

    if os.path.exists(clean_dir):
        items_to_delete.append(f"  - Clean directory: {clean_dir}")

    if os.path.exists(iterations_dir):
        items_to_delete.append(f"  - Iterations directory: {iterations_dir}")

    if os.path.exists(skill_dir):
        items_to_delete.append(f"  - Skill directory: {skill_dir}")

    if not items_to_delete:
        logging.info(f"Nothing found for URL: {url}")
        return

    logging.info(f"The following will be deleted for '{base_name}':")
    for item in items_to_delete:
        logging.info(item)

    response = input("\nAre you sure you want to delete these items? (y/n): ").lower().strip()

    if response != 'y':
        logging.info("Deletion cancelled.")
        return

    if os.path.exists(pages_dir):
        shutil.rmtree(pages_dir)
        log_success(f"Deleted pages directory: {pages_dir}")

    if os.path.exists(clean_dir):
        shutil.rmtree(clean_dir)
        log_success(f"Deleted clean directory: {clean_dir}")

    if os.path.exists(iterations_dir):
        shutil.rmtree(iterations_dir)
        log_success(f"Deleted iterations directory: {iterations_dir}")

    if os.path.exists(skill_dir):
        shutil.rmtree(skill_dir)
        log_success(f"Deleted skill directory: {skill_dir}")

    remove_skill_from_marketplace(base_name)

    logging.info("\nDeletion complete!")
