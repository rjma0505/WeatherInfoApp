def parse_forecast_data(forecast_list):
    forecast = []
    for day in forecast_list:
        if "forecastDate" not in day:
            continue
        forecast.append({
            "date": day["forecastDate"],
            "tMin": day.get("tMin", "N/A"),
            "tMax": day.get("tMax", "N/A"),
            "weather_description": get_weather_description(day.get("idWeatherType", -1)),
        })
    return forecast

def get_weather_description(weather_type_id):
    mapping = {
        0: "Clear sky",
        1: "Partly cloudy",
        2: "Cloudy",
        3: "Overcast",
        4: "Rain",
        5: "Heavy rain",
        6: "Showers",
        7: "Thunderstorm",
    }
    return mapping.get(weather_type_id, f"Unknown (ID {weather_type_id})")
