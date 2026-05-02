# Smart Price Alert Bot

A Python-based automated bot that monitors any product's prices on Google Shopping using SerpAPI. It continuously scrapes both local and international stores, automatically converts currencies to evaluate your predefined price limits, and sends real-time WhatsApp alerts via CallMeBot if a product falls below your desired price threshold.

## Features
- **Dual-Region Search**: Simultaneously scrapes your local country's Google Shopping and the United States to ensure you get both local retail options and international deals (like Amazon or eBay).
- **Smart Store Deduplication**: Automatically filters out duplicate listings from the same store, ensuring you get a clean list of top unique retailers.
- **WhatsApp Pagination**: Bypasses CallMeBot character limits by sending 1 product per message with built-in rate-limiting delays to avoid spam blocks.
- **Empty State Notifications**: Proactively notifies you via WhatsApp even if no products were found under the price limit, including backup SerpAPI HTML links to manually verify the Google Shopping results.
- **Serverless Architecture**: Runs entirely on GitHub Actions via Cron jobs. No servers, Heroku, or Railway deployment needed!

## Requirements
- Python 3.11+
- [SerpAPI](https://serpapi.com/) account (Free tier is sufficient)
- [CallMeBot](https://www.callmebot.com/) activation for WhatsApp

## Setup Steps

1. **Clone the repo**
   ```bash
   git clone https://github.com/ElianBustamante/price-alert-bot.git
   cd price-alert-bot
   ```

2. **Install dependencies**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Mac/Linux:
   # source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**
   Copy `.env.example` to `.env` and fill in all variables:
   - `SERPAPI_KEY`: Your SerpAPI key
   - `PHONE_NUMBER`: Your WhatsApp number (e.g., +56912345678)
   - `CALLMEBOT_KEY`: Your CallMeBot API key
   - `PRODUCT_QUERY`: The exact product you want to search for (e.g., "Sony WH-1000XM5 -refurbished")
   - `PRICE_LIMIT_USD` and `PRICE_LIMIT_CLP`: Your desired price limits.

4. **How to activate CallMeBot**
   To get your API key, send the activation message (e.g., `I allow callmebot to send me messages`) to `+1 (206) 337-5567` on WhatsApp. They will reply with your API Key.

5. **Test the Bot Locally**
   Ensure your `.env` is configured correctly, then run:
   ```bash
   python run_now.py
   ```
   You should receive your live price alerts directly on your WhatsApp.

## GitHub Actions Deployment

This bot is configured to run completely free on GitHub Actions.
1. Fork or push this repository to your own GitHub account.
2. Go to your repository **Settings** > **Secrets and variables** > **Actions**.
3. Add all the variables from your `.env` file as **Repository Secrets**.
4. Go to the **Actions** tab in GitHub and enable workflows.
5. The bot will automatically run twice a day (configured in `.github/workflows/price-alert.yml`). You can also run it manually at any time by clicking **Run workflow**.