import tkinter as tk
from tkinter import messagebox

class WeatherViewModel:
    def __init__(self, model):
        self.model = model
        self.current_weather = tk.StringVar()
        self.forecast_data = None
        
    def update_weather(self, city):
        try:
            raw_data = self.model.get_weather_data(city)
            self.forecast_data = self.model.prepare_forecast_data(raw_data)
            self._update_current_weather(raw_data)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _update_current_weather(self, data):
        current = data['current']
        location = data['location']
        text = (
            f"📍 {location['name']}, {location['country']}\n\n"
            f"🌡 Температура: {current['temp_c']}°C\n"
            f"🤔 Ощущается как: {current['feelslike_c']}°C\n"
            f"💧 Влажность: {current['humidity']}%\n"
            f"💨 Ветер: {current['wind_kph']} kph\n"
            f"📊 Давление: {current['pressure_mb']} mb\n"
            f"⛅️ Состояние: {current['condition']['text']}"
        )
        self.current_weather.set(text)