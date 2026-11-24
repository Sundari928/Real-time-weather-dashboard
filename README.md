# 🌦️ Weather Dashboard

## Overview
This project is a real-time weather dashboard built with Python and Streamlit.  
A background script fetches live weather data every 5 minutes and stores it in a local SQLite database. A FastAPI server exposes this data, and the Streamlit dashboard displays the latest temperature, humidity, wind speed, and weather condition for multiple cities.

## Features
- Live weather cards for each city
- Temperature trend chart over time
- Humidity comparison chart
- Raw weather data table
- Auto-refresh support (data updates every 5 minutes)

## Tech Stack
- Python
- Streamlit
- FastAPI + Uvicorn
- Pandas
- Requests
- SQLite (via `database.py`)

## Project Structure
```text
weather/
├── api_server.py       # FastAPI server exposing weather data (/latest endpoint)
├── dashboard.py         # Streamlit dashboard (main app)
├── database.py          # SQLite connection, table setup, and queries
├── fetch_data.py        # Background script that fetches weather data every 5 minutes and stores it in the database
├── requirements.txt      # Python dependencies
└── .gitignore
```

## Requirements
Make sure you have Python installed.  
All required packages are listed in `requirements.txt`.

## Setup and Usage

1. Clone the repository:
```bash
git clone https://github.com/Sundari928/Real-time-weather-dashboard.git
cd Real-time-weather-dashboard
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate
```

3. Install the dependencies:
```bash
pip install -r requirements.txt
```

4. Start fetching weather data (runs continuously, updates every 5 minutes):
```bash
python fetch_data.py
```

5. In a new terminal (with the virtual environment activated), start the API server:
```bash
uvicorn api_server:app --reload --port 8000
```
The API should now be running at:
```text
http://127.0.0.1:8000/latest
```

6. In another new terminal (with the virtual environment activated), run the dashboard:
```bash
streamlit run dashboard.py
```

7. Open your browser and go to:
```text
http://localhost:8501
```

## Contributing
Contributions are welcome. If you want to improve the project, feel free to open an issue or submit a pull request.
