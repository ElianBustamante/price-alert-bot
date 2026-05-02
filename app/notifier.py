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

    phone = os.getenv("PHONE_NUMBER")
    apikey = os.getenv("CALLMEBOT_KEY")
    
    if not phone or not apikey:
        logger.error("PHONE_NUMBER or CALLMEBOT_KEY is missing in environment variables.")
        return False

    header = "🧪 *[TEST] Alerta de precio!*" if is_test else "🚨 *Alerta de precio!*"
    
    has_cl = any(a.get("region") == "CL" for a in alerts)
    has_us = any(a.get("region") == "US" for a in alerts)
    
    missing_texts = []
    if not has_cl:
        missing_texts.append("⚠️ No se encontraron ofertas nacionales bajo el límite.")
    if not has_us:
        missing_texts.append("⚠️ No se encontraron ofertas internacionales bajo el límite.")
        
    if not alerts:
        timestamp = datetime.now().strftime("%d/%m/%Y a las %H:%M")
        message_lines = [
            header,
            f"*{product_name}*",
            "",
            *missing_texts,
            "",
            f"⏰ Revisado el {timestamp}"
        ]
        text_to_send = "\n".join(message_lines)
        params = {"phone": phone, "text": text_to_send, "apikey": apikey}
        try:
            response = requests.get("https://api.callmebot.com/whatsapp.php", params=params, timeout=10)
            if response.status_code == 200:
                logger.info("Empty alerts WhatsApp message sent successfully.")
                return True
            else:
                logger.error(f"Failed to send empty message. Status code: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"Exception while sending empty WhatsApp message: {e}")
            return False
            
    # Split alerts into groups of 1 to avoid exceeding CallMeBot's text limit
    import time
    alerts_chunks = [alerts[i:i + 1] for i in range(0, len(alerts), 1)]
    all_success = True
    
    for index, chunk in enumerate(alerts_chunks):
        message_lines = [header]
        if index == 0:
            message_lines.append(f"*{product_name}*")
            message_lines.append(f"Mostrando {len(alerts)} resultados...")
            if missing_texts:
                message_lines.append("")
                message_lines.extend(missing_texts)
        else:
            message_lines.append(f"*(Continuación {index+1}/{len(alerts_chunks)})*")
        message_lines.append("")
        
        for alert in chunk:
            store_raw = alert.get("store", "Desconocido")
            store = store_raw.split('.')[0].capitalize()
            
            price_usd = alert.get("price_usd", 0.0)
            price_clp = alert.get("price_clp", 0)
            price_usd_str = f"{price_usd:.2f}".replace(".", ",")
            
            trigger = alert.get("triggered_by", "UNKNOWN")
            # Replace spaces with %20 so WhatsApp doesn't break the link
            link = alert.get("link", "#").replace(" ", "%20")
            
            message_lines.append(f"🛒 *{store}*")
            message_lines.append(f"💵 USD: {price_usd_str}")
            message_lines.append(f"🇨🇱 CLP: {price_clp}")
            message_lines.append(f"🎯 Disparador: {trigger}")
            message_lines.append(f"🔗 {link}")
            message_lines.append("")
            
        if index == len(alerts_chunks) - 1:
            timestamp = datetime.now().strftime("%d/%m/%Y a las %H:%M")
            message_lines.append(f"⏰ Revisado el {timestamp}")
            
            unique_htmls = []
            for c in alerts_chunks:
                for a in c:
                    html = a.get("source_html")
                    if html and html not in unique_htmls:
                        unique_htmls.append(html)
                        
            for i, html in enumerate(unique_htmls):
                message_lines.append(f"📄 Respaldo HTML {i+1}: {html}")
        
        text_to_send = "\n".join(message_lines)
        params = {
            "phone": phone,
            "text": text_to_send,
            "apikey": apikey
        }
        
        try:
            response = requests.get("https://api.callmebot.com/whatsapp.php", params=params, timeout=10)
            if response.status_code == 200:
                logger.info(f"WhatsApp message chunk {index+1} sent successfully.")
            else:
                logger.error(f"Failed to send chunk {index+1}. Status code: {response.status_code}")
                all_success = False
        except Exception as e:
            logger.error(f"Exception while sending chunk {index+1}: {e}")
            all_success = False
            
        if len(alerts_chunks) > 1 and index < len(alerts_chunks) - 1:
            time.sleep(12) # Wait 12 seconds between messages to prevent strict spam blocking by CallMeBot
            
    return all_success
