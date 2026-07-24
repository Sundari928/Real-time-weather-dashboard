import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Real-Time Weather Dashboard", layout="wide")
st.title("🌦️ Real-Time Weather Dashboard")
st.caption("Live weather data — auto-refreshing every 5 minutes")

API_KEY = st.secrets["OPENWEATHER_API_KEY"]
CITIES = ["Delhi", "Mumbai", "Bangalore", "Chennai", "Kolkata"]

def fetch_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            "city": city,
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
            "weather_condition": data["weather"][0]["description"]
        }
    return None

@st.cache_data(ttl=300)
def get_all_weather():
    results = []
    for city in CITIES:
        data = fetch_weather(city)
        if data:
            results.append(data)
    return pd.DataFrame(results)

df = get_all_weather()

if not df.empty:
    st.subheader("📍 Current Weather by City")
    cols = st.columns(len(df))
    for idx, row in df.iterrows():
        with cols[idx]:
            st.metric(label=row["city"], value=f"{row['temperature']} °C", delta=row["weather_condition"])
            st.caption(f"💧 {row['humidity']}%  |  💨 {row['wind_speed']} m/s")

    st.divider()
    st.subheader("💧 Humidity Comparison")
    st.bar_chart(df.set_index("city")["humidity"])

    with st.expander("🔍 Raw Data"):
        st.dataframe(df)
else:
    st.error("Could not fetch weather data. Please check API key.")