
import os

APP_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(APP_DIR)
SKILLS_DIR = os.path.join(ROOT_DIR, "skills")
INTERMEDIATE_DIR = os.path.join(ROOT_DIR, "intermediate")

PAGES_DIR = os.path.join(INTERMEDIATE_DIR, "pages")
CLEAN_DIR = os.path.join(INTERMEDIATE_DIR, "clean")

PAGES_FILENAME = "pages.txt"
TO_VISIT_FILENAME = "to_visit.txt"
CLEANING_FUNCTION_FILENAME = "cleaning_function.py"

def get_pages_filename(base_name: str) -> str:
    return os.path.join(PAGES_DIR, os.path.join(base_name, PAGES_FILENAME))

def get_to_visit_filename(base_name: str) -> str:
    return os.path.join(PAGES_DIR, os.path.join(base_name, TO_VISIT_FILENAME))

def get_cleaning_function_filename(base_name: str) -> str:
    return os.path.join(CLEAN_DIR, os.path.join(base_name, CLEANING_FUNCTION_FILENAME))



os.makedirs(SKILLS_DIR, exist_ok=True)
os.makedirs(PAGES_DIR, exist_ok=True)
os.makedirs(CLEAN_DIR, exist_ok=True)
