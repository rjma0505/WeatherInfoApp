from presentation.terminal_interface import select_city, display_forecast
from logic.controller import fetch_forecast_by_city_name

def main():
    city = select_city()
    forecast = fetch_forecast_by_city_name(city)
    
    if forecast:
        display_forecast(forecast)
    else:
        print("Unable to fetch forecast. Please try again later.")

if __name__ == "__main__":
    main()
