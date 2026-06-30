# Computer Networks (Elsevier) — Submission Checklist

**Project:** RPL-ClusterIDS  
**Target journal:** Computer Networks (Elsevier)  
**Last updated:** 2026-06-30  
**Phase:** 2.0 — pilot campaign data collected; full campaign pending

---

## Pre-Submission Requirements

### Results Data (Phase 2 — CRITICAL PATH)

- [ ] `data/real/aggregated/*.csv` populated (8 metric files)
- [ ] `data/real/statistics/pairwise_tests.csv` computed
- [ ] All `\EstimatedCell{—}` replaced with `\RealCell{value}` in:
  - `tables/table02_detection.tex` (Table II)
  - `tables/table03_operating_modes.tex` (Table III)
  - `tables/table06_dataset.tex` (Table VI — sample count)
  - `tables/table08_ablation.tex` (Table VIII)
  - `tables/table09_statistics.tex` (Table IX)
- [ ] Figs 4–11 generated from real data, `[ESTIMATED RESULT]` banners removed
- [ ] `figures_manifest.csv` status: `ESTIMATED` → `REAL_RESULT`
- [ ] Abstract updated with real DR/FPR values
- [ ] Conclusion updated with validated metrics

### PDF Quality

- [ ] PDF compiles cleanly (`pdflatex` × 4: no errors, no undefined refs)
- [ ] 11–13 pages (11 pp verified on 2026-06-17)
- [ ] All `\cite{}` resolve (no `?` in PDF)
- [ ] No `[ESTIMATED RESULT]` visible in camera-ready PDF
- [ ] Figures render correctly from real data
- [ ] Tables fit within column/page width
- [ ] No overfull/underfull hbox warnings (minor acceptable)

### Manuscript Content

- [ ] Section ordering: Intro → Related Work → Threat → Architecture → Implementation → Experimental Setup → Results → Discussion → Limitations → Conclusion → Reproducibility
- [ ] Abstract contains no invented metrics
- [ ] Conclusion contains no invented metrics
- [ ] "fully distributed" → "hierarchical distributed" (checked)
- [ ] No forbidden placeholder phrases
- [ ] `sections/limitations.tex` updated (remove "campaign pending" after Phase 2)
- [ ] `sections/reproducibility.tex` — update `data/real/` status

### References

- [ ] All DOIs verified and resolvable
- [ ] `belacel2025rplaer` DOI no longer "pending" (update if available)
- [ ] `belacel2026thesis` — verify institutional deposit URL
- [ ] No orphan BibTeX entries in `bib/references.bib`
- [ ] No `@article` entries that are actually RFCs
- [ ] Maximum ~45 references (currently ~34)
- [ ] At least 8 references from 2023–2025

### Reproducibility

- [ ] `SIMULATION_CAMPAIGN_READY/` complete with matrix + seeds + attack specs
- [ ] `code_source_RPL_ClusterIDS/` firmware compiles on Ubuntu
- [ ] `scripts/parse_cooja_ids_metrics.py` tested with real logs
- [ ] `scripts/statistics/compute_statistics.py` produces pairwise_tests.csv
- [ ] `scripts/python/generate_figures.py` generates Figs 4–11
- [ ] `MASTER_TRACKER.md` updated to Phase 2 statuses
- [ ] `checklist.md` Phase 2 items all checked
- [ ] Public repository + DOI ready (or planned for acceptance)

### Elsevier Formatting (elsarticle)

- [ ] `elsarticle.cls` — preprint 12pt numbered format
- [ ] Research Highlights (3–5 bullets, ~85 chars each)
- [ ] Graphical Abstract (optional but recommended)
- [ ] Author name(s) + affiliation(s) + ORCID
- [ ] Abstract: 150–250 words
- [ ] Keywords: 5–8 terms
- [ ] All figures in vector format (TikZ/PGFPlots)
- [ ] All tables use booktabs (`\toprule`/`\midrule`/`\bottomrule`)
- [ ] Bibliography in elsarticle-num style

---

## Submission Process

### Before Upload

- [ ] Final PDF: `main.pdf` (Elsevier format)
- [ ] Source files: `.tex`, `.bib`, `.sty`, `.cls`, figures
- [ ] Readme with build instructions
- [ ] ORCID iD linked to Editorial Manager account

### On Editorial Manager

- [ ] Manuscript type: "Research Paper"
- [ ] Cover letter (optional but recommended)
- [ ] Suggested reviewers (optional)
- [ ] All authors with correct affiliations
- [ ] Funding information (if applicable)

### Post-Submission

- [ ] Await desk decision (~1–2 weeks)
- [ ] If desk rejected: address issues and resubmit or transfer
- [ ] If sent to review: respond to reviewer comments within revision deadline

---

## Status Summary (Pre-Phase 2)

| Area | Status | Blocker |
|------|--------|---------|
| Manuscript structure | ✅ DONE | — |
| PDF compilation | ✅ DONE (11 pp) | — |
| Tables I–IX structure | ✅ DONE | Real data (Phase 2) |
| Figures 1–3 | ✅ DONE (illustrative) | — |
| Figures 4–11 | ❌ ESTIMATED | Campaign execution |
| References | ✅ ~34 entries | 2 entries need DOI update |
| Ablation variants | ✅ FIXED (rows 30–33) | — |
| Anomalies P0–P1 | ✅ CLOSED | — |
| Campaign matrix | ✅ 33 rows × 20 seeds | — |
| Parse pipeline | ✅ Ready | Campaign logs needed |
| Statistics | ✅ Structure ready | Real CSV needed |
| ML model | ❌ Not trained | Campaign traces needed |

**Estimated acceptance probability:**
- Current (pre-full-campaign): **~30%** (pilot data present but B1/B2/B3 0% DR issue unresolved)
- Target (post-full-campaign, real data): **~85%**
