#!/usr/bin/env python3
import socket, sys, urllib.request, json
from datetime import datetime, timezone
import importlib.util
from pathlib import Path

LOG_DIR = Path("/workspace/logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_PATH = LOG_DIR / "devcontainer_health.log"
BANNER_PATH = LOG_DIR / "DEVCONTAINER_STATUS.txt"  # student-friendly summary

REQUIRED_PKGS = ["netmiko", "ntc_templates"]  # add "jinja2" if needed
DNS_HOSTS = [
    "github.com",
    "pypi.org",
    "google.com"
]
# Optional: include your sandbox hostname if stable:
# DNS_HOSTS.append("sandbox-iosxe-latest-1.cisco.com")

def now_iso():
    return datetime.now(timezone.utc).isoformat().replace("+00:00","Z")

def log(line: str):
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(line.rstrip() + "\n")

def banner(lines):
    with BANNER_PATH.open("w", encoding="utf-8") as f:
        for l in lines:
            f.write(l.rstrip() + "\n")

def check_dns():
    ok = True
    for host in DNS_HOSTS:
        try:
            ip = socket.gethostbyname(host)
            log(f"DNS_OK host={host} ip={ip}")
        except Exception as e:
            ok = False
            log(f"DNS_FAIL host={host} err={type(e).__name__}:{e}")
    return ok

def check_internet():
    # tiny HEAD request to a fast endpoint
    try:
        req = urllib.request.Request("https://www.google.com", method="HEAD")
        with urllib.request.urlopen(req, timeout=5) as resp:
            log(f"NET_OK status={resp.status}")
            return 200 <= resp.status < 400
    except Exception as e:
        log(f"NET_FAIL err={type(e).__name__}:{e}")
        return False

def check_packages():
    all_ok = True
    for pkg in REQUIRED_PKGS:
        spec = importlib.util.find_spec(pkg)
        if spec is not None:
            log(f"PKG_OK name={pkg}")
        else:
            all_ok = False
            log(f"PKG_FAIL name={pkg}")
    return all_ok

def main(deep=False):
    log(f"LAB2_HEALTH_START ts={now_iso()} deep={deep}")
    dns_ok = check_dns()
    net_ok = check_internet()
    pkg_ok = check_packages()
    overall = dns_ok and net_ok and pkg_ok
    log(f"LAB2_HEALTH_SUMMARY dns={dns_ok} net={net_ok} pkg={pkg_ok} overall={overall}")
    log(f"LAB2_HEALTH_END ts={now_iso()}")

    # Student-facing banner
    lines = [
        "================= DEVCONTAINER HEALTH =================",
        f"Time (UTC): {now_iso()}",
        f"DNS resolution: {'PASS' if dns_ok else 'FAIL'}",
        f"Internet reachability: {'PASS' if net_ok else 'FAIL'}",
        "Required Python packages:",
    ]
    for pkg in REQUIRED_PKGS:
        lines.append(f"  - {pkg}: {'OK' if importlib.util.find_spec(pkg) else 'MISSING'}")
    lines.append("Overall status: " + ("READY ✅" if overall else "NOT READY ❌"))
    lines.append("Details: logs/devcontainer_health.log")
    lines.append("=======================================================")
    banner(lines)

    # Exit code for CI or post-create script
    sys.exit(0 if overall else 1 if deep else 0)

if __name__ == "__main__":
    # deep=True on postCreate (will fail if unhealthy), deep=False on postStart (won't block)
    deep_flag = "--deep" in sys.argv
    main(deep=deep_flag)
