// State Store
const state = {
    dataset: null,
    routeShapes: [],
    algorithm: "kmeans",
    n_clusters: 4,
    linkage: "ward",
    metric: "euclidean",
    imputation: "knn",
    scaler: "standard",
    is3D: false,
    clusterLabelsMap: {},
    pcaData: null,
    clusteringRes: null,
    profiles: []
};

document.addEventListener("DOMContentLoaded", () => {
    initTabNavigation();
    initControls();
    loadInitialData();
});

function initTabNavigation() {
    const navItems = document.querySelectorAll(".nav-item");
    navItems.forEach(item => {
        item.addEventListener("click", () => {
            navItems.forEach(n => n.classList.remove("active"));
            item.classList.add("active");
            
            const tabId = item.getAttribute("data-tab");
            document.querySelectorAll(".tab-content").forEach(t => t.classList.remove("active"));
            document.getElementById(`tab-${tabId}`).classList.add("active");
            
            // Update Title
            const titleMap = {
                "overview": "Transit Overview & Data Catalog",
                "distance": "Distance Metric & Preprocessing Analysis",
                "clustering": "Clustering Studio & PCA Dimensionality Reduction",
                "validation": "Cluster Quality & Stability Benchmark Suite",
                "map-profiles": "Spatial Bus Network Map & Operational Profiles"
            };
            document.getElementById("current-tab-title").innerText = titleMap[tabId] || "Analytics Dashboard";
            
            // Trigger Map / Plotly Resize
            if (tabId === "map-profiles" && state.routeShapes.length > 0) {
                setTimeout(() => updateMapRoutes(state.routeShapes, state.clusterLabelsMap), 100);
            } else if (tabId === "clustering" && state.pcaData) {
                setTimeout(() => renderPlotlyPCA(state.pcaData, state.is3D), 100);
            }
        });
    });
}

function initControls() {
    const kSlider = document.getElementById("param-k");
    const kValSpan = document.getElementById("val-k");
    const algSelect = document.getElementById("param-algorithm");
    const linkageGroup = document.getElementById("linkage-group");
    const linkageSelect = document.getElementById("param-linkage");
    const metricSelect = document.getElementById("param-metric");
    const runBtn = document.getElementById("btn-run-pipeline");

    kSlider.addEventListener("input", (e) => {
        kValSpan.innerText = e.target.value;
        state.n_clusters = parseInt(e.target.value);
    });

    algSelect.addEventListener("change", (e) => {
        state.algorithm = e.target.value;
        linkageGroup.style.display = state.algorithm === "hierarchical" ? "flex" : "none";
        document.getElementById("dendrogram-card").style.display = state.algorithm === "hierarchical" ? "block" : "none";
    });

    linkageSelect.addEventListener("change", (e) => state.linkage = e.target.value);
    metricSelect.addEventListener("change", (e) => state.metric = e.target.value);

    runBtn.addEventListener("click", () => executeFullPipeline());

    document.getElementById("btn-pca-2d").addEventListener("click", (e) => {
        document.getElementById("btn-pca-2d").classList.add("active");
        document.getElementById("btn-pca-3d").classList.remove("active");
        state.is3D = false;
        if (state.pcaData) renderPlotlyPCA(state.pcaData, false);
    });

    document.getElementById("btn-pca-3d").addEventListener("click", (e) => {
        document.getElementById("btn-pca-3d").classList.add("active");
        document.getElementById("btn-pca-2d").classList.remove("active");
        state.is3D = true;
        if (state.pcaData) renderPlotlyPCA(state.pcaData, true);
    });

    // Report Modal triggers
    document.getElementById("btn-export").addEventListener("click", () => openReportModal());
    document.getElementById("btn-close-modal").addEventListener("click", () => {
        document.getElementById("report-modal").style.display = "none";
    });
    document.getElementById("btn-copy-report").addEventListener("click", () => {
        const text = document.getElementById("report-text-container").innerText;
        navigator.clipboard.writeText(text);
        alert("Markdown Report copied to clipboard!");
    });
}

async function loadInitialData() {
    try {
        const res = await fetch("/api/data");
        const data = await res.json();
        state.dataset = data;
        state.routeShapes = data.route_shapes;
        
        document.getElementById("kpi-routes").innerText = data.total_routes;
        
        const missingCount = Object.values(data.missing_counts).reduce((a, b) => a + b, 0);
        document.getElementById("kpi-missing").innerText = `${missingCount} Imputed`;

        renderDatasetTable(data.head);
        executeFullPipeline();
    } catch (err) {
        console.error("Failed to load initial dataset:", err);
    }
}

function renderDatasetTable(rows) {
    const tbody = document.querySelector("#dataset-table tbody");
    tbody.innerHTML = "";
    rows.forEach(r => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td><strong>${r.route_id}</strong></td>
            <td>${r.route_name}</td>
            <td><span class="badge">${r.time_window}</span></td>
            <td>${r.length_km}</td>
            <td>${r.avg_speed_kmh}</td>
            <td>${r.speed_variance !== null ? r.speed_variance : '<span style="color:#ef4444;">NaN</span>'}</td>
            <td>${r.peak_congestion_index}</td>
            <td>${r.stop_density_per_km}</td>
            <td>${r.dwell_time_per_stop_sec !== null ? r.dwell_time_per_stop_sec : '<span style="color:#ef4444;">NaN</span>'}</td>
            <td>${r.schedule_delay_index}</td>
            <td>${r.reliability_score}</td>
        `;
        tbody.appendChild(tr);
    });
}

async function executeFullPipeline() {
    const payload = {
        algorithm: state.algorithm,
        n_clusters: state.n_clusters,
        linkage: state.linkage,
        metric: state.metric,
        imputation_strategy: state.imputation,
        scaler_type: state.scaler
    };

    try {
        // 1. Distance Compare
        const distRes = await fetch("/api/distance-compare", {
            method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload)
        }).then(r => r.json());

        document.getElementById("euc-contrast").innerText = `Contrast: ${distRes.euclidean.stats.contrast_ratio.toFixed(3)}`;
        document.getElementById("euc-sil").innerText = distRes.euclidean.silhouette.toFixed(3);
        document.getElementById("euc-mean").innerText = distRes.euclidean.stats.mean.toFixed(2);

        document.getElementById("man-contrast").innerText = `Contrast: ${distRes.manhattan.stats.contrast_ratio.toFixed(3)}`;
        document.getElementById("man-sil").innerText = distRes.manhattan.silhouette.toFixed(3);
        document.getElementById("man-mean").innerText = distRes.manhattan.stats.mean.toFixed(2);

        document.getElementById("distance-rec-text").innerText = distRes.recommendation;
        renderDistanceDistributionChart(distRes.euclidean.sample_matrix, distRes.manhattan.sample_matrix);

        // 2. Cluster & PCA
        const clusterRes = await fetch("/api/cluster", {
            method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload)
        }).then(r => r.json());

        state.clusteringRes = clusterRes.clustering;
        document.getElementById("kpi-silhouette").innerText = clusterRes.clustering.silhouette_score;
        document.getElementById("kpi-dbi").innerText = clusterRes.clustering.davies_bouldin_index;

        renderKMeansSweepChart(clusterRes.kmeans_sweep, clusterRes.optimal_k_kmeans);
        if (clusterRes.dendrogram) renderDendrogramChart(clusterRes.dendrogram);

        // Build route_id -> cluster label mapping
        const labels = clusterRes.clustering.labels;
        state.clusterLabelsMap = {};
        state.dataset.head.forEach((r, idx) => {
            state.clusterLabelsMap[r.route_id] = labels[idx % labels.length];
        });

        // 3. PCA
        const pcaRes = await fetch("/api/pca", {
            method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload)
        }).then(r => r.json());

        state.pcaData = pcaRes;
        renderPlotlyPCA(pcaRes, state.is3D);

        // 4. Quality & Stability
        const evalRes = await fetch("/api/evaluate", {
            method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload)
        }).then(r => r.json());

        document.getElementById("val-sil-score").innerText = evalRes.quality.silhouette;
        document.getElementById("val-dbi-score").innerText = evalRes.quality.davies_bouldin;
        document.getElementById("val-chi-score").innerText = evalRes.quality.calinski_harabasz;

        document.getElementById("val-stability-ari").innerText = evalRes.stability.mean_ari;
        document.getElementById("val-stability-badge").innerText = evalRes.stability.stability_rating;

        renderBenchmarkTable(evalRes.benchmarks);

        // 5. Profiles
        const profRes = await fetch("/api/profiles", {
            method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload)
        }).then(r => r.json());

        state.profiles = profRes;
        renderProfileCards(profRes);

        // Update Map
        updateMapRoutes(state.routeShapes, state.clusterLabelsMap);

    } catch (err) {
        console.error("Pipeline execution failed:", err);
    }
}

function renderBenchmarkTable(benchmarks) {
    const tbody = document.querySelector("#benchmark-table tbody");
    tbody.innerHTML = "";
    benchmarks.slice(0, 10).forEach(b => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td><strong>${b.algorithm} ${b.linkage !== 'N/A' ? '('+b.linkage+')' : ''}</strong></td>
            <td>${b.k}</td>
            <td><span style="color:#10b981;">${b.silhouette}</span></td>
            <td>${b.davies_bouldin}</td>
        `;
        tbody.appendChild(tr);
    });
}

function renderProfileCards(profiles) {
    const container = document.getElementById("profiles-container");
    container.innerHTML = "";

    profiles.forEach(p => {
        const card = document.createElement("div");
        card.className = "profile-card";
        card.innerHTML = `
            <div class="profile-card-header">
                <h4 style="font-family:var(--font-heading); font-size:1.1rem; color:#fff;">Cluster ${p.cluster_id}: ${p.title}</h4>
                <span class="profile-badge" style="background:${p.badge_color};">${p.percentage}% (${p.route_count} routes)</span>
            </div>
            <p>${p.description}</p>
            <div class="profile-rec">
                <strong><i class="fa-solid fa-lightbulb"></i> Actionable Recommendation:</strong><br>
                ${p.recommendation}
            </div>
        `;
        container.appendChild(card);
    });
}

async function openReportModal() {
    const modal = document.getElementById("report-modal");
    const container = document.getElementById("report-text-container");
    container.innerText = "Generating report...";
    modal.style.display = "flex";

    try {
        const res = await fetch("/api/export-report", {
            method: "POST", headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ algorithm: state.algorithm, n_clusters: state.n_clusters })
        }).then(r => r.json());
        container.innerText = res.markdown;
    } catch (err) {
        container.innerText = "Failed to generate report.";
    }
}
