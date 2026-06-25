# SIMULATION_CAMPAIGN_READY

**Status:** `READY_FOR_SIMULATION`  
**Execute on:** Ubuntu with Contiki-NG 4.8+ and Cooja  
**Do not run on Windows** — this folder prepares Phase 2 only.

## Purpose

Complete experimental campaign specification for the IEEE IoT Journal submission of RPL-ClusterIDS.

## Contents

| Path | Description |
|------|-------------|
| `scenarios/` | Per-scale topology and timing (50–500 nodes) |
| `attacks/` | Attack injection parameters |
| `metrics/METRICS.md` | Metric definitions and log format |
| `run_campaign.sh` | Master launcher (calls `code_source_RPL_ClusterIDS/simulations/scripts/`) |
| `campaign_matrix.tsv` | Full factorial design |
| `seeds.txt` | 20 random seeds (s001–s020) |

## Campaign Design

- **Variants:** B1, B2, B3, CLUSTERIDS
- **Node counts:** 50, 100, 200, 300, 500
- **Topologies:** grid + random (per scale)
- **Attacks:** Rank, Selective Forwarding, Wormhole, DAO Flooding, Mixed
- **Seeds:** 20 per configuration (see `seeds.txt`)
- **Duration:** 3 h simulated time per run
- **Modes:** Full, Balanced, Eco (CLUSTERIDS only)

## Output Layout (Phase 2)

```
data/real/
  raw_logs/          # Cooja serial exports
  parsed/            # parse_cooja_ids_metrics.py output
  aggregated/        # per-metric CSV files
  statistics/        # CI, tests, summary tables
```

## Quick Start (Ubuntu)

```bash
export CONTIKI_NG=/path/to/contiki-ng
cd IDS_IOT/SIMULATION_CAMPAIGN_READY
./run_campaign.sh --dry-run    # validate matrix
./run_campaign.sh --pilot      # 50 nodes, 3 seeds, 30 min
./run_campaign.sh --full       # complete campaign
```

After completion, run from project root:

```bash
python3 scripts/statistics/compute_statistics.py --input data/real/aggregated
python3 scripts/python/generate_figures.py --csv data/real/aggregated --out Figures/
```
