# Phase 2 — Ubuntu Campaign Command Summary

**Generated:** 2026-06-17  
**Reference:** `UBUNTU_EXECUTION_PLAN.md` for full instructions.

---

## Prerequisites (Ubuntu 22.04)

```bash
# System packages
sudo apt install -y build-essential git ant openjdk-11-jdk python3 python3-pip \
  python3-venv gcc-arm-none-eabi lib32z1 curl wget unzip texlive-full

# Python
python3 -m venv .venv && source .venv/bin/activate
pip install numpy scipy pandas matplotlib

# Contiki-NG
cd $HOME && git clone https://github.com/contiki-ng/contiki-ng.git
cd contiki-ng && git checkout release/v4.8
export CONTIKI_NG=$HOME/contiki-ng
```

---

## Gate G1 — Smoke Build

```bash
export IDS_ROOT=/path/to/IDS_IOT
export CLUSTERIDS=$IDS_ROOT/code_source_RPL_ClusterIDS
cd $CLUSTERIDS
make clean && make TARGET=cooja IDS_VARIANT=CLUSTERIDS
```

**Expected:** Build succeeds (exit 0).

---

## Gate G2 — Smoke Simulation

```bash
cd $CLUSTERIDS/simulations
python3 scripts/generate_campaign_csc.py --nodes 3 --out cooja/ids-smoke-3nodes.csc
NUM_SEEDS=1 SIM_TIMEOUT_MS=90000 ./scripts/run_ids_campaign.sh smoke
```

**Expected:** Log contains `METRIC,...` lines per `LOG_FORMAT.md`.

---

## Gate G3 — Parse Pipeline

```bash
python3 $CLUSTERIDS/simulations/scripts/parse_cooja_ids_metrics.py \
  --logs $CLUSTERIDS/simulations/logs/ids_campaign/ \
  --out $IDS_ROOT/data/real/parsed/
```

**Expected:** CSVs in `data/real/parsed/`.

---

## Gate G4 — Pilot Campaign (50 nodes, 3 seeds)

```bash
cd $IDS_ROOT/SIMULATION_CAMPAIGN_READY
./run_campaign.sh --dry-run        # validate matrix
./run_campaign.sh --pilot          # 50 nodes, 3 seeds, rank attack, ~30 min
```

**Validate:**
```bash
ls -la $IDS_ROOT/data/real/raw_logs/
python3 $IDS_ROOT/scripts/statistics/compute_statistics.py \
  --input $IDS_ROOT/data/real/aggregated --dry-run
```

---

## Gate G5 — Full Campaign

**Campaign scope:** 33 configurations × 20 seeds (see `campaign_matrix.tsv`).

```bash
cd $IDS_ROOT/SIMULATION_CAMPAIGN_READY
nohup ./run_campaign.sh --full > campaign.log 2>&1 &
tail -f campaign.log
```

**Monitor:**
```bash
du -sh $IDS_ROOT/data/real/
```

**Expected wall time:** 48–120 h (depends on CPU).

---

## Gate G5b — Ablation Variants (rows 30–33)

Built as separate firmware variants. From `ABLATION_VARIANTS.md`:

```bash
cd $CLUSTERIDS
make TARGET=cooja IDS_VARIANT=CLUSTERIDS IDS_ABLATION=NO_CLUSTER
make TARGET=cooja IDS_VARIANT=CLUSTERIDS IDS_ABLATION=NO_ML
make TARGET=cooja IDS_VARIANT=CLUSTERIDS IDS_ABLATION=NO_CONTEXT
make TARGET=cooja IDS_VARIANT=CLUSTERIDS IDS_ABLATION=NO_ENERGY
```

---

## Post-Processing Pipeline

```bash
# 1. Aggregate metrics (8 output CSVs expected)
#    data/real/aggregated/{detection_rate,detection_latency,fpr,
#                         energy_overhead,alert_overhead,cluster_stability,
#                         temporal_detection,operating_modes}.csv

# 2. Compute statistics
python3 $IDS_ROOT/scripts/statistics/compute_statistics.py \
  --input $IDS_ROOT/data/real/aggregated \
  --output $IDS_ROOT/data/real/statistics

# 3. Generate figures (Figs 4–11)
python3 $IDS_ROOT/scripts/python/generate_figures.py \
  --csv $IDS_ROOT/data/real/aggregated \
  --out $IDS_ROOT/Figures/
```

---

## Gate G6 — Camera-Ready PDF

```bash
cd $IDS_ROOT
pdflatex main-ieee.tex && bibtex main-ieee && pdflatex main-ieee.tex && pdflatex main-ieee.tex
```

**Verify:** 11–13 pages, no `EST.` markers, all figures rendered from real data.

---

## Matrix Summary

| Scale | Attacks | Variants | Seeds | Rows |
|-------|---------|----------|-------|------|
| 50 | rank, sel_fwd, wormhole, dao_flood, mixed | B1, B2, B3, CLUSTERIDS (+ modes) | 20 | 1–23 |
| 100 | rank, mixed | CLUSTERIDS | 20 | 24–25 |
| 200 | mixed (grid + random) | CLUSTERIDS | 20 | 26–27 |
| 300 | mixed | CLUSTERIDS | 20 | 28 |
| 500 | mixed | CLUSTERIDS | 20 | 29 |
| 50 (ablation) | mixed | NOCLUS, NOML, NOCTX, NOENR | 20 | 30–33 |

**Total configurations:** 33 rows × 20 seeds = **660 simulation runs**.
