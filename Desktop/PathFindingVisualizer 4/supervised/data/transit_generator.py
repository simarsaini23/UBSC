import numpy as np
import pandas as pd
import json
import random
import os

def generate_urban_transit_dataset(n_routes=160, seed=42):
    """
    Generates a realistic urban bus route transit dataset with operational & temporal features.
    Simulates distinct operational patterns:
    1. Downtown Congested Arterials (Low speed, high stop density, high dwell time, high congestion)
    2. High-Speed Express Corridors (High speed, low stop density, low dwell time, high reliability)
    3. Suburban Feeder Routes (Moderate speed, medium stop density, variable delays)
    4. Peak-Hour Bottleneck Routes (Extreme speed variance, high schedule delay, high congestion)
    5. Night & Off-Peak Feeder Routes (Consistent speed, low passenger turnover, high schedule adherence)
    """
    np.random.seed(seed)
    random.seed(seed)

    archetypes = [
        {"name": "Downtown Congested Arterial", "weight": 0.30, 
         "speed": (12, 4), "speed_var": (6, 2), "congestion": (0.82, 0.1), "stop_density": (4.5, 0.8), "dwell": (45, 10), "delay": (0.75, 0.12), "turnover": (0.85, 0.1), "reliability": (0.45, 0.1)},
        {"name": "High-Speed Express Corridor", "weight": 0.25, 
         "speed": (48, 6), "speed_var": (3, 1), "congestion": (0.25, 0.08), "stop_density": (1.2, 0.3), "dwell": (18, 4), "delay": (0.18, 0.05), "turnover": (0.35, 0.08), "reliability": (0.90, 0.05)},
        {"name": "Suburban Feeder Line", "weight": 0.20, 
         "speed": (30, 5), "speed_var": (4, 1.5), "congestion": (0.40, 0.1), "stop_density": (2.2, 0.5), "dwell": (25, 6), "delay": (0.32, 0.08), "turnover": (0.50, 0.1), "reliability": (0.75, 0.08)},
        {"name": "Peak-Hour Bottleneck Route", "weight": 0.15, 
         "speed": (18, 5), "speed_var": (12, 3), "congestion": (0.92, 0.05), "stop_density": (3.2, 0.6), "dwell": (55, 12), "delay": (0.88, 0.08), "turnover": (0.70, 0.12), "reliability": (0.32, 0.08)},
        {"name": "Low-Frequency Peripheral Connector", "weight": 0.10, 
         "speed": (38, 4), "speed_var": (2.5, 0.8), "congestion": (0.20, 0.06), "stop_density": (1.5, 0.4), "dwell": (20, 5), "delay": (0.22, 0.06), "turnover": (0.25, 0.06), "reliability": (0.82, 0.06)}
    ]

    records = []
    
    # Generate spatial GeoJSON routes near major urban grid (e.g. Delhi / Bangalore / Mumbai grid centered near 28.6139, 77.2090)
    base_lat, base_lon = 28.6139, 77.2090

    time_windows = ["AM_PEAK", "MIDDAY", "PM_PEAK", "NIGHT"]

    route_counter = 101
    geo_routes = []

    for i in range(n_routes):
        # Pick archetype based on weights
        arch = np.random.choice(archetypes, p=[a["weight"] for a in archetypes])
        
        route_num = route_counter + (i // len(time_windows))
        time_slot = time_windows[i % len(time_windows)]
        route_id = f"R-{route_num}_{time_slot}"
        
        # Base Route Name
        route_name = f"Route {route_num} ({time_slot.replace('_', ' ')})"
        
        # Sample features from Gaussian distributions with bounds clipping
        length_km = round(float(np.clip(np.random.normal(14, 5), 4, 38)), 2)
        avg_speed = round(float(np.clip(np.random.normal(arch["speed"][0], arch["speed"][1]), 5, 75)), 2)
        speed_var = round(float(np.clip(np.random.normal(arch["speed_var"][0], arch["speed_var"][1]), 0.5, 20)), 2)
        congestion = round(float(np.clip(np.random.normal(arch["congestion"][0], arch["congestion"][1]), 0.05, 0.99)), 3)
        stop_density = round(float(np.clip(np.random.normal(arch["stop_density"][0], arch["stop_density"][1]), 0.5, 8.0)), 2)
        dwell_time = round(float(np.clip(np.random.normal(arch["dwell"][0], arch["dwell"][1]), 10, 90)), 1)
        delay_index = round(float(np.clip(np.random.normal(arch["delay"][0], arch["delay"][1]), 0.02, 0.98)), 3)
        turnover = round(float(np.clip(np.random.normal(arch["turnover"][0], arch["turnover"][1]), 0.05, 0.98)), 3)
        reliability = round(float(np.clip(np.random.normal(arch["reliability"][0], arch["reliability"][1]), 0.1, 0.99)), 3)

        # Introduce missing values for ~4% of entries to demonstrate Objective 1 missing value imputation
        if random.random() < 0.04:
            dwell_time = np.nan
        if random.random() < 0.03:
            speed_var = np.nan

        records.append({
            "route_id": route_id,
            "route_name": route_name,
            "time_window": time_slot,
            "ground_truth_archetype": arch["name"], # For internal benchmark analysis
            "length_km": length_km,
            "avg_speed_kmh": avg_speed,
            "speed_variance": speed_var,
            "peak_congestion_index": congestion,
            "stop_density_per_km": stop_density,
            "dwell_time_per_stop_sec": dwell_time,
            "schedule_delay_index": delay_index,
            "passenger_turnover_rate": turnover,
            "reliability_score": reliability
        })

        # Generate map trajectory coordinates for GeoJSON
        start_lat = base_lat + np.random.uniform(-0.12, 0.12)
        start_lon = base_lon + np.random.uniform(-0.12, 0.12)
        waypoints = [[start_lon, start_lat]]
        
        cur_lat, cur_lon = start_lat, start_lon
        num_stops = max(3, int(length_km * stop_density / 3))
        for _ in range(num_stops):
            cur_lat += np.random.uniform(-0.02, 0.02)
            cur_lon += np.random.uniform(-0.02, 0.02)
            waypoints.append([round(cur_lon, 5), round(cur_lat, 5)])
            
        geo_routes.append({
            "route_id": route_id,
            "route_name": route_name,
            "archetype": arch["name"],
            "coordinates": waypoints
        })

    df = pd.DataFrame(records)
    return df, geo_routes

if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    df, geo = generate_urban_transit_dataset(160)
    df.to_csv("data/urban_bus_transit_observations.csv", index=False)
    with open("data/route_shapes.json", "w") as f:
        json.dump(geo, f, indent=2)
    print(f"Generated transit dataset: {df.shape[0]} rows, saved to data/urban_bus_transit_observations.csv")
