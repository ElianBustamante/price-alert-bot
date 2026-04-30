import pytest
from app.checker import check_prices

@pytest.fixture
def mock_env(monkeypatch):
    monkeypatch.setenv("PRICE_LIMIT_USD", "80.0")
    monkeypatch.setenv("PRICE_LIMIT_CLP", "75000.0")

def test_check_prices_no_alerts(mock_env, mocker):
    mocker.patch("app.converter.to_usd", return_value=85.0)
    mocker.patch("app.converter.to_clp", return_value=80000.0)
    
    prices = [{"price_value": 85.0, "currency": "USD"}]
    
    alerts = check_prices(prices)
    assert len(alerts) == 0

def test_check_prices_trigger_usd(mock_env, mocker):
    mocker.patch("app.converter.to_usd", return_value=79.0)
    mocker.patch("app.converter.to_clp", return_value=80000.0)
    
    prices = [{"price_value": 79.0, "currency": "USD"}]
    
    alerts = check_prices(prices)
    assert len(alerts) == 1
    assert alerts[0]["price_usd"] == 79.0
    assert alerts[0]["price_clp"] == 80000
    assert alerts[0]["triggered_by"] == "USD"

def test_check_prices_trigger_clp(mock_env, mocker):
    mocker.patch("app.converter.to_usd", return_value=85.0)
    mocker.patch("app.converter.to_clp", return_value=74000.0)
    
    prices = [{"price_value": 74000.0, "currency": "CLP"}]
    
    alerts = check_prices(prices)
    assert len(alerts) == 1
    assert alerts[0]["price_usd"] == 85.0
    assert alerts[0]["price_clp"] == 74000
    assert alerts[0]["triggered_by"] == "CLP"

def test_check_prices_trigger_both(mock_env, mocker):
    mocker.patch("app.converter.to_usd", return_value=75.0)
    mocker.patch("app.converter.to_clp", return_value=72000.0)
    
    prices = [{"price_value": 75.0, "currency": "USD"}]
    
    alerts = check_prices(prices)
    assert len(alerts) == 1
    assert alerts[0]["triggered_by"] == "BOTH"
