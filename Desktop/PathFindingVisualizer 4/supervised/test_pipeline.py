import unittest
import json
import pandas as pd
import numpy as np
from src.preprocessing import preprocess_transit_data
from src.distance_metrics import compare_distance_metrics
from src.clustering_engine import run_kmeans_sweep, run_hierarchical_clustering, execute_clustering
from src.pca_analysis import run_pca_reduction
from src.evaluation import evaluate_cluster_quality, evaluate_cluster_stability, benchmark_configurations
from src.profiler import generate_cluster_profiles
from app import app

class TestUrbanFlowPipeline(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.df = pd.read_csv("data/urban_bus_transit_observations.csv")
        with open("data/route_shapes.json", "r") as f:
            cls.geo = json.load(f)
            
    def test_objective1_preprocessing(self):
        prep = preprocess_transit_data(self.df, imputation_strategy="knn", scaler_type="standard")
        self.assertIn("X_scaled", prep)
        self.assertFalse(prep["X_scaled"].isnull().any().any(), "Scaled feature matrix should have 0 missing values.")
        self.assertGreater(len(prep["feature_names"]), 8)
        print("✓ Objective 1 Preprocessing & Imputation Test Passed")
        
    def test_objective1_distance_metrics(self):
        prep = preprocess_transit_data(self.df)
        dist_res = compare_distance_metrics(prep["X_scaled"].values, n_clusters=4)
        self.assertIn("euclidean", dist_res)
        self.assertIn("manhattan", dist_res)
        self.assertIn("contrast_ratio", dist_res["euclidean"]["stats"])
        self.assertIn(dist_res["recommended_metric"], ["euclidean", "manhattan"])
        print("✓ Objective 1 Distance Metrics Suitability Test Passed")
        
    def test_objective2_clustering_engine(self):
        prep = preprocess_transit_data(self.df)
        X_scaled = prep["X_scaled"].values
        
        # Test K-Means Sweep
        sweep = run_kmeans_sweep(X_scaled, min_k=2, max_k=6)
        self.assertEqual(len(sweep["sweep"]), 5)
        
        # Test Hierarchical Clustering
        hier = run_hierarchical_clustering(X_scaled, n_clusters=4, linkage_strategy="ward")
        self.assertEqual(len(hier["labels"]), len(self.df))
        self.assertIn("dendrogram_data", hier)
        print("✓ Objective 2 K-Means & Hierarchical Clustering Test Passed")

    def test_objective2_pca_analysis(self):
        prep = preprocess_transit_data(self.df)
        X_scaled = prep["X_scaled"].values
        clustering_res = execute_clustering(X_scaled, algorithm="kmeans", n_clusters=4)
        
        pca_res = run_pca_reduction(X_scaled, prep["feature_names"], prep["metadata"], clustering_res["labels"], n_components=3)
        self.assertEqual(len(pca_res["points"]), len(self.df))
        self.assertEqual(len(pca_res["explained_variance_ratio"]), 3)
        print("✓ Objective 2 PCA 2D/3D Dimensionality Reduction Test Passed")

    def test_objective3_evaluation_and_profiling(self):
        prep = preprocess_transit_data(self.df)
        X_scaled = prep["X_scaled"].values
        clustering_res = execute_clustering(X_scaled, algorithm="kmeans", n_clusters=4)
        labels = clustering_res["labels"]
        
        quality = evaluate_cluster_quality(X_scaled, labels)
        self.assertGreater(quality["silhouette"], -1.0)
        self.assertLessEqual(quality["silhouette"], 1.0)
        
        stability = evaluate_cluster_stability(X_scaled, algorithm="kmeans", n_clusters=4, n_bootstraps=5)
        self.assertGreaterEqual(stability["mean_ari"], 0.0)
        
        profiles = generate_cluster_profiles(prep["X_imputed"], labels, prep["metadata"])
        self.assertEqual(len(profiles), 4)
        print("✓ Objective 3 Quality Metrics, Stability, & Operational Profiling Test Passed")

    def test_flask_api_endpoints(self):
        client = app.test_client()
        
        res_data = client.get("/api/data")
        self.assertEqual(res_data.status_code, 200)
        
        res_cluster = client.post("/api/cluster", json={"algorithm": "kmeans", "n_clusters": 4})
        self.assertEqual(res_cluster.status_code, 200)
        
        res_pca = client.post("/api/pca", json={"algorithm": "kmeans", "n_clusters": 4})
        self.assertEqual(res_pca.status_code, 200)
        
        res_eval = client.post("/api/evaluate", json={"algorithm": "kmeans", "n_clusters": 4})
        self.assertEqual(res_eval.status_code, 200)
        
        print("✓ Flask REST API Endpoints Integration Test Passed")

if __name__ == "__main__":
    unittest.main()
