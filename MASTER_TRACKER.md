# RPL-ClusterIDS — MASTER TRACKER

**Project root:** `IDS_IOT/`  
**Target journal:** Computer Networks (Elsevier)  
**Phase:** 2.0 (Phase 2 Campaign — real data, tables/figures updated)  
**Last updated:** 2026-06-22

---

## Global Progress

| Area | Status | Notes |
|------|--------|-------|
| Architecture | DONE | `code_source_RPL_ClusterIDS/` modular firmware |
| Article (11–13 pp.) | IN_PROGRESS | Real data in Tables II, III, VIII, IX; Figs 4–11 updated |
| Figures | IN_PROGRESS | Figs. 1–3 illustrative; Figs. 4–11 populated from pilot data only |
| Tables | IN_PROGRESS | Tables II, III, VIII, IX updated with pilot values; IV–V design |
| Dataset / ML | IN_PROGRESS | Pilot campaign collected (21 seeds CLUSTERIDS); full ML pending |
| Statistics | DONE (pilot) | `compute_statistics.py` run on pilot data (8 comparisons) |
| Reproducibility | IN_PROGRESS | Pipeline validated; full-scale campaign pending |
| References | IN_PROGRESS | Bib cleaned; recent references still need a final pass |
| Simulations | DONE (pilot) | 21 seeds CLUSTERIDS + 3 seeds ablation; full-scale validation pending |
| Windows tooling | DONE | `WINDOWS_SETUP_GUIDE.md`, Docker, PS scripts |
| Final Validation | IN_PROGRESS | Final submission-level validation remains pending |

**Legend:** `TODO` | `IN_PROGRESS` | `DONE` | `BLOCKED` | `READY_FOR_SIMULATION`

---

## Architecture

| Item | Status |
|------|--------|
| `clus_form`, `ch_elect`, `ids_member`, `ids_ch`, `ctx_policy` | DONE |
| Attack injector `ids_attack` | DONE |
| Campaign logger `ids_campaign_log` | DONE |
| Variants B1, B2, B3, CLUSTERIDS | DONE |
| Compile on Ubuntu (`TARGET=cooja`) | DONE |

---

## Article

| Item | Status |
|------|--------|
| `main-ieee.tex` — IEEE two-column build | DONE |
| §I Introduction | DONE |
| §II Related Work | DONE (hierarchical distributed wording) |
| §III Threat Model | DONE |
| §IV Architecture | DONE |
| §V Implementation + ML pipeline | IN_PROGRESS |
| §VI Experimental Setup | DONE |
| §VII Results + statistical validation | DONE (pilot campaign) |
| §VIII Discussion | DONE |
| §IX Limitations | DONE |
| §X Conclusion | IN_PROGRESS (no definitive metrics) |
| §XI Reproducibility | DONE |
| Abstract — no invented metrics | IN_PROGRESS |
| Forbidden placeholder phrases removed | DONE |

---

## Figures

| Fig | File | Status |
|-----|------|--------|
| 1 | `Fig_1_ClusterIDS_Architecture.tex` | DONE |
| 2 | `Fig_2_DODAG_Cluster_Overlay.tex` | DONE |
| 3 | `Fig_3_Context_Policy_Weights.tex` | DONE |
| 4 | `Fig_4_Detection_Rate_Comparison.tex` | REAL_RESULT |
| 5 | `Fig_5_Detection_Latency_Comparison.tex` | REAL_RESULT |
| 6 | `Fig_6_FPR_By_Scenario.tex` | REAL_RESULT |
| 7 | `Fig_7_Energy_Overhead_Comparison.tex` | REAL_RESULT |
| 8 | `Fig_8_Alert_Control_Overhead.tex` | REAL_RESULT |
| 9 | `Fig_9_Cluster_Stability.tex` | REAL_RESULT |
| 10 | `Fig_10_Temporal_Detection_Stratification.tex` | REAL_RESULT |
| 11 | `Fig_11_Operating_Mode_Sensitivity.tex` | REAL_RESULT |

---

## Tables

| Table | File | Status |
|-------|------|--------|
| I | Related work comparison (`sections/related_work.tex`) | DONE |
| II | Detection performance (`tables/table02_detection.tex`) | REAL_RESULT |
| III | Operating modes (`tables/table03_operating_modes.tex`) | REAL_RESULT |
| IV | Parameter configuration (`tables/table04_parameters.tex`) | DONE |
| V | Experimental setup (`tables/table05_experimental_setup.tex`) | READY_FOR_SIMULATION |
| VI | ML dataset (`tables/table06_dataset.tex`) | READY_FOR_SIMULATION |
| VII | ML hyperparameters (`tables/table07_ml_hyperparameters.tex`) | READY_FOR_SIMULATION |
| VIII | Ablation study (`tables/table08_ablation.tex`) | REAL_RESULT |
| IX | Statistical validation (`tables/table09_statistics.tex`) | REAL_RESULT |

---

## Dataset

| Item | Status |
|------|--------|
| Feature schema documented | DONE (`data/estimated/dataset_schema.md`) |
| Training/validation/test split defined | READY_FOR_SIMULATION |
| Raw Cooja traces collected | IN_PROGRESS (pilot campaign 21 seeds) |
| `data/real/` populated | IN_PROGRESS (pilot data present) |

---

## Machine Learning

| Item | Status |
|------|--------|
| Model type (gradient-boosted trees at CH) | DONE (design) |
| Hyperparameter table (Table VII) | READY_FOR_SIMULATION |
| Feature list documented | DONE |
| Trained model artifact | BLOCKED |

---

## Statistics

| Item | Status |
|------|--------|
| 3 seeds planned (pilot) | DONE |
| `scripts/statistics/compute_statistics.py` | DONE (scipy + bootstrap CI) |
| Unit tests + synthetic CSVs | DONE (`data/estimated/aggregated/`) |
| 95% CI, t-test, Mann-Whitney | DONE (on synthetic); real CSV pending |
| Boxplots / error bars generation | BLOCKED |

---

## Reproducibility

| Item | Status |
|------|--------|
| `SIMULATION_CAMPAIGN_READY/` | DONE |
| `sim/DATA_PROVENANCE.md` | DONE |
| `figures_manifest.csv` | IN_PROGRESS |
| `checklist.md` | DONE |
| Phase 1.5 audit docs (6 files) | DONE |
| Public repository release | TODO |

---

## References

| Item | Status |
|------|--------|
| Current count | DONE (~34 cited, cleaned) |
| Belacel 2025–2026 refs | DONE |
| DOI verification pass | IN_PROGRESS |
| Recent refs (2023–2025) | IN_PROGRESS |

---

## Simulations (Phase 2 — Ubuntu only)

| Node count | Attacks × metrics | Status |
|------------|-------------------|--------|
| 50 | 5 attacks, full metric set | PARTIAL (pilot: 21 seeds CLUSTERIDS, 3 seeds ablation) |
| 100 | 5 attacks, full metric set | BLOCKED |
| 200 | 5 attacks, full metric set | BLOCKED |
| 300 | 5 attacks, full metric set | BLOCKED |
| 500 | 5 attacks, full metric set | BLOCKED |

---

## Final Validation

| Check | Status |
|-------|--------|
| No `[ESTIMATED RESULT]` in camera-ready PDF | DONE |
| All tables populated from `data/real/` | PARTIAL (II, III, VIII, IX done; V, VI, VII pending) |
| 3 seeds + statistical tests reported | DONE (pilot, 8 comparisons) |
| Reviewer P0 anomalies (ChatGpt audit) closed | IN_PROGRESS |
| 11–13 pages compiled | DONE (11 pp, 2026-06-15) |

---

## Phase 2 Execution Checklist

Execute under Ubuntu with Contiki-NG + Cooja:

1. [x] Gate G1: Smoke build (`make TARGET=cooja`) — DONE
2. [x] Gate G2: Smoke sim (3 nodes, 1 seed → METRIC log lines) — DONE
3. [x] Gate G3: Parse pipeline (`parse_cooja_ids_metrics.py`) — DONE (1808K rows)
4. [x] Gate G4: Pilot campaign (50 nodes, 3 seeds) — DONE
5. [~] Gate G5: Full campaign — **PARTIAL** (21 seeds for CLUSTERIDS, 3 seeds for ablation; B1/B2/B3 have 0% DR issue)
6. [x] Aggregate metrics → `data/real/parsed/*.csv` (8 files) — DONE
7. [x] Run `scripts/statistics/compute_statistics.py` — DONE (8 comparisons)
8. [ ] Run `scripts/python/generate_figures.py` — validation script (figures use PGFPlots directly from agg CSVs)
9. [x] Replace all `\EstimatedCell{—}` in tables II, III, VI, VIII, IX — DONE
10. [x] Remove ESTIMATED banners from Figs 4–11 — DONE
11. [x] Update statuses to `REAL_RESULT` in this tracker — DONE
12. [ ] Gate G6: Camera-ready PDF — PENDING
