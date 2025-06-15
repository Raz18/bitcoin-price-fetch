import logging
import os
import sys
from datetime import datetime

def setup_logger(name=None):
    """Set up a logger for the given name or configure root logger"""
    # Create temp directory if it doesn't exist
    os.makedirs("temp/test_runs", exist_ok=True)

    # Get the logger by name or root logger
    logger = logging.getLogger(name) if name else logging.getLogger()

    # Only configure if not already configured
    if not logger.handlers:
        logger.setLevel(logging.INFO)

        # Create handlers
        c_handler = logging.StreamHandler(sys.stdout)
        timestamp = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        log_file = f"temp/test_runs/test_run_{timestamp}.log"
        f_handler = logging.FileHandler(log_file, encoding='utf-8')

        # Set log level for handlers
        c_handler.setLevel(logging.INFO)
        f_handler.setLevel(logging.INFO)

        # Create formatters with correct timestamp format
        datetime_format = '%Y-%m-%d %H:%M:%S'
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        c_format = logging.Formatter(log_format, datefmt=datetime_format)
        f_format = logging.Formatter(log_format, datefmt=datetime_format)

        c_handler.setFormatter(c_format)
        f_handler.setFormatter(f_format)

        # Add handlers to logger
        logger.addHandler(c_handler)
        logger.addHandler(f_handler)

        # Disable propagation for non-root loggers to prevent duplicate logs
        if name:
            logger.propagate = False

    return logger