import sqlite3

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