import os
import streamlit as st
import requests
from advisor import mushroom_score, hiking_score
from api_fetcher import fetch_weather
import base64

# --- Page Configuration ---
st.set_page_config(
    page_title="Spores & Outdoors", 
    page_icon="🍄🥾",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Enhanced Styling ---
st.markdown(
    """
    <style>
    /* Import modern fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600&display=swap');

    /* Global app styling */
    .stApp {
        font-family: 'Inter', sans-serif;
    }
    
    /* Remove default padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Main title styling */
    .main-title {
        font-family: 'Poppins', sans-serif;
        font-size: 3.5rem;
        font-weight: 700;
        text-align: center;
        background: linear-gradient(135deg, #2E8B57, #228B22, #32CD32);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
        text-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    /* Subtitle styling */
    .subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 1.3rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 300;
    }
    
    /* Weather card styling */
    .weather-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.2);
        margin: 1rem 0;
    }
    
    /* Input field styling */
    .stTextInput > div > div > input {
        border-radius: 15px;
        border: 2px solid #e0e0e0;
        padding: 0.75rem 1rem;
        font-size: 1.1rem;
        color: #154f24;
        transition: all 0.3s ease;
        background: rgba(255,255,255,0.9);
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #2E8B57;
        box-shadow: 0 0 0 3px rgba(46,139,87,0.1);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #2E8B57, #228B22);
        color: black;
        border: none;
        border-radius: 15px;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        font-weight: 500;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(46,139,87,0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(46,139,87,0.4);
    }
    
    /* Score cards */
    .score-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.9), rgba(240,248,255,0.9));
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 5px solid #2E8B57;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    }
    
    /* Weather metrics */
    .weather-metric {
        background: rgba(46,139,87,0.1);
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 3px solid #2E8B57;
    }
    
    /* Headers */
    h1, h2, h3 {
        font-family: 'Poppins', sans-serif;
        color: black;
    }
    
    /* Success/warning/info messages */
    .stSuccess, .stWarning, .stInfo {
        border-radius: 15px;
        border: none;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    /* Loading spinner */
    .stSpinner > div {
        border-top-color: #2E8B57 !important;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2.5rem;
        }
        .subtitle {
            font-size: 1.1rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- API key loader ---
@st.cache_data
def get_api_key():
    try:
        if "OPENWEATHER_API_KEY" in st.secrets:
            return st.secrets["OPENWEATHER_API_KEY"]
    except Exception:
        pass
    return os.getenv("OPENWEATHER_API_KEY")

API_KEY = get_api_key()

@st.cache_data
# def fetch_weather(city, api_key, units="metric"):
#     url = "https://api.openweathermap.org/data/2.5/weather"
#     r = requests.get(url, params={"q": city, "appid": api_key, "units": units}, timeout=10)
#     r.raise_for_status()
#     return r.json()

@st.cache_data
def get_base64_image(image_filename):
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(script_dir, image_filename)
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        return None

# --- Background image ---
bg_image = get_base64_image("background2.jpg")
if bg_image:
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{bg_image}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# --- UI Layout ---
# Header section 
st.markdown('<h1 class="main-title"> 🍄🥾 Spores & Outdoors 🍀</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Discover if today is perfect for mushroom foraging, hiking, or staying cozy indoors</p>', unsafe_allow_html=True)

# Create columns for better layout
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    # Input section
    st.markdown("### 📍 Choose Your Location")


    st.markdown("""
        <style>
        input::placeholder {
            color: #156e2d;  /* DodgerBlue for placeholder */
            font-weight: bold;
        }
        input {
            color: #156e2d;  /* ForestGreen for user input */
        }
        </style>
    """, unsafe_allow_html=True)


    city = st.text_input("", placeholder="Enter a city name (e.g., Berlin)", label_visibility="collapsed")
    
    # Check conditions button
    check_button = st.button("🌤️ Check Weather Conditions", use_container_width=True)

# Weather display section
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
            
        # Weather information display
        col_left, col_right = st.columns([1, 1])
        
        with col_left:
            st.markdown("### 🌤️ Current Weather")
            
            # Extract weather data
            main = weather.get("weather", [{}])[0].get("main", "—")
            desc = weather.get("weather", [{}])[0].get("description", "—").title()
            temp = weather.get("main", {}).get("temp", "—")
            humidity = weather.get("main", {}).get("humidity", "—")
            wind = weather.get("wind", {}).get("speed", "—")
            
            # Weather card
            st.markdown(f"""
            <div class="weather-card">
                <h4 style="margin-top: 0; color: #2E8B57;">📍 {city}</h4>
                <div class="weather-metric">
                <strong style="color: #1E90FF;">🌤️ Condition:</strong> <span style="color: #555;">{desc}</span> <span style="color: #888;">({main})</span>
                </div>
                <div class="weather-metric">
                    <strong style="color: #1E90FF;">🌡️ Temperature:</strong>  </span> <span style="color: #888;">{temp}°C
                </div>
                <div class="weather-metric">
                    <strong style="color: #1E90FF;">💧 Humidity:</strong> </span> <span style="color: #888;">{humidity}%
                </div>
                <div class="weather-metric">
                    <strong style="color: #1E90FF;">💨 Wind Speed:</strong> </span> <span style="color: #888;">{wind} m/s
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_right:
            st.markdown("### 🎯 Activity Scores")
            
            # Calculate scores
            m_score = mushroom_score(weather)
            h_score = hiking_score(weather)
            
            # Score cards
            st.markdown(f"""
            <div class="score-card">
                <h4 style="margin-top: 0; color: #8B4513;">🍄 Mushroom Foraging</h4>
                <div style="font-size: 2rem; font-weight: bold; color: #2E8B57;">{m_score}/10</div>
                <div style="color: #666; margin-top: 0.5rem;">
                    {"Excellent" if m_score >= 8 else "Good" if m_score >= 6 else "Fair" if m_score >= 4 else "Poor"} conditions
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="score-card">
                <h4 style="margin-top: 0; color: #4169E1;">🥾 Hiking</h4>
                <div style="font-size: 2rem; font-weight: bold; color: #2E8B57;">{h_score}/10</div>
                <div style="color: #666; margin-top: 0.5rem;">
                    {"Excellent" if h_score >= 8 else "Good" if h_score >= 6 else "Fair" if h_score >= 4 else "Poor"} conditions
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Final verdict section
        st.markdown("---")
        st.markdown("### 🎯 Today's Recommendation")
        
        col_verdict = st.columns(1)[0]
        with col_verdict:
            if max(m_score, h_score) < 5:
                st.warning("🏠 Not ideal for outdoor activities today. Perfect time to stay cozy indoors with a good book or movie! ☕")
            elif m_score > h_score:
                if m_score >= 8:
                    st.success("🍄 Exceptional mushroom foraging weather! Don't miss this opportunity to explore the forest!")
                else:
                    st.success("🍄 Great conditions for mushroom foraging! Pack your basket and head to the woods!")
            elif h_score > m_score:
                if h_score >= 8:
                    st.success("🥾 Perfect hiking weather! The trails are calling your name!")
                else:
                    st.success("🥾 Good day for a hike! Lace up those boots and enjoy nature!")
            else:
                st.info("🌟 Both activities look promising today! Follow your heart and choose your adventure! 🌍")
                
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

# Footer
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #666; font-size: 0.9rem; margin-top: 2rem;">
        🌿 Made with ❤️ for outdoor enthusiasts | Data powered by OpenWeatherMap
    </div>
    """, 
    unsafe_allow_html=True
)