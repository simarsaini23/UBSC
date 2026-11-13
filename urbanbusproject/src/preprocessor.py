"""
Data Preprocessing Module for Urban Transit Telemetry
Handles missing values, outlier detection, and standardization.
"""

from typing import Dict, List, Optional, Tuple
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer, SimpleImputer
from sklearn.preprocessing import RobustScaler, StandardScaler


class TransitPreprocessor:
    """
    Robust transit data preprocessor that handles missing sensor values,
    detects anomalies, and scales numerical movement features.
    """

    def __init__(
        self,
        imputation_strategy: str = "knn",
        scaling_strategy: str = "standard",
        n_neighbors: int = 5
    ):
        self.imputation_strategy = imputation_strategy
        self.scaling_strategy = scaling_strategy
        self.n_neighbors = n_neighbors
        self.imputer = None
        self.scaler = None
        self.feature_columns: List[str] = []
        self.imputation_stats: Dict = {}

    def fit_impute(
        self,
        df: pd.DataFrame,
        feature_cols: List[str]
    ) -> Tuple[pd.DataFrame, Dict]:
        """
        Detects missing values and imputes them using KNN or Median strategy.
        Tracks missingness statistics before imputation.
        """
        self.feature_columns = feature_cols
        imputed_df = df.copy()

        # Track missingness
        missing_counts = imputed_df[feature_cols].isnull().sum().to_dict()
        missing_pct = {k: round((v / len(df)) * 100, 2) for k, v in missing_counts.items()}
        total_missing = sum(missing_counts.values())

        if self.imputation_strategy == "knn":
            self.imputer = KNNImputer(n_neighbors=self.n_neighbors, weights="distance")
        else:
            self.imputer = SimpleImputer(strategy="median")

        imputed_values = self.imputer.fit_transform(imputed_df[feature_cols])
        imputed_df[feature_cols] = imputed_values

        self.imputation_stats = {
            "strategy": self.imputation_strategy,
            "total_missing_cells": total_missing,
            "missing_counts_per_column": missing_counts,
            "missing_percentage_per_column": missing_pct
        }

        return imputed_df, self.imputation_stats

    def fit_scale(
        self,
        df: pd.DataFrame,
        feature_cols: List[str]
    ) -> Tuple[np.ndarray, pd.DataFrame, Dict]:
        """
        Scales numerical variables using StandardScaler or RobustScaler.
        Provides both standardized array and DataFrame with z-scores.
        """
        X = df[feature_cols].values

        if self.scaling_strategy == "robust":
            self.scaler = RobustScaler()
        else:
            self.scaler = StandardScaler()

        X_scaled = self.scaler.fit_transform(X)
        scaled_df = pd.DataFrame(
            X_scaled,
            columns=[f"{col}_scaled" for col in feature_cols],
            index=df.index
        )

        scaler_stats = {
            "strategy": self.scaling_strategy,
            "means": self.scaler.mean_.tolist() if hasattr(self.scaler, "mean_") else None,
            "scales": self.scaler.scale_.tolist() if hasattr(self.scaler, "scale_") else None,
            "feature_names": feature_cols
        }

        return X_scaled, scaled_df, scaler_stats

    def transform(self, df: pd.DataFrame) -> np.ndarray:
        """Transforms new incoming transit observations."""
        X_imputed = self.imputer.transform(df[self.feature_columns])
        X_scaled = self.scaler.transform(X_imputed)
        return X_scaled

