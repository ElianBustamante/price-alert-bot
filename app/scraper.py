import os
import re
from typing import List, Dict, Any
from dotenv import load_dotenv
from serpapi import GoogleSearch

load_dotenv()

def parse_price(raw: str) -> float:
    """
    Extract numeric value from strings like "$79.99", "$74.990", "USD 80", "CLP 72.990".
    Remove dots and commas correctly depending on format.
    """
    # Remove everything except digits, dots and commas
    clean_str = re.sub(r'[^\d.,]', '', raw).strip()
    if not clean_str:
        return 0.0
        
    # If the string ends with a dot/comma and 3 digits (e.g. .990), it's likely a thousands separator in CLP
    if re.search(r'\.\d{3}$', clean_str):
        clean_str = clean_str.replace('.', '')
    elif re.search(r',\d{3}$', clean_str):
        clean_str = clean_str.replace(',', '')
        
    # Replace remaining commas with dots for valid float parsing
    clean_str = clean_str.replace(',', '.')
    
    try:
        return float(clean_str)
    except ValueError:
        return 0.0

def detect_currency(raw: str, value: float) -> str:
    """
    Return "USD" if the string contains "$" or "USD" and the value is under 10.000
    Return "CLP" if the string contains "CLP" or the value is over 10.000
    Default to "USD" if uncertain
    """
    upper_raw = raw.upper()
    if "CLP" in upper_raw or value > 10000:
        return "CLP"
    if ("$" in upper_raw or "USD" in upper_raw) and value <= 10000:
        return "USD"
    return "USD"

def get_prices(product_query: str) -> List[Dict[str, Any]]:
    serpapi_key = os.getenv("SERPAPI_KEY")
    if not serpapi_key:
        raise ValueError("SERPAPI_KEY is missing from environment variables.")
        
    params = {
        "engine": "google_shopping",
        "q": product_query,
        "gl": "cl",
        "hl": "es",
        "api_key": serpapi_key
    }
    
    try:
        search = GoogleSearch(params)
        results = search.get_dict()
    except Exception as e:
        raise RuntimeError(f"SerpAPI call failed: {e}")
        
    if "error" in results:
        raise RuntimeError(f"SerpAPI returned an error: {results['error']}")
        
    shopping_results = results.get("shopping_results", [])
    
    top_results = []
    for item in shopping_results[:20]:
        title = item.get("title", "")
        price_raw = item.get("price", "")
        store = item.get("source", "")
        link = item.get("product_link") or item.get("link", "")
        
        price_value = parse_price(price_raw)
        currency = detect_currency(price_raw, price_value)
        
        top_results.append({
            "title": title,
            "price_raw": price_raw,
            "price_value": price_value,
            "currency": currency,
            "store": store,
            "link": link
        })
        
    return top_results
