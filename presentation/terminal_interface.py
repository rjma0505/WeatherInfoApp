from data_access.ipma_api import listar_cidades

def select_city():
    cities = listar_cidades()
    if not cities:
        print("Could not fetch cities.")
        return None

    print("\nSelect a city:")
    for idx, city in enumerate(cities, 1):
        print(f"{idx}. {city['local']}")

    while True:
        try:
            choice = int(input("\nEnter the number of the city: "))
            if 1 <= choice <= len(cities):
                return cities[choice - 1]["local"]
            else:
                print("Invalid number. Try again.")
        except ValueError:
            print("Please enter a valid number.")


def display_forecast(forecast_data):
    print("\nWeather Forecast:")
    for day in forecast_data:
        print(f"{day['date']}: {day['weather_description']} - Min: {day['tMin']}°C | Max: {day['tMax']}°C")
