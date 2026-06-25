# WINDOWS_SETUP_GUIDE.md

**Complement to:** `UBUNTU_EXECUTION_PLAN.md`  
**Purpose:** Maximize progress on Windows before WSL2 / Ubuntu / Docker campaign execution.

---

## Prerequisites (Windows)

| Tool | Purpose | Install |
|------|---------|---------|
| Python 3.10+ | Stats, synthetic CSVs, tests | python.org or `winget install Python.Python.3.12` |
| MiKTeX or TeX Live | PDF compile check | miktex.org |
| Git | Version control | git-scm.com |
| WSL2 + Ubuntu 22.04 | Cooja campaigns (recommended) | `wsl --install -d Ubuntu-22.04` |
| Docker Desktop | Optional isolated Ubuntu toolchain | docker.com |

---

## Quick Start (Windows — no Cooja)

```powershell
cd C:\Users\madan\Desktop\projet_madani_v2_ubuntu\IDS_IOT

# Python environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Generate synthetic data + test full post-processing pipeline
.\scripts\windows\run_pipeline_test.ps1

# Compile PDF and check page count (11–13 target)
.\scripts\windows\compile_check.ps1
# or: scripts\windows\compile_check.bat
```

---

## What Works on Windows Native

| Task | Script | Status |
|------|--------|--------|
| Bibliography cleanup | Manual / done | DONE |
| Synthetic CSV generation | `scripts/python/generate_synthetic_csv.py` | DONE |
| Statistics (t-test, MWU, bootstrap CI) | `scripts/statistics/compute_statistics.py` | DONE |
| Unit tests | `scripts/statistics/test_compute_statistics.py` | DONE |
| Figure CSV validation | `scripts/python/generate_figures.py --dry-run` | DONE |
| LaTeX PDF compile | `scripts/windows/compile_check.ps1` | Requires TeX |
| Manuscript editing | `sections/`, `tables/` | DONE |

---

## What Requires WSL2 / Ubuntu / Docker

| Task | Why |
|------|-----|
| `make TARGET=cooja` | Contiki-NG + ARM toolchain + Linux paths |
| Cooja simulations | Java + Contiki-NG native on Linux |
| Full 20-seed campaign | CPU/RAM + Cooja |
| Real `data/real/` population | Cooja log export |

---

## Option A — WSL2 (Recommended)

1. Install WSL2 Ubuntu 22.04.
2. Mount project: `/mnt/c/Users/madan/Desktop/projet_madani_v2_ubuntu/IDS_IOT`
3. Follow `UBUNTU_EXECUTION_PLAN.md` inside WSL.

Dry-run from Windows PowerShell:
```powershell
.\scripts\windows\wsl_run.ps1 -Command "cd /mnt/c/Users/madan/Desktop/projet_madani_v2_ubuntu/IDS_IOT && bash SIMULATION_CAMPAIGN_READY/run_campaign.sh --dry-run"
```

---

## Option B — Docker

From project root (Docker Desktop running):

```powershell
# Interactive dev shell with Contiki-NG 4.8
docker compose run --rm clusterids

# Inside container:
export CONTIKI_NG=/opt/contiki-ng
cd code_source_RPL_ClusterIDS && make TARGET=cooja IDS_VARIANT=CLUSTERIDS

# Pipeline test (synthetic data, no Cooja)
docker compose run --rm pipeline-test
```

Files:
- `docker/Dockerfile`
- `docker-compose.yml`

---

## Synthetic vs Real Data

| Path | Purpose | Use in manuscript? |
|------|---------|-------------------|
| `data/estimated/aggregated/` | Pipeline testing | **NO** — marked SYNTHETIC |
| `data/real/aggregated/` | Cooja campaign output | **YES** — after Phase 2 |

---

## Author References (Belacel)

Added to `bib/references.bib` and cited in `sections/related_work.tex`:

- `belacel2025rplaer` — RPL-AER (AEEE 2025, early access)
- `belacel2025rplmqos` — RPLMQoS (Microwave Review 2025, DOI verified)
- `belacel2026thesis` — Ph.D. thesis (2026)

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `ModuleNotFoundError: scipy` | `pip install -r requirements.txt` |
| pdflatex not found | Install MiKTeX; restart terminal |
| WSL path not found | Use `/mnt/c/...` not `C:\...` |
| Docker build slow | First build clones Contiki-NG (~5 min) |
| Page count out of range | Normal in ESTIMATED phase; grows after real results |

---

## Next Step After Windows Setup

1. WSL2 smoke build (Gate G1 in `UBUNTU_EXECUTION_PLAN.md`)
2. Pilot campaign 50 nodes × 3 seeds
3. Replace `data/estimated/` workflow with `data/real/`
