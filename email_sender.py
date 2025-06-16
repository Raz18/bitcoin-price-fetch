# email_sender.py
import asyncio
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from utils.logger import setup_logger


class EmailSender:
    """Handles sending emails asynchronously."""

    def __init__(self, smtp_server, port, sender_email, sender_password):
        self.smtp_server = smtp_server
        self.port = port
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.logger = setup_logger(__name__)

    async def send_report_email(self, recipient_email, max_price, graph_path):
        msg = MIMEMultipart()
        msg['Subject'] = f"Bitcoin Hourly Price Report - Max Price: ${max_price:,.2f}"
        msg['From'] = self.sender_email
        msg['To'] = recipient_email

        body = f"""
        Hello,

        This is your automated Bitcoin price report.

        The maximum price recorded in the last hour was: ${max_price:,.2f}

        The attached graph shows the price trend over this period.

        Best Regards,
        Your Bitcoin Price Tracker
        """
        msg.attach(MIMEText(body, 'plain'))

        # Attach the graph if available
        try:
            with open(graph_path, 'rb') as fp:
                img = MIMEImage(fp.read())
                img.add_header('Content-Disposition', 'attachment', filename=Path(graph_path).name)
                msg.attach(img)
        except IOError as e:
            self.logger.error(f"Could not attach graph file: {e}")
            return

        # Run email sending in a thread pool to avoid blocking
        loop = asyncio.get_running_loop()
        try:

            await loop.run_in_executor(None, self._send_email_sync, msg, recipient_email)
            self.logger.info(f"Email report sent successfully to {recipient_email}")
        except Exception as e:
            self.logger.critical(f"Failed to send email: {e}")
            self.logger.critical(f"Error type: {type(e).__name__}, Details: {str(e)}")

    def _send_email_sync(self, msg, recipient_email):
        """Synchronous email sending using standard smtplib"""
        import smtplib
        import ssl

        context = ssl.create_default_context()

        if self.port == 465:
            # Use SSL connection directly
            with smtplib.SMTP_SSL(self.smtp_server, self.port, context=context) as server:
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
        else:
            # Use STARTTLS
            with smtplib.SMTP(self.smtp_server, self.port) as server:
                server.ehlo()
                server.starttls(context=context)
                server.ehlo()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
