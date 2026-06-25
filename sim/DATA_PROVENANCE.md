# Data Provenance — RPL-ClusterIDS

## Pipeline

```
Cooja serial logs
  → parse_cooja_ids_metrics.py (parses METRIC lines from .log files)
  → data/real/parsed/ (*.csv per metric: detection_rate, latency, fpr, energy, alerts, stability, temporal, modes)
  → aggregate_figures.sh (awk-based per-figure aggregation)
  → data/real/parsed/agg/ (fig4_*.csv … fig11_*.csv)
  → compute_statistics.py (statistical tests, confidence intervals)
```

## Phase 2 Campaign Data

| Scale | Nodes | Seeds | Scenarios | Variants | Total runs |
|-------|-------|-------|-----------|----------|------------|
| Pilot | 50    | 3     | 5+none    | 8        | 144        |

## CSV Schema

Each CSV under `data/real/parsed/` follows a strict schema documented in `scripts/statistics/test_compute_statistics.py`.

## Status

- `data/real/parsed/` — parsed output from Phase 2 pilot campaign (real Cooja logs)
- `data/estimated/` — synthetic data for pipeline testing only (not for publication)
