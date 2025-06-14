import smtplib
import logging
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from utils.logger import setup_logger
class EmailSender:
    """Handles sending emails with attachments."""
    def __init__(self, smtp_server, port, sender_email, sender_password):
        self.smtp_server = smtp_server
        self.port = port
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.logger = setup_logger(__name__)

    def send_report_email(self, recipient_email, max_price, graph_path):
        """Sends an email with the max Bitcoin price and the price graph."""
        self.logger.info(f"Preparing email for {recipient_email}")
        msg = MIMEMultipart()
        msg['Subject'] = f"Bitcoin Hourly Price Report - Max Price: ${max_price:.2f}"
        msg['From'] = self.sender_email
        msg['To'] = recipient_email

        body = f"""
        Hello,

        This is your automated Bitcoin price report.

        The maximum price recorded in the last hour was: ${max_price:,.2f}

        The attached graph shows the price trend over this period.

        BestRegards,
        Your Bitcoin Price Tracker
        
        """
        msg.attach(MIMEText(body, 'plain'))

        try:
            with open(graph_path, 'rb') as fp:
                img = MIMEImage(fp.read())
                img.add_header('Content-Disposition', 'attachment', filename=Path(graph_path).name)
                msg.attach(img)
            self.logger.debug("Graph attached to email.")
        except IOError as e:
            self.logger.error(f"Could not attach graph file: {e}")
            return

        try:
            with smtplib.SMTP(self.smtp_server, self.port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            self.logger.info(f"Email report sent successfully to {recipient_email}")
        except Exception as e:
            self.logger.critical(f"Failed to send email: {e}")