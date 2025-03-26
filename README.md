# AIEngineerPack Monitor

This script monitors the [AIEngineerPack website](https://www.aiengineerpack.com/) for changes and sends notifications when updates are detected, such as when a new volume (Vol 4) is released.

## Setup

1. Make sure you have Python 3.6+ installed
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Running the Monitor

Simply run the script:
```
python website_monitor.py
```

The script will:
- Check the website every hour (configurable)
- Save snapshots of the site when changes are detected
- Notify you of changes via console output

## Email Notifications (Optional)

To receive email notifications:

1. Edit `website_monitor.py`
2. Uncomment and fill in the `email_config` section with your email details
3. For Gmail, you'll need to use an App Password (not your regular password)

## Customization

You can modify these settings in `website_monitor.py`:
- Change the check interval (default: 60 minutes)
- Change the target URL (if needed)
- Adjust notification settings

## Running as a Background Service

### Windows

1. Create a batch file `start_monitor.bat`:
   ```
   @echo off
   pythonw website_monitor.py
   ```

2. Add this batch file to your startup folder or create a scheduled task

### Linux/macOS

1. Create a systemd service or use cron to run the script regularly

## Troubleshooting

If you encounter any issues:
- Check your internet connection
- Verify email settings if using email notifications
- Make sure the `monitor_data` directory is writable 