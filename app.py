"""Streamlit dashboard for weather forecasts and alerts."""

from __future__ import annotations

from html import escape
from pathlib import Path

import streamlit as st

from src.reports import build_daily_report, build_hourly_report, save_reports
from src.rules import evaluate_alerts
from src.weather import WeatherError, fetch_weather, load_simulation


ROOT = Path(__file__).resolve().parent
st.set_page_config(
    page_title="Weather Forecast & Alerts",
    page_icon=":material/cloud:",
    layout="wide",
)

with st.sidebar:
    st.markdown("## :material/cloud: Weather desk")
    st.caption("Forecast intelligence for your day")
    st.space("small")
    with st.form("weather_search"):
        mode = st.segmented_control(
            "Data source",
            options=["Simulation", "Live API"],
            default="Simulation",
            key="weather_mode",
        )
        city = st.text_input("City", value="Delhi", key="city")
        fetch = st.form_submit_button(
            "Update forecast",
            icon=":material/search:",
            type="primary",
            width="stretch",
        )
    st.space("small")
    st.caption("Live forecasts are provided by Open-Meteo. Simulation works offline.")
    st.caption("Threshold alerts are for planning and demonstration only.")

if "weather_payload" not in st.session_state:
    st.session_state["weather_payload"] = load_simulation(ROOT / "data" / "sample_weather.json")
    st.session_state["weather_source"] = "Simulation"

if fetch:
    try:
        if mode == "Live API":
            st.session_state["weather_payload"] = fetch_weather(city)
            st.session_state["weather_source"] = "Live API"
            st.toast("Live forecast updated", icon=":material/cloud_done:")
        else:
            st.session_state["weather_payload"] = load_simulation(ROOT / "data" / "sample_weather.json")
            st.session_state["weather_source"] = "Simulation"
            st.toast("Simulation data loaded", icon=":material/science:")
    except WeatherError as exc:
        st.error(str(exc))

payload = st.session_state["weather_payload"]
source = st.session_state["weather_source"]
alerts = evaluate_alerts(payload)
hourly = build_hourly_report(payload)
daily = build_daily_report(payload)
current = payload.get("current", {})
city_name = escape(str(payload.get("city", "Unknown")))
timezone = escape(str(payload.get("timezone", "Local time")))
latitude = payload.get("latitude")
longitude = payload.get("longitude")
coordinates = (
    f"{latitude:.2f}, {longitude:.2f}"
    if isinstance(latitude, (int, float)) and isinstance(longitude, (int, float))
    else "Location coordinates unavailable"
)
source_label = "LIVE FORECAST" if source == "Live API" else "SIMULATION MODE"

st.html(
    f"""
    <style>
        .weather-hero {{
            position: relative;
            overflow: hidden;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1.5rem;
            padding: 2rem 2.2rem;
            margin: 0.4rem 0 1.35rem;
            border: 1px solid rgba(255,255,255,.16);
            border-radius: 22px;
            color: #f8fafc;
            background: linear-gradient(118deg, #10243a 0%, #163b53 56%, #087e83 100%);
            box-shadow: 0 16px 38px rgba(15, 35, 55, .16);
        }}
        .weather-hero::after {{
            content: "";
            position: absolute;
            width: 250px;
            height: 250px;
            right: 12%;
            top: -155px;
            border: 1px solid rgba(255,255,255,.16);
            border-radius: 50%;
            box-shadow: 0 0 0 28px rgba(255,255,255,.035), 0 0 0 58px rgba(255,255,255,.025);
        }}
        .weather-hero__copy, .weather-hero__meta {{ position: relative; z-index: 1; }}
        .weather-hero__eyebrow {{
            margin: 0 0 .45rem;
            color: #a7f3e8;
            font-size: .82rem;
            font-weight: 700;
            letter-spacing: .14em;
        }}
        .weather-hero__title {{
            margin: 0;
            color: #fff;
            font-size: clamp(2.1rem, 4vw, 3rem);
            font-weight: 700;
            letter-spacing: -.045em;
            line-height: 1.15;
        }}
        .weather-hero__subtitle {{
            margin: .55rem 0 0;
            color: #d3e2ec;
            font-size: 1.08rem;
        }}
        .weather-hero__meta {{
            min-width: 185px;
            padding: .9rem 1rem;
            border: 1px solid rgba(255,255,255,.2);
            border-radius: 14px;
            background: rgba(7, 24, 39, .24);
        }}
        .weather-hero__meta-label {{
            color: #b7cbd7;
            font-size: .78rem;
            letter-spacing: .1em;
            text-transform: uppercase;
        }}
        .weather-hero__place {{ margin-top: .25rem; color: #fff; font-size: 1.12rem; font-weight: 650; }}
        .weather-hero__coords {{ margin-top: .25rem; color: #d3e2ec; font-size: .9rem; }}
        @media (max-width: 640px) {{
            .weather-hero {{ align-items: flex-start; flex-direction: column; padding: 1.5rem; }}
            .weather-hero__meta {{ width: 100%; box-sizing: border-box; }}
        }}
    </style>
    <section class="weather-hero">
        <div class="weather-hero__copy">
            <p class="weather-hero__eyebrow">WEATHER INTELLIGENCE · {source_label}</p>
            <h1 class="weather-hero__title">A clearer view of your day.</h1>
            <p class="weather-hero__subtitle">Current conditions, the week ahead, and alerts worth knowing.</p>
        </div>
        <div class="weather-hero__meta">
            <div class="weather-hero__meta-label">Forecast location</div>
            <div class="weather-hero__place">{city_name}</div>
            <div class="weather-hero__coords">{timezone} · {coordinates}</div>
        </div>
    </section>
    """
)

csv_path, summary_path = save_reports(payload, alerts, ROOT / "outputs")
with st.container(horizontal=True, horizontal_alignment="distribute"):
    st.caption(f"Showing {source.lower()} data · Units: °C, mm, m/s")
    st.download_button(
        "Hourly CSV",
        data=csv_path.read_bytes(),
        file_name=f"{payload.get('city', 'weather').lower().replace(' ', '_')}_hourly_forecast.csv",
        mime="text/csv",
        icon=":material/download:",
    )
    st.download_button(
        "Summary JSON",
        data=summary_path.read_bytes(),
        file_name=f"{payload.get('city', 'weather').lower().replace(' ', '_')}_weather_summary.json",
        mime="application/json",
        icon=":material/data_object:",
    )

st.subheader("Conditions now")
with st.container(horizontal=True):
    st.metric("Temperature", f"{current.get('temperature_2m', 'N/A')} °C", border=True)
    st.metric("Feels like", f"{current.get('apparent_temperature', 'N/A')} °C", border=True)
    st.metric("Humidity", f"{current.get('relative_humidity_2m', 'N/A')}%", border=True)
    st.metric("Wind speed", f"{current.get('wind_speed_10m', 'N/A')} m/s", border=True)

st.subheader("Weather alerts")
if alerts:
    alert_columns = st.columns(2)
    badge_colors = {"critical": "red", "warn": "orange", "info": "green"}
    for index, alert in enumerate(alerts):
        with alert_columns[index % 2]:
            with st.container(border=True):
                st.badge(
                    alert["severity"].capitalize(),
                    color=badge_colors.get(alert["severity"], "gray"),
                )
                st.write(alert["label"])

st.subheader("Forecast at a glance")
left, right = st.columns(2)
with left:
    with st.container(border=True):
        st.markdown("**Temperature trend**")
        st.caption("Hourly outlook for the next 24 hours")
        st.line_chart(
            hourly.head(24).set_index("time"),
            y="temperature_c",
            y_label="Temperature (°C)",
        )

with right:
    with st.container(border=True):
        st.markdown("**Rain outlook**")
        st.caption("Expected daily precipitation over the next 7 days")
        st.bar_chart(
            daily.set_index("date"),
            y="rain_mm",
            y_label="Precipitation (mm)",
        )

with st.container(border=True):
    st.markdown("**7-day forecast details**")
    daily_display = daily.rename(columns={
        "date": "Date",
        "temperature_max_c": "High (°C)",
        "temperature_min_c": "Low (°C)",
        "rain_mm": "Rain (mm)",
        "rain_probability_percent": "Rain chance (%)",
        "wind_max_mps": "Wind max (m/s)",
        "uv_index_max": "UV index",
    })
    st.dataframe(
        daily_display,
        hide_index=True,
        column_config={
            "High (°C)": st.column_config.NumberColumn(format="%.1f"),
            "Low (°C)": st.column_config.NumberColumn(format="%.1f"),
            "Rain (mm)": st.column_config.NumberColumn(format="%.1f"),
            "Rain chance (%)": st.column_config.NumberColumn(format="%.0f%%"),
            "Wind max (m/s)": st.column_config.NumberColumn(format="%.1f"),
            "UV index": st.column_config.NumberColumn(format="%.1f"),
        },
    )

st.caption("Forecasts can change. Use official local guidance for safety-critical decisions.")
