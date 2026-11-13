"""
Dimensionality Reduction Module
Implements Principal Component Analysis (PCA) for Scree analysis,
factor loadings biplot, and 2D/3D visualization of transit traffic patterns.
"""

from typing import Dict, List, Tuple
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA


class TransitDimensionalityReducer:
    """
    Performs PCA on standardized transit features to capture latent operational dimensions
    and project multi-dimensional route profiles into 2D and 3D spaces.
    """

    def __init__(self, n_components: int = 4):
        self.n_components = n_components
        self.pca = PCA(n_components=n_components)
        self.feature_names: List[str] = []
        self.loadings_df: pd.DataFrame = pd.DataFrame()
        self.explained_variance_ratio: np.ndarray = np.array([])
        self.cumulative_variance: np.ndarray = np.array([])

    def fit_transform(
        self,
        X: np.ndarray,
        feature_names: List[str]
    ) -> Tuple[np.ndarray, Dict]:
        """
        Fits PCA on feature matrix X and transforms data into principal components.
        Extracts explained variance, eigenvalues, and feature loadings.
        """
        self.feature_names = feature_names
        X_pca = self.pca.fit_transform(X)

        self.explained_variance_ratio = self.pca.explained_variance_ratio_
        self.cumulative_variance = np.cumsum(self.explained_variance_ratio)

        # Factor Loadings: components_ has shape (n_components, n_features)
        # Loadings = components_ * sqrt(explained_variance_)
        loadings = self.pca.components_.T * np.sqrt(self.pca.explained_variance_)
        self.loadings_df = pd.DataFrame(
            loadings,
            index=self.feature_names,
            columns=[f"PC{i+1}" for i in range(self.n_components)]
        )

        scree_data = []
        for i in range(self.n_components):
            scree_data.append({
                "component": f"PC{i+1}",
                "eigenvalue": round(float(self.pca.explained_variance_[i]), 4),
                "explained_variance_ratio": round(float(self.explained_variance_ratio[i]), 4),
                "cumulative_variance_ratio": round(float(self.cumulative_variance[i]), 4)
            })

        # Feature contribution to PC1 and PC2 (biplot coordinates)
        biplot_vectors = {}
        for feat in self.feature_names:
            biplot_vectors[feat] = {
                "pc1_loading": round(float(self.loadings_df.loc[feat, "PC1"]), 4),
                "pc2_loading": round(float(self.loadings_df.loc[feat, "PC2"]), 4),
                "magnitude": round(float(np.sqrt(self.loadings_df.loc[feat, "PC1"]**2 + self.loadings_df.loc[feat, "PC2"]**2)), 4)
            }

        # Interpret the top driving features of PC1 and PC2
        pc1_top = self.loadings_df["PC1"].abs().sort_values(ascending=False).index[:3].tolist()
        pc2_top = self.loadings_df["PC2"].abs().sort_values(ascending=False).index[:3].tolist()

        pca_summary = {
            "scree_data": scree_data,
            "biplot_vectors": biplot_vectors,
            "total_explained_variance_top2": round(float(self.cumulative_variance[1]), 4),
            "total_explained_variance_top3": round(float(self.cumulative_variance[2]), 4) if self.n_components >= 3 else None,
            "pc1_dominant_features": pc1_top,
            "pc2_dominant_features": pc2_top,
            "interpretation_pc1": f"Traffic Friction & Impedance (heavily loaded by {', '.join(pc1_top)})",
            "interpretation_pc2": f"Operational Regularity & Stop Density (heavily loaded by {', '.join(pc2_top)})"
        }

        return X_pca, pca_summary

    def transform(self, X: np.ndarray) -> np.ndarray:
        """Projects new observations into existing PCA space."""
        return self.pca.transform(X)

