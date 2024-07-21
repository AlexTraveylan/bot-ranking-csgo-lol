"""
Module to setup logging for the application.

:author: Alex Traveylan
:date: 2024
"""

import json
import logging.config
import logging.handlers
from pathlib import Path

from app.core.constants import LOGGER_NAME, LOGGING_CONFIG_PATH

logger = logging.getLogger(LOGGER_NAME)


def setup_logging(config_file_path: Path | str):
    """Setup logging configuration from a JSON file.

    Parameters
    ----------
    config_file_path : Path | str
        Path to the JSON file containing the logging configuration.
    """
    with open(config_file_path, encoding="utf-8") as f_in:
        config = json.load(f_in)

    logging.config.dictConfig(config)


def init_logger():
    """Initialize the logger with the default configuration."""

    setup_logging(LOGGING_CONFIG_PATH)
    logging.basicConfig(level="DEBUG")

    # Example usage
    logger.info("Logger initialized.")
