import os
import logging
from pathlib import Path

# Determine the absolute project root (assuming this file is in engine/config.py)
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Default I/O Directories
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "output"
LOG_DIR = PROJECT_ROOT / "logs"

# Ensure default directories exist upon import
os.makedirs(DEFAULT_OUTPUT_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

# Logging Configuration
LOGGING_LEVEL_CONSOLE = logging.INFO
LOGGING_LEVEL_FILE = logging.DEBUG
LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(module)s | %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Supported Format Mappings (Input Format -> Supported Output Formats)
SUPPORTED_CONVERSIONS = {
    ".pdf": [".docx", ".txt", ".png", ".jpeg", ".pptx"],
    ".docx": [".pdf", ".txt", ".pptx"],
    ".doc": [".pdf", ".docx", ".txt"],
    ".pptx": [".pdf", ".docx"],
    ".xlsx": [".pdf", ".csv"],
    ".xls": [".pdf", ".xlsx", ".csv"],
    ".csv": [".pdf", ".xlsx"],
    ".txt": [".pdf", ".docx"],
    ".png": [".pdf", ".jpeg"],
    ".jpeg": [".pdf", ".png"],
    ".jpg": [".pdf", ".png"],
    ".mp4": [".mp3", ".gif", ".mov", ".avi"],
    ".mov": [".mp3", ".gif", ".mp4", ".avi"],
    ".avi": [".mp3", ".gif", ".mp4", ".mov"],
    ".mp3": [".wav"],
    ".wav": [".mp3"]
}
