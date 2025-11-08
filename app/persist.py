from collections import deque
import os
from typing import Callable, Iterable, TypeVar, Optional

T = TypeVar('T')


def load(path: str, coerce: Callable[[Iterable], T], default: T | None = None) -> T | None:
    if not os.path.exists(path):
        return default
    with open(path, "r") as f:
        return coerce(line.strip() for line in f.readlines())


def save(iterable: list[str], path: str) -> None:
    with open(path, "w") as f:
        f.write("\n".join(iterable))


def save_array(array: list[str], path: str) -> None:
    """Save an array of strings to a file."""
    with open(path, "w") as f:
        f.write("\n".join(array))


def load_array(path: str, default: list[str] | None = None) -> list[str]:
    """
    Load an array of strings from a file.

    Args:
        path: Path to the file.
        default: Default list to return if file doesn't exist.

    Returns:
        List of strings from the file, or default if file doesn't exist.
    """
    if default is None:
        default = []

    if not os.path.exists(path):
        return default

    with open(path, "r") as f:
        return [line.strip() for line in f.readlines()]


def save_set(set_data: set[str], path: str) -> None:
    """Save a set of strings to a file."""
    with open(path, "w") as f:
        f.write("\n".join(sorted(set_data)))


def load_set(path: str, default: set[str] | None = None) -> set[str]:
    """
    Load a set of strings from a file.

    Args:
        path: Path to the file.
        default: Default set to return if file doesn't exist.

    Returns:
        Set of strings from the file, or default if file doesn't exist.
    """
    if default is None:
        default = set()

    if not os.path.exists(path):
        return default

    with open(path, "r") as f:
        return set(line.strip() for line in f.readlines())


def save_deque(deque_data: deque[str], path: str) -> None:
    """Save a deque of strings to a file."""
    with open(path, "w") as f:
        f.write("\n".join(deque_data))


def load_deque(path: str, default: deque[str] | None = None) -> deque[str]:
    """
    Load a deque of strings from a file.

    Args:
        path: Path to the file.
        default: Default deque to return if file doesn't exist.

    Returns:
        Deque of strings from the file, or default if file doesn't exist.
    """
    if default is None:
        default = deque()

    if not os.path.exists(path):
        return default

    with open(path, "r") as f:
        return deque(line.strip() for line in f.readlines())
