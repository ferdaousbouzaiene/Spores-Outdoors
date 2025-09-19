# app/db.py
import os
from sqlalchemy import create_engine, text
from sqlalchemy.exc import ArgumentError
from dotenv import load_dotenv
import streamlit as st

# Load local .env if present
load_dotenv()

# --- Resolve DATABASE_URL ---
DATABASE_URL = None

# 1. Try Streamlit secrets
try:
    if "DATABASE_URL" in st.secrets:
        DATABASE_URL = st.secrets["DATABASE_URL"]
except Exception:
    pass

# 2. Try system env
if not DATABASE_URL:
    DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError(
        "❌ DATABASE_URL not found. Please set it in .streamlit/secrets.toml or in a .env file"
    )

# --- Init DB connection ---
try:
    engine = create_engine(DATABASE_URL)
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    print("✅ Connected to database.")
except ArgumentError as e:
    raise RuntimeError(f"❌ Invalid DATABASE_URL format: {DATABASE_URL}") from e

# --- Functions ---
def insert_weather(city, weather_json):
    with engine.begin() as conn:
        conn.execute(
            text("INSERT INTO weather_data (city, payload) VALUES (:city, :payload)"),
            {"city": city, "payload": str(weather_json)}
        )

def insert_user_query(city, m_score, h_score, verdict):
    with engine.begin() as conn:
        conn.execute(
            text("INSERT INTO user_queries (city, mushroom_score, hiking_score, verdict) "
                 "VALUES (:city, :m, :h, :v)"),
            {"city": city, "m": m_score, "h": h_score, "v": verdict}
        )