import requests
import tkinter as tk
from plyer import notification

def get_weather():
    city = city_entry.get()

    geo_url = "https://geocoding-api.open-meteo.com/v1/search"
    geo_params = {"name": city, "count": 1}
    geo_res = requests.get(geo_url, params=geo_params).json()

    if "results" in geo_res:
        lat = geo_res["results"][0]["latitude"]
        lon = geo_res["results"][0]["longitude"]

        weather_url = "https://api.open-meteo.com/v1/forecast"
        weather_params = {
            "latitude": lat,
            "longitude": lon,
            "current_weather": True
        }
        weather_res = requests.get(weather_url, params=weather_params).json()

        if "current_weather" in weather_res:
            temp = weather_res["current_weather"]["temperature"]
            wind = weather_res["current_weather"]["windspeed"]

            result = f"{city}: {temp}°C, Wind {wind} km/h"
            result_label.config(text=result)

            notification.notify(
                title="Weather Update",
                message=result,
                timeout=5
            )
        else:
            result_label.config(text="Weather not found")
    else:
        result_label.config(text="City not found")


# GUI
app = tk.Tk()
app.title("Weather App")
app.geometry("300x200")

tk.Label(app, text="Enter City").pack()

city_entry = tk.Entry(app)
city_entry.pack()

tk.Button(app, text="Get Weather", command=get_weather).pack()

result_label = tk.Label(app, text="")
result_label.pack()

app.mainloop()