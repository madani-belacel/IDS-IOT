#!/usr/bin/env python3
"""
Validate aggregated CSV files for Figs. 4-11 and report data provenance.

Figures are maintained as hand-written PGFPlots TikZ code in Figures/Fig_*.tex,
which read directly from data/real/parsed/agg/ CSVs via \\addplot table.
This script validates all CSV files exist and have expected content.

Usage:
  python generate_figures.py --csv data/real/parsed/agg --out Figures/
  python generate_figures.py --csv data/real/parsed/agg --dry-run
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path


def load_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", type=Path, required=True, help="CSV data directory (data/real/parsed/agg/)")
    ap.add_argument("--out", type=Path, required=True, help="Output directory (Figures/)")
    ap.add_argument("--dry-run", action="store_true", help="Validate only, do not write")
    args = ap.parse_args()

    # Expected CSV files per figure (matched to existing files in data/real/parsed/agg/)
    csv_checks = {
        4: {"fig4_detection_rate.csv", "fig4_detection_rate_B1.csv", "fig4_detection_rate_CLUSTERIDS.csv"},
        5: {"fig5_latency.csv", "fig5_latency_B1.csv", "fig5_latency_CLUSTERIDS.csv"},
        6: {"fig6_fpr.csv", "fig6_B1.csv", "fig6_CLUSTERIDS.csv"},
        7: {"fig7_energy.csv", "fig7_ch.csv", "fig7_member.csv"},
        8: {"fig8_alerts.csv", "fig8_alerts_B1.csv", "fig8_alerts_CLUSTERIDS.csv"},
        9: {"fig9_stability.csv"},
        10: {"fig10_temporal.csv"},
        11: {"fig11_modes.csv"},
    }

    all_ok = True
    for fig_num, expected_files in sorted(csv_checks.items()):
        present = []
        missing = []
        for fname in expected_files:
            csv_path = args.csv / fname
            rows = load_csv(csv_path)
            if rows:
                present.append((fname, len(rows)))
            else:
                missing.append(fname)

        if missing:
            all_ok = False
            print(f"[WARNING] Fig {fig_num}: missing {', '.join(missing)}")
        if present:
            for fname, nrows in present:
                print(f"[OK] Fig {fig_num}: {fname} ({nrows} rows)")

    if all_ok:
        print("\n[OK] All CSV files present for all 8 figures (Figs. 4-11).")
        print("[NOTE] Figures are hand-written PGFPlots TikZ in Figures/Fig_*.tex.")
        print("       Run pdflatex on main.tex to render them into the manuscript PDF.")
    else:
        print("\n[WARNING] Some CSV files are missing. Run the Cooja campaign + parse pipeline first.",
              file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()