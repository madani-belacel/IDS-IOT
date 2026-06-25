#!/usr/bin/env python3
"""
SYNTHETIC DATA GENERATOR — NOT FOR MANUSCRIPT SUBMISSION.

Generates campaign CSVs from random distributions (gaussian, uniform)
for pipeline testing and schema validation.  ALL OUTPUTS ARE SYNTHETIC
and must NOT be used as experimental results.

The real Cooja campaign produces logs in data/real/raw_logs/ and the
parsing pipeline (parse_cooja_ids_metrics.py) converts them to the
aggregated format.  This script exists solely to help develop and test
the figure-generation and statistics toolchain before the real data is
available.

Usage:
  python generate_synthetic_csv.py
  python generate_synthetic_csv.py --out data/estimated/aggregated --seeds 20
"""
from __future__ import annotations

import argparse
import csv
import random
from pathlib import Path

ATTACKS = ["rank", "sel_fwd", "wormhole", "dao_flood", "mixed"]
VARIANTS = ["B1", "B2", "B3", "CLUSTERIDS"]
MODES = ["full", "balanced", "eco"]
SCALES = [50, 100, 200, 300, 500]
TRAFFIC_CLASSES = ["C0", "C1", "C2", "C3"]
PHASES = ["stabilization", "attack", "recovery"]
ROLES = ["member", "cluster_head"]
ABLATION_VARIANTS = [
    "CLUSTERIDS",
    "CLUSTERIDS_NOCLUS",
    "CLUSTERIDS_NOML",
    "CLUSTERIDS_NOCTX",
    "CLUSTERIDS_NOENR",
]

DR_BASE = {
    "B1": 0.78,
    "B2": 0.82,
    "B3": 0.85,
    "CLUSTERIDS": 0.93,
    "CLUSTERIDS_NOCLUS": 0.86,
    "CLUSTERIDS_NOML": 0.89,
    "CLUSTERIDS_NOCTX": 0.88,
    "CLUSTERIDS_NOENR": 0.87,
}


def jitter(base: float, spread: float = 0.02) -> float:
    return round(max(0.0, min(1.0, base + random.gauss(0, spread))), 4)


def write_csv(path: Path, fieldnames: list[str], rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)


def generate_summary_runs(seeds: int) -> list[dict]:
    rows: list[dict] = []
    for seed in range(1, seeds + 1):
        for attack in ATTACKS:
            for variant in VARIANTS:
                mode = "balanced"
                dr = jitter(DR_BASE[variant] - (0.03 if attack == "wormhole" else 0))
                rows.append(
                    {
                        "variant": variant,
                        "seed": str(seed),
                        "scenario": attack,
                        "nodes": "50",
                        "topology": "grid",
                        "attack": attack,
                        "mode": mode,
                        "detection_rate": str(dr),
                        "fpr": str(jitter(0.05 if variant == "B2" else 0.03, 0.008)),
                        "detection_latency_s": str(round(random.uniform(80, 200), 1)),
                        "energy_overhead_pct": str(round(random.uniform(5, 12), 2)),
                        "cpu_overhead_pct": str(round(random.uniform(2, 8), 2)),
                        "ram_overhead_kb": str(round(random.uniform(1.5, 3.0), 2)),
                        "alert_overhead_pkt_h": str(round(30 + (50 if variant == "B2" else 20) + random.gauss(0, 5), 1)),
                        "control_overhead_pkt_h": str(round(random.uniform(10, 25), 1)),
                        "network_lifetime_h": str(round(random.uniform(2.5, 3.0), 3)),
                        "cluster_stability": str(jitter(0.88 if variant == "CLUSTERIDS" else 0.5, 0.03)),
                        "status": "SYNTHETIC",
                    }
                )
        for mode in MODES:
            dr = {"full": 0.95, "balanced": 0.93, "eco": 0.82}[mode]
            rows.append(
                {
                    "variant": "CLUSTERIDS",
                    "seed": str(seed),
                    "scenario": "mixed",
                    "nodes": "50",
                    "topology": "grid",
                    "attack": "mixed",
                    "mode": mode,
                    "detection_rate": str(jitter(dr)),
                    "fpr": str(jitter(0.025 if mode != "eco" else 0.015, 0.006)),
                    "detection_latency_s": str(round(random.uniform(90, 160), 1)),
                    "energy_overhead_pct": str(round({"full": 11, "balanced": 8.5, "eco": 5.5}[mode] + random.gauss(0, 0.5), 2)),
                    "cpu_overhead_pct": str(round({"full": 7, "balanced": 5, "eco": 3}[mode] + random.gauss(0, 0.3), 2)),
                    "ram_overhead_kb": "2.8",
                    "alert_overhead_pkt_h": str(round({"full": 55, "balanced": 42, "eco": 28}[mode] + random.gauss(0, 3), 1)),
                    "control_overhead_pkt_h": "18",
                    "network_lifetime_h": str(round({"full": 2.6, "balanced": 2.8, "eco": 3.0}[mode], 3)),
                    "cluster_stability": str(jitter(0.9, 0.02)),
                    "status": "SYNTHETIC",
                }
            )
        for abl in ABLATION_VARIANTS:
            rows.append(
                {
                    "variant": abl,
                    "seed": str(seed),
                    "scenario": "mixed",
                    "nodes": "50",
                    "topology": "grid",
                    "attack": "mixed",
                    "mode": "balanced",
                    "detection_rate": str(jitter(DR_BASE[abl])),
                    "fpr": str(jitter(0.04, 0.01)),
                    "detection_latency_s": str(round(random.uniform(95, 170), 1)),
                    "energy_overhead_pct": str(round(random.uniform(6, 11), 2)),
                    "cpu_overhead_pct": "5",
                    "ram_overhead_kb": "2.8",
                    "alert_overhead_pkt_h": str(round(35 + random.gauss(0, 4), 1)),
                    "control_overhead_pkt_h": "16",
                    "network_lifetime_h": "2.75",
                    "cluster_stability": str(jitter(0.85, 0.04)),
                    "status": "SYNTHETIC",
                }
            )
        for nodes in SCALES:
            if nodes == 50:
                continue
            alert_b2 = 40 + nodes * 0.35
            alert_ours = 25 + nodes * 0.12
            for variant, alert in [("B2", alert_b2), ("CLUSTERIDS", alert_ours)]:
                rows.append(
                    {
                        "variant": variant,
                        "seed": str(seed),
                        "scenario": "mixed",
                        "nodes": str(nodes),
                        "topology": "grid",
                        "attack": "mixed",
                        "mode": "balanced",
                        "detection_rate": str(jitter(DR_BASE[variant] - nodes * 0.0001)),
                        "fpr": "0.03",
                        "detection_latency_s": "130",
                        "energy_overhead_pct": "8",
                        "cpu_overhead_pct": "5",
                        "ram_overhead_kb": "2.8",
                        "alert_overhead_pkt_h": str(round(alert + random.gauss(0, 5), 1)),
                        "control_overhead_pkt_h": "15",
                        "network_lifetime_h": "2.7",
                        "cluster_stability": "0.87",
                        "status": "SYNTHETIC",
                    }
                )
    return rows


def aggregate_metric_files(summary: list[dict], out_dir: Path) -> None:
    dr_rows = [
        {
            "nodes": r["nodes"],
            "topology": r["topology"],
            "attack": r["attack"],
            "variant": r["variant"],
            "mode": r["mode"],
            "seed": r["seed"],
            "detection_rate": r["detection_rate"],
        }
        for r in summary
    ]
    write_csv(out_dir / "detection_rate.csv", list(dr_rows[0].keys()), dr_rows)

    lat_rows = [
        {
            "nodes": r["nodes"],
            "attack": r["attack"],
            "variant": r["variant"],
            "seed": r["seed"],
            "detection_latency_s": r["detection_latency_s"],
        }
        for r in summary
        if r["nodes"] == "50"
    ]
    write_csv(out_dir / "detection_latency.csv", list(lat_rows[0].keys()), lat_rows)

    fpr_rows = []
    for r in summary:
        if r["nodes"] != "50" or r["attack"] == "mixed":
            continue
        for tc in TRAFFIC_CLASSES:
            fpr_rows.append(
                {
                    "attack": r["attack"],
                    "traffic_class": tc,
                    "variant": r["variant"],
                    "seed": r["seed"],
                    "fpr": str(jitter(float(r["fpr"]) + (0.01 if tc == "C3" else 0), 0.005)),
                }
            )
    write_csv(out_dir / "fpr.csv", list(fpr_rows[0].keys()), fpr_rows)

    energy_rows = []
    for r in summary:
        if r["attack"] != "mixed" or r["nodes"] != "50":
            continue
        for role in ROLES:
            base = float(r["energy_overhead_pct"])
            energy_rows.append(
                {
                    "nodes": r["nodes"],
                    "variant": r["variant"],
                    "role": role,
                    "seed": r["seed"],
                    "energy_overhead_pct": str(round(base * (1.2 if role == "cluster_head" else 0.7), 2)),
                }
            )
    write_csv(out_dir / "energy_overhead.csv", list(energy_rows[0].keys()), energy_rows)

    alert_rows = [
        {
            "nodes": r["nodes"],
            "topology": r["topology"],
            "variant": r["variant"],
            "seed": r["seed"],
            "alert_overhead_pkt_h": r["alert_overhead_pkt_h"],
            "control_overhead_pkt_h": r["control_overhead_pkt_h"],
        }
        for r in summary
        if r["attack"] == "mixed" and r["mode"] == "balanced"
    ]
    write_csv(out_dir / "alert_overhead.csv", list(alert_rows[0].keys()), alert_rows)

    stab_rows = [
        {
            "nodes": r["nodes"],
            "seed": r["seed"],
            "ch_tenure_s": str(round(random.uniform(600, 1500), 0)),
            "recluster_rate": str(round(random.uniform(0.05, 0.2), 4)),
            "mean_nre": str(jitter(0.55, 0.05)),
            "cluster_stability": r["cluster_stability"],
        }
        for r in summary
        if r["variant"] == "CLUSTERIDS" and r["attack"] == "mixed"
    ]
    write_csv(out_dir / "cluster_stability.csv", list(stab_rows[0].keys()), stab_rows)

    temp_rows = []
    for seed in range(1, int(max(r["seed"] for r in summary)) + 1):
        for phase, base in zip(PHASES, [0.99, 0.91, 0.94]):
            temp_rows.append(
                {
                    "seed": str(seed),
                    "phase": phase,
                    "detection_rate": str(jitter(base, 0.015)),
                }
            )
    write_csv(out_dir / "temporal_detection.csv", ["seed", "phase", "detection_rate"], temp_rows)

    mode_rows = [
        {
            "mode": r["mode"],
            "seed": r["seed"],
            "detection_rate": r["detection_rate"],
            "fpr": r["fpr"],
            "cpu_overhead_pct": r["cpu_overhead_pct"],
        }
        for r in summary
        if r["variant"] == "CLUSTERIDS" and r["attack"] == "mixed" and r["nodes"] == "50"
    ]
    write_csv(out_dir / "operating_modes.csv", list(mode_rows[0].keys()), mode_rows)

    ablation_rows = [
        {
            "variant": r["variant"],
            "seed": r["seed"],
            "detection_rate": r["detection_rate"],
            "fpr": r["fpr"],
            "energy_overhead_pct": r["energy_overhead_pct"],
        }
        for r in summary
        if r["variant"] in ABLATION_VARIANTS and r["attack"] == "mixed" and r["mode"] == "balanced"
    ]
    write_csv(out_dir / "ablation_mixed.csv", list(ablation_rows[0].keys()), ablation_rows)

    write_csv(out_dir / "summary_runs.csv", list(summary[0].keys()), summary)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=Path("data/estimated/aggregated"))
    ap.add_argument("--seeds", type=int, default=20)
    ap.add_argument("--seed", type=int, default=42, help="RNG seed for reproducibility")
    args = ap.parse_args()

    random.seed(args.seed)
    summary = generate_summary_runs(args.seeds)
    aggregate_metric_files(summary, args.out)
    print(f"[SYNTHETIC] Wrote {len(summary)} runs + 9 CSV files to {args.out}")
    print("[NOTE] Data is for pipeline testing only — not for manuscript submission.")


if __name__ == "__main__":
    main()
