import requests
import time
import smtplib
import hashlib
import os
import logging
from email.message import EmailMessage
from pathlib import Path
from datetime import datetime

# Set up logging
logging.basicConfig(
    filename='website_monitor.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class WebsiteMonitor:
    def __init__(self, url, check_interval_minutes=60, email_config=None):
        self.url = url
        self.check_interval_seconds = check_interval_minutes * 60
        self.email_config = email_config
        self.last_hash = None
        self.first_run = True
        self.data_dir = Path("monitor_data")
        self.data_dir.mkdir(exist_ok=True)
        self.hash_file = self.data_dir / "last_hash.txt"
        self.load_last_hash()
        logging.info(f"Monitor initialized for {url}")

    def load_last_hash(self):
        if self.hash_file.exists():
            self.last_hash = self.hash_file.read_text().strip()
            self.first_run = False
            logging.info(f"Loaded previous hash: {self.last_hash}")
        else:
            logging.info("No previous hash found, will create on first check")

    def save_hash(self, hash_value):
        self.hash_file.write_text(hash_value)
        self.last_hash = hash_value
        logging.info(f"Saved new hash: {hash_value}")

    def get_website_content(self):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(self.url, headers=headers, timeout=30)
            if response.status_code == 200:
                logging.info(f"Successfully retrieved website content")
                return response.text
            else:
                logging.error(f"Failed to retrieve website. Status code: {response.status_code}")
                return None
        except Exception as e:
            logging.error(f"Error retrieving website: {e}")
            return None

    def compute_hash(self, content):
        return hashlib.md5(content.encode()).hexdigest()

    def save_snapshot(self, content):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        snapshot_file = self.data_dir / f"snapshot_{timestamp}.html"
        snapshot_file.write_text(content)
        logging.info(f"Saved snapshot to {snapshot_file}")

    def send_notification(self, subject, message):
        if not self.email_config:
            logging.info(f"NOTIFICATION: {subject}")
            return True
        
        try:
            msg = EmailMessage()
            msg.set_content(message)
            msg['Subject'] = subject
            msg['From'] = self.email_config['from']
            msg['To'] = self.email_config['to']
            
            with smtplib.SMTP_SSL(self.email_config['smtp_server'], self.email_config['smtp_port']) as server:
                server.login(self.email_config['username'], self.email_config['password'])
                server.send_message(msg)
            logging.info(f"Email notification sent to {self.email_config['to']}")
            return True
        except Exception as e:
            logging.error(f"Failed to send email notification: {e}")
            return False

    def check_for_changes(self):
        content = self.get_website_content()
        if not content:
            return False
        
        current_hash = self.compute_hash(content)
        
        if self.first_run:
            self.save_hash(current_hash)
            self.first_run = False
            logging.info(f"First run: Website hash saved ({current_hash})")
            return False
        
        if current_hash != self.last_hash:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.save_snapshot(content)
            self.save_hash(current_hash)
            
            subject = "AIEngineerPack Website Change Detected!"
            message = f"""
Change detected on {self.url} at {timestamp}.

The website content has changed. Check it out to see if a new volume (like Vol 4) has been released!

Visit the website: {self.url}
            """
            
            self.send_notification(subject, message)
            logging.info("Change detected and notification sent!")
            return True
        
        return False

    def start_monitoring(self):
        logging.info(f"Starting to monitor {self.url}")
        logging.info(f"Checking every {self.check_interval_seconds//60} minutes")
        
        try:
            while True:
                logging.info(f"Checking {self.url} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                changed = self.check_for_changes()
                
                if changed:
                    logging.info("Change detected!")
                else:
                    logging.info("No changes detected.")
                
                time.sleep(self.check_interval_seconds)
        except KeyboardInterrupt:
            logging.info("Monitoring stopped by user.")
        except Exception as e:
            logging.error(f"Error in monitoring loop: {e}")


if __name__ == "__main__":
    # Configure email for ranjanvernekar45@gmail.com
    # Note: You need to set up your own SMTP settings and password
    email_config = {
        'smtp_server': 'smtp.gmail.com',
        'smtp_port': 465,
        'username': 'YOUR_EMAIL@gmail.com',  # Replace with your Gmail address
        'password': 'YOUR_APP_PASSWORD',     # Replace with your app password
        'from': 'YOUR_EMAIL@gmail.com',      # Replace with your Gmail address
        'to': 'ranjanvernekar45@gmail.com'
    }
    
    # If you don't want to use email notifications, set this to None
    # email_config = None
    
    try:
        monitor = WebsiteMonitor(
            url="https://www.aiengineerpack.com/",
            check_interval_minutes=60,  # Check every hour
            email_config=email_config
        )
        
        monitor.start_monitoring()
    except Exception as e:
        logging.critical(f"Fatal error: {e}")
        # Sleep briefly to ensure log is written before exit
        time.sleep(1) 