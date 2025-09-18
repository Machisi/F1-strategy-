import os
import pandas as pd
import random


def load_historical_data(base_dir):
    """
    Carga los datasets históricos: carreras y paradas.
    """
    races = pd.read_csv(os.path.join(base_dir, "historical_information", "races.csv"))
    pitstops = pd.read_csv(os.path.join(base_dir, "historical_information", "pit_stops.csv"))
    return races, pitstops


def find_similar_races(races, next_race, avg_temp, rain):
    """
    Busca carreras históricas en el mismo circuito.
    En el futuro se puede mejorar comparando con clima histórico.
    """
    circuit_races = races[races["circuitId"] == next_race["circuitId"]]
    return circuit_races


def extract_strategies(pitstops, race_ids):
    """
    Extrae estrategias reales de pilotos en las carreras históricas seleccionadas.
    """
    strategies = []

    for race_id in race_ids:
        race_pits = pitstops[pitstops["raceId"] == race_id]

        if race_pits.empty:
            continue

        # Agrupar por piloto
        for driver_id, group in race_pits.groupby("driverId"):
            stops = group.sort_values("stop")
            strat = {
                "driver": driver_id,
                "laps": list(stops["lap"].values),
                "n_stops": stops["stop"].max()
            }
            strategies.append(strat)

    return strategies


def generate_strategies(weather, next_race, races, pitstops):
    """
    Genera estrategias basadas en condiciones meteorológicas + histórico de pitstops.
    """
    avg_temp = sum([w["temperature"] for w in weather]) / len(weather)
    rain = any("rain" in w["description"].lower() for w in weather)

    # Buscar carreras históricas similares
    similar_races = find_similar_races(races, next_race, avg_temp, rain)
    race_ids = similar_races["raceId"].tolist()

    # Extraer estrategias reales
    hist_strategies = extract_strategies(pitstops, race_ids)

    final_strategies = []
    for i in range(min(3, len(hist_strategies))):  # elegir 3
        strat = hist_strategies[i]

        # Selección de neumático inicial según clima
        if rain:
            start_tyre = random.choice(["intermediate", "wet"])
        elif avg_temp > 28:
            start_tyre = random.choice(["medium", "hard"])
        else:
            start_tyre = random.choice(["soft", "medium", "hard"])

        final_strategies.append({
            "start": start_tyre,
            "lap1": strat["laps"][0] if len(strat["laps"]) > 0 else 20,
            "tyre2": random.choice(["soft", "medium", "hard"]),
            "lap2": strat["laps"][1] if len(strat["laps"]) > 1 else 40,
            "tyre3": random.choice(["soft", "medium", "hard"]),
            "source_driver": strat["driver"]
        })

    return final_strategies
