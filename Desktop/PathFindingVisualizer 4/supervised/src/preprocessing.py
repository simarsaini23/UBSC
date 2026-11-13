import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer, SimpleImputer
from sklearn.preprocessing import StandardScaler, MinMaxScaler

FEATURE_COLUMNS = [
    "length_km",
    "avg_speed_kmh",
    "speed_variance",
    "peak_congestion_index",
    "stop_density_per_km",
    "dwell_time_per_stop_sec",
    "schedule_delay_index",
    "passenger_turnover_rate",
    "reliability_score"
]

def preprocess_transit_data(df, imputation_strategy="knn", scaler_type="standard"):
    """
    Implements Objective 1:
    - Handles missing values using KNN or Median imputation
    - Constructs movement & temporal composite features
    - Standardizes numerical variables using StandardScaler or MinMaxScaler
    """
    data = df.copy()
    
    # 1. Feature Engineering: Composite Movement & Temporal Features
    # Speed-to-Congestion Ratio
    data["speed_congestion_ratio"] = data["avg_speed_kmh"] / (data["peak_congestion_index"] + 0.01)
    # Stop Dwell Delay Index
    data["stop_dwell_factor"] = data["stop_density_per_km"] * data["dwell_time_per_stop_sec"]
    
    extended_features = FEATURE_COLUMNS + ["speed_congestion_ratio", "stop_dwell_factor"]
    
    X_raw = data[extended_features].copy()
    
    # 2. Impute Missing Values
    if imputation_strategy == "knn":
        imputer = KNNImputer(n_neighbors=5)
        X_imputed = imputer.fit_transform(X_raw)
    else:
        imputer = SimpleImputer(strategy="median")
        X_imputed = imputer.fit_transform(X_raw)
        
    X_imputed_df = pd.DataFrame(X_imputed, columns=extended_features, index=data.index)
    
    # 3. Standardize Numerical Variables
    if scaler_type == "standard":
        scaler = StandardScaler()
    else:
        scaler = MinMaxScaler()
        
    X_scaled = scaler.fit_transform(X_imputed_df)
    X_scaled_df = pd.DataFrame(X_scaled, columns=extended_features, index=data.index)
    
    # Summary of missing values handled
    missing_summary = X_raw.isnull().sum().to_dict()
    
    return {
        "X_raw": X_raw,
        "X_imputed": X_imputed_df,
        "X_scaled": X_scaled_df,
        "scaler": scaler,
        "feature_names": extended_features,
        "missing_handled": missing_summary,
        "metadata": data[["route_id", "route_name", "time_window"]]
    }
