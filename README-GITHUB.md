# AIEngineerPack Monitor - Free Forever

This project monitors the AIEngineerPack website (https://www.aiengineerpack.com/) for changes and sends you email notifications when updates are detected, such as when a new volume (Vol 4) is released.

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

You can either:
- Use the GitHub web interface to upload files
- Use git commands if you're familiar with them

### Step 3: Set Up Email Secrets

1. In your GitHub repository, go to "Settings" → "Secrets and variables" → "Actions"
2. Click "New repository secret" and add these three secrets:

   | Name | Value |
   |------|-------|
   | EMAIL_USERNAME | Your Gmail address (that will send emails) |
   | EMAIL_PASSWORD | Your Gmail App Password (not your regular password) |
   | EMAIL_FROM | Your Gmail address (same as EMAIL_USERNAME) |

#### Creating a Gmail App Password:
1. Go to your [Google Account](https://myaccount.google.com/)
2. Select "Security" → "2-Step Verification" (enable if not already on)
3. At the bottom, select "App passwords"
4. Select "Mail" as the app and "Other" as the device
5. Enter "AIEngineerPack Monitor" as the name
6. Copy the generated 16-character password

### Step 4: Run Manually (Optional)

1. Go to the "Actions" tab in your repository
2. Select the "Check AIEngineerPack Website" workflow
3. Click "Run workflow" → "Run workflow"

This will run the check immediately to confirm everything works.

## How It Works

- The script runs automatically twice a day (8:00 AM and 8:00 PM UTC)
- It checks if the AIEngineerPack website has changed
- If changes are detected, it sends an email to ranjanvernekar45@gmail.com
- The website hash is stored in GitHub between runs

## Cost

This setup is **completely free** and will remain free forever. GitHub Actions provides:
- Free unlimited minutes for public repositories
- Free scheduled runs (cron jobs)
- No credit card required

## Troubleshooting

If you're not receiving emails:
1. Check the Actions tab to see if the workflow is running
2. Verify your secrets are set correctly
3. Make sure you used an App Password for Gmail, not your regular password

## Customizing

- To change how often it checks, edit the cron schedule in `.github/workflows/check_website.yml`
- To change the notification email, edit the `'to'` field in `check_aiengineerpack.py` 