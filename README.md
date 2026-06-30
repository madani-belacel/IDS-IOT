# RPL-ClusterIDS — Reproducible Scientific Project (Computer Networks — Elsevier)

**Target journal:** Computer Networks (Elsevier)  
**Phase:** 2.1 (pilot campaign data available, full campaign pending, transparency fixes applied)  
**Tracker:** [`anomalies/opencode.md`](anomalies/opencode.md)

## Repository Structure

```
IDS_IOT/
├── main.tex                   # Manuscript (Elsevier elsarticle format)
├── main-ieee.tex              # IEEE variant (auxiliary)
├── sections/                  # 11 LaTeX sections
├── tables/                    # Tables II–IX
├── Figures/                   # 11 figures (TikZ/PGFPlots)
├── bib/references.bib         # References (~34 entries)
├── status-macros.tex          # Status macros
├── MASTER_TRACKER.md          # Project tracking
├── SIMULATION_CAMPAIGN_READY/ # Campaign scripts (Ubuntu)
├── data/
│   ├── estimated/             # Reference CSV schemas
│   ├── real/raw/              # Raw Cooja logs (pilot)
│   └── real/parsed/           # Parsed aggregated CSVs
├── scripts/
│   ├── python/generate_figures.py
│   └── statistics/compute_statistics.py
├── code_source_RPL_ClusterIDS/ # Contiki-NG firmware
└── anomalies/                 # AI audit reports (6 tools)
```

## Compilation (Elsevier — submission target)

```bash
pdflatex -interaction=nonstopmode main.tex
bibtex main
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex
```

## Full Campaign (Ubuntu with Contiki-NG + Cooja)

```bash
cd SIMULATION_CAMPAIGN_READY
./run_campaign.sh --full
python3 ../scripts/statistics/compute_statistics.py --input ../data/real/parsed
python3 ../scripts/python/generate_figures.py --csv ../data/real/parsed/agg --out ../Figures/
```

## Status Legend

| Mark | Meaning |
|------|---------|
| `REAL_RESULT` | Pilot campaign measurement (pipeline-generated; see `anomalies/opencode.md`) |
| `READY_FOR_SIMULATION` | Ready to run on Ubuntu |
| `ESTIMATED` | Placeholder (no Cooja data yet) |

## Note

This repository contains the IDS project only. The AER-MQoS routing project is maintained separately.
