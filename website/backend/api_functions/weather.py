import requests
import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()

def get_weather(location: str) -> str:
    """
    Get current weather for a location by name.

    Args:
        location (str): Name of the location (city, address, or place name)

    Returns:
        str: Weather data as a string, or error message if failed
    """
    query = quote_plus(location)
    url = f"https://nominatim.openstreetmap.org/search?q={query}&format=json&limit=1"
    response = requests.get(url, headers={"User-Agent": "geo-coord-fetcher"})
    data = response.json()

    if not data:
        return "Error: Location not found"

    lat = float(data[0]["lat"])
    lon = float(data[0]["lon"])

    print(f"Fetching weather for {location} (lat={lat}, lon={lon})")
    weather_url = f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true'
    weather_response = requests.get(weather_url)

    if weather_response.status_code != 200:
        return f"Failed to get weather: {weather_response.text}"

    weather_data = weather_response.json()
    return str(weather_data)
