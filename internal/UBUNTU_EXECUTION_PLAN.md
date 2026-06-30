# RPL-ClusterIDS — UBUNTU EXECUTION PLAN

**Phase:** 2 (execution) — prepared in Phase 1.5  
**Target OS:** Ubuntu 22.04 LTS (64-bit)  
**Project root:** `IDS_IOT/`  
**Do not run full campaign on Windows.**

---

## Overview

```
Install toolchain → Clone/sync project → Smoke build → Smoke sim
    → Pilot campaign (50n, 3 seeds) → Validate pipeline
    → Full campaign → Statistics → Figures → LaTeX update → PDF
```

**Estimated wall time:**
- Setup: 2–4 h
- Smoke: 30 min
- Pilot: 4–8 h
- Full campaign: 48–120 h (depends on CPU; run overnight)

---

## Step 0 — Hardware / VM Requirements

| Resource | Minimum | Recommended |
|----------|---------|-------------|
| CPU | 4 cores | 8+ cores |
| RAM | 8 GB | 16 GB |
| Disk | 30 GB free | 60 GB free |
| OS | Ubuntu 22.04 | Ubuntu 22.04 |

---

## Step 1 — System Packages

```bash
sudo apt update
sudo apt install -y \
  build-essential \
  git \
  ant \
  openjdk-11-jdk \
  python3 \
  python3-pip \
  python3-venv \
  gcc-arm-none-eabi \
  lib32z1 \
  curl \
  wget \
  unzip \
  texlive-full
```

Verify:
```bash
java -version        # openjdk 11+
arm-none-eabi-gcc --version
python3 --version    # 3.10+
```

---

## Step 2 — Python Environment

```bash
cd /path/to/IDS_IOT
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install numpy scipy pandas matplotlib
```

---

## Step 3 — Contiki-NG

```bash
export HOME=/home/$USER
cd $HOME
git clone https://github.com/contiki-ng/contiki-ng.git
cd contiki-ng
git checkout release/v4.8   # match manuscript Table V
export CONTIKI_NG=$HOME/contiki-ng
echo 'export CONTIKI_NG=$HOME/contiki-ng' >> ~/.bashrc
source ~/.bashrc
```

Optional — add to `~/.bashrc`:
```bash
export PATH=$CONTIKI_NG/tools/cooja:$PATH
```

---

## Step 4 — Sync RPL-ClusterIDS Firmware

Copy or clone project so this path exists:
```bash
export IDS_ROOT=/path/to/IDS_IOT
export CLUSTERIDS=$IDS_ROOT/code_source_RPL_ClusterIDS
```

---

## Step 5 — Smoke Build (Gate G1)

```bash
cd $CLUSTERIDS
make clean
make TARGET=cooja IDS_VARIANT=CLUSTERIDS
```

**Expected:** `clusterids-node.cooja` (or equivalent) builds without errors.

If build fails, check:
- `CONTIKI_NG` env var
- `variants/imacros-CLUSTERIDS.h` include path
- ARM GCC in PATH

---

## Step 6 — Generate Cooja Scenario

```bash
cd $CLUSTERIDS/simulations
python3 scripts/generate_campaign_csc.py --nodes 3 --out cooja/ids-smoke-3nodes.csc
```

---

## Step 7 — Smoke Simulation (Gate G2)

```bash
cd $CLUSTERIDS/simulations
NUM_SEEDS=1 SIM_TIMEOUT_MS=90000 ./scripts/run_ids_campaign.sh smoke
```

**Expected:**
- Cooja headless or GUI completes ~90 s
- Log file in `simulations/logs/ids_campaign/`
- Log contains `METRIC,...` lines per `metrics/LOG_FORMAT.md`

---

## Step 8 — Parse Logs (Gate G3)

```bash
python3 $CLUSTERIDS/simulations/scripts/parse_cooja_ids_metrics.py \
  --logs $CLUSTERIDS/simulations/logs/ids_campaign/ \
  --out $IDS_ROOT/data/real/parsed/
```

**Expected:** CSV files in `data/real/parsed/`

---

## Step 9 — Pilot Campaign (Gate G4)

From project root:
```bash
cd $IDS_ROOT/SIMULATION_CAMPAIGN_READY
export CONTIKI_NG=$CONTIKI_NG
./run_campaign.sh --dry-run     # validate matrix
./run_campaign.sh --pilot       # 50 nodes, 3 seeds, 30 min
```

Alternative (firmware-local script):
```bash
cd $CLUSTERIDS/simulations
NUM_SEEDS=3 SIM_TIMEOUT_MS=1800000 ./scripts/run_ids_campaign.sh pilot
```

**Validate:**
```bash
ls -la $IDS_ROOT/data/real/raw_logs/
python3 $IDS_ROOT/scripts/statistics/compute_statistics.py \
  --input $IDS_ROOT/data/real/aggregated --dry-run
```

---

## Step 10 — Implement Statistics (if not done)

Before full campaign, ensure `scripts/statistics/compute_statistics.py` computes:
- Mean, SD, 95% CI (bootstrap or t-distribution)
- `scipy.stats.ttest_ind` (two-sided)
- `scipy.stats.mannwhitneyu`

```bash
python3 $IDS_ROOT/scripts/statistics/compute_statistics.py \
  --input $IDS_ROOT/data/real/aggregated \
  --output $IDS_ROOT/data/real/statistics
```

Output: `data/real/statistics/pairwise_tests.csv` for Table IX.

---

## Step 11 — Full Campaign (Gate G5)

```bash
cd $IDS_ROOT/SIMULATION_CAMPAIGN_READY
nohup ./run_campaign.sh --full > campaign.log 2>&1 &
tail -f campaign.log
```

**Campaign scope** (`campaign_matrix.tsv`):
- 29 base configurations × 20 seeds
- Plus ablation variants (add to matrix first — see `TRACEABILITY_MATRIX.md` gap)

Monitor disk space:
```bash
du -sh $IDS_ROOT/data/real/
```

---

## Step 12 — Aggregate Metrics

```bash
# Post-process parsed CSVs into aggregated metric files
# (run_ids_campaign.sh or dedicated aggregator should produce:)
#   data/real/aggregated/detection_rate.csv
#   data/real/aggregated/detection_latency.csv
#   data/real/aggregated/fpr.csv
#   data/real/aggregated/energy_overhead.csv
#   data/real/aggregated/alert_overhead.csv
#   data/real/aggregated/cluster_stability.csv
#   data/real/aggregated/temporal_detection.csv
#   data/real/aggregated/operating_modes.csv
#   data/real/aggregated/summary_runs.csv
```

---

## Step 13 — Generate Figures

```bash
python3 $IDS_ROOT/scripts/python/generate_figures.py \
  --csv $IDS_ROOT/data/real/aggregated \
  --out $IDS_ROOT/Figures/

# Or legacy path:
python3 $IDS_ROOT/scripts/generate_ids_figures.py \
  --csv $IDS_ROOT/data/real/aggregated \
  --out $IDS_ROOT/Figures/
```

Update `figures_manifest.csv` status: `ESTIMATED` → `REAL_RESULT`

---

## Step 14 — Update LaTeX Tables

1. Replace `\EstimatedCell{—}` with measured values in:
   - `tables/table02_detection.tex`
   - `tables/table03_operating_modes.tex`
   - `tables/table06_dataset.tex` (sample count)
   - `tables/table08_ablation.tex`
   - `tables/table09_statistics.tex`

2. Remove `[ESTIMATED RESULT]` banners from Figs 4–11 for camera-ready.

3. Update `sections/limitations.tex` — remove « campaign pending » once complete.

---

## Step 15 — Compile Manuscript (Gate G6)

```bash
cd $IDS_ROOT
pdflatex main-ieee.tex
bibtex main-ieee
pdflatex main-ieee.tex
pdflatex main-ieee.tex
```

**Verify:**
- PDF is 11–13 pages
- No `EST.` markers in camera-ready build
- All figures render from real data
- All `\cite{}` resolve

---

## Step 16 — ML Training (Parallel Track)

After collecting benign + attack traces:

```bash
mkdir -p $IDS_ROOT/data/real/ml
# Export features per data/estimated/dataset_schema.md
# Train gradient-boosted model with Table VII hyperparameters
# Archive model + metrics to data/real/ml/
```

Update Table VI sample count and report test accuracy in §VII.

---

## Validation Gates Summary

| Gate | Criterion | Pass condition |
|------|-----------|----------------|
| G1 | Firmware build | `make TARGET=cooja` exit 0 |
| G2 | Smoke sim | Log with METRIC lines |
| G3 | Parse pipeline | CSV in `data/real/parsed/` |
| G4 | Pilot | 3 seeds aggregated; stats dry-run OK |
| G5 | Full campaign | All matrix rows × 20 seeds |
| G6 | Camera-ready PDF | 11–13 pp, REAL_RESULT only |

---

## Troubleshooting

| Problem | Likely cause | Fix |
|---------|--------------|-----|
| Cooja OOM at 500 nodes | Insufficient RAM | Reduce parallel jobs; run 500-node alone |
| Empty parse CSV | Log format mismatch | Compare log to `LOG_FORMAT.md` |
| All DR = 0 | Attack not triggered | Check `IDS_ATTACK_START_S=1800` |
| Build can't find Contiki | Env var | `export CONTIKI_NG=...` |
| Stats script exits 1 | Missing summary_runs.csv | Complete aggregation step |

---

## Environment Variables Reference

```bash
export CONTIKI_NG=/home/user/contiki-ng
export IDS_ROOT=/path/to/IDS_IOT
export CLUSTERIDS=$IDS_ROOT/code_source_RPL_ClusterIDS
export IDS_VARIANT=CLUSTERIDS   # or B1, B2, B3
export NUM_SEEDS=20
export SIM_TIMEOUT_MS=10800000  # 3 hours
export IDS_ATTACK_START_S=1800    # 30 min stabilization
```

---

## Post-Campaign Checklist

- [ ] `data/real/aggregated/*.csv` populated (8 files)
- [ ] `data/real/statistics/pairwise_tests.csv` populated
- [ ] Figs 4–11 status = REAL_RESULT
- [ ] Tables II, III, VIII, IX populated
- [ ] `MASTER_TRACKER.md` updated
- [ ] `checklist.md` Phase 2 items checked
- [ ] Public repo + DOI (optional pre-submission)
