from flask import Flask, request, jsonify
from flask_cors import CORS
from urllib.parse import urlparse
import ipaddress
import re

from modules.dns_recon import resolve_dns
from modules.http_recon import http_recon
from modules.rdap_recon import rdap_recon

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

DOMAIN_RE = re.compile(
    r"^(?=.{1,253}$)([A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?\.)+[A-Za-z]{2,63}$"
)

def normalize_target(value):
    value = value.strip()
    if "://" not in value:
        value = "https://" + value
    parsed = urlparse(value)
    host = parsed.hostname
    return host.lower() if host else ""

def valid_target(target):
    try:
        ipaddress.ip_address(target)
        return True
    except ValueError:
        return bool(DOMAIN_RE.fullmatch(target))

@app.get("/")
def home():
    return jsonify({
        "status": "ok",
        "service": "ReconScope API",
        "message": "Backend is working"
    })

@app.get("/api/health")
def health():
    return jsonify({"status": "healthy"})

@app.post("/api/recon")
def recon():
    data = request.get_json(silent=True) or {}
    raw_target = str(data.get("target", "")).strip()

    if not raw_target:
        return jsonify({"error": "Target is required"}), 400

    target = normalize_target(raw_target)

    if not valid_target(target):
        return jsonify({
            "error": "Invalid target. Enter a domain such as example.com or an IP address."
        }), 400

    dns = resolve_dns(target)
    http = http_recon(target)
    rdap = rdap_recon(target)

    return jsonify({
        "success": True,
        "target": target,
        "dns": dns,
        "http": http,
        "rdap": rdap
    })

if __name__ == "__main__":
    print("\nReconScope API")
    print("Open frontend at: http://127.0.0.1:8000")
    print("API health:       http://127.0.0.1:5000/api/health\n")
    app.run(host="127.0.0.1", port=5000, debug=True)
