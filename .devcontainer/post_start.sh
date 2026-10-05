#!/usr/bin/env bash
set -euo pipefail

# Quick, non-blocking health check (won't fail the container)
python .devcontainer/health_check.py || true

# Show student banner in terminal once per session
if [ -f "/workspace/logs/DEVCONTAINER_STATUS.txt" ]; then
  echo
  cat /workspace/logs/DEVCONTAINER_STATUS.txt || true
  echo
fi
