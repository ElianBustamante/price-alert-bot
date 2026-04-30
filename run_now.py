import os
import asyncio
import logging
from dotenv import load_dotenv

from app.scraper import get_prices
from app.checker import check_prices
from app.notifier import send_whatsapp

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Re-using the exact same logic we had in the scheduler
def price_check_job():
    product_query = os.getenv("PRODUCT_QUERY", "Samsung SSD 990 PRO 1TB Heatsink")
    
    logger.info(f"Starting price check execution for: {product_query}")
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
    logger.info("Running manual/GitHub Actions price check...")
    price_check_job()
    logger.info("Execution finished.")
