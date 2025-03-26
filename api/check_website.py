import requests
import hashlib
import os
import smtplib
from email.message import EmailMessage
import json
import redis

def connect_to_redis():
    """Connect to Vercel KV (Redis) if credentials are available"""
    redis_url = os.environ.get('REDIS_URL', None)
    if redis_url:
        return redis.from_url(redis_url)
    return None

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
        return True
    except Exception as e:
        print(f"Failed to send email notification: {e}")
        return False

def handler(request):
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
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Email credentials not configured in environment variables"})
        }
    
    url = "https://www.aiengineerpack.com/"
    
    try:
        # Get website content
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30)
        
        if response.status_code != 200:
            return {
                "statusCode": response.status_code,
                "body": json.dumps({"error": f"Failed to retrieve website. Status code: {response.status_code}"})
            }
        
        content = response.text
        current_hash = hashlib.md5(content.encode()).hexdigest()
        
        # Connect to Redis (Vercel KV) if available
        redis_client = connect_to_redis()
        
        if redis_client:
            # Use Redis for state management
            previous_hash = redis_client.get('aiengineer_previous_hash')
            if previous_hash:
                previous_hash = previous_hash.decode('utf-8')
            
            if not previous_hash:
                # First run, save hash
                redis_client.set('aiengineer_previous_hash', current_hash)
                return {
                    "statusCode": 200,
                    "body": json.dumps({"message": "First run, hash saved in Redis", "hash": current_hash})
                }
            
            if current_hash != previous_hash:
                # Website changed
                subject = "AIEngineerPack Website Change Detected!"
                message = f"""
Change detected on {url}

The website content has changed. Check it out to see if a new volume (like Vol 4) has been released!

Visit the website: {url}
                """
                
                send_email_notification(subject, message, email_config)
                
                # Update hash
                redis_client.set('aiengineer_previous_hash', current_hash)
                
                return {
                    "statusCode": 200,
                    "body": json.dumps({"message": "Change detected and notification sent!", "old_hash": previous_hash, "new_hash": current_hash})
                }
                
            return {
                "statusCode": 200,
                "body": json.dumps({"message": "No changes detected (Redis state)", "hash": current_hash})
            }
            
        else:
            # Fallback to environment variable if Redis not available
            previous_hash = os.environ.get('PREVIOUS_HASH')
            
            if not previous_hash:
                # Can't update env vars on Vercel, so just log this
                return {
                    "statusCode": 200,
                    "body": json.dumps({
                        "message": "First run, but cannot save hash (no Redis). Set PREVIOUS_HASH env var to: " + current_hash,
                        "hash": current_hash
                    })
                }
            
            if current_hash != previous_hash:
                # Website changed
                subject = "AIEngineerPack Website Change Detected!"
                message = f"""
Change detected on {url}

The website content has changed. Check it out to see if a new volume (like Vol 4) has been released!

Visit the website: {url}
                """
                
                send_email_notification(subject, message, email_config)
                
                return {
                    "statusCode": 200,
                    "body": json.dumps({
                        "message": "Change detected and notification sent! Update PREVIOUS_HASH env var to: " + current_hash,
                        "old_hash": previous_hash,
                        "new_hash": current_hash
                    })
                }
            
            return {
                "statusCode": 200,
                "body": json.dumps({"message": "No changes detected (env var state)", "hash": current_hash})
            }
        
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        } 