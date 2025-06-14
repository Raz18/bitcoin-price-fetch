import requests
import json
import logging
import time
import threading
import smtplib
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from typing import List, Dict, Optional
import os
from utils.logger import setup_logger

'''
class DataManager:
    """Handles data storage and retrieval operations."""
    
    def __init__(self, logger: logging.Logger, data_file: str = "bitcoin_prices.json"):
        self.logger = logger
        self.data_file = data_file
        self.price_data: List[Dict] = []
        self.load_existing_data()
    
    def load_existing_data(self):
        """Load existing price data from JSON file."""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    self.price_data = json.load(f)
                self.logger.info(f"Loaded {len(self.price_data)} existing price records")
            else:
                self.logger.info("No existing data file found, starting fresh")
        except Exception as e:
            self.logger.error(f"Error loading existing data: {e}")
            self.price_data = []
    
    def save_price(self, price: float):
        """Save a price data point with timestamp."""
        timestamp = datetime.now().isoformat()
        price_entry = {
            "timestamp": timestamp,
            "price": price,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.price_data.append(price_entry)
        
        try:
            with open(self.data_file, 'w') as f:
                json.dump(self.price_data, f, indent=2)
            self.logger.info(f"Saved price ${price:,.2f} at {price_entry['date']}")
        except Exception as e:
            self.logger.error(f"Error saving price data: {e}")
    
    def get_last_hour_data(self) -> List[Dict]:
        """Get price data from the last hour."""
        one_hour_ago = datetime.now() - timedelta(hours=1)
        
        recent_data = []
        for entry in self.price_data:
            entry_time = datetime.fromisoformat(entry['timestamp'])
            if entry_time >= one_hour_ago:
                recent_data.append(entry)
        
        self.logger.info(f"Retrieved {len(recent_data)} price records from last hour")
        return recent_data
    
    def get_max_price_last_hour(self) -> Optional[float]:
        """Get the maximum price from the last hour."""
        recent_data = self.get_last_hour_data()
        if not recent_data:
            return None
        
        max_price = max(entry['price'] for entry in recent_data)
        self.logger.info(f"Maximum price in last hour: ${max_price:,.2f}")
        return max_price


class GraphGenerator:
    """Handles graph generation for Bitcoin price data."""
    
    def __init__(self, logger: logging.Logger):
        self.logger = logger
    
    def generate_price_graph(self, price_data: List[Dict], output_file: str = "bitcoin_price_graph.png"):
        """Generate a price graph from the data."""
        if not price_data:
            self.logger.warning("No data available for graph generation")
            return None
        
        try:
            # Extract timestamps and prices
            timestamps = [datetime.fromisoformat(entry['timestamp']) for entry in price_data]
            prices = [entry['price'] for entry in price_data]
            
            # Create the plot
            plt.figure(figsize=(12, 6))
            plt.plot(timestamps, prices, marker='o', linewidth=2, markersize=4)
            plt.title('Bitcoin Price Index (BPI) - Last Hour', fontsize=16, fontweight='bold')
            plt.xlabel('Time', fontsize=12)
            plt.ylabel('Price (USD)', fontsize=12)
            plt.grid(True, alpha=0.3)
            plt.xticks(rotation=45)
            
            # Format y-axis to show currency
            plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
            
            plt.tight_layout()
            plt.savefig(output_file, dpi=300, bbox_inches='tight')
            plt.close()
            
            self.logger.info(f"Price graph saved as {output_file}")
            return output_file
            
        except Exception as e:
            self.logger.error(f"Error generating graph: {e}")
            return None


class EmailNotifier:
    """Handles email notifications."""
    
    def __init__(self, logger: logging.Logger, smtp_server: str = "smtp.gmail.com", 
                 smtp_port: int = 587):
        self.logger = logger
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
    
    def send_report(self, sender_email: str, sender_password: str, recipient_email: str,
                   max_price: float, graph_file: str):
        """Send email report with max price and graph."""
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = recipient_email
            msg['Subject'] = f"Bitcoin Price Report - Max: ${max_price:,.2f}"
            
            # Email body
            body = f"""
            Bitcoin Price Tracker Report
            
            Time Period: Last Hour
            Maximum Price: ${max_price:,.2f}
            Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            
            Please find the attached price graph for visual analysis.
            
            Best regards,
            Bitcoin Price Tracker
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Attach graph if it exists
            if graph_file and os.path.exists(graph_file):
                with open(graph_file, 'rb') as f:
                    img_data = f.read()
                    image = MIMEImage(img_data)
                    image.add_header('Content-Disposition', 
                                   f'attachment; filename={os.path.basename(graph_file)}')
                    msg.attach(image)
            
            # Send email
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
            server.quit()
            
            self.logger.info(f"Email report sent successfully to {recipient_email}")
            
        except Exception as e:
            self.logger.error(f"Error sending email: {e}")


class BitcoinPriceTracker:
    """Main business logic class for Bitcoin price tracking."""
    
    def __init__(self):
        self.logger_manager = BitcoinPriceLogger()
        self.logger = self.logger_manager.get_logger()
        
        self.api_client = BitcoinPriceAPI(self.logger)
        self.data_manager = DataManager(self.logger)
        self.graph_generator = GraphGenerator(self.logger)
        self.email_notifier = EmailNotifier(self.logger)
        
        self.is_running = False
        self.collection_thread = None
        
        self.logger.info("Bitcoin Price Tracker initialized")
    
    def collect_price_data(self):
        """Collect Bitcoin price data every minute."""
        while self.is_running:
            price = self.api_client.get_bitcoin_price()
            if price is not None:
                self.data_manager.save_price(price)
            
            # Wait for 60 seconds (1 minute)
            time.sleep(60)
    
    def start_data_collection(self):
        """Start collecting price data in a separate thread."""
        if not self.is_running:
            self.is_running = True
            self.collection_thread = threading.Thread(target=self.collect_price_data)
            self.collection_thread.daemon = True
            self.collection_thread.start()
            self.logger.info("Started price data collection")
    
    def stop_data_collection(self):
        """Stop collecting price data."""
        self.is_running = False
        if self.collection_thread:
            self.collection_thread.join()
        self.logger.info("Stopped price data collection")
    
    def generate_hourly_report(self, sender_email: str = None, sender_password: str = None,
                             recipient_email: str = None):
        """Generate and send hourly report."""
        try:
            # Get data from last hour
            last_hour_data = self.data_manager.get_last_hour_data()
            
            if not last_hour_data:
                self.logger.warning("No data available for hourly report")
                return
            
            # Get maximum price
            max_price = self.data_manager.get_max_price_last_hour()
            
            # Generate graph
            graph_file = self.graph_generator.generate_price_graph(last_hour_data)
            
            # Send email if credentials provided
            if all([sender_email, sender_password, recipient_email, max_price]):
                self.email_notifier.send_report(
                    sender_email, sender_password, recipient_email,
                    max_price, graph_file
                )
            
            self.logger.info("Hourly report completed")
            
        except Exception as e:
            self.logger.error(f"Error generating hourly report: {e}")
    
    def run_for_duration(self, duration_minutes: int = 60, 
                        sender_email: str = None, sender_password: str = None,
                        recipient_email: str = None):
        """Run the tracker for a specified duration then generate report."""
        self.logger.info(f"Starting Bitcoin price tracking for {duration_minutes} minutes")
        
        # Start data collection
        self.start_data_collection()
        
        # Wait for the specified duration
        time.sleep(duration_minutes * 60)
        
        # Stop data collection
        self.stop_data_collection()
        
        # Generate report
        self.generate_hourly_report(sender_email, sender_password, recipient_email)
        
        self.logger.info("Bitcoin price tracking completed")


def main():
    """Main function to run the Bitcoin price tracker."""
    tracker = BitcoinPriceTracker()
    
    # Example usage - collect data for 1 hour then generate report
    # Uncomment and configure email settings as needed
    """
    tracker.run_for_duration(
        duration_minutes=60,
        sender_email="your-email@gmail.com",
        sender_password="your-app-password",
        recipient_email="recipient@gmail.com"
    )
    """
    
    # For testing - collect a few data points
    tracker.start_data_collection()
    print("Collecting Bitcoin price data...")
    print("Press Ctrl+C to stop and generate report")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        tracker.stop_data_collection()
        tracker.generate_hourly_report()
        print("\nReport generated. Check bitcoin_price_graph.png and bitcoin_prices.json")


if __name__ == "__main__":
    main()
'''