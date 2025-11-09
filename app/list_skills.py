import os
import logging
from datetime import datetime
from app.folder_structure import SKILLS_DIR, PAGES_DIR, CLEAN_DIR, get_pages_filename, get_iterations_dir, SKILL_FILENAME
from app.iteration_manager import load_best_iteration
from app.logging_util import log_centered_header
import app.persist as persist


def list_skills():
    if not os.path.exists(SKILLS_DIR):
        logging.info("No skills found. Run a crawl first!")
        return

    skill_dirs = [d for d in os.listdir(SKILLS_DIR) if os.path.isdir(os.path.join(SKILLS_DIR, d))]

    if not skill_dirs:
        logging.info("No skills found. Run a crawl first!")
        return

    log_centered_header("SKILLMAKER - ALL SKILLS", width=80)

    for idx, base_name in enumerate(sorted(skill_dirs), 1):
        skill_dir = os.path.join(SKILLS_DIR, base_name)
        skill_file = os.path.join(skill_dir, SKILL_FILENAME)
        pages_dir = os.path.join(PAGES_DIR, base_name)
        clean_dir = os.path.join(CLEAN_DIR, base_name)
        iterations_dir = get_iterations_dir(base_name)

        pages_filename = get_pages_filename(pages_dir)
        visited = persist.load_set(pages_filename, set())

        url_count = len(visited)
        page_count = len([f for f in os.listdir(pages_dir) if f.endswith('.md')]) if os.path.exists(pages_dir) else 0

        skill_file_size = 0
        skill_file_lines = 0
        skill_exists = os.path.exists(skill_file)

        if skill_exists:
            skill_file_size = os.path.getsize(skill_file)
            with open(skill_file, 'r') as f:
                skill_file_lines = sum(1 for _ in f)

        if skill_file_size > 1024 * 1024:
            size_str = f"{skill_file_size / (1024 * 1024):.2f} MB"
        elif skill_file_size > 1024:
            size_str = f"{skill_file_size / 1024:.2f} KB"
        else:
            size_str = f"{skill_file_size} bytes"

        best_iteration = load_best_iteration(base_name)
        cleaned = os.path.exists(clean_dir) and best_iteration is not None

        if cleaned:
            quality_score = best_iteration['evaluation']['quality_score']
            cleaning_str = f"Cleaned (quality: {quality_score:.2f})"
        else:
            cleaning_str = "No cleaning"

        logging.info(f"[{idx}] {base_name}")
        logging.info(f"    Pages:        {page_count} files ({url_count} URLs crawled)")
        logging.info(f"    Skill size:   {size_str} ({skill_file_lines:,} lines)")
        logging.info(f"    Cleaning:     {cleaning_str}")

        if skill_exists:
            logging.info(f"    Skill file:   {skill_file}")
        else:
            logging.info(f"    Skill file:   NOT FOUND")

        logging.info("")

    logging.info("=" * 80)
    logging.info(f"Total: {len(skill_dirs)} skill(s)")
    logging.info("=" * 80)
    logging.info("")
