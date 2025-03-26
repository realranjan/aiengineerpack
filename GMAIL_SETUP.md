# Setting Up Gmail for AIEngineerPack Monitor

To receive email notifications at ranjanvernekar45@gmail.com, you need to configure the script to send emails from a Gmail account. Here's how to set it up:

## Step 1: Choose a Gmail Account to Send From

You can use your own Gmail account or create a new one specifically for sending notifications.

## Step 2: Generate an App Password

Google doesn't allow regular passwords for programmatic email access. You need to generate an "App Password":

1. Go to your [Google Account](https://myaccount.google.com/)
2. Select "Security" from the left menu
3. Under "Signing in to Google," select "2-Step Verification" (enable it if not already on)
4. At the bottom of the page, select "App passwords"
5. Click "Select app" and choose "Mail"
6. Click "Select device" and choose "Other (Custom name)"
7. Enter "AIEngineerPack Monitor" and click "Generate"
8. Google will display a 16-character password - **copy this password**

## Step 3: Update the Script Configuration

Open `website_monitor.py` and edit the `email_config` section:

```python
email_config = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 465,
    'username': 'YOUR_EMAIL@gmail.com',  # Replace with your Gmail address
    'password': 'YOUR_APP_PASSWORD',     # Replace with the app password you generated
    'from': 'YOUR_EMAIL@gmail.com',      # Replace with your Gmail address
    'to': 'ranjanvernekar45@gmail.com'
}
```

Replace:
- `YOUR_EMAIL@gmail.com` with the Gmail address you're sending from
- `YOUR_APP_PASSWORD` with the 16-character app password you generated

## Step 4: Test the Configuration

Run the script to test if emails are being sent properly:

```
python website_monitor.py
```

The first run will only save the website's current state. To test email sending, you can modify the script temporarily to force a notification.

## Troubleshooting

- If emails aren't being sent, check your app password and make sure it's entered correctly
- Ensure your sending Gmail account has less secure app access enabled
- Check the console output for any error messages 