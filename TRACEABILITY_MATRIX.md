# RPL-ClusterIDS — TRACEABILITY MATRIX

**Phase:** 1.5  
**Rule:** No new scientific claims. Every comparative or quantitative assertion must link to simulation, CSV, figure, and statistical test.

**Status legend:** `VALIDATED` | `ESTIMATED` | `READY_FOR_SIMULATION` | `PENDING_VALIDATION` | `DESIGN_ONLY` | `ILLUSTRATIVE`

---

## Core Performance Claims

| Scientific Claim | Article Section | Required Simulation | Required CSV | Required Figure | Required Statistical Test | Current Status |
|------------------|-----------------|---------------------|--------------|-----------------|---------------------------|----------------|
| Detection rate across 5 attack scenarios (B1/B2/B3/Ours) | §VII, Table II | 50-node grid, balanced, 5 attacks × 4 variants × 20 seeds | `summary_runs.csv`, `detection_rate.csv` | Fig 4 | Mean ± SD, 95% CI; Ours vs B1/B2/B3 t-test + MWU | **ESTIMATED** |
| Mean detection latency by scenario and variant | §VII | Same as above | `detection_latency.csv` | Fig 5 | 95% CI per variant | **ESTIMATED** |
| False-positive rate by scenario and traffic class C0–C3 | §VII, Table II | 50-node, benign + attack phases, class-tagged traffic | `fpr.csv` | Fig 6 | CI; stratified by class | **ESTIMATED** |
| Energest energy overhead (member vs CH) | §VII | 50-node mixed, CLUSTERIDS, Energest enabled | `energy_overhead.csv` | Fig 7 | Mean ΔE%, SD | **ESTIMATED** |
| Alert and control packet overhead vs network size | §VII, §VII scalability | 50–500 nodes, mixed, balanced | `alert_overhead.csv` | Fig 8 | Regression slope; Ours vs B2 alert t-test | **PENDING_VALIDATION** |
| Cluster stability (CH tenure, recluster rate, NRE) | §VII ablation | 50–500 nodes, CLUSTERIDS | `cluster_stability.csv` | Fig 9 | Mean S_clust, SD | **ESTIMATED** |
| Temporal DR stratification (stabilize / attack / recovery) | §VII | Mixed campaign, time-windowed metrics | `temporal_detection.csv` | Fig 10 | Phase-wise mean DR | **ESTIMATED** |
| Operating mode sensitivity (Full / Balanced / Eco) | §VII, Table III | 50-node mixed, 3 modes × 20 seeds | `operating_modes.csv` | Fig 11 | Full vs Eco DR t-test + MWU | **ESTIMATED** |

---

## Ablation Claims

| Scientific Claim | Article Section | Required Simulation | Required CSV | Required Figure | Required Statistical Test | Current Status |
|------------------|-----------------|---------------------|--------------|-----------------|---------------------------|----------------|
| Full system DR/FPR/ΔE on mixed campaign | §VII, Table VIII | 50-node, 5 ablation variants | `ablation_mixed.csv` | — (Table VIII) | Pairwise vs Full (optional) | **ESTIMATED** |
| Without clustering — degraded DR, higher alert load | §VIII discussion | Variant: disable clustering | `ablation_mixed.csv` | Fig 8 (indirect) | Compare alert overhead | **PENDING_VALIDATION** |
| Without ML — higher FPR on ambiguous cases | §VIII | Variant: rules-only at CH | `ablation_mixed.csv` | Fig 6 | FPR comparison | **PENDING_VALIDATION** |
| Without context adaptation — uniform vigilance penalty | §VIII | Variant: fixed policy | `ablation_mixed.csv` | Fig 11 | Mode-equivalent DR | **PENDING_VALIDATION** |
| Without energy awareness — reduced lifetime | §VIII | Variant: no NRE weighting | `ablation_mixed.csv` | Fig 7, Fig 9 | ΔE, T_life | **PENDING_VALIDATION** |

---

## Scalability & Hypothesis Claims

| Scientific Claim | Article Section | Required Simulation | Required CSV | Required Figure | Required Statistical Test | Current Status |
|------------------|-----------------|---------------------|--------------|-----------------|---------------------------|----------------|
| B2 alert traffic grows faster than RPL-ClusterIDS with node count | §VIII L10 | 50–500 nodes, B2 + CLUSTERIDS mixed | `alert_overhead.csv` | Fig 8 | Slope comparison; Ours vs B2 t-test | **PENDING_VALIDATION** |
| Sublinear alert growth (Ours) vs near-linear (B2) | §VII L104 | 50–500 nodes | `alert_overhead.csv` | Fig 8 | Log-linear fit R² | **PENDING_VALIDATION** |
| Centralized B1/B3 higher latency for spatially local attacks | §VIII L13 | 50-node, rank + sel.fwd | `detection_latency.csv` | Fig 5 | Ours vs B1/B3 latency t-test | **PENDING_VALIDATION** |
| Network lifetime T_life scales with energy-aware policy | §VII | 50–500 nodes, Eco vs Full | `summary_runs.csv` | — | Full vs Eco t-test (Table IX) | **PENDING_VALIDATION** |

---

## ML & Dataset Claims

| Scientific Claim | Article Section | Required Simulation | Required CSV | Required Figure | Required Statistical Test | Current Status |
|------------------|-----------------|---------------------|--------------|-----------------|---------------------------|----------------|
| 12-dim feature vector at cluster head | §VI, Table VI | Cooja traces with METRIC lines | `ml/features.csv`, `ml/labels.csv` | — | — | **READY_FOR_SIMULATION** |
| 70/15/15 train/val/test split | §VI, Table VI | Labeled trace export | `ml/split_manifest.json` | — | — | **READY_FOR_SIMULATION** |
| ≤8 trees, max_depth=3, lr=0.1 | §VI, Table VII | Offline training run | `ml/model_metrics.json` | — | Test accuracy, F1 | **DESIGN_ONLY** |
| Model fits in ≤3 KB RAM at CH | §V, architecture | Profiling during inference | `summary_runs.csv` (ram_overhead_kb) | — | — | **PENDING_VALIDATION** |

---

## Design & Architecture Claims (No Campaign Required)

| Scientific Claim | Article Section | Required Simulation | Required CSV | Required Figure | Required Statistical Test | Current Status |
|------------------|-----------------|---------------------|--------------|-----------------|---------------------------|----------------|
| Hierarchical distributed IDS with optional border corroboration | §I, §VIII | — | — | Fig 1 | — | **ILLUSTRATIVE** |
| DODAG + cluster overlay topology | §IV | — | — | Fig 2 | — | **ILLUSTRATIVE** |
| Context policy weights w_e–w_d, λ₁–λ₄ | §IV, Table IV | — | — | Fig 3 | — | **DESIGN_ONLY** |
| Thresholds τ_low=0.25, τ_CH=0.40, τ_las=0.70, τ_inter=0.80 | Table IV | Sensitivity sweep (optional) | `statistics/sensitivity/` | — | DR/FPR heatmaps | **DESIGN_ONLY** (values set; sensitivity **PENDING_VALIDATION**) |
| Traffic classes C0–C3 taxonomy | Table IV (classes) | — | — | — | — | **DESIGN_ONLY** |
| 20 seeds per configuration | §VI, Table V | Campaign execution | `seeds.txt` | — | All result CIs | **READY_FOR_SIMULATION** |
| Five attack families as defined | §VI | Per attack scenario runs | `summary_runs.csv` | — | — | **READY_FOR_SIMULATION** |

---

## Statistical Validation (Table IX)

| Comparison | Metric | Required Runs | CSV Field | Test | Current Status |
|------------|--------|---------------|-----------|------|----------------|
| Ours vs B1 | DR | Mixed, 50-node, 20 seeds each | `detection_rate` | t-test, MWU, 95% CI | **ESTIMATED** |
| Ours vs B2 | DR | Mixed, 50-node | `detection_rate` | t-test, MWU, 95% CI | **ESTIMATED** |
| Ours vs B3 | DR | Mixed, 50-node | `detection_rate` | t-test, MWU, 95% CI | **ESTIMATED** |
| Ours vs B1 | FPR | Mixed, 50-node | `fpr` | t-test, MWU, 95% CI | **ESTIMATED** |
| Ours vs B2 | FPR | Mixed, 50-node | `fpr` | t-test, MWU, 95% CI | **ESTIMATED** |
| Ours vs B3 | FPR | Mixed, 50-node | `fpr` | t-test, MWU, 95% CI | **ESTIMATED** |
| Ours vs B2 | O_alert | Mixed, 50-node | `alert_overhead_pkt_h` | t-test, MWU, 95% CI | **ESTIMATED** |
| Full vs Eco | DR | Mixed, 50-node, CLUSTERIDS | `detection_rate` | t-test, MWU, 95% CI | **ESTIMATED** |

---

## Forbidden-Phrase Audit

Phrases requiring experimental proof per Phase 1.5 rule (`above`, `lower`, `better`, `outperform`, `significantly`):

| Phrase context | File | Marked | Action |
|----------------|------|--------|--------|
| « grows much faster » (B2 alerts) | `discussion.tex` | **PENDING_VALIDATION** | Prove via Fig 8 + Table IX |
| « sublinear » vs « near-linear » | `results.tex` | **PENDING_VALIDATION** | Prove via Fig 8 regression |
| « above hysteresis threshold » | `architecture.tex` | N/A (design param) | No action |
| « suspicion above τ_ml » | `architecture.tex` | N/A (design param) | No action |
| « faster out-of-band path » | `threat_model.tex` | N/A (attack description) | No action |

**No forbidden unmarked comparative metrics found in Abstract or Conclusion.**

---

## Campaign Row Mapping (Quick Reference)

| Claim cluster | `campaign_matrix.tsv` rows | Seeds |
|---------------|---------------------------|-------|
| Table II / Figs 4–6 | Rows 1–20 (50-node, all attacks, all variants) | 20 |
| Table III / Fig 11 | Rows 21–23 (mixed, CLUSTERIDS modes) | 20 |
| Table VIII ablation | Rows 30–33 (CLUSTERIDS\_NOCLUS, \_NOML, \_NOCTX, \_NOENR) | 20 |
| Fig 8 scalability | Rows 24–29 (100–500 nodes, mixed) | 20 |
| Table IX statistics | Subset: row 20 (mixed balanced, all variants) | 20 |

**Gap CR-7 (FIXED):** Ablation variants are now rows 30–33 in `campaign_matrix.tsv`. Build flags documented in `ABLATION_VARIANTS.md`.
