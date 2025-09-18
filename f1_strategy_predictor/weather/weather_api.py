import os 
import requests
from dotenv import load_dotenv 

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")

if API_KEY is None: 
    raise ValueError("API key not found. Please  set OPENWEATHER_API_KEY in you .env file. ")

def get_weather_forecast(city_name): 
    """
    Fetch 5-day weather forecast data (3-hour intervals) for a given city using OpenWeattherMap API. 

    Args:
        city_name (str): Name of the city to fetch the weather forecast for.
        
        Returns: 
            list: A list of dicts containing forecast datetime, temperature in Celsius, and weather description.
              Returns an empty list if data is not found or on error.
    """
    
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={API_KEY}&units=metric"
    response = requests.get(url)

    if response.status_code != 200: 
        print(f"Error fetching weather data: {response.status_code} - {response.text}")
        return []
        
        
    data = response.json()

    if "list" not in data: 
        print("No weather data found for the specify city. ")
        return []
        
    weather_forecast = []

    for forecast in data["list"][:8]:
        weather_forecast.append({
            "datatime": forecast["dt_txt"], 
            "temperature": forecast["main"]["temp"], 
            "description": forecast["weather"][0]["description"]
        })
        
    return weather_forecast




            
            