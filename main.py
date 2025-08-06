from presentation.terminal_interface import select_city, display_forecast
from logic.controller import fetch_forecast_by_city_name

def main():
    city = select_city()
    forecast = fetch_forecast_by_city_name(city)
    
    if forecast:
        display_forecast(forecast)
    else:
        print("Unable to fetch forecast. Please try again later.")

from presentation.gui_interface import run_gui

if __name__ == "__main__":
    run_gui()
