"""
Main Pipeline Orchestrator for Urban Bus Route Clustering
Smart India Hackathon (SIH) Grade Unsupervised Machine Learning System

Executes:
1. Data generation & simulation of urban transit telemetry (AVL/GTFS)
2. Data preprocessing & missing value imputation (KNN)
3. Movement & temporal feature engineering
4. Distance metric analysis (Euclidean vs. Manhattan)
5. Multi-algorithm clustering (K-Means++ & Hierarchical Linkages)
6. PCA dimensionality reduction, Scree analysis & biplot
7. Cluster quality validation (Silhouette, Davies-Bouldin, Calinski-Harabasz)
8. Cluster stability testing via bootstrap ARI/NMI perturbation
9. Domain interpretation & transit archetype profiling
10. Exporting publication-grade visualization charts, JSON artifacts, and SIH PPTX deck
"""

import json
import os
import sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend for headless execution
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.cluster.hierarchy import dendrogram

from src.data_generator import generate_synthetic_transit_dataset
from src.preprocessor import TransitPreprocessor
from src.feature_engineering import TransitFeatureEngineer
from src.distance_metrics import DistanceMetricComparator
from src.clustering import TransitClusteringEngine
from src.dimensionality_reduction import TransitDimensionalityReducer
from src.validation import TransitClusterValidator
from src.interpretation import TransitClusterInterpreter
from generate_pitch_deck import create_presentation_deck


def run_pipeline(output_dir: str = ".", target_k: int = 4):
    print("=" * 75)
    print("SMART INDIA HACKATHON: URBAN BUS ROUTE CLUSTERING SYSTEM")
    print("Unsupervised Discovery of Operational Regimes from Traffic Telemetry")
    print("=" * 75)

    data_dir = os.path.join(output_dir, "data")
    reports_dir = os.path.join(output_dir, "reports")
    dashboard_dir = os.path.join(output_dir, "dashboard")
    for d in [data_dir, reports_dir, dashboard_dir]:
        os.makedirs(d, exist_ok=True)

    # ---------------------------------------------------------
    # STEP 1: Data Generation & Ingestion
    # ---------------------------------------------------------
    print("\n[Step 1/9] Generating realistic multi-corridor transit telemetry...")
    raw_observations, routes_meta = generate_synthetic_transit_dataset(num_routes=60, seed=42)
    raw_df = pd.DataFrame(raw_observations)
    raw_csv_path = os.path.join(data_dir, "raw_transit_data.csv")
    raw_df.to_csv(raw_csv_path, index=False)
    print(f"  ✓ Generated {len(raw_df)} observations across {len(routes_meta)} routes.")
    print(f"  ✓ Raw dataset saved to {raw_csv_path}")

    # ---------------------------------------------------------
    # STEP 2: Preprocessing & Missing Value Imputation
    # ---------------------------------------------------------
    print("\n[Step 2/9] Handling missing values & standardizing variables...")
    numeric_impute_cols = [
        "avg_operational_speed_kmh",
        "speed_variability_kmh",
        "congestion_index",
        "stop_dwell_time_min",
        "stop_dwell_time_ratio",
        "acceleration_noise_mps2",
        "schedule_adherence_delay_min"
    ]
    preprocessor = TransitPreprocessor(imputation_strategy="knn", scaling_strategy="standard", n_neighbors=5)
    cleaned_df, impute_stats = preprocessor.fit_impute(raw_df, numeric_impute_cols)
    print(f"  ✓ Imputed {impute_stats['total_missing_cells']} missing sensor cells using KNN-distance weighting.")

    # ---------------------------------------------------------
    # STEP 3: Movement & Temporal Feature Engineering
    # ---------------------------------------------------------
    print("\n[Step 3/9] Constructing temporal and movement transit features...")
    fe = TransitFeatureEngineer()
    segment_df, segment_features = fe.construct_segment_features(cleaned_df)
    route_df, route_features = fe.aggregate_to_route_level(segment_df)
    
    processed_csv_path = os.path.join(data_dir, "processed_route_features.csv")
    route_df.to_csv(processed_csv_path, index=False)
    print(f"  ✓ Engineered {len(route_features)} movement features: {', '.join(route_features)}")
    print(f"  ✓ Aggregated route feature matrix saved to {processed_csv_path}")

    # Standardize route-level features for clustering
    X_scaled, scaled_route_df, scaler_stats = preprocessor.fit_scale(route_df, route_features)

    # ---------------------------------------------------------
    # STEP 4: Euclidean vs Manhattan Distance Comparison
    # ---------------------------------------------------------
    print("\n[Step 4/9] Comparing Euclidean (L2) and Manhattan (L1) distance metrics...")
    dist_comp = DistanceMetricComparator(X_scaled, route_features)
    dist_analysis = dist_comp.analyze_metrics_contrast()
    clustering_suitability = dist_comp.evaluate_clustering_suitability(k=target_k)

    print(f"  ✓ Euclidean Relative Contrast: {dist_analysis['euclidean']['relative_contrast']}")
    print(f"  ✓ Manhattan Relative Contrast: {dist_analysis['manhattan']['relative_contrast']}")
    print(f"  ✓ Pearson Correlation (L1 vs L2): {dist_analysis['correlations']['pearson_linear_correlation']}")
    print(f"  ✓ Silhouette under Euclidean Clustering: {clustering_suitability['euclidean_model']['silhouette_euclidean_eval']}")
    print(f"  ✓ Silhouette under Manhattan Clustering: {clustering_suitability['manhattan_model']['silhouette_manhattan_eval']}")

    # ---------------------------------------------------------
    # STEP 5: Clustering Suite (K-Means & Hierarchical Linkages)
    # ---------------------------------------------------------
    print("\n[Step 5/9] Applying K-Means & Hierarchical Clustering across linkages...")
    engine = TransitClusteringEngine(X_scaled, route_features)
    kmeans_results_df, best_stat_k = engine.evaluate_kmeans_spectrum(k_min=2, k_max=8)
    linkage_eval = engine.evaluate_hierarchical_linkages(k=target_k)

    print(f"  ✓ Statistical optimal K (spectrum sweep): k = {best_stat_k}")
    print(f"  ✓ Domain-grounded operational taxonomy chosen: k = {target_k}")
    print("  ✓ K-Means Spectrum:")
    for _, row in kmeans_results_df.iterrows():
        print(f"     k={int(row['k'])}: Silhouette={row['silhouette_score']}, DB Index={row['davies_bouldin_index']}, Inertia={row['inertia']}")

    print(f"  ✓ Hierarchical Linkage Comparison (k={target_k}):")
    for link, res in linkage_eval.items():
        print(f"     Linkage '{link}': Cophenetic Corr={res['cophenetic_correlation']}, Silhouette={res['silhouette_score']}, DB Index={res['davies_bouldin_index']}")

    # Fit champion K-Means model with target_k
    champion_labels, cluster_centers = engine.get_kmeans_champion(target_k)
    route_df["cluster"] = champion_labels

    # ---------------------------------------------------------
    # STEP 6: Dimensionality Reduction (PCA)
    # ---------------------------------------------------------
    print("\n[Step 6/9] Performing PCA Scree analysis and factor loadings biplot...")
    dim_reducer = TransitDimensionalityReducer(n_components=4)
    X_pca, pca_summary = dim_reducer.fit_transform(X_scaled, route_features)
    
    route_df["pca_1"] = np.round(X_pca[:, 0], 3)
    route_df["pca_2"] = np.round(X_pca[:, 1], 3)
    route_df["pca_3"] = np.round(X_pca[:, 2], 3)

    print(f"  ✓ Cumulative Variance (PC1 + PC2): {pca_summary['total_explained_variance_top2'] * 100:.1f}%")
    print(f"  ✓ Cumulative Variance (Top 3 PCs): {pca_summary['total_explained_variance_top3'] * 100:.1f}%")
    print(f"  ✓ PC1 Dominant Drivers: {', '.join(pca_summary['pc1_dominant_features'])}")
    print(f"  ✓ PC2 Dominant Drivers: {', '.join(pca_summary['pc2_dominant_features'])}")

    # ---------------------------------------------------------
    # STEP 7: Cluster Quality & Stability Validation
    # ---------------------------------------------------------
    print("\n[Step 7/9] Validating cluster quality & stability via bootstrap perturbation...")
    validator = TransitClusterValidator(X_scaled, champion_labels)
    quality_report = validator.compute_quality_metrics()
    stability_report = validator.evaluate_cluster_stability(n_bootstraps=40, subsample_ratio=0.85)

    print(f"  ✓ Overall Silhouette Score: {quality_report['overall_silhouette_score']}")
    print(f"  ✓ Davies-Bouldin Index: {quality_report['davies_bouldin_index']} ({quality_report['interpretation']['davies_bouldin_verdict']})")
    print(f"  ✓ Calinski-Harabasz Index: {quality_report['calinski_harabasz_index']}")
    print(f"  ✓ Bootstrap Stability (ARI Mean ± Std): {stability_report['adjusted_rand_index']['mean']} ± {stability_report['adjusted_rand_index']['std']}")
    print(f"  ✓ Bootstrap Stability (NMI Mean): {stability_report['normalized_mutual_information']['mean']}")
    print(f"  ✓ Stability Verdict: {stability_report['assessment']}")

    # ---------------------------------------------------------
    # STEP 8: Interpretation & Actionable Policy Archetypes
    # ---------------------------------------------------------
    print("\n[Step 8/9] Interpreting traffic patterns and generating municipal policy interventions...")
    interpreter = TransitClusterInterpreter()
    profile_table, cluster_profiles = interpreter.profile_clusters(route_df, route_features, cluster_col="cluster")

    for cid, prof in cluster_profiles.items():
        print(f"\n  ➤ [Cluster {cid}] {prof['archetype_name']}")
        print(f"     Routes Assigned: {prof['route_count']} ({prof['route_percentage']}%)")
        print(f"     Mean Speed: {prof['centroid_metrics']['mean_speed_kmh']} km/h | Congestion Index: {prof['centroid_metrics']['mean_congestion_index']} | Dwell Ratio: {prof['centroid_metrics']['mean_dwell_ratio']}")
        print(f"     Policy Action: {prof['policy_recommendation']}")

    # Attach archetype info to route_df
    route_df["archetype_name"] = route_df["cluster"].map(lambda c: cluster_profiles[c]["archetype_name"])
    route_df["archetype_color"] = route_df["cluster"].map(lambda c: cluster_profiles[c]["color"])

    # ---------------------------------------------------------
    # STEP 9: Generate Publication Plots, Artifacts & PPTX
    # ---------------------------------------------------------
    print("\n[Step 9/9] Generating analytical plots, dashboard payload, and SIH presentation...")
    generate_visualizations(
        reports_dir=reports_dir,
        kmeans_results=kmeans_results_df,
        linkage_eval=linkage_eval,
        linkage_matrices=engine.linkage_matrices,
        X_scaled=X_scaled,
        X_pca=X_pca,
        labels=champion_labels,
        cluster_profiles=cluster_profiles,
        pca_summary=pca_summary,
        dist_analysis=dist_analysis
    )

    # Save Dashboard Payload
    dashboard_payload = {
        "metadata": {
            "title": "Unsupervised Clustering of Urban Bus Routes Using Traffic Patterns",
            "hackathon": "Smart India Hackathon (SIH)",
            "num_routes": len(route_df),
            "num_observations": len(raw_df),
            "optimal_k": target_k,
            "statistical_best_k": best_stat_k
        },
        "quality_metrics": quality_report,
        "stability_metrics": stability_report,
        "distance_comparison": {
            "analysis": dist_analysis,
            "suitability": clustering_suitability
        },
        "pca_summary": pca_summary,
        "cluster_profiles": cluster_profiles,
        "kmeans_spectrum": kmeans_results_df.to_dict(orient="records"),
        "linkage_comparison": {k: {m: v for m, v in val.items() if m != "labels"} for k, val in linkage_eval.items()},
        "routes": []
    }

    # Add routes with GIS coordinates
    for idx, r_row in route_df.iterrows():
        r_meta = next((r for r in routes_meta if r["route_id"] == r_row["route_id"]), None)
        dashboard_payload["routes"].append({
            "route_id": r_row["route_id"],
            "route_name": r_row["route_name"],
            "corridor_type": r_row["corridor_archetype"],
            "cluster": int(r_row["cluster"]),
            "archetype_name": r_row["archetype_name"],
            "color": r_row["archetype_color"],
            "length_km": float(r_row["route_length_km"]),
            "stop_count": int(r_row["stop_count"]),
            "mean_speed_kmh": float(r_row["mean_speed_kmh"]),
            "congestion_index": float(r_row["mean_congestion_index"]),
            "dwell_ratio": float(r_row["mean_dwell_ratio"]),
            "headway_irreg": float(r_row["mean_headway_irregularity"]),
            "accel_noise": float(r_row["mean_accel_noise"]),
            "delay_min": float(r_row["mean_delay_min"]),
            "pca_1": float(r_row["pca_1"]),
            "pca_2": float(r_row["pca_2"]),
            "pca_3": float(r_row["pca_3"]),
            "waypoints": r_meta["waypoints"] if r_meta else []
        })

    dashboard_json_path = os.path.join(dashboard_dir, "dashboard_data.json")
    with open(dashboard_json_path, "w") as f:
        json.dump(dashboard_payload, f, indent=2)
    print(f"  ✓ Web Dashboard JSON payload generated: {dashboard_json_path}")

    dashboard_js_path = os.path.join(dashboard_dir, "dashboard_data.js")
    with open(dashboard_js_path, "w") as f:
        f.write("window.EMBEDDED_DASHBOARD_DATA = ")
        json.dump(dashboard_payload, f, indent=2)
        f.write(";\n")
    print(f"  ✓ Standalone Embedded Dashboard JS payload generated: {dashboard_js_path}")

    # Save reports JSON
    metrics_summary_path = os.path.join(reports_dir, "clustering_metrics.json")
    with open(metrics_summary_path, "w") as f:
        json.dump(dashboard_payload, f, indent=2)

    # Generate PPTX Presentation Deck
    pptx_path = os.path.join(output_dir, "SIH_Urban_Transit_Clustering_Presentation.pptx")
    create_presentation_deck(output_path=pptx_path, metrics_data=dashboard_payload)
    print(f"  ✓ SIH Presentation Deck (.pptx) successfully compiled: {pptx_path}")

    print("\n" + "=" * 75)
    print("PIPELINE EXECUTION COMPLETE! ALL DELIVERABLES GENERATED.")
    print("=" * 75)

    return dashboard_payload


def generate_visualizations(
    reports_dir: str,
    kmeans_results: pd.DataFrame,
    linkage_eval: dict,
    linkage_matrices: dict,
    X_scaled: np.ndarray,
    X_pca: np.ndarray,
    labels: np.ndarray,
    cluster_profiles: dict,
    pca_summary: dict,
    dist_analysis: dict
):
    """Generates high-resolution analytical plots."""
    sns.set_theme(style="whitegrid", palette="muted")
    plt.rcParams.update({"font.sans-serif": "DejaVu Sans", "font.size": 10})

    # Plot 1: Elbow Curve & Silhouette Spectrum
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    ax1.plot(kmeans_results["k"], kmeans_results["inertia"], marker="o", color="#0D9488", linewidth=2.5, markersize=8)
    ax1.set_title("K-Means Elbow Method (Inertia vs. k)", fontsize=13, fontweight="bold")
    ax1.set_xlabel("Number of Clusters (k)")
    ax1.set_ylabel("Inertia (Sum of Squared Distances)")
    ax1.grid(True, linestyle="--", alpha=0.6)

    ax2.plot(kmeans_results["k"], kmeans_results["silhouette_score"], marker="s", color="#3B82F6", linewidth=2.5, label="Silhouette Score")
    ax2.set_title("Cluster Quality: Silhouette vs. Davies-Bouldin", fontsize=13, fontweight="bold")
    ax2.set_xlabel("Number of Clusters (k)")
    ax2.set_ylabel("Silhouette Score (Higher is Better)", color="#3B82F6")
    ax2.tick_params(axis="y", labelcolor="#3B82F6")

    ax2_twin = ax2.twinx()
    ax2_twin.plot(kmeans_results["k"], kmeans_results["davies_bouldin_index"], marker="^", color="#EF4444", linewidth=2.5, linestyle="--", label="Davies-Bouldin Index")
    ax2_twin.set_ylabel("Davies-Bouldin Index (Lower is Better)", color="#EF4444")
    ax2_twin.tick_params(axis="y", labelcolor="#EF4444")
    ax2.grid(True, linestyle="--", alpha=0.6)

    plt.tight_layout()
    fig.savefig(os.path.join(reports_dir, "elbow_and_silhouette_evaluation.png"), dpi=200)
    plt.close()

    # Plot 2: Dendrogram & Linkage Comparison
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    if "ward" in linkage_matrices:
        dendrogram(linkage_matrices["ward"], ax=ax1, truncate_mode="lastp", p=20, color_threshold=10, show_leaf_counts=True)
        ax1.set_title("Hierarchical Clustering Dendrogram (Ward Linkage)", fontsize=13, fontweight="bold")
        ax1.set_xlabel("Cluster / Sample Subsets")
        ax1.set_ylabel("Euclidean Cophenetic Distance")

    link_names = list(linkage_eval.keys())
    coph_scores = [linkage_eval[l]["cophenetic_correlation"] for l in link_names]
    sil_scores = [linkage_eval[l]["silhouette_score"] for l in link_names]

    x = np.arange(len(link_names))
    width = 0.35
    ax2.bar(x - width/2, coph_scores, width, label="Cophenetic Corr", color="#0D9488")
    ax2.bar(x + width/2, sil_scores, width, label="Silhouette Score", color="#3B82F6")
    ax2.set_xticks(x)
    ax2.set_xticklabels([l.capitalize() for l in link_names], fontsize=11, fontweight="bold")
    ax2.set_title("Linkage Strategy Evaluation (Cophenetic vs Silhouette)", fontsize=13, fontweight="bold")
    ax2.set_ylabel("Score")
    ax2.legend()
    ax2.grid(True, linestyle="--", alpha=0.6)

    plt.tight_layout()
    fig.savefig(os.path.join(reports_dir, "hierarchical_dendrogram_and_linkages.png"), dpi=200)
    plt.close()

    # Plot 3: PCA 2D Scatter & Factor Loadings Biplot
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6.5))
    colors = [cluster_profiles[c]["color"] for c in sorted(cluster_profiles.keys())]

    for c in sorted(cluster_profiles.keys()):
        mask = labels == c
        ax1.scatter(
            X_pca[mask, 0],
            X_pca[mask, 1],
            c=cluster_profiles[c]["color"],
            label=f"Cluster {c}: {cluster_profiles[c]['archetype_name'].split('(')[0]}",
            s=70,
            alpha=0.85,
            edgecolors="k",
            linewidth=0.5
        )

    # Overlay biplot loading vectors on ax1
    for feat, vec in list(pca_summary["biplot_vectors"].items())[:6]:
        scale = 3.5
        ax1.arrow(0, 0, vec["pc1_loading"] * scale, vec["pc2_loading"] * scale,
                  color="#1E293B", alpha=0.75, width=0.03, head_width=0.15)
        ax1.text(vec["pc1_loading"] * scale * 1.15, vec["pc2_loading"] * scale * 1.15,
                 feat.replace("_", " "), color="#0F172A", fontsize=9, fontweight="bold")

    ax1.set_title(f"PCA 2D Projection with Biplot Loadings ({pca_summary['total_explained_variance_top2']*100:.1f}% Variance)", fontsize=13, fontweight="bold")
    ax1.set_xlabel(f"PC1: {pca_summary['interpretation_pc1']}")
    ax1.set_ylabel(f"PC2: {pca_summary['interpretation_pc2']}")
    ax1.axhline(0, color="gray", linestyle="--", alpha=0.5)
    ax1.axvline(0, color="gray", linestyle="--", alpha=0.5)
    ax1.legend(loc="upper right", fontsize=8.5)
    ax1.grid(True, linestyle="--", alpha=0.6)

    # Scree Plot
    scree_pcs = [s["component"] for s in pca_summary["scree_data"]]
    scree_vars = [s["explained_variance_ratio"] * 100 for s in pca_summary["scree_data"]]
    scree_cum = [s["cumulative_variance_ratio"] * 100 for s in pca_summary["scree_data"]]

    ax2.bar(scree_pcs, scree_vars, color="#0D9488", alpha=0.8, label="Individual Variance (%)")
    ax2.plot(scree_pcs, scree_cum, marker="o", color="#F59E0B", linewidth=2.5, label="Cumulative Variance (%)")
    for i, v in enumerate(scree_cum):
        ax2.text(i, v + 2, f"{v:.1f}%", ha="center", fontsize=10, fontweight="bold")
    ax2.set_title("PCA Scree Plot & Cumulative Explained Variance", fontsize=13, fontweight="bold")
    ax2.set_ylabel("Variance Explained (%)")
    ax2.set_ylim(0, 110)
    ax2.legend()
    ax2.grid(True, linestyle="--", alpha=0.6)

    plt.tight_layout()
    fig.savefig(os.path.join(reports_dir, "pca_traffic_clusters_biplot.png"), dpi=200)
    plt.close()

    # Plot 4: Distance Metric Comparison (Euclidean vs Manhattan)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))
    euc_stats = dist_analysis["euclidean"]
    man_stats = dist_analysis["manhattan"]

    metrics = ["Mean Distance", "Std Dev", "Max Distance", "Relative Contrast"]
    euc_vals = [euc_stats["mean_distance"], euc_stats["std_distance"], euc_stats["max_distance"], euc_stats["relative_contrast"]]
    man_vals = [man_stats["mean_distance"], man_stats["std_distance"], man_stats["max_distance"], man_stats["relative_contrast"]]

    x = np.arange(len(metrics))
    width = 0.35
    ax1.bar(x - width/2, euc_vals, width, label="Euclidean (L2)", color="#3B82F6")
    ax1.bar(x + width/2, man_vals, width, label="Manhattan (L1)", color="#10B981")
    ax1.set_xticks(x)
    ax1.set_xticklabels(metrics, fontsize=10, fontweight="bold")
    ax1.set_title("Distance Dispersion & Contrast Comparison", fontsize=13, fontweight="bold")
    ax1.set_ylabel("Value")
    ax1.legend()
    ax1.grid(True, linestyle="--", alpha=0.6)

    # Narrative card on ax2
    ax2.axis("off")
    summary_text = (
        "MATHEMATICAL DISTANCE COMPARISON:\n\n"
        f"• Euclidean Metric: {euc_stats['formula']}\n"
        f"  - Relative Contrast: {euc_stats['relative_contrast']}\n"
        f"  - Geometry: Hyperspherical. Best for K-Means sum-of-squares optimization.\n"
        f"  - Vulnerability: Squared penalty makes it sensitive to extreme delay spikes.\n\n"
        f"• Manhattan Metric: {man_stats['formula']}\n"
        f"  - Relative Contrast: {man_stats['relative_contrast']}\n"
        f"  - Geometry: Taxicab L1. Linear penalty prevents outlier domination.\n"
        f"  - Superiority in Transit: Resilient against occasional sensor disruptions.\n\n"
        f"• Metric Correlation:\n"
        f"  - Pearson Correlation: {dist_analysis['correlations']['pearson_linear_correlation']}\n"
        f"  - Spearman Rank Corr: {dist_analysis['correlations']['spearman_rank_correlation']}"
    )
    ax2.text(0.05, 0.5, summary_text, fontsize=11, family="monospace", va="center",
             bbox=dict(boxstyle="round,pad=1.2", facecolor="#F1F5F9", edgecolor="#CBD5E1", alpha=0.9))

    plt.tight_layout()
    fig.savefig(os.path.join(reports_dir, "distance_metric_comparison.png"), dpi=200)
    plt.close()

    print("  ✓ All publication figures successfully generated in reports/ directory.")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Urban Bus Route Clustering System (SIH)")
    parser.add_argument("--k", type=int, default=4, help="Number of clusters (default: 4)")
    parser.add_argument("--output_dir", type=str, default=".", help="Output directory")
    args = parser.parse_args()
    run_pipeline(output_dir=args.output_dir, target_k=args.k)
