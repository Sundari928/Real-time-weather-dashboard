from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import get_latest_data

app = FastAPI()

# CORS enable karo taaki Streamlit dashboard access kar sake
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Weather API is running!"}

@app.get("/latest")
def latest_weather():
    data = get_latest_data()
    result = []
    for row in data:
        result.append({
            "id": row[0],
            "city": row[1],
            "temperature": row[2],
            "humidity": row[3],
            "wind_speed": row[4],
            "weather_condition": row[5],
            "timestamp": row[6]
        })
    return result