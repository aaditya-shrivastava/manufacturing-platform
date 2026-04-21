#!/bin/sh

# ============================================================
#  start.sh — Local Development Only
#  Starts all 3 Streamlit apps simultaneously.
#
#  Usage:
#    chmod +x start.sh
#    ./start.sh
#
#  Access:
#    App 1 - manufacturing-creator     → http://localhost:8500
#    App 2 - multi-agent-manufacturing → http://localhost:8501
#    App 3 - main-app                  → http://localhost:8502
# ============================================================

echo "========================================"
echo " Starting all 3 Streamlit apps..."
echo "========================================"

# ── App 1: manufacturing-creator (port 8500) ──
echo "[1/3] Starting manufacturing-creator on port 8500..."
streamlit run manufacturing-creator/app.py \
  --server.port=8500 \
  --server.address=0.0.0.0 \
  --server.headless=true &

# ── App 2: multi-agent-manufacturing (port 8501) ──
echo "[2/3] Starting multi-agent-manufacturing on port 8501..."
streamlit run multi-agent-manufacturing/app.py \
  --server.port=8501 \
  --server.address=0.0.0.0 \
  --server.headless=true &

# ── App 3: main-app (port 8502) ──
echo "[3/3] Starting main-app on port 8502..."
streamlit run app.py \
  --server.port=8502 \
  --server.address=0.0.0.0 \
  --server.headless=true

# Note: App 3 runs in foreground to keep the script alive.
# Killing this terminal will stop all 3 apps.