"""Centralized logging setup for ENGTools."""

import logging
import sys
from pathlib import Path


def setup_logging() -> None:
    """Configure logging to stdout and engtools.log in the working directory."""
    root_logger = logging.getLogger()

    if getattr(setup_logging, "_configured", False):
        return

    formatter = logging.Formatter(
        fmt="[%(levelname)s] %(asctime)s — %(message)s",
        datefmt="%H:%M:%S",
    )

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(Path.cwd() / "engtools.log", encoding="utf-8")
    file_handler.setFormatter(formatter)

    root_logger.setLevel(logging.INFO)
    root_logger.handlers.clear()
    root_logger.addHandler(stream_handler)
    root_logger.addHandler(file_handler)

    setattr(setup_logging, "_configured", True)
