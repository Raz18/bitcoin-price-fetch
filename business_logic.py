import datetime as dt
from api_handler import APIHandler
from price_data_storage import DataStorage
from graph_generator import GraphGenerator
from email_sender import EmailSender
from utils.logger import setup_logger
import asyncio


class BusinessLogic:
    """Orchestrates and centralizes the price tracking process."""

    def __init__(self, config):
        self.config = config
        self.logger = setup_logger(__name__)
        self.api_handler = APIHandler(config['api_url'])
        self.data_storage = DataStorage(config['json_filepath'])
        self.graph_generator = GraphGenerator(config['graph_filepath'])
        self.email_sender = EmailSender(
            config['smtp_server'],
            config['smtp_port'],
            config['sender_email'],
            config['sender_password']
        )

    async def run_tracker(self):
        """Executes the main async logic of the application."""
        self.logger.info("Starting Bitcoin price tracking task.")
        loop = asyncio.get_event_loop()
        start_time = loop.time()
        duration_seconds = self.config['duration_minutes'] * 60
        # Initialize the data storage
        while loop.time() - start_time < duration_seconds:
            self.logger.debug("Requesting new price data.")
            price = await self.api_handler.get_bitcoin_price()
            if price is not None:
                timestamp = dt.datetime.now().isoformat()
                self.data_storage.store_price(timestamp, price)
            else:
                self.logger.warning("Skipping storage due to fetch error.")

            self.logger.debug("Waiting for next 60-second interval.")
            await asyncio.sleep(60)

        self.data_storage.save_to_json()
        # Log the completion of data collection
        if self.data_storage.data:
            self.logger.info("Generating price graph in executor...")
            # Run the blocking graph generation in a separate thread
            await loop.run_in_executor(
                None, self.graph_generator.generate_graph, self.data_storage.data
            )

            max_price = self.data_storage.get_max_price()
            self.logger.info(f"Maximum price recorded: ${max_price:,.2f}")
            # Send the email report
            self.logger.info("Sending email report.")
            await self.email_sender.send_report_email(
                self.config['recipient_email'],
                max_price,
                self.config['graph_filepath']
            )
        else:
            self.logger.warning("No data collected. Skipping graph and email steps.")

        self.logger.info("Bitcoin price tracking task finished.")
