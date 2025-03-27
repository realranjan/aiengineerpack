import requests
import os
import smtplib
import re
import json
import argparse
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
        
        # Handle different chat_id formats
        # If it's a channel username, make sure it starts with @
        if isinstance(chat_id, str) and chat_id.strip().startswith('@'):
            formatted_chat_id = chat_id.strip()
        # If it looks like a channel ID but doesn't have -100 prefix, add it
        elif isinstance(chat_id, str) and chat_id.strip().isdigit() and not chat_id.startswith('-100'):
            formatted_chat_id = f"-100{chat_id.strip()}"
        else:
            formatted_chat_id = chat_id
            
        data = {
            "chat_id": formatted_chat_id,
            "text": message,
            "parse_mode": "HTML"
        }
        
        print(f"Sending Telegram notification to chat_id: {formatted_chat_id}")
        response = requests.post(url, data=data)
        
        if response.status_code == 200:
            print("Telegram notification sent successfully")
            return True
        else:
            print(f"Failed to send Telegram notification. Status code: {response.status_code}")
            print(f"Response content: {response.text}")
            return False
    except Exception as e:
        print(f"Failed to send Telegram notification: {e}")
        return False

def notify_public_subscribers(new_volumes, all_volumes, url, timestamp, bot_token):
    """Notify all subscribers in the telegram_subscribers.json file"""
    if not bot_token:
        print("⚠️ WARNING: Telegram bot token not configured, skipping public subscribers")
        return False
    
    # Load subscribers
    subscribers_file = 'telegram_subscribers.json'
    try:
        if os.path.exists(subscribers_file):
            with open(subscribers_file, 'r') as f:
                subscribers = json.load(f)
        else:
            print(f"⚠️ No subscribers file found at {subscribers_file}")
            return False
    except Exception as e:
        print(f"❌ Error loading subscribers: {e}")
        return False
    
    if not subscribers:
        print("ℹ️ No subscribers to notify")
        return True
    
    # Create notification message
    volume_text = ', '.join(f"Vol {vol}" for vol in new_volumes)
    verb = "have" if len(new_volumes) > 1 else "has"
    
    message = (
        f"🎉 <b>New AIEngineerPack Volume{'s' if len(new_volumes) > 1 else ''} Released!</b>\n\n"
        f"New volume{'s' if len(new_volumes) > 1 else ''} detected at {timestamp}:\n\n"
        f"{volume_text} {verb} been released!\n\n"
        f"Visit the website to claim your offers: {url}"
    )
    
    # Send notifications to each subscriber
    success_count = 0
    removed_subscribers = []
    
    for i, chat_id in enumerate(subscribers):
        try:
            send_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            send_data = {
                "chat_id": chat_id,
                "text": message,
                "parse_mode": "HTML"
            }
            
            print(f"Sending to subscriber {i+1}/{len(subscribers)}: {chat_id}")
            response = requests.post(send_url, data=send_data)
            
            if response.status_code == 200:
                success_count += 1
            else:
                response_json = response.json()
                if response.status_code == 403 or (response.status_code == 400 and "chat not found" in response.text.lower()):
                    # User blocked the bot or chat not found
                    print(f"⚠️ Removing subscriber {chat_id} (blocked bot or chat not found)")
                    removed_subscribers.append(chat_id)
                else:
                    print(f"❌ Failed to send to {chat_id}: {response.text}")
        except Exception as e:
            print(f"❌ Error sending to {chat_id}: {e}")
    
    # Remove blocked users from subscribers list
    if removed_subscribers:
        updated_subscribers = [s for s in subscribers if s not in removed_subscribers]
        try:
            with open(subscribers_file, 'w') as f:
                json.dump(updated_subscribers, f)
            print(f"✅ Removed {len(removed_subscribers)} blocked subscribers")
        except Exception as e:
            print(f"❌ Error updating subscribers file: {e}")
    
    print(f"📊 Notified {success_count}/{len(subscribers)} subscribers")
    return success_count > 0

def handle_bot_commands(bot_token):
    """Check for new commands from users and handle them"""
    if not bot_token:
        print("⚠️ WARNING: Telegram bot token not configured, skipping command handling")
        return
    
    print("🔍 Checking for new bot commands...")
    
    # Load subscribers list
    subscribers_file = 'telegram_subscribers.json'
    try:
        if os.path.exists(subscribers_file):
            with open(subscribers_file, 'r') as f:
                subscribers = json.load(f)
        else:
            subscribers = []
            with open(subscribers_file, 'w') as f:
                json.dump(subscribers, f)
    except Exception as e:
        print(f"❌ Error loading subscribers: {e}")
        return
    
    # Get updates from Telegram
    try:
        url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
        response = requests.get(url)
        
        if response.status_code != 200:
            print(f"❌ Failed to get updates from Telegram: {response.text}")
            return
        
        updates = response.json()
        
        if not updates.get('ok'):
            print(f"❌ Error in Telegram response: {updates}")
            return
        
        # Load current volumes
        volumes_file = 'volumes_found.txt'
        current_volumes = []
        if os.path.exists(volumes_file):
            with open(volumes_file, 'r') as f:
                content = f.read().strip()
                if content:
                    current_volumes = [int(vol) for vol in content.split(',')]
        
        current_volumes_text = ', '.join(f"Vol {vol}" for vol in current_volumes) if current_volumes else "None"
        
        # Process each update
        for update in updates.get('result', []):
            if 'message' not in update:
                continue
                
            message = update.get('message')
            chat_id = message.get('chat', {}).get('id')
            text = message.get('text', '')
            
            if not chat_id or not text:
                continue
                
            # Convert chat_id to string for consistent handling
            chat_id = str(chat_id)
            
            # Handle /start command
            if text.startswith('/start'):
                if chat_id not in subscribers:
                    subscribers.append(chat_id)
                    welcome_message = (
                        "🚀 Welcome to the AIEngineerPack Monitor Bot!\n\n"
                        "You're now subscribed to receive notifications when new AIEngineerPack volumes are released.\n\n"
                        f"Current volumes: {current_volumes_text}\n\n"
                        "Commands:\n"
                        "/status - Check monitor status\n"
                        "/stop - Unsubscribe from notifications"
                    )
                    send_telegram_notification(welcome_message, bot_token, chat_id)
                else:
                    send_telegram_notification("You're already subscribed to AIEngineerPack notifications!", bot_token, chat_id)
            
            # Handle /stop command
            elif text.startswith('/stop'):
                if chat_id in subscribers:
                    subscribers.remove(chat_id)
                    send_telegram_notification("✅ You've been unsubscribed from AIEngineerPack notifications.", bot_token, chat_id)
                else:
                    send_telegram_notification("You weren't subscribed to notifications.", bot_token, chat_id)
            
            # Handle /status command
            elif text.startswith('/status'):
                status_message = (
                    f"📊 AIEngineerPack Monitor Status:\n\n"
                    f"🔍 Currently monitoring for new volumes beyond {current_volumes_text}\n"
                    f"🕒 Checks run twice daily at 8:00 AM & 8:00 PM US Eastern Time\n"
                    f"👥 {len(subscribers)} users subscribed to notifications\n\n"
                    f"📱 You'll be notified as soon as new volumes are released!"
                )
                send_telegram_notification(status_message, bot_token, chat_id)
            
            # Handle /help command
            elif text.startswith('/help'):
                help_message = (
                    "📚 AIEngineerPack Monitor Bot Help:\n\n"
                    "/start - Subscribe to notifications\n"
                    "/stop - Unsubscribe from notifications\n"
                    "/status - Check current monitor status\n"
                    "/help - Show this help message\n\n"
                    "This bot monitors the AIEngineerPack website for new volume releases and sends you notifications when new volumes are detected."
                )
                send_telegram_notification(help_message, bot_token, chat_id)
        
        # Save updated subscribers list
        with open(subscribers_file, 'w') as f:
            json.dump(subscribers, f)
            
        # Clear processed updates
        if updates.get('result'):
            last_update_id = updates['result'][-1]['update_id']
            requests.get(f"{url}?offset={last_update_id + 1}")
            
        print(f"✅ Processed bot commands, current subscribers: {len(subscribers)}")
            
    except Exception as e:
        print(f"❌ Error handling bot commands: {e}")

def check_for_new_volumes(dry_run=False, force_notify=False):
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
    
    if dry_run:
        print("🔍 DRY RUN MODE: Will check for volumes but not send notifications or process bot commands")
    else:
        # Handle any pending bot commands first
        handle_bot_commands(telegram_bot_token)
    
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

The script will now check for new volumes twice daily (8:00 AM & 8:00 PM US Eastern Time).
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
        
        if new_volumes or force_notify:
            if force_notify and not new_volumes:
                print("🔔 Force notification requested. Sending notifications for current volumes.")
                new_volumes = volumes_found  # Use all volumes when forcing notification
            
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"🎉 {'New' if not force_notify else 'Current'} volumes detected at {timestamp}: {new_volumes}")
            
            # Create notification messages
            email_subject = "New AIEngineerPack Volume Released!"
            email_message = f"""
New volume{'s' if len(new_volumes) > 1 else ''} detected on {url} at {timestamp}:

{', '.join(f'Vol {vol}' for vol in new_volumes)} {'have' if len(new_volumes) > 1 else 'has'} been released!

Visit the website to claim your offers: {url}
            """
            
            # Format for Discord with markdown
            discord_message = f"""**New AIEngineerPack Volume Released!**

New volume{'s' if len(new_volumes) > 1 else ''} detected on {url} at {timestamp}:

{', '.join(f'Vol {vol}' for vol in new_volumes)} {'have' if len(new_volumes) > 1 else 'has'} been released!

Visit the website to claim your offers: {url}"""
            
            # Format for Telegram with HTML
            telegram_message = f"<b>New AIEngineerPack Volume Released!</b>\n\nNew volume{'s' if len(new_volumes) > 1 else ''} detected on {url} at {timestamp}:\n\n{', '.join(f'Vol {vol}' for vol in new_volumes)} {'have' if len(new_volumes) > 1 else 'has'} been released!\n\nVisit the website to claim your offers: {url}"
            
            # Send notifications
            notifications_sent = 0
            
            if dry_run:
                print("🔍 DRY RUN MODE: Would have sent the following notifications:")
                print(f"📧 Email: {email_subject}")
                print(f"💬 Discord: {discord_message}")
                print(f"📱 Telegram: {telegram_message}")
                print(f"🤖 Public subscribers: Would notify {len(subscribers) if 'subscribers' in locals() else '?'} subscribers")
                
                # Print full message examples for debugging in dry-run mode
                print("\n🔍 EMAIL MESSAGE WOULD BE:")
                print(email_message)
                print("\n🔍 DISCORD MESSAGE WOULD BE:")
                print(discord_message)
                print("\n🔍 TELEGRAM MESSAGE WOULD BE:")
                print(telegram_message)
            else:
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
                
                # Notify all public subscribers
                if notify_public_subscribers(new_volumes, volumes_found, url, timestamp, telegram_bot_token):
                    notifications_sent += 1
                    print("🤖 Notifications sent to public subscribers!")
                    
                if notifications_sent == 0:
                    print("⚠️ WARNING: No notifications were sent successfully. Please check your configuration.")
        else:
            print("ℹ️ No new volumes detected.")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Check AIEngineerPack website for new volumes")
    parser.add_argument("--dry-run", action="store_true", help="Check for new volumes but don't send notifications")
    parser.add_argument("--force-notify", action="store_true", help="Force send notification even if no new volumes")
    args = parser.parse_args()
    
    print("🚀 Starting AIEngineerPack volume check...")
    check_for_new_volumes(dry_run=args.dry_run, force_notify=args.force_notify)
    print("✅ Check completed!") 