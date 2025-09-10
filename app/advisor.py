# advisor.py

def mushroom_foraging_score(weather: dict) -> int:
    """
    Calculates a mushroom foraging score based on weather and season.
    Returns a score from 0 to 100.
    """
    temp = weather.get("temperature", 0)
    humidity = weather.get("humidity", 0)
    rainfall = weather.get("rainfall_48h", 0)  # mm in last 48 hours
    month = weather.get("month", 0)

    score = 0

    # Ideal temperature range: 12–20°C
    if 12 <= temp <= 20:
        score += 25
    elif 8 <= temp < 12 or 20 < temp <= 24:
        score += 15

    # Humidity above 80% is ideal
    if humidity >= 80:
        score += 25
    elif humidity >= 65:
        score += 15

    # Rainfall sweet spot: 5–20 mm in last 48h
    if 5 <= rainfall <= 20:
        score += 25
    elif rainfall > 0:
        score += 10

    # Peak mushroom season: September–October
    if month in [9, 10]:
        score += 25
    elif month in [8, 11]:
        score += 15

    return min(score, 100)



def hiking_score(weather: dict) -> int:


    temp = weather["temperature"]
    desc = weather["description"]

    score = 0
    if 15 <= temp <= 25:
        score += 5
    if "rain" not in desc.lower():
        score += 5
    return score
