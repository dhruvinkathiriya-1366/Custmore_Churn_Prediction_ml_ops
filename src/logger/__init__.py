import logging
import os
from pathlib import Path
from datetime import datetime


# Create logger
logger = logging.getLogger("customer_churn_logger")
logger.setLevel(logging.INFO)
logger.propagate = False

# Log format
formatter = logging.Formatter(
    "[%(asctime)s] "
    "%(levelname)s "
    "[%(filename)s:%(lineno)d] "
    "%(funcName)s() - "
    "%(message)s",
    datefmt="%d-%m-%Y %H:%M:%S"
)

# Always add console handler (works everywhere including Vercel)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Add file handler only when running in a writable local environment
# Vercel serverless has a read-only filesystem — skip file logging there
try:
    PROJECT_ROOT = Path(__file__).resolve().parents[2]
    LOG_DIR = PROJECT_ROOT / "logs"
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    current_time = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
    LOG_FILE = LOG_DIR / f"{current_time}.log"
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
except (OSError, PermissionError):
    # Read-only filesystem (e.g. Vercel serverless) — console logging only
    pass