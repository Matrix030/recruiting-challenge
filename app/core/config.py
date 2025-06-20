"""Configuration settings for the Validia Face Recognition API.

This module handles all configuration settings through environment variables
with sensible defaults for development.
"""

import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# API Settings
API_V1_STR: str = "/api/v1"
PROJECT_NAME: str = "Validia Face Recognition API"

# Face Recognition Settings
FACE_MODEL_NAME: str = "buffalo_l"
DETECTION_SIZE: tuple[int, int] = (640, 640)
# Use GPU (ctx_id=0) if available, otherwise CPU (ctx_id=-1)
CONTEXT_ID: int = 0 if os.getenv("USE_GPU", "true").lower() == "true" else -1

# Database Settings
SQLITE_URL: str = os.getenv("SQLITE_URL", "sqlite:///./validia.db")

# Verification Settings
SIMILARITY_THRESHOLD: float = float(os.getenv("SIMILARITY_THRESHOLD", "0.6"))

# Paths
BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
UPLOAD_DIR: Path = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

# Create upload directory if it doesn't exist
UPLOAD_DIR.mkdir(parents=True, exist_ok=True) 