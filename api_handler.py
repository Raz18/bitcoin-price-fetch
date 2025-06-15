import asyncio
from typing import Optional
import aiohttp
from utils.logger import setup_logger


class APIHandler:
    """Handles fetching data from the Coinbase API asynchronously."""

    def __init__(self, url, timeout=10):
        self.url = url
        self.timeout = timeout
        self.logger = setup_logger(__name__)

    async def get_bitcoin_price(self) -> Optional[float]:
        """Asynchronously fetch the current Bitcoin price."""
        self.logger.info("Fetching Bitcoin price from API")
        try:
            # aiohttp uses a client session
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.timeout)) as session:
                async with session.get(self.url) as response:
                    response.raise_for_status()
                    data = await response.json()
                    price = float(data['data']['amount'])
                    self.logger.info(f"Successfully fetched Bitcoin price: ${price:,.2f}")
                    return price
        except (aiohttp.ClientError, asyncio.TimeoutError) as e:
            self.logger.error(f"Error fetching Bitcoin price: {e}")
            return None
        except (KeyError, ValueError) as e:
            self.logger.error(f"Error parsing API response: {e}")
            return None
