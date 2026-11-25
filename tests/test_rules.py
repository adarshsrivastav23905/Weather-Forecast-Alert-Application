from src.rules import evaluate_alerts
from src.weather import load_simulation


def test_simulation_generates_expected_alert_types():
    payload = load_simulation("data/sample_weather.json")
    alerts = evaluate_alerts(payload)
    codes = {alert["code"] for alert in alerts}

    assert "RAIN_SOON" in codes
    assert "HEAT_WAVE" in codes
    assert "WIND_HIGH" in codes
    assert "UV_HIGH" in codes


def test_no_alert_payload_is_safe():
    payload = {
        "current": {"relative_humidity_2m": 50},
        "hourly": {
            "precipitation_probability": [10] * 12,
            "wind_gusts_10m": [5] * 24,
        },
        "daily": {
            "temperature_2m_max": [30, 31],
            "uv_index_max": [4],
        },
    }
    alerts = evaluate_alerts(payload)

    assert alerts == [{
        "code": "NO_ALERT",
        "severity": "info",
        "label": "No warning conditions are currently met.",
    }]
