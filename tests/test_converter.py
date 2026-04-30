import pytest
from unittest.mock import patch, MagicMock
from app import converter

@pytest.fixture(autouse=True)
def reset_cache():
    # Reset cache before each test to ensure isolated testing
    converter._cached_rate = None
    converter._last_fetch_time = 0.0

@patch("app.converter.requests.get")
def test_get_usd_to_clp_success(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {"rates": {"CLP": 950.5}}
    mock_get.return_value = mock_response
    
    rate = converter.get_usd_to_clp()
    assert rate == 950.5
    mock_get.assert_called_once()

@patch("app.converter.requests.get")
def test_get_usd_to_clp_cache(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {"rates": {"CLP": 950.0}}
    mock_get.return_value = mock_response
    
    # First call - should hit the API
    rate1 = converter.get_usd_to_clp()
    assert rate1 == 950.0
    assert mock_get.call_count == 1
    
    # Second call - should use cache
    rate2 = converter.get_usd_to_clp()
    assert rate2 == 950.0
    assert mock_get.call_count == 1
    
    # Simulate time passing beyond 1 hour (TTL = 3600s)
    converter._last_fetch_time -= 3601
    
    # Third call - should hit the API again
    rate3 = converter.get_usd_to_clp()
    assert rate3 == 950.0
    assert mock_get.call_count == 2

@patch("app.converter.requests.get")
def test_get_usd_to_clp_error(mock_get):
    mock_get.side_effect = Exception("Network Error")
    
    with pytest.raises(RuntimeError, match="Failed to fetch exchange rate"):
        converter.get_usd_to_clp()

@patch("app.converter.get_usd_to_clp", return_value=950.0)
def test_to_usd(mock_rate):
    assert converter.to_usd(50.0, "USD") == 50.0
    assert converter.to_usd(95000.0, "CLP") == 100.0
    assert converter.to_usd(100000.0, "CLP") == 105.26
    
    with pytest.raises(ValueError, match="Unsupported currency"):
        converter.to_usd(100.0, "EUR")

@patch("app.converter.get_usd_to_clp", return_value=950.0)
def test_to_clp(mock_rate):
    assert converter.to_clp(75000.0, "CLP") == 75000.0
    assert converter.to_clp(100.0, "USD") == 95000
    assert converter.to_clp(100.5, "USD") == 95475

    with pytest.raises(ValueError, match="Unsupported currency"):
        converter.to_clp(100.0, "EUR")
