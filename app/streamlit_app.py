import streamlit as st
from api_fetcher import get_weather
from advisor import mushroom_score, hiking_score
import base64
import os

# --- Page config ---
st.set_page_config(page_title="HikeCast", page_icon="🍄", layout="wide")
st.title("🍄🥾 Mushroom & Hiking Weather Advisor 🍀🥾")

# --- Background setup ---
BASE_DIR = os.path.dirname(__file__)
main_bg_path = os.path.join(BASE_DIR, "bg.jpg")

if os.path.exists(main_bg_path):
    with open(main_bg_path, "rb") as f:
        encoded_bg = base64.b64encode(f.read()).decode()

    file_ext = os.path.splitext(main_bg_path)[1][1:]  # e.g., "jpg"

    st.markdown(
        f"""
        <style>
        [data-testid="stAppViewContainer"] {{
            background: url(data:image/{file_ext};base64,{encoded_bg});
            background-size: cover;
        }}
        [data-testid="stSidebar"] {{
            background: url(data:image/{file_ext};base64,{encoded_bg});
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
else:
    st.warning("Background image not found — make sure bg.jpg is in the app folder.")

# --- User input ---
city = st.text_input("Enter your city :3", "Berlin")

if st.button("Check Conditions"):
    # strip out weird chars like "<3"
    clean_city = "".join(ch for ch in city if ch.isalnum() or ch.isspace()).strip()

    weather = get_weather(clean_city)

    if "error" in weather:
        st.error(weather["error"])
    else:
        # Compute scores
        m_score = mushroom_score(weather)
        h_score = hiking_score(weather)

        # Show weather summary
        st.subheader(f"Weather in {clean_city}")
        st.write(f"🌡️ {weather['temperature']}°C — {weather['description']}")
        st.write(f"🍄 Mushroom Foraging Score: **{m_score}/10**")
        st.write(f"🥾 Hiking Score: **{h_score}/10**")

        # Recommendation
        if m_score >= 7:
            st.success("Great day for mushrooms! 🍄")
        elif h_score >= 7:
            st.success("Perfect for hiking! 🥾")
        else:
            st.warning("Maybe stay indoors today 🌧️")
