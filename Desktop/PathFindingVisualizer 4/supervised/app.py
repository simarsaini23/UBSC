import os
import json
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, send_from_directory

from src.preprocessing import preprocess_transit_data
from src.distance_metrics import compare_distance_metrics
from src.clustering_engine import run_kmeans_sweep, run_hierarchical_clustering, execute_clustering
from src.pca_analysis import run_pca_reduction
from src.evaluation import evaluate_cluster_quality, evaluate_cluster_stability, benchmark_configurations
from src.profiler import generate_cluster_profiles
from data.transit_generator import generate_urban_transit_dataset

app = Flask(__name__, static_folder="static", static_url_path="")

# Load or generate initial dataset
DATA_PATH = "data/urban_bus_transit_observations.csv"
GEO_PATH = "data/route_shapes.json"

if not os.path.exists(DATA_PATH) or not os.path.exists(GEO_PATH):
    os.makedirs("data", exist_ok=True)
    df, geo = generate_urban_transit_dataset(160)
    df.to_csv(DATA_PATH, index=False)
    with open(GEO_PATH, "w") as f:
        json.dump(geo, f, indent=2)

def load_current_dataset():
    df = pd.read_csv(DATA_PATH)
    with open(GEO_PATH, "r") as f:
        geo = json.load(f)
    return df, geo

@app.route("/")
def serve_index():
    return send_from_directory("static", "index.html")

@app.route("/api/data", methods=["GET"])
def get_data_summary():
    df, geo = load_current_dataset()
    summary = {
        "total_routes": len(df),
        "columns": list(df.columns),
        "head": df.head(15).replace({np.nan: None}).to_dict(orient="records"),
        "missing_counts": df.isnull().sum().to_dict(),
        "stats": df.describe().round(2).replace({np.nan: None}).to_dict(),
        "route_shapes": geo
    }
    return jsonify(summary)

@app.route("/api/preprocess", methods=["POST"])
def preprocess_data_endpoint():
    req = request.get_json() or {}
    imputation_strategy = req.get("imputation_strategy", "knn")
    scaler_type = req.get("scaler_type", "standard")
    
    df, _ = load_current_dataset()
    prep = preprocess_transit_data(df, imputation_strategy, scaler_type)
    
    return jsonify({
        "imputation_strategy": imputation_strategy,
        "scaler_type": scaler_type,
        "feature_names": prep["feature_names"],
        "missing_handled": prep["missing_handled"],
        "sample_scaled": prep["X_scaled"].head(10).to_dict(orient="records")
    })

@app.route("/api/distance-compare", methods=["POST"])
def distance_compare_endpoint():
    req = request.get_json() or {}
    imputation_strategy = req.get("imputation_strategy", "knn")
    scaler_type = req.get("scaler_type", "standard")
    n_clusters = int(req.get("n_clusters", 4))
    
    df, _ = load_current_dataset()
    prep = preprocess_transit_data(df, imputation_strategy, scaler_type)
    
    result = compare_distance_metrics(prep["X_scaled"].values, n_clusters=n_clusters)
    return jsonify(result)

@app.route("/api/cluster", methods=["POST"])
def cluster_endpoint():
    req = request.get_json() or {}
    algorithm = req.get("algorithm", "kmeans")
    n_clusters = int(req.get("n_clusters", 4))
    linkage_strategy = req.get("linkage", "ward")
    metric = req.get("metric", "euclidean")
    imputation_strategy = req.get("imputation_strategy", "knn")
    scaler_type = req.get("scaler_type", "standard")
    
    df, _ = load_current_dataset()
    prep = preprocess_transit_data(df, imputation_strategy, scaler_type)
    X_scaled = prep["X_scaled"].values
    
    clustering_res = execute_clustering(X_scaled, algorithm, n_clusters, linkage_strategy, metric)
    
    # Always compute K-Means sweep for Elbow plot reference
    kmeans_sweep = run_kmeans_sweep(X_scaled, min_k=2, max_k=8)
    
    # Hierarchical dendrogram data if hierarchical selected
    dendrogram_data = None
    if algorithm == "hierarchical":
        hier = run_hierarchical_clustering(X_scaled, n_clusters, linkage_strategy, metric)
        dendrogram_data = hier["dendrogram_data"]
        
    return jsonify({
        "clustering": clustering_res,
        "kmeans_sweep": kmeans_sweep["sweep"],
        "optimal_k_kmeans": kmeans_sweep["optimal_k"],
        "dendrogram": dendrogram_data
    })

@app.route("/api/pca", methods=["POST"])
def pca_endpoint():
    req = request.get_json() or {}
    algorithm = req.get("algorithm", "kmeans")
    n_clusters = int(req.get("n_clusters", 4))
    linkage_strategy = req.get("linkage", "ward")
    metric = req.get("metric", "euclidean")
    imputation_strategy = req.get("imputation_strategy", "knn")
    scaler_type = req.get("scaler_type", "standard")
    
    df, _ = load_current_dataset()
    prep = preprocess_transit_data(df, imputation_strategy, scaler_type)
    X_scaled = prep["X_scaled"].values
    
    clustering_res = execute_clustering(X_scaled, algorithm, n_clusters, linkage_strategy, metric)
    labels = clustering_res["labels"]
    
    pca_res = run_pca_reduction(X_scaled, prep["feature_names"], prep["metadata"], labels, n_components=3)
    return jsonify(pca_res)

@app.route("/api/evaluate", methods=["POST"])
def evaluate_endpoint():
    req = request.get_json() or {}
    algorithm = req.get("algorithm", "kmeans")
    n_clusters = int(req.get("n_clusters", 4))
    linkage_strategy = req.get("linkage", "ward")
    metric = req.get("metric", "euclidean")
    imputation_strategy = req.get("imputation_strategy", "knn")
    scaler_type = req.get("scaler_type", "standard")
    
    df, _ = load_current_dataset()
    prep = preprocess_transit_data(df, imputation_strategy, scaler_type)
    X_scaled = prep["X_scaled"].values
    
    clustering_res = execute_clustering(X_scaled, algorithm, n_clusters, linkage_strategy, metric)
    labels = clustering_res["labels"]
    
    quality = evaluate_cluster_quality(X_scaled, labels, metric=metric if algorithm != "kmeans" else "euclidean")
    stability = evaluate_cluster_stability(X_scaled, algorithm, n_clusters, linkage_strategy)
    benchmarks = benchmark_configurations(X_scaled)
    
    return jsonify({
        "quality": quality,
        "stability": stability,
        "benchmarks": benchmarks
    })

@app.route("/api/profiles", methods=["POST"])
def profiles_endpoint():
    req = request.get_json() or {}
    algorithm = req.get("algorithm", "kmeans")
    n_clusters = int(req.get("n_clusters", 4))
    linkage_strategy = req.get("linkage", "ward")
    metric = req.get("metric", "euclidean")
    imputation_strategy = req.get("imputation_strategy", "knn")
    scaler_type = req.get("scaler_type", "standard")
    
    df, _ = load_current_dataset()
    prep = preprocess_transit_data(df, imputation_strategy, scaler_type)
    X_scaled = prep["X_scaled"].values
    
    clustering_res = execute_clustering(X_scaled, algorithm, n_clusters, linkage_strategy, metric)
    labels = clustering_res["labels"]
    
    profiles = generate_cluster_profiles(prep["X_imputed"], labels, prep["metadata"])
    return jsonify(profiles)

@app.route("/api/export-report", methods=["POST"])
def export_report_endpoint():
    req = request.get_json() or {}
    algorithm = req.get("algorithm", "kmeans")
    n_clusters = int(req.get("n_clusters", 4))
    
    df, _ = load_current_dataset()
    prep = preprocess_transit_data(df)
    X_scaled = prep["X_scaled"].values
    
    clustering_res = execute_clustering(X_scaled, algorithm, n_clusters)
    labels = clustering_res["labels"]
    quality = evaluate_cluster_quality(X_scaled, labels)
    profiles = generate_cluster_profiles(prep["X_imputed"], labels, prep["metadata"])
    
    report_md = f"""# UrbanFlow-AI: Executive Analytical Report
## Unsupervised Clustering of Urban Bus Routes Using Traffic Patterns

### Executive Summary
- **Total Bus Routes Analyzed**: {len(df)} routes/time segments
- **Clustering Algorithm Executed**: {algorithm.upper()} (k={n_clusters})
- **Silhouette Score**: {quality['silhouette']}
- **Davies-Bouldin Index**: {quality['davies_bouldin']}
- **Calinski-Harabasz Index**: {quality['calinski_harabasz']}

---

### Discovered Urban Traffic Patterns & Operational Archetypes

"""
    for p in profiles:
        report_md += f"""#### Cluster {p['cluster_id']}: {p['title']} ({p['percentage']}% of Fleet, {p['route_count']} Routes)
- **Description**: {p['description']}
- **Recommendation**: {p['recommendation']}
- **Average Speed**: {p['features']['avg_speed_kmh']} km/h
- **Peak Congestion Index**: {p['features']['peak_congestion_index']}
- **Dwell Time per Stop**: {p['features']['dwell_time_per_stop_sec']} sec
- **Schedule Delay Index**: {p['features']['schedule_delay_index']}

"""

    report_md += """---
*Report generated automatically by UrbanFlow-AI Machine Learning Analytics Platform (SIH Edition).*
"""
    return jsonify({"markdown": report_md})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
