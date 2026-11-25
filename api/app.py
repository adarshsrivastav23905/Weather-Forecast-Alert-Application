"""FastAPI service for weather and alert data."""

from pathlib import Path

from fastapi import FastAPI, HTTPException, Query

from src.reports import build_daily_report, build_hourly_report
from src.rules import evaluate_alerts
from src.weather import WeatherError, fetch_weather, load_simulation


ROOT = Path(__file__).resolve().parents[1]
app = FastAPI(
    title="Weather Forecast & Alert API",
    description="Live Open-Meteo forecasts and threshold-based weather alerts.",
    version="1.0.0",
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/weather")
def weather(city: str = Query(min_length=2, description="City name")) -> dict:
    try:
        payload = fetch_weather(city)
    except WeatherError as exc:
        raise HTTPException(status_code=404 if "not found" in str(exc).lower() else 502, detail=str(exc)) from exc
    alerts = evaluate_alerts(payload)
    return {
        "location": {
            "city": payload["city"],
            "timezone": payload["timezone"],
            "latitude": payload["latitude"],
            "longitude": payload["longitude"],
        },
        "current": payload.get("current", {}),
        "hourly": build_hourly_report(payload).to_dict(orient="records"),
        "daily": build_daily_report(payload).to_dict(orient="records"),
        "alerts": alerts,
    }


@app.get("/simulation")
def simulation() -> dict:
    payload = load_simulation(ROOT / "data" / "sample_weather.json")
    alerts = evaluate_alerts(payload)
    return {
        "location": {
            "city": payload["city"],
            "timezone": payload["timezone"],
            "latitude": payload["latitude"],
            "longitude": payload["longitude"],
        },
        "current": payload.get("current", {}),
        "hourly": build_hourly_report(payload).to_dict(orient="records"),
        "daily": build_daily_report(payload).to_dict(orient="records"),
        "alerts": alerts,
    }
