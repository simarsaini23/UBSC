# UrbanFlow-AI: Unsupervised Urban Bus Route Clustering & Traffic Pattern Analytics Platform (SIH Level Project)

![SIH Solution](https://img.shields.io/badge/Smart%20India%20Hackathon-SIH%20Level%20Project-blue?style=for-the-badge&logo=target)
![Python](https://img.shields.io/badge/Python-3.12-brightgreen?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.1-black?style=for-the-badge&logo=flask)
![Scikit-Learn](https://img.shields.io/badge/scikit--learn-ML%20Engine-orange?style=for-the-badge&logo=scikit-learn)

An end-to-end Smart India Hackathon (SIH) grade solution for unsupervised clustering of urban bus routes using traffic patterns, movement dynamics, and temporal transit metrics.

---

## 🎯 Objectives & Outcome Alignment

### Objective 1: Transit Dataset Preparation & Distance Metric Analysis
- **Route-level Transit Dataset**: Generates and ingests temporal observations (160+ bus routes across AM Peak, Midday, PM Peak, and Night windows).
- **Missing Value Handling**: Implements K-Nearest Neighbors (KNN, $k=5$) and Median Imputation for missing observations.
- **Feature Engineering & Scaling**: Constructs composite movement indicators (`speed_congestion_ratio`, `stop_dwell_factor`) and applies `StandardScaler` / `MinMaxScaler`.
- **Distance Suitability Evaluation**: Calculates pairwise Euclidean ($L_2$) and Manhattan ($L_1$) distance matrices, assessing distance variance contrast ratio $\frac{\sigma(D)}{\mu(D)}$ for high-dimensional transit data.

### Objective 2: Multi-Algorithm Clustering & Dimensionality Reduction
- **K-Means Clustering**: Parameter sweep over $k = 2 \dots 8$ tracking WCSS (Elbow method) and Silhouette curves.
- **Agglomerative Hierarchical Clustering**: Flexible linkage strategies (**Ward**, **Complete**, **Average**, **Single**) with dendrogram hierarchy extraction.
- **PCA Dimensionality Reduction**: 2D and 3D Principal Component Analysis with Explained Variance Ratios and Biplot feature loading vectors.

### Objective 3: Quality Evaluation, Stability & Operational Interpretation
- **Validation Metrics**: Calculates Silhouette Score ($S$), Davies-Bouldin Index ($DBI$), and Calinski-Harabasz Index ($CHI$).
- **Cluster Stability Analysis**: Subsamples data (80% bootstrap samples over 15 iterations) measuring partition drift via Adjusted Rand Index (ARI).
- **Operational Pattern Profiling**: Automatically maps clusters into real-world operational transit archetypes (*Downtown Congested Arterial*, *High-Speed Express Corridor*, *Suburban Feeder Line*, *Peak-Hour Bottleneck Route*, *Peripheral Connector*).
- **Interactive Visual Dashboard**: Leaflet.js spatial route map, Plotly.js 3D PCA projection space, dendrogram viewer, and report generator.

---

## 📐 Mathematical Formulation

### 1. Distance Metrics
- **Euclidean Distance ($L_2$ Norm)**:
  $$d_{Euc}(\mathbf{x}, \mathbf{y}) = \sqrt{\sum_{i=1}^{n} (x_i - y_i)^2}$$
- **Manhattan Distance ($L_1$ Norm)**:
  $$d_{Man}(\mathbf{x}, \mathbf{y}) = \sum_{i=1}^{n} |x_i - y_i|$$
- **Distance Contrast Ratio**:
  $$CR = \frac{\sigma(D)}{\mu(D) + \epsilon}$$

### 2. K-Means Within-Cluster Sum of Squares (WCSS / Inertia)
$$J(K) = \sum_{k=1}^{K} \sum_{\mathbf{x} \in C_k} ||\mathbf{x} - \boldsymbol{\mu}_k||^2$$

### 3. Ward's Linkage Criterion
$$\Delta(A, B) = \frac{n_A n_B}{n_A + n_B} ||\boldsymbol{\mu}_A - \boldsymbol{\mu}_B||^2$$

### 4. Silhouette Score
$$S(i) = \frac{b(i) - a(i)}{\max(a(i), b(i))}$$
*Where $a(i)$ is the mean intra-cluster distance and $b(i)$ is the mean nearest-cluster distance.*

### 5. Davies-Bouldin Index
$$DBI = \frac{1}{K} \sum_{i=1}^{K} \max_{j \neq i} \left( \frac{R_i + R_j}{d(\boldsymbol{\mu}_i, \boldsymbol{\mu}_j)} \right)$$

---

## 🏗️ Project Structure

```
supervised/
├── app.py                      # Flask REST API Microservice Backend
├── requirements.txt            # Dependency Manifest
├── test_pipeline.py            # End-to-End Automated Test Suite
├── README.md                   # Comprehensive SIH Documentation
├── data/
│   ├── transit_generator.py   # Realistic Urban Bus Route Dataset Generator
│   ├── urban_bus_transit_observations.csv
│   └── route_shapes.json       # GeoJSON Trajectory Coordinates
├── src/
│   ├── preprocessing.py       # Imputation, Feature Engineering & Scaling
│   ├── distance_metrics.py    # Euclidean vs Manhattan Matrix Analysis
│   ├── clustering_engine.py   # K-Means Sweep & Hierarchical Linkages
│   ├── pca_analysis.py        # 2D & 3D PCA Projection & Biplot Loadings
│   ├── evaluation.py          # Silhouette, DBI, CHI & Bootstrap Stability
│   └── profiler.py            # Operational Traffic Pattern Profiler
└── static/
    ├── index.html              # Modern Glassmorphic Dashboard Layout
    ├── css/style.css           # Custom CSS Theme & Glassmorphism Rules
    └── js/
        ├── app.js              # State Controller & API Interactivity
        ├── charts.js           # Plotly 2D/3D PCA & Chart.js Visualizations
        └── map.js              # Leaflet.js Spatial Network Route Map
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites
Ensure Python 3.10+ is installed on your system.

### 2. Environment Setup & Dependency Installation
```bash
# Create Virtual Environment
python3 -m venv venv

# Activate Virtual Environment
source venv/bin/activate  # On macOS/Linux
# or venv\Scripts\activate on Windows

# Install Dependencies
pip install -r requirements.txt
```

### 3. Run Pipeline Tests
Verify end-to-end machine learning algorithms and API endpoints:
```bash
python test_pipeline.py
```

### 4. Launch Web Application Dashboard
```bash
python app.py
```
Open your browser and navigate to: `http://localhost:5001`

---

## 🔌 REST API Endpoints Summary

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `GET /api/data` | `GET` | Returns raw dataset head, feature statistics, and GeoJSON shapes |
| `POST /api/preprocess` | `POST` | Executes missing value imputation and standard feature scaling |
| `POST /api/distance-compare` | `POST` | Computes Euclidean vs Manhattan distance metrics & contrast ratios |
| `POST /api/cluster` | `POST` | Executes K-Means or Hierarchical clustering & returns dendrogram data |
| `POST /api/pca` | `POST` | Generates 2D/3D PCA coordinate points & biplot feature loadings |
| `POST /api/evaluate` | `POST` | Evaluates Silhouette, Davies-Bouldin, and bootstrap ARI stability |
| `POST /api/profiles` | `POST` | Generates operational traffic pattern descriptions & recommendations |
| `POST /api/export-report` | `POST` | Compiles downloadable executive markdown analytical report |

---

## 📜 License
Developed for Smart India Hackathon (SIH) - Open Academic & Transit Research Use.
