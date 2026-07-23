import requests
import os
from dotenv import load_dotenv
from database import insert_weather_data, create_table
import time

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
CITIES = ["Delhi", "Mumbai", "Bangalore", "Chennai", "Kolkata"]

def fetch_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        weather_condition = data["weather"][0]["description"]
        
        insert_weather_data(city, temperature, humidity, wind_speed, weather_condition)
        print(f"✅ {city}: {temperature}°C, {weather_condition}")
    else:
        print(f"❌ Error fetching data for {city}: {response.status_code}")

def fetch_all_cities():
    for city in CITIES:
        fetch_weather(city)

if __name__ == "__main__":
    create_table()  # ensure table exists
    
    while True:
        print("\n--- Fetching new weather data ---")
        fetch_all_cities()
        print("Waiting 5 minutes for next fetch...\n")
        time.sleep(300)  # 5 minutes