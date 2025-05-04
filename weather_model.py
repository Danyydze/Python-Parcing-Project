import requests
import pandas as pd

class WeatherModel:
    def __init__(self):
        self.api_key = self._load_api_key()
        
    @staticmethod
    def _load_api_key(filepath="api_key.txt"):
        try:
            with open(filepath, "r") as f:
                return f.read().strip()
        except FileNotFoundError:
            raise Exception("API key file not found")

    def get_weather_data(self, city):
        url = f"http://api.weatherapi.com/v1/forecast.json?key={self.api_key}&q={city}&days=7"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def prepare_forecast_data(self, data):
        forecast_days = data['forecast']['forecastday']
        return pd.DataFrame({
            "date": [day['date'] for day in forecast_days],
            "temp_c": [day['day']['avgtemp_c'] for day in forecast_days],
            "feelslike_c": [day['day']['maxtemp_c'] for day in forecast_days],
            "humidity": [day['day']['avghumidity'] for day in forecast_days],
            "wind_kph": [day['day']['maxwind_kph'] for day in forecast_days]
        })