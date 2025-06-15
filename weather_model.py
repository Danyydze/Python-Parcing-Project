import requests
import pandas as pd

class WeatherModel:
    def __init__(self):
        self.weather_api_key = self._load_api_key("api_key.txt")
        self.owm_api_key = self._load_api_key("owm_api_key.txt")
        
    @staticmethod
    def _load_api_key(filepath):
        try:
            with open(filepath, "r") as f:
                return f.read().strip()
        except FileNotFoundError:
            raise Exception(f"API key file {filepath} not found")

    def get_weather_data(self, city):
        """Получение данных с WeatherAPI"""
        url = f"http://api.weatherapi.com/v1/forecast.json?key={self.weather_api_key}&q={city}&days=7&lang=ru"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def get_owm_data(self, city):
        """Получение данных с OpenWeatherMap"""
        url = "http://api.openweathermap.org/data/2.5/forecast"
        params = {
            'q': city,
            'appid': self.owm_api_key,
            'units': 'metric',
            'lang': 'ru'
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def prepare_forecast_data(self, data, source='weatherapi'):
        """Подготовка данных для графиков"""
        if source == 'weatherapi':
            return self._prepare_weatherapi(data)
        elif source == 'openweathermap':
            return self._prepare_owm(data)
        else:
            raise ValueError("Неизвестный источник данных")

    def _prepare_weatherapi(self, data):
        forecast_days = data['forecast']['forecastday']
        return pd.DataFrame({
            "date": [day['date'] for day in forecast_days],
            "temp_c": [day['day']['avgtemp_c'] for day in forecast_days],
            "feelslike_c": [day['day']['maxtemp_c'] for day in forecast_days],
            "humidity": [day['day']['avghumidity'] for day in forecast_days],
            "wind_kph": [day['day']['maxwind_kph'] for day in forecast_days]
        })

    def _prepare_owm(self, data):
        dates = []
        temps = []
        feels = []
        hums = []
        winds = []

        for item in data['list']:
            dates.append(item['dt_txt'][:10])  # дата в формате YYYY-MM-DD
            temps.append(item['main']['temp'])
            feels.append(item['main']['feels_like'])
            hums.append(item['main']['humidity'])
            winds.append(item['wind']['speed'] * 3.6)  # м/с → км/ч

        df = pd.DataFrame({
            "date": dates,
            "temp_c": temps,
            "feelslike_c": feels,
            "humidity": hums,
            "wind_kph": winds
        })

        # Группируем по дате, берем среднее значение за день
        df = df.groupby("date").mean().reset_index()
        return df
