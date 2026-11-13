"""
Flask REST API & Web Dashboard Server for Urban Bus Clustering System
Smart India Hackathon (SIH) Grade Implementation
"""

import json
import os
import numpy as np
from flask import Flask, jsonify, request, send_file, send_from_directory
from flask_cors import CORS

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DASHBOARD_DIR = os.path.join(BASE_DIR, "dashboard")
PRESENTATION_DIR = os.path.join(BASE_DIR, "presentation")
DATA_DIR = os.path.join(BASE_DIR, "data")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
DATA_JSON_PATH = os.path.join(DASHBOARD_DIR, "dashboard_data.json")
PPTX_PATH = os.path.join(BASE_DIR, "SIH_Urban_Transit_Clustering_Presentation.pptx")

app = Flask(__name__, static_folder=DASHBOARD_DIR)
CORS(app)

# Load cached clustering artifacts
cached_data = None
if os.path.exists(DATA_JSON_PATH):
    with open(DATA_JSON_PATH, "r") as f:
        cached_data = json.load(f)


@app.route("/")
def index():
    return send_from_directory(DASHBOARD_DIR, "index.html")


@app.route("/presentation")
@app.route("/presentation/")
def presentation_index():
    return send_from_directory(PRESENTATION_DIR, "index.html")


@app.route("/presentation/<path:filename>")
def presentation_static(filename):
    return send_from_directory(PRESENTATION_DIR, filename)


@app.route("/reports/<path:filename>")
def reports_static(filename):
    return send_from_directory(REPORTS_DIR, filename)


@app.route("/<path:filename>")
def static_files(filename):
    return send_from_directory(DASHBOARD_DIR, filename)


@app.route("/api/data", methods=["GET"])
def get_data():
    global cached_data
    if cached_data is None and os.path.exists(DATA_JSON_PATH):
        with open(DATA_JSON_PATH, "r") as f:
            cached_data = json.load(f)
    if cached_data is None:
        return jsonify({"error": "Dashboard data not generated. Run main.py first."}), 404
    return jsonify(cached_data)


@app.route("/api/predict", methods=["POST"])
def predict_route_archetype():
    """
    Classifies a proposed or monitored bus route in real-time
    based on operational telemetry parameters.
    """
    global cached_data
    if not cached_data or "cluster_profiles" not in cached_data:
        return jsonify({"error": "Clustering model not loaded"}), 400

    req = request.get_json() or {}
    speed = float(req.get("speed_kmh", 16.0))
    congestion = float(req.get("congestion_index", 1.45))
    dwell = float(req.get("dwell_ratio", 0.28))
    accel = float(req.get("accel_noise", 1.10))
    headway = float(req.get("headway_irreg", 0.32))

    profiles = cached_data["cluster_profiles"]
    best_cluster = 0
    min_dist = float("inf")
    distances = {}

    for cid_str, prof in profiles.items():
        cid = int(cid_str)
        cm = prof["centroid_metrics"]
        
        # Normalized Manhattan distance to centroid
        c_speed = cm.get("mean_speed_kmh", 20.0)
        c_cong = cm.get("mean_congestion_index", 1.4)
        c_dwell = cm.get("mean_dwell_ratio", 0.25)
        c_accel = cm.get("mean_accel_noise", 1.0)
        c_head = cm.get("mean_headway_irregularity", 0.3)

        d = (
            abs(speed - c_speed) / 20.0 +
            abs(congestion - c_cong) / 0.8 +
            abs(dwell - c_dwell) / 0.3 +
            abs(accel - c_accel) / 1.0 +
            abs(headway - c_head) / 0.4
        )
        distances[cid] = round(d, 3)
        if d < min_dist:
            min_dist = d
            best_cluster = cid

    champion_profile = profiles[str(best_cluster)]

    return jsonify({
        "assigned_cluster": best_cluster,
        "archetype_name": champion_profile["archetype_name"],
        "color": champion_profile["color"],
        "severity_level": champion_profile["severity_level"],
        "policy_recommendation": champion_profile["policy_recommendation"],
        "distance_to_centroids": distances,
        "radar_metrics": champion_profile["radar_metrics"]
    })


ZIP_PATH = os.path.join(BASE_DIR, "urban_transit_clustering_SIH_Project.zip")


@app.route("/api/download/zip", methods=["GET"])
def download_zip():
    if os.path.exists(ZIP_PATH):
        return send_file(ZIP_PATH, as_attachment=True, download_name="urban_transit_clustering_SIH_Project.zip")
    return jsonify({"error": "Zip archive not found"}), 404


@app.route("/api/download/pptx", methods=["GET"])
def download_pptx():
    if os.path.exists(PPTX_PATH):
        return send_file(PPTX_PATH, as_attachment=True, download_name="SIH_Urban_Transit_Clustering_Presentation.pptx")
    return jsonify({"error": "PPTX presentation not found"}), 404


@app.route("/api/download/report", methods=["GET"])
def download_report():
    if os.path.exists(DATA_JSON_PATH):
        return send_file(DATA_JSON_PATH, as_attachment=True, download_name="clustering_report.json")
    return jsonify({"error": "Report not found"}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=False)

