window.EMBEDDED_DASHBOARD_DATA = {
  "metadata": {
    "title": "Unsupervised Clustering of Urban Bus Routes Using Traffic Patterns",
    "hackathon": "Smart India Hackathon (SIH)",
    "num_routes": 60,
    "num_observations": 1200,
    "optimal_k": 4,
    "statistical_best_k": 2
  },
  "quality_metrics": {
    "num_clusters_k": 4,
    "overall_silhouette_score": 0.2599,
    "davies_bouldin_index": 1.4155,
    "calinski_harabasz_index": 41.14,
    "per_cluster_breakdown": {
      "Cluster_0": {
        "count": 13,
        "mean_silhouette": 0.2859,
        "min_silhouette": 0.0818,
        "max_silhouette": 0.4444
      },
      "Cluster_1": {
        "count": 13,
        "mean_silhouette": 0.2485,
        "min_silhouette": 0.1397,
        "max_silhouette": 0.3903
      },
      "Cluster_2": {
        "count": 17,
        "mean_silhouette": 0.3503,
        "min_silhouette": 0.1583,
        "max_silhouette": 0.4908
      },
      "Cluster_3": {
        "count": 17,
        "mean_silhouette": 0.1582,
        "min_silhouette": 0.0192,
        "max_silhouette": 0.315
      }
    },
    "interpretation": {
      "silhouette_verdict": "Reasonable structure with minor boundary overlap",
      "davies_bouldin_verdict": "Good operational separation"
    }
  },
  "stability_metrics": {
    "n_bootstraps": 40,
    "subsample_ratio": 0.85,
    "adjusted_rand_index": {
      "mean": 0.8915,
      "std": 0.0814,
      "min": 0.7424,
      "max": 1.0
    },
    "normalized_mutual_information": {
      "mean": 0.9229,
      "std": 0.0553,
      "min": 0.8207,
      "max": 1.0
    },
    "assessment": "Highly Stable & Robust (>0.75 ARI)"
  },
  "distance_comparison": {
    "analysis": {
      "n_samples": 60,
      "n_features": 10,
      "euclidean": {
        "metric_name": "Euclidean (L2 Norm)",
        "formula": "||x - y||_2 = sqrt(sum((x_i - y_i)^2))",
        "mean_distance": 4.189,
        "std_distance": 1.671,
        "min_distance": 0.52,
        "max_distance": 9.106,
        "relative_contrast": 16.514,
        "variance_ratio": 0.399,
        "geometry": "Hyperspherical (sensitive to squared extreme variations)"
      },
      "manhattan": {
        "metric_name": "Manhattan (L1 Norm / Cityblock)",
        "formula": "||x - y||_1 = sum(|x_i - y_i|)",
        "mean_distance": 11.411,
        "std_distance": 5.343,
        "min_distance": 1.262,
        "max_distance": 26.774,
        "relative_contrast": 20.212,
        "variance_ratio": 0.468,
        "geometry": "Diamond / Taxicab (robust against isolated sensor shocks)"
      },
      "correlations": {
        "pearson_linear_correlation": 0.9793,
        "spearman_rank_correlation": 0.9774
      }
    },
    "suitability": {
      "tested_k": 4,
      "euclidean_model": {
        "silhouette_euclidean_eval": 0.333,
        "silhouette_manhattan_eval": 0.366,
        "cluster_counts": {
          "0": 30,
          "1": 27,
          "3": 2,
          "2": 1
        }
      },
      "manhattan_model": {
        "silhouette_euclidean_eval": 0.333,
        "silhouette_manhattan_eval": 0.366,
        "cluster_counts": {
          "1": 30,
          "0": 27,
          "3": 2,
          "2": 1
        }
      },
      "recommendation": "Manhattan distance is superior for outlier-resilient transit telemetry where localized congestion spikes can artificially distort squared Euclidean distances. Euclidean distance remains ideal when optimizing intra-cluster variance under K-Means."
    }
  },
  "pca_summary": {
    "scree_data": [
      {
        "component": "PC1",
        "eigenvalue": 6.401,
        "explained_variance_ratio": 0.6294,
        "cumulative_variance_ratio": 0.6294
      },
      {
        "component": "PC2",
        "eigenvalue": 1.7626,
        "explained_variance_ratio": 0.1733,
        "cumulative_variance_ratio": 0.8028
      },
      {
        "component": "PC3",
        "eigenvalue": 0.9485,
        "explained_variance_ratio": 0.0933,
        "cumulative_variance_ratio": 0.896
      },
      {
        "component": "PC4",
        "eigenvalue": 0.481,
        "explained_variance_ratio": 0.0473,
        "cumulative_variance_ratio": 0.9433
      }
    ],
    "biplot_vectors": {
      "mean_speed_kmh": {
        "pc1_loading": -0.9849,
        "pc2_loading": -0.0158,
        "magnitude": 0.985
      },
      "speed_cv": {
        "pc1_loading": 0.2719,
        "pc2_loading": 0.5818,
        "magnitude": 0.6422
      },
      "mean_congestion_index": {
        "pc1_loading": 0.0361,
        "pc2_loading": 0.9344,
        "magnitude": 0.9351
      },
      "mean_dwell_ratio": {
        "pc1_loading": 1.0009,
        "pc2_loading": -0.0499,
        "magnitude": 1.0022
      },
      "mean_headway_irregularity": {
        "pc1_loading": 0.8633,
        "pc2_loading": 0.0153,
        "magnitude": 0.8635
      },
      "mean_accel_noise": {
        "pc1_loading": 0.9933,
        "pc2_loading": -0.0684,
        "magnitude": 0.9957
      },
      "mean_turbulence": {
        "pc1_loading": 0.9962,
        "pc2_loading": -0.0321,
        "magnitude": 0.9967
      },
      "mean_delay_min": {
        "pc1_loading": 0.8164,
        "pc2_loading": 0.1663,
        "magnitude": 0.8332
      },
      "peak_vulnerability_ratio": {
        "pc1_loading": -0.1395,
        "pc2_loading": 0.7088,
        "magnitude": 0.7224
      },
      "stop_density_per_km": {
        "pc1_loading": 0.9714,
        "pc2_loading": -0.1109,
        "magnitude": 0.9777
      }
    },
    "total_explained_variance_top2": 0.8028,
    "total_explained_variance_top3": 0.896,
    "pc1_dominant_features": [
      "mean_dwell_ratio",
      "mean_turbulence",
      "mean_accel_noise"
    ],
    "pc2_dominant_features": [
      "mean_congestion_index",
      "peak_vulnerability_ratio",
      "speed_cv"
    ],
    "interpretation_pc1": "Traffic Friction & Impedance (heavily loaded by mean_dwell_ratio, mean_turbulence, mean_accel_noise)",
    "interpretation_pc2": "Operational Regularity & Stop Density (heavily loaded by mean_congestion_index, peak_vulnerability_ratio, speed_cv)"
  },
  "cluster_profiles": {
    "2": {
      "cluster_id": 2,
      "archetype_name": "Radial Express Arterial (High Speed & Smooth Flow)",
      "color": "#10B981",
      "severity_level": "Low Friction",
      "route_count": 17,
      "route_percentage": 28.3,
      "centroid_metrics": {
        "mean_speed_kmh": 23.928,
        "speed_cv": 0.412,
        "mean_congestion_index": 1.533,
        "mean_dwell_ratio": 0.207,
        "mean_headway_irregularity": 0.316,
        "mean_accel_noise": 0.767,
        "mean_turbulence": 1.096,
        "mean_delay_min": 23.491,
        "peak_vulnerability_ratio": 1.627,
        "stop_density_per_km": 1.12
      },
      "radar_metrics": {
        "Speed": 0.75,
        "Congestion": 0.44,
        "Stop Dwell": 0.46,
        "Headway Variance": 0.53,
        "Accel Turbulence": 0.38,
        "Schedule Delay": 1.0
      },
      "policy_recommendation": "High-speed commuter corridor. Ideal candidate for Electric Bus (EV) fleet allocation due to consistent speeds and minimal stop-and-go energy loss. Maintain express timetable.",
      "routes_assigned": [
        "R-002",
        "R-010",
        "R-015",
        "R-018",
        "R-022",
        "R-023",
        "R-026",
        "R-030",
        "R-034",
        "R-038",
        "R-039",
        "R-042",
        "R-043",
        "R-050",
        "R-051",
        "R-054",
        "R-059"
      ]
    },
    "0": {
      "cluster_id": 0,
      "archetype_name": "Suburban Feeder / Metro Link (Predictable Steady Flow)",
      "color": "#3B82F6",
      "severity_level": "Moderate Friction",
      "route_count": 13,
      "route_percentage": 21.7,
      "centroid_metrics": {
        "mean_speed_kmh": 19.761,
        "speed_cv": 0.433,
        "mean_congestion_index": 1.734,
        "mean_dwell_ratio": 0.248,
        "mean_headway_irregularity": 0.351,
        "mean_accel_noise": 0.929,
        "mean_turbulence": 1.347,
        "mean_delay_min": 38.041,
        "peak_vulnerability_ratio": 1.945,
        "stop_density_per_km": 1.339
      },
      "radar_metrics": {
        "Speed": 0.62,
        "Congestion": 0.61,
        "Stop Dwell": 0.55,
        "Headway Variance": 0.58,
        "Accel Turbulence": 0.46,
        "Schedule Delay": 1.0
      },
      "policy_recommendation": "Reliable feeder route. Synchronize dispatch headways with adjacent Metro rail arrival times and optimize timetable spacing to eliminate bus bunching.",
      "routes_assigned": [
        "R-003",
        "R-006",
        "R-007",
        "R-011",
        "R-014",
        "R-019",
        "R-027",
        "R-031",
        "R-035",
        "R-046",
        "R-047",
        "R-055",
        "R-058"
      ]
    },
    "3": {
      "cluster_id": 3,
      "archetype_name": "Congested Urban Core (Heavy Impedance Chokepoint)",
      "color": "#EF4444",
      "severity_level": "Critical Friction",
      "route_count": 17,
      "route_percentage": 28.3,
      "centroid_metrics": {
        "mean_speed_kmh": 9.393,
        "speed_cv": 0.407,
        "mean_congestion_index": 1.545,
        "mean_dwell_ratio": 0.468,
        "mean_headway_irregularity": 0.486,
        "mean_accel_noise": 1.868,
        "mean_turbulence": 2.651,
        "mean_delay_min": 58.083,
        "peak_vulnerability_ratio": 1.67,
        "stop_density_per_km": 2.918
      },
      "radar_metrics": {
        "Speed": 0.29,
        "Congestion": 0.45,
        "Stop Dwell": 1.0,
        "Headway Variance": 0.81,
        "Accel Turbulence": 0.93,
        "Schedule Delay": 1.0
      },
      "policy_recommendation": "Severe bottleneck corridor. Implement Transit Signal Priority (TSP) at key junctions, demarcate dedicated bus lanes, and pilot off-board fare ticketing to slash boarding dwell.",
      "routes_assigned": [
        "R-001",
        "R-004",
        "R-012",
        "R-013",
        "R-017",
        "R-020",
        "R-024",
        "R-025",
        "R-033",
        "R-037",
        "R-041",
        "R-044",
        "R-045",
        "R-049",
        "R-052",
        "R-053",
        "R-057"
      ]
    },
    "1": {
      "cluster_id": 1,
      "archetype_name": "High-Friction Historic / Commercial Belt (Stop-and-Go)",
      "color": "#F59E0B",
      "severity_level": "High Turbulence",
      "route_count": 13,
      "route_percentage": 21.7,
      "centroid_metrics": {
        "mean_speed_kmh": 7.624,
        "speed_cv": 0.455,
        "mean_congestion_index": 1.678,
        "mean_dwell_ratio": 0.528,
        "mean_headway_irregularity": 0.506,
        "mean_accel_noise": 2.14,
        "mean_turbulence": 3.134,
        "mean_delay_min": 92.745,
        "peak_vulnerability_ratio": 1.744,
        "stop_density_per_km": 3.154
      },
      "radar_metrics": {
        "Speed": 0.24,
        "Congestion": 0.56,
        "Stop Dwell": 1.0,
        "Headway Variance": 0.84,
        "Accel Turbulence": 1.0,
        "Schedule Delay": 1.0
      },
      "policy_recommendation": "Extreme stop-and-go turbulence. Enforce curbside parking restrictions, consolidate closely spaced bus stops, and evaluate mini-bus fleet rightsizing.",
      "routes_assigned": [
        "R-005",
        "R-008",
        "R-009",
        "R-016",
        "R-021",
        "R-028",
        "R-029",
        "R-032",
        "R-036",
        "R-040",
        "R-048",
        "R-056",
        "R-060"
      ]
    }
  },
  "kmeans_spectrum": [
    {
      "k": 2,
      "inertia": 273.02,
      "silhouette_score": 0.4557,
      "davies_bouldin_index": 0.8736,
      "calinski_harabasz_index": 69.46
    },
    {
      "k": 3,
      "inertia": 225.3,
      "silhouette_score": 0.3489,
      "davies_bouldin_index": 1.0718,
      "calinski_harabasz_index": 47.4
    },
    {
      "k": 4,
      "inertia": 187.26,
      "silhouette_score": 0.2599,
      "davies_bouldin_index": 1.4155,
      "calinski_harabasz_index": 41.14
    },
    {
      "k": 5,
      "inertia": 167.76,
      "silhouette_score": 0.265,
      "davies_bouldin_index": 1.3082,
      "calinski_harabasz_index": 35.43
    },
    {
      "k": 6,
      "inertia": 154.25,
      "silhouette_score": 0.2619,
      "davies_bouldin_index": 1.1855,
      "calinski_harabasz_index": 31.21
    },
    {
      "k": 7,
      "inertia": 142.92,
      "silhouette_score": 0.2305,
      "davies_bouldin_index": 1.195,
      "calinski_harabasz_index": 28.25
    },
    {
      "k": 8,
      "inertia": 123.41,
      "silhouette_score": 0.2566,
      "davies_bouldin_index": 1.1481,
      "calinski_harabasz_index": 28.69
    }
  ],
  "linkage_comparison": {
    "ward": {
      "linkage_method": "ward",
      "cophenetic_correlation": 0.7621,
      "silhouette_score": 0.3202,
      "davies_bouldin_index": 1.0751,
      "calinski_harabasz_index": 35.79,
      "cluster_distribution": {
        "0": 29,
        "2": 18,
        "3": 10,
        "1": 3
      },
      "characteristics": "Minimizes the total within-cluster variance. Produces balanced, compact, spherical clusters."
    },
    "complete": {
      "linkage_method": "complete",
      "cophenetic_correlation": 0.6685,
      "silhouette_score": 0.2121,
      "davies_bouldin_index": 1.444,
      "calinski_harabasz_index": 37.2,
      "cluster_distribution": {
        "1": 21,
        "2": 17,
        "0": 13,
        "3": 9
      },
      "characteristics": "Finds clusters based on maximum pairwise distance. Favors compact clusters of equal diameter."
    },
    "average": {
      "linkage_method": "average",
      "cophenetic_correlation": 0.819,
      "silhouette_score": 0.3333,
      "davies_bouldin_index": 0.8487,
      "calinski_harabasz_index": 28.97,
      "cluster_distribution": {
        "0": 30,
        "1": 27,
        "3": 2,
        "2": 1
      },
      "characteristics": "Computes average distance between all pairs. Balanced compromise between Ward and Single."
    },
    "single": {
      "linkage_method": "single",
      "cophenetic_correlation": 0.7654,
      "silhouette_score": -0.0329,
      "davies_bouldin_index": 0.8712,
      "calinski_harabasz_index": 1.71,
      "cluster_distribution": {
        "0": 57,
        "2": 1,
        "3": 1,
        "1": 1
      },
      "characteristics": "Computes minimum pairwise distance. Highly prone to chaining; identifies non-spherical serpentine shapes."
    }
  },
  "routes": [
    {
      "route_id": "R-001",
      "route_name": "Route 1 (CBD_Core_Trunk)",
      "corridor_type": "CBD_Core_Trunk",
      "cluster": 3,
      "archetype_name": "Congested Urban Core (Heavy Impedance Chokepoint)",
      "color": "#EF4444",
      "length_km": 25.53,
      "stop_count": 61,
      "mean_speed_kmh": 10.036,
      "congestion_index": 1.547,
      "dwell_ratio": 0.443,
      "headway_irreg": 0.463,
      "accel_noise": 1.641,
      "delay_min": 60.52,
      "pca_1": 1.259,
      "pca_2": -1.42,
      "pca_3": 1.145,
      "waypoints": [
        [
          28.65873,
          77.21956
        ],
        [
          28.66309,
          77.22787
        ],
        [
          28.66656,
          77.23518
        ],
        [
          28.67198,
          77.23804
        ],
        [
          28.68042,
          77.23399
        ],
        [
          28.68919,
          77.22276
        ]
      ]
    },
    {
      "route_id": "R-002",
      "route_name": "Route 2 (Radial_Express_Arterial)",
      "corridor_type": "Radial_Express_Arterial",
      "cluster": 2,
      "archetype_name": "Radial Express Arterial (High Speed & Smooth Flow)",
      "color": "#10B981",
      "length_km": 17.88,
      "stop_count": 16,
      "mean_speed_kmh": 26.711,
      "congestion_index": 1.539,
      "dwell_ratio": 0.165,
      "headway_irreg": 0.286,
      "accel_noise": 0.667,
      "delay_min": 17.71,
      "pca_1": -3.4,
      "pca_2": -0.741,
      "pca_3": 0.11,
      "waypoints": [
        [
          28.65193,
          77.22104
        ],
        [
          28.65423,
          77.22753
        ],
        [
          28.65599,
          77.23309
        ],
        [
          28.65956,
          77.23548
        ],
        [
          28.66586,
          77.23307
        ],
        [
          28.67292,
          77.2255
        ]
      ]
    },
    {
      "route_id": "R-003",
      "route_name": "Route 3 (Suburban_Feeder_Loop)",
      "corridor_type": "Suburban_Feeder_Loop",
      "cluster": 0,
      "archetype_name": "Suburban Feeder / Metro Link (Predictable Steady Flow)",
      "color": "#3B82F6",
      "length_km": 21.91,
      "stop_count": 31,
      "mean_speed_kmh": 18.522,
      "congestion_index": 1.629,
      "dwell_ratio": 0.263,
      "headway_irreg": 0.288,
      "accel_noise": 0.972,
      "delay_min": 33.785,
      "pca_1": -1.961,
      "pca_2": 0.636,
      "pca_3": -0.748,
      "waypoints": [
        [
          28.67439,
          77.23064
        ],
        [
          28.67445,
          77.24299
        ],
        [
          28.67423,
          77.2523
        ],
        [
          28.67827,
          77.25566
        ],
        [
          28.68791,
          77.25123
        ],
        [
          28.6994,
          77.23876
        ]
      ]
    },
    {
      "route_id": "R-004",
      "route_name": "Route 4 (High_Friction_Historic_Belt)",
      "corridor_type": "High_Friction_Historic_Belt",
      "cluster": 3,
      "archetype_name": "Congested Urban Core (Heavy Impedance Chokepoint)",
      "color": "#EF4444",
      "length_km": 26.25,
      "stop_count": 98,
      "mean_speed_kmh": 8.8,
      "congestion_index": 1.26,
      "dwell_ratio": 0.475,
      "headway_irreg": 0.461,
      "accel_noise": 2.032,
      "delay_min": 46.61,
      "pca_1": 1.883,
      "pca_2": -3.008,
      "pca_3": -1.796,
      "waypoints": [
        [
          28.65876,
          77.22884
        ],
        [
          28.66018,
          77.23869
        ],
        [
          28.66109,
          77.24712
        ],
        [
          28.66548,
          77.25164
        ],
        [
          28.67518,
          77.25018
        ],
        [
          28.68754,
          77.24165
        ]
      ]
    },
    {
      "route_id": "R-005",
      "route_name": "Route 5 (CBD_Core_Trunk)",
      "corridor_type": "CBD_Core_Trunk",
      "cluster": 1,
      "archetype_name": "High-Friction Historic / Commercial Belt (Stop-and-Go)",
      "color": "#F59E0B",
      "length_km": 26.87,
      "stop_count": 76,
      "mean_speed_kmh": 9.396,
      "congestion_index": 1.799,
      "dwell_ratio": 0.482,
      "headway_irreg": 0.489,
      "accel_noise": 1.722,
      "delay_min": 92.095,
      "pca_1": 2.111,
      "pca_2": 1.278,
      "pca_3": 0.28,
      "waypoints": [
        [
          28.66738,
          77.23742
        ],
        [
          28.66625,
          77.24964
        ],
        [
          28.6651,
          77.25939
        ],
        [
          28.66909,
          77.26446
        ],
        [
          28.68029,
          77.26295
        ],
        [
          28.6953,
          77.25354
        ]
      ]
    },
    {
      "route_id": "R-006",
      "route_name": "Route 6 (Radial_Express_Arterial)",
      "corridor_type": "Radial_Express_Arterial",
      "cluster": 0,
      "archetype_name": "Suburban Feeder / Metro Link (Predictable Steady Flow)",
      "color": "#3B82F6",
      "length_km": 30.81,
      "stop_count": 31,
      "mean_speed_kmh": 25.156,
      "congestion_index": 1.695,
      "dwell_ratio": 0.166,
      "headway_irreg": 0.343,
      "accel_noise": 0.721,
      "delay_min": 37.52,
      "pca_1": -2.827,
      "pca_2": 1.409,
      "pca_3": -0.78,
      "waypoints": [
        [
          28.64913,
          77.22951
        ],
        [
          28.65047,
          77.23888
        ],
        [
          28.651,
          77.24765
        ],
        [
          28.65494,
          77.25391
        ],
        [
          28.66488,
          77.25575
        ],
        [
          28.67904,
          77.25124
        ]
      ]
    },
    {
      "route_id": "R-007",
      "route_name": "Route 7 (Suburban_Feeder_Loop)",
      "corridor_type": "Suburban_Feeder_Loop",
      "cluster": 0,
      "archetype_name": "Suburban Feeder / Metro Link (Predictable Steady Flow)",
      "color": "#3B82F6",
      "length_km": 12.91,
      "stop_count": 18,
      "mean_speed_kmh": 18.082,
      "congestion_index": 1.699,
      "dwell_ratio": 0.295,
      "headway_irreg": 0.326,
      "accel_noise": 1.063,
      "delay_min": 23.12,
      "pca_1": -1.52,
      "pca_2": 1.286,
      "pca_3": 0.701,
      "waypoints": [
        [
          28.65253,
          77.23564
        ],
        [
          28.6493,
          77.24257
        ],
        [
          28.64673,
          77.24766
        ],
        [
          28.6481,
          77.25044
        ],
        [
          28.65457,
          77.25023
        ],
        [
          28.66405,
          77.24601
        ]
      ]
    },
    {
      "route_id": "R-008",
      "route_name": "Route 8 (High_Friction_Historic_Belt)",
      "corridor_type": "High_Friction_Historic_Belt",
      "cluster": 1,
      "archetype_name": "High-Friction Historic / Commercial Belt (Stop-and-Go)",
      "color": "#F59E0B",
      "length_km": 11.13,
      "stop_count": 37,
      "mean_speed_kmh": 6.525,
      "congestion_index": 1.746,
      "dwell_ratio": 0.548,
      "headway_irreg": 0.561,
      "accel_noise": 2.411,
      "delay_min": 52.66,
      "pca_1": 3.205,
      "pca_2": 0.91,
      "pca_3": -0.685,
      "waypoints": [
        [
          28.67066,
          77.26019
        ],
        [
          28.66072,
          77.27046
        ],
        [
          28.65355,
          77.27663
        ],
        [
          28.65448,
          77.27914
        ],
        [
          28.66455,
          77.2775
        ],
        [
          28.67959,
          77.27011
        ]
      ]
    },
    {
      "route_id": "R-009",
      "route_name": "Route 9 (CBD_Core_Trunk)",
      "corridor_type": "CBD_Core_Trunk",
      "cluster": 1,
      "archetype_name": "High-Friction Historic / Commercial Belt (Stop-and-Go)",
      "color": "#F59E0B",
      "length_km": 16.32,
      "stop_count": 43,
      "mean_speed_kmh": 7.788,
      "congestion_index": 2.075,
      "dwell_ratio": 0.501,
      "headway_irreg": 0.575,
      "accel_noise": 1.902,
      "delay_min": 75.055,
      "pca_1": 2.665,
      "pca_2": 4.004,
      "pca_3": 0.748,
      "waypoints": [
        [
          28.64761,
          77.23887
        ],
        [
          28.6435,
          77.24563
        ],
        [
          28.64015,
          77.25086
        ],
        [
          28.64111,
          77.25466
        ],
        [
          28.648,
          77.25648
        ],
        [
          28.65912,
          77.25471
        ]
      ]
    },
    {
      "route_id": "R-010",
      "route_name": "Route 10 (Radial_Express_Arterial)",
      "corridor_type": "Radial_Express_Arterial",
      "cluster": 2,
      "archetype_name": "Radial Express Arterial (High Speed & Smooth Flow)",
      "color": "#10B981",
      "length_km": 16.29,
      "stop_count": 14,
      "mean_speed_kmh": 26.863,
      "congestion_index": 1.528,
      "dwell_ratio": 0.169,
      "headway_irreg": 0.329,
      "accel_noise": 0.626,
      "delay_min": 15.925,
      "pca_1": -3.267,
      "pca_2": -0.515,
      "pca_3": 0.566,
      "waypoints": [
        [
          28.64503,
          77.24013
        ],
        [
          28.64031,
          77.24639
        ],
        [
          28.63648,
          77.25122
        ],
        [
          28.63703,
          77.25509
        ],
        [
          28.64365,
          77.25763
        ],
        [
          28.6548,
          77.25706
        ]
      ]
    },
    {
      "route_id": "R-011",
      "route_name": "Route 11 (Suburban_Feeder_Loop)",
      "corridor_type": "Suburban_Feeder_Loop",
      "cluster": 0,
      "archetype_name": "Suburban Feeder / Metro Link (Predictable Steady Flow)",
      "color": "#3B82F6",
      "length_km": 28.36,
      "stop_count": 41,
      "mean_speed_kmh": 16.7,
      "congestion_index": 1.772,
      "dwell_ratio": 0.279,
      "headway_irreg": 0.447,
      "accel_noise": 1.063,
      "delay_min": 52.025,
      "pca_1": -0.617,
      "pca_2": 2.371,
      "pca_3": 1.433,
      "waypoints": [
        [
          28.6416,
          77.23939
        ],
        [
          28.63728,
          77.24781
        ],
        [
          28.63298,
          77.25512
        ],
        [
          28.63324,
          77.26192
        ],
        [
          28.64101,
          77.26788
        ],
        [
          28.65544,
          77.27048
        ]
      ]
    },
    {
      "route_id": "R-012",
      "route_name": "Route 12 (High_Friction_Historic_Belt)",
      "corridor_type": "High_Friction_Historic_Belt",
      "cluster": 3,
      "archetype_name": "Congested Urban Core (Heavy Impedance Chokepoint)",
      "color": "#EF4444",
      "length_km": 22.5,
      "stop_count": 66,
      "mean_speed_kmh": 7.541,
      "congestion_index": 1.451,
      "dwell_ratio": 0.525,
      "headway_irreg": 0.555,
      "accel_noise": 2.214,
      "delay_min": 64.875,
      "pca_1": 2.755,
      "pca_2": -2.005,
      "pca_3": -0.045,
      "waypoints": [
        [
          28.64809,
          77.26774
        ],
        [
          28.63616,
          77.27559
        ],
        [
          28.62723,
          77.28103
        ],
        [
          28.62687,
          77.28642
        ],
        [
          28.63744,
          77.29174
        ],
        [
          28.65643,
          77.29342
        ]
      ]
    },
    {
      "route_id": "R-013",
      "route_name": "Route 13 (CBD_Core_Trunk)",
      "corridor_type": "CBD_Core_Trunk",
      "cluster": 3,
      "archetype_name": "Congested Urban Core (Heavy Impedance Chokepoint)",
      "color": "#EF4444",
      "length_km": 19.28,
      "stop_count": 61,
      "mean_speed_kmh": 12.12,
      "congestion_index": 1.391,
      "dwell_ratio": 0.403,
      "headway_irreg": 0.479,
      "accel_noise": 1.572,
      "delay_min": 35.63,
      "pca_1": 0.77,
      "pca_2": -0.924,
      "pca_3": -1.444,
      "waypoints": [
        [
          28.63832,
          77.24879
        ],
        [
          28.63054,
          77.25412
        ],
        [
          28.62434,
          77.25814
        ],
        [
          28.62356,
          77.2627
        ],
        [
          28.63018,
          77.26799
        ],
        [
          28.64313,
          77.27142
        ]
      ]
    },
    {
      "route_id": "R-014",
      "route_name": "Route 14 (Radial_Express_Arterial)",
      "corridor_type": "Radial_Express_Arterial",
      "cluster": 0,
      "archetype_name": "Suburban Feeder / Metro Link (Predictable Steady Flow)",
      "color": "#3B82F6",
      "length_km": 19.25,
      "stop_count": 19,
      "mean_speed_kmh": 23.341,
      "congestion_index": 1.892,
      "dwell_ratio": 0.178,
      "headway_irreg": 0.333,
      "accel_noise": 0.734,
      "delay_min": 29.695,
      "pca_1": -2.875,
      "pca_2": 2.488,
      "pca_3": -1.468,
      "waypoints": [
        [
          28.6339,
          77.23957
        ],
        [
          28.62791,
          77.24408
        ],
        [
          28.62273,
          77.24771
        ],
        [
          28.62147,
          77.25216
        ],
        [
          28.62611,
          77.25782
        ],
        [
          28.63632,
          77.26254
        ]
      ]
    },
    {
      "route_id": "R-015",
      "route_name": "Route 15 (Suburban_Feeder_Loop)",
      "corridor_type": "Suburban_Feeder_Loop",
      "cluster": 2,
      "archetype_name": "Radial Express Arterial (High Speed & Smooth Flow)",
      "color": "#10B981",
      "length_km": 31.04,
      "stop_count": 51,
      "mean_speed_kmh": 20.072,
      "congestion_index": 1.458,
      "dwell_ratio": 0.283,
      "headway_irreg": 0.352,
      "accel_noise": 0.897,
      "delay_min": 34.295,
      "pca_1": -1.545,
      "pca_2": -0.883,
      "pca_3": 1.338,
      "waypoints": [
        [
          28.6315,
          77.24791
        ],
        [
          28.62249,
          77.2543
        ],
        [
          28.61438,
          77.25951
        ],
        [
          28.61161,
          77.26643
        ],
        [
          28.61729,
          77.27603
        ],
        [
          28.6315,
          77.28516
        ]
      ]
    },
    {
      "route_id": "R-016",
      "route_name": "Route 16 (High_Friction_Historic_Belt)",
      "corridor_type": "High_Friction_Historic_Belt",
      "cluster": 1,
      "archetype_name": "High-Friction Historic / Commercial Belt (Stop-and-Go)",
      "color": "#F59E0B",
      "length_km": 26.54,
      "stop_count": 81,
      "mean_speed_kmh": 6.877,
      "congestion_index": 1.607,
      "dwell_ratio": 0.52,
      "headway_irreg": 0.497,
      "accel_noise": 2.293,
      "delay_min": 99.13,
      "pca_1": 3.197,
      "pca_2": 0.204,
      "pca_3": -0.288,
      "waypoints": [
        [
          28.62911,
          77.2394
        ],
        [
          28.62177,
          77.24422
        ],
        [
          28.61492,
          77.24816
        ],
        [
          28.61195,
          77.25379
        ],
        [
          28.6154,
          77.26224
        ],
        [
          28.62579,
          77.27107
        ]
      ]
    },
    {
      "route_id": "R-017",
      "route_name": "Route 17 (CBD_Core_Trunk)",
      "corridor_type": "CBD_Core_Trunk",
      "cluster": 3,
      "archetype_name": "Congested Urban Core (Heavy Impedance Chokepoint)",
      "color": "#EF4444",
      "length_km": 25.39,
      "stop_count": 66,
      "mean_speed_kmh": 10.292,
      "congestion_index": 1.526,
      "dwell_ratio": 0.452,
      "headway_irreg": 0.476,
      "accel_noise": 1.664,
      "delay_min": 59.395,
      "pca_1": 1.359,
      "pca_2": -1.622,
      "pca_3": 0.725,
      "waypoints": [
        [
          28.62144,
          77.26403
        ],
        [
          28.60807,
          77.26588
        ],
        [
          28.59781,
          77.26704
        ],
        [
          28.59442,
          77.2721
        ],
        [
          28.60021,
          77.28239
        ],
        [
          28.61511,
          77.29383
        ]
      ]
    },
    {
      "route_id": "R-018",
      "route_name": "Route 18 (Radial_Express_Arterial)",
      "corridor_type": "Radial_Express_Arterial",
      "cluster": 2,
      "archetype_name": "Radial Express Arterial (High Speed & Smooth Flow)",
      "color": "#10B981",
      "length_km": 32.76,
      "stop_count": 34,
      "mean_speed_kmh": 25.271,
      "congestion_index": 1.614,
      "dwell_ratio": 0.175,
      "headway_irreg": 0.307,
      "accel_noise": 0.631,
      "delay_min": 34.875,
      "pca_1": -3.113,
      "pca_2": -0.372,
      "pca_3": -0.622,
      "waypoints": [
        [
          28.61421,
          77.26991
        ],
        [
          28.59819,
          77.27112
        ],
        [
          28.58563,
          77.27177
        ],
        [
          28.58059,
          77.27781
        ],
        [
          28.58587,
          77.29124
        ],
        [
          28.60206,
          77.3073
        ]
      ]
    },
    {
      "route_id": "R-019",
      "route_name": "Route 19 (Suburban_Feeder_Loop)",
      "corridor_type": "Suburban_Feeder_Loop",
      "cluster": 0,
      "archetype_name": "Suburban Feeder / Metro Link (Predictable Steady Flow)",
      "color": "#3B82F6",
      "length_km": 29.29,
      "stop_count": 50,
      "mean_speed_kmh": 18.536,
      "congestion_index": 1.661,
      "dwell_ratio": 0.263,
      "headway_irreg": 0.34,
      "accel_noise": 0.989,
      "delay_min": 46.195,
      "pca_1": -1.651,
      "pca_2": 0.415,
      "pca_3": -1.708,
      "waypoints": [
        [
          28.61691,
          77.24947
        ],
        [
          28.6054,
          77.25074
        ],
        [
          28.59571,
          77.25151
        ],
        [
          28.59067,
          77.25641
        ],
        [
          28.59257,
          77.26748
        ],
        [
          28.60262,
          77.28157
        ]
      ]
    },
    {
      "route_id": "R-020",
      "route_name": "Route 20 (High_Friction_Historic_Belt)",
      "corridor_type": "High_Friction_Historic_Belt",
      "cluster": 3,
      "archetype_name": "Congested Urban Core (Heavy Impedance Chokepoint)",
      "color": "#EF4444",
      "length_km": 26.9,
      "stop_count": 81,
      "mean_speed_kmh": 7.795,
      "congestion_index": 1.461,
      "dwell_ratio": 0.516,
      "headway_irreg": 0.524,
      "accel_noise": 2.217,
      "delay_min": 79.455,
      "pca_1": 2.773,
      "pca_2": -1.113,
      "pca_3": -0.767,
      "waypoints": [
        [
          28.60884,
          77.25594
        ],
        [
          28.59588,
          77.25427
        ],
        [
          28.58575,
          77.25271
        ],
        [
          28.58067,
          77.2567
        ],
        [
          28.58256,
          77.26833
        ],
        [
          28.5927,
          77.2839
        ]
      ]
    },
    {
      "route_id": "R-021",
      "route_name": "Route 21 (CBD_Core_Trunk)",
      "corridor_type": "CBD_Core_Trunk",
      "cluster": 1,
      "archetype_name": "High-Friction Historic / Commercial Belt (Stop-and-Go)",
      "color": "#F59E0B",
      "length_km": 31.57,
      "stop_count": 98,
      "mean_speed_kmh": 9.58,
      "congestion_index": 1.671,
      "dwell_ratio": 0.477,
      "headway_irreg": 0.407,
      "accel_noise": 1.727,
      "delay_min": 91.3,
      "pca_1": 1.986,
      "pca_2": 0.6,
      "pca_3": 0.655,
      "waypoints": [
        [
          28.59934,
          77.26097
        ],
        [
          28.58415,
          77.25718
        ],
        [
          28.57238,
          77.25393
        ],
        [
          28.56597,
          77.25797
        ],
        [
          28.56688,
          77.27195
        ],
        [
          28.57707,
          77.29161
        ]
      ]
    },
    {
      "route_id": "R-022",
      "route_name": "Route 22 (Radial_Express_Arterial)",
      "corridor_type": "Radial_Express_Arterial",
      "cluster": 2,
      "archetype_name": "Radial Express Arterial (High Speed & Smooth Flow)",
      "color": "#10B981",
      "length_km": 11.18,
      "stop_count": 12,
      "mean_speed_kmh": 25.168,
      "congestion_index": 1.609,
      "dwell_ratio": 0.168,
      "headway_irreg": 0.286,
      "accel_noise": 0.738,
      "delay_min": 12.26,
      "pca_1": -3.015,
      "pca_2": -0.241,
      "pca_3": 1.444,
      "waypoints": [
        [
          28.61994,
          77.22953
        ],
        [
          28.61506,
          77.22801
        ],
        [
          28.61119,
          77.2267
        ],
        [
          28.60878,
          77.22788
        ],
        [
          28.60843,
          77.23257
        ],
        [
          28.61097,
          77.2395
        ]
      ]
    },
    {
      "route_id": "R-023",
      "route_name": "Route 23 (Suburban_Feeder_Loop)",
      "corridor_type": "Suburban_Feeder_Loop",
      "cluster": 2,
      "archetype_name": "Radial Express Arterial (High Speed & Smooth Flow)",
      "color": "#10B981",
      "length_km": 25.48,
      "stop_count": 34,
      "mean_speed_kmh": 17.808,
      "congestion_index": 1.571,
      "dwell_ratio": 0.274,
      "headway_irreg": 0.325,
      "accel_noise": 0.946,
      "delay_min": 35.16,
      "pca_1": -1.624,
      "pca_2": -0.863,
      "pca_3": 1.335,
      "waypoints": [
        [
          28.59579,
          77.24885
        ],
        [
          28.58392,
          77.24257
        ],
        [
          28.57493,
          77.23752
        ],
        [
          28.56919,
          77.23963
        ],
        [
          28.5678,
          77.25133
        ],
        [
          28.57307,
          77.26931
        ]
      ]
    },
    {
      "route_id": "R-024",
      "route_name": "Route 24 (High_Friction_Historic_Belt)",
      "corridor_type": "High_Friction_Historic_Belt",
      "cluster": 3,
      "archetype_name": "Congested Urban Core (Heavy Impedance Chokepoint)",
      "color": "#EF4444",
      "length_km": 11.38,
      "stop_count": 34,
      "mean_speed_kmh": 7.166,
      "congestion_index": 1.553,
      "dwell_ratio": 0.543,
      "headway_irreg": 0.52,
      "accel_noise": 2.254,
      "delay_min": 40.46,
      "pca_1": 2.614,
      "pca_2": -0.692,
      "pca_3": 0.173,
      "waypoints": [
        [
          28.60117,
          77.23874
        ],
        [
          28.59434,
          77.23211
        ],
        [
          28.58986,
          77.22724
        ],
        [
          28.58721,
          77.22791
        ],
        [
          28.58678,
          77.23525
        ],
        [
          28.59012,
          77.24677
        ]
      ]
    },
    {
      "route_id": "R-025",
      "route_name": "Route 25 (CBD_Core_Trunk)",
      "corridor_type": "CBD_Core_Trunk",
      "cluster": 3,
      "archetype_name": "Congested Urban Core (Heavy Impedance Chokepoint)",
      "color": "#EF4444",
      "length_km": 13.47,
      "stop_count": 35,
      "mean_speed_kmh": 10.177,
      "congestion_index": 1.617,
      "dwell_ratio": 0.424,
      "headway_irreg": 0.565,
      "accel_noise": 1.708,
      "delay_min": 35.865,
      "pca_1": 1.388,
      "pca_2": 0.195,
      "pca_3": 0.106,
      "waypoints": [
        [
          28.61132,
          77.22835
        ],
        [
          28.60606,
          77.22425
        ],
        [
          28.60204,
          77.22095
        ],
        [
          28.59884,
          77.22141
        ],
        [
          28.59676,
          77.22701
        ],
        [
          28.59732,
          77.23643
        ]
      ]
    },
    {
      "route_id": "R-026",
      "route_name": "Route 26 (Radial_Express_Arterial)",
      "corridor_type": "Radial_Express_Arterial",
      "cluster": 2,
      "archetype_name": "Radial Express Arterial (High Speed & Smooth Flow)",
      "color": "#10B981",
      "length_km": 33.01,
      "stop_count": 29,
      "mean_speed_kmh": 26.99,
      "congestion_index": 1.559,
      "dwell_ratio": 0.161,
      "headway_irreg": 0.24,
      "accel_noise": 0.579,
      "delay_min": 31.76,
      "pca_1": -3.717,
      "pca_2": -0.585,
      "pca_3": -1.359,
      "waypoints": [
        [
          28.60321,
          77.2293
        ],
        [
          28.59327,
          77.22381
        ],
        [
          28.58472,
          77.2185
        ],
        [
          28.57681,
          77.2188
        ],
        [
          28.5699,
          77.22815
        ],
        [
          28.56702,
          77.24541
        ]
      ]
    },
    {
      "route_id": "R-027",
      "route_name": "Route 27 (Suburban_Feeder_Loop)",
      "corridor_type": "Suburban_Feeder_Loop",
      "cluster": 0,
      "archetype_name": "Suburban Feeder / Metro Link (Predictable Steady Flow)",
      "color": "#3B82F6",
      "length_km": 14.64,
      "stop_count": 24,
      "mean_speed_kmh": 17.528,
      "congestion_index": 1.777,
      "dwell_ratio": 0.287,
      "headway_irreg": 0.426,
      "accel_noise": 1.037,
      "delay_min": 28.04,
      "pca_1": -1.206,
      "pca_2": 1.955,
      "pca_3": -0.554,
      "waypoints": [
        [
          28.57599,
          77.23474
        ],
        [
          28.56981,
          77.22159
        ],
        [
          28.56625,
          77.21237
        ],
        [
          28.56274,
          77.21214
        ],
        [
          28.5593,
          77.22242
        ],
        [
          28.55928,
          77.24017
        ]
      ]
    },
    {
      "route_id": "R-028",
      "route_name": "Route 28 (High_Friction_Historic_Belt)",
      "corridor_type": "High_Friction_Historic_Belt",
      "cluster": 1,
      "archetype_name": "High-Friction Historic / Commercial Belt (Stop-and-Go)",
      "color": "#F59E0B",
      "length_km": 18.88,
      "stop_count": 68,
      "mean_speed_kmh": 7.357,
      "congestion_index": 1.634,
      "dwell_ratio": 0.523,
      "headway_irreg": 0.463,
      "accel_noise": 2.304,
      "delay_min": 76.84,
      "pca_1": 2.985,
      "pca_2": 0.861,
      "pca_3": -1.203,
      "waypoints": [
        [
          28.59547,
          77.22436
        ],
        [
          28.59015,
          77.21564
        ],
        [
          28.58627,
          77.20889
        ],
        [
          28.58181,
          77.20812
        ],
        [
          28.57656,
          77.21529
        ],
        [
          28.57331,
          77.22907
        ]
      ]
    },
    {
      "route_id": "R-029",
      "route_name": "Route 29 (CBD_Core_Trunk)",
      "corridor_type": "CBD_Core_Trunk",
      "cluster": 1,
      "archetype_name": "High-Friction Historic / Commercial Belt (Stop-and-Go)",
      "color": "#F59E0B",
      "length_km": 23.59,
      "stop_count": 75,
      "mean_speed_kmh": 10.332,
      "congestion_index": 1.603,
      "dwell_ratio": 0.486,
      "headway_irreg": 0.576,
      "accel_noise": 1.709,
      "delay_min": 61.57,
      "pca_1": 2.354,
      "pca_2": 0.786,
      "pca_3": 1.524,
      "waypoints": [
        [
          28.60053,
          77.21996
        ],
        [
          28.59501,
          77.21191
        ],
        [
          28.59064,
          77.20514
        ],
        [
          28.58519,
          77.2036
        ],
        [
          28.57816,
          77.20971
        ],
        [
          28.57237,
          77.22291
        ]
      ]
    },
    {
      "route_id": "R-030",
      "route_name": "Route 30 (Radial_Express_Arterial)",
      "corridor_type": "Radial_Express_Arterial",
      "cluster": 2,
      "archetype_name": "Radial Express Arterial (High Speed & Smooth Flow)",
      "color": "#10B981",
      "length_km": 12.58,
      "stop_count": 11,
      "mean_speed_kmh": 25.494,
      "congestion_index": 1.622,
      "dwell_ratio": 0.192,
      "headway_irreg": 0.42,
      "accel_noise": 0.743,
      "delay_min": 14.21,
      "pca_1": -2.688,
      "pca_2": -0.066,
      "pca_3": 0.636,
      "waypoints": [
        [
          28.61538,
          77.2167
        ],
        [
          28.61289,
          77.21224
        ],
        [
          28.61093,
          77.20847
        ],
        [
          28.60813,
          77.20735
        ],
        [
          28.60408,
          77.21013
        ],
        [
          28.60029,
          77.2167
        ]
      ]
    },
    {
      "route_id": "R-031",
      "route_name": "Route 31 (Suburban_Feeder_Loop)",
      "corridor_type": "Suburban_Feeder_Loop",
      "cluster": 0,
      "archetype_name": "Suburban Feeder / Metro Link (Predictable Steady Flow)",
      "color": "#3B82F6",
      "length_km": 32.67,
      "stop_count": 53,
      "mean_speed_kmh": 17.368,
      "congestion_index": 1.681,
      "dwell_ratio": 0.291,
      "headway_irreg": 0.369,
      "accel_noise": 0.98,
      "delay_min": 53.085,
      "pca_1": -1.087,
      "pca_2": 0.515,
      "pca_3": 0.59,
      "waypoints": [
        [
          28.58885,
          77.21222
        ],
        [
          28.58368,
          77.19979
        ],
        [
          28.5797,
          77.18939
        ],
        [
          28.57276,
          77.18573
        ],
        [
          28.5615,
          77.19195
        ],
        [
          28.54987,
          77.20812
        ]
      ]
    },
    {
      "route_id": "R-032",
      "route_name": "Route 32 (High_Friction_Historic_Belt)",
      "corridor_type": "High_Friction_Historic_Belt",
      "cluster": 1,
      "archetype_name": "High-Friction Historic / Commercial Belt (Stop-and-Go)",
      "color": "#F59E0B",
      "length_km": 28.39,
      "stop_count": 86,
      "mean_speed_kmh": 7.073,
      "congestion_index": 1.586,
      "dwell_ratio": 0.525,
      "headway_irreg": 0.575,
      "accel_noise": 2.285,
      "delay_min": 102.9,
      "pca_1": 3.496,
      "pca_2": 0.109,
      "pca_3": -0.074,
      "waypoints": [
        [
          28.59933,
          77.20986
        ],
        [
          28.59566,
          77.19963
        ],
        [
          28.59285,
          77.19083
        ],
        [
          28.58718,
          77.18704
        ],
        [
          28.5772,
          77.19084
        ],
        [
          28.56601,
          77.20278
        ]
      ]
    },
    {
      "route_id": "R-033",
      "route_name": "Route 33 (CBD_Core_Trunk)",
      "corridor_type": "CBD_Core_Trunk",
      "cluster": 3,
      "archetype_name": "Congested Urban Core (Heavy Impedance Chokepoint)",
      "color": "#EF4444",
      "length_km": 30.51,
      "stop_count": 84,
      "mean_speed_kmh": 10.471,
      "congestion_index": 1.633,
      "dwell_ratio": 0.439,
      "headway_irreg": 0.305,
      "accel_noise": 1.744,
      "delay_min": 84.14,
      "pca_1": 0.957,
      "pca_2": -0.29,
      "pca_3": -1.47,
      "waypoints": [
        [
          28.60289,
          77.2074
        ],
        [
          28.5996,
          77.19717
        ],
        [
          28.59714,
          77.18807
        ],
        [
          28.59151,
          77.18339
        ],
        [
          28.58086,
          77.18571
        ],
        [
          28.56807,
          77.19609
        ]
      ]
    },
    {
      "route_id": "R-034",
      "route_name": "Route 34 (Radial_Express_Arterial)",
      "corridor_type": "Radial_Express_Arterial",
      "cluster": 2,
      "archetype_name": "Radial Express Arterial (High Speed & Smooth Flow)",
      "color": "#10B981",
      "length_km": 26.02,
      "stop_count": 22,
      "mean_speed_kmh": 30.016,
      "congestion_index": 1.343,
      "dwell_ratio": 0.164,
      "headway_irreg": 0.292,
      "accel_noise": 0.69,
      "delay_min": 17.17,
      "pca_1": -3.59,
      "pca_2": -2.361,
      "pca_3": 0.129,
      "waypoints": [
        [
          28.59157,
          77.19892
        ],
        [
          28.59185,
          77.18631
        ],
        [
          28.59231,
          77.17641
        ],
        [
          28.58796,
          77.17193
        ],
        [
          28.57698,
          77.17491
        ],
        [
          28.56304,
          77.18622
        ]
      ]
    },
    {
      "route_id": "R-035",
      "route_name": "Route 35 (Suburban_Feeder_Loop)",
      "corridor_type": "Suburban_Feeder_Loop",
      "cluster": 0,
      "archetype_name": "Suburban Feeder / Metro Link (Predictable Steady Flow)",
      "color": "#3B82F6",
      "length_km": 14.29,
      "stop_count": 21,
      "mean_speed_kmh": 17.977,
      "congestion_index": 1.684,
      "dwell_ratio": 0.271,
      "headway_irreg": 0.336,
      "accel_noise": 1.023,
      "delay_min": 23.825,
      "pca_1": -1.694,
      "pca_2": 1.371,
      "pca_3": -0.395,
      "waypoints": [
        [
          28.58533,
          77.19004
        ],
        [
          28.59032,
          77.17766
        ],
        [
          28.59428,
          77.16941
        ],
        [
          28.59216,
          77.16672
        ],
        [
          28.58285,
          77.17058
        ],
        [
          28.57048,
          77.18147
        ]
      ]
    },
    {
      "route_id": "R-036",
      "route_name": "Route 36 (High_Friction_Historic_Belt)",
      "corridor_type": "High_Friction_Historic_Belt",
      "cluster": 1,
      "archetype_name": "High-Friction Historic / Commercial Belt (Stop-and-Go)",
      "color": "#F59E0B",
      "length_km": 28.84,
      "stop_count": 95,
      "mean_speed_kmh": 6.958,
      "congestion_index": 1.561,
      "dwell_ratio": 0.544,
      "headway_irreg": 0.502,
      "accel_noise": 2.25,
      "delay_min": 100.44,
      "pca_1": 3.383,
      "pca_2": -0.762,
      "pca_3": 0.457,
      "waypoints": [
        [
          28.59293,
          77.18868
        ],
        [
          28.59602,
          77.17521
        ],
        [
          28.59872,
          77.16465
        ],
        [
          28.59503,
          77.15879
        ],
        [
          28.58253,
          77.15942
        ],
        [
          28.56494,
          77.16834
        ]
      ]
    },
    {
      "route_id": "R-037",
      "route_name": "Route 37 (CBD_Core_Trunk)",
      "corridor_type": "CBD_Core_Trunk",
      "cluster": 3,
      "archetype_name": "Congested Urban Core (Heavy Impedance Chokepoint)",
      "color": "#EF4444",
      "length_km": 13.77,
      "stop_count": 41,
      "mean_speed_kmh": 9.532,
      "congestion_index": 1.601,
      "dwell_ratio": 0.472,
      "headway_irreg": 0.497,
      "accel_noise": 1.731,
      "delay_min": 38.525,
      "pca_1": 1.759,
      "pca_2": -0.751,
      "pca_3": 1.973,
      "waypoints": [
        [
          28.59051,
          77.17979
        ],
        [
          28.59836,
          77.16854
        ],
        [
          28.60423,
          77.16128
        ],
        [
          28.60277,
          77.15832
        ],
        [
          28.59274,
          77.16037
        ],
        [
          28.57823,
          77.16874
        ]
      ]
    },
    {
      "route_id": "R-038",
      "route_name": "Route 38 (Radial_Express_Arterial)",
      "corridor_type": "Radial_Express_Arterial",
      "cluster": 2,
      "archetype_name": "Radial Express Arterial (High Speed & Smooth Flow)",
      "color": "#10B981",
      "length_km": 14.08,
      "stop_count": 14,
      "mean_speed_kmh": 25.942,
      "congestion_index": 1.551,
      "dwell_ratio": 0.168,
      "headway_irreg": 0.306,
      "accel_noise": 0.66,
      "delay_min": 14.69,
      "pca_1": -3.112,
      "pca_2": -0.293,
      "pca_3": 1.262,
      "waypoints": [
        [
          28.60648,
          77.18891
        ],
        [
          28.61203,
          77.18088
        ],
        [
          28.61625,
          77.17527
        ],
        [
          28.61509,
          77.1721
        ],
        [
          28.60719,
          77.17198
        ],
        [
          28.59518,
          77.17636
        ]
      ]
    },
    {
      "route_id": "R-039",
      "route_name": "Route 39 (Suburban_Feeder_Loop)",
      "corridor_type": "Suburban_Feeder_Loop",
      "cluster": 2,
      "archetype_name": "Radial Express Arterial (High Speed & Smooth Flow)",
      "color": "#10B981",
      "length_km": 29.33,
      "stop_count": 44,
      "mean_speed_kmh": 17.691,
      "congestion_index": 1.595,
      "dwell_ratio": 0.295,
      "headway_irreg": 0.366,
      "accel_noise": 1.039,
      "delay_min": 42.385,
      "pca_1": -1.188,
      "pca_2": -0.365,
      "pca_3": 0.962,
      "waypoints": [
        [
          28.60598,
          77.18158
        ],
        [
          28.61217,
          77.1701
        ],
        [
          28.61739,
          77.16096
        ],
        [
          28.61567,
          77.15414
        ],
        [
          28.60408,
          77.15059
        ],
        [
          28.58529,
          77.1531
        ]
      ]
    },
    {
      "route_id": "R-040",
      "route_name": "Route 40 (High_Friction_Historic_Belt)",
      "corridor_type": "High_Friction_Historic_Belt",
      "cluster": 1,
      "archetype_name": "High-Friction Historic / Commercial Belt (Stop-and-Go)",
      "color": "#F59E0B",
      "length_km": 31.01,
      "stop_count": 110,
      "mean_speed_kmh": 7.025,
      "congestion_index": 1.607,
      "dwell_ratio": 0.525,
      "headway_irreg": 0.474,
      "accel_noise": 2.28,
      "delay_min": 115.74,
      "pca_1": 3.444,
      "pca_2": -0.095,
      "pca_3": -0.526,
      "waypoints": [
        [
          28.60746,
          77.17506
        ],
        [
          28.6157,
          77.16347
        ],
        [
          28.62251,
          77.15437
        ],
        [
          28.62145,
          77.14701
        ],
        [
          28.60935,
          77.14206
        ],
        [
          28.58885,
          77.14283
        ]
      ]
    },
    {
      "route_id": "R-041",
      "route_name": "Route 41 (CBD_Core_Trunk)",
      "corridor_type": "CBD_Core_Trunk",
      "cluster": 3,
      "archetype_name": "Congested Urban Core (Heavy Impedance Chokepoint)",
      "color": "#EF4444",
      "length_km": 27.25,
      "stop_count": 75,
      "mean_speed_kmh": 10.815,
      "congestion_index": 1.66,
      "dwell_ratio": 0.414,
      "headway_irreg": 0.422,
      "accel_noise": 1.695,
      "delay_min": 79.485,
      "pca_1": 1.141,
      "pca_2": 0.705,
      "pca_3": -1.869,
      "waypoints": [
        [
          28.61757,
          77.18542
        ],
        [
          28.62405,
          77.1766
        ],
        [
          28.62968,
          77.16941
        ],
        [
          28.62943,
          77.16287
        ],
        [
          28.62046,
          77.15731
        ],
        [
          28.60427,
          77.15554
        ]
      ]
    },
    {
      "route_id": "R-042",
      "route_name": "Route 42 (Radial_Express_Arterial)",
      "corridor_type": "Radial_Express_Arterial",
      "cluster": 2,
      "archetype_name": "Radial Express Arterial (High Speed & Smooth Flow)",
      "color": "#10B981",
      "length_km": 31.94,
      "stop_count": 27,
      "mean_speed_kmh": 27.439,
      "congestion_index": 1.532,
      "dwell_ratio": 0.158,
      "headway_irreg": 0.309,
      "accel_noise": 0.674,
      "delay_min": 29.705,
      "pca_1": -3.324,
      "pca_2": -1.173,
      "pca_3": -0.242,
      "waypoints": [
        [
          28.62,
          77.18131
        ],
        [
          28.62796,
          77.17196
        ],
        [
          28.63498,
          77.16427
        ],
        [
          28.63549,
          77.15663
        ],
        [
          28.62614,
          77.14904
        ],
        [
          28.60816,
          77.14486
        ]
      ]
    },
    {
      "route_id": "R-043",
      "route_name": "Route 43 (Suburban_Feeder_Loop)",
      "corridor_type": "Suburban_Feeder_Loop",
      "cluster": 2,
      "archetype_name": "Radial Express Arterial (High Speed & Smooth Flow)",
      "color": "#10B981",
      "length_km": 25.94,
      "stop_count": 34,
      "mean_speed_kmh": 20.128,
      "congestion_index": 1.395,
      "dwell_ratio": 0.251,
      "headway_irreg": 0.271,
      "accel_noise": 0.913,
      "delay_min": 24.81,
      "pca_1": -2.323,
      "pca_2": -2.235,
      "pca_3": 0.251,
      "waypoints": [
        [
          28.62125,
          77.16846
        ],
        [
          28.63293,
          77.16118
        ],
        [
          28.64201,
          77.15583
        ],
        [
          28.64307,
          77.1497
        ],
        [
          28.63341,
          77.1425
        ],
        [
          28.61477,
          77.13801
        ]
      ]
    },
    {
      "route_id": "R-044",
      "route_name": "Route 44 (High_Friction_Historic_Belt)",
      "corridor_type": "High_Friction_Historic_Belt",
      "cluster": 3,
      "archetype_name": "Congested Urban Core (Heavy Impedance Chokepoint)",
      "color": "#EF4444",
      "length_km": 16.02,
      "stop_count": 51,
      "mean_speed_kmh": 7.089,
      "congestion_index": 1.55,
      "dwell_ratio": 0.543,
      "headway_irreg": 0.639,
      "accel_noise": 2.219,
      "delay_min": 55.6,
      "pca_1": 3.039,
      "pca_2": -1.404,
      "pca_3": -0.592,
      "waypoints": [
        [
          28.62754,
          77.17907
        ],
        [
          28.63692,
          77.17537
        ],
        [
          28.64389,
          77.17289
        ],
        [
          28.64494,
          77.16919
        ],
        [
          28.63842,
          77.16394
        ],
        [
          28.62554,
          77.15995
        ]
      ]
    },
    {
      "route_id": "R-045",
      "route_name": "Route 45 (CBD_Core_Trunk)",
      "corridor_type": "CBD_Core_Trunk",
      "cluster": 3,
      "archetype_name": "Congested Urban Core (Heavy Impedance Chokepoint)",
      "color": "#EF4444",
      "length_km": 21.58,
      "stop_count": 56,
      "mean_speed_kmh": 9.786,
      "congestion_index": 1.695,
      "dwell_ratio": 0.436,
      "headway_irreg": 0.363,
      "accel_noise": 1.746,
      "delay_min": 64.31,
      "pca_1": 1.071,
      "pca_2": 0.75,
      "pca_3": -0.513,
      "waypoints": [
        [
          28.6315,
          77.1675
        ],
        [
          28.64417,
          77.16382
        ],
        [
          28.65361,
          77.1614
        ],
        [
          28.65554,
          77.15659
        ],
        [
          28.64779,
          77.14871
        ],
        [
          28.6315,
          77.1416
        ]
      ]
    },
    {
      "route_id": "R-046",
      "route_name": "Route 46 (Radial_Express_Arterial)",
      "corridor_type": "Radial_Express_Arterial",
      "cluster": 0,
      "archetype_name": "Suburban Feeder / Metro Link (Predictable Steady Flow)",
      "color": "#3B82F6",
      "length_km": 30.37,
      "stop_count": 29,
      "mean_speed_kmh": 23.018,
      "congestion_index": 1.878,
      "dwell_ratio": 0.179,
      "headway_irreg": 0.284,
      "accel_noise": 0.712,
      "delay_min": 45.435,
      "pca_1": -2.844,
      "pca_2": 2.434,
      "pca_3": -1.147,
      "waypoints": [
        [
          28.63531,
          77.18042
        ],
        [
          28.64609,
          77.17543
        ],
        [
          28.65531,
          77.17153
        ],
        [
          28.65871,
          77.16509
        ],
        [
          28.65338,
          77.15482
        ],
        [
          28.63912,
          77.14418
        ]
      ]
    },
    {
      "route_id": "R-047",
      "route_name": "Route 47 (Suburban_Feeder_Loop)",
      "corridor_type": "Suburban_Feeder_Loop",
      "cluster": 0,
      "archetype_name": "Suburban Feeder / Metro Link (Predictable Steady Flow)",
      "color": "#3B82F6",
      "length_km": 22.3,
      "stop_count": 33,
      "mean_speed_kmh": 18.282,
      "congestion_index": 1.686,
      "dwell_ratio": 0.288,
      "headway_irreg": 0.331,
      "accel_noise": 1.093,
      "delay_min": 37.11,
      "pca_1": -1.574,
      "pca_2": 0.336,
      "pca_3": -0.956,
      "waypoints": [
        [
          28.63672,
          77.19212
        ],
        [
          28.64461,
          77.18918
        ],
        [
          28.65143,
          77.18692
        ],
        [
          28.65441,
          77.18247
        ],
        [
          28.65151,
          77.17469
        ],
        [
          28.64229,
          77.16594
        ]
      ]
    },
    {
      "route_id": "R-048",
      "route_name": "Route 48 (High_Friction_Historic_Belt)",
      "corridor_type": "High_Friction_Historic_Belt",
      "cluster": 1,
      "archetype_name": "High-Friction Historic / Commercial Belt (Stop-and-Go)",
      "color": "#F59E0B",
      "length_km": 23.69,
      "stop_count": 75,
      "mean_speed_kmh": 6.697,
      "congestion_index": 1.641,
      "dwell_ratio": 0.594,
      "headway_irreg": 0.374,
      "accel_noise": 2.342,
      "delay_min": 94.215,
      "pca_1": 3.368,
      "pca_2": 1.021,
      "pca_3": 1.337,
      "waypoints": [
        [
          28.64225,
          77.1836
        ],
        [
          28.65264,
          77.18217
        ],
        [
          28.66105,
          77.18122
        ],
        [
          28.66469,
          77.17686
        ],
        [
          28.66154,
          77.16762
        ],
        [
          28.65104,
          77.15656
        ]
      ]
    },
    {
      "route_id": "R-049",
      "route_name": "Route 49 (CBD_Core_Trunk)",
      "corridor_type": "CBD_Core_Trunk",
      "cluster": 3,
      "archetype_name": "Congested Urban Core (Heavy Impedance Chokepoint)",
      "color": "#EF4444",
      "length_km": 10.88,
      "stop_count": 29,
      "mean_speed_kmh": 10.431,
      "congestion_index": 1.517,
      "dwell_ratio": 0.425,
      "headway_irreg": 0.422,
      "accel_noise": 1.629,
      "delay_min": 24.73,
      "pca_1": 0.694,
      "pca_2": -1.424,
      "pca_3": 0.516,
      "waypoints": [
        [
          28.64529,
          77.18573
        ],
        [
          28.65371,
          77.18772
        ],
        [
          28.65955,
          77.18942
        ],
        [
          28.66142,
          77.1876
        ],
        [
          28.65848,
          77.1815
        ],
        [
          28.6506,
          77.1738
        ]
      ]
    },
    {
      "route_id": "R-050",
      "route_name": "Route 50 (Radial_Express_Arterial)",
      "corridor_type": "Radial_Express_Arterial",
      "cluster": 2,
      "archetype_name": "Radial Express Arterial (High Speed & Smooth Flow)",
      "color": "#10B981",
      "length_km": 16.5,
      "stop_count": 17,
      "mean_speed_kmh": 26.324,
      "congestion_index": 1.611,
      "dwell_ratio": 0.171,
      "headway_irreg": 0.351,
      "accel_noise": 0.652,
      "delay_min": 17.99,
      "pca_1": -3.203,
      "pca_2": -0.05,
      "pca_3": -0.861,
      "waypoints": [
        [
          28.64858,
          77.18711
        ],
        [
          28.65773,
          77.18903
        ],
        [
          28.66457,
          77.19067
        ],
        [
          28.66768,
          77.18822
        ],
        [
          28.6659,
          77.18041
        ],
        [
          28.65848,
          77.16996
        ]
      ]
    },
    {
      "route_id": "R-051",
      "route_name": "Route 51 (Suburban_Feeder_Loop)",
      "corridor_type": "Suburban_Feeder_Loop",
      "cluster": 2,
      "archetype_name": "Radial Express Arterial (High Speed & Smooth Flow)",
      "color": "#10B981",
      "length_km": 15.07,
      "stop_count": 25,
      "mean_speed_kmh": 18.204,
      "congestion_index": 1.559,
      "dwell_ratio": 0.268,
      "headway_irreg": 0.346,
      "accel_noise": 1.02,
      "delay_min": 21.47,
      "pca_1": -1.48,
      "pca_2": -0.845,
      "pca_3": 1.518,
      "waypoints": [
        [
          28.66078,
          77.1764
        ],
        [
          28.67211,
          77.18198
        ],
        [
          28.67977,
          77.1863
        ],
        [
          28.68284,
          77.18437
        ],
        [
          28.68036,
          77.17493
        ],
        [
          28.67141,
          77.16177
        ]
      ]
    },
    {
      "route_id": "R-052",
      "route_name": "Route 52 (High_Friction_Historic_Belt)",
      "corridor_type": "High_Friction_Historic_Belt",
      "cluster": 3,
      "archetype_name": "Congested Urban Core (Heavy Impedance Chokepoint)",
      "color": "#EF4444",
      "length_km": 12.0,
      "stop_count": 36,
      "mean_speed_kmh": 7.659,
      "congestion_index": 1.5,
      "dwell_ratio": 0.549,
      "headway_irreg": 0.659,
      "accel_noise": 2.256,
      "delay_min": 37.81,
      "pca_1": 2.9,
      "pca_2": -0.786,
      "pca_3": -0.753,
      "waypoints": [
        [
          28.64739,
          77.19905
        ],
        [
          28.65343,
          77.20161
        ],
        [
          28.65797,
          77.20367
        ],
        [
          28.66056,
          77.2024
        ],
        [
          28.66055,
          77.19671
        ],
        [
          28.65702,
          77.18835
        ]
      ]
    },
    {
      "route_id": "R-053",
      "route_name": "Route 53 (CBD_Core_Trunk)",
      "corridor_type": "CBD_Core_Trunk",
      "cluster": 3,
      "archetype_name": "Congested Urban Core (Heavy Impedance Chokepoint)",
      "color": "#EF4444",
      "length_km": 30.74,
      "stop_count": 96,
      "mean_speed_kmh": 9.403,
      "congestion_index": 1.685,
      "dwell_ratio": 0.46,
      "headway_irreg": 0.502,
      "accel_noise": 1.77,
      "delay_min": 91.095,
      "pca_1": 2.013,
      "pca_2": -0.946,
      "pca_3": -0.684,
      "waypoints": [
        [
          28.64342,
          77.20597
        ],
        [
          28.65207,
          77.20552
        ],
        [
          28.6604,
          77.20607
        ],
        [
          28.66732,
          77.20352
        ],
        [
          28.67152,
          77.19495
        ],
        [
          28.67083,
          77.18129
        ]
      ]
    },
    {
      "route_id": "R-054",
      "route_name": "Route 54 (Radial_Express_Arterial)",
      "corridor_type": "Radial_Express_Arterial",
      "cluster": 2,
      "archetype_name": "Radial Express Arterial (High Speed & Smooth Flow)",
      "color": "#10B981",
      "length_km": 19.48,
      "stop_count": 17,
      "mean_speed_kmh": 27.417,
      "congestion_index": 1.461,
      "dwell_ratio": 0.176,
      "headway_irreg": 0.26,
      "accel_noise": 0.594,
      "delay_min": 16.065,
      "pca_1": -3.665,
      "pca_2": -1.647,
      "pca_3": -0.062,
      "waypoints": [
        [
          28.6598,
          77.19614
        ],
        [
          28.66813,
          77.2015
        ],
        [
          28.67448,
          77.20582
        ],
        [
          28.67901,
          77.20467
        ],
        [
          28.68109,
          77.19613
        ],
        [
          28.67872,
          77.1824
        ]
      ]
    },
    {
      "route_id": "R-055",
      "route_name": "Route 55 (Suburban_Feeder_Loop)",
      "corridor_type": "Suburban_Feeder_Loop",
      "cluster": 0,
      "archetype_name": "Suburban Feeder / Metro Link (Predictable Steady Flow)",
      "color": "#3B82F6",
      "length_km": 25.67,
      "stop_count": 37,
      "mean_speed_kmh": 15.984,
      "congestion_index": 1.828,
      "dwell_ratio": 0.295,
      "headway_irreg": 0.404,
      "accel_noise": 1.016,
      "delay_min": 50.41,
      "pca_1": -0.813,
      "pca_2": 2.366,
      "pca_3": 1.105,
      "waypoints": [
        [
          28.6655,
          77.19707
        ],
        [
          28.67505,
          77.20378
        ],
        [
          28.68256,
          77.20934
        ],
        [
          28.68866,
          77.20846
        ],
        [
          28.69277,
          77.19852
        ],
        [
          28.69218,
          77.18167
        ]
      ]
    },
    {
      "route_id": "R-056",
      "route_name": "Route 56 (High_Friction_Historic_Belt)",
      "corridor_type": "High_Friction_Historic_Belt",
      "cluster": 1,
      "archetype_name": "High-Friction Historic / Commercial Belt (Stop-and-Go)",
      "color": "#F59E0B",
      "length_km": 30.15,
      "stop_count": 94,
      "mean_speed_kmh": 7.039,
      "congestion_index": 1.604,
      "dwell_ratio": 0.551,
      "headway_irreg": 0.535,
      "accel_noise": 2.243,
      "delay_min": 113.69,
      "pca_1": 3.524,
      "pca_2": -0.154,
      "pca_3": -0.053,
      "waypoints": [
        [
          28.68251,
          77.19399
        ],
        [
          28.69351,
          77.20517
        ],
        [
          28.70176,
          77.214
        ],
        [
          28.70899,
          77.21372
        ],
        [
          28.71485,
          77.20121
        ],
        [
          28.71556,
          77.17927
        ]
      ]
    },
    {
      "route_id": "R-057",
      "route_name": "Route 57 (CBD_Core_Trunk)",
      "corridor_type": "CBD_Core_Trunk",
      "cluster": 3,
      "archetype_name": "Congested Urban Core (Heavy Impedance Chokepoint)",
      "color": "#EF4444",
      "length_km": 32.92,
      "stop_count": 104,
      "mean_speed_kmh": 10.571,
      "congestion_index": 1.619,
      "dwell_ratio": 0.43,
      "headway_irreg": 0.404,
      "accel_noise": 1.66,
      "delay_min": 88.9,
      "pca_1": 1.491,
      "pca_2": 0.107,
      "pca_3": -0.774,
      "waypoints": [
        [
          28.6533,
          77.20962
        ],
        [
          28.66222,
          77.21427
        ],
        [
          28.67013,
          77.21926
        ],
        [
          28.67802,
          77.21979
        ],
        [
          28.68585,
          77.21239
        ],
        [
          28.69087,
          77.19741
        ]
      ]
    },
    {
      "route_id": "R-058",
      "route_name": "Route 58 (Radial_Express_Arterial)",
      "corridor_type": "Radial_Express_Arterial",
      "cluster": 0,
      "archetype_name": "Suburban Feeder / Metro Link (Predictable Steady Flow)",
      "color": "#3B82F6",
      "length_km": 30.55,
      "stop_count": 26,
      "mean_speed_kmh": 26.401,
      "congestion_index": 1.663,
      "dwell_ratio": 0.175,
      "headway_irreg": 0.342,
      "accel_noise": 0.668,
      "delay_min": 34.29,
      "pca_1": -2.947,
      "pca_2": 1.262,
      "pca_3": -0.004,
      "waypoints": [
        [
          28.6498,
          77.21281
        ],
        [
          28.65753,
          77.21737
        ],
        [
          28.66438,
          77.22238
        ],
        [
          28.67161,
          77.22363
        ],
        [
          28.67952,
          77.21793
        ],
        [
          28.68565,
          77.20519
        ]
      ]
    },
    {
      "route_id": "R-059",
      "route_name": "Route 59 (Suburban_Feeder_Loop)",
      "corridor_type": "Suburban_Feeder_Loop",
      "cluster": 2,
      "archetype_name": "Radial Express Arterial (High Speed & Smooth Flow)",
      "color": "#10B981",
      "length_km": 14.31,
      "stop_count": 20,
      "mean_speed_kmh": 19.232,
      "congestion_index": 1.519,
      "dwell_ratio": 0.276,
      "headway_irreg": 0.32,
      "accel_noise": 0.971,
      "delay_min": 18.86,
      "pca_1": -1.9,
      "pca_2": -0.498,
      "pca_3": 0.535,
      "waypoints": [
        [
          28.66978,
          77.21268
        ],
        [
          28.67307,
          77.22215
        ],
        [
          28.67515,
          77.22905
        ],
        [
          28.67845,
          77.22998
        ],
        [
          28.68329,
          77.22349
        ],
        [
          28.68686,
          77.21088
        ]
      ]
    },
    {
      "route_id": "R-060",
      "route_name": "Route 60 (High_Friction_Historic_Belt)",
      "corridor_type": "High_Friction_Historic_Belt",
      "cluster": 1,
      "archetype_name": "High-Friction Historic / Commercial Belt (Stop-and-Go)",
      "color": "#F59E0B",
      "length_km": 31.29,
      "stop_count": 98,
      "mean_speed_kmh": 6.46,
      "congestion_index": 1.674,
      "dwell_ratio": 0.585,
      "headway_irreg": 0.547,
      "accel_noise": 2.346,
      "delay_min": 130.045,
      "pca_1": 4.184,
      "pca_2": 0.758,
      "pca_3": 0.888,
      "waypoints": [
        [
          28.65923,
          77.2167
        ],
        [
          28.66577,
          77.22491
        ],
        [
          28.67119,
          77.23257
        ],
        [
          28.67816,
          77.23536
        ],
        [
          28.68768,
          77.23016
        ],
        [
          28.69677,
          77.2167
        ]
      ]
    }
  ]
};
