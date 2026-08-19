import requests
from urllib.parse import urlparse

def http_recon(target):
    target = target.strip()
    if "://" not in target:
        candidates = [f"https://{target}", f"http://{target}"]
    else:
        candidates = [target]

    errors = []

    for url in candidates:
        try:
            response = requests.get(
                url,
                timeout=8,
                allow_redirects=True,
                headers={"User-Agent": "ReconScope/2.0 Educational-Lab"}
            )
            return {
                "reachable": True,
                "requested_url": url,
                "final_url": response.url,
                "status_code": response.status_code,
                "reason": response.reason,
                "server": response.headers.get("Server"),
                "content_type": response.headers.get("Content-Type"),
                "content_length": response.headers.get("Content-Length"),
                "headers": dict(response.headers)
            }
        except requests.RequestException as e:
            errors.append(f"{url}: {e}")

    return {
        "reachable": False,
        "error": " | ".join(errors)
    }
