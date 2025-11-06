
import os

APP_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(APP_DIR)
SKILLS_DIR = os.path.join(ROOT_DIR, "skills")
PAGES_DIR = os.path.join(ROOT_DIR, "pages")

SKILLS_INDEX = os.path.join(PAGES_DIR, "index.json")

os.makedirs(SKILLS_DIR, exist_ok=True)
os.makedirs(PAGES_DIR, exist_ok=True)
