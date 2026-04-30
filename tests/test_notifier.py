import pytest
from unittest.mock import patch, MagicMock
from app.notifier import send_whatsapp

@pytest.fixture
def mock_env(monkeypatch):
    monkeypatch.setenv("PHONE_NUMBER", "+56912345678")
    monkeypatch.setenv("CALLMEBOT_KEY", "fake_key")

def test_send_whatsapp_success(mock_env, mocker):
    mock_get = mocker.patch("app.notifier.requests.get")
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_get.return_value = mock_response
    
    alerts = [{
        "store": "Amazon",
        "price_usd": 74.99,
        "price_clp": 71240,
        "triggered_by": "USD",
        "link": "http://amazon"
    }]
    
    result = send_whatsapp(alerts, "Samsung SSD", is_test=False)
    
    assert result is True
    mock_get.assert_called_once()
    
    called_args = mock_get.call_args[1]["params"]
    text = called_args["text"]
    
    assert "🚨 *Alerta de precio!*" in text
    assert "*Samsung SSD*" in text
    assert "Amazon" in text
    assert "74.99" in text
    assert "71240" in text
    assert "USD" in text
    assert "http://amazon" in text

def test_send_whatsapp_is_test(mock_env, mocker):
    mock_get = mocker.patch("app.notifier.requests.get")
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_get.return_value = mock_response
    
    alerts = [{"store": "TestStore"}]
    
    result = send_whatsapp(alerts, "TestProduct", is_test=True)
    
    assert result is True
    called_args = mock_get.call_args[1]["params"]
    assert "🧪 *[TEST] Alerta de precio!*" in called_args["text"]

def test_send_whatsapp_failure(mock_env, mocker):
    mock_get = mocker.patch("app.notifier.requests.get")
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_get.return_value = mock_response
    
    alerts = [{"store": "TestStore"}]
    
    result = send_whatsapp(alerts, "TestProduct")
    assert result is False

def test_send_whatsapp_missing_credentials(monkeypatch):
    monkeypatch.delenv("PHONE_NUMBER", raising=False)
    monkeypatch.delenv("CALLMEBOT_KEY", raising=False)
    
    alerts = [{"store": "TestStore"}]
    result = send_whatsapp(alerts, "TestProduct")
    
    assert result is False

def test_send_whatsapp_no_alerts(mock_env):
    result = send_whatsapp([], "TestProduct")
    assert result is False
