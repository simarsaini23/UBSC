"""
Feature Engineering Module for Urban Transit Analysis
Constructs temporal, operational, and movement features from transit telemetry.
"""

from typing import Dict, List, Tuple
import numpy as np
import pandas as pd


class TransitFeatureEngineer:
    """
    Constructs multi-dimensional temporal and movement transit indicators
    at both route-level and route-time segment levels.
    """

    @staticmethod
    def construct_segment_features(df: pd.DataFrame) -> Tuple[pd.DataFrame, List[str]]:
        """
        Constructs operational and movement features for each route-time segment.
        """
        data = df.copy()

        # 1. Speed Variability Coefficient of Variation (CV = std / mean)
        data["speed_cv"] = (
            data["speed_variability_kmh"] / data["avg_operational_speed_kmh"].clip(lower=1.0)
        ).round(3)

        # 2. Stop Dwell Time Ratio (dwell time / actual trip time)
        if "stop_dwell_time_ratio" not in data.columns or data["stop_dwell_time_ratio"].isnull().all():
            data["stop_dwell_time_ratio"] = (
                data["stop_dwell_time_min"] / data["actual_trip_time_min"].clip(lower=1.0)
            ).clip(0.05, 0.75).round(3)

        # 3. Headway Regularity Index (headway deviation ratio)
        data["headway_irregularity"] = (
            np.sqrt(data["headway_variance_min2"].clip(lower=0)) / data["scheduled_headway_min"].clip(lower=1.0)
        ).round(3)

        # 4. Movement Turbulence Factor (combination of accel noise and speed CV)
        data["movement_turbulence"] = (
            data["acceleration_noise_mps2"] * (1.0 + data["speed_cv"])
        ).round(3)

        # 5. Peak Hour Binary Indicator
        data["is_peak_hour"] = data["time_window"].isin(["AM_PEAK", "PM_PEAK"]).astype(int)

        feature_cols = [
            "avg_operational_speed_kmh",
            "speed_cv",
            "congestion_index",
            "stop_dwell_time_ratio",
            "headway_irregularity",
            "acceleration_noise_mps2",
            "movement_turbulence",
            "schedule_adherence_delay_min"
        ]

        return data, feature_cols

    @staticmethod
    def aggregate_to_route_level(segment_df: pd.DataFrame) -> Tuple[pd.DataFrame, List[str]]:
        """
        Aggregates operational observations across days and time windows
        to build a robust route-level profile including peak-to-offpeak ratios
        and directional asymmetry.
        """
        grouped = segment_df.groupby("route_id")

        route_summary = grouped.agg(
            route_name=("route_name", "first"),
            corridor_archetype=("corridor_archetype", "first"),
            route_length_km=("route_length_km", "first"),
            stop_count=("stop_count", "first"),
            stop_density_per_km=("stop_density_per_km", "first"),
            mean_speed_kmh=("avg_operational_speed_kmh", "mean"),
            speed_cv=("speed_cv", "mean"),
            mean_congestion_index=("congestion_index", "mean"),
            max_congestion_index=("congestion_index", "max"),
            mean_dwell_ratio=("stop_dwell_time_ratio", "mean"),
            mean_headway_irregularity=("headway_irregularity", "mean"),
            mean_accel_noise=("acceleration_noise_mps2", "mean"),
            mean_turbulence=("movement_turbulence", "mean"),
            mean_delay_min=("schedule_adherence_delay_min", "mean")
        ).reset_index()

        # Calculate Peak Vulnerability Index (Off-Peak Speed / Peak Speed)
        peak_speeds = segment_df[segment_df["is_peak_hour"] == 1].groupby("route_id")["avg_operational_speed_kmh"].mean()
        offpeak_speeds = segment_df[segment_df["is_peak_hour"] == 0].groupby("route_id")["avg_operational_speed_kmh"].mean()
        
        route_summary["peak_vulnerability_ratio"] = (
            offpeak_speeds / peak_speeds.clip(lower=1.0)
        ).fillna(1.0).round(3).values

        # Directional Asymmetry Ratio (Inbound vs Outbound delay difference)
        inbound_delay = segment_df[segment_df["direction"] == "Inbound"].groupby("route_id")["schedule_adherence_delay_min"].mean()
        outbound_delay = segment_df[segment_df["direction"] == "Outbound"].groupby("route_id")["schedule_adherence_delay_min"].mean()
        route_summary["directional_asymmetry_min"] = (
            (inbound_delay - outbound_delay).abs()
        ).fillna(0.0).round(2).values

        feature_cols = [
            "mean_speed_kmh",
            "speed_cv",
            "mean_congestion_index",
            "mean_dwell_ratio",
            "mean_headway_irregularity",
            "mean_accel_noise",
            "mean_turbulence",
            "mean_delay_min",
            "peak_vulnerability_ratio",
            "stop_density_per_km"
        ]

        # Round numerical features
        for col in feature_cols:
            route_summary[col] = route_summary[col].round(3)

        return route_summary, feature_cols

