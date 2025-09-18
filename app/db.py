import os
from sqlalchemy import create_engine, text

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

def insert_weather(city: str, weather: dict):
    """Insert normalized weather into DB."""
    sql = text("""
        INSERT INTO weather_data
        (city, ts, temperature, humidity, rainfall, wind_speed, condition)
        VALUES (:city, to_timestamp(:dt), :temp, :hum, :rain, :wind, :cond)
    """)
    with engine.begin() as conn:
        conn.execute(sql, {
            "city": city,
            "dt": weather.get("dt", 0), 
            "temp": weather.get("main", {}).get("temp"),
            "hum": weather.get("main", {}).get("humidity"),
            "rain": weather.get("rain", {}).get("1h", 0),
            "wind": weather.get("wind", {}).get("speed"),
            "cond": weather.get("weather", [{}])[0].get("main")
        })

def insert_user_query(city: str, m_score: float, h_score: float, reco: str):
    """Insert user query + scores."""
    sql = text("""
        INSERT INTO user_queries (city, mushroom_score, hiking_score, recommendation)
        VALUES (:city, :m, :h, :r)
    """)
    with engine.begin() as conn:
        conn.execute(sql, {"city": city, "m": m_score, "h": h_score, "r": reco})

