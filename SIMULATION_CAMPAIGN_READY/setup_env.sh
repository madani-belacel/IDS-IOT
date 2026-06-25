#!/usr/bin/env bash
# RPL-ClusterIDS — Phase 2 environment setup
# Run: bash setup_env.sh
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
echo "[SETUP] RPL-ClusterIDS environment setup"
echo "========================================"

# ── 1. System packages ──────────────────────────────────────────
echo ""
echo "[1/6] Installing system packages (sudo required)..."
sudo apt update -qq
sudo apt install -y openjdk-17-jdk ant gcc-arm-none-eabi python3-pip

# ── 2. Python packages ──────────────────────────────────────────
echo ""
echo "[2/6] Installing Python packages..."
pip3 install --user numpy scipy pandas matplotlib 2>&1 | tail -3

# ── 3. Set CONTIKI_NG ───────────────────────────────────────────
echo ""
echo "[3/6] Setting CONTIKI_NG environment variable..."
CONTIKI_NG="${HOME}/contiki-ng"
if ! grep -q "CONTIKI_NG" ~/.bashrc; then
  echo "export CONTIKI_NG=${CONTIKI_NG}" >> ~/.bashrc
  echo "export PATH=\$PATH:\$CONTIKI_NG/tools/cooja" >> ~/.bashrc
fi
export CONTIKI_NG="${CONTIKI_NG}"
echo "CONTIKI_NG=${CONTIKI_NG}"

# ── 4. Verify tools ─────────────────────────────────────────────
echo ""
echo "[4/6] Verifying tools..."
java -version 2>&1 | head -1
ant -version 2>&1 | head -1
arm-none-eabi-gcc --version 2>&1 | head -1
python3 --version 2>&1
python3 -c "import numpy; import scipy; import pandas; import matplotlib; print('Python packages OK')"

# ── 5. Build Cooja ──────────────────────────────────────────────
echo ""
echo "[5/6] Building Cooja..."
cd ${CONTIKI_NG}/tools/cooja
./gradlew build 2>&1 | tail -5
ls dist/cooja*.jar 2>/dev/null && echo "Cooja built OK" || echo "Cooja build FAILED"

# ── 6. Smoke build ──────────────────────────────────────────────
echo ""
echo "[6/6] Smoke build firmware..."
cd ${ROOT}/code_source_RPL_ClusterIDS
make clean 2>/dev/null || true
make TARGET=cooja IDS_VARIANT=CLUSTERIDS 2>&1 | tail -5

echo ""
echo "========================================"
echo "[SETUP] Done."
echo "Next: Gate G2 — smoke simulation"
echo "  cd ${ROOT}/SIMULATION_CAMPAIGN_READY"
echo "  bash run_campaign.sh --dry-run"
