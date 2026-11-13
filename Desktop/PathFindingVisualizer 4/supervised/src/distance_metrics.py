import numpy as np
import pandas as pd
from sklearn.metrics import pairwise_distances, silhouette_score
from sklearn.cluster import AgglomerativeClustering, KMeans

def compare_distance_metrics(X_scaled, n_clusters=4):
    """
    Implements Objective 1 Distance Comparison:
    Computes pairwise Euclidean and Manhattan distance matrices,
    evaluates distance variance/contrast ratio, and compares silhouette score suitability.
    """
    dist_euclidean = pairwise_distances(X_scaled, metric="euclidean")
    dist_manhattan = pairwise_distances(X_scaled, metric="manhattan")
    
    # Extract upper triangle values (excluding diagonal zero)
    triu_idx = np.triu_indices_from(dist_euclidean, k=1)
    euc_vals = dist_euclidean[triu_idx]
    man_vals = dist_manhattan[triu_idx]
    
    # Statistical analysis of distance metrics
    euc_stats = {
        "mean": float(np.mean(euc_vals)),
        "std": float(np.std(euc_vals)),
        "min": float(np.min(euc_vals)),
        "max": float(np.max(euc_vals)),
        "contrast_ratio": float(np.std(euc_vals) / (np.mean(euc_vals) + 1e-6))
    }
    
    man_stats = {
        "mean": float(np.mean(man_vals)),
        "std": float(np.std(man_vals)),
        "min": float(np.min(man_vals)),
        "max": float(np.max(man_vals)),
        "contrast_ratio": float(np.std(man_vals) / (np.mean(man_vals) + 1e-6))
    }
    
    # Evaluate Hierarchical Clustering quality under Euclidean vs Manhattan
    agg_euc = AgglomerativeClustering(n_clusters=n_clusters, metric="euclidean", linkage="complete")
    labels_euc = agg_euc.fit_predict(X_scaled)
    sil_euc = float(silhouette_score(X_scaled, labels_euc, metric="euclidean"))
    
    agg_man = AgglomerativeClustering(n_clusters=n_clusters, metric="manhattan", linkage="complete")
    labels_man = agg_man.fit_predict(X_scaled)
    sil_man = float(silhouette_score(X_scaled, labels_man, metric="manhattan"))
    
    # Determine suitability recommendation
    if euc_stats["contrast_ratio"] >= man_stats["contrast_ratio"] and sil_euc >= sil_man:
        suitability_rec = "Euclidean metric demonstrates higher contrast ratio and better spatial separation in standardized feature space."
        best_metric = "euclidean"
    else:
        suitability_rec = "Manhattan metric shows superior robustness against feature scale variance and higher silhouette separation."
        best_metric = "manhattan"
        
    return {
        "euclidean": {
            "stats": euc_stats,
            "silhouette": sil_euc,
            "sample_matrix": dist_euclidean[:10, :10].tolist()
        },
        "manhattan": {
            "stats": man_stats,
            "silhouette": sil_man,
            "sample_matrix": dist_manhattan[:10, :10].tolist()
        },
        "recommendation": suitability_rec,
        "recommended_metric": best_metric
    }
