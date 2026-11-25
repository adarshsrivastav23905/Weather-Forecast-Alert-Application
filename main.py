"""Command-line entry point for Weather Forecast & Alert Application."""

from __future__ import annotations

import argparse
from pathlib import Path

from src.reports import build_daily_report, build_hourly_report, save_reports
from src.rules import evaluate_alerts
from src.weather import WeatherError, fetch_weather, load_simulation


ROOT = Path(__file__).resolve().parent


def print_weather(payload: dict, alerts: list[dict[str, str]]) -> None:
    current = payload.get("current", {})
    print("\nWeather report")
    print("--------------")
    print(f"Location: {payload.get('city', 'Unknown')}")
    print(f"Timezone: {payload.get('timezone', 'UTC')}")
    print(f"Temperature: {current.get('temperature_2m', 'N/A')} C")
    print(f"Feels like: {current.get('apparent_temperature', 'N/A')} C")
    print(f"Humidity: {current.get('relative_humidity_2m', 'N/A')}%")
    print(f"Wind: {current.get('wind_speed_10m', 'N/A')} m/s")

    print("\nForecast alerts")
    for alert in alerts:
        print(f"- [{alert['severity'].upper()}] {alert['label']}")

    print("\nNext 7 days")
    print(build_daily_report(payload).to_string(index=False))


def main() -> None:
    parser = argparse.ArgumentParser(description="Weather Forecast & Alert Application")
    parser.add_argument("--city", default="Delhi", help="City name for live weather")
    parser.add_argument("--mode", choices=["api", "simulation"], default="api")
    parser.add_argument("--sample", default=str(ROOT / "data" / "sample_weather.json"))
    args = parser.parse_args()

    try:
        payload = fetch_weather(args.city) if args.mode == "api" else load_simulation(args.sample)
    except WeatherError as exc:
        print(f"Error: {exc}")
        return

    alerts = evaluate_alerts(payload)
    print_weather(payload, alerts)

    hourly_path, summary_path = save_reports(payload, alerts, ROOT / "outputs")
    print(f"\nGenerated: {hourly_path}")
    print(f"Generated: {summary_path}")


if __name__ == "__main__":
    main()
