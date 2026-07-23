import streamlit as st
import pandas as pd
import requests
import time

st.set_page_config(page_title="Real-Time Weather Dashboard", layout="wide")

st.title("🌦️ Real-Time Weather Dashboard")
st.caption("Live weather data updated every 5 minutes")

API_URL = "http://127.0.0.1:8000/latest"

# Auto-refresh every 60 seconds
st_autorefresh_placeholder = st.empty()

def fetch_data():
    try:
        response = requests.get(API_URL)
        data = response.json()
        df = pd.DataFrame(data)
        return df
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return pd.DataFrame()

df = fetch_data()

if not df.empty:
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # Latest reading per city
    latest_per_city = df.sort_values("timestamp").groupby("city").tail(1)

    # ---- Live Cards ----
    st.subheader("📍 Current Weather by City")
    cols = st.columns(len(latest_per_city))
    for idx, row in enumerate(latest_per_city.itertuples()):
        with cols[idx]:
            st.metric(
                label=row.city,
                value=f"{row.temperature} °C",
                delta=row.weather_condition
            )
            st.caption(f"💧 Humidity: {row.humidity}%  |  💨 Wind: {row.wind_speed} m/s")

    st.divider()

    # ---- Temperature Trend Chart ----
    st.subheader("📈 Temperature Trend")
    temp_pivot = df.pivot_table(index="timestamp", columns="city", values="temperature")
    st.line_chart(temp_pivot)

    # ---- Humidity Bar Chart ----
    st.subheader("💧 Current Humidity Comparison")
    st.bar_chart(latest_per_city.set_index("city")["humidity"])

    # ---- Raw Data Table ----
    with st.expander("🔍 View Raw Data"):
        st.dataframe(df.sort_values("timestamp", ascending=False))

else:
    st.warning("No data available yet. Make sure fetch_data.py is running.")

# Auto refresh every 60 seconds
time.sleep(60)
st.rerun()