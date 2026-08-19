import requests
import ipaddress

def rdap_recon(target):
    value = target.strip()
    if "://" in value:
        value = value.split("://", 1)[1]
    value = value.split("/", 1)[0].split(":", 1)[0]

    try:
        ipaddress.ip_address(value)
        object_type = "ip"
    except ValueError:
        object_type = "domain"

    url = f"https://rdap.org/{object_type}/{value}"

    try:
        response = requests.get(
            url,
            timeout=10,
            allow_redirects=True,
            headers={"User-Agent": "ReconScope/2.0 Educational-Lab"}
        )

        if response.status_code >= 400:
            return {
                "available": False,
                "status_code": response.status_code,
                "error": f"RDAP returned HTTP {response.status_code}"
            }

        data = response.json()

        return {
            "available": True,
            "object_type": object_type,
            "status_code": response.status_code,
            "handle": data.get("handle"),
            "name": data.get("ldhName") or data.get("name"),
            "status": data.get("status", []),
            "nameservers": [
                ns.get("ldhName")
                for ns in data.get("nameservers", [])
                if ns.get("ldhName")
            ],
            "raw": data
        }

    except requests.RequestException as e:
        return {"available": False, "error": str(e)}
    except ValueError:
        return {"available": False, "error": "RDAP returned non-JSON data"}
