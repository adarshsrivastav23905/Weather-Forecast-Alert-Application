"""Weather provider and simulation data helpers."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import requests


GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"


class WeatherError(RuntimeError):
    """Raised when a weather request or response cannot be processed."""


def fetch_weather(city: str, timeout: int = 20) -> dict[str, Any]:
    """Resolve a city and fetch its current, hourly, and daily forecast."""
    if not city.strip():
        raise WeatherError("City name cannot be empty.")

    try:
        geo_response = requests.get(
            GEOCODING_URL,
            params={"name": city.strip(), "count": 1, "language": "en", "format": "json"},
            timeout=timeout,
        )
        geo_response.raise_for_status()
        geo_data = geo_response.json()
    except requests.RequestException as exc:
        raise WeatherError("Could not connect to the weather service.") from exc

    results = geo_data.get("results")
    if not results:
        raise WeatherError(f'City "{city.strip()}" was not found.')

    location = results[0]
    forecast_params = {
        "latitude": location["latitude"],
        "longitude": location["longitude"],
        "current": "temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,wind_speed_10m,weather_code",
        "hourly": "temperature_2m,relative_humidity_2m,precipitation_probability,precipitation,wind_speed_10m,wind_gusts_10m",
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,precipitation_probability_max,wind_speed_10m_max,uv_index_max",
        "timezone": "auto",
        "forecast_days": 7,
    }

    try:
        forecast_response = requests.get(FORECAST_URL, params=forecast_params, timeout=timeout)
        forecast_response.raise_for_status()
        payload = forecast_response.json()
    except requests.RequestException as exc:
        raise WeatherError("Could not fetch the weather forecast.") from exc

    payload["city"] = location.get("name", city.strip())
    payload["timezone"] = location.get("timezone", payload.get("timezone", "UTC"))
    payload["latitude"] = location["latitude"]
    payload["longitude"] = location["longitude"]
    return payload

def load_simulation(path: str | Path) -> dict[str, Any]:
    """Load a self-contained sample Open-Meteo-compatible payload."""
    sample_path = Path(path)
    if not sample_path.exists():
        raise WeatherError(f"Simulation file not found: {sample_path}")

    with sample_path.open("r", encoding="utf-8") as file:
        payload = json.load(file)
    return payload
