# RPL-ClusterIDS — TABLE DEPENDENCIES

**Phase:** 1.5  
**Manuscript tables:** I–IX (+ traffic-class sub-table in Table IV block)

**Status legend:** `DONE` | `ESTIMATED` | `READY_FOR_SIMULATION` | `REAL_RESULT`

---

## Summary

| Table | Label | Content | Status |
|-------|-------|---------|--------|
| I | `tab:related` | Related work comparison | **DONE** |
| II | `tab:detection` | Detection performance DR/FPR | **ESTIMATED** |
| III | `tab:modes` | Operating modes Full/Balanced/Eco | **ESTIMATED** |
| IV | `tab:parameters` | Parameters, weights, thresholds | **DONE** (design values) |
| IVb | `tab:traffic-classes` | C0–C3 taxonomy | **DONE** (design values) |
| V | `tab:experimental-setup` | Experimental setup | **READY_FOR_SIMULATION** |
| VI | `tab:dataset` | ML dataset specification | **READY_FOR_SIMULATION** |
| VIb | `tab:features` | 12-dim feature vector | **DONE** (design) |
| VII | `tab:ml-hyperparams` | ML hyperparameters | **READY_FOR_SIMULATION** |
| VIII | `tab:ablation` | Ablation study (5 variants) | **ESTIMATED** |
| IX | `tab:statistics` | Statistical validation | **ESTIMATED** |

---

## Table I — Related Work Comparison

| Field | Value |
|-------|-------|
| **File** | `sections/related_work.tex` (inline) |
| **Required source data** | Bibliographic survey (no simulation) |
| **Required simulations** | None |
| **Required metrics** | Qualitative feature matrix |
| **Required validation** | Peer-review of feature assignments |
| **Status** | **DONE** |
| **Notes** | Compares RPL-ClusterIDS vs raza2017, hindy2020, garg2023, dib2024 |

---

## Table II — Detection Performance

| Field | Value |
|-------|-------|
| **File** | `tables/table02_detection.tex` |
| **Required source data** | `data/real/aggregated/detection_rate.csv`, `fpr.csv` |
| **Required simulations** | 50-node grid, 5 attacks, B1/B2/B3/CLUSTERIDS, balanced, 20 seeds |
| **Matrix rows** | `campaign_matrix.tsv` rows 1–20 |
| **Required metrics** | DR (%) per scenario; aggregate FPR (%) |
| **Required validation** | Mean ± SD; feeds Table IX comparisons |
| **Aggregation** | Group by `(attack, variant)` → mean over 20 seeds |
| **LaTeX update** | Replace `\EstimatedCell{—}` with `\RealCell{value}` |
| **Status** | **ESTIMATED** |
| **Linked figures** | Figs 4, 5, 6 |

---

## Table III — Operating Modes

| Field | Value |
|-------|-------|
| **File** | `tables/table03_operating_modes.tex` |
| **Required source data** | `data/real/aggregated/operating_modes.csv` |
| **Required simulations** | 50-node mixed, CLUSTERIDS: full / balanced / eco × 20 seeds |
| **Matrix rows** | Rows 21–23 |
| **Required metrics** | DR (%), FPR (%), CPU overhead (%) |
| **Required validation** | Full vs Eco: t-test + MWU (Table IX row 8) |
| **Status** | **ESTIMATED** |
| **Linked figures** | Fig 11 |

---

## Table IV — Parameter Configuration

| Field | Value |
|-------|-------|
| **File** | `tables/table04_parameters.tex` |
| **Required source data** | Design document / firmware `ids_conf.h` |
| **Required simulations** | None (design-time constants) |
| **Required metrics** | w_e–w_d, λ₁–λ₄, τ thresholds, Δ₀, T_max, α, β |
| **Required validation** | Sensitivity sweep (optional, §VII) — `[PENDING_VALIDATION]` for robustness |
| **Status** | **DONE** |
| **Cross-check** | Must match `code_source_RPL_ClusterIDS/ids_conf.h` |

---

## Table IVb — Traffic-Priority Classes (C0–C3)

| Field | Value |
|-------|-------|
| **File** | `tables/table04_parameters.tex` (second table) |
| **Required source data** | Application taxonomy (design) |
| **Required simulations** | None |
| **Required metrics** | Class → example → vigilance level |
| **Required validation** | Fig 6 FPR stratification by class |
| **Status** | **DONE** |

---

## Table V — Experimental Setup

| Field | Value |
|-------|-------|
| **File** | `tables/table05_experimental_setup.tex` |
| **Required source data** | `SIMULATION_CAMPAIGN_READY/`, `seeds.txt`, `campaign_matrix.tsv` |
| **Required simulations** | None (describes protocol) |
| **Required metrics** | N/A — configuration table |
| **Required validation** | Campaign execution must match stated parameters |
| **Status** | **READY_FOR_SIMULATION** |
| **Verify at Phase 2** | 20 seeds executed; 3 h duration; 5–10% malicious fraction |

---

## Table VI — ML Dataset Specification

| Field | Value |
|-------|-------|
| **File** | `tables/table06_dataset.tex` |
| **Required source data** | `data/real/ml/dataset_summary.json` |
| **Required simulations** | Cooja traces (benign + all attack classes) |
| **Required metrics** | Total samples, split counts, label distribution |
| **Required validation** | Stratified 70/15/15; class balance report |
| **Status** | **READY_FOR_SIMULATION** (sample count cell **ESTIMATED**) |
| **Linked** | Table VII, feature table `tab:features` |

---

## Table VII — ML Hyperparameters

| Field | Value |
|-------|-------|
| **File** | `tables/table07_ml_hyperparameters.tex` |
| **Required source data** | Training script config / `ml/training_config.yaml` |
| **Required simulations** | Offline training on collected traces |
| **Required metrics** | trees ≤8, max_depth=3, lr=0.1, RAM ≤3 KB |
| **Required validation** | Test-set accuracy/F1 in `ml/model_metrics.json` |
| **Status** | **READY_FOR_SIMULATION** (hyperparams **DONE**; metrics pending) |

---

## Table VIII — Ablation Study

| Field | Value |
|-------|-------|
| **File** | `tables/table08_ablation.tex` |
| **Required source data** | `data/real/aggregated/ablation_mixed.csv` |
| **Required simulations** | 50-node mixed, 5 firmware variants × 20 seeds |
| **Variants** | Full; −clustering; −ML; −context; −energy |
| **Build flags** | `IDS_VARIANT=CLUSTERIDS` + ablation macros in `variants/` |
| **Required metrics** | DR (%), FPR (%), ΔE (%) |
| **Required validation** | Optional pairwise vs Full |
| **Status** | **ESTIMATED** |
| **GAP** | Ablation rows missing from `campaign_matrix.tsv` — add before Phase 2 |
| **Linked figures** | Fig 7, Fig 9 (indirect) |

---

## Table IX — Statistical Validation

| Field | Value |
|-------|-------|
| **File** | `tables/table09_statistics.tex` |
| **Required source data** | `data/real/statistics/pairwise_tests.csv` |
| **Produced by** | `scripts/statistics/compute_statistics.py` |
| **Required simulations** | 50-node mixed balanced: Ours + B1/B2/B3; Full + Eco modes |
| **Required metrics** | Mean, SD, 95% CI, t-test p, Mann-Whitney p |
| **Comparisons (8 rows)** | Ours vs B1/B2/B3 on DR; same on FPR; Ours vs B2 on O_alert; Full vs Eco on DR |
| **Required validation** | scipy `ttest_ind`, `mannwhitneyu`; α=0.05 |
| **Status** | **ESTIMATED** |
| **Linked figures** | Error bars on Figs 4–11 |

---

## Table → CSV → Script Mapping

| Table | Primary CSV | Statistics output | Update method |
|-------|-------------|-------------------|---------------|
| II | `detection_rate.csv`, `fpr.csv` | `statistics/summary_detection.json` | Manual or `update_tables.py` |
| III | `operating_modes.csv` | `statistics/modes.json` | Manual or script |
| VI | `ml/dataset_summary.json` | — | Manual |
| VIII | `ablation_mixed.csv` | `statistics/ablation.json` | Manual or script |
| IX | `statistics/pairwise_tests.csv` | (self) | Auto from `compute_statistics.py` |

---

## Phase 2 Replacement Checklist

- [ ] All `\EstimatedCell` → `\RealCell` in tables II, III, VI (sample count), VIII, IX
- [ ] Remove `\TableStatusNote` ESTIMATED banners for camera-ready
- [ ] Verify Table IV values match compiled firmware
- [ ] Table V unchanged (protocol table)
- [ ] Table IX p-values < 0.05 only where claim uses « significantly »
