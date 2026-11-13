"""
Distance Metrics Comparison Module
Compares Euclidean (L2) and Manhattan (L1) distance measures for clustering transit patterns.
"""

from typing import Dict, Tuple
import numpy as np
import pandas as pd
from scipy.spatial.distance import pdist, squareform
from scipy.stats import pearsonr, spearmanr
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import silhouette_score


class DistanceMetricComparator:
    """
    Evaluates Euclidean vs. Manhattan distance suitability across transit feature spaces,
    analyzing distance contrast, correlation, and clustering separation.
    """

    def __init__(self, X: np.ndarray, feature_names: list):
        self.X = X
        self.feature_names = feature_names
        self.n_samples, self.n_features = X.shape

    def compute_distance_matrices(self) -> Tuple[np.ndarray, np.ndarray]:
        """Computes pairwise Euclidean (L2) and Manhattan (L1) distance matrices."""
        dist_euclidean = squareform(pdist(self.X, metric="euclidean"))
        dist_manhattan = squareform(pdist(self.X, metric="cityblock"))
        return dist_euclidean, dist_manhattan

    def analyze_metrics_contrast(self) -> Dict:
        """
        Analyzes distance concentration effect and relative contrast:
        Contrast = (d_max - d_min) / d_min.
        Higher contrast indicates greater discriminative power between routes.
        """
        d_euc_condensed = pdist(self.X, metric="euclidean")
        d_man_condensed = pdist(self.X, metric="cityblock")

        # Non-zero minimum distance
        min_euc = np.min(d_euc_condensed[d_euc_condensed > 0])
        max_euc = np.max(d_euc_condensed)
        mean_euc = np.mean(d_euc_condensed)
        std_euc = np.std(d_euc_condensed)
        contrast_euc = (max_euc - min_euc) / (min_euc + 1e-9)

        min_man = np.min(d_man_condensed[d_man_condensed > 0])
        max_man = np.max(d_man_condensed)
        mean_man = np.mean(d_man_condensed)
        std_man = np.std(d_man_condensed)
        contrast_man = (max_man - min_man) / (min_man + 1e-9)

        # Correlation between distance measures
        p_corr, _ = pearsonr(d_euc_condensed, d_man_condensed)
        s_corr, _ = spearmanr(d_euc_condensed, d_man_condensed)

        analysis = {
            "n_samples": self.n_samples,
            "n_features": self.n_features,
            "euclidean": {
                "metric_name": "Euclidean (L2 Norm)",
                "formula": "||x - y||_2 = sqrt(sum((x_i - y_i)^2))",
                "mean_distance": round(float(mean_euc), 3),
                "std_distance": round(float(std_euc), 3),
                "min_distance": round(float(min_euc), 3),
                "max_distance": round(float(max_euc), 3),
                "relative_contrast": round(float(contrast_euc), 3),
                "variance_ratio": round(float(std_euc / (mean_euc + 1e-9)), 3),
                "geometry": "Hyperspherical (sensitive to squared extreme variations)"
            },
            "manhattan": {
                "metric_name": "Manhattan (L1 Norm / Cityblock)",
                "formula": "||x - y||_1 = sum(|x_i - y_i|)",
                "mean_distance": round(float(mean_man), 3),
                "std_distance": round(float(std_man), 3),
                "min_distance": round(float(min_man), 3),
                "max_distance": round(float(max_man), 3),
                "relative_contrast": round(float(contrast_man), 3),
                "variance_ratio": round(float(std_man / (mean_man + 1e-9)), 3),
                "geometry": "Diamond / Taxicab (robust against isolated sensor shocks)"
            },
            "correlations": {
                "pearson_linear_correlation": round(float(p_corr), 4),
                "spearman_rank_correlation": round(float(s_corr), 4)
            }
        }

        return analysis

    def evaluate_clustering_suitability(self, k: int = 4) -> Dict:
        """
        Runs Hierarchical Agglomerative clustering using Euclidean vs Manhattan distance
        and calculates Silhouette scores under both distance spaces.
        """
        # Euclidean Agglomerative
        agg_euc = AgglomerativeClustering(n_clusters=k, metric="euclidean", linkage="average")
        labels_euc = agg_euc.fit_predict(self.X)
        sil_euc_in_euc = silhouette_score(self.X, labels_euc, metric="euclidean")
        sil_euc_in_man = silhouette_score(self.X, labels_euc, metric="cityblock")

        # Manhattan Agglomerative
        agg_man = AgglomerativeClustering(n_clusters=k, metric="manhattan", linkage="average")
        labels_man = agg_man.fit_predict(self.X)
        sil_man_in_euc = silhouette_score(self.X, labels_man, metric="euclidean")
        sil_man_in_man = silhouette_score(self.X, labels_man, metric="cityblock")

        agreement_ari = float(
            pd.Series(labels_euc).corr(pd.Series(labels_man), method="pearson")
        )

        return {
            "tested_k": k,
            "euclidean_model": {
                "silhouette_euclidean_eval": round(float(sil_euc_in_euc), 3),
                "silhouette_manhattan_eval": round(float(sil_euc_in_man), 3),
                "cluster_counts": pd.Series(labels_euc).value_counts().to_dict()
            },
            "manhattan_model": {
                "silhouette_euclidean_eval": round(float(sil_man_in_euc), 3),
                "silhouette_manhattan_eval": round(float(sil_man_in_man), 3),
                "cluster_counts": pd.Series(labels_man).value_counts().to_dict()
            },
            "recommendation": (
                "Manhattan distance is superior for outlier-resilient transit telemetry where localized "
                "congestion spikes can artificially distort squared Euclidean distances. Euclidean distance "
                "remains ideal when optimizing intra-cluster variance under K-Means."
            )
        }

