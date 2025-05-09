import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from weather_viewmodel import WeatherViewModel
from weather_model import WeatherModel


class WeatherView:
    def __init__(self, root, viewmodel):
        self.root = root
        self.vm = viewmodel
        self._setup_ui()
        
    def _setup_ui(self):
        self.root.title("🌦 Прогноз погоды")
        self.root.geometry("850x700")

        # Top frame
        frame_top = tk.Frame(self.root)
        frame_top.pack(pady=10)

        tk.Label(frame_top, text="Город:").pack(side=tk.LEFT)
        self.city_entry = tk.Entry(frame_top, width=30)
        self.city_entry.pack(side=tk.LEFT, padx=5)

        get_btn = tk.Button(frame_top, text="Получить погоду", command=self._on_get_weather)
        get_btn.pack(side=tk.LEFT, padx=5)

        # Weather info
        self.weather_label = tk.Label(self.root, textvariable=self.vm.current_weather, 
                                    justify="left", font=("Arial", 12))
        self.weather_label.pack(pady=10)

        # Charts frame
        self.frame_chart = tk.Frame(self.root)
        self.frame_chart.pack(fill="both", expand=True, padx=10, pady=10)

    def _on_get_weather(self):
        city = self.city_entry.get()
        if city:
            self.vm.update_weather(city)
            if self.vm.forecast_data is not None:
                self._plot_forecast(self.vm.forecast_data)

    def _plot_forecast(self, df):
        fig, axs = plt.subplots(2, 2, figsize=(10, 6))
        axs = axs.flatten()

        # Temperature
        axs[0].plot(df["date"], df["temp_c"], marker='o', label="Температура")
        axs[0].plot(df["date"], df["feelslike_c"], marker='o', linestyle='--', label="Ощущается")
        axs[0].set_title("Температура (°C)")
        axs[0].legend()

        axs[1].plot(df["date"], df["temp_c"], marker='s', color='orange')
        axs[1].set_title("Средняя температура (°C)")

        # Humidity
        axs[2].plot(df["date"], df["humidity"], marker='o', color='blue')
        axs[2].set_title("Влажность (%)")

        # Wind
        axs[3].plot(df["date"], df["wind_kph"], marker='o', color='green')
        axs[3].set_title("Скорость ветра (kph)")

        for ax in axs:
            ax.set_xticks(range(len(df["date"])))
            ax.set_xticklabels(df["date"], rotation=45)
            ax.grid(True)

        plt.tight_layout()

        # Clear previous chart
        for widget in self.frame_chart.winfo_children():
            widget.destroy()

        # Embed chart
        canvas = FigureCanvasTkAgg(fig, master=self.frame_chart)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    model = WeatherModel()
    viewmodel = WeatherViewModel(model)
    view = WeatherView(root, viewmodel)
    root.mainloop()
