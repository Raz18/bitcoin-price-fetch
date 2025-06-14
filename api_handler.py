from typing import Optional

import requests
from utils.logger import setup_logger

class APIHandler:
    """Handles fetching data from the Coinbase API."""
    def __init__(self, url):
        self.url = url
        self.logger = setup_logger(__name__)

    def get_bitcoin_price(self) -> Optional[float]:
        """Fetch the current Bitcoin price from the Coinbase API."""
        try:
            self.logger.info("Fetching Bitcoin price from API")
            response = requests.get(self.url, timeout=10)
            response.raise_for_status()

            data = response.json()
            price = float(data['data']['amount'])

            self.logger.info(f"Successfully fetched Bitcoin price: ${price:,.2f}")
            return price

        except requests.RequestException as e:
            self.logger.error(f"Error fetching Bitcoin price: {e}")
            return None
        except (KeyError, ValueError) as e:
            self.logger.error(f"Error parsing API response: {e}")
            return None
