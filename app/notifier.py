import os
import requests
import logging
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def send_whatsapp(alerts: list[dict], product_name: str, is_test: bool = False) -> bool:
    """
    Sends a formatted WhatsApp message via CallMeBot API.
    Returns True if the message was sent successfully, False otherwise.
    """
    if not alerts:
        return False
        
    phone = os.getenv("PHONE_NUMBER")
    apikey = os.getenv("CALLMEBOT_KEY")
    
    if not phone or not apikey:
        logger.error("PHONE_NUMBER or CALLMEBOT_KEY is missing in environment variables.")
        return False

    header = "🧪 *[TEST] Alerta de precio!*" if is_test else "🚨 *Alerta de precio!*"
    
    message_lines = [
        header,
        f"*{product_name}*",
        ""
    ]
    
    for alert in alerts:
        store = alert.get("store", "Desconocido")
        price_usd = alert.get("price_usd", 0.0)
        price_clp = alert.get("price_clp", 0)
        trigger = alert.get("triggered_by", "UNKNOWN")
        link = alert.get("link", "#")
        
        message_lines.append(f"🛒 *{store}*")
        message_lines.append(f"💵 USD: ${price_usd}")
        message_lines.append(f"🇨🇱 CLP: ${price_clp}")
        message_lines.append(f"🎯 Disparador: {trigger}")
        message_lines.append(f"🔗 {link}")
        message_lines.append("")
        
    timestamp = datetime.now().strftime("%d/%m/%Y a las %H:%M")
    message_lines.append(f"⏰ Revisado el {timestamp}")
    
    # The requests library automatically URL-encodes the params dict
    text_to_send = "\n".join(message_lines)
    
    params = {
        "phone": phone,
        "text": text_to_send,
        "apikey": apikey
    }
    
    try:
        response = requests.get("https://api.callmebot.com/whatsapp.php", params=params, timeout=10)
        if response.status_code == 200:
            logger.info("WhatsApp message sent successfully.")
            return True
        else:
            logger.error(f"Failed to send WhatsApp message. Status code: {response.status_code}, Response: {response.text}")
            return False
    except Exception as e:
        logger.error(f"Exception while sending WhatsApp message: {e}")
        return False
