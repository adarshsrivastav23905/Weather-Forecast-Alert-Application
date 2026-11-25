"""CSV and JSON report generation."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


def build_hourly_report(payload: dict) -> pd.DataFrame:
    hourly = payload.get("hourly", {})
    if not hourly:
        return pd.DataFrame()
    frame = pd.DataFrame({
        "time": hourly.get("time", []),
        "temperature_c": hourly.get("temperature_2m", []),
        "humidity_percent": hourly.get("relative_humidity_2m", []),
        "rain_probability_percent": hourly.get("precipitation_probability", []),
        "rain_mm": hourly.get("precipitation", []),
        "wind_mps": hourly.get("wind_speed_10m", []),
        "wind_gust_mps": hourly.get("wind_gusts_10m", []),
    })
    return frame


def build_daily_report(payload: dict) -> pd.DataFrame:
    daily = payload.get("daily", {})
    if not daily:
        return pd.DataFrame()
    return pd.DataFrame({
        "date": daily.get("time", []),
        "temperature_max_c": daily.get("temperature_2m_max", []),
        "temperature_min_c": daily.get("temperature_2m_min", []),
        "rain_mm": daily.get("precipitation_sum", []),
        "rain_probability_percent": daily.get("precipitation_probability_max", []),
        "wind_max_mps": daily.get("wind_speed_10m_max", []),
        "uv_index_max": daily.get("uv_index_max", []),
    })


def save_reports(payload: dict, alerts: list[dict[str, str]], output_dir: str | Path) -> tuple[Path, Path]:
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    hourly_path = directory / "hourly_forecast.csv"
    summary_path = directory / "weather_summary.json"

    build_hourly_report(payload).to_csv(hourly_path, index=False)
    summary = {
        "city": payload.get("city", "Unknown"),
        "timezone": payload.get("timezone", "UTC"),
        "latitude": payload.get("latitude"),
        "longitude": payload.get("longitude"),
        "current": payload.get("current", {}),
        "alerts": alerts,
        "daily_forecast": build_daily_report(payload).to_dict(orient="records"),
    }
    with summary_path.open("w", encoding="utf-8") as file:
        json.dump(summary, file, indent=2, ensure_ascii=False)
    return hourly_path, summary_path
