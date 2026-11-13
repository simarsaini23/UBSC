"""
Data Generator for Urban Transit Operational Telemetry
Simulates high-fidelity multi-route, multi-temporal urban bus observations
modeled after real-world metropolitan public transit networks.
"""

import math
import random
from typing import Dict, List, Tuple

# We implement a pure standard-library fallback if numpy isn't loaded yet,
# but dynamically import if available.


def generate_synthetic_transit_dataset(
    num_routes: int = 60,
    seed: int = 42
) -> Tuple[List[Dict], List[Dict]]:
    """
    Generates:
    1. Operational route-time observations (raw dataset with some missing values)
    2. Route spatial geometry metadata (coordinates for GIS/Leaflet mapping)
    """
    random.seed(seed)
    
    # Archetype corridor templates representing urban transit corridors
    archetypes = [
        {
            "corridor": "CBD_Core_Trunk",
            "speed_base": 11.5,
            "speed_jitter": 1.8,
            "dwell_ratio_base": 0.36,
            "accel_noise_base": 1.35,
            "congestion_base": 1.88,
            "headway_cv": 0.45,
            "stop_density": 2.8,  # stops per km
            "desc": "Heavy urban core, frequent signalized intersections, high passenger boarding"
        },
        {
            "corridor": "Radial_Express_Arterial",
            "speed_base": 29.5,
            "speed_jitter": 3.0,
            "dwell_ratio_base": 0.14,
            "accel_noise_base": 0.55,
            "congestion_base": 1.25,
            "headway_cv": 0.18,
            "stop_density": 1.0,
            "desc": "Wide divided highway / radial expressway connecting suburbs to business hubs"
        },
        {
            "corridor": "Suburban_Feeder_Loop",
            "speed_base": 21.0,
            "speed_jitter": 2.2,
            "dwell_ratio_base": 0.22,
            "accel_noise_base": 0.80,
            "congestion_base": 1.16,
            "headway_cv": 0.14,
            "stop_density": 1.5,
            "desc": "Last-mile feeder linking residential sectors to metro/rail stations"
        },
        {
            "corridor": "High_Friction_Historic_Belt",
            "speed_base": 8.0,
            "speed_jitter": 1.4,
            "dwell_ratio_base": 0.46,
            "accel_noise_base": 1.85,
            "congestion_base": 2.15,
            "headway_cv": 0.58,
            "stop_density": 3.4,
            "desc": "Narrow historic streets, heavy mixed pedestrian-rickshaw traffic, stop-and-go"
        }
    ]

    time_windows = [
        {"name": "AM_PEAK", "speed_mult": 0.72, "cong_mult": 1.55, "headway_mult": 1.40, "dwell_mult": 1.35, "weight": 0.30},
        {"name": "MIDDAY_OFFPEAK", "speed_mult": 1.05, "cong_mult": 1.02, "headway_mult": 0.95, "dwell_mult": 0.90, "weight": 0.25},
        {"name": "PM_PEAK", "speed_mult": 0.68, "cong_mult": 1.68, "headway_mult": 1.50, "dwell_mult": 1.45, "weight": 0.30},
        {"name": "NIGHT", "speed_mult": 1.35, "cong_mult": 0.85, "headway_mult": 0.80, "dwell_mult": 0.75, "weight": 0.15}
    ]

    # City center anchor (e.g. New Delhi / Connaught Place: 28.6315° N, 77.2167° E)
    center_lat, center_lon = 28.6315, 77.2167

    routes_meta = []
    observations = []

    for r_idx in range(1, num_routes + 1):
        arch = archetypes[(r_idx - 1) % len(archetypes)]
        route_id = f"R-{r_idx:03d}"
        route_name = f"Route {r_idx} ({arch['corridor']})"
        
        # Route geometry parameters
        angle = (r_idx / num_routes) * 2 * math.pi
        length_km = round(random.uniform(10.5, 34.0), 2)
        stops_count = max(8, int(length_km * arch["stop_density"] * random.uniform(0.85, 1.15)))
        
        # Generate route coordinate polyline
        num_waypoints = 6
        waypoints = []
        start_r = random.uniform(1.0, 4.0)
        end_r = start_r + length_km * 0.08  # rough km to degrees conversion scale
        for wp in range(num_waypoints):
            t = wp / (num_waypoints - 1)
            cur_r = start_r + t * (end_r - start_r)
            cur_ang = angle + math.sin(t * math.pi) * 0.4
            lat = center_lat + cur_r * 0.015 * math.cos(cur_ang)
            lon = center_lon + cur_r * 0.015 * math.sin(cur_ang)
            waypoints.append([round(lat, 5), round(lon, 5)])

        routes_meta.append({
            "route_id": route_id,
            "route_name": route_name,
            "corridor_type": arch["corridor"],
            "description": arch["desc"],
            "length_km": length_km,
            "stops_count": stops_count,
            "waypoints": waypoints
        })

        # Scheduled baseline parameters
        scheduled_base_speed = arch["speed_base"] * 1.25
        scheduled_trip_time_min = (length_km / scheduled_base_speed) * 60.0
        scheduled_headway_min = random.choice([10, 12, 15, 20])

        # Generate observations across days & time windows
        # 20 observations per route across time windows
        for obs_i in range(20):
            tw = random.choices(time_windows, weights=[tw["weight"] for tw in time_windows])[0]
            direction = random.choice(["Inbound", "Outbound"])
            
            # Directional asymmetry: Inbound is worse in AM, Outbound is worse in PM
            asym_factor = 1.0
            if tw["name"] == "AM_PEAK" and direction == "Inbound":
                asym_factor = 1.25
            elif tw["name"] == "PM_PEAK" and direction == "Outbound":
                asym_factor = 1.30
            elif tw["name"] == "AM_PEAK" and direction == "Outbound":
                asym_factor = 0.88
            elif tw["name"] == "PM_PEAK" and direction == "Inbound":
                asym_factor = 0.85

            eff_speed = max(4.0, (arch["speed_base"] * tw["speed_mult"] / asym_factor) + random.gauss(0, arch["speed_jitter"]))
            actual_trip_time = (length_km / eff_speed) * 60.0
            speed_std = max(1.2, eff_speed * random.uniform(0.18, 0.45) * tw["cong_mult"])
            
            # Dwell time
            dwell_ratio = min(0.65, max(0.08, arch["dwell_ratio_base"] * tw["dwell_mult"] * random.uniform(0.85, 1.25)))
            dwell_time_min = actual_trip_time * dwell_ratio
            
            # Congestion index = Actual Travel Time / Free Flow Scheduled Time
            congestion_index = round(actual_trip_time / max(1.0, scheduled_trip_time_min), 3)
            
            # Headway jitter
            actual_headway = max(3.0, scheduled_headway_min * tw["headway_mult"] + random.gauss(0, scheduled_headway_min * arch["headway_cv"]))
            headway_variance = round((actual_headway - scheduled_headway_min) ** 2, 2)
            
            # Acceleration shocks / stop-and-go noise
            accel_noise = max(0.2, arch["accel_noise_base"] * (1.0 + (congestion_index - 1.0) * 0.4) + random.gauss(0, 0.15))
            
            # Schedule adherence delay
            schedule_delay = max(-5.0, actual_trip_time - scheduled_trip_time_min + random.gauss(2.0, 3.0))

            obs_record = {
                "observation_id": f"OBS-{r_idx:03d}-{obs_i:03d}",
                "route_id": route_id,
                "route_name": route_name,
                "corridor_archetype": arch["corridor"],
                "time_window": tw["name"],
                "direction": direction,
                "route_length_km": length_km,
                "stop_count": stops_count,
                "stop_density_per_km": round(stops_count / length_km, 2),
                "scheduled_trip_time_min": round(scheduled_trip_time_min, 1),
                "actual_trip_time_min": round(actual_trip_time, 1),
                "avg_operational_speed_kmh": round(eff_speed, 2),
                "speed_variability_kmh": round(speed_std, 2),
                "congestion_index": congestion_index,
                "stop_dwell_time_min": round(dwell_time_min, 1),
                "stop_dwell_time_ratio": round(dwell_ratio, 3),
                "scheduled_headway_min": scheduled_headway_min,
                "actual_headway_min": round(actual_headway, 1),
                "headway_variance_min2": headway_variance,
                "acceleration_noise_mps2": round(accel_noise, 3),
                "schedule_adherence_delay_min": round(schedule_delay, 1),
                "passenger_load_factor": round(min(1.0, max(0.15, random.uniform(0.3, 0.95) * tw["dwell_mult"])), 2)
            }

            # Inject realistic missing values (sensor dropout) in ~3.5% of rows for dwell time or speed variability
            if random.random() < 0.035:
                obs_record["stop_dwell_time_min"] = None
                obs_record["stop_dwell_time_ratio"] = None
            if random.random() < 0.025:
                obs_record["speed_variability_kmh"] = None
            if random.random() < 0.020:
                obs_record["acceleration_noise_mps2"] = None

            observations.append(obs_record)

    return observations, routes_meta
