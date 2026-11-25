"""Threshold-based weather alert engine."""

from __future__ import annotations

from typing import Iterable


def safe_max(values: Iterable[float | int | None]) -> float | None:
    present = [float(value) for value in values if value is not None]
    return max(present) if present else None


def evaluate_alerts(payload: dict) -> list[dict[str, str]]:
    """Generate human-readable alerts from current, hourly, and daily data."""
    alerts: list[dict[str, str]] = []
    hourly = payload.get("hourly", {})
    daily = payload.get("daily", {})
    current = payload.get("current", {})

    rain_probability = hourly.get("precipitation_probability", [])[:12]
    rain_max = safe_max(rain_probability)
    if rain_max is not None and rain_max >= 60:
        alerts.append({
            "code": "RAIN_SOON",
            "severity": "warn",
            "label": f"Rain likely in the next 12 hours ({rain_max:.0f}% probability).",
        })

    tomorrow_high = (daily.get("temperature_2m_max") or [None, None])
    tomorrow_value = tomorrow_high[1] if len(tomorrow_high) > 1 else None
    if tomorrow_value is not None and tomorrow_value >= 40:
        alerts.append({
            "code": "HEAT_WAVE",
            "severity": "critical",
            "label": f"Heat alert: tomorrow's maximum is {tomorrow_value:.1f} C.",
        })

    humidity = current.get("relative_humidity_2m")
    if humidity is not None and humidity >= 85:
        alerts.append({
            "code": "HUMIDITY_HIGH",
            "severity": "warn",
            "label": f"High humidity warning ({humidity:.0f}%).",
        })

    gusts = hourly.get("wind_gusts_10m", [])[:24]
    gust_max = safe_max(gusts)
    if gust_max is not None and gust_max >= 15:
        alerts.append({
            "code": "WIND_HIGH",
            "severity": "warn",
            "label": f"Strong wind gusts possible (up to {gust_max:.1f} m/s).",
        })

    uv_values = daily.get("uv_index_max") or []
    uv_today = uv_values[0] if uv_values else None
    if uv_today is not None and uv_today >= 8:
        alerts.append({
            "code": "UV_HIGH",
            "severity": "warn",
            "label": f"Very high UV index today ({uv_today:.1f}).",
        })

    if not alerts:
        alerts.append({
            "code": "NO_ALERT",
            "severity": "info",
            "label": "No warning conditions are currently met.",
        })
    return alerts
