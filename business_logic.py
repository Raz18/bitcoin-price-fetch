import time
import datetime as dt
from api_handler import APIHandler
from price_data_storage import DataStorage
from graph_generator import GraphGenerator
from email_sender import EmailSender
from utils.logger import setup_logger


class BusinessLogic:
    """Orchestrates the price tracking process."""

    def __init__(self, config):
        self.config = config
        self.logger = setup_logger(self.__class__.__name__)
        self.api_handler = APIHandler(config['api_url'])
        self.data_storage = DataStorage(config['json_filepath'])
        self.graph_generator = GraphGenerator(config['graph_filepath'])
        self.email_sender = EmailSender(
            config['smtp_server'],
            config['smtp_port'],
            config['sender_email'],
            config['sender_password']
        )

    def run_tracker(self):
        """Executes the main logic of the application of fetching bitcoin price."""
        self.logger.info("Starting Bitcoin price tracking task.")
        start_time = time.time()
        duration_seconds = self.config['duration_minutes'] * 60

        while time.time() - start_time < duration_seconds:
            self.logger.debug("Requesting new price data.")
            price = self.api_handler.get_bitcoin_price()
            if price is not None:
                timestamp = dt.datetime.now().isoformat()
                self.data_storage.store_price(timestamp, price)
            else:
                self.logger.warning("Skipping storage due to fetch error.")

            self.logger.debug("Waiting for next 60-second interval.")
            time.sleep(60)

        self.logger.info("Finished collecting price data for the hour.")
        self.data_storage.save_to_json()

        if self.data_storage.data:
            self.logger.info("Generating price graph.")
            self.graph_generator.generate_graph(self.data_storage.data)

            max_price = self.data_storage.get_max_price()
            self.logger.info(f"Maximum price recorded: ${max_price:.2f}")

            self.logger.info("Sending email report.")
            self.email_sender.send_report_email(
                self.config['recipient_email'],
                max_price,
                self.config['graph_filepath']
            )
        else:
            self.logger.warning("No data collected. Skipping graph and email steps.")

        self.logger.info("Bitcoin price tracking task finished.")
