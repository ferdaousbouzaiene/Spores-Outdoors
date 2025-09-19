-- Database: spores

-- Drop tables if they exist (for re-runs during dev)
DROP TABLE IF EXISTS user_queries;
DROP TABLE IF EXISTS weather_data;

-- Weather observations table
CREATE TABLE weather_data (
    id SERIAL PRIMARY KEY,
    city TEXT NOT NULL,
    ts TIMESTAMP NOT NULL,             -- when the weather is valid (from API)
    fetched_at TIMESTAMP DEFAULT NOW(),-- when we pulled it
    temperature FLOAT,
    humidity FLOAT,
    rainfall FLOAT,
    wind_speed FLOAT,
    condition TEXT
);

-- User queries / app interactions
CREATE TABLE user_queries (
    id SERIAL PRIMARY KEY,
    city TEXT NOT NULL,
    ts TIMESTAMP DEFAULT NOW(),        -- query time
    mushroom_score FLOAT,
    hiking_score FLOAT,
    recommendation TEXT
);

-- Indexes to speed up queries
CREATE INDEX idx_weather_city_ts ON weather_data(city, ts);
CREATE INDEX idx_user_city_ts ON user_queries(city, ts);
