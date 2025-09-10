import requests

def fetch_weather(city: str, api_key: str, units: str = "metric") -> dict:
    """
    Fetch current weather from OpenWeatherMap API.
    Returns the raw JSON response as a Python dict.
    """
    url = "https://api.openweathermap.org/data/2.5/weather"
    r = requests.get(
        url,
        params={"q": city, "appid": api_key, "units": units},
        timeout=10
    )
    r.raise_for_status()
    return r.json()
