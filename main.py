import sys
from config.app_config import load_configuration
from utils.logger import setup_logger
from business_logic import BusinessLogic
import asyncio


async def main():
    """Main function to run the Bitcoin tracker application."""
    # Configure the root logger first
    logger = setup_logger(__name__)
    logger.info("Starting Bitcoin Tracker Application")

    config = load_configuration()
    if config is None:
        sys.exit(1)

    tracker = BusinessLogic(config)
    await tracker.run_tracker()


if __name__ == "__main__":
    asyncio.run(main())
