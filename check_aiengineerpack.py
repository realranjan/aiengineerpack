import requests
import os
import smtplib
import re
from email.message import EmailMessage
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

def send_discord_notification(message, webhook_url):
    try:
        data = {
            "content": message,
            "username": "AIEngineerPack Monitor"
        }
        response = requests.post(webhook_url, json=data)
        if response.status_code == 204:
            print("Discord notification sent successfully")
            return True
        else:
            print(f"Failed to send Discord notification. Status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"Failed to send Discord notification: {e}")
        return False

def send_telegram_notification(message, bot_token, chat_id):
    try:
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        data = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "HTML"
        }
        response = requests.post(url, data=data)
        if response.status_code == 200:
            print("Telegram notification sent successfully")
            return True
        else:
            print(f"Failed to send Telegram notification. Status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"Failed to send Telegram notification: {e}")
        return False

def check_for_new_volumes():
    # Configuration for email
    email_config = {
        'smtp_server': 'smtp.gmail.com',
        'smtp_port': 465,
        'username': os.environ.get('EMAIL_USERNAME', ''),
        'password': os.environ.get('EMAIL_PASSWORD', ''),
        'from': os.environ.get('EMAIL_FROM', ''),
        'to': 'ranjanvernekar45@gmail.com'
    }
    
    # Configuration for Discord
    discord_webhook_url = os.environ.get('DISCORD_WEBHOOK_URL', '')
    
    # Configuration for Telegram
    telegram_bot_token = os.environ.get('TELEGRAM_BOT_TOKEN', '')
    telegram_chat_id = os.environ.get('TELEGRAM_CHAT_ID', '')
    
    # Print status for debugging
    if not email_config['username'] or not email_config['password']:
        print("⚠️ WARNING: Email credentials not configured in environment variables")
        print("Username set:", bool(email_config['username']))
        print("Password set:", bool(email_config['password']))
        print("From set:", bool(email_config['from']))
    else:
        print("✅ Email credentials configured")
        
    if not discord_webhook_url:
        print("⚠️ WARNING: Discord webhook URL not configured")
    else:
        print("✅ Discord webhook configured")
        
    if not telegram_bot_token or not telegram_chat_id:
        print("⚠️ WARNING: Telegram credentials not configured")
        print("Bot token set:", bool(telegram_bot_token))
        print("Chat ID set:", bool(telegram_chat_id))
    else:
        print("✅ Telegram credentials configured")
    
    url = "https://www.aiengineerpack.com/"
    print(f"📋 Checking website for new volumes: {url}")
    
    try:
        # Get website content
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30)
        
        if response.status_code != 200:
            print(f"❌ Failed to retrieve website. Status code: {response.status_code}")
            return
        
        print(f"✅ Website retrieved successfully (status {response.status_code})")
        content = response.text
        
        # Find all volume mentions in the content
        volume_pattern = r'Vol\s+(\d+)'
        volumes_found = re.findall(volume_pattern, content)
        
        # Convert to integers and remove duplicates
        volumes_found = sorted(set(int(vol) for vol in volumes_found))
        print(f"🔍 Volumes found on website: {volumes_found}")
        
        # Get previously found volumes
        volumes_file = 'volumes_found.txt'
        previous_volumes = []
        
        if os.path.exists(volumes_file):
            with open(volumes_file, 'r') as f:
                previous_content = f.read().strip()
                if previous_content:
                    previous_volumes = [int(vol) for vol in previous_content.split(',')]
            print(f"📁 Previously found volumes: {previous_volumes}")
        else:
            print(f"📁 No previous volumes file found, will create one")
        
        # Save current volumes for next time
        with open(volumes_file, 'w') as f:
            f.write(','.join(str(vol) for vol in volumes_found))
        print(f"💾 Saved current volumes to file")
        
        # First run
        if not previous_volumes:
            print(f"ℹ️ First run, volumes saved: {volumes_found}")
            
            setup_subject = "AIEngineerPack Monitor Setup Complete"
            setup_message = f"""
Your AIEngineerPack volume monitor has been set up successfully!

The script will now check for new volumes twice daily (8:00 AM and 8:00 PM UTC).
When a new volume is released, you'll receive a notification.

Currently available volumes: {', '.join(f'Vol {vol}' for vol in volumes_found)}
Website: {url}
            """
            
            # Send email notification
            if email_config['username'] and email_config['password']:
                send_email_notification(setup_subject, setup_message, email_config)
                print("📧 Setup confirmation email sent!")
                
            # Send Discord notification
            if discord_webhook_url:
                discord_message = f"**AIEngineerPack Monitor Setup Complete**\n\n{setup_message}"
                send_discord_notification(discord_message, discord_webhook_url)
                print("💬 Setup confirmation Discord message sent!")
                
            # Send Telegram notification
            if telegram_bot_token and telegram_chat_id:
                telegram_message = f"<b>AIEngineerPack Monitor Setup Complete</b>\n\n{setup_message}"
                send_telegram_notification(telegram_message, telegram_bot_token, telegram_chat_id)
                print("📱 Setup confirmation Telegram message sent!")
                
            return
        
        # Check for new volumes
        new_volumes = [vol for vol in volumes_found if vol not in previous_volumes]
        
        if new_volumes:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"🎉 New volumes detected at {timestamp}: {new_volumes}")
            
            # Create notification messages
            email_subject = "New AIEngineerPack Volume Released!"
            email_message = f"""
New volume{'s' if len(new_volumes) > 1 else ''} detected on {url} at {timestamp}:

{', '.join(f'Vol {vol}' for vol in new_volumes)} {'have' if len(new_volumes) > 1 else 'has'} been released!

Visit the website to claim your offers: {url}
            """
            
            # Format for Discord with markdown
            discord_message = f"**New AIEngineerPack Volume Released!**\n\nNew volume{'s' if len(new_volumes) > 1 else ''} detected on {url} at {timestamp}:\n\n{', '.join(f'Vol {vol}' for vol in new_volumes)} {'have' if len(new_volumes) > 1 else 'has'} been released!\n\nVisit the website to claim your offers: {url}"
            
            # Format for Telegram with HTML
            telegram_message = f"<b>New AIEngineerPack Volume Released!</b>\n\nNew volume{'s' if len(new_volumes) > 1 else ''} detected on {url} at {timestamp}:\n\n{', '.join(f'Vol {vol}' for vol in new_volumes)} {'have' if len(new_volumes) > 1 else 'has'} been released!\n\nVisit the website to claim your offers: {url}"
            
            # Send notifications
            notifications_sent = 0
            
            # Send email notification
            if email_config['username'] and email_config['password']:
                if send_email_notification(email_subject, email_message, email_config):
                    notifications_sent += 1
                print("📧 New volume notification email sent!")
                
            # Send Discord notification
            if discord_webhook_url:
                if send_discord_notification(discord_message, discord_webhook_url):
                    notifications_sent += 1
                print("💬 New volume notification Discord message sent!")
                
            # Send Telegram notification
            if telegram_bot_token and telegram_chat_id:
                if send_telegram_notification(telegram_message, telegram_bot_token, telegram_chat_id):
                    notifications_sent += 1
                print("📱 New volume notification Telegram message sent!")
                
            if notifications_sent == 0:
                print("⚠️ WARNING: No notifications were sent successfully. Please check your configuration.")
        else:
            print("ℹ️ No new volumes detected.")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🚀 Starting AIEngineerPack volume check...")
    check_for_new_volumes()
    print("✅ Check completed!") 