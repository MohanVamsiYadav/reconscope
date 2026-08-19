import dns.resolver
import socket
import ipaddress

RECORD_TYPES = ["A", "AAAA", "MX", "NS", "TXT", "CNAME", "SOA", "CAA"]

def clean_domain(target):
    target = target.strip()
    if "://" in target:
        target = target.split("://", 1)[1]
    target = target.split("/", 1)[0]
    target = target.split(":", 1)[0]
    return target.strip(".").lower()

def resolve_dns(target):
    domain = clean_domain(target)
    result = {
        "domain": domain,
        "records": {},
        "resolved_ips": [],
        "reverse_dns": []
    }

    for record_type in RECORD_TYPES:
        try:
            answers = dns.resolver.resolve(domain, record_type, lifetime=5)
            result["records"][record_type] = [str(a) for a in answers]
        except Exception as e:
            result["records"][record_type] = []
            result.setdefault("errors", {})[record_type] = type(e).__name__

    for record_type in ("A", "AAAA"):
        result["resolved_ips"].extend(result["records"].get(record_type, []))

    for ip in result["resolved_ips"]:
        try:
            result["reverse_dns"].append({
                "ip": ip,
                "hostname": socket.gethostbyaddr(ip)[0]
            })
        except Exception:
            result["reverse_dns"].append({
                "ip": ip,
                "hostname": None
            })

    return result
