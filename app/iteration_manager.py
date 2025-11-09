import json
import os
import shutil
from datetime import datetime
from typing import Dict, List
from app.folder_structure import get_iteration_dir, get_best_iteration_dir, get_iterations_dir


def save_iteration(base_name: str, iteration_num: int, iteration_data: Dict) -> None:
    iteration_dir = get_iteration_dir(base_name, iteration_num)
    os.makedirs(iteration_dir, exist_ok=True)

    with open(os.path.join(iteration_dir, "SAMPLE_BEFORE.md"), "w") as f:
        f.write(iteration_data["sample_before"])

    with open(os.path.join(iteration_dir, "SAMPLE_AFTER.md"), "w") as f:
        f.write(iteration_data["sample_after"])

    with open(os.path.join(iteration_dir, "cleaning_functions.py"), "w") as f:
        f.write(iteration_data["cleaning_code"])

    with open(os.path.join(iteration_dir, "evaluation.json"), "w") as f:
        json.dump(iteration_data["evaluation"], f, indent=2)

    code_tokens = iteration_data.get("code_generation_tokens", {})
    eval_tokens = iteration_data["evaluation"].get("token_usage", {})
    total_tokens = iteration_data.get("total_tokens", {})

    metadata_lines = [
        f"iteration_num: {iteration_num}",
        f"timestamp: {datetime.now().isoformat()}",
        f"code_generation_input_tokens: {code_tokens.get('input_tokens', 0)}",
        f"code_generation_output_tokens: {code_tokens.get('output_tokens', 0)}",
        f"evaluation_input_tokens: {eval_tokens.get('input_tokens', 0)}",
        f"evaluation_output_tokens: {eval_tokens.get('output_tokens', 0)}",
        f"total_input_tokens: {total_tokens.get('input_tokens', 0)}",
        f"total_output_tokens: {total_tokens.get('output_tokens', 0)}"
    ]

    with open(os.path.join(iteration_dir, "metadata.txt"), "w") as f:
        f.write("\n".join(metadata_lines))


def load_iteration(base_name: str, iteration_num: int) -> Dict | None:
    iteration_dir = get_iteration_dir(base_name, iteration_num)

    if not os.path.exists(iteration_dir):
        return None

    with open(os.path.join(iteration_dir, "SAMPLE_BEFORE.md"), "r") as f:
        sample_before = f.read()

    with open(os.path.join(iteration_dir, "SAMPLE_AFTER.md"), "r") as f:
        sample_after = f.read()

    with open(os.path.join(iteration_dir, "cleaning_functions.py"), "r") as f:
        cleaning_code = f.read()

    with open(os.path.join(iteration_dir, "evaluation.json"), "r") as f:
        evaluation = json.load(f)

    metadata = {}
    with open(os.path.join(iteration_dir, "metadata.txt"), "r") as f:
        for line in f:
            if ": " in line:
                key, value = line.strip().split(": ", 1)
                if key == "timestamp":
                    metadata[key] = value
                else:
                    metadata[key] = int(value)

    return {
        "iteration_num": metadata.get("iteration_num", iteration_num),
        "timestamp": metadata.get("timestamp"),
        "cleaning_code": cleaning_code,
        "sample_before": sample_before,
        "sample_after": sample_after,
        "evaluation": evaluation,
        "code_generation_tokens": {
            "input_tokens": metadata.get("code_generation_input_tokens", 0),
            "output_tokens": metadata.get("code_generation_output_tokens", 0)
        },
        "total_tokens": {
            "input_tokens": metadata.get("total_input_tokens", 0),
            "output_tokens": metadata.get("total_output_tokens", 0)
        }
    }


def load_iterations(base_name: str) -> List[Dict]:
    iterations_dir = get_iterations_dir(base_name)

    if not os.path.exists(iterations_dir):
        return []

    iterations = []
    iteration_folders = sorted([
        d for d in os.listdir(iterations_dir)
        if d.startswith("iteration_") and os.path.isdir(os.path.join(iterations_dir, d))
    ])

    for folder in iteration_folders:
        iteration_num = int(folder.replace("iteration_", ""))
        iteration_data = load_iteration(base_name, iteration_num)
        if iteration_data:
            iterations.append(iteration_data)

    return iterations


def save_best_iteration(base_name: str, best_iteration_data: Dict) -> None:
    best_dir = get_best_iteration_dir(base_name)

    if os.path.exists(best_dir):
        shutil.rmtree(best_dir)

    os.makedirs(best_dir, exist_ok=True)

    with open(os.path.join(best_dir, "SAMPLE_BEFORE.md"), "w") as f:
        f.write(best_iteration_data["sample_before"])

    with open(os.path.join(best_dir, "SAMPLE_AFTER.md"), "w") as f:
        f.write(best_iteration_data["sample_after"])

    with open(os.path.join(best_dir, "cleaning_functions.py"), "w") as f:
        f.write(best_iteration_data["cleaning_code"])

    with open(os.path.join(best_dir, "evaluation.json"), "w") as f:
        json.dump(best_iteration_data["evaluation"], f, indent=2)

    code_tokens = best_iteration_data.get("code_generation_tokens", {})
    eval_tokens = best_iteration_data["evaluation"].get("token_usage", {})
    total_tokens = best_iteration_data.get("total_tokens", {})

    metadata_lines = [
        f"iteration_num: {best_iteration_data.get('iteration_num', 0)}",
        f"timestamp: {best_iteration_data.get('timestamp', datetime.now().isoformat())}",
        f"code_generation_input_tokens: {code_tokens.get('input_tokens', 0)}",
        f"code_generation_output_tokens: {code_tokens.get('output_tokens', 0)}",
        f"evaluation_input_tokens: {eval_tokens.get('input_tokens', 0)}",
        f"evaluation_output_tokens: {eval_tokens.get('output_tokens', 0)}",
        f"total_input_tokens: {total_tokens.get('input_tokens', 0)}",
        f"total_output_tokens: {total_tokens.get('output_tokens', 0)}"
    ]

    with open(os.path.join(best_dir, "metadata.txt"), "w") as f:
        f.write("\n".join(metadata_lines))


def load_best_iteration(base_name: str) -> Dict | None:
    best_dir = get_best_iteration_dir(base_name)

    if not os.path.exists(best_dir):
        return None

    with open(os.path.join(best_dir, "SAMPLE_BEFORE.md"), "r") as f:
        sample_before = f.read()

    with open(os.path.join(best_dir, "SAMPLE_AFTER.md"), "r") as f:
        sample_after = f.read()

    with open(os.path.join(best_dir, "cleaning_functions.py"), "r") as f:
        cleaning_code = f.read()

    with open(os.path.join(best_dir, "evaluation.json"), "r") as f:
        evaluation = json.load(f)

    metadata = {}
    with open(os.path.join(best_dir, "metadata.txt"), "r") as f:
        for line in f:
            if ": " in line:
                key, value = line.strip().split(": ", 1)
                if key == "timestamp":
                    metadata[key] = value
                else:
                    metadata[key] = int(value)

    return {
        "iteration_num": metadata.get("iteration_num", 0),
        "timestamp": metadata.get("timestamp"),
        "cleaning_code": cleaning_code,
        "sample_before": sample_before,
        "sample_after": sample_after,
        "evaluation": evaluation,
        "code_generation_tokens": {
            "input_tokens": metadata.get("code_generation_input_tokens", 0),
            "output_tokens": metadata.get("code_generation_output_tokens", 0)
        },
        "total_tokens": {
            "input_tokens": metadata.get("total_input_tokens", 0),
            "output_tokens": metadata.get("total_output_tokens", 0)
        }
    }
