# -*- coding: utf-8 -*-
import logging
from typing import Optional


def log_header(title: str, width: int = 60, newline_before: bool = True, newline_after: bool = True):
    """
    Print a formatted header with a title.

    Args:
        title: The text to display in the header
        width: Width of the header separator (default 60)
        newline_before: Add newline before header (default True)
        newline_after: Add newline after header (default True)
    """
    if newline_before:
        logging.info("")
    logging.info("=" * width)
    logging.info(title)
    logging.info("=" * width)
    if newline_after:
        logging.info("")


def log_section(title: str, width: int = 60):
    """
    Print a section header (header without extra newlines).

    Args:
        title: The section title
        width: Width of the separator (default 60)
    """
    log_header(title, width=width, newline_before=False, newline_after=False)


def log_centered_header(title: str, width: int = 80):
    """
    Print a centered header with title.

    Args:
        title: The text to center
        width: Total width of the header (default 80)
    """
    logging.info("")
    logging.info("=" * width)
    logging.info(f"{title:^{width}}")
    logging.info("=" * width)
    logging.info("")


def log_cost_estimate(title: str, items: dict, width: int = 60):
    """
    Print a formatted cost estimate section.

    Args:
        title: Title of the cost estimate
        items: Dictionary of items to display
        width: Width of the separator (default 60)
    """
    logging.info("")
    logging.info("=" * width)
    logging.info(title)
    logging.info("=" * width)
    for key, value in items.items():
        logging.info(f"{key}: {value}")
    logging.info("=" * width)
    logging.info("")


def log_info(message: str, prefix: str = "->"):
    """
    Log an info message with a prefix.

    Args:
        message: The message to log
        prefix: Prefix symbol (default "->")
    """
    logging.info(f"  {prefix} {message}")


def log_success(message: str):
    """Log a success message with checkmark."""
    logging.info(f"  ✓ {message}")


def log_warning(message: str):
    """Log a warning message with warning symbol."""
    logging.warning(f"  ⚠ {message}")


def log_error(message: str):
    """Log an error message with X symbol."""
    logging.error(f"  ✗ {message}")
