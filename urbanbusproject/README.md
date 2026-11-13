# Unsupervised Clustering of Urban Bus Routes Using Traffic Patterns
### Smart India Hackathon (SIH) Grade Intelligent Transit Analytics System

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Scikit-Learn](https://img.shields.io/badge/ML-Scikit--Learn-orange.svg)](https://scikit-learn.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![SIH Track](https://img.shields.io/badge/SIH-Smart%20Mobility-purple.svg)]()

> **Project Mission**: Uncover latent operational regimes, dynamic bottlenecks, and traffic-pattern structures from raw urban bus telemetry without requiring supervised labels, enabling municipal transit corporations (DTC, BMTC, BEST) to deploy precision interventions like dedicated bus lanes, Transit Signal Priority (TSP), and optimal Electric Bus (EV) allocation.

---

## 📌 Executive Summary

Traditional urban transit timetables are static and fail to capture real-world traffic dynamics, leading to severe bus bunching, unpredictable headway variance, and passenger delays. Because **ground-truth labels do not exist** for "traffic pattern types", supervised machine learning is unusable without subjective manual bias.

This project delivers an end-to-end, mathematically validated **unsupervised learning pipeline** that:
1. **Preprocesses Transit Telemetry**: Handles missing GPS/AVL sensor dropouts using distance-weighted **KNN Imputation** and scales multi-dimensional variables via **StandardScaler** & **RobustScaler**.
2. **Engineers Movement & Temporal Indicators**: Extracts 10 operational transit metrics including speed variability ($CV$), congestion index ($CI$), stop dwell time ratio, headway irregularity, and acceleration noise ($m/s^2$).
3. **Compares Similarity Metrics**: Benchmarks **Euclidean ($L_2$)** versus **Manhattan ($L_1$)** distance measures, demonstrating Manhattan's superiority against traffic outlier spikes and higher relative contrast (20.2 vs 16.5).
4. **Applies Multi-Algorithm Clustering**: Evaluates **K-Means++** across $k \in [2, 8]$ alongside **Hierarchical Agglomerative Clustering** comparing four linkage strategies: **Ward**, **Complete**, **Average**, and **Single**.
5. **Reduces Dimensionality via PCA**: Performs Scree eigenvalue decomposition ($80.3\%$ variance in top 2 PCs, $89.6\%$ in top 3 PCs) and constructs factor loading biplots to visualize traffic friction and operational regularity axes.
6. **Validates Quality & Stability**: Evaluates Silhouette score, Davies-Bouldin index, and runs a **40-fold bootstrap perturbation test** achieving a mean **Adjusted Rand Index (ARI) of 0.892** and **NMI of 0.923** (confirming high mathematical stability).
7. **Delivers Production-Grade Tools**: Ships an interactive GIS Leaflet web dashboard, real-time REST API, automated unit test suite, and a complete 11-slide presentation pitch deck (`.pptx`).

---

## 🚀 Key Results & Benchmarks

| Metric / Evaluation Step | Euclidean ($L_2$) | Manhattan ($L_1$) | Winner / Optimal Config |
| :--- | :---: | :---: | :---: |
| **Distance Relative Contrast** | $16.51$ | **$20.21$** | **Manhattan ($L_1$)** (Superior discriminative spread) |
| **Outlier Robustness** | Sensitive to squared spikes | **Linear penalty** | **Manhattan ($L_1$)** |
| **Hierarchical Silhouette ($k=4$)** | $0.320$ (Ward) | **$0.366$** (Average) | **Manhattan + Average Linkage** |
| **Cophenetic Correlation** | $0.762$ (Ward) | **$0.819$** (Average) | **Average Linkage ($c = 0.819$)** |
| **PCA Cumulative Variance (Top 2 PCs)** | — | — | **$80.3\%$** ($89.6\%$ with PC3) |
| **Bootstrap Stability (40 resamples)** | — | — | **Mean ARI: $0.892 \pm 0.081$** (Highly Stable) |

---

## 🚌 Discovered Traffic Archetypes & Policy Interventions

1. 🟢 **Radial Express Arterial (High Speed & Smooth Flow)**
   - *Characteristics*: Mean speed $\ge 24$ km/h, low congestion index ($1.15-1.30$), dwell ratio $< 18\%$.
   - *Policy Action*: Prime corridor for **Electric Bus (EV)** deployment due to uniform regenerative braking and predictable energy drain.
2. 🔵 **Suburban Feeder / Metro Link (Predictable Steady Flow)**
   - *Characteristics*: Speed $18-24$ km/h, stable headway, minimal bunching, low schedule delay.
   - *Policy Action*: Timed-transfer synchronization with Metro rail train arrival waves.
3. 🔴 **Congested Urban Core (Heavy Impedance Chokepoint)**
   - *Characteristics*: Speed $< 14$ km/h, congestion index $> 1.70$, severe peak delay, high boarding dwell.
   - *Policy Action*: Deploy **Dedicated Bus Lanes** and **Transit Signal Priority (TSP)** at signalized junctions.
4. 🟠 **High-Friction Historic / Commercial Belt (Stop-and-Go)**
   - *Characteristics*: Speed $< 10$ km/h, high acceleration noise ($> 1.4\text{ m/s}^2$), extreme dwell ($> 40\%$).
   - *Policy Action*: Institute curbside parking bans, off-board smart card ticketing, and fleet rightsizing to 9m mini-buses.

---

## 🛠️ Project Architecture

```
urban_transit_clustering/
├── README.md                                    # Executive overview & deployment guide
├── PROJECT_REPORT.md                            # Comprehensive technical report for SIH jury
├── SIH_Urban_Transit_Clustering_Presentation.pptx # Compiled 11-slide pitch presentation
├── generate_pitch_deck.py                       # Automated PowerPoint generation script
├── main.py                                      # End-to-end CLI ML pipeline orchestrator
├── app.py                                       # Flask REST API & Web Dashboard backend
├── data/
│   ├── raw_transit_data.csv                     # Raw transit telemetry (1,200+ observations)
│   └── processed_route_features.csv             # Standardized multi-dimensional route features
├── src/
│   ├── __init__.py
│   ├── data_generator.py                        # Realistic AVL/GTFS multi-corridor telemetry simulator
│   ├── preprocessor.py                          # Missing value KNN imputer & StandardScaler
│   ├── feature_engineering.py                   # Temporal & movement transit indicator construction
│   ├── distance_metrics.py                      # Euclidean vs. Manhattan mathematical comparator
│   ├── clustering.py                            # K-Means++ & Hierarchical Linkages (Ward/Complete/Avg/Single)
│   ├── dimensionality_reduction.py              # PCA Scree decomposition & factor loadings biplot
│   ├── validation.py                            # Silhouette, Davies-Bouldin & 40-fold Bootstrap ARI stability
│   └── interpretation.py                        # Domain archetype profiling & policy mapping
├── dashboard/
│   ├── index.html                               # High-tech interactive Leaflet GIS dashboard
│   ├── app.js                                   # Interactive visualizations & What-If simulator
│   └── dashboard_data.json                      # Pre-calculated clustering payload & coordinates
├── reports/
│   ├── clustering_metrics.json                  # Complete metric export
│   ├── distance_metric_comparison.png           # Dispersion & contrast histograms
│   ├── elbow_and_silhouette_evaluation.png      # Elbow & quality spectrum plots
│   ├── hierarchical_dendrogram_and_linkages.png # Dendrogram & linkage benchmark
│   └── pca_traffic_clusters_biplot.png          # 2D projection with factor loading arrows
└── tests/
    └── test_pipeline.py                         # 7 automated unit & integration tests
```

---

## ⚡ Quick Start & Execution

### 1. Run the Full ML Pipeline
```bash
python3 main.py --k 4
```
This generates the raw dataset, imputes missing values, engineers features, computes distance metrics, runs K-Means and Hierarchical clustering across all linkages, performs PCA, validates stability, generates publication plots in `reports/`, and compiles `SIH_Urban_Transit_Clustering_Presentation.pptx`.

### 2. Run the Automated Unit Tests
```bash
python3 -m unittest discover tests
```
Runs 7 comprehensive tests covering the entire data science pipeline.

### 3. Launch the Interactive Web Dashboard & API
```bash
python3 app.py
```
Open **`http://localhost:5050`** in any web browser to explore:
- Interactive Leaflet GIS map of the bus route network.
- PCA 2D/3D scatter visualization.
- Distance metric comparative analysis.
- Live "What-If" route classifier and municipal policy advisor.

---

## 👥 Authors & Smart India Hackathon Submission
- **Problem Statement**: Unsupervised Clustering of Urban Bus Routes Using Traffic Patterns
- **Track**: Smart Mobility & Intelligent Transportation Systems
- **Target Deployers**: Delhi Transport Corporation (DTC), Bangalore Metropolitan Transport Corporation (BMTC), Brihanmumbai Electric Supply and Transport (BEST).

