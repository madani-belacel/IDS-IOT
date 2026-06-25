# RPL-ClusterIDS — FIGURE DEPENDENCIES

**Phase:** 1.5  
**Source of truth:** `figures_manifest.csv` + this matrix.

**Status legend:** `ILLUSTRATIVE` | `ESTIMATED` | `READY_FOR_SIMULATION` | `REAL_RESULT`

---

## Summary

| Fig | Title (short) | Status | Blocker |
|-----|---------------|--------|---------|
| 1 | Architecture | ILLUSTRATIVE | None |
| 2 | DODAG cluster overlay | ILLUSTRATIVE | None |
| 3 | Context policy weights | ILLUSTRATIVE | None |
| 4 | Detection rate comparison | ESTIMATED | Ubuntu campaign |
| 5 | Detection latency | ESTIMATED | Ubuntu campaign |
| 6 | FPR by scenario/class | ESTIMATED | Ubuntu campaign |
| 7 | Energy overhead | ESTIMATED | Ubuntu campaign |
| 8 | Alert/control overhead | ESTIMATED | Ubuntu campaign |
| 9 | Cluster stability | ESTIMATED | Ubuntu campaign |
| 10 | Temporal detection | ESTIMATED | Ubuntu campaign |
| 11 | Operating mode sensitivity | ESTIMATED | Ubuntu campaign |

---

## Figure 1 — ClusterIDS Architecture

| Field | Value |
|-------|-------|
| **File** | `Figures/Fig_1_ClusterIDS_Architecture.tex` |
| **Type** | Manual TikZ diagram |
| **Input CSV** | None |
| **Simulation** | None |
| **Seeds** | N/A |
| **Statistics** | N/A |
| **Status** | **ILLUSTRATIVE** |
| **Phase 2 action** | None |

---

## Figure 2 — DODAG Cluster Overlay

| Field | Value |
|-------|-------|
| **File** | `Figures/Fig_2_DODAG_Cluster_Overlay.tex` |
| **Type** | Manual TikZ diagram |
| **Input CSV** | None |
| **Simulation** | None |
| **Seeds** | N/A |
| **Statistics** | N/A |
| **Status** | **ILLUSTRATIVE** |
| **Phase 2 action** | None |

---

## Figure 3 — Context Policy Weights

| Field | Value |
|-------|-------|
| **File** | `Figures/Fig_3_Context_Policy_Weights.tex` |
| **Type** | Manual TikZ (design values from Table IV) |
| **Input CSV** | None (values: w_e=0.35, w_s=0.25, w_t=0.25, w_d=0.15) |
| **Simulation** | None |
| **Seeds** | N/A |
| **Statistics** | N/A |
| **Status** | **ILLUSTRATIVE** |
| **Phase 2 action** | None |

---

## Figure 4 — Detection Rate Comparison

| Field | Value |
|-------|-------|
| **File** | `Figures/Fig_4_Detection_Rate_Comparison.tex` |
| **Metric** | Detection rate (DR, %) |
| **Protocols / variants** | B1, B2, B3, CLUSTERIDS |
| **Input CSV** | `data/real/aggregated/detection_rate.csv` |
| **CSV schema** | `nodes, topology, attack, variant, mode, seed, detection_rate` |
| **Simulation** | 50-node grid, 5 attacks, 4 variants, balanced mode, 20 seeds |
| **Matrix rows** | `campaign_matrix.tsv` rows 1–20 |
| **Seeds** | 20 (`seeds.txt` s001–s020) |
| **Statistics** | Mean ± SD, 95% CI error bars per bar group |
| **Generator** | `scripts/python/generate_figures.py --figure 4` |
| **Status** | **READY_FOR_SIMULATION** |
| **Phase 2 action** | Replace ESTIMATED banner → REAL_RESULT |

---

## Figure 5 — Detection Latency Comparison

| Field | Value |
|-------|-------|
| **File** | `Figures/Fig_5_Detection_Latency_Comparison.tex` |
| **Metric** | Mean detection latency L_det (seconds) |
| **Protocols / variants** | B1, B2, B3, CLUSTERIDS |
| **Input CSV** | `data/real/aggregated/detection_latency.csv` |
| **CSV schema** | `nodes, attack, variant, seed, detection_latency_s` |
| **Simulation** | 50-node grid, 5 attacks, 4 variants, 20 seeds |
| **Matrix rows** | Rows 1–20 |
| **Seeds** | 20 |
| **Statistics** | 95% CI |
| **Generator** | `scripts/python/generate_figures.py --figure 5` |
| **Status** | **READY_FOR_SIMULATION** |

---

## Figure 6 — FPR by Scenario and Traffic Class

| Field | Value |
|-------|-------|
| **File** | `Figures/Fig_6_FPR_By_Scenario.tex` |
| **Metric** | False-positive rate (%) |
| **Stratification** | Attack scenario × traffic class C0–C3 |
| **Input CSV** | `data/real/aggregated/fpr.csv` |
| **CSV schema** | `attack, traffic_class, variant, seed, fpr` |
| **Simulation** | 50-node grid, CLUSTERIDS balanced (+ baselines for comparison) |
| **Matrix rows** | Rows 1–20 |
| **Seeds** | 20 |
| **Statistics** | 95% CI per group |
| **Generator** | `scripts/python/generate_figures.py --figure 6` |
| **Status** | **READY_FOR_SIMULATION** |

---

## Figure 7 — Energy Overhead Comparison

| Field | Value |
|-------|-------|
| **File** | `Figures/Fig_7_Energy_Overhead_Comparison.tex` |
| **Metric** | Energest ΔE (%) — member vs cluster-head |
| **Input CSV** | `data/real/aggregated/energy_overhead.csv` |
| **CSV schema** | `nodes, variant, role, seed, energy_overhead_pct` |
| **Simulation** | 50-node mixed, CLUSTERIDS (+ baselines) |
| **Matrix rows** | Row 20 (mixed balanced) + ablation variants |
| **Seeds** | 20 |
| **Statistics** | Mean ± SD |
| **Generator** | `scripts/python/generate_figures.py --figure 7` |
| **Status** | **READY_FOR_SIMULATION** |

---

## Figure 8 — Alert and Control Overhead

| Field | Value |
|-------|-------|
| **File** | `Figures/Fig_8_Alert_Control_Overhead.tex` |
| **Metric** | O_alert, O_ctrl (packets/hour) |
| **Input CSV** | `data/real/aggregated/alert_overhead.csv` |
| **CSV schema** | `nodes, topology, variant, seed, alert_overhead_pkt_h, control_overhead_pkt_h` |
| **Simulation** | 50, 100, 200, 300, 500 nodes — mixed campaign, balanced |
| **Matrix rows** | Rows 20, 24–29 (CLUSTERIDS); B2 rows for comparison at 50-node minimum |
| **Seeds** | 20 |
| **Statistics** | 95% CI; regression slope (scalability claim) |
| **Generator** | `scripts/python/generate_figures.py --figure 8` |
| **Status** | **READY_FOR_SIMULATION** |
| **Critical for** | `[PENDING_VALIDATION]` sublinear vs near-linear claim |

---

## Figure 9 — Cluster Stability

| Field | Value |
|-------|-------|
| **File** | `Figures/Fig_9_Cluster_Stability.tex` |
| **Metric** | S_clust (CH tenure, recluster rate, mean NRE) |
| **Input CSV** | `data/real/aggregated/cluster_stability.csv` |
| **CSV schema** | `nodes, seed, ch_tenure_s, recluster_rate, mean_nre, cluster_stability` |
| **Simulation** | CLUSTERIDS, 50–500 nodes, mixed balanced |
| **Matrix rows** | Rows 20, 24–29 |
| **Seeds** | 20 |
| **Statistics** | Mean ± SD |
| **Generator** | `scripts/python/generate_figures.py --figure 9` |
| **Status** | **READY_FOR_SIMULATION** |

---

## Figure 10 — Temporal Detection Stratification

| Field | Value |
|-------|-------|
| **File** | `Figures/Fig_10_Temporal_Detection_Stratification.tex` |
| **Metric** | DR (%) in phases: stabilization / attack / recovery |
| **Input CSV** | `data/real/aggregated/temporal_detection.csv` |
| **CSV schema** | `seed, phase, detection_rate` |
| **Simulation** | 50-node mixed, CLUSTERIDS balanced, 3 h run |
| **Matrix rows** | Row 20 |
| **Seeds** | 20 |
| **Statistics** | Phase-wise mean ± SD |
| **Generator** | `scripts/python/generate_figures.py --figure 10` |
| **Status** | **READY_FOR_SIMULATION** |

---

## Figure 11 — Operating Mode Sensitivity

| Field | Value |
|-------|-------|
| **File** | `Figures/Fig_11_Operating_Mode_Sensitivity.tex` |
| **Metric** | DR, FPR, CPU overhead by mode |
| **Input CSV** | `data/real/aggregated/operating_modes.csv` |
| **CSV schema** | `mode, seed, detection_rate, fpr, cpu_overhead_pct` |
| **Simulation** | 50-node mixed, CLUSTERIDS: full / balanced / eco |
| **Matrix rows** | Rows 21–23 |
| **Seeds** | 20 |
| **Statistics** | 95% CI; Full vs Eco t-test (Table IX) |
| **Generator** | `scripts/python/generate_figures.py --figure 11` |
| **Status** | **READY_FOR_SIMULATION** |

---

## Pipeline (All Figures 4–11)

```
Cooja logs (raw_logs/)
    ↓ parse_cooja_ids_metrics.py
data/real/parsed/*.csv
    ↓ aggregation script (campaign post-process)
data/real/aggregated/*.csv
    ↓ compute_statistics.py (CI, tests)
data/real/statistics/*.json
    ↓ generate_figures.py
Figures/Fig_4..11_*.tex  (REAL_RESULT)
    ↓ pdflatex
main-ieee.pdf
```

**Pre-flight check:**
```bash
python3 scripts/statistics/compute_statistics.py --input data/real/aggregated --dry-run
python3 scripts/python/generate_figures.py --csv data/real/aggregated --dry-run
```
