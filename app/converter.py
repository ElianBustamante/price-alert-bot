import time
import requests

_CACHE_TTL = 3600  # 1 hour in seconds
_cached_rate = None
_last_fetch_time = 0.0

def get_usd_to_clp() -> float:
    """
    Fetch the real-time exchange rate from exchangerate-api.com.
    Caches the result for 1 hour to avoid hitting API limits.
    """
    global _cached_rate, _last_fetch_time
    
    current_time = time.time()
    
    # Return cached rate if it's still valid
    if _cached_rate is not None and (current_time - _last_fetch_time) < _CACHE_TTL:
        return _cached_rate
        
    try:
        response = requests.get("https://api.exchangerate-api.com/v4/latest/USD", timeout=10)
        response.raise_for_status()
        data = response.json()
        
        clp_rate = float(data["rates"]["CLP"])
        
        # Update cache
        _cached_rate = clp_rate
        _last_fetch_time = current_time
        
        return clp_rate
    except Exception as e:
        raise RuntimeError(f"Failed to fetch exchange rate: {e}")

def to_usd(value: float, currency: str) -> float:
    """
    Convert a value to USD. 
    If it's already USD, returns as-is.
    If it's CLP, divides by exchange rate and rounds to 2 decimals.
    """
    if currency.upper() == "USD":
        return value
    if currency.upper() == "CLP":
        rate = get_usd_to_clp()
        return round(value / rate, 2)
    raise ValueError(f"Unsupported currency: {currency}")

def to_clp(value: float, currency: str) -> float:
    """
    Convert a value to CLP. 
    If it's already CLP, returns as-is.
    If it's USD, multiplies by exchange rate and rounds to nearest integer.
    """
    if currency.upper() == "CLP":
        return value
    if currency.upper() == "USD":
        rate = get_usd_to_clp()
        return round(value * rate)
    raise ValueError(f"Unsupported currency: {currency}")
