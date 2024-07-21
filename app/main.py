"""
Main module for the application
"""

import logging
from atexit import register

from app.core.constants import LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)


def main():
    """Entry point for the application."""

    logger.info("Application started.")


@register
def exit_function():
    """Auto execute when application end"""

    logger.info("application ended")


if __name__ == "__main__":
    main()
