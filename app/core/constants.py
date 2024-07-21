"""
This module contains the configuration for the app

:author: Alex Traveylan
:date: 2024
"""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
RIOT_API_KEY = os.getenv("RIOT_API_KEY")


# Paths of the application

WORKSPACE_DIR = Path(__file__).parents[2].absolute()

APP_DIR = WORKSPACE_DIR / "app"

ADAPTERS_DIR = APP_DIR / "adapter"

CORE_DIR = APP_DIR / "core"
