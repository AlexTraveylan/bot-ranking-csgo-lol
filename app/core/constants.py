"""
This module contains the configuration for the app

:author: Alex Traveylan
:date: 2024
"""

from pathlib import Path

# Paths of the application

WORKSPACE_DIR = Path(__file__).parents[2].absolute()

APP_DIR = WORKSPACE_DIR / "app"

ADAPTERS_DIR = APP_DIR / "adapter"

CORE_DIR = APP_DIR / "core"
