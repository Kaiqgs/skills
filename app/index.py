import json
from app.folder_structure import SKILLS_INDEX

_index = None
def load_index() -> dict:

    global _index

    if _index is not None:
        return _index

    try:
        with open(SKILLS_INDEX, "r") as f:
            _index = json.load(f)
            return _index
    except FileNotFoundError:
        _index = {}
        return _index

def save_index(index: dict):
    global _index
    _index = index

    with open(SKILLS_INDEX, "w") as f:
        json.dump(index, f)
