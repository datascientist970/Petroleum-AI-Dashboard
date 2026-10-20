# Petroleum AI Dashboard

> A real-time Django dashboard for oil & gas monitoring — live Brent, WTI and Natural Gas tracking, Prophet production forecasting, predictive-maintenance demos, MQTT data ingestion and one-click PDF executive reports.

![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-Web%20App-092E20?logo=django&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-Interactive%20Charts-3F4F75?logo=plotly&logoColor=white)
![MQTT](https://img.shields.io/badge/MQTT-Live%20Ingestion-660066?logo=mqtt&logoColor=white)

## Overview

The Petroleum AI Dashboard brings commodity monitoring and operational analytics into a single web interface. It tracks Brent crude, WTI crude and Natural Gas data over selectable time ranges, visualises trends with interactive Plotly charts, exposes JSON APIs for dashboard data and AI insights, can ingest live sensor-style data over MQTT, and generates formatted PDF reports with ReportLab.

Where no live feed is connected, the dashboard generates realistic sample data so every feature can be explored immediately.

## Key Features

- **Real-time commodity dashboard** — line, bar and pie charts (Plotly) for Brent, WTI and Natural Gas, with time-range selectors (today / 7 / 30 days / quarter / year) and an asset filter
- **JSON APIs** — `api/dashboard-data/` for chart data and metrics, `api/ai-insights/` for insight summaries, designed for auto-refreshing front ends
- **Production forecasting** — Prophet-based forecasting of numeric production series (10-day horizon) in `analytics/utils.py`
- **Predictive-maintenance demo** — a demo module that attaches failure-probability estimates to operational data for evaluation of the workflow
- **MQTT live ingestion** — a Paho MQTT client subscribes to the `oil_gas/sensors` topic and appends incoming price payloads to `realtime_data.csv`
- **PDF executive reports** — one-click ReportLab reports with summary tables
- **Summary metrics** — current values, changes and aggregate metrics calculated per selected range and asset

## Tech Stack

- **Backend:** Django (Python)
- **Data:** Pandas, NumPy
- **Forecasting:** Prophet
- **Visualisation:** Plotly (Python + Plotly.js), Bootstrap 5, Font Awesome
- **Live Data:** Paho MQTT (HiveMQ public broker for testing)
- **Reporting:** ReportLab
- **Database:** SQLite (development)

## Project Structure

```text
Petroleum-AI-Dashboard/
└── petro_ai/
    ├── manage.py
    ├── petro_ai/               # Django project settings & URLs
    └── analytics/              # Analytics app
        ├── views.py            # Dashboard, APIs, charts, PDF report
        ├── utils.py            # Prophet forecasting & maintenance demo
        ├── mqtt_client.py      # MQTT subscriber → realtime_data.csv
        ├── mqtt_publisher.py   # MQTT test publisher
        ├── realtime_data.csv   # Ingested / sample time-series data
        ├── urls.py
        └── templates/home.html # Dashboard UI
```

## Getting Started

```bash
git clone https://github.com/datascientist970/Petroleum-AI-Dashboard.git
cd Petroleum-AI-Dashboard/petro_ai
pip install django pandas numpy plotly reportlab prophet paho-mqtt
python manage.py migrate
python manage.py runserver
```

Open `http://127.0.0.1:8000/` to view the dashboard.

## Usage

- **Explore:** change the time range or asset filter — charts, metrics and insights update through the JSON APIs.
- **Generate a report:** use the PDF report action (`/generate-pdf-report/`) for a downloadable executive summary.
- **Stream live data (optional):** run the MQTT publisher / client pair to append sensor payloads to `realtime_data.csv`:

```bash
python analytics/mqtt_publisher.py   # publish test payloads
python analytics/mqtt_client.py      # subscribe and store them
```

## Author

**Muhammad Dawood** — AI & Data Science Engineer
GitHub: https://github.com/datascientist970 · Mardan, Pakistan
LinkedIn: https://www.linkedin.com/in/dawood406/

⭐ If you find this project useful, consider giving it a star.
