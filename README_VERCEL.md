# AIEngineerPack Monitor - Vercel Deployment

This project creates a serverless function that checks the AIEngineerPack website for changes and sends email notifications when updates (like a new Vol 4) are detected.

## How It Works

- The function runs hourly via Vercel Cron Jobs
- It checks https://www.aiengineerpack.com/ for changes
- When changes are detected, it sends an email to ranjanvernekar45@gmail.com

## Deployment to Vercel

### Prerequisites

1. Create a Vercel account at [vercel.com](https://vercel.com) (free)
2. Install the Vercel CLI:
   ```
   npm install -g vercel
   ```
3. Have a Gmail account for sending notifications

### Steps to Deploy

1. **Install Vercel CLI and login**
   ```
   npm install -g vercel
   vercel login
   ```

2. **Clone this repository or prepare your files**
   Make sure you have:
   - `api/check_website.py`
   - `vercel.json`
   - `requirements.txt`

3. **Set up environment variables**
   
   Create a `.env` file based on `.env.example`:
   ```
   EMAIL_USERNAME=your-gmail@gmail.com
   EMAIL_PASSWORD=your-app-password
   EMAIL_FROM=your-gmail@gmail.com
   ```
   
   For Gmail, you need to [create an App Password](https://support.google.com/accounts/answer/185833).

4. **Deploy to Vercel**
   ```
   vercel
   ```
   
   During deployment, Vercel will ask you to confirm some settings and also prompt you to add your environment variables.

5. **Set up environment variables in Vercel Dashboard**
   
   After deploying, go to your Vercel dashboard, select your project, and:
   - Go to Settings → Environment Variables
   - Add the environment variables from your `.env` file

6. **Set up Vercel KV (Redis) for persistent storage**

   Vercel KV is a Redis database that works seamlessly with Vercel functions.
   
   a. In your Vercel dashboard, go to "Storage" and create a new KV Database
   
   b. Connect the KV database to your project
   
   c. Vercel will automatically add the REDIS_URL environment variable to your project
   
   This allows the script to remember the previous state of the website between executions.

7. **Enable Cron Jobs**
   
   Make sure you're on at least the Pro plan ($20/mo) to use Cron Jobs, or check if there's a free allowance for your account.

   In your project settings, verify that the Cron Job is enabled for `/api/check` running hourly.

## Testing Your Deployment

After deployment, you can test your function by visiting:
```
https://your-project-name.vercel.app/api/check
```

This should return a JSON response indicating whether the script is working.

## Alternative Storage Options

If you don't want to use Vercel KV, you have other options:

1. **Vercel Postgres**: Similar setup to KV but using a Postgres database
2. **MongoDB Atlas**: Free tier available, update the script to use MongoDB
3. **Upstash Redis**: Another Redis provider with a generous free tier

## Pricing Considerations

- **Vercel Hobby Plan (Free)**: Limited to 12 serverless function executions per day
- **Vercel Pro Plan ($20/month)**: Includes Cron Jobs and more executions
- **Vercel KV**: Has its own pricing based on usage
- **Gmail**: Free for sending emails through SMTP

## Troubleshooting

- If emails aren't being sent, check that your Gmail app password is correct
- Ensure all environment variables are set in the Vercel dashboard
- Check the function logs in the Vercel dashboard for any errors

## Alternative to Vercel

If you find Vercel's pricing too high, consider these alternatives:

1. **GitHub Actions**: Free for public repositories, can run scheduled jobs
2. **Fly.io**: Generous free tier, can run persistent applications
3. **Render**: Free tier with limited usage, but enough for this use case