#!/usr/bin/env python3
"""Print summary stats for LaTeX tables from parsed campaign CSVs."""
from __future__ import annotations

import csv
import statistics
from collections import defaultdict

CSV = "data/real/parsed"


def seed_drs(det: list[dict], var: str, scen: str) -> dict[str, float]:
    rows = [r for r in det if r["variant"] == var and r["scenario"] == scen]
    by_seed: dict[str, dict[str, int]] = defaultdict(lambda: {"tp": 0, "fn": 0})
    for r in rows:
        s = r["seed"]
        by_seed[s]["tp"] += int(r["tp"])
        by_seed[s]["fn"] += int(r["fn"])
    return {
        s: v["tp"] / (v["tp"] + v["fn"]) if (v["tp"] + v["fn"]) else 0.0
        for s, v in by_seed.items()
    }


def main() -> None:
    det = list(csv.DictReader(open(f"{CSV}/detection_rate.csv")))
    fpr_data = list(csv.DictReader(open(f"{CSV}/fpr.csv")))
    modes = list(csv.DictReader(open(f"{CSV}/modes.csv")))

    variants = ["B1", "B2", "B3", "MAIN"]
    scenarios = ["rank", "sel_fwd", "wormhole", "dao_flood", "mixed"]

    print("% === TABLE II: Detection Rate ===")
    for scen in scenarios:
        cells = [scen]
        for var in variants:
            drs = seed_drs(det, var, scen)
            if not drs or all(v == 0.0 for v in drs.values()):
                cells.append("0.0\\%")
            else:
                vals = list(drs.values())
                m = statistics.mean(vals) * 100
                cells.append(f"{m:.1f}\\%")
        print("  &  ".join(cells) + r"  \\")

    print()
    print("% === TABLE II: FPR ===")
    for scen in scenarios:
        cells = [scen]
        for var in variants:
            vals = [
                float(r["fpr"])
                for r in fpr_data
                if r["variant"] == var and r["scenario"] == scen
            ]
            if not vals:
                cells.append("---")
            else:
                m = statistics.mean(vals) * 100
                cells.append(f"{m:.4f}\\%")
        print("  &  ".join(cells) + r"  \\")

    print()
    print("% === TABLE III: Operating Modes ===")
    for mode_name in ["Full", "Balanced", "Eco"]:
        rows = [r for r in modes if r["mode"] == mode_name]
        dr = statistics.mean(float(r["det_rate"]) for r in rows) * 100
        fpr = statistics.mean(float(r["fpr"]) for r in rows) * 100
        cpu = statistics.mean(float(r["cpu_overhead_pct"]) for r in rows)
        print(
            f"  \\textsc{{{mode_name}}}  &  {dr:.1f}\\%  &  {fpr:.4f}\\%  &  {cpu:.0f}\\%  \\\\"
        )

    print()
    print("% === TABLE IX: DR per-seed stats for mixed scenario ===")
    for baseline in ["B1", "B2", "B3"]:
        ours = seed_drs(det, "MAIN", "mixed")
        base = seed_drs(det, baseline, "mixed")
        our_vals = list(ours.values())
        base_vals = list(base.values())
        print(f"% Ours vs {baseline} (DR, mixed):")
        sd_ours = statistics.stdev(our_vals) if len(our_vals) > 1 else 0.0
        sd_base = statistics.stdev(base_vals) if len(base_vals) > 1 else 0.0
        print(
            f"%   MAIN: n={len(our_vals)} mean={statistics.mean(our_vals)*100:.2f}%"
            f" sd={sd_ours*100:.2f}%"
        )
        print(
            f"%   {baseline}: n={len(base_vals)} mean={statistics.mean(base_vals)*100:.2f}%"
            f" sd={sd_base*100:.2f}%"
        )


if __name__ == "__main__":
    main()
