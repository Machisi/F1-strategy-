import pandas as pd
import os
import numpy as np

def load_historical_data():
    """
    Carga los datasets históricos de races y pit stops.
    Devuelve:
        - races_df: información de las carreras
        - pitstops_df: información de las paradas
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    data_dir = os.path.join(base_dir, "f1_strategy_predictor", "data", "historical_information")

    races_path = os.path.join(data_dir, "races.csv")
    pitstops_path = os.path.join(data_dir, "pit_stops.csv")

    races_df = pd.read_csv(races_path)
    pitstops_df = pd.read_csv(pitstops_path)

    # Convertir a tipos numéricos donde haga falta
    pitstops_df['lap'] = pd.to_numeric(pitstops_df['lap'], errors='coerce')
    pitstops_df['stop'] = pd.to_numeric(pitstops_df['stop'], errors='coerce')
    pitstops_df = pitstops_df.dropna(subset=['lap', 'stop'])

    return races_df, pitstops_df


def generate_strategies(next_race, weather, races_df, pitstops_df, top_n=3):
    """
    Genera estrategias optimizadas basadas en histórico y clima.
    Params:
        - next_race: diccionario con info de la próxima carrera ('raceId', 'circuitId', 'city', etc.)
        - weather: diccionario con 'temperature' y 'rain' (boolean)
        - races_df, pitstops_df: datasets históricos
        - top_n: número de estrategias a devolver
    Returns:
        - lista de estrategias
    """
    strategies = []

    # Filtrar histórico por circuito
        # Buscar circuitId en races.csv a partir del nombre de la carrera
    race_row = races_df[races_df['name'].str.contains(next_race['race'], case=False, na=False)]

    if not race_row.empty:
        circuit_id = race_row.iloc[0]['circuitId']
        race_history = races_df[races_df['circuitId'] == circuit_id]
    else:
        print(f"No historical race found for {next_race['race']}. Returning default strategies.")
        default_laps = [15, 30, 45]
        for start in ['soft', 'medium', 'hard']:
            strategies.append({
                'start': start,
                'lap1': default_laps[0],
                'tyre2': 'medium',
                'lap2': default_laps[1],
                'tyre3': 'hard'
            })
        return strategies

    if race_history.empty:
        # Si no hay histórico, generar estrategias estándar
        default_laps = [15, 30, 45]
        for start in ['soft', 'medium', 'hard']:
            strategies.append({
                'start': start,
                'lap1': default_laps[0],
                'tyre2': 'medium',
                'lap2': default_laps[1],
                'tyre3': 'hard'
            })
        return strategies

    # Unir pitstops con las carreras del circuito
    merged = pitstops_df.merge(
    race_history[['raceId', 'year']], 
    left_on='thisraceId', 
    right_on='raceId'
)

    # Analizar clima: temperatura y lluvia
    avg_temp = weather.get('temperature', 25)
    rain = weather.get('rain', False)

    # Filtrar estrategias según condiciones similares
    if rain:
        tyre_options = ['intermediate', 'wet']
    elif avg_temp > 28:
        tyre_options = ['medium', 'hard']  # soft se degrada rápido
    else:
        tyre_options = ['soft', 'medium', 'hard']

    # Seleccionar paradas históricas de pilotos en condiciones similares
    candidate_stops = []
    for _, row in merged.iterrows():
        candidate_stops.append({
            'start': np.random.choice(tyre_options),
            'lap1': int(row['lap']),
            'tyre2': np.random.choice(tyre_options),
            'lap2': int(row['lap']) + 10,  # estimación simple
            'tyre3': np.random.choice(tyre_options)
        })

    # Elegir top N estrategias
    if len(candidate_stops) >= top_n:
        strategies = np.random.choice(candidate_stops, top_n, replace=False).tolist()
    else:
        strategies = candidate_stops

    return strategies


