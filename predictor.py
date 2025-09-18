import sys
import os
import matplotlib.pyplot as plt
from f1_strategy_predictor.weather.f1_next_race_weather import get_next_race, get_weather_forecast, recommend_tyres, f1_calendar, API_KEY
from f1_strategy_predictor.models.strategy_model import load_historical_data, generate_strategies

if __name__ == "__main__":
    print("Loading historical data...")
    races_df, pitstops_df = load_historical_data()
    print("Historical data loaded successfully!")

    # Obtener próxima carrera
    next_race = get_next_race(f1_calendar)
    if not next_race:
        print("No upcoming races found in the calendar.")
        exit()

    print(f"\nNext Grand Prix: {next_race['race']} in {next_race['city']} ({next_race['date']})")

    # Obtener clima para la ciudad de la carrera
    weather = get_weather_forecast(next_race["lat"], next_race["long"], API_KEY)

    if weather:
        avg_temp = sum([entry['temperature'] for entry in weather])/len(weather)
        rain = any('rain' in entry['description'].lower() for entry in weather)
        print(f"\nWeather analysis: Avg temp = {avg_temp:.1f} ºC, Rain = {rain}")

        for entry in weather:
            print(f"{entry['datetime']}: {entry['temperature']} ºC - {entry['description']}")

        recommendation = recommend_tyres(weather)
        print(f"\nRecommended tyres: {recommendation}")
    else:
        avg_temp = 25
        rain = False
        print("Weather data unavailable.")

    # Generar estrategias basadas en histórico
    strategies = generate_strategies(next_race, {'temperature': avg_temp, 'rain': rain}, races_df, pitstops_df, top_n=3)

    print("\nRecommended strategies for the next race:\n")
    for i, strat in enumerate(strategies, 1):
        print(f"Strategy {i}:")
        print(f"  Start tyre: {strat['start'].capitalize()}")
        print(f"  Change lap {strat['lap1']} -> {strat['tyre2'].capitalize()}")
        print(f"  Change lap {strat['lap2']} -> {strat['tyre3'].capitalize()}\n")

    # Gráfico de temperatura
    if weather:
        temps = [entry['temperature'] for entry in weather]
        times = [entry['datetime'][-8:-3] for entry in weather]  # hora
        plt.figure(figsize=(10, 5))
        plt.plot(times, temps, marker='o')
        plt.title(f"Temperature forecast - {next_race['city']}")
        plt.xlabel("Time")
        plt.ylabel("Temperature (ºC)")
        plt.grid(True)
        plt.tight_layout()
        plt.show()
