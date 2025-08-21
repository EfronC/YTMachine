import logging
from logging.handlers import TimedRotatingFileHandler
import os
from datetime import datetime

LOGS_DIR = "logs"
os.makedirs(LOGS_DIR, exist_ok=True)

# Base log file (will get suffixes for rotation)
base_log_file = os.path.join(LOGS_DIR, "app.log")

# Create a logger
logger = logging.getLogger("app_logger")
logger.setLevel(logging.INFO)

# Create timed rotating handler (rotate every 24h, keep 7 days for example)
handler = TimedRotatingFileHandler(
    base_log_file,
    when="midnight",      # rotate at midnight
    interval=1,           # every 1 day
    backupCount=7,        # keep 7 days of logs
    encoding="utf-8",
    utc=False
)

# Format filenames with date suffix: app.log.20250821
handler.suffix = "%Y%m%d"

# Optional: control how the rotated files are named (strip default .log extension duplication)
handler.extMatch = r"^\d{8}$"

# Create formatter
formatter = logging.Formatter("[%(asctime)s](%(levelname)s) %(message)s", "%Y-%m-%d %H:%M:%S")
handler.setFormatter(formatter)

# Attach handler
logger.addHandler(handler)