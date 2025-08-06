"""Logging configuration module."""
from __future__ import annotations

import logging
import sys
from typing import Any

from .config import settings


def configure_logging() -> None:
    """Configure root logger with JSON formatted output."""
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        '{"time": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s", "name": "%(name)s"}'
    )
    handler.setFormatter(formatter)
    logging.basicConfig(level=settings.log_level, handlers=[handler])


def get_logger(name: str) -> logging.Logger:
    """Return a module-specific logger."""
    return logging.getLogger(name)
