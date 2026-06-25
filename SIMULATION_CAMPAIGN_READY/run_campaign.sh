#!/usr/bin/env bash
# RPL-ClusterIDS — Phase 2 campaign launcher (Ubuntu + Cooja).
# Status: READY_FOR_SIMULATION
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SCRIPTS="${ROOT}/code_source_RPL_ClusterIDS/simulations/scripts"
DATA_REAL="${ROOT}/data/real"

usage() {
  echo "Usage: $0 [--dry-run | --pilot | --full]"
  exit 1
}

MODE="${1:-}"
case "${MODE}" in
  --dry-run)
    echo "[READY_FOR_SIMULATION] Campaign matrix:"
    column -t -s $'\t' "${ROOT}/SIMULATION_CAMPAIGN_READY/campaign_matrix.tsv" | head -20
    echo "... (see campaign_matrix.tsv for full factorial design)"
    ;;
  --pilot)
    echo "[READY_FOR_SIMULATION] Pilot: 50 nodes, 3 seeds, rank attack, CLUSTERIDS Balanced"
    bash "${SCRIPTS}/run_ids_campaign.sh" pilot
    ;;
  --full)
    echo "[READY_FOR_SIMULATION] Full campaign — requires CONTIKI_NG and Cooja"
    bash "${SCRIPTS}/run_ids_campaign.sh" full
    mkdir -p "${DATA_REAL}/raw_logs" "${DATA_REAL}/parsed" "${DATA_REAL}/aggregated"
    python3 "${SCRIPTS}/parse_cooja_ids_metrics.py" --logs "${DATA_REAL}/raw_logs" --out "${DATA_REAL}/parsed"
    ;;
  *) usage ;;
esac
