import numpy as np
import pandas as pd
from sklearn.cluster import KMeans, AgglomerativeClustering
from scipy.cluster.hierarchy import linkage, dendrogram
from sklearn.metrics import silhouette_score, davies_bouldin_score

def run_kmeans_sweep(X_scaled, min_k=2, max_k=8, random_state=42):
    """
    Executes K-Means over k=min_k..max_k, tracking WCSS (inertia),
    Silhouette Score, and Davies-Bouldin Index for Elbow & evaluation curve analysis.
    """
    results = []
    best_k = min_k
    best_sil = -1.0
    
    for k in range(min_k, max_k + 1):
        km = KMeans(n_clusters=k, init="k-means++", n_init=10, random_state=random_state)
        labels = km.fit_predict(X_scaled)
        
        inertia = float(km.inertia_)
        sil = float(silhouette_score(X_scaled, labels)) if k > 1 else 0.0
        dbi = float(davies_bouldin_score(X_scaled, labels)) if k > 1 else 0.0
        
        if sil > best_sil:
            best_sil = sil
            best_k = k
            
        results.append({
            "k": k,
            "inertia": inertia,
            "silhouette_score": round(sil, 4),
            "davies_bouldin_index": round(dbi, 4),
            "labels": labels.tolist(),
            "centroids": km.cluster_centers_.tolist()
        })
        
    return {
        "sweep": results,
        "optimal_k": best_k,
        "best_silhouette": round(best_sil, 4)
    }

def run_hierarchical_clustering(X_scaled, n_clusters=4, linkage_strategy="ward", metric="euclidean"):
    """
    Executes Agglomerative Hierarchical Clustering with flexible linkage strategies:
    'ward', 'complete', 'average', 'single'.
    Returns linkage matrix for dendrogram tree generation.
    """
    # Ward linkage requires Euclidean distance
    if linkage_strategy == "ward":
        metric = "euclidean"
        
    model = AgglomerativeClustering(n_clusters=n_clusters, linkage=linkage_strategy, metric=metric)
    labels = model.fit_predict(X_scaled)
    
    # Compute dendrogram linkage matrix using scipy
    Z = linkage(X_scaled, method=linkage_strategy, metric=metric)
    
    # Format top N dendrogram nodes for JSON API visualization
    # We truncate dendrogram tree to top 30 merged nodes for UI rendering clarity
    dendro = dendrogram(Z, no_plot=True, truncate_mode="lastp", p=30)
    
    sil = float(silhouette_score(X_scaled, labels, metric=metric))
    dbi = float(davies_bouldin_score(X_scaled, labels))
    
    return {
        "n_clusters": n_clusters,
        "linkage_strategy": linkage_strategy,
        "metric": metric,
        "labels": labels.tolist(),
        "silhouette_score": round(sil, 4),
        "davies_bouldin_index": round(dbi, 4),
        "dendrogram_data": {
            "icoord": dendro["icoord"],
            "dcoord": dendro["dcoord"],
            "leaves": dendro["leaves"],
            "color_list": dendro["color_list"]
        }
    }

def execute_clustering(X_scaled, algorithm="kmeans", n_clusters=4, linkage_strategy="ward", metric="euclidean"):
    """
    Unified execution pipeline wrapper for K-Means and Hierarchical Clustering.
    """
    if algorithm.lower() == "kmeans":
        km = KMeans(n_clusters=n_clusters, init="k-means++", n_init=10, random_state=42)
        labels = km.fit_predict(X_scaled)
        centroids = km.cluster_centers_.tolist()
    else:
        if linkage_strategy == "ward":
            metric = "euclidean"
        agg = AgglomerativeClustering(n_clusters=n_clusters, linkage=linkage_strategy, metric=metric)
        labels = agg.fit_predict(X_scaled)
        centroids = None
        
    sil = float(silhouette_score(X_scaled, labels, metric=metric if algorithm != "kmeans" else "euclidean"))
    dbi = float(davies_bouldin_score(X_scaled, labels))
    
    return {
        "algorithm": algorithm,
        "n_clusters": n_clusters,
        "linkage_strategy": linkage_strategy if algorithm != "kmeans" else "N/A",
        "metric": metric,
        "labels": labels.tolist(),
        "centroids": centroids,
        "silhouette_score": round(sil, 4),
        "davies_bouldin_index": round(dbi, 4)
    }
