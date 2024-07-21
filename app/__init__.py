"""Entry point for the application."""

import sys

from app.adapter.logger.activation_condition import is_on_site_packages
from app.adapter.logger.setup_logging import init_logger

if not is_on_site_packages(__file__) and "pytest" not in sys.modules:
    init_logger()
