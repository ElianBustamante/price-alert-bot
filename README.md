# Price Alert Bot

A Python script that monitors Google Shopping prices and sends real-time WhatsApp alerts via CallMeBot. It automatically handles currency conversions and compares prices against your custom limits.

---

## Key Features

- **Dual-Region Search**: Scrapes Google Shopping in both your local country and the US simultaneously.
- **Smart Deduplication**: Automatically filters out duplicate products from the same store.
- **Strict Exclusion Filters**: Use negative keywords (like `-EVO` or `-Aliexpress`) to ban specific models or block unwanted sellers.
- **WhatsApp Alerts**: Sends deals directly to your phone, automatically bypassing CallMeBot's character limits.
- **Always-On Reporting**: Messages you even if no deals are found, including a backup link to verify the results.
- **Serverless**: Runs entirely on GitHub Actions for free. No Heroku or 24/7 servers needed.

---

## Tech Stack

- **Python 3.11+**
- **SerpAPI** (Google Shopping scraper) & **CallMeBot API** (WhatsApp gateway)
- **GitHub Actions** (Serverless CI/CD & Cron Job Scheduler)
- **pytest** & **pytest-mock** (Unit testing and API mocking)
- **requests** (HTTP client) & **python-dotenv** (Environment management)

---

## Setup & Installation

### 1. Requirements

- [SerpAPI](https://serpapi.com/) account (Free tier is sufficient)
- [CallMeBot](https://www.callmebot.com/) activation for WhatsApp (Send `I allow callmebot to send me messages` to `+1 (206) 337-5567` on WhatsApp)

### 2. Running Locally

```bash
git clone https://github.com/ElianBustamante/price-alert-bot.git
cd price-alert-bot
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/macOS
.\venv\Scripts\activate   # Windows

pip install -r requirements.txt
cp .env.example .env       # Fill in your variables
python run_now.py
```

---

## GitHub Actions Deployment

This bot is configured to run completely free on GitHub Actions.

1. Fork or push this repository to your own GitHub account.
2. Go to your repository **Settings** > **Secrets and variables** > **Actions**.
3. Add all the variables from your `.env` file as **Repository Secrets**.
4. Go to the **Actions** tab in GitHub and enable workflows.
5. The bot will automatically run twice a day (configured in `.github/workflows/price-alert.yml`). You can also run it manually at any time by clicking **Run workflow**.
