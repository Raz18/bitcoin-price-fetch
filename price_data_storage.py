import json

from pathlib import Path
from utils.logger import setup_logger
class DataStorage:
    """Handles storage of the price data."""
    def __init__(self, filepath):
        self.filepath = Path(filepath)
        self.data = []
        self.logger = setup_logger(__name__)

    def store_price(self, timestamp, price):
        """Adds a new price entry to the data list."""
        self.data.append({'timestamp': timestamp, 'price': price})
        self.logger.info(f"Stored price: ${price:.2f} at {timestamp}")

    def save_to_json(self):
        """Saves the collected data to a JSON file."""
        try:
            with open(self.filepath, 'w') as f:
                json.dump(self.data, f, indent=4)
            self.logger.info(f"Data successfully saved to {self.filepath}")
        except IOError as e:
            self.logger.error(f"Error saving data to JSON file: {e}")

    def get_max_price(self):
        """Returns the maximum price from the collected data."""
        if not self.data:
            return None
        return max(item['price'] for item in self.data)