#!/usr/bin/env bash
set -euo pipefail

LOG_CB="/workspace/logs/connect_basic.log"
mkdir -p /workspace/logs
touch "$LOG_CB"

now_iso() {
  python - <<'PY'
from datetime import datetime, timezone
print(datetime.now(timezone.utc).isoformat().replace("+00:00","Z"))
PY
}

log_cb() { printf '%s %s\n' "$1" "$(now_iso)" >> "$LOG_CB"; }

log_cb "LAB2_START ts="
log_cb "DEVCONTAINER_OK"
python --version >> "$LOG_CB" 2>&1 || true

# Deep health: fail container creation if unhealthy (students see banner)
python .devcontainer/health_check.py --deep || {
  echo
  echo "Devcontainer health check FAILED. See logs/DEVCONTAINER_STATUS.txt and logs/devcontainer_health.log"
  echo
  exit 1
}

# Package echoes for rubric convenience
python - <<'PY' >> "$LOG_CB" 2>&1
import importlib.util
for pkg in ("netmiko","ntc_templates"):
    print("PKG_OK:" if importlib.util.find_spec(pkg) else "PKG_FAIL:", pkg)
PY

log_cb "LAB2_END ts="
