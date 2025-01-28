# Logging setup
import logging
from datetime import datetime

from config.config import LOG_FILE


# log normal messages
def log_info(message):
    """Log info messages."""
    logging.basicConfig(filename=LOG_FILE, level=logging.INFO)
    logging.info(f"{datetime.now} - INFO: {message}")


# log error messages
def log_error(message):
    """Log error messages."""
    logging.basicConfig(filename=LOG_FILE, level=logging.ERROR)
    logging.error(f"{datetime.now} - ERROR: {message}")
