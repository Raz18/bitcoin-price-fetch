import sys
from config.app_config import load_configuration
from utils.logger import setup_logger
from business_logic import BusinessLogic

def main():
    """Main function to run the Bitcoin tracker application."""
    setup_logger(__name__)
    config = load_configuration()
    if config is None:
        sys.exit(1)

    tracker = BusinessLogic(config)
    tracker.run_tracker()

if __name__ == "__main__":
    main()