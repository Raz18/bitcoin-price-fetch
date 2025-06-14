import os
import logging
import sys
from datetime import datetime

from dotenv import load_dotenv

def load_configuration():
    """
    Loads configuration from the .env file and validates it.

    Returns:
        dict: A dictionary with configuration values, or None if validation fails.
    """
    load_dotenv()

    config = {
        "api_url": os.getenv("API_URL"),
        "duration_minutes": int(os.getenv("TRACKING_DURATION", 60)),
        "json_filepath": os.getenv("JSON_FILEPATH"),
        "graph_filepath": os.getenv("GRAPH_FILEPATH"),
        "recipient_email": os.getenv("RECIPIENT_EMAIL"),
        "smtp_server": os.getenv("SMTP_SERVER"),
        "smtp_port": int(os.getenv("SMTP_PORT", 587)),
        "sender_email": os.getenv("SENDER_EMAIL"),
        "sender_password": os.getenv("SENDER_PASSWORD")
    }

    # Validate that all necessary configurations are present
    missing_configs = [key for key, value in config.items() if value is None]
    if missing_configs:
        logging.error(f"Error: Missing required environment variables: {', '.join(missing_configs)}")
        logging.error("Please ensure your .env file is correctly set up.")
        return None

    return config

