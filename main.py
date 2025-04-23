import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import requests
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg



# Глобальная переменная для хранения прогноза
weather_forecast_data = None
def load_api_key(filepath="api_key.txt"):
    try:
        with open(filepath, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        raise Exception("Файл с API ключом не найден. Убедитесь, что 'api_key.txt' существует.")

API_KEY = load_api_key()
def get_weather(city):
    url = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={city}&days=7&aqi=no&alerts=no"
    try:
        response = requests.get(url)
        data = response.json()
        if "error" in data:
            raise Exception(data["error"]["message"])
        return data
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось получить данные: {e}")
        return None

def show_current_weather(data):
    current = data['current']
    location = data['location']
    output = (
        f"📍 {location['name']}, {location['country']}\n\n"
        f"🌡 Температура: {current['temp_c']}°C\n"
        f"🤔 Ощущается как: {current['feelslike_c']}°C\n"
        f"💧 Влажность: {current['humidity']}%\n"
        f"💨 Ветер: {current['wind_kph']} kph\n"
        f"📊 Давление: {current['pressure_mb']} mb\n"
        f"⛅ Состояние: {current['condition']['text']}"
    )
    weather_text.set(output)

def prepare_forecast_data(data):
    forecast_days = data['forecast']['forecastday']
    weather_data = {
        "date": [],
        "temp_c": [],
        "feelslike_c": [],
        "humidity": [],
        "wind_kph": []
    }

    for day in forecast_days:
        weather_data["date"].append(day['date'])
        weather_data["temp_c"].append(day['day']['avgtemp_c'])
        weather_data["feelslike_c"].append(day['day']['maxtemp_c'])  # Используем max для разнообразия
        weather_data["humidity"].append(day['day']['avghumidity'])
        weather_data["wind_kph"].append(day['day']['maxwind_kph'])

    return pd.DataFrame(weather_data)



def plot_forecast(df):
    fig, axs = plt.subplots(2, 2, figsize=(10, 6))
    axs = axs.ravel()

    # Температура
    axs[0].plot(df["date"], df["temp_c"], marker='o', label="Температура")
    axs[0].plot(df["date"], df["feelslike_c"], marker='o', linestyle='--', label="Ощущается")
    axs[0].set_title("Температура (°C)")
    axs[0].legend()

   
    axs[1].plot(df["date"], df["temp_c"], marker='s', color='orange')
    axs[1].set_title("Средняя температура (°C)")


    # Влажность
    axs[2].plot(df["date"], df["humidity"], marker='o', color='blue')
    axs[2].set_title("Влажность (%)")

    # Ветер
    axs[3].plot(df["date"], df["wind_kph"], marker='o', color='green')
    axs[3].set_title("Скорость ветра (kph)")

    for ax in axs:
        ax.set_xticks(range(len(df["date"])))
        ax.set_xticklabels(df["date"], rotation=45)
        ax.grid(True)

    plt.tight_layout()

    # Отображение графиков в окне
    for widget in frame_chart.winfo_children():
        widget.destroy()
    canvas = FigureCanvasTkAgg(fig, master=frame_chart)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

def on_get_weather():
    global weather_forecast_data
    city = city_entry.get()
    if not city:
        messagebox.showwarning("Внимание", "Введите город.")
        return
    data = get_weather(city)
    if data:
        weather_forecast_data = prepare_forecast_data(data)
        show_current_weather(data)
        plot_forecast(weather_forecast_data)

# --- Интерфейс ---
root = tk.Tk()
root.title("🌦 Прогноз погоды")
root.geometry("850x700")

frame_top = tk.Frame(root)
frame_top.pack(pady=10)

tk.Label(frame_top, text="Город:").pack(side=tk.LEFT)
city_entry = tk.Entry(frame_top, width=30)
city_entry.pack(side=tk.LEFT, padx=5)

get_button = tk.Button(frame_top, text="Получить погоду", command=on_get_weather)
get_button.pack(side=tk.LEFT, padx=5)

# Текстовая информация
weather_text = tk.StringVar()
weather_label = tk.Label(root, textvariable=weather_text, justify="left", font=("Arial", 12))
weather_label.pack(pady=10)

# Графики
frame_chart = tk.Frame(root)
frame_chart.pack(fill="both", expand=True, padx=10, pady=10)

root.mainloop()

