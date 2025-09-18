import pandas as pd
import ergast_py

def fetch_all_pitstops(start_season=1950, end_season=2025):
    e = ergast_py.Ergast()
    records = []
    
    for season in range(start_season, end_season + 1): 
        races = e.season(season).get_races()
        for race in races: 
            round.num = race.round
            circuit = race.circuit.circuitName
            location = race.circuit.location.locality
            date = race.date 
            
        pitstops = e.season(season).round(race.round).get_pit_stops()
        for ps in pitstops:
            records.append({
                "year": season,
                "round": race.round,
                "circuit": circuit,
                "race": race.raceName,
                "location": location,
                "date": date,
                "driver_id": ps.driver.driverId,
                "stop": ps.stop,
                "lap": ps.lap,
                "duration": ps.duration,
            })
        return pd.DataFrame(records)

if __name__ == "__main__": 
    df = fetch_all_pitstops(2000, 2025)
    df.to_csv("race_pitstops.csv", index=False)
    print("The data has been saved in race_pitstops.csv, total number of pit stops:", len(df))
        
        