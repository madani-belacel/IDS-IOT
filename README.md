# RPL-ClusterIDS — Projet scientifique reproductible (IEEE IoT Journal)

**Phase actuelle :** 1 (Windows — squelette 95%, résultats `ESTIMATED`)  
**Tracker central :** [`MASTER_TRACKER.md`](MASTER_TRACKER.md)  
**Checklist soumission :** [`checklist.md`](checklist.md)

## Structure du projet

```
IDS_IOT/
├── main-ieee.tex              # Manuscrit IEEE (soumission)
├── sections/                  # 11 sections LaTeX
├── tables/                    # Tables II–IX
├── Figures/                   # 11 figures (4–11 = ESTIMATED)
├── bib/references.bib         # ~45 références
├── status-macros.tex          # ESTIMATED / REAL_RESULT
├── MASTER_TRACKER.md          # Centre de pilotage
├── SIMULATION_CAMPAIGN_READY/ # Campagne Ubuntu (Phase 2)
├── data/
│   ├── estimated/             # Schémas, templates CSV
│   └── real/                  # Résultats Cooja (Phase 2)
├── scripts/
│   ├── python/generate_figures.py
│   └── statistics/compute_statistics.py
├── code_source_RPL_ClusterIDS/ # Firmware Contiki-NG
└── article/README.md          # Carte du manuscrit
```

## Compilation IEEE

```bash
pdflatex -interaction=nonstopmode main-ieee.tex
bibtex main-ieee
pdflatex -interaction=nonstopmode main-ieee.tex
pdflatex -interaction=nonstopmode main-ieee.tex
```

Soumettre **`main-ieee.pdf`** (11 pages, Phase 1).

## Phase 2 (Ubuntu — NE PAS exécuter sous Windows)

```bash
cd SIMULATION_CAMPAIGN_READY
./run_campaign.sh --full
python3 ../scripts/statistics/compute_statistics.py --input ../data/real/aggregated
python3 ../scripts/python/generate_figures.py --csv ../data/real/aggregated --out ../Figures/
```

## Règles de statut

| Statut | Signification |
|--------|---------------|
| `ESTIMATED` | Placeholder Phase 1 — pas de donnée Cooja |
| `READY_FOR_SIMULATION` | Spécification prête, exécution Ubuntu requise |
| `TO_BE_REPLACED` | Template en attente de CSV réel |
| `REAL_RESULT` | Mesure Cooja validée (Phase 2) |

## Séparation AER-MQoS

Projet IDS indépendant — pas de métriques routage AER-MQoS.
