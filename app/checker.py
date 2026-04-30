import os
from typing import List, Dict, Any
from dotenv import load_dotenv
from app import converter

load_dotenv()

def check_prices(prices: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Checks a list of prices against the configured limits in .env.
    Returns only the items that trigger an alert, adding price_usd, price_clp, and triggered_by fields.
    """
    # Load limits, defaulting to 0 if missing or invalid
    try:
        limit_usd = float(os.getenv("PRICE_LIMIT_USD", "0"))
        limit_clp = float(os.getenv("PRICE_LIMIT_CLP", "0"))
    except ValueError:
        limit_usd = 0.0
        limit_clp = 0.0

    alerts = []
    
    for item in prices:
        # Create a copy to avoid mutating the original list
        checked_item = item.copy()
        
        val = checked_item["price_value"]
        cur = checked_item["currency"]
        
        price_usd = converter.to_usd(val, cur)
        price_clp = int(converter.to_clp(val, cur))
        
        checked_item["price_usd"] = price_usd
        checked_item["price_clp"] = price_clp
        
        trigger_usd = price_usd <= limit_usd
        trigger_clp = price_clp <= limit_clp
        
        if trigger_usd and trigger_clp:
            checked_item["triggered_by"] = "BOTH"
            alerts.append(checked_item)
        elif trigger_usd:
            checked_item["triggered_by"] = "USD"
            alerts.append(checked_item)
        elif trigger_clp:
            checked_item["triggered_by"] = "CLP"
            alerts.append(checked_item)
            
    return alerts
