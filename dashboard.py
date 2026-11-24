import unicodedata
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
    
ICON_EMOJI = {
    "01d": "☀️", "01n": "🌙", "02d": "⛅", "02n": "☁️",
    "03d": "☁️", "03n": "☁️", "04d": "☁️", "04n": "☁️",
    "09d": "🌧️", "09n": "🌧️", "10d": "🌦️", "10n": "🌧️",
    "11d": "⛈️", "11n": "⛈️", "13d": "❄️", "13n": "❄️",
    "50d": "🌫️", "50n": "🌫️",
}

def clean_text(text):
    """Remove accent marks (e.g. Bānsi -> Bansi)"""
    cleaned = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    return cleaned or text

@st.cache_data(ttl=600)
def search_city(query):
    """Search Indian places by name (Open-Meteo Geocoding API)"""
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {"name": query, "count": 10, "countryCode": "IN", "language": "en"}
    r = requests.get(url, params=params, timeout=10)
    r.raise_for_status()
    results = r.json().get("results", [])
    return [
        {
            "name": clean_text(p["name"]),
            "state": ", ".join(
                clean_text(x) for x in filter(None, [p.get("admin2"), p.get("admin1")])
            ) or "India",
            "lat": p["latitude"],
            "lon": p["longitude"],
        }
        for p in results
        if p.get("country_code") == "IN"
    ]

@st.cache_data(ttl=300)
def fetch_weather_by_coords(lat, lon):
    """Fetch current weather using lat/lon"""
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"lat": lat, "lon": lon, "appid": API_KEY, "units": "metric"}
    r = requests.get(url, params=params, timeout=10)
    r.raise_for_status()
    return r.json()

st.subheader("🔎 Search any Indian city")

with st.form("search_form"):
    query = st.text_input("Enter city name", placeholder="e.g. Pune, Jaipur, Udaipur")
    submitted = st.form_submit_button("Search")

if submitted and query.strip():
    st.session_state["query"] = query.strip()

q = st.session_state.get("query")
if q:
    try:
        matches = search_city(q)
    except requests.RequestException:
        matches = None
        st.error("Search failed. Please check your internet connection or API key.")

    if matches is not None:
        if not matches:
            st.warning(f"No Indian city found with the name '{q}'. Please check the spelling.")
        else:
            labels = [f"{m['name']}, {m.get('state', 'India')}" for m in matches]
            idx = st.selectbox(
                "select the correct city from the list below",
                range(len(matches)),
                format_func=lambda i: labels[i],
            ) if len(matches) > 1 else 0

            place = matches[idx]
            try:
                w = fetch_weather_by_coords(place["lat"], place["lon"])
                st.markdown(f"### 📍 {labels[idx]}")
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("🌡️ Temperature", f"{w['main']['temp']} °C")
                c2.metric("🤔 Feels like", f"{w['main']['feels_like']} °C")
                c3.metric("💧 Humidity", f"{w['main']['humidity']}%")
                c4.metric("💨 Wind", f"{w['wind']['speed']} m/s")
                icon = w["weather"][0]["icon"]
                st.markdown(f"## {ICON_EMOJI.get(icon, '🌡️')} {w['weather'][0]['description'].title()}")
            except requests.RequestException:
                st.error("Could not fetch weather data. Please try again later.")

st.divider()