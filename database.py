import sqlite3
from datetime import datetime

def create_connection():
    conn = sqlite3.connect("weather.db")
    return conn

def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS weather_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT,
            temperature REAL,
            humidity REAL,
            wind_speed REAL,
            weather_condition TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    
    # Add sample data if table is empty
    cursor.execute("SELECT COUNT(*) FROM weather_data")
    if cursor.fetchone()[0] == 0:
        sample_data = [
            ("Mumbai", 32.5, 75, 15, "Partly Cloudy"),
            ("Delhi", 28.3, 65, 10, "Clear"),
            ("Bangalore", 25.1, 70, 8, "Rainy"),
        ]
        cursor.executemany("""
            INSERT INTO weather_data (city, temperature, humidity, wind_speed, weather_condition)
            VALUES (?, ?, ?, ?, ?)
        """, sample_data)
        conn.commit()
    
    conn.close()
    print("Table created successfully!")

def insert_weather_data(city, temperature, humidity, wind_speed, weather_condition):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO weather_data (city, temperature, humidity, wind_speed, weather_condition)
        VALUES (?, ?, ?, ?, ?)
    """, (city, temperature, humidity, wind_speed, weather_condition))
    conn.commit()
    conn.close()

def get_latest_data():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM weather_data
        ORDER BY timestamp DESC
        LIMIT 20
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows

if __name__ == "__main__":
    create_table()