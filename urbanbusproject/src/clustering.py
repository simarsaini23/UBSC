"""
Clustering Engine Module
Implements K-Means and Hierarchical Agglomerative Clustering with multi-configuration
and linkage strategy evaluation (Ward, Complete, Average, Single).
"""

from typing import Dict, List, Optional, Tuple
import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import cophenet, linkage
from scipy.spatial.distance import pdist
from sklearn.cluster import AgglomerativeClustering, KMeans
from sklearn.metrics import calinski_harabasz_score, davies_bouldin_score, silhouette_score


class TransitClusteringEngine:
    """
    Manages multi-algorithm unsupervised clustering across bus route operational behaviors.
    """

    def __init__(self, X: np.ndarray, feature_names: List[str]):
        self.X = X
        self.feature_names = feature_names
        self.kmeans_models: Dict[int, KMeans] = {}
        self.hierarchical_models: Dict[str, AgglomerativeClustering] = {}
        self.linkage_matrices: Dict[str, np.ndarray] = {}

    def evaluate_kmeans_spectrum(
        self,
        k_min: int = 2,
        k_max: int = 8,
        random_state: int = 42
    ) -> Tuple[pd.DataFrame, int]:
        """
        Sweeps K-Means across k_min to k_max to compute:
        - Inertia (Sum of squared errors / Elbow curve)
        - Silhouette Score (higher is better)
        - Davies-Bouldin Index (lower is better)
        - Calinski-Harabasz Index (higher is better)
        Identifies mathematically recommended optimal k.
        """
        results = []
        best_k = k_min
        best_silhouette = -1.0

        for k in range(k_min, k_max + 1):
            km = KMeans(n_clusters=k, init="k-means++", n_init=20, max_iter=300, random_state=random_state)
            labels = km.fit_predict(self.X)
            self.kmeans_models[k] = km

            inertia = float(km.inertia_)
            sil = float(silhouette_score(self.X, labels, metric="euclidean"))
            db = float(davies_bouldin_score(self.X, labels))
            ch = float(calinski_harabasz_score(self.X, labels))

            results.append({
                "k": k,
                "inertia": round(inertia, 2),
                "silhouette_score": round(sil, 4),
                "davies_bouldin_index": round(db, 4),
                "calinski_harabasz_index": round(ch, 2)
            })

            if sil > best_silhouette:
                best_silhouette = sil
                best_k = k

        results_df = pd.DataFrame(results)
        return results_df, best_k

    def evaluate_hierarchical_linkages(
        self,
        k: int = 4,
        metric: str = "euclidean"
    ) -> Dict:
        """
        Evaluates 4 hierarchical linkage strategies:
        1. Ward: Minimizes variance growth (requires euclidean)
        2. Complete: Maximum pairwise cluster distance
        3. Average: Mean pairwise cluster distance
        4. Single: Minimum pairwise cluster distance (chaining behavior)
        Computes Cophenetic Correlation Coefficient for each linkage.
        """
        linkage_types = ["ward", "complete", "average", "single"]
        pdist_condensed = pdist(self.X, metric=metric)

        linkage_eval = {}

        for link in linkage_types:
            # Ward requires euclidean metric
            current_metric = "euclidean" if link == "ward" else metric

            # Scipy linkage tree for dendrogram & cophenetic correlation
            Z = linkage(self.X, method=link, metric=current_metric)
            self.linkage_matrices[link] = Z
            coph_corr, _ = cophenet(Z, pdist_condensed)

            # Sklearn model for predictions and metrics
            model = AgglomerativeClustering(n_clusters=k, metric=current_metric, linkage=link)
            labels = model.fit_predict(self.X)
            self.hierarchical_models[link] = model

            sil = float(silhouette_score(self.X, labels, metric=current_metric))
            db = float(davies_bouldin_score(self.X, labels))
            ch = float(calinski_harabasz_score(self.X, labels))

            # Cluster distribution
            cluster_distribution = pd.Series(labels).value_counts().to_dict()

            linkage_eval[link] = {
                "linkage_method": link,
                "cophenetic_correlation": round(float(coph_corr), 4),
                "silhouette_score": round(sil, 4),
                "davies_bouldin_index": round(db, 4),
                "calinski_harabasz_index": round(ch, 2),
                "cluster_distribution": cluster_distribution,
                "labels": labels.tolist(),
                "characteristics": self._get_linkage_desc(link)
            }

        return linkage_eval

    def _get_linkage_desc(self, link: str) -> str:
        descs = {
            "ward": "Minimizes the total within-cluster variance. Produces balanced, compact, spherical clusters.",
            "complete": "Finds clusters based on maximum pairwise distance. Favors compact clusters of equal diameter.",
            "average": "Computes average distance between all pairs. Balanced compromise between Ward and Single.",
            "single": "Computes minimum pairwise distance. Highly prone to chaining; identifies non-spherical serpentine shapes."
        }
        return descs.get(link, "")

    def get_kmeans_champion(self, k: int) -> Tuple[np.ndarray, np.ndarray]:
        """Returns labels and cluster centroids for chosen k."""
        if k not in self.kmeans_models:
            km = KMeans(n_clusters=k, init="k-means++", n_init=20, random_state=42)
            labels = km.fit_predict(self.X)
            self.kmeans_models[k] = km
        else:
            km = self.kmeans_models[k]
            labels = km.labels_
        return labels, km.cluster_centers_

