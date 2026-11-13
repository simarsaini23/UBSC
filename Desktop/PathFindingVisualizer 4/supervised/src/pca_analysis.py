import numpy as np
import pandas as pd
from sklearn.decomposition import PCA

def run_pca_reduction(X_scaled, feature_names, metadata_df, cluster_labels=None, n_components=3):
    """
    Implements Objective 2 PCA Dimensionality Reduction:
    - Projects high-dimensional route features to 2D and 3D space
    - Computes explained variance ratios & cumulative variance
    - Extracts component loading vectors (feature contributions)
    """
    pca = PCA(n_components=n_components)
    X_pca = pca.fit_transform(X_scaled)
    
    explained_var = pca.explained_variance_ratio_.tolist()
    cumulative_var = np.cumsum(pca.explained_variance_ratio_).tolist()
    
    # Extract Feature Loading Vectors (Biplot vectors)
    loadings = pca.components_ # shape: (n_components, n_features)
    loadings_dict = {}
    for i in range(n_components):
        loadings_dict[f"PC{i+1}"] = {
            feature_names[j]: float(loadings[i, j])
            for j in range(len(feature_names))
        }
        
    # Format point coordinates for interactive plot
    points = []
    for i in range(len(X_pca)):
        row_meta = metadata_df.iloc[i].to_dict()
        point = {
            "route_id": str(row_meta.get("route_id", f"R-{i}")),
            "route_name": str(row_meta.get("route_name", f"Route {i}")),
            "time_window": str(row_meta.get("time_window", "N/A")),
            "pc1": float(X_pca[i, 0]),
            "pc2": float(X_pca[i, 1]),
            "pc3": float(X_pca[i, 2]) if n_components >= 3 else 0.0,
            "cluster": int(cluster_labels[i]) if cluster_labels is not None else 0
        }
        points.append(point)
        
    return {
        "points": points,
        "explained_variance_ratio": [round(v, 4) for v in explained_var],
        "cumulative_variance_ratio": [round(v, 4) for v in cumulative_var],
        "loadings": loadings_dict
    }
