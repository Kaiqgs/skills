import json
import os
from typing import Dict, Any
from app.folder_structure import ROOT_DIR, SKILLS_DIR
from app.logging_util import log_success, log_info, log_warning

CLAUDE_PLUGIN_DIR = os.path.join(ROOT_DIR, ".claude-plugin")
MARKETPLACE_PATH = os.path.join(CLAUDE_PLUGIN_DIR, "marketplace.json")


def load_marketplace_json() -> Dict[str, Any]:
    if not os.path.exists(MARKETPLACE_PATH):
        log_warning(f"marketplace.json not found at {MARKETPLACE_PATH}")
        return None

    with open(MARKETPLACE_PATH, "r") as f:
        return json.load(f)


def save_marketplace_json(data: Dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(MARKETPLACE_PATH), exist_ok=True)

    with open(MARKETPLACE_PATH, "w") as f:
        json.dump(data, f, indent=2)

    log_success(f"Updated marketplace.json")


def get_skill_path(skill_name: str) -> str:
    return f"./skills/{skill_name}"


def add_skill_to_marketplace(skill_name: str) -> None:
    data = load_marketplace_json()

    if not data:
        log_warning("Could not update marketplace.json - file not found")
        return

    skill_path = get_skill_path(skill_name)

    crawled_docs_plugin = None
    for plugin in data.get("plugins", []):
        if plugin.get("name") == "crawled-docs":
            crawled_docs_plugin = plugin
            break

    if not crawled_docs_plugin:
        log_warning("crawled-docs plugin not found in marketplace.json")
        return

    existing_skills = crawled_docs_plugin.get("skills", [])

    if skill_path in existing_skills:
        log_info(f"Skill already in marketplace.json: {skill_path}")
        return

    existing_skills.append(skill_path)
    crawled_docs_plugin["skills"] = sorted(existing_skills)

    save_marketplace_json(data)
    log_success(f"Added skill to marketplace.json: {skill_path}")


def remove_skill_from_marketplace(skill_name: str) -> None:
    data = load_marketplace_json()

    if not data:
        log_warning("Could not update marketplace.json - file not found")
        return

    skill_path = get_skill_path(skill_name)

    crawled_docs_plugin = None
    for plugin in data.get("plugins", []):
        if plugin.get("name") == "crawled-docs":
            crawled_docs_plugin = plugin
            break

    if not crawled_docs_plugin:
        log_warning("crawled-docs plugin not found in marketplace.json")
        return

    existing_skills = crawled_docs_plugin.get("skills", [])

    if skill_path not in existing_skills:
        log_info(f"Skill not in marketplace.json: {skill_path}")
        return

    existing_skills.remove(skill_path)
    crawled_docs_plugin["skills"] = sorted(existing_skills)

    save_marketplace_json(data)
    log_success(f"Removed skill from marketplace.json: {skill_path}")
