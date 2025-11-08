import glob
import os

APP_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(APP_DIR)
SKILLS_DIR = os.path.join(ROOT_DIR, "skills")
INTERMEDIATE_DIR = os.path.join(ROOT_DIR, "intermediate")

PAGES_DIR = os.path.join(INTERMEDIATE_DIR, "pages")
CLEAN_DIR = os.path.join(INTERMEDIATE_DIR, "clean")

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


os.makedirs(SKILLS_DIR, exist_ok=True)
os.makedirs(PAGES_DIR, exist_ok=True)
os.makedirs(CLEAN_DIR, exist_ok=True)
