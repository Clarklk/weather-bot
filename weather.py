from requests import get as make_request_to
from datetime import datetime
# Shahar nomi qabul qilib shu shahardagi ob-havo ma'lumotini olish
# openweathermap.org -> shahar nomini berish orqali shu shahardagi ob-havo ma'lumotlarini beradigan API servis

API_KEY = "9ff2206588d4121162efd6d4bba6c220"


def get_weather_data(city_name: str, key: str = API_KEY) -> str | None:
    response = make_request_to(
        url=f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={key}&units=metric")
    data = response.json()  # JSON -> Python

    if data['cod'] != 404:
        text = f"""Bugun 🏙️ {city_name.capitalize()} da
        
🌡️ Havo harorati: {data['main']['temp']} C
🥵 Minimal harorat: {data['main']['temp_min']} C
🥶 Maksimal harorat: {data['main']['temp_max']} C

💦 Namlik: {data['main']['humidity']} %
䷮ Bosim: {data['main']['pressure']} Pa
💨 Shamol tezligi: {data['wind']['speed']} m/s

🌅 Quyosh chiqish vaqti: {datetime.fromtimestamp(int(data['sys']['sunrise'])).strftime("%H:%M:%S")}
🌇 Quyosh botish vaqti: {datetime.fromtimestamp(int(data['sys']['sunset'])).strftime("%H:%M:%S")}
"""

        return text
    else:
        return None 
