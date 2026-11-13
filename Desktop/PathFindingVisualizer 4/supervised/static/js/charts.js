let kmeansSweepChart = null;
let distanceDistChart = null;
let dendrogramChart = null;

const COLOR_PALETTE = [
    "#ef4444", // Red
    "#10b981", // Emerald Green
    "#3b82f6", // Bright Blue
    "#f59e0b", // Amber
    "#8b5cf6", // Purple
    "#ec4899", // Pink
    "#06b6d4", // Cyan
    "#f97316"  // Orange
];

function renderKMeansSweepChart(sweepData, optimalK) {
    const ctx = document.getElementById("chart-kmeans-sweep");
    if (!ctx) return;
    
    const ks = sweepData.map(d => d.k);
    const inertias = sweepData.map(d => d.inertia);
    const sils = sweepData.map(d => d.silhouette_score);
    
    if (kmeansSweepChart) kmeansSweepChart.destroy();
    
    kmeansSweepChart = new Chart(ctx, {
        type: "line",
        data: {
            labels: ks,
            datasets: [
                {
                    label: "Inertia (Elbow WCSS)",
                    data: inertias,
                    borderColor: "#3b82f6",
                    backgroundColor: "rgba(59, 130, 246, 0.15)",
                    yAxisID: "y-inertia",
                    tension: 0.35,
                    fill: true,
                    pointRadius: 4,
                    pointHoverRadius: 7
                },
                {
                    label: "Silhouette Score",
                    data: sils,
                    borderColor: "#10b981",
                    backgroundColor: "rgba(16, 185, 129, 0.15)",
                    yAxisID: "y-sil",
                    tension: 0.35,
                    pointRadius: 4,
                    pointHoverRadius: 7
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { labels: { color: "#cbd5e1", font: { family: "Inter", weight: 600 } } }
            },
            scales: {
                x: {
                    title: { display: true, text: "Number of Clusters (k)", color: "#94a3b8", font: { weight: 600 } },
                    ticks: { color: "#94a3b8" },
                    grid: { color: "rgba(255, 255, 255, 0.06)" }
                },
                "y-inertia": {
                    type: "linear",
                    position: "left",
                    title: { display: true, text: "Inertia (WCSS)", color: "#3b82f6", font: { weight: 600 } },
                    ticks: { color: "#3b82f6" },
                    grid: { color: "rgba(255, 255, 255, 0.06)" }
                },
                "y-sil": {
                    type: "linear",
                    position: "right",
                    title: { display: true, text: "Silhouette Score", color: "#10b981", font: { weight: 600 } },
                    ticks: { color: "#10b981" },
                    grid: { drawOnChartArea: false }
                }
            }
        }
    });
}

function renderDistanceDistributionChart(eucMatrix, manMatrix) {
    const ctx = document.getElementById("chart-distance-dist");
    if (!ctx) return;

    // Flatten upper triangle
    const eucVals = [];
    const manVals = [];
    for (let i = 0; i < eucMatrix.length; i++) {
        for (let j = i + 1; j < eucMatrix[i].length; j++) {
            eucVals.push(eucMatrix[i][j]);
            manVals.push(manMatrix[i][j]);
        }
    }

    if (distanceDistChart) distanceDistChart.destroy();

    const numBins = 14;
    const eucMin = Math.min(...eucVals), eucMax = Math.max(...eucVals);
    const manMin = Math.min(...manVals), manMax = Math.max(...manVals);

    const stepEuc = (eucMax - eucMin) / numBins;
    const stepMan = (manMax - manMin) / numBins;

    const labels = Array.from({length: numBins}, (_, i) => `Bin ${i+1}`);
    const eucCounts = new Array(numBins).fill(0);
    const manCounts = new Array(numBins).fill(0);

    eucVals.forEach(v => {
        const bin = Math.min(numBins - 1, Math.floor((v - eucMin) / stepEuc));
        eucCounts[bin]++;
    });

    manVals.forEach(v => {
        const bin = Math.min(numBins - 1, Math.floor((v - manMin) / stepMan));
        manCounts[bin]++;
    });

    distanceDistChart = new Chart(ctx, {
        type: "bar",
        data: {
            labels: labels,
            datasets: [
                {
                    label: "Euclidean Distances (L2)",
                    data: eucCounts,
                    backgroundColor: "rgba(59, 130, 246, 0.7)",
                    borderColor: "#3b82f6",
                    borderWidth: 1.5
                },
                {
                    label: "Manhattan Distances (L1)",
                    data: manCounts,
                    backgroundColor: "rgba(245, 158, 11, 0.7)",
                    borderColor: "#f59e0b",
                    borderWidth: 1.5
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { labels: { color: "#cbd5e1", font: { family: "Inter", weight: 600 } } }
            },
            scales: {
                x: { ticks: { color: "#94a3b8" }, grid: { color: "rgba(255,255,255,0.06)" } },
                y: { ticks: { color: "#94a3b8" }, grid: { color: "rgba(255,255,255,0.06)" } }
            }
        }
    });
}

function renderPlotlyPCA(pcaData, is3D = false) {
    const container = document.getElementById("plotly-pca-container");
    if (!container || !pcaData || !pcaData.points) return;

    const points = pcaData.points;
    const clusters = [...new Set(points.map(p => p.cluster))].sort((a, b) => a - b);

    const traces = clusters.map(c => {
        const cPoints = points.filter(p => p.cluster === c);
        const color = COLOR_PALETTE[c % COLOR_PALETTE.length];

        if (is3D) {
            return {
                x: cPoints.map(p => p.pc1),
                y: cPoints.map(p => p.pc2),
                z: cPoints.map(p => p.pc3),
                text: cPoints.map(p => `<b>${p.route_name}</b><br>ID: ${p.route_id}<br>Cluster ${c}`),
                hoverinfo: "text",
                mode: "markers",
                type: "scatter3d",
                name: `Cluster ${c}`,
                marker: {
                    size: 6,
                    color: color,
                    opacity: 0.9,
                    line: { color: "#ffffff", width: 0.5 }
                }
            };
        } else {
            return {
                x: cPoints.map(p => p.pc1),
                y: cPoints.map(p => p.pc2),
                text: cPoints.map(p => `<b>${p.route_name}</b><br>ID: ${p.route_id}<br>Cluster ${c}`),
                hoverinfo: "text",
                mode: "markers",
                type: "scatter",
                name: `Cluster ${c}`,
                marker: {
                    size: 10,
                    color: color,
                    opacity: 0.9,
                    line: { color: "#ffffff", width: 1 }
                }
            };
        }
    });

    const pc1Var = pcaData.explained_variance_ratio ? (pcaData.explained_variance_ratio[0]*100).toFixed(1) : "0";
    const pc2Var = pcaData.explained_variance_ratio ? (pcaData.explained_variance_ratio[1]*100).toFixed(1) : "0";
    const pc3Var = (pcaData.explained_variance_ratio && pcaData.explained_variance_ratio[2]) ? (pcaData.explained_variance_ratio[2]*100).toFixed(1) : "0";

    const layout = {
        paper_bgcolor: "rgba(0,0,0,0)",
        plot_bgcolor: "rgba(0,0,0,0)",
        font: { color: "#cbd5e1", family: "Inter, sans-serif" },
        margin: { l: 50, r: 20, t: 30, b: 50 },
        legend: {
            orientation: "h",
            y: -0.18,
            font: { color: "#f8fafc", size: 12 }
        },
        xaxis: {
            title: { text: `PC1 (${pc1Var}% Variance)`, font: { color: "#f8fafc", size: 12, weight: 600 } },
            tickfont: { color: "#94a3b8" },
            gridcolor: "rgba(255,255,255,0.08)",
            zerolinecolor: "rgba(255,255,255,0.2)",
            zeroline: true
        },
        yaxis: {
            title: { text: `PC2 (${pc2Var}% Variance)`, font: { color: "#f8fafc", size: 12, weight: 600 } },
            tickfont: { color: "#94a3b8" },
            gridcolor: "rgba(255,255,255,0.08)",
            zerolinecolor: "rgba(255,255,255,0.2)",
            zeroline: true
        },
        scene: is3D ? {
            xaxis: { title: `PC1 (${pc1Var}%)`, gridcolor: "rgba(255,255,255,0.15)", tickfont: { color: "#94a3b8" } },
            yaxis: { title: `PC2 (${pc2Var}%)`, gridcolor: "rgba(255,255,255,0.15)", tickfont: { color: "#94a3b8" } },
            zaxis: { title: `PC3 (${pc3Var}%)`, gridcolor: "rgba(255,255,255,0.15)", tickfont: { color: "#94a3b8" } },
            bgcolor: "rgba(0,0,0,0)"
        } : undefined
    };

    Plotly.react(container, traces, layout, { responsive: true, displayModeBar: false });
    
    // Force Plotly resize to fit parent card container
    setTimeout(() => {
        Plotly.Plots.resize(container);
    }, 150);
}

function renderDendrogramChart(dendroData) {
    const ctx = document.getElementById("chart-dendrogram");
    if (!ctx || !dendroData) return;

    if (dendrogramChart) dendrogramChart.destroy();

    const icoords = dendroData.icoord;
    const dcoords = dendroData.dcoord;

    const datasets = [];
    for (let i = 0; i < icoords.length; i++) {
        const x = icoords[i];
        const y = dcoords[i];
        datasets.push({
            label: `Branch ${i}`,
            data: x.map((xv, idx) => ({ x: xv, y: y[idx] })),
            borderColor: "#8b5cf6",
            borderWidth: 1.5,
            showLine: true,
            pointRadius: 0
        });
    }

    dendrogramChart = new Chart(ctx, {
        type: "scatter",
        data: { datasets: datasets },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                x: { display: false },
                y: {
                    title: { display: true, text: "Distance / Height", color: "#94a3b8", font: { weight: 600 } },
                    ticks: { color: "#94a3b8" },
                    grid: { color: "rgba(255,255,255,0.06)" }
                }
            }
        }
    });
}
