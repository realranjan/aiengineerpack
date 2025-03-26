# AIEngineerPack Volume Monitor - Free Forever

This project monitors the AIEngineerPack website for new volume releases (like Vol 4) and sends you notifications through email, Discord, and/or Telegram when new volumes are detected.

## Completely Free Setup (5 Minutes)

### Step 1: Create a GitHub Repository

1. Go to https://github.com/new
2. Name your repository (e.g., "aiengineerpack-monitor")
3. Make it Public (required for free GitHub Actions)
4. Click "Create repository"

### Step 2: Upload These Files

Upload these files to your new repository:
- `check_aiengineerpack.py`
- `requirements.txt`
- `.github/workflows/check_website.yml`
- `volumes_found.txt`

You can either:
- Use the GitHub web interface to upload files
- Use git commands if you're familiar with them

### Step 3: Set Up Notification Options

You can choose any or all of these notification methods:

#### Email Notifications

1. In your GitHub repository, go to "Settings" → "Secrets and variables" → "Actions"
2. Click "New repository secret" and add these three secrets:

   | Name | Value |
   |------|-------|
   | EMAIL_USERNAME | Your Gmail address (that will send emails) |
   | EMAIL_PASSWORD | Your Gmail App Password (not your regular password) |
   | EMAIL_FROM | Your Gmail address (same as EMAIL_USERNAME) |

##### Creating a Gmail App Password:
1. Go to your [Google Account](https://myaccount.google.com/)
2. Select "Security" → "2-Step Verification" (enable if not already on)
3. At the bottom, select "App passwords"
4. Select "Mail" as the app and "Other" as the device
5. Enter "AIEngineerPack Monitor" as the name
6. Copy the generated 16-character password

#### Discord Notifications

1. Create a Discord server or use an existing one
2. Go to Server Settings → Integrations → Webhooks
3. Click "New Webhook"
4. Name it "AIEngineerPack Monitor"
5. Choose the channel you want notifications in
6. Click "Copy Webhook URL"
7. Add this secret to your GitHub repository:

   | Name | Value |
   |------|-------|
   | DISCORD_WEBHOOK_URL | The webhook URL you copied |

#### Telegram Notifications

1. Start a chat with [@BotFather](https://t.me/BotFather) on Telegram
2. Send the command `/newbot` and follow instructions to create a bot
3. BotFather will give you a bot token (like `123456789:ABCdefGhIJKlmNoPQRsTUVwxyZ`)
4. Start a chat with your new bot
5. Get your chat ID by either:
   - Starting a chat with [@userinfobot](https://t.me/userinfobot)
   - OR visiting `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates` after messaging your bot
6. Add these secrets to your GitHub repository:

   | Name | Value |
   |------|-------|
   | TELEGRAM_BOT_TOKEN | Your bot token from BotFather |
   | TELEGRAM_CHAT_ID | Your chat ID (number like `123456789`) |

### Step 4: Run Manually (Optional)

1. Go to the "Actions" tab in your repository
2. Select the "Check AIEngineerPack for New Volumes" workflow
3. Click "Run workflow" → "Run workflow"

This will run the check immediately to confirm everything works.

## How It Works

- The script runs automatically twice a day (8:00 AM and 8:00 PM UTC)
- It specifically checks for new volumes on the AIEngineerPack website
- It currently knows about Vol 1, Vol 2, and Vol 3
- When a new volume (like Vol 4) is detected, it sends notifications to your configured channels
- The tracked volumes are stored in GitHub between runs

## What You'll Receive

When a new volume is detected, you'll get notifications like these:

### Email
```
Subject: New AIEngineerPack Volume Released!

New volume detected on https://www.aiengineerpack.com/ at 2023-10-15 08:00:00:

Vol 4 has been released!

Visit the website to claim your offers: https://www.aiengineerpack.com/
```

### Discord
A nicely formatted message in your Discord channel with the same information.

### Telegram
A notification on your Telegram with the same information.

## Cost

This setup is **completely free** and will remain free forever:
- GitHub Actions: Free for public repositories
- Discord webhooks: Free
- Telegram bots: Free
- Gmail SMTP: Free

## Troubleshooting

If you're not receiving notifications:
1. Check the Actions tab to see if the workflow is running
2. Verify your secrets are set correctly
3. For email, make sure you used an App Password for Gmail, not your regular password
4. For Discord, ensure the webhook URL is correct and the bot has permission to send messages
5. For Telegram, make sure you've started a chat with your bot and the chat ID is correct

## Email Privacy

If you don't want to use your personal Gmail account, you can:
1. Create a new Gmail account just for sending these notifications
2. Set up the App Password on that account instead
3. The emails will still be sent to ranjanvernekar45@gmail.com 