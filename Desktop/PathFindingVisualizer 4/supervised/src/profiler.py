import numpy as np
import pandas as pd

def generate_cluster_profiles(X_imputed_df, labels, metadata_df):
    """
    Implements Objective 3 & Outcome Interpretation:
    Analyzes cluster centroids in original feature space, identifies dominant operational traits,
    assigns archetype titles, and suggests operational recommendations for transit planning.
    """
    df = X_imputed_df.copy()
    df["cluster"] = labels
    
    unique_clusters = sorted(df["cluster"].unique())
    fleet_means = df.drop(columns=["cluster"]).mean()
    
    profiles = []
    
    for c in unique_clusters:
        c_df = df[df["cluster"] == c].drop(columns=["cluster"])
        c_size = len(c_df)
        c_percent = round((c_size / len(df)) * 100, 1)
        
        c_means = c_df.mean()
        
        # Calculate feature ratios relative to fleet mean
        ratios = c_means / (fleet_means + 1e-6)
        
        avg_speed = float(c_means.get("avg_speed_kmh", 0))
        congestion = float(c_means.get("peak_congestion_index", 0))
        delay = float(c_means.get("schedule_delay_index", 0))
        dwell = float(c_means.get("dwell_time_per_stop_sec", 0))
        reliability = float(c_means.get("reliability_score", 0))
        stop_density = float(c_means.get("stop_density_per_km", 0))
        
        # Rule-based Operational Archetype Assignment
        if avg_speed < 18 and congestion > 0.7:
            title = "Downtown Congested Arterial"
            badge_color = "#ef4444" # Red
            desc = "Low operational speeds (<18 km/h), high peak congestion, and frequent stop dwell delays. Typical of CBD corridors."
            recommendation = "Recommend dedicated Bus Rapid Transit (BRT) lanes, transit signal priority at intersections, and stop consolidation."
        elif avg_speed > 35 and congestion < 0.35:
            title = "High-Speed Express Corridor"
            badge_color = "#10b981" # Green
            desc = "High average speeds (>35 km/h), low stop density, and high service reliability. Connects suburban hubs to core."
            recommendation = "Maintain current frequency; explore express schedule optimization and long-distance articulated buses."
        elif delay > 0.65 or dwell > 45:
            title = "High-Delay Bottleneck Corridor"
            badge_color = "#f59e0b" # Amber
            desc = "Severe dwell delays per stop and schedule variance. High passenger turnover bottlenecks at key transit hubs."
            recommendation = "Deploy off-board ticketing systems, multi-door boarding, and targeted station infrastructure upgrades."
        elif stop_density > 3.5:
            title = "Dense Urban Feeder Network"
            badge_color = "#3b82f6" # Blue
            desc = "High stop density (>3.5 stops/km) with frequent passenger boarding and moderate traffic speeds."
            recommendation = "Optimize stop spacing (target 300-400m intervals) and introduce micro-transit feeders."
        else:
            title = "Standard Suburban Transit Corridor"
            badge_color = "#8b5cf6" # Purple
            desc = "Balanced operational performance with moderate speeds, reliable schedule adherence, and steady demand."
            recommendation = "Adjust vehicle deployment during peak hours and monitor headways."

        # Get route IDs in this cluster
        cluster_routes = metadata_df[df["cluster"] == c]["route_id"].tolist()
        
        feature_breakdown = {k: round(float(v), 2) for k, v in c_means.items()}
        fleet_comparison = {k: round(float(ratios[k]), 2) for k in c_means.keys()}
        
        profiles.append({
            "cluster_id": int(c),
            "title": title,
            "badge_color": badge_color,
            "route_count": c_size,
            "percentage": c_percent,
            "description": desc,
            "recommendation": recommendation,
            "features": feature_breakdown,
            "fleet_ratios": fleet_comparison,
            "sample_routes": cluster_routes[:5]
        })
        
    return profiles
