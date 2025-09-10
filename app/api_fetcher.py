import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")  # safer than hardcoding
print("Loaded API key?", bool(os.getenv("OPENWEATHER_API_KEY")))
url = f"http://api.openweathermap.org/data/2.5/weather?q=Berlin&appid={API_KEY}&units=metric"
print(requests.get(url).json())
def get_weather(city="Berlin", units="metric"):
    if not API_KEY:
        return {"error": "Missing OpenWeather API key."}

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units={units}"
    response = requests.get(url)
    data = response.json()

    # Handle errors gracefully
    if response.status_code == 401:
        return {"error": "Unauthorized: Invalid API key."}
    if response.status_code == 404 or data.get("cod") == "404":
        return {"error": f"City '{city}' not found."}
    if response.status_code != 200:
        return {"error": f"API Error {response.status_code}: {data}"}

    # Normalize data into a consistent structure
    return {
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "description": data["weather"][0]["description"],
    }
