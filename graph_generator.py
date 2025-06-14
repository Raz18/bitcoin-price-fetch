import logging
import datetime as dt
from pathlib import Path
import matplotlib.pyplot as plt
from utils.logger import setup_logger
class GraphGenerator:
    """Generates a graph from the collected price data."""
    def __init__(self, filepath):
        self.filepath = Path(filepath)
        self.logger = setup_logger(__name__)

    def generate_graph(self, data):
        """Generates and saves a line graph of Bitcoin prices."""
        if not data:
            self.logger.warning("No data provided to generate graph.")
            return
        try:
            timestamps = [dt.datetime.fromisoformat(item['timestamp']) for item in data]
            prices = [item['price'] for item in data]

            plt.style.use('seaborn-v0_8-whitegrid')
            fig, ax = plt.subplots(figsize=(12, 7))
            ax.plot(timestamps, prices, marker='.', linestyle='-', color='#f2a900')

            ax.set_title('Bitcoin Price Index (BPI) Over 1 Hour', fontsize=16, weight='bold')
            ax.set_xlabel('Time', fontsize=12)
            ax.set_ylabel('Price (USD)', fontsize=12)

            fig.autofmt_xdate()
            plt.tight_layout()
            plt.savefig(self.filepath)
            self.logger.info(f"Graph successfully saved to {self.filepath}")
        except Exception as e:
            self.logger.error(f"Failed to generate graph: {e}")