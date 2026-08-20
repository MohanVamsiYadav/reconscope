from flask import Flask, request, jsonify
from flask_cors import CORS
from urllib.parse import urlparse
import ipaddress
import re

from dns_recon import resolve_dns
from http_recon import http_recon
from rdap_recon import rdap_recon

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

DOMAIN_RE = re.compile(r"^(?=.{1,253}$)([A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?\.)+[A-Za-z]{2,63}$")

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
def home():
    return jsonify({"status": "ok", "service": "BLACK//AI Lab API"})

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
        return jsonify({"error": "Invalid domain or IP address."}), 400
    return jsonify({"success": True, "target": target, "dns": resolve_dns(target), "http": http_recon(target), "rdap": rdap_recon(target)})

@app.post("/api/assistant")
def assistant():
    data = request.get_json(silent=True) or {}
    message = str(data.get("message", "")).strip()
    target = str(data.get("target", "")).strip()
    if not message:
        return jsonify({"error": "Message is required"}), 400

    text = message.lower()
    if any(x in text for x in ["steal password", "steal credentials", "ransomware", "bypass authentication", "hack instagram", "hack facebook", "malware deployment"]):
        reply = "I can help with the same cybersecurity concept in an authorized lab, but I cannot provide instructions for compromising real accounts or systems. Try a DVWA, Juice Shop, Metasploitable, or CTF target instead."
    elif "nmap" in text or "scan" in text:
        reply = "For an authorized lab, start with service discovery. Example: nmap -sV <LAB_IP>. Review open ports, identify services and versions, then map findings to defensive remediation."
    elif "sql injection" in text or "sqli" in text:
        reply = "SQL injection occurs when untrusted input changes a database query's structure. In a lab such as DVWA, study the vulnerable query, observe the request/response, then fix it with parameterized queries and strict input handling."
    elif "xss" in text:
        reply = "XSS occurs when attacker-controlled content is interpreted as script in a user's browser. In a lab, compare reflected, stored, and DOM-based XSS, then mitigate with contextual output encoding, CSP, and safe DOM APIs."
    elif "privilege escalation" in text:
        reply = "For an authorized Linux lab, enumerate permissions, services, scheduled tasks, SUID files, capabilities, and configuration mistakes. Document the finding and remediate the vulnerable permission or service configuration."
    else:
        reply = f"BLACK//AI is ready for authorized security research. Target context: {target or 'not specified'}. Ask about reconnaissance, web security, Linux/Windows labs, malware analysis, detection, or mitigation."
    return jsonify({"reply": reply, "mode": "authorized-lab"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
