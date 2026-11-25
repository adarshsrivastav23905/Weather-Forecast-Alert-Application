# Weather Forecast & Alert Application

A student-friendly Python project that fetches live weather forecasts from **Open-Meteo** and generates rain, heat, humidity, wind, and UV alerts. It includes a terminal interface, FastAPI service, Streamlit dashboard, simulation mode, CSV reports, and tests.

## Problem statement

Users and organizations often need quick, understandable warnings for weather conditions that could affect travel, outdoor events, farming, logistics, or public safety. This application turns provider data into a compact forecast and actionable alert list.

## Features

- Live city lookup and 7-day forecast through Open-Meteo
- Safe simulation mode that works without an API key or internet
- Rain, heat, humidity, high-wind, and UV alert rules
- Hourly CSV and JSON summary reports
- Streamlit dashboard with KPI cards and charts
- FastAPI endpoints for application integrations
- Beginner-friendly modular source code

## Tech stack

- Python 3.11+
- Requests
- Pandas
- Streamlit
- FastAPI and Uvicorn
- Open-Meteo APIs
- pytest

## Project structure

```text
Weather-Forecast-Alert-Application/
├── api/app.py
├── data/sample_weather.json
├── outputs/
├── screenshots/
├── .streamlit/config.toml
├── src/
│   ├── weather.py
│   ├── rules.py
│   └── reports.py
├── tests/test_rules.py
├── app.py
├── main.py
├── requirements.txt
├── .env.example
└── .gitignore
```

## Setup

### Windows

```powershell
cd "D:\Diploma Course\subjects\Python\Weather Forecast & Alert Application"
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

### macOS/Linux

```bash
cd "Weather-Forecast-Alert-Application"
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Open-Meteo live weather does not require an API key for basic use. Copy `.env.example` only if you later add a notification integration such as Telegram.

## Run the terminal application

Simulation mode:

```bash
python main.py --mode simulation
```

Live mode:

```bash
python main.py --mode api --city "Delhi"
```

Generated reports appear in `outputs/`:

- `hourly_forecast.csv`
- `weather_summary.json`

## Run the Streamlit dashboard

```bash
streamlit run app.py
```

Open the local address printed by Streamlit (normally `http://localhost:8501`). Choose **Live API** or **Simulation**, then select **Get forecast**.

## Run the API

```bash
uvicorn api.app:app --reload
```

- API docs: `http://127.0.0.1:8000/docs`
- Health: `http://127.0.0.1:8000/health`
- Live weather: `http://127.0.0.1:8000/weather?city=Delhi`
- Simulation: `http://127.0.0.1:8000/simulation`

## Run tests

```bash
python -m pytest
```

## Alert thresholds

| Alert | Condition |
|---|---|
| Rain | Any rain probability of at least 60% in the next 12 hours |
| Heat | Tomorrow's maximum temperature of at least 40 C |
| Humidity | Current humidity of at least 85% |
| Wind | Wind gust of at least 15 m/s in the next 24 hours |
| UV | Today's UV index of at least 8 |

Thresholds are demonstration values and should be reviewed by qualified services before real-world emergency use.

## Workflow

```text
City or simulation input
        |
        v
Provider fetch or sample data
        |
        v
JSON normalization
        |
        v
Hourly/daily report tables
        |
        v
Threshold alert engine
        |
        v
CLI, Streamlit, FastAPI, and saved reports
```

## GitHub upload

Recommended repository name: `weather-forecast-alert-application`

Example repository description:

`Python weather forecast and alert application with Open-Meteo API, simulation mode, Streamlit dashboard, FastAPI, CSV reports, and automated weather rules`

Suggested tags: `python`, `weather`, `streamlit`, `fastapi`, `open-meteo`, `data-visualization`, `alerts`

Before uploading:

1. Run the project in simulation mode.
2. Save screenshots in `screenshots/`.
3. Confirm `outputs/` contains only safe demonstration data.
4. Never commit `.env`, API keys, tokens, or `.streamlit/secrets.toml`.
5. Commit the source, README, requirements, sample data, and tests.

## Screenshots

| Screenshot | File |
|---|---|
| Dashboard overview | [01_dashboard_overview.png](screenshots/01_dashboard_overview.png) |
| Weather alerts | [02_weather_alerts.png](screenshots/02_weather_alerts.png) |
| Temperature trend | [03_temperature_trend.png](screenshots/03_temperature_trend.png) |
| Rain outlook | [04_rain_outlook.png](screenshots/04_rain_outlook.png) |
| Daily forecast table | [05_daily_forecast_table.png](screenshots/05_daily_forecast_table.png) |
| Live API forecast | [06_live_api_forecast.png](screenshots/06_live_api_forecast.png) |
| Simulation terminal output | [07_simulation_terminal.png](screenshots/07_simulation_terminal.png) |
| Hourly CSV report | [08_hourly_csv.png](screenshots/08_hourly_csv.png) |
| Weather summary JSON | [09_weather_summary_json.png](screenshots/09_weather_summary_json.png) |
| FastAPI documentation | [10_fastapi_docs.png](screenshots/10_fastapi_docs.png) |
| Passing tests | [11_tests_passed.png](screenshots/11_tests_passed.png) |

## Industry relevance

Weather-aware planning is useful in logistics, agriculture, event operations, travel, energy, and public safety. The project demonstrates API integration, JSON processing, rule engines, caching-compatible modular design, data reporting, REST APIs, and dashboards.

## Interview questions

1. **Explain your project.** I built a Python weather application that can retrieve live Open-Meteo data or use sample data, normalize forecast values, evaluate warning rules, and present results through a CLI, FastAPI, and Streamlit.
2. **What problem does it solve?** It reduces the effort of interpreting raw forecast data and gives users early, condition-specific warnings.
3. **Why did you use Open-Meteo?** It provides public forecast endpoints and is easy to use for a student project without storing an API key.
4. **How are alerts generated?** The engine checks predefined thresholds across current, hourly, and daily values and returns structured alert records.
5. **How is API data processed?** Requests fetch JSON, the provider fields are normalized into Python dictionaries and Pandas tables, and alert/report functions consume those structures.
6. **How does the app handle errors?** Custom exceptions, HTTP status checks, city-not-found handling, and Streamlit/FastAPI error responses show clear messages.
7. **How does simulation mode help?** It allows deterministic testing and screenshots when network access or a provider is unavailable.
8. **How can the project scale?** Add caching, database storage, scheduled refreshes, multiple locations, notification integrations, authentication, and provider-specific adapters.
9. **How would you explain this to a non-technical person?** It checks a city or uses safe sample weather data and warns when rain, heat, humidity, wind, or UV conditions may need attention.
10. **What would you improve next?** Time-aware alert scheduling, 12-hour/24-hour rolling windows, data caching, notification deduplication, AQI data, and deployment.

## Security

- Never commit real API keys or bot tokens.
- Keep secrets in `.env` or platform secret storage.
- Treat this alert engine as a planning aid, not an official emergency warning service.
