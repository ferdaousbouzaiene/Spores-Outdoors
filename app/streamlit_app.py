import os
import streamlit as st
import requests
from advisor import mushroom_score, hiking_score

import base64
st.set_page_config(page_title="Spores & Outdoors", page_icon="🍄🥾")
st.markdown(
    """
    <style>
    /* Import a Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Fredoka+One&family=Roboto:wght@300;500&display=swap');

    /* Change overall app font */
    html, body, [class*="css"]  {
        font-family: 'Quicksand', sans-serif;
    }

    /* Style headers (title, subheaders) */
    h1, h2, h3 {
        font-family: 'Quicksand', cursive;
        color: #2E8B57;  /* forest green for vibe */
    }

    /* Optional: style captions */
    .stCaption {
        font-style: italic;
        color: #555;
    }
    </style>
    """,
    unsafe_allow_html=True
)


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
@st.cache_data
def get_base64_image(image_filename):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(script_dir, image_filename)
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

bg_image = get_base64_image("background2.jpg")



# --- Background image ---
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("data:jpg;base64,{bg_image}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# --- UI ---
st.title("🍄🥾 Spores & Outdoors 🍀")
st.caption("Is today for mushrooms, hiking, or Netflix?")

city = st.text_input("Enter a city", "Berlin")
with st.spinner("Fetching weather..."):
    weather = fetch_weather(city, API_KEY)

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

    # Quick weather summary
    main = weather.get("weather", [{}])[0].get("main", "—")
    desc = weather.get("weather", [{}])[0].get("description", "—").title()
    temp = weather.get("main", {}).get("temp", "—")

    st.subheader(f"Weather in {city}")
    st.write(f"🌤️ {desc} ({main})")
    st.write(f"🌡️ Temperature: {temp}°C")
    humidity = weather.get("main", {}).get("humidity", "—")
    wind = weather.get("wind", {}).get("speed", "—")

    st.write(f"💧 Humidity: {humidity}%")
    st.write(f"💨 Wind Speed: {wind} m/s")

    # Advisor scores
    m_score = mushroom_score(weather)
    h_score = hiking_score(weather)

    st.subheader("Verdict?")
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