"""
Domain Interpretation and Transit Policy Module
Maps mathematical cluster centroids to operational transit archetypes
and generates actionable transit planning recommendations.
"""

from typing import Dict, List, Tuple
import numpy as np
import pandas as pd


class TransitClusterInterpreter:
    """
    Interprets unsupervised cluster centroids and creates transit policy archetypes.
    """

    @staticmethod
    def profile_clusters(
        route_df: pd.DataFrame,
        feature_cols: List[str],
        cluster_col: str = "cluster"
    ) -> Tuple[pd.DataFrame, Dict]:
        """
        Calculates mean, median, min, max for each feature per cluster
        and assigns descriptive urban archetype names.
        """
        cluster_profiles = {}
        grouped = route_df.groupby(cluster_col)

        profile_table = grouped[feature_cols].mean().round(3)
        route_counts = grouped.size().to_dict()

        # Rank clusters by mean speed descending to uniquely map the 4 operational archetypes
        sorted_by_speed = profile_table.sort_values(by="mean_speed_kmh", ascending=False).index.tolist()
        
        archetype_blueprints = [
            {
                "name": "Radial Express Arterial (High Speed & Smooth Flow)",
                "color": "#10B981",  # Emerald Green
                "severity": "Low Friction",
                "recommendation": (
                    "High-speed commuter corridor. Ideal candidate for Electric Bus (EV) fleet allocation "
                    "due to consistent speeds and minimal stop-and-go energy loss. Maintain express timetable."
                )
            },
            {
                "name": "Suburban Feeder / Metro Link (Predictable Steady Flow)",
                "color": "#3B82F6",  # Royal Blue
                "severity": "Moderate Friction",
                "recommendation": (
                    "Reliable feeder route. Synchronize dispatch headways with adjacent Metro rail arrival times "
                    "and optimize timetable spacing to eliminate bus bunching."
                )
            },
            {
                "name": "Congested Urban Core (Heavy Impedance Chokepoint)",
                "color": "#EF4444",  # Coral Red
                "severity": "Critical Friction",
                "recommendation": (
                    "Severe bottleneck corridor. Implement Transit Signal Priority (TSP) at key junctions, "
                    "demarcate dedicated bus lanes, and pilot off-board fare ticketing to slash boarding dwell."
                )
            },
            {
                "name": "High-Friction Historic / Commercial Belt (Stop-and-Go)",
                "color": "#F59E0B",  # Amber Orange
                "severity": "High Turbulence",
                "recommendation": (
                    "Extreme stop-and-go turbulence. Enforce curbside parking restrictions, consolidate closely "
                    "spaced bus stops, and evaluate mini-bus fleet rightsizing."
                )
            }
        ]

        for rank, c_id in enumerate(sorted_by_speed):
            row = profile_table.loc[c_id]
            blueprint = archetype_blueprints[min(rank, len(archetype_blueprints) - 1)]

            speed = row.get("mean_speed_kmh", 0)
            congestion = row.get("mean_congestion_index", 0)
            dwell = row.get("mean_dwell_ratio", 0)
            headway_irreg = row.get("mean_headway_irregularity", 0)
            accel_noise = row.get("mean_accel_noise", 0)
            delay = row.get("mean_delay_min", 0)

            archetype_name = blueprint["name"]
            color = blueprint["color"]
            severity = blueprint["severity"]
            recommendation = blueprint["recommendation"]

            # Normalized radar metric (scale 0-1 across feature domain)
            radar_profile = {
                "Speed": round(min(1.0, max(0.1, speed / 32.0)), 2),
                "Congestion": round(min(1.0, max(0.1, (congestion - 1.0) / 1.2)), 2),
                "Stop Dwell": round(min(1.0, max(0.1, dwell / 0.45)), 2),
                "Headway Variance": round(min(1.0, max(0.1, headway_irreg / 0.6)), 2),
                "Accel Turbulence": round(min(1.0, max(0.1, accel_noise / 2.0)), 2),
                "Schedule Delay": round(min(1.0, max(0.1, max(0, delay) / 18.0)), 2)
            }

            cluster_profiles[int(c_id)] = {
                "cluster_id": int(c_id),
                "archetype_name": archetype_name,
                "color": color,
                "severity_level": severity,
                "route_count": int(route_counts.get(c_id, 0)),
                "route_percentage": round(route_counts.get(c_id, 0) / len(route_df) * 100, 1),
                "centroid_metrics": row.to_dict(),
                "radar_metrics": radar_profile,
                "policy_recommendation": recommendation,
                "routes_assigned": route_df[route_df[cluster_col] == c_id]["route_id"].tolist()
            }

        return profile_table, cluster_profiles
