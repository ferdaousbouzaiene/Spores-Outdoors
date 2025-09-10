"""
advisor.py
----------
Scoring functions and wrappers for Spores & Outdoors.

Provides:
- normalize_weather(api_weather: dict) -> dict
- mushroom_foraging_score(weather: dict) -> float
- hiking_comfort_score(weather: dict) -> float
- mushroom_score(api_weather: dict) -> float  # wrapper
- hiking_score(api_weather: dict) -> float    # wrapper
"""

from datetime import datetime
from typing import Optional


def normalize_weather(api_weather: dict) -> dict:
    """Convert OpenWeather API JSON to the format expected by scoring functions."""
    main = api_weather.get("main", {})
    temp = main.get("temp", 0)
    humidity = main.get("humidity", 0)
    wind_speed = api_weather.get("wind", {}).get("speed", 0)

    # Approx rainfall (OpenWeather only gives recent windows, not 48h totals)
    rain = api_weather.get("rain", {})
    rainfall_24h = rain.get("1h", 0) + rain.get("3h", 0)
    rainfall_48h = rainfall_24h  # fallback until you collect longer history

    # Month from timestamp
    dt = api_weather.get("dt")
    month = datetime.utcfromtimestamp(dt).month if dt else 0

    return {
        "temperature": temp,
        "humidity": humidity,
        "wind_speed": wind_speed,
        "rainfall_24h": rainfall_24h,
        "rainfall_48h": rainfall_48h,
        "month": month,
        # optional extras (future features)
        "soil_moisture": None,
        "uv_index": None,
        "daylight_hours": None,
    }


def mushroom_foraging_score(weather: dict) -> float:
    """
    Calculates a mushroom foraging score (0–10).
    """
    temp = weather.get("temperature", 0)
    humidity = weather.get("humidity", 0)
    rainfall = weather.get("rainfall_48h", 0)
    month = weather.get("month", 0)
    soil_moisture: Optional[float] = weather.get("soil_moisture")

    score = 0

    # 🌡️ Temperature
    if 12 <= temp <= 20:
        score += 25
    elif 8 <= temp < 12 or 20 < temp <= 24:
        score += 15

    # 💧 Humidity
    if humidity >= 85:
        score += 20
    elif humidity >= 70:
        score += 10

    # 🌧️ Rainfall (last 48h)
    if 5 <= rainfall <= 25:
        score += 20
    elif rainfall > 0:
        score += 10

    # 🍂 Seasonality
    if month in [9, 10]:
        score += 20
    elif month in [8, 11]:
        score += 10

    # 🌱 Soil moisture (optional)
    if soil_moisture is not None:
        if 30 <= soil_moisture <= 60:
            score += 15
        elif 20 <= soil_moisture < 30 or 60 < soil_moisture <= 70:
            score += 8

    return round(min(score, 100) / 10, 1)


def hiking_comfort_score(weather: dict) -> float:
    """
    Calculates a hiking comfort score (0–10).
    """
    temp = weather.get("temperature", 0)
    humidity = weather.get("humidity", 0)
    wind_speed = weather.get("wind_speed", 0)
    rainfall = weather.get("rainfall_24h", 0)
    month = weather.get("month", 0)
    uv_index: Optional[float] = weather.get("uv_index")
    daylight_hours: Optional[float] = weather.get("daylight_hours")

    score = 0

    # 🌡️ Temperature
    if 15 <= temp <= 24:
        score += 30
    elif 10 <= temp < 15 or 24 < temp <= 28:
        score += 20

    # 💧 Humidity
    if humidity <= 60:
        score += 15
    elif humidity <= 75:
        score += 10

    # 💨 Wind
    if 0 <= wind_speed <= 5:
        score += 15
    elif 5 < wind_speed <= 8:
        score += 10

    # 🌧️ Rainfall
    if rainfall == 0:
        score += 15
    elif rainfall <= 3:
        score += 8
    else:
        score -= 10

    # ☀️ UV index
    if uv_index is not None:
        if 0 <= uv_index <= 5:
            score += 10
        elif 6 <= uv_index <= 7:
            score += 5
        else:
            score -= 5

    # 🌅 Daylight
    if daylight_hours is not None:
        if daylight_hours >= 10:
            score += 10
        elif 7 <= daylight_hours < 10:
            score += 5
        else:
            score -= 5

    # 🍂 Seasonal bonus
    if month in [4, 5, 9, 10]:
        score += 5

    return round(max(0, min(score, 100)) / 10, 1)


# --- Wrappers so Streamlit app can call directly with raw API JSON ---
def mushroom_score(api_weather: dict) -> float:
    return mushroom_foraging_score(normalize_weather(api_weather))


def hiking_score(api_weather: dict) -> float:
    return hiking_comfort_score(normalize_weather(api_weather))
