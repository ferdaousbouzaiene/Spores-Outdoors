import requests
import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

def get_weather(city="Berlin", units="metric", api_key=None):
    # Get API key from parameter, secrets, or environment variable
    if api_key is None:
        try:
            api_key = st.secrets["OPENWEATHER_API_KEY"]
        except:
            api_key = os.getenv("OPENWEATHER_API_KEY")
    
    if not api_key:
        return {"error": "Missing OpenWeather API key. Please set it in secrets.toml or as an environment variable."}

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units={units}"

    try:
        response = requests.get(url, timeout=10)
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
    
    except requests.exceptions.RequestException as e:
        return {"error": f"Network error: {str(e)}"}
    except KeyError as e:
        return {"error": f"Unexpected API response format: missing {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}