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
    
    # Dividir las alertas en grupos de 4 para no exceder el límite de texto de CallMeBot
    import time
    alerts_chunks = [alerts[i:i + 4] for i in range(0, len(alerts), 4)]
    all_success = True
    
    for index, chunk in enumerate(alerts_chunks):
        message_lines = [header]
        if index == 0:
            message_lines.append(f"*{product_name}*")
            message_lines.append(f"Mostrando {len(alerts)} resultados...")
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
            # Reemplazar espacios por %20 para que WhatsApp no corte el enlace
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
            time.sleep(2) # Esperar 2 segundos entre mensajes para evitar bloqueo por spam
            
    return all_success
