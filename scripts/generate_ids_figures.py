#!/usr/bin/env python3
"""
Generate measured figures 4-11 from sim/ids_campaign/*.csv.
Updates TikZ/pgfplots snippets or PDF exports under Figures/.
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path


FIG_MAP = {
    4: ("detection_rate.csv", "Fig_4_Detection_Rate_Comparison.tex"),
    5: ("latency.csv", "Fig_5_Detection_Latency_Comparison.tex"),
    6: ("fpr.csv", "Fig_6_FPR_By_Scenario.tex"),
    7: ("energy.csv", "Fig_7_Energy_Overhead_Comparison.tex"),
    8: ("alerts.csv", "Fig_8_Alert_Control_Overhead.tex"),
    9: ("stability.csv", "Fig_9_Cluster_Stability.tex"),
    10: ("temporal.csv", "Fig_10_Temporal_Detection_Stratification.tex"),
    11: ("modes.csv", "Fig_11_Operating_Mode_Sensitivity.tex"),
}


def load_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", type=Path, required=True, help="sim/ids_campaign/ directory")
    ap.add_argument("--out", type=Path, required=True, help="Figures/ output directory")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    missing = []
    for fig_num, (csv_name, tex_name) in FIG_MAP.items():
        csv_path = args.csv / csv_name
        rows = load_csv(csv_path)
        if not rows:
            missing.append(csv_name)
            continue
        out_path = args.out / tex_name
        if args.dry_run:
            print(f"Fig {fig_num}: {len(rows)} rows from {csv_name} -> {tex_name}")
        else:
            print(f"Fig {fig_num}: {len(rows)} rows — TODO regenerate {out_path}")

    if missing:
        print("\nMissing or empty CSV:", ", ".join(missing), file=sys.stderr)
        print("Run Cooja campaign + parse_cooja_ids_metrics.py first.", file=sys.stderr)
        sys.exit(1)

    print("\nNext: implement pgfplots/matplotlib export per figure (Pass 4).")


if __name__ == "__main__":
    main()
