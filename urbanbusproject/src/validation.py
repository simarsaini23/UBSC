"""
Cluster Quality and Stability Validation Module
Computes Silhouette Score, Davies-Bouldin Index, Calinski-Harabasz Index,
and runs perturbation bootstrapping to evaluate Adjusted Rand Index (ARI) and NMI stability.
"""

from typing import Dict, List, Tuple
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import (
    adjusted_rand_score,
    calinski_harabasz_score,
    davies_bouldin_score,
    normalized_mutual_info_score,
    silhouette_samples,
    silhouette_score,
)


class TransitClusterValidator:
    """
    Evaluates cluster compactness, separation, and sampling stability.
    """

    def __init__(self, X: np.ndarray, labels: np.ndarray):
        self.X = X
        self.labels = labels
        self.n_samples = len(labels)
        self.unique_labels = np.unique(labels)
        self.k = len(self.unique_labels)

    def compute_quality_metrics(self) -> Dict:
        """
        Calculates Silhouette Score (overall & per-cluster),
        Davies-Bouldin Index, and Calinski-Harabasz Index.
        """
        sil_overall = float(silhouette_score(self.X, self.labels, metric="euclidean"))
        sil_samples = silhouette_samples(self.X, self.labels, metric="euclidean")
        db_index = float(davies_bouldin_score(self.X, self.labels))
        ch_index = float(calinski_harabasz_score(self.X, self.labels))

        per_cluster_sil = {}
        for c in self.unique_labels:
            cluster_mask = self.labels == c
            per_cluster_sil[f"Cluster_{c}"] = {
                "count": int(np.sum(cluster_mask)),
                "mean_silhouette": round(float(np.mean(sil_samples[cluster_mask])), 4),
                "min_silhouette": round(float(np.min(sil_samples[cluster_mask])), 4),
                "max_silhouette": round(float(np.max(sil_samples[cluster_mask])), 4)
            }

        quality_report = {
            "num_clusters_k": self.k,
            "overall_silhouette_score": round(sil_overall, 4),
            "davies_bouldin_index": round(db_index, 4),
            "calinski_harabasz_index": round(ch_index, 2),
            "per_cluster_breakdown": per_cluster_sil,
            "interpretation": {
                "silhouette_verdict": (
                    "Strong cluster separation" if sil_overall > 0.45
                    else "Reasonable structure with minor boundary overlap" if sil_overall > 0.25
                    else "Weak clustering structure"
                ),
                "davies_bouldin_verdict": (
                    "Excellent compactness and separation" if db_index < 1.0
                    else "Good operational separation" if db_index < 1.5
                    else "Moderate cluster overlap"
                )
            }
        }

        return quality_report

    def evaluate_cluster_stability(
        self,
        n_bootstraps: int = 40,
        subsample_ratio: float = 0.85,
        random_state: int = 42
    ) -> Dict:
        """
        Tests cluster stability by resampling 85% of routes over multiple bootstrap iterations.
        Computes Adjusted Rand Index (ARI) and Normalized Mutual Information (NMI)
        between original labels and perturbed models on overlapping samples.
        """
        rng = np.random.RandomState(random_state)
        ari_scores = []
        nmi_scores = []

        subsample_size = int(self.n_samples * subsample_ratio)

        for i in range(n_bootstraps):
            indices = rng.choice(self.n_samples, size=subsample_size, replace=False)
            X_sub = self.X[indices]
            original_labels_sub = self.labels[indices]

            # Fit perturbed model
            km_sub = KMeans(n_clusters=self.k, init="k-means++", n_init=10, random_state=i + 100)
            resampled_labels = km_sub.fit_predict(X_sub)

            ari = adjusted_rand_score(original_labels_sub, resampled_labels)
            nmi = normalized_mutual_info_score(original_labels_sub, resampled_labels)

            ari_scores.append(ari)
            nmi_scores.append(nmi)

        mean_ari = float(np.mean(ari_scores))
        std_ari = float(np.std(ari_scores))
        mean_nmi = float(np.mean(nmi_scores))
        std_nmi = float(np.std(nmi_scores))

        stability_assessment = (
            "Highly Stable & Robust (>0.75 ARI)" if mean_ari >= 0.75
            else "Moderately Stable (0.50-0.75 ARI)" if mean_ari >= 0.50
            else "Sensitive to Sampling Noise (<0.50 ARI)"
        )

        return {
            "n_bootstraps": n_bootstraps,
            "subsample_ratio": subsample_ratio,
            "adjusted_rand_index": {
                "mean": round(mean_ari, 4),
                "std": round(std_ari, 4),
                "min": round(float(np.min(ari_scores)), 4),
                "max": round(float(np.max(ari_scores)), 4)
            },
            "normalized_mutual_information": {
                "mean": round(mean_nmi, 4),
                "std": round(std_nmi, 4),
                "min": round(float(np.min(nmi_scores)), 4),
                "max": round(float(np.max(nmi_scores)), 4)
            },
            "assessment": stability_assessment
        }

