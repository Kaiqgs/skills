import os


def save_array(array: list, path: str):
    with open(path, "w") as f:
        f.write("\n".join(array))


def load_array(path: str) -> list:
    with open(path, "r") as f:
        return [line.strip() for line in f.readlines()]

def save_set(set: set, path: str):
    with open(path, "w") as f:
        f.write("\n".join(sorted(set)))

def load_set(path: str) -> set:
    if not os.path.exists(path):
        return set()
    with open(path, "r") as f:
        return set(line.strip() for line in f.readlines())
