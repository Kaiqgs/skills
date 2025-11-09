import glob
import os

APP_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(APP_DIR)
SKILLS_DIR = os.path.join(ROOT_DIR, "skills")
INTERMEDIATE_DIR = os.path.join(ROOT_DIR, "intermediate")

PAGES_DIR = os.path.join(INTERMEDIATE_DIR, "pages")
CLEAN_DIR = os.path.join(INTERMEDIATE_DIR, "clean")
ITERATIONS_DIR = os.path.join(INTERMEDIATE_DIR, "iterations")

SKILLS_SCRIPTS_DIRNAME  = "scripts"
SKILLS_REFERENCES_DIRNAME  = "references"
SKILLS_ASSETS_DIRNAME  = "assets"

SKILL_FILENAME = "SKILL.md"
PAGES_FILENAME = "pages.txt"
QUEUE_FILENAME = "queue.txt"
CLEANING_FUNCTION_FILENAME = "cleaning_functions.py"

def get_pages_filename(pages_dir: str) -> str:
    return os.path.join(pages_dir, PAGES_FILENAME)

def get_queue_filename(pages_dir: str) -> str:
    return os.path.join(pages_dir, QUEUE_FILENAME)

def get_cleaning_function_filename(clean_dir: str) -> str:
    return  os.path.join(clean_dir, CLEANING_FUNCTION_FILENAME)

def get_all_pages(pages_dir: str) -> list[str]:
    return list(glob.glob(os.path.join(pages_dir, "*.md")))

def get_iterations_dir(base_name: str) -> str:
    return os.path.join(ITERATIONS_DIR, base_name)

def get_iteration_dir(base_name: str, iteration_num: int) -> str:
    return os.path.join(ITERATIONS_DIR, base_name, f"iteration_{iteration_num}")

def get_best_iteration_dir(base_name: str) -> str:
    return os.path.join(ITERATIONS_DIR, base_name, "best")

def make_skill_dir(base_name: str) -> dict:
    os.makedirs(SKILLS_DIR, exist_ok=True)
    skill_dir = os.path.join(SKILLS_DIR, base_name)
    references_dir = os.path.join(skill_dir, SKILLS_REFERENCES_DIRNAME)
    scripts_dir = os.path.join(skill_dir, SKILLS_SCRIPTS_DIRNAME)
    assets_dir = os.path.join(skill_dir, SKILLS_ASSETS_DIRNAME)
    os.makedirs(skill_dir, exist_ok=True)
    os.makedirs(references_dir, exist_ok=True)
    os.makedirs(scripts_dir, exist_ok=True)
    os.makedirs(assets_dir, exist_ok=True)

    return {
        "skill_file": os.path.join(skill_dir, SKILL_FILENAME),
        "references_dir": references_dir,
        "scripts_dir": scripts_dir,
        "assets_dir": assets_dir
    }

os.makedirs(SKILLS_DIR, exist_ok=True)
os.makedirs(PAGES_DIR, exist_ok=True)
os.makedirs(CLEAN_DIR, exist_ok=True)
os.makedirs(ITERATIONS_DIR, exist_ok=True)
