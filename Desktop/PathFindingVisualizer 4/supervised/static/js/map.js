let transitMap = null;
let routeLayers = [];

const CLUSTER_COLORS = [
    "#ef4444", // Cluster 0: Red
    "#10b981", // Cluster 1: Green
    "#3b82f6", // Cluster 2: Blue
    "#f59e0b", // Cluster 3: Amber
    "#8b5cf6", // Cluster 4: Purple
    "#ec4899", // Cluster 5: Pink
    "#14b8a6", // Cluster 6: Teal
    "#f97316"  // Cluster 7: Orange
];

function initTransitMap() {
    if (transitMap) {
        setTimeout(() => transitMap.invalidateSize(), 150);
        return;
    }
    
    const container = document.getElementById("leaflet-map");
    if (!container) return;
    
    // Default Delhi / Urban Grid center (28.6139, 77.2090)
    transitMap = L.map("leaflet-map").setView([28.6139, 77.2090], 11);
    
    // OpenStreetMap / CartoDB dark tile layer
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        maxZoom: 18
    }).addTo(transitMap);
    
    setTimeout(() => transitMap.invalidateSize(), 200);
}

function updateMapRoutes(routeShapes, clusterLabelsMap) {
    initTransitMap();
    if (!transitMap) return;

    // Force Leaflet to re-calculate container size when tab becomes visible
    transitMap.invalidateSize();

    // Clear existing polylines
    routeLayers.forEach(layer => transitMap.removeLayer(layer));
    routeLayers = [];

    if (!routeShapes || routeShapes.length === 0) return;

    const bounds = L.latLngBounds();

    routeShapes.forEach(route => {
        const routeId = route.route_id;
        const clusterId = clusterLabelsMap[routeId] !== undefined ? clusterLabelsMap[routeId] : 0;
        const color = CLUSTER_COLORS[clusterId % CLUSTER_COLORS.length];

        // Leaflet expects [lat, lon]
        const latLngs = route.coordinates.map(coord => [coord[1], coord[0]]);
        latLngs.forEach(ll => bounds.extend(ll));

        const polyline = L.polyline(latLngs, {
            color: color,
            weight: 5,
            opacity: 0.85
        }).addTo(transitMap);

        polyline.bindPopup(`
            <div style="font-family: var(--font-body, sans-serif); color: #0f172a; padding: 4px;">
                <h4 style="margin:0 0 6px; color:${color}; font-size: 14px; font-weight: 700;">${route.route_name}</h4>
                <p style="margin:0 0 4px; font-size:12px;"><strong>Route ID:</strong> ${route.route_id}</p>
                <p style="margin:0 0 4px; font-size:12px;"><strong>Cluster:</strong> Cluster ${clusterId}</p>
                <p style="margin:0; font-size:12px;"><strong>Archetype:</strong> ${route.archetype}</p>
            </div>
        `);

        routeLayers.push(polyline);
    });

    if (routeLayers.length > 0 && bounds.isValid()) {
        setTimeout(() => {
            transitMap.invalidateSize();
            transitMap.fitBounds(bounds, { padding: [30, 30] });
        }, 150);
    }
}
