import datetime
import requests
from f1_strategy_predictor.weather.race_calendar import f1_calendar
from .race_calendar import f1_calendar


API_KEY = "0a9724b3f1f96f3f6823d29554a0804b"


def get_next_race(calendar): 
    today = datetime.datetime.now().date()
    for race in calendar:
        race_date = datetime.datetime.strptime(race["date"], "%Y-%m-%d").date()
        if race_date >= today: 
            return race
    return None

def get_weather_forecast(lat, long, api_key): 
    url = (
        f"https://api.openweathermap.org/data/2.5/forecast?"
        f"lat={lat}&lon={long}&appid={api_key}&units=metric&lang=es"
    )
    response = requests.get(url)
    data = response.json()
        
    weather_list = []
    
    if "list" in data: 
        for forecast in data["list"][:8]: 
            entry = {
                "datetime": forecast['dt_txt'],
                "temperature": forecast['main']['temp'], 
                "description": forecast['weather'][0]['description']
            }
            weather_list.append(entry)
        return weather_list 
    else: 
        print("No weather data found for the specified city")
        return []

def recommend_tyres(weather_data): 
    rain_keyword = ["rain", "shower", "drizzle"]
    rain_detected = any(any(word in entry["description"].lower() for word in rain_keyword ) for entry in weather_data)
    
    if rain_detected: 
        return "Recommended tyres: Wet tyres" 
    else: 
        return "Recommended tyres: Dry tyres" 

if __name__ == "__main__": 
    next_race = get_next_race(f1_calendar)
    
    if next_race: 
        print(f"\nNext Grand Prix: {next_race['race']} in {next_race['city']} on {next_race['date']}")
        weather = get_weather_forecast(next_race["city"], API_KEY)
        if weather: 
            for entry in weather:
                print(f"{entry['datetime']}: {entry['temperature']}ºC, {entry['description']}")
            recommendation = recommend_tyres(weather)
            print(f"\nRecommended tyres: {recommendation}")
        else: 
            print("Weather data unavailable.")
    else: 
        print("No upcoming races found in the calendar.")
