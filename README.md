# SSD Price Alert Bot

A Python-based automated bot that monitors product prices (e.g., Samsung SSD 990 PRO) on Google Shopping using SerpAPI. It automatically converts currencies to evaluate price limits and sends real-time WhatsApp alerts via CallMeBot if a product falls below your desired price threshold.

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
   - `PRODUCT_QUERY`: The product you want to search for
   - `PRICE_LIMIT_USD` and `PRICE_LIMIT_CLP`: Your limits

4. **How to activate CallMeBot**
   To get your API key, send the activation message (e.g., `I allow callmebot to send me messages`) to `+1 (206) 337-5567` on WhatsApp. They will reply with your API Key.

5. **How to run the test**
   Ensure your `.env` is configured correctly with CallMeBot variables, then run:
   ```bash
   python send_test.py
   ```
   You should receive a fake alert on your WhatsApp.

6. **How to run the bot locally**
   ```bash
   python app/scheduler.py
   ```
   The bot will run continuously and check prices twice a day (9:00 AM and 9:00 PM).

7. **How to deploy to Railway**
   - Connect your GitHub repository to Railway.
   - Railway will automatically detect the `Procfile`.
   - Go to the "Variables" tab in Railway and add all the variables from your `.env` file.
   - Deploy!

## Configuration

**How to change the price limits:**
Edit `PRICE_LIMIT_USD` and `PRICE_LIMIT_CLP` in your `.env` file. If the price falls below EITHER of these limits, an alert will be sent.

**How to change the check frequency:**
Edit `CHECK_INTERVAL_HOURS` in your `.env` file (if you choose to implement a dynamic interval) and update the `CronTrigger` inside `app/scheduler.py`.