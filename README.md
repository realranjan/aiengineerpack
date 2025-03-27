# AIEngineerPack Volume Monitor

A free, automatic tool that monitors [AIEngineerPack](https://www.aiengineerpack.com/) for new volume releases (like Vol 4) and sends instant notifications to your Telegram, Discord, or email.

## Public Telegram Channel

For instant updates without any setup, just join our public channel:
**[@aiengineernotify](https://t.me/aiengineernotify)**

## What This Does

This tool runs entirely on GitHub Actions (free forever) and:

- Checks twice daily (8:00 AM & 8:00 PM US Eastern Time) for new AIEngineerPack volumes
- Detects when volumes beyond Vol 1, 2, and 3 appear
- Sends immediate notifications via Telegram, Discord, or email
- Works 24/7 with zero maintenance

## Telegram Bot Commands

When you set up your own Telegram bot, users can interact with it using these commands:

- `/start` - Subscribe to notifications and see current volumes
- `/stop` - Unsubscribe from notifications
- `/status` - Check bot status and subscriber count
- `/latest` - See all currently available volumes
- `/website` - Get a direct link to the AIEngineerPack website
- `/feedback` - Send feedback to the bot administrator
- `/stats` - View usage statistics (for subscribers only)
- `/help` - Show all available commands

## Create Your Own Monitor (Optional)

If you want your own private notifications instead of using the public channel:

### 1. Fork This Repository

Click the "Fork" button at the top right of this page.

### 2. Set Up at Least One Notification Method

#### A. Telegram (Recommended)

1. Message [@BotFather](https://t.me/BotFather) on Telegram
2. Send `/newbot` and follow instructions to create a bot
3. Copy your bot token (looks like `123456789:ABCdefGhIJKlmNoPQRsTUVwxyZ`)
4. Message your new bot (at least once)
5. Get your chat ID:
   - Visit `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates` in your browser
   - Find the "id" number in the "chat" section (example: `7405584529`)

6. In your forked repository:
   - Go to Settings → Secrets and variables → Actions
   - Add two repository secrets:
     - Name: `TELEGRAM_BOT_TOKEN` – Value: Your bot token
     - Name: `TELEGRAM_CHAT_ID` – Value: Your chat ID

#### B. Discord (Optional)

1. In your Discord server:
   - Go to Server Settings → Integrations → Webhooks
   - Create a webhook and copy its URL
   
2. In your repository:
   - Add a secret named `DISCORD_WEBHOOK_URL` with the webhook URL as the value

#### C. Email (Optional)

1. Create a Gmail App Password:
   - Go to your Google Account → Security → 2-Step Verification → App passwords
   - Create a new app password

2. In your repository:
   - Add three secrets:
     - `EMAIL_USERNAME`: Your Gmail address
     - `EMAIL_PASSWORD`: The App Password you created
     - `EMAIL_FROM`: Your Gmail address

### 3. Start Monitoring

1. In your forked repository, go to Actions tab
2. Enable workflows if prompted
3. Click on "Check AIEngineerPack for New Volumes"
4. Click "Run workflow" → "Run workflow"

You'll get a confirmation message if everything works!

## That's It!

Your monitor is now running automatically. It will check for new AIEngineerPack volumes twice daily (8:00 AM & 8:00 PM Eastern Time) and notify you as soon as new ones (like Vol 4) appear. No further action needed!

## Testing

To test your notifications:
1. Edit `volumes_found.txt` in your repository
2. Change `1,2,3` to just `1,2`
3. Run the workflow manually
4. You should receive a notification about Vol 3 being "new"

## Troubleshooting

Not receiving notifications?

1. Check if the workflow is running (Actions tab)
2. Verify your notification credentials (Secrets)
3. For Telegram, make sure you sent at least one message to your bot
4. For Discord, verify the webhook URL and channel permissions
5. For email, ensure you used an App Password, not your regular password

## Contributing

Feel free to improve this tool! Just submit a pull request with your enhancements.

## License

MIT License - See [LICENSE](LICENSE) file.

---

Created by [@realranjan](https://github.com/realranjan) 