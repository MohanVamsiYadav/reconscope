from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from urllib.parse import urlparse
import ipaddress
import os
import re

from modules.dns_recon import resolve_dns
from modules.http_recon import http_recon
from modules.rdap_recon import rdap_recon

app = Flask(__name__, static_folder="static", static_url_path="")
CORS(app, resources={r"/api/*": {"origins": "*"}})

DOMAIN_RE = re.compile(
    r"^(?=.{1,253}$)([A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?\.)+[A-Za-z]{2,63}$"
)

def normalize_target(value):
    value = value.strip()
    if "://" not in value:
        value = "https://" + value
    parsed = urlparse(value)
    return parsed.hostname.lower() if parsed.hostname else ""

def valid_target(target):
    try:
        ipaddress.ip_address(target)
        return True
    except ValueError:
        return bool(DOMAIN_RE.fullmatch(target))

@app.get("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

@app.get("/<path:path>")
def static_files(path):
    return send_from_directory(app.static_folder, path)

@app.get("/api/health")
def health():
    return jsonify({"status": "healthy", "service": "ReconScope"})

@app.post("/api/recon")
def recon():
    data = request.get_json(silent=True) or {}
    raw_target = str(data.get("target", "")).strip()

    if not raw_target:
        return jsonify({"error": "Target is required"}), 400

    target = normalize_target(raw_target)

    if not valid_target(target):
        return jsonify({"error": "Invalid target. Enter a domain or IP address."}), 400

    return jsonify({
        "success": True,
        "target": target,
        "dns": resolve_dns(target),
        "http": http_recon(target),
        "rdap": rdap_recon(target)
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
