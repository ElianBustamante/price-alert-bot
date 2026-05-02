import pytest
from app.scraper import parse_price, detect_currency, get_prices

def test_parse_price():
    assert parse_price("$79.99") == 79.99
    assert parse_price("$74.990") == 74990.0
    assert parse_price("72.990") == 72990.0
    assert parse_price("USD 80") == 80.0
    assert parse_price("CLP 72.990") == 72990.0

def test_detect_currency():
    assert detect_currency("$79.99", 79.99) == "USD"
    assert detect_currency("USD 80", 80.0) == "USD"
    assert detect_currency("CLP 72.990", 72990.0) == "CLP"
    assert detect_currency("$74.990", 74990.0) == "CLP"
    assert detect_currency("Unknown 50", 50.0) == "USD"

def test_get_prices_success(mocker):
    # Mock SerpAPI
    mock_search = mocker.patch("app.scraper.GoogleSearch")
    mock_instance = mock_search.return_value
    mock_instance.get_dict.return_value = {
        "shopping_results": [
            {"title": "SSD 1", "price": "$79.99", "source": "Amazon", "link": "http://amazon"},
            {"title": "SSD 2", "price": "CLP 75.000", "source": "MercadoLibre", "link": "http://ml"},
            {"title": "SSD 3", "price": "$74.990", "source": "Falabella", "link": "http://fala"},
            {"title": "SSD 4", "price": "USD 80", "source": "Ebay", "link": "http://ebay"},
            {"title": "SSD 5", "price": "85.000", "source": "Paris", "link": "http://paris"},
            {"title": "SSD 6", "price": "$90.99", "source": "BestBuy", "link": "http://bb"} # 6th item should now be included
        ]
    }
    
    mocker.patch("os.getenv", return_value="fake_api_key")
    
    results = get_prices("Samsung SSD 990 PRO 1TB Heatsink")
    
    assert len(results) == 9
    
    # First batch (CL) should have 3 items
    assert results[0]["title"] == "SSD 1"
    assert results[0]["store"] == "Amazon"
    assert results[1]["title"] == "SSD 2"
    assert results[1]["store"] == "MercadoLibre"
    assert results[2]["title"] == "SSD 3"
    assert results[2]["store"] == "Falabella"
    
    # Second batch (US) should have 6 items (all unique in mock)
    assert results[3]["title"] == "SSD 1"
    assert results[3]["store"] == "Amazon"
    assert results[8]["title"] == "SSD 6"
    assert results[8]["store"] == "BestBuy"

def test_get_prices_missing_key(mocker):
    mocker.patch("os.getenv", return_value=None)
    with pytest.raises(ValueError, match="SERPAPI_KEY is missing"):
        get_prices("SSD")

def test_get_prices_api_error(mocker):
    mock_search = mocker.patch("app.scraper.GoogleSearch")
    mock_instance = mock_search.return_value
    mock_instance.get_dict.side_effect = Exception("Network error")
    
    mocker.patch("os.getenv", return_value="fake_api_key")
    
    with pytest.raises(RuntimeError, match="SerpAPI call failed"):
        get_prices("SSD")
