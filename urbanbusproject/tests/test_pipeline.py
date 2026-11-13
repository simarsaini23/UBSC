"""
Comprehensive Unit & Integration Tests for Urban Bus Clustering System
Smart India Hackathon (SIH) Grade Validation
"""

import unittest
import numpy as np
import pandas as pd

from src.data_generator import generate_synthetic_transit_dataset
from src.preprocessor import TransitPreprocessor
from src.feature_engineering import TransitFeatureEngineer
from src.distance_metrics import DistanceMetricComparator
from src.clustering import TransitClusteringEngine
from src.dimensionality_reduction import TransitDimensionalityReducer
from src.validation import TransitClusterValidator
from src.interpretation import TransitClusterInterpreter


class TestUrbanTransitClustering(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Generate test dataset once for the test suite."""
        cls.raw_obs, cls.routes_meta = generate_synthetic_transit_dataset(num_routes=24, seed=123)
        cls.raw_df = pd.DataFrame(cls.raw_obs)
        cls.impute_cols = [
            "avg_operational_speed_kmh",
            "speed_variability_kmh",
            "congestion_index",
            "stop_dwell_time_min",
            "stop_dwell_time_ratio",
            "acceleration_noise_mps2",
            "schedule_adherence_delay_min"
        ]

    def test_01_data_generator(self):
        """Verify data generator produces valid observations with expected columns and routes."""
        self.assertGreater(len(self.raw_df), 100)
        self.assertEqual(len(self.routes_meta), 24)
        expected_cols = ["route_id", "time_window", "avg_operational_speed_kmh", "congestion_index"]
        for col in expected_cols:
            self.assertIn(col, self.raw_df.columns)

    def test_02_preprocessor_imputation(self):
        """Verify KNN imputation eliminates all missing values."""
        preprocessor = TransitPreprocessor(imputation_strategy="knn", n_neighbors=3)
        cleaned_df, stats = preprocessor.fit_impute(self.raw_df, self.impute_cols)
        self.assertEqual(cleaned_df[self.impute_cols].isnull().sum().sum(), 0)
        self.assertGreaterEqual(stats["total_missing_cells"], 0)

    def test_03_feature_engineering(self):
        """Verify temporal and movement feature engineering."""
        preprocessor = TransitPreprocessor(imputation_strategy="knn", n_neighbors=3)
        cleaned_df, _ = preprocessor.fit_impute(self.raw_df, self.impute_cols)
        
        fe = TransitFeatureEngineer()
        seg_df, seg_cols = fe.construct_segment_features(cleaned_df)
        self.assertIn("speed_cv", seg_cols)
        self.assertIn("headway_irregularity", seg_cols)

        route_df, route_cols = fe.aggregate_to_route_level(seg_df)
        self.assertEqual(len(route_df), 24)
        self.assertIn("mean_speed_kmh", route_cols)
        self.assertIn("peak_vulnerability_ratio", route_cols)
        self.assertFalse(route_df[route_cols].isnull().any().any())

    def test_04_distance_metrics(self):
        """Verify Euclidean vs Manhattan distance metrics calculations."""
        preprocessor = TransitPreprocessor(imputation_strategy="knn", n_neighbors=3)
        cleaned_df, _ = preprocessor.fit_impute(self.raw_df, self.impute_cols)
        fe = TransitFeatureEngineer()
        seg_df, _ = fe.construct_segment_features(cleaned_df)
        route_df, route_cols = fe.aggregate_to_route_level(seg_df)
        X_scaled, _, _ = preprocessor.fit_scale(route_df, route_cols)

        comparator = DistanceMetricComparator(X_scaled, route_cols)
        dist_analysis = comparator.analyze_metrics_contrast()
        self.assertIn("euclidean", dist_analysis)
        self.assertIn("manhattan", dist_analysis)
        self.assertGreater(dist_analysis["euclidean"]["relative_contrast"], 0)
        self.assertGreater(dist_analysis["manhattan"]["relative_contrast"], 0)
        self.assertGreater(dist_analysis["correlations"]["pearson_linear_correlation"], 0.8)

    def test_05_clustering_algorithms(self):
        """Verify K-Means and Hierarchical Linkage strategies."""
        preprocessor = TransitPreprocessor(imputation_strategy="knn", n_neighbors=3)
        cleaned_df, _ = preprocessor.fit_impute(self.raw_df, self.impute_cols)
        fe = TransitFeatureEngineer()
        seg_df, _ = fe.construct_segment_features(cleaned_df)
        route_df, route_cols = fe.aggregate_to_route_level(seg_df)
        X_scaled, _, _ = preprocessor.fit_scale(route_df, route_cols)

        engine = TransitClusteringEngine(X_scaled, route_cols)
        kmeans_results, best_k = engine.evaluate_kmeans_spectrum(k_min=2, k_max=4)
        self.assertEqual(len(kmeans_results), 3)

        linkages = engine.evaluate_hierarchical_linkages(k=3)
        for link in ["ward", "complete", "average", "single"]:
            self.assertIn(link, linkages)
            self.assertGreater(linkages[link]["cophenetic_correlation"], 0)

    def test_06_pca_dimensionality_reduction(self):
        """Verify PCA eigenvalues, explained variance, and biplot vectors."""
        preprocessor = TransitPreprocessor(imputation_strategy="knn", n_neighbors=3)
        cleaned_df, _ = preprocessor.fit_impute(self.raw_df, self.impute_cols)
        fe = TransitFeatureEngineer()
        seg_df, _ = fe.construct_segment_features(cleaned_df)
        route_df, route_cols = fe.aggregate_to_route_level(seg_df)
        X_scaled, _, _ = preprocessor.fit_scale(route_df, route_cols)

        reducer = TransitDimensionalityReducer(n_components=3)
        X_pca, summary = reducer.fit_transform(X_scaled, route_cols)
        self.assertEqual(X_pca.shape, (24, 3))
        self.assertGreater(summary["total_explained_variance_top2"], 0.60)
        self.assertEqual(len(summary["scree_data"]), 3)

    def test_07_validation_and_stability(self):
        """Verify Silhouette, Davies-Bouldin, and bootstrap ARI stability."""
        preprocessor = TransitPreprocessor(imputation_strategy="knn", n_neighbors=3)
        cleaned_df, _ = preprocessor.fit_impute(self.raw_df, self.impute_cols)
        fe = TransitFeatureEngineer()
        seg_df, _ = fe.construct_segment_features(cleaned_df)
        route_df, route_cols = fe.aggregate_to_route_level(seg_df)
        X_scaled, _, _ = preprocessor.fit_scale(route_df, route_cols)

        engine = TransitClusteringEngine(X_scaled, route_cols)
        labels, _ = engine.get_kmeans_champion(k=3)

        validator = TransitClusterValidator(X_scaled, labels)
        qual = validator.compute_quality_metrics()
        self.assertIn("overall_silhouette_score", qual)
        self.assertIn("davies_bouldin_index", qual)

        stability = validator.evaluate_cluster_stability(n_bootstraps=10, subsample_ratio=0.8)
        self.assertGreater(stability["adjusted_rand_index"]["mean"], 0.40)


    def test_08_gtfs_ingestion(self):
        """Verify GTFS table parsing and conversion into telemetry schema."""
        from src.gtfs_ingestion import GTFSFeedIngester, convert_gtfs_to_telemetry_schema
        
        # Mock GTFS DataFrames
        routes = pd.DataFrame([{"route_id": "R1"}, {"route_id": "R2"}])
        trips = pd.DataFrame([
            {"route_id": "R1", "trip_id": "T1"},
            {"route_id": "R1", "trip_id": "T2"},
            {"route_id": "R2", "trip_id": "T3"}
        ])
        stop_times = pd.DataFrame([
            {"trip_id": "T1", "stop_sequence": 1, "arrival_time": "08:00:00", "departure_time": "08:00:00"},
            {"trip_id": "T1", "stop_sequence": 10, "arrival_time": "08:45:00", "departure_time": "08:45:00"},
            {"trip_id": "T2", "stop_sequence": 1, "arrival_time": "08:15:00", "departure_time": "08:15:00"},
            {"trip_id": "T2", "stop_sequence": 10, "arrival_time": "09:00:00", "departure_time": "09:00:00"},
            {"trip_id": "T3", "stop_sequence": 1, "arrival_time": "08:00:00", "departure_time": "08:00:00"},
            {"trip_id": "T3", "stop_sequence": 15, "arrival_time": "09:10:00", "departure_time": "09:10:00"}
        ])
        stops = pd.DataFrame([{"stop_id": "S1"}])

        ingester = GTFSFeedIngester()
        ingester.load_gtfs_tables(routes, trips, stop_times, stops)
        features_df = ingester.compute_route_gtfs_features()
        self.assertEqual(len(features_df), 2)
        self.assertIn("scheduled_trip_time_min", features_df.columns)

        telemetry_df = convert_gtfs_to_telemetry_schema(features_df)
        self.assertEqual(len(telemetry_df), 8) # 2 routes * 4 time windows
        self.assertIn("avg_operational_speed_kmh", telemetry_df.columns)


if __name__ == "__main__":
    unittest.main()
