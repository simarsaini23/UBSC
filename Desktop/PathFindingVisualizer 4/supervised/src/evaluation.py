import numpy as np
import pandas as pd
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score, adjusted_rand_score
from sklearn.cluster import KMeans, AgglomerativeClustering

def evaluate_cluster_quality(X_scaled, labels, metric="euclidean"):
    """
    Computes core cluster quality metrics:
    - Silhouette Score (Separation & Cohesion)
    - Davies-Bouldin Index (Cluster Compactness vs Separation)
    - Calinski-Harabasz Index (Variance Ratio)
    """
    n_clusters = len(set(labels))
    if n_clusters < 2:
        return {"silhouette": 0.0, "davies_bouldin": 0.0, "calinski_harabasz": 0.0}
        
    sil = float(silhouette_score(X_scaled, labels, metric=metric))
    dbi = float(davies_bouldin_score(X_scaled, labels))
    chi = float(calinski_harabasz_score(X_scaled, labels))
    
    return {
        "silhouette": round(sil, 4),
        "davies_bouldin": round(dbi, 4),
        "calinski_harabasz": round(chi, 2)
    }

def evaluate_cluster_stability(X_scaled, algorithm="kmeans", n_clusters=4, linkage_strategy="ward", n_bootstraps=15, sample_ratio=0.8, seed=42):
    """
    Implements Objective 3 Cluster Stability Examination:
    Subsamples data (80%) across 15 iterations and evaluates average Adjusted Rand Index (ARI)
    between original cluster model and subsampled re-clustering to measure partition stability.
    """
    np.random.seed(seed)
    n_samples = X_scaled.shape[0]
    subsample_size = int(n_samples * sample_ratio)
    
    # Fit full model
    if algorithm == "kmeans":
        model_full = KMeans(n_clusters=n_clusters, init="k-means++", n_init=10, random_state=seed)
        full_labels = model_full.fit_predict(X_scaled)
    else:
        model_full = AgglomerativeClustering(n_clusters=n_clusters, linkage=linkage_strategy)
        full_labels = model_full.fit_predict(X_scaled)
        
    ari_scores = []
    
    for i in range(n_bootstraps):
        indices = np.random.choice(n_samples, size=subsample_size, replace=False)
        X_sub = X_scaled[indices]
        full_labels_sub = full_labels[indices]
        
        if algorithm == "kmeans":
            model_sub = KMeans(n_clusters=n_clusters, init="k-means++", n_init=10, random_state=seed + i)
            sub_labels = model_sub.fit_predict(X_sub)
        else:
            model_sub = AgglomerativeClustering(n_clusters=n_clusters, linkage=linkage_strategy)
            sub_labels = model_sub.fit_predict(X_sub)
            
        score = adjusted_rand_score(full_labels_sub, sub_labels)
        ari_scores.append(score)
        
    mean_ari = float(np.mean(ari_scores))
    std_ari = float(np.std(ari_scores))
    
    if mean_ari >= 0.75:
        stability_rating = "Highly Stable (Consistent operational partition across subsamples)"
    elif mean_ari >= 0.50:
        stability_rating = "Moderately Stable (Minor cluster boundary shift on subset data)"
    else:
        stability_rating = "Low Stability (Sensitive to data perturbations)"
        
    return {
        "mean_ari": round(mean_ari, 4),
        "std_ari": round(std_ari, 4),
        "bootstrap_count": n_bootstraps,
        "sample_ratio": sample_ratio,
        "stability_rating": stability_rating
    }

def benchmark_configurations(X_scaled):
    """
    Benchmarks multiple algorithm configurations (K-Means vs Ward vs Complete vs Average vs Single)
    across k=2..6 for comprehensive comparison table.
    """
    benchmarks = []
    
    configs = [
        ("kmeans", "N/A", "euclidean"),
        ("hierarchical", "ward", "euclidean"),
        ("hierarchical", "complete", "euclidean"),
        ("hierarchical", "complete", "manhattan"),
        ("hierarchical", "average", "euclidean"),
        ("hierarchical", "single", "euclidean")
    ]
    
    for alg, linkage_strat, metric in configs:
        for k in range(2, 6):
            try:
                if alg == "kmeans":
                    m = KMeans(n_clusters=k, init="k-means++", n_init=10, random_state=42)
                    lbls = m.fit_predict(X_scaled)
                else:
                    m = AgglomerativeClustering(n_clusters=k, linkage=linkage_strat, metric=metric)
                    lbls = m.fit_predict(X_scaled)
                    
                q = evaluate_cluster_quality(X_scaled, lbls, metric=metric if alg != "kmeans" else "euclidean")
                benchmarks.append({
                    "algorithm": alg.upper(),
                    "linkage": linkage_strat,
                    "metric": metric,
                    "k": k,
                    "silhouette": q["silhouette"],
                    "davies_bouldin": q["davies_bouldin"],
                    "calinski_harabasz": q["calinski_harabasz"]
                })
            except Exception as e:
                continue
                
    return benchmarks
