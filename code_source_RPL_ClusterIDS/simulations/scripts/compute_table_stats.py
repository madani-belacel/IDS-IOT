#!/usr/bin/env python3
"""Compute statistics from parsed campaign CSVs for LaTeX tables."""
from __future__ import annotations

import csv
import math
import statistics
import sys
from collections import defaultdict

CSV_DIR = "data/real/parsed"


def load_csv(name: str) -> list[dict]:
    with open(f"{CSV_DIR}/{name}") as f:
        return list(csv.DictReader(f))


def stats_str(vals: list[float]) -> str:
    if not vals:
        return "—"
    m = statistics.mean(vals)
    if len(vals) > 1:
        s = statistics.stdev(vals)
        return f"${m*100:.1f}\\pm{s*100:.1f}$"
    return f"${m*100:.1f}$"


def main() -> None:
    det = load_csv("detection_rate.csv")
    lat = load_csv("latency.csv")
    fpr_csv = load_csv("fpr.csv")
    eng = load_csv("energy.csv")
    modes_csv = load_csv("modes.csv")

    variants = ["B1", "B2", "B3", "MAIN"]
    scenarios = ["rank", "sel_fwd", "wormhole", "dao_flood", "mixed"]

    # ──────────────────────────────────────────────
    # Table II — Detection performance
    # ──────────────────────────────────────────────
    print("% === Table II — Detection Rate ===")
    for scen in scenarios:
        cells = [f"{scen}"]
        for var in variants:
            vals = [
                float(r["det_rate"])
                for r in det
                if r["scenario"] == scen and r["variant"] == var
            ]
            if not vals:
                cells.append("—")
            else:
                m = sum(vals) / len(vals)
                if m == 0:
                    cells.append("0.0\\%")
                else:
                    cells.append(f"{m*100:.1f}\\%")
        print("  &  ".join(cells) + r"  \\")

    print()
    print("% === Table II — FPR ===")
    for scen in scenarios:
        cells = [f"{scen}"]
        for var in variants:
            vals = [
                float(r["fpr"])
                for r in fpr_csv
                if r["scenario"] == scen and r["variant"] == var
            ]
            if not vals:
                cells.append("—")
            else:
                m = sum(vals) / len(vals)
                cells.append(f"{m*100:.2f}\\%")
        print("  &  ".join(cells) + r"  \\")

    # ──────────────────────────────────────────────
    # Table III — Operating modes
    # ──────────────────────────────────────────────
    print()
    print("% === Table III — Operating Modes ===")
    for mode_name in ["Full", "Balanced", "Eco"]:
        rows = [r for r in modes_csv if r["mode"].lower() == mode_name.lower()]
        if rows:
            dr = sum(float(r["det_rate"]) for r in rows) / len(rows)
            fpr_m = sum(float(r["fpr"]) for r in rows) / len(rows)
            cpu = sum(float(r["cpu_overhead_pct"]) for r in rows) / len(rows)
            print(
                f"  \\textsc{{{mode_name}}}  &  {dr*100:.1f}\\%  &  {fpr_m*100:.2f}\\%  &  {cpu:.0f}\\%  \\\\"
            )
        else:
            print(f"  \\textsc{{{mode_name}}}  &  —  &  —  &  —  \\\\")

    # ──────────────────────────────────────────────
    # Table IX — Statistical validation (DR)
    # ──────────────────────────────────────────────
    print()
    print("% === Table IX — DR statistics (mixed scenario) ===")

    def seed_drs(var: str, scen: str) -> dict[str, float]:
        rows = [r for r in det if r["variant"] == var and r["scenario"] == scen]
        by_seed: dict[str, dict[str, int]] = defaultdict(
            lambda: {"tp": 0, "fn": 0}
        )
        for r in rows:
            s = r["seed"]
            by_seed[s]["tp"] += int(r["tp"])
            by_seed[s]["fn"] += int(r["fn"])
        result = {}
        for s, v in by_seed.items():
            denom = v["tp"] + v["fn"]
            result[s] = v["tp"] / denom if denom else 0.0
        return result

    for baseline in ["B1", "B2", "B3"]:
        ours_dict = seed_drs("MAIN", "mixed")
        base_dict = seed_drs(baseline, "mixed")
        ours_vals = list(ours_dict.values())
        base_vals = list(base_dict.values())
        print(f"% Ours vs {baseline} DR")
        print(
            f"%   Ours: n={len(ours_vals)} mean={statistics.mean(ours_vals)*100:.2f}% "
            f"sd={statistics.stdev(ours_vals)*100:.2f}%"
        )
        print(
            f"%   {baseline}: n={len(base_vals)} mean={statistics.mean(base_vals)*100:.2f}% "
            f"sd={statistics.stdev(base_vals)*100:.2f}%"
        )

    # ──────────────────────────────────────────────
    # Latency
    # ──────────────────────────────────────────────
    print()
    print("% === Latency per (scenario, variant) ===")
    for scen in scenarios:
        cells = [f"{scen}"]
        for var in variants:
            vals = [
                float(r["latency_s_mean"])
                for r in lat
                if r["scenario"] == scen and r["variant"] == var
            ]
            if not vals:
                cells.append("—")
            else:
                cells.append(stats_str(vals))
        print("  &  ".join(cells) + r"  \\")

    # ──────────────────────────────────────────────
    # Energy
    # ──────────────────────────────────────────────
    print()
    print("% === Energy per variant (mixed, member role) ===")
    for var in variants:
        rows = [
            r
            for r in eng
            if r["variant"] == var and r["role"] == "0" and r["scenario"] == "mixed"
        ]
        if not rows:
            print(f"% {var}: —")
            continue
        cpu_vals = [float(r["cpu_overhead_pct"]) for r in rows]
        ram_vals = [float(r["ram_kb"]) for r in rows]
        energest_vals = [float(r["energest_delta_pct"]) for r in rows]
        print(
            f"% {var}: CPU={statistics.mean(cpu_vals):.1f}+-{statistics.stdev(cpu_vals):.1f}%, "
            f"RAM={statistics.mean(ram_vals):.0f}KB, "
            f"Energest={statistics.mean(energest_vals):.0f}%"
        )


if __name__ == "__main__":
    main()
