import os
import streamlit as st
import requests
from advisor import mushroom_report, hiking_report
from db import insert_weather, insert_user_query
from api_fetcher import fetch_weather
import base64
from dotenv import load_dotenv
load_dotenv()


# --- Page Config 🐼 --- #
st.set_page_config(
    page_title="Spores & Outdoors",
    page_icon="🍄🥾",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Background Handling 🖼️ --- #
@st.cache_data
def get_base64_image(image_filename):
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(script_dir, image_filename)
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        return None

bg_image = get_base64_image("background2.jpg")

# --- Cute Theme CSS Only 🌸 --- #
custom_css = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;600&family=Inter:wght@300;500&display=swap');

.stApp {{
    font-family: 'Inter', sans-serif;
    background-image: url("data:image/jpg;base64,{bg_image}");
    background-size: cover;
    background-attachment: fixed;
}}

.main-title {{
    font-family: 'Poppins', sans-serif;
    font-size: 3.5rem;
    font-weight: 700;
    text-align: center;
    background: linear-gradient(135deg, #ffb6c1, #98fb98, #f0e68c);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: title-shimmer 6s ease infinite;
}}

@keyframes title-shimmer {{
    0% {{ background-position: 0% 50%; }}
    50% {{ background-position: 100% 50%; }}
    100% {{ background-position: 0% 50%; }}
}}

.weather-card, .score-card {{
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    padding: 2rem;
    box-shadow: 0 8px 24px rgba(0,0,0,0.08);
    animation: floaty 6s ease-in-out infinite;
}}

@keyframes floaty {{
    0% {{ transform: translateY(0); }}
    50% {{ transform: translateY(-5px); }}
    100% {{ transform: translateY(0); }}
}}

.stTextInput > div > div > input {{
    border-radius: 15px;
    border: 2px solid #f4c2c2;
    padding: 0.75rem 1rem;
    font-size: 1.1rem;
    color: #154f24;
}}

.stButton > button {{
    background: linear-gradient(135deg, #ffc0cb, #b0e57c);
    border-radius: 15px;
    color: #333;
    font-weight: 600;
}}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# --- API Key Loader --- #
@st.cache_data
def get_api_key():
    try:
        if "OPENWEATHER_API_KEY" in st.secrets:
            return st.secrets["OPENWEATHER_API_KEY"]
    except Exception:
        pass
    return os.getenv("OPENWEATHER_API_KEY")

API_KEY = get_api_key()

# --- UI Layout --- #
st.markdown("""
<h1 style="text-align: center; font-size: 3.5rem; font-family: 'Poppins', sans-serif; font-weight: 700;">
    <span style="font-size: 2.5rem;">🍄🥾</span>
    <span style="
        background: linear-gradient(135deg, #ffb6c1, #98fb98, #f0e68c);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    ">
        Spores & Outdoors
    </span>
    <span style="font-size: 2.5rem;">🍀</span>
</h1>
""", unsafe_allow_html=True)

st.markdown("""
    <div style="
        text-align: center;
        font-family: 'Inter', sans-serif;
        font-size: 1.3rem;
        color: #50ba70;
        font-weight: 300;
        margin-top: -0.5rem;
        margin-bottom: 2rem;
        max-width: 700px;
        margin-left: auto;
        margin-right: auto;
    ">
        Discover if today is perfect for mushroom foraging, hiking, or staying cozy indoors
    </div>
""", unsafe_allow_html=True)

# Location input
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("### 📍 Choose Your Location")
    st.markdown("""
        <style>
        input::placeholder {
            color: #156e2d;
            font-weight: bold;
        }

        input {
            color: #5f8c6b !important;  /* Soft cute green */
            font-weight: 500 !important;
            background-color: rgba(255, 255, 255, 0.8) !important;
            border-radius: 12px !important;
        }
        </style>
    """, unsafe_allow_html=True)

    city = st.text_input("", placeholder="Enter a city name (e.g., Berlin)", label_visibility="collapsed")
    check_button = st.button("🌤️ Check Weather Conditions", use_container_width=True)

# --- Weather Logic --- #
if check_button or city:
    if not API_KEY:
        st.error("⚠️ Missing OpenWeather API key. Add it to `.streamlit/secrets.toml` or as an environment variable.")
        st.stop()

    if not city.strip():
        st.warning("📝 Please enter a city name to check the weather conditions.")
        st.stop()

    try:
        with st.spinner("🌍 Fetching weather data..."):
            weather = fetch_weather(city, API_KEY)

        col_left, col_right = st.columns([1, 1])

        # --- Weather Card --- #
        with col_left:
            st.markdown("### 🌤️ Current Weather")
            main = weather.get("weather", [{}])[0].get("main", "—")
            desc = weather.get("weather", [{}])[0].get("description", "—").title()
            temp = weather.get("main", {}).get("temp", "—")
            humidity = weather.get("main", {}).get("humidity", "—")
            wind = weather.get("wind", {}).get("speed", "—")

            st.markdown(f"""
            <div class="weather-card">
                <h4 style="margin-top: 0;">
                    <span style="font-size: 1.5rem;">📍</span>
                    <span style="color: #5f8c6b;">{city}</span>
                </h4>
                <div class="weather-metric">
                    <strong style="color: #1E90FF;">🌤️ Condition:</strong>
                    <span style="color: #333;"> {desc}</span>
                    <span style="color: #888;"> ({main})</span>
                </div>
                <div class="weather-metric">
                    <strong style="color: #1E90FF;">🌡️ Temperature:</strong>
                    <span style="color: #333;"> {temp}°C</span>
                </div>
                <div class="weather-metric">
                    <strong style="color: #1E90FF;">💧 Humidity:</strong>
                    <span style="color: #333;"> {humidity}%</span>
                </div>
                <div class="weather-metric">
                    <strong style="color: #1E90FF;">💨 Wind Speed:</strong>
                    <span style="color: #333;"> {wind} m/s</span>
                </div>
            </div>
            """, unsafe_allow_html=True)


        # --- Score Cards --- #
        with col_right:
            st.markdown("### 🎯 Activity Scores")

            mushroom = mushroom_report(weather)
            hiking = hiking_report(weather)

            m_score, m_expl = mushroom["score"], mushroom["explanation"]
            h_score, h_expl = hiking["score"], hiking["explanation"]

            def render_reasons(reasons: list[str]) -> str:
                if not reasons:
                    return "<em>No major contributing factors</em>"
                return "<ul style='margin-top:0.5rem; color:#444; font-size:0.95rem;'>" + "".join(
                    f"<li>{r}</li>" for r in reasons
                ) + "</ul>"

            # Mushroom
            st.markdown(f"""
            <div class="score-card" style="margin-bottom: 2rem;">
                <h4 style="margin-top: 0; color: #8B4513;">🍄 Mushroom Foraging</h4>
                <div style="font-size: 2rem; font-weight: bold; color: #2E8B57;">{m_score}/10</div>
                <div style="color: #666; margin-top: 0.5rem;">
                    {"Excellent" if m_score >= 8 else "Good" if m_score >= 6 else "Fair" if m_score >= 4 else "Poor"} conditions
                </div>
                {render_reasons(m_expl)}
            </div>
            """, unsafe_allow_html=True)

            # Hiking
            st.markdown(f"""
            <div class="score-card">
                <h4 style="margin-top: 0; color: #4169E1;">🥾 Hiking</h4>
                <div style="font-size: 2rem; font-weight: bold; color: #2E8B57;">{h_score}/10</div>
                <div style="color: #666; margin-top: 0.5rem;">
                    {"Excellent" if h_score >= 8 else "Good" if h_score >= 6 else "Fair" if h_score >= 4 else "Poor"} conditions
                </div>
                {render_reasons(h_expl)}
            </div>
            """, unsafe_allow_html=True)

        # --- Final Verdict --- #
        st.markdown("---")
        st.markdown("### 🎯 Today's Recommendation")

        if max(m_score, h_score) < 5:
            st.warning("🏠 Not ideal for outdoor activities today. Perfect time to stay cozy indoors with a good book or movie! ☕")
            verdict = "indoors"
        elif m_score > h_score:
            st.success("🍄 Exceptional mushroom foraging weather!" if m_score >= 8 else "🍄 Great conditions for mushroom foraging!")
            verdict = "mushroom"
        elif h_score > m_score:
            st.success("🥾 Perfect hiking weather!" if h_score >= 8 else "🥾 Good day for a hike!")
            verdict = "hiking"
        else:
            st.info("🌟 Both activities look promising today! Follow your heart and choose your adventure! 🌍")
            verdict = "either"
        insert_user_query(city, m_score, h_score, verdict)

    except requests.HTTPError as e:
        status = getattr(e.response, "status_code", None)
        if status == 401:
            st.error("🔑 Invalid API key. Please check your OpenWeather API key.")
        elif status == 404:
            st.error(f"🗺️ City '{city}' not found. Please check the spelling and try again.")
        else:
            st.error("🌐 Weather service temporarily unavailable. Please try again in a moment.")
    except Exception as e:
        st.error(f"❌ An unexpected error occurred: {str(e)}")

# --- Footer --- #
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.9rem; margin-top: 2rem;">
        🌿 Made with ❤️ for outdoor enthusiasts | Data powered by OpenWeatherMap
    </div>
    """, unsafe_allow_html=True
)
