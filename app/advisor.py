def mushroom_score(weather: dict) -> int:
    main = weather.get("main", {})
    temp = main.get("temp")
    humidity = main.get("humidity")
    rain = weather.get("rain", {}).get("1h", 0)

    score = 0
    if temp is not None and 10 <= temp <= 22:
        score += 3
    if humidity and humidity > 70:
        score += 3
    if rain > 0:
        score += 4

    return min(score, 10)


def hiking_score(weather: dict) -> int:
    main = weather.get("main", {})
    temp = main.get("temp")
    condition = weather.get("weather", [{}])[0].get("main", "")
    wind = weather.get("wind", {}).get("speed", 0)

    score = 0
    if temp is not None and 15 <= temp <= 28:
        score += 4
    if condition in ["Clear", "Clouds"]:
        score += 4
    if wind < 5:
        score += 2

    return min(score, 10)
