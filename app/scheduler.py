import os
import asyncio
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from dotenv import load_dotenv

from app.scraper import get_prices
from app.checker import check_prices
from app.notifier import send_whatsapp

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

async def price_check_job():
    product_query = os.getenv("PRODUCT_QUERY", "Samsung SSD 990 PRO 1TB Heatsink")
    
    logger.info(f"Starting price check job for: {product_query}")
    try:
        # Step 1: Scrape prices
        prices = get_prices(product_query)
        logger.info(f"Fetched {len(prices)} results from SerpAPI.")
        
        # Step 2: Check against limits
        alerts = check_prices(prices)
        logger.info(f"{len(alerts)} results triggered a price alert.")
        
        # Step 3: Send notifications if any alerts exist
        if alerts:
            success = send_whatsapp(alerts, product_name=product_query, is_test=False)
            if success:
                logger.info("WhatsApp message sent successfully.")
            else:
                logger.error("Failed to send WhatsApp message.")
        else:
            logger.info("No alerts triggered. No WhatsApp message sent.")
            
    except Exception as e:
        logger.error(f"An error occurred during the price check job: {e}", exc_info=True)

if __name__ == "__main__":
    logger.info("Initializing Price Alert Bot Scheduler...")
    
    # Initialize scheduler
    scheduler = AsyncIOScheduler()
    
    # Schedule job at 9:00 AM and 9:00 PM (21:00) every day
    scheduler.add_job(
        price_check_job,
        trigger=CronTrigger(hour="9,21", minute="0"),
        id="price_check_job",
        name="Check prices twice a day",
        replace_existing=True
    )
    
    scheduler.start()
    
    logger.info("Scheduler started. Waiting for jobs to execute... (Press Ctrl+C to exit)")
    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Scheduler shutting down.")
