# AIEngineerPack Volume Monitor

This tool automatically checks [AIEngineerPack](https://www.aiengineerpack.com/) for new volume releases and sends you notifications via Telegram, Discord, or email when new volumes are detected.

![AIEngineerPack Monitor](https://i.imgur.com/TBD.png)

## Features

✅ **Real-time monitoring** - Checks twice daily for new volume releases  
✅ **Multi-platform notifications** - Supports Telegram, Discord, and email  
✅ **Zero cost** - Runs entirely on GitHub's free tier  
✅ **Zero maintenance** - Set it up once and forget it  
✅ **Privacy focused** - Your notification details stay private  

## How It Works

The monitor runs automatically on GitHub Actions twice per day and:

1. Scans the AIEngineerPack website specifically for volume numbers
2. Compares with previously detected volumes
3. Sends notifications when new volumes are released
4. Works continuously in the background with no interaction needed

## Quick Setup (5 minutes)

### 1. Fork This Repository

Click the "Fork" button at the top right of this repository.

### 2. Set Up Notifications

Choose one or more notification methods:

#### Telegram (Recommended)

1. Start a chat with [@BotFather](https://t.me/BotFather) on Telegram
2. Send `/newbot` command and follow prompts to create a bot
3. Get your bot token from BotFather
4. Send a message to your new bot
5. Get your chat ID:
   - Visit `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
   - Find the "id" field in the chat section

6. Add these to your repository secrets:
   - Name: `TELEGRAM_BOT_TOKEN` – Value: Your bot token
   - Name: `TELEGRAM_CHAT_ID` – Value: Your chat ID

#### Discord (Optional)

1. In your Discord server, go to Server Settings → Integrations → Webhooks
2. Create a new webhook and copy the URL
3. Add to repository secrets:
   - Name: `DISCORD_WEBHOOK_URL` – Value: Your webhook URL

#### Email (Optional)

1. Create a Gmail App Password (Google Account → Security → App Passwords)
2. Add to repository secrets:
   - Name: `EMAIL_USERNAME` – Value: Your Gmail address
   - Name: `EMAIL_PASSWORD` – Value: Your App Password
   - Name: `EMAIL_FROM` – Value: Your Gmail address

### 3. Enable GitHub Actions

1. In your forked repository, go to Actions tab
2. Click "I understand my workflows, go ahead and enable them"
3. Run the workflow manually once to test:
   - Click on "Check AIEngineerPack for New Volumes"
   - Click "Run workflow" → "Run workflow"

You'll receive a confirmation message shortly if everything is configured correctly!

## Files Overview

- `check_aiengineerpack.py` - Main monitoring script
- `.github/workflows/check_website.yml` - GitHub Actions workflow configuration
- `volumes_found.txt` - Tracks previously discovered volumes
- `requirements.txt` - Python dependencies

## Customization

- **Checking frequency**: Edit the cron schedule in `.github/workflows/check_website.yml`
- **Notification message**: Modify the message templates in `check_aiengineerpack.py`

## Troubleshooting

If you're not receiving notifications:

1. Check the Actions tab to see if the workflow runs successfully
2. Verify your notification credentials in repository secrets
3. For Telegram, ensure you've started a chat with your bot
4. For Discord, check webhook URL and permissions
5. For email, verify you're using an App Password, not your regular password

## Privacy & Security

- Your notification credentials are stored as GitHub secrets and not exposed
- The monitor only tracks AIEngineerPack volume numbers, not personal data
- Your bot tokens and webhooks are only used to send notifications

## License

MIT License - Feel free to modify and use as needed.

---

Created by [@realranjan](https://github.com/realranjan) 