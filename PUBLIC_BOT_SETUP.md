# AIEngineerPack Telegram Notification Bot Setup

This guide explains how to set up notifications for new AIEngineerPack volume releases through Telegram without requiring any external hosting.

## Overview

The updated system now uses GitHub Actions to directly handle Telegram bot functionality. This simplifies the setup process significantly as everything runs directly in your GitHub repository without requiring external hosting like Replit.

## Setup Instructions

### Step 1: Create a Telegram Bot

1. **Create a Telegram Bot**:
   - Start a chat with [@BotFather](https://t.me/BotFather) on Telegram
   - Send the command `/newbot`
   - Follow the instructions to choose a name and username for your bot
   - Once created, you'll receive a **token** - keep this token secure, you'll need it later

2. **Optional: Customize your bot**:
   - Use `/setdescription` to add a description like "This bot sends notifications when new AIEngineerPack volumes are released"
   - Use `/setabouttext` to add information about the bot's purpose
   - Use `/setuserpic` to add a profile picture

### Step 2: Configure GitHub Secrets

1. Go to your GitHub repository containing the AIEngineerPack monitor
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Add the following secrets:
   - `TELEGRAM_BOT_TOKEN`: The token you received from BotFather
   - `TELEGRAM_CHAT_ID`: Your personal Telegram chat ID (for admin notifications)
   
   Optional (for additional notification methods):
   - Email configuration: `EMAIL_USERNAME`, `EMAIL_PASSWORD`, and `EMAIL_FROM`
   - Discord configuration: `DISCORD_WEBHOOK_URL`

### Step 3: How the Bot Works

The GitHub Actions workflow will:
1. Run automatically twice daily (8:00 AM and 8:00 PM UTC) to check for new volumes
2. Process any `/start`, `/stop`, `/status`, or `/help` commands from users
3. Maintain a list of subscribers in the `telegram_subscribers.json` file in your repository
4. Notify all subscribers when new volumes are detected

### Step 4: Finding Your Chat ID

To get your personal chat ID (for admin notifications):
1. Start a conversation with [@userinfobot](https://t.me/userinfobot) on Telegram
2. It will reply with your chat ID
3. Use this ID as the value for the `TELEGRAM_CHAT_ID` secret

### Using the Bot

#### For Administrators
- The GitHub Actions log will show detailed information about the bot's operations
- You can manually trigger the workflow from the "Actions" tab in your repository

#### For Users
To subscribe to notifications, users can:
1. Start a conversation with your bot on Telegram
2. Send the `/start` command to subscribe
3. Use `/stop` to unsubscribe
4. Use `/status` to check the current monitoring status
5. Use `/latest` to see all currently available volumes
6. Use `/website` to get a direct link to the AIEngineerPack site
7. Use `/feedback` to send feedback to the bot administrator
8. Use `/stats` to view usage statistics (subscribers only)
9. Use `/help` to see available commands

## Advanced Features

### User Feedback
The bot now includes a feedback system:
- Users can send feedback using the `/feedback` command followed by their message
- Feedback is stored in `user_feedback.json` in your repository
- As the bot administrator, you can review this file to see user suggestions and comments

### Usage Statistics
The bot automatically tracks usage statistics:
- Command usage frequency
- Daily activity patterns
- Subscriber count
- User engagement

This data is stored in `bot_stats.json` and can be viewed by subscribers using the `/stats` command.

### Enhanced Notifications
Notifications now include:
- Detailed formatting with emojis for better readability
- Direct link to the website
- Total count of available volumes
- Command shortcuts to check latest volumes

## Testing the Bot

1. Make a small change to the `volumes_found.txt` file in your repository
2. Run the GitHub workflow manually from the Actions tab
3. Check that your bot processes commands and sends notifications correctly

## Troubleshooting

- **Commands not working**: Verify your `TELEGRAM_BOT_TOKEN` is correct
- **Not receiving notifications**: Ensure you've started a chat with the bot and used the `/start` command
- **Workflow errors**: Check the GitHub Actions logs for detailed error messages

---

This simplified approach eliminates the need for external hosting services like Replit, making the setup process more streamlined and maintenance-free. 