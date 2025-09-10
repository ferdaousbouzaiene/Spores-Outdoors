import os
import streamlit as st
import requests
from advisor import mushroom_score, hiking_score

st.set_page_config(page_title="Spores & Outdoors", page_icon="🍄🥾")

# --- API key loader ---
def get_api_key():
    try:
        if "OPENWEATHER_API_KEY" in st.secrets:
            return st.secrets["OPENWEATHER_API_KEY"]
    except Exception:
        pass
    return os.getenv("OPENWEATHER_API_KEY")

API_KEY = get_api_key()

def fetch_weather(city, api_key, units="metric"):
    url = "https://api.openweathermap.org/data/2.5/weather"
    r = requests.get(url, params={"q": city, "appid": api_key, "units": units}, timeout=10)
    r.raise_for_status()
    return r.json()

# --- UI ---
st.title("🍄🥾 Spores & Outdoors")
st.caption("Is today for mushrooms, hiking, or Netflix?")

city = st.text_input("Enter a city", "Berlin")

if st.button("Check conditions"):
    if not API_KEY:
        st.error("Missing OpenWeather API key. Add it to `.streamlit/secrets.toml` or as an environment variable.")
        st.stop()

    try:
        weather = fetch_weather(city, API_KEY)
    except requests.HTTPError as e:
        status = getattr(e.response, "status_code", None)
        if status == 401:
            st.error("Invalid API key — check your OpenWeather key.")
        elif status == 404:
            st.error(f"City '{city}' not found.")
        else:
            st.error("Weather service not available right now.")
        st.stop()

    # Show quick weather summary (compact, no fancy columns)
    main = weather.get("weather", [{}])[0].get("main", "—")
    desc = weather.get("weather", [{}])[0].get("description", "—").title()
    temp = weather.get("main", {}).get("temp", "—")

    st.subheader(f"Weather in {city}")
    st.write(f"🌤️ {desc} ({main})")
    st.write(f"🌡️ Temperature: {temp}°C")

    # Advisor scores
    m_score = mushroom_score(weather)
    h_score = hiking_score(weather)

    st.subheader("Scores")
    st.write(f"🍄 Mushroom Foraging Score: **{m_score}/10**")
    st.write(f"🥾 Hiking Score: **{h_score}/10**")

    # Verdict
    if max(m_score, h_score) < 5:
        st.warning("Not great for outdoors today… maybe stay cozy indoors 🛋️")
    elif m_score > h_score:
        st.success("Perfect for mushroom foraging! 🍄")
    elif h_score > m_score:
        st.success("Ideal for hiking! 🥾")
    else:
        st.info("Both look pretty good — your choice! 🌍")
