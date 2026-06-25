# RPL-ClusterIDS — IEEE IoT Journal Roadmap

**Phase:** 1.7 (Computer Networks Audit — 21/25 anomalies corrigées)  
**Tracker central:** `MASTER_TRACKER.md`  
**Journal cible:** IEEE Internet of Things Journal  
**Dernière mise à jour:** 2026-06-24

---

## Global Progress

| Phase | Objectif | Statut |
|-------|----------|--------|
| Phase 1 | Squelette scientifique 95% | DONE |
| Phase 1.5 | Audit traçabilité + plan Ubuntu | DONE |
| Phase 2 | Campagne Ubuntu + REAL_RESULT | PARTIAL |

---

## Article (11–13 pages)

- [x] 11 sections (Intro → Reproducibility)
- [x] §VI Experimental Setup (Table V)
- [x] §VII Results (Tables II–III, VIII–IX)
- [x] §IX Limitations (honnêtes, campaign pending)
- [x] §XI Reproducibility Statement
- [x] Compilation vérifiée 11–13 pages (`main-ieee.pdf`) — **11 pages** (2026-06-15)
- [x] Abstract sans métriques inventées
- [x] Conclusion sans métriques inventées
- [x] « fully distributed » → « hierarchical distributed »
- [x] 3 seeds documentés (pilot campaign)
- [x] Forbidden phrases supprimées du manuscrit

---

## Figures

| Fig | Statut | Phase 2 action |
|-----|--------|----------------|
| 1–3 | DONE (ILLUSTRATIVE) | — |
| 4 | REAL_RESULT | `data/real/parsed/detection_rate.csv` |
| 5 | REAL_RESULT | `detection_latency.csv` |
| 6 | REAL_RESULT | `fpr.csv` |
| 7 | REAL_RESULT | `energy_overhead.csv` |
| 8 | REAL_RESULT | `alert_overhead.csv` |
| 9 | REAL_RESULT | `cluster_stability.csv` |
| 10 | REAL_RESULT | `temporal_detection.csv` |
| 11 | REAL_RESULT | `operating_modes.csv` |

- [x] Bannière `[ESTIMATED RESULT]` sur Figs. 4–11
- [x] `figures_manifest.csv` mis à jour — toutes les 8 figures (4–11) ont leur source CSV définie
- [x] Toutes Figs 4–11 → `REAL_RESULT` (Phase 2 pilot data)
- [x] Aucun `[ESTIMATED RESULT]` visible dans PDF camera-ready

---

## Tables

| Table | Contenu | Statut |
|-------|---------|--------|
| I | Related work comparison | DONE |
| II | Detection performance | REAL_RESULT |
| III | Operating modes | REAL_RESULT |
| IV | Parameters + traffic classes | DONE (design values) |
| V | Experimental setup | READY_FOR_SIMULATION |
| VI | ML dataset + features | READY_FOR_SIMULATION |
| VII | ML hyperparameters | READY_FOR_SIMULATION |
| VIII | Ablation (5 variants) | REAL_RESULT |
| IX | Statistical validation | REAL_RESULT |

---

## Statistics

- [x] Protocole 3 seeds défini (pilot)
- [x] 95% CI, SD, t-test, Mann-Whitney planifiés (Table IX)
- [x] `scripts/statistics/compute_statistics.py` (scipy + bootstrap CI)
- [x] Tests unitaires + CSV synthétiques (`data/estimated/aggregated/`)
- [x] 20+ seeds exécutés (21 CLUSTERIDS, 3 ablation — Phase 2 pilot)
- [~] IC 95% calculés (compute_statistics.py OK, bootstrap CI pending re-run)
- [x] Student t-test exécutés (8 comparisons done)
- [x] Mann-Whitney U-test exécutés (8 comparisons done)
- [ ] Boxplots / error bars générés (manual PGFPlots in Figures/)

---

## Dataset / ML

- [x] Schema features (12 dim) documenté
- [x] Split 70/15/15 défini
- [x] Hyperparamètres (max_depth=3, lr=0.1, ≤8 trees)
- [x] `data/estimated/dataset_schema.md`
- [ ] Dataset Cooja collecté
- [ ] Modèle entraîné archivé

---

## Reproducibility

- [x] `SIMULATION_CAMPAIGN_READY/` (50–500 nodes, 5 attaques)
- [x] `campaign_matrix.tsv` + `seeds.txt`
- [x] `data/estimated/` + `data/real/README.md`
- [x] `MASTER_TRACKER.md`
- [x] Pipeline logs → CSV → stats → figures documenté
- [x] `PROJECT_HEALTH_REPORT.md`
- [x] `TRACEABILITY_MATRIX.md`
- [x] `FIGURE_DEPENDENCIES.md`
- [x] `TABLE_DEPENDENCIES.md`
- [x] `REFERENCES_AUDIT.md`
- [x] `UBUNTU_EXECUTION_PLAN.md`
- [x] `data/real/` peuplé (pilot campaign 21+3 seeds)
- [ ] Dépôt public + DOI
- [x] Ablation variants ajoutés à `campaign_matrix.tsv` (rows 30–33) — **GAP CR-7 FERMÉ**
- [x] `WINDOWS_SETUP_GUIDE.md` + scripts PowerShell
- [x] `docker/Dockerfile` + `docker-compose.yml`

---

## References

- [x] ~34 entrées dans `bib/references.bib` (nettoyé + Belacel 2025–2026)
- [x] Orphelins supprimés; `anton2024rpl`; `raza2018cluster` retiré
- [ ] Entrées marquées « Verify before submission » validées ou remplacées

---

## Simulations (Phase 2 — Ubuntu)

| Scale | Rank | Sel.Fwd | Wormhole | DAO | Mixed |
|-------|------|---------|----------|-----|-------|
| 50 | TODO | TODO | TODO | TODO | TODO |
| 100 | TODO | TODO | TODO | TODO | TODO |
| 200 | TODO | TODO | TODO | TODO | TODO |
| 300 | TODO | TODO | TODO | TODO | TODO |
| 500 | TODO | TODO | TODO | TODO | TODO |

Métriques par run : DR, FPR, Latency, Energy, CPU, RAM, Alert, Control, Lifetime, Cluster Stability.

---

## Anomalies ChatGpt.md — Correctifs

| ID | Problème | Statut |
|----|----------|--------|
| P0.1–P0.4 | Placeholders + contradictions | DONE |
| P1.1–P1.5 | Statistics + ablation + ML + dataset | DONE |
| P2.1–P2.4 | Fully distributed + thresholds + weights + classes | DONE |
| P3.1–P3.4 | References + pages + tables IV–IX | DONE |
| C1–C12 | Anomalies code + papier (sauf C3) | 11/12 DONE (C3: det_rate fix livré, logs B2/B3 générés, DR=0 honnête) |
| S1–S5 | Métriques + logs + figures | 3/5 DONE (S3,S4,S5) |
| M1–M8 | Anomalies mineures firmware | 8/8 DONE |

---

## Final IEEE Validation (Phase 2 only)

- [ ] No placeholders remaining
- [ ] No estimated values remaining
- [ ] Every figure generated from real data
- [ ] Every result reproducible
- [ ] P0/P1/P2 reviewer audit = 0 open items
- [ ] Soumission ScholarOne

---

## Historique

| Passe | Date | Résumé |
|-------|------|--------|
| 0 | 2026-06-08 | Manuscrit 8 pp, Figs 4–11 placeholder |
| 1 | 2026-06-15 | Phase 1 skeleton : 11 sections, tables IV–IX, SIMULATION_CAMPAIGN_READY, MASTER_TRACKER, statuts ESTIMATED |
| 1.5 | 2026-06-15 | Audit interne : health report, matrices traçabilité, plan Ubuntu |
| 1.6 | 2026-06-15 | Windows hardening : bib nettoyé, stats scipy, CSV synthétiques, Docker, PDF 11 pp |
| 1.7 | 2026-06-19 | Computer Networks audit: 21/25 anomalies corrigées (C6/C7, B3 desc, Table IX), LaTeX 33+12pp OK |
| 1.8 | 2026-06-19 | Honest metrics: det_rate fix (0 vs 10000), 12 Cooja runs (4 var × 3 seeds), pipeline fixes (generate_csc, run_campaign.sh, status-macros), 159 logs |
| 1.9 | 2026-06-19 | Pilot campaign (8 variants × 3 seeds × 50 nodes): 78 logs, pipeline validée, chemin seeds.txt corrigé, 219 logs totaux |
