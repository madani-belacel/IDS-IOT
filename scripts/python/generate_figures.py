#!/usr/bin/env python3
"""
Validate CSV → Figure mapping for Figs. 4-11 (stub: no figure generation).

This script validates that aggregated CSV files exist for all 8 figures.
Actual figures are hand-written PGFPlods code in Figures/Fig_*.tex,
which read directly from data/real/parsed/agg/ CSVs.

Usage:
  python generate_figures.py --csv data/real/parsed/agg --out Figures/
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

FIG_MAP = {
    4: ("detection_rate.csv", "Fig_4_Detection_Rate_Comparison.tex"),
    5: ("detection_latency.csv", "Fig_5_Detection_Latency_Comparison.tex"),
    6: ("fpr.csv", "Fig_6_FPR_By_Scenario.tex"),
    7: ("energy_overhead.csv", "Fig_7_Energy_Overhead_Comparison.tex"),
    8: ("alert_overhead.csv", "Fig_8_Alert_Control_Overhead.tex"),
    9: ("cluster_stability.csv", "Fig_9_Cluster_Stability.tex"),
    10: ("temporal_detection.csv", "Fig_10_Temporal_Detection_Stratification.tex"),
    11: ("operating_modes.csv", "Fig_11_Operating_Mode_Sensitivity.tex"),
}


def load_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    missing = []
    ready = []
    for fig_num, (csv_name, tex_name) in FIG_MAP.items():
        csv_path = args.csv / csv_name
        rows = load_csv(csv_path)
        if not rows:
            missing.append(csv_name)
        else:
            ready.append((fig_num, csv_name, tex_name, len(rows)))

    if ready:
        print("[REAL_RESULT] Ready to generate:")
        for item in ready:
            print(f"  Fig {item[0]}: {item[2]} ({item[3]} rows from {item[1]})")

    if missing:
        print("\n[ESTIMATED] Missing CSV (Phase 1 expected):", ", ".join(missing))
        if not args.dry_run:
            sys.exit(1)

    if not missing:
        print("\n[TO_BE_REPLACED] Implement pgfplots/matplotlib export per figure.")


if __name__ == "__main__":
    main()
