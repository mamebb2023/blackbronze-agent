import logging
import os
from datetime import datetime
from config.config import LOG_FILE

# Ensure the logs directory exists
log_dir = os.path.dirname(LOG_FILE)
os.makedirs(log_dir, exist_ok=True)


# log normal messages
def log_info(message):
    """Log info messages."""
    logging.basicConfig(filename=LOG_FILE, level=logging.INFO)
    logging.info(f"{datetime.now()} - INFO: {message}")


# log error messages
def log_error(message):
    """Log error messages."""
    logging.basicConfig(filename=LOG_FILE, level=logging.ERROR)
    logging.error(f"{datetime.now()} - ERROR: {message}")
