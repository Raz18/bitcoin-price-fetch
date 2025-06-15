import datetime as dt
from pathlib import Path
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
from utils.logger import setup_logger


class GraphGenerator:
    """Generates a graph from the collected price data."""

    def __init__(self, filepath):
        self.filepath = Path(filepath)
        self.logger = setup_logger(__name__)

    def generate_graph(self, data):
        """Generates an hourly based and saves a line graph of Bitcoin prices."""
        if not data:
            self.logger.warning("No data provided to generate graph.")
            return
        try:
            fig, ax = plt.subplots(figsize=(12, 7))
            timestamps = [dt.datetime.fromisoformat(item['timestamp']) for item in data]
            prices = [item['price'] for item in data]

            plt.style.use('seaborn-v0_8-whitegrid')

            ax.plot(timestamps, prices, marker='.', linestyle='-', color='#0056b3')

            # Set title and labels
            date_str = timestamps[0].strftime('%d/%m/%Y')
            ax.set_title(f'Bitcoin Price Index (BPI) Over 1 Hour - {date_str}', fontsize=16, weight='bold')
            ax.set_xlabel('Time', fontsize=12)
            ax.set_ylabel('Price (USD)', fontsize=12)

            # Format y-axis to show dollar amounts
            ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'${x:,.2f}'))

            # Set x-axis to show ticks every 5 minutes
            from matplotlib.dates import MinuteLocator, DateFormatter
            ax.xaxis.set_major_locator(MinuteLocator(interval=5))
            ax.xaxis.set_major_formatter(DateFormatter('%H:%M'))

            plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

            plt.tight_layout()
            plt.savefig(self.filepath)
            self.logger.info(f"Graph successfully saved to {self.filepath}")
            plt.close(fig)
        except Exception as e:
            self.logger.error(f"Failed to generate graph: {e}")
