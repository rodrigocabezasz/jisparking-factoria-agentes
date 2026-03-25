import pytest
from src.factory_health import get_status

def test_get_status():
    status = get_status()
    assert status["ok"] is True
    assert status["service"] == "jislab-factory"
    assert status["version"] == "0.1.0"
