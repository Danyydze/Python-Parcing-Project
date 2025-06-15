import tkinter as tk
from tkinter import messagebox

class WeatherViewModel:
    def __init__(self, model):
        self.model = model
        self.current_weather = tk.StringVar()
        self.forecast_data = None
        
    def update_weather(self, city, source="weatherapi"):
        try:
            if source == "weatherapi":
                raw_data = self.model.get_weather_data(city)
            elif source == "openweathermap":
                raw_data = self.model.get_owm_data(city)
            else:
                raise ValueError("Неизвестный источник данных")

            self.forecast_data = self.model.prepare_forecast_data(raw_data, source)
            self._update_current_weather(raw_data, source)
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def _update_current_weather(self, data, source):
        if source == 'weatherapi':
            current = data['current']
            location = data['location']
            condition = current['condition']['text']
            temp = current['temp_c']
            feels_like = current['feelslike_c']
            humidity = current['humidity']
            wind = current['wind_kph']
            country = location.get('country', 'N/A')
            city = location.get('name', 'N/A')
        else:  # openweathermap
            current = data['list'][0]
            main = current['main']
            wind_data = current['wind']
            weather = current['weather'][0]
            city = data['city'].get('name', 'N/A')
            country = data['city'].get('country', 'N/A')
            temp = main.get('temp', 'N/A')
            feels_like = main.get('feels_like', 'N/A')
            humidity = main.get('humidity', 'N/A')
            wind = wind_data.get('speed', 0) * 3.6  # м/с → км/ч
            condition = weather.get('description', 'N/A')

        text = (
            f"📍 {city}, {country}\n\n"
            f"🌡 Температура: {temp}°C\n"
            f"🤔 Ощущается как: {feels_like}°C\n"
            f"💧 Влажность: {humidity}%\n"
            f"💨 Ветер: {wind:.1f} kph\n"
            f"⛅️ Состояние: {condition.capitalize()}"
        )
        self.current_weather.set(text)