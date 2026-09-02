import logging
from pathlib import Path
from datetime import datetime


# Project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Log directory
LOG_DIR = PROJECT_ROOT / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)


# Log file name
current_time = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")

LOG_FILE = LOG_DIR / f"{current_time}.log"


# Create logger
logger = logging.getLogger("customer_churn_logger")

logger.setLevel(logging.INFO)

# Prevent duplicate handlers
logger.propagate = False


# File handler
file_handler = logging.FileHandler(
    LOG_FILE,
    encoding="utf-8"
)

console_handler=logging.StreamHandler()
file_handler.setLevel(logging.INFO)


# Log format
formatter = logging.Formatter(
    "[%(asctime)s] "
    "%(levelname)s "
    "[%(filename)s:%(lineno)d] "
    "%(funcName)s() - "
    "%(message)s",
    datefmt="%d-%m-%Y %H:%M:%S"
)

file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)