import requests
import hashlib
import os
import smtplib
from email.message import EmailMessage
import json
from datetime import datetime

def send_email_notification(subject, message, email_config):
    try:
        msg = EmailMessage()
        msg.set_content(message)
        msg['Subject'] = subject
        msg['From'] = email_config['from']
        msg['To'] = email_config['to']
        
        with smtplib.SMTP_SSL(email_config['smtp_server'], email_config['smtp_port']) as server:
            server.login(email_config['username'], email_config['password'])
            server.send_message(msg)
        print(f"Email notification sent to {email_config['to']}")
        return True
    except Exception as e:
        print(f"Failed to send email notification: {e}")
        return False

def check_website():
    # Configuration for email
    email_config = {
        'smtp_server': 'smtp.gmail.com',
        'smtp_port': 465,
        'username': os.environ.get('EMAIL_USERNAME', ''),
        'password': os.environ.get('EMAIL_PASSWORD', ''),
        'from': os.environ.get('EMAIL_FROM', ''),
        'to': 'ranjanvernekar45@gmail.com'
    }
    
    # Check if email credentials are set
    if not email_config['username'] or not email_config['password']:
        print("Email credentials not configured in environment variables")
        return
    
    url = "https://www.aiengineerpack.com/"
    
    try:
        # Get website content
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30)
        
        if response.status_code != 200:
            print(f"Failed to retrieve website. Status code: {response.status_code}")
            return
        
        content = response.text
        current_hash = hashlib.md5(content.encode()).hexdigest()
        
        # Get previous hash from GitHub Actions
        previous_hash_file = 'previous_hash.txt'
        previous_hash = None
        
        if os.path.exists(previous_hash_file):
            with open(previous_hash_file, 'r') as f:
                previous_hash = f.read().strip()
        
        # Save current hash for next time
        with open(previous_hash_file, 'w') as f:
            f.write(current_hash)
        
        if not previous_hash:
            print(f"First run, hash saved: {current_hash}")
            return
        
        # Check if the hash has changed
        if current_hash != previous_hash:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"Change detected at {timestamp}!")
            
            # Send notification
            subject = "AIEngineerPack Website Change Detected!"
            message = f"""
Change detected on {url} at {timestamp}.

The website content has changed. Check it out to see if a new volume (like Vol 4) has been released!

Visit the website: {url}
            """
            
            send_email_notification(subject, message, email_config)
            print("Notification sent!")
        else:
            print("No changes detected.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_website() 