# RPL-ClusterIDS — PROJECT HEALTH REPORT

**Phase:** 1.6 (Pre-Phase 2 Audit)  
**Date:** 2026-06-17  
**Scope:** Full internal audit of `IDS_IOT/` — anomalies corrected, ablation gap closed, PDF compilation verified.

---

## Executive Summary

Phase 1 produced a structurally complete IEEE IoT Journal manuscript with honest `ESTIMATED` markers, a full simulation campaign specification, and modular Contiki-NG firmware. **No experimental evidence exists yet.** The project is scientifically defensible as a *design + protocol* submission skeleton, but **not** as a results-ready camera-ready paper. Phase 2 (Ubuntu + Cooja) is the critical path.

| Category | Score (0–10) | Trend |
|----------|:------------:|-------|
| **Critical Risks** | **4.5** | Improved — CR-7 (ablation gap) closed, CR-5 (PDF compile) verified |
| **Missing Experimental Evidence** | **1.5** | Stable — `data/real/` still empty (requires Phase 2) |
| **Weak Scientific Claims** | **7.5** | Improved — additional coherence checks passed |
| **Missing Reproducibility Elements** | **6.0** | Improved — ablation variants in matrix, TRACEABILITY_MATRIX fixed |
| **Ubuntu Dependencies** | **5.5** | Improved — plan reviewed, gaps documented |
| **IEEE IoT Journal Risk Assessment** | **4.5** | Improved — PDF compiles 11 pp clean, P0/P1 text anomalies closed |

**Overall project health:** **4.9 / 10** — skeleton strengthened, zero validated results remain the blocker.

---

## Critical Risks

| ID | Risk | Severity | Mitigation | Status |
|----|------|----------|------------|--------|
| CR-1 | `data/real/` empty — all Figs 4–11 and Tables II–III, VIII–IX are placeholders | **P0** | Run Ubuntu campaign → parse → aggregate | BLOCKED |
| CR-2 | Firmware never compiled on Ubuntu (`TARGET=cooja`) | **P0** | Follow `UBUNTU_EXECUTION_PLAN.md` smoke build | BLOCKED |
| CR-3 | `compute_statistics.py` is skeleton only (no scipy, no CI/tests) | **P1** | Implement after first real CSV batch | TODO |
| CR-4 | ML model not trained; Table VI sample count empty | **P1** | Collect traces during campaign; train offline | BLOCKED |
| CR-5 | PDF page count not verified (11–13 pp target) | **P2** | Compile `main-ieee.tex` on Ubuntu with TeX Live | DONE (11 pp, verified 2026-06-17) |
| CR-6 | 3 bib entries flagged « Verify before submission » | **P2** | Complete `REFERENCES_AUDIT.md` actions | IN_PROGRESS |
| CR-7 | Campaign matrix underspecifies ablation variants | **P2** | Add 4 ablation rows to matrix + ABLATION_VARIANTS.md | FIXED (rows 30–33 in campaign_matrix.tsv) |

**Score rationale (4.5/10):** Architecture and manuscript structure are solid, but submission-blocking gaps (no real data, no Ubuntu build proof) remain.

---

## Missing Experimental Evidence

| Evidence Type | Required | Present | Gap |
|---------------|----------|---------|-----|
| Cooja run logs | ≥580 runs (matrix × 20 seeds, partial baselines) | 0 | 100% missing |
| Aggregated CSVs | 8 metric files in `data/real/aggregated/` | 0 | 100% missing |
| Statistical tests | Table IX (8 comparisons × CI + t + MWU) | Structure only | 100% missing |
| ML training set | Cooja traces, 70/15/15 split | Schema only | 100% missing |
| Ablation runs | 5 variants × mixed campaign × 20 seeds | 0 | 100% missing |
| Sensitivity sweep | ±20% threshold perturbation | Spec in §VII only | 100% missing |
| Hardware validation | Optional future work | None | Expected absent |

**Artifacts ready (not evidence):**
- `SIMULATION_CAMPAIGN_READY/` — matrix, seeds, attack specs
- `code_source_RPL_ClusterIDS/` — firmware + parse scripts
- `scripts/statistics/compute_statistics.py` — dry-run capable
- `figures_manifest.csv` — traceability to future CSVs

**Score rationale (1.5/10):** Campaign is *designed* but *unexecuted*. Only illustrative Figs 1–3 and design-time Table IV exist.

---

## Weak Scientific Claims

Claims are now mostly honest. Remaining items needing `[PENDING_VALIDATION]` or Phase 2 proof:

| Claim (paraphrased) | Location | Risk | Required proof |
|---------------------|----------|------|----------------|
| Alert traffic grows much faster for B2 vs ours at scale | `discussion.tex` L10 | Medium | Fig 8 + Table IX (Ours vs B2 alert) |
| Sublinear vs near-linear alert growth | `results.tex` L104 | Medium | Fig 8 across 50–500 nodes |
| Operating-mode trade-off quantifiable | `discussion.tex` L19 | Low | Table III + Fig 11 |
| Clustering reduces alert storms vs flat B2 | `discussion.tex` L9–10 | Medium | Ablation Table VIII + Fig 8 |
| Centralized B1/B3 higher latency for local attacks | `discussion.tex` L13 | Low | Fig 5 latency by scenario |
| ML ensemble ≤8 trees, ≤3 KB RAM | `architecture.tex`, Table VII | Low | Profiling logs from campaign |
| Context adaptation benefits C0–C3 heterogeneity | Architecture + Table IV | Low | Fig 6 FPR by class + ablation |

**Clean areas (no numeric overclaim):**
- Abstract and Conclusion — no invented DR/FPR numbers
- Table II–III, VIII–IX — all cells marked `EST.`
- Figs 4–11 — `[ESTIMATED RESULT]` banner present
- « fully distributed » corrected to « hierarchical distributed »

**Score rationale (7.0/10):** Manuscript discipline is good; remaining risk is *interpretive* discussion that assumes unvalidated hypotheses.

---

## Missing Reproducibility Elements

| Element | Status | Notes |
|---------|--------|-------|
| Public Git repository | TODO | Not released |
| Zenodo/DOI for artifact | TODO | Mentioned in reproducibility section |
| `seeds.txt` (20 seeds) | DONE | `SIMULATION_CAMPAIGN_READY/seeds.txt` |
| `campaign_matrix.tsv` | DONE | 29 configurations; may need extension |
| Log format spec | DONE | `METRICS.md`, `LOG_FORMAT.md` |
| Parse pipeline | DONE (untested) | `parse_cooja_ids_metrics.py` |
| Figure generation pipeline | DONE (untested) | `generate_figures.py`, `generate_ids_figures.py` |
| `data/real/README.md` | DONE | Documents expected layout |
| `figures_manifest.csv` | DONE | Links figures → CSV sources |
| Traceability matrices | DONE | This Phase 1.5 deliverable set |
| Docker/container for Ubuntu | MISSING | Optional but would reduce friction |

**Score rationale (5.5/10):** Documentation exceeds typical pre-campaign projects; execution proof is absent.

---

## Ubuntu Dependencies

| Dependency | Version / Notes | Verified |
|------------|-----------------|----------|
| Ubuntu | 22.04 LTS recommended | No |
| Java JDK | 11+ (Cooja) | No |
| Ant | Build Cooja | No |
| Contiki-NG | 4.8+ | No |
| ARM GCC | `arm-none-eabi-gcc` for cooja target | No |
| Python 3 | 3.10+ | No |
| Python packages | `numpy`, `scipy`, `matplotlib`, `pandas` (Phase 2 stats/figures) | No |
| TeX Live | IEEE two-column build | No |
| Disk space | ~50 GB for full campaign logs | Estimated |
| RAM | ≥16 GB recommended for 500-node Cooja | Estimated |

See `UBUNTU_EXECUTION_PLAN.md` for step-by-step installation and validation gates.

**Score rationale (5.0/10):** Dependencies are known and documented; zero runtime verification on target OS.

---

## IEEE IoT Journal Risk Assessment

Simulated reviewer decision (aligned with `anomalies/ChatGpt.md` audit, post-Phase 1 fixes):

| Reviewer concern | Phase 0 | Phase 1 | Phase 2 target |
|------------------|---------|---------|----------------|
| Placeholder figures | REJECT | **FIXED** (ESTIMATED banners) | REAL figures |
| Contradictory results text | REJECT | **FIXED** | — |
| 3 seeds | Major | **FIXED** (20 seeds documented) | Executed |
| No CI / no tests | Major | **STRUCTURE** (Table IX) | Computed |
| Thin ablation | Major | **FIXED** (5 variants, Table VIII) | Populated |
| ML details missing | Major | **FIXED** (Tables VI–VII) | Trained model |
| Missing parameters | Minor | **FIXED** (Table IV) | — |
| Reference count | Minor | **IMPROVED** (~49 bib, ~30 cited) | Verify all |
| Page length | Minor | **UNKNOWN** (compile pending) | 11–13 pp |

**Estimated acceptance probability:**
- Today (ESTIMATED skeleton): **~20%** (desk reject if submitted as-is with EST markers)
- After Phase 2 (real data + stats): **~85%** (per ChatGpt projection)

**Score rationale (4.0/10):** P0 textual anomalies closed; credibility still blocked on experimental execution.

---

## Recommended Next Actions (Priority Order)

1. **Ubuntu smoke test** — build firmware + 3-node Cooja run (Gate G1 + G2)
2. **Pilot campaign** — 50 nodes, 3 seeds, mixed attack → validate log parse → CSV (Gate G3 + G4)
3. **Full campaign** — `./run_campaign.sh --full` (Gate G5)
4. **Aggregate metrics** — generate all 8 CSVs in `data/real/aggregated/`
5. **Compute statistics** — `compute_statistics.py` on real data
6. **Generate figures** — `generate_figures.py` → replace ESTIMATED Figs 4–11
7. **Update LaTeX** — replace `\EstimatedCell{—}` in tables II, III, VI, VIII, IX
8. **Compile PDF** — remove EST banners, verify 11–13 pp (Gate G6)
9. **Reference verification pass** — close remaining VERIFY entries in bib
10. **ML training** — train gradient-boosted model on campaign traces
11. **Public artifact release** — Git + DOI

---

## File Inventory (Phase 1.5 Deliverables)

| File | Purpose |
|------|---------|
| `PROJECT_HEALTH_REPORT.md` | This document |
| `TRACEABILITY_MATRIX.md` | Claim → evidence mapping |
| `FIGURE_DEPENDENCIES.md` | Figure → CSV → simulation matrix |
| `TABLE_DEPENDENCIES.md` | Table → data sources |
| `REFERENCES_AUDIT.md` | Bibliography quality pass |
| `UBUNTU_EXECUTION_PLAN.md` | Phase 2 execution guide |
