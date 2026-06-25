#!/usr/bin/env python3
"""
Parse Cooja logs containing METRIC,... lines (see simulations/metrics/LOG_FORMAT.md).
Writes CSV files under --out for the figure pipeline (Figs 4-11).
"""
from __future__ import annotations

import argparse
import csv
import re
import typing
from collections import defaultdict
from pathlib import Path

LOG_NAME_RE = re.compile(
    r"log_(?P<variant>MAIN_NOCLUS|MAIN_NOML|MAIN_NOCTX|MAIN_NOENR|B1|B2|B3|MAIN)_"
    r"(?P<topo>\w+)_(?P<nodes>\d+)nodes_"
    r"(?P<scenario>[a-z_]+)_seed(?P<seed>\d+)\.log"
)

MODE_SUFFIXES = ("_full", "_balanced", "_eco")

CSV_SPECS: dict[str, list[str]] = {
    "detection_rate.csv": [
        "variant", "seed", "scenario", "nodes", "topology", "mode",
        "det_rate", "tp", "fp", "tn", "fn",
    ],
    "latency.csv": [
        "variant", "seed", "scenario", "latency_s_mean", "latency_s_std",
    ],
    "fpr.csv": ["variant", "seed", "scenario", "traffic_class", "fpr"],
    "energy.csv": [
        "variant", "seed", "role", "mode", "cpu_overhead_pct",
        "ram_kb", "energest_delta_pct", "nodes",
    ],
    "alerts.csv": [
        "variant", "seed", "nodes", "alerts_per_hour", "control_pkts_per_hour",
    ],
    "stability.csv": [
        "seed", "time_min", "ch_tenure_s_mean", "recluster_events", "mean_nre",
    ],
    "temporal.csv": ["seed", "phase", "det_rate"],
    "modes.csv": ["seed", "mode", "det_rate", "fpr", "cpu_overhead_pct"],
}


def parse_log_meta(path: Path) -> dict[str, str]:
    m = LOG_NAME_RE.search(path.name)
    if not m:
        return {
            "variant": "UNKNOWN",
            "topo": "grid",
            "nodes": "50",
            "scenario": "mixed",
            "seed": "0",
            "mode": "—",
        }
    raw = m.groupdict()
    scenario = raw["scenario"]
    mode = "—"
    for suffix in MODE_SUFFIXES:
        if scenario.endswith(suffix):
            mode = scenario[-len(suffix) + 1:]
            scenario = scenario[: -len(suffix)]
            break
    raw["scenario"] = scenario
    raw["mode"] = mode
    return raw


def _fix_locale_float(parts: list[str], i: int) -> str:
    """Rejoin a float split by locale decimal comma.

    printf with French locale emits "0,0050" instead of "0.0050",
    which split(',') turns into ["0","0050"].
    """
    raw = parts[i]
    if i + 1 < len(parts) and raw.isdigit() and parts[i + 1].isdigit():
        raw = f"{raw}.{parts[i + 1]}"
    return raw


def _norm_float(raw: str) -> str:
    """Convert comma decimal to dot, strip leading zeros from fractional part."""
    raw = raw.replace(",", ".")
    # Handle "0.0050" -> ok as-is
    return raw


def parse_log(path: Path) -> dict[str, list[dict]]:
    meta = parse_log_meta(path)
    seed_val = meta["seed"]
    scenario_val = meta["scenario"]
    rows: dict[str, list[dict]] = defaultdict(list)

    with path.open(encoding="utf-8", errors="replace") as f:
        for line in f:
            if not line.startswith("METRIC,"):
                continue
            kind = line.split(",", 2)[1]
            parts = line.strip().split(",")

            if kind == "DET" and len(parts) >= 10:
                dr = _fix_locale_float(parts, 9)
                rows["detection_rate.csv"].append({
                    "variant": parts[3],
                    "seed": seed_val,
                    "scenario": scenario_val,
                    "nodes": meta["nodes"],
                    "topology": meta["topo"],
                    "mode": meta.get("mode") or "—",
                    "det_rate": _norm_float(dr),
                    "tp": parts[5],
                    "fp": parts[6],
                    "tn": parts[7],
                    "fn": parts[8],
                })
            elif kind == "LAT" and len(parts) >= 6:
                rows["latency.csv"].append({
                    "variant": parts[3],
                    "seed": seed_val,
                    "scenario": scenario_val,
                    "latency_s_mean": parts[5],
                    "latency_s_std": "0",
                })
            elif kind == "FPR" and len(parts) >= 7:
                fpr_val = _fix_locale_float(parts, 6)
                rows["fpr.csv"].append({
                    "variant": parts[3],
                    "seed": seed_val,
                    "scenario": scenario_val,
                    "traffic_class": parts[5],
                    "fpr": _norm_float(fpr_val),
                })
            elif kind == "NRG" and len(parts) >= 9:
                rows["energy.csv"].append({
                    "variant": parts[3],
                    "seed": seed_val,
                    "role": parts[4],
                    "mode": parts[5],
                    "cpu_overhead_pct": parts[6],
                    "ram_kb": parts[7],
                    "energest_delta_pct": parts[8],
                    "nodes": meta["nodes"],
                })
            elif kind == "ALERT" and len(parts) >= 6:
                rows["alerts.csv"].append({
                    "variant": parts[3],
                    "seed": seed_val,
                    "nodes": parts[4],
                    "alerts_per_hour": parts[5],
                    "control_pkts_per_hour": "0",
                })
            elif kind == "CLUST" and len(parts) >= 7:
                rows["stability.csv"].append({
                    "seed": seed_val,
                    "time_min": parts[3],
                    "ch_tenure_s_mean": parts[4],
                    "recluster_events": parts[5],
                    "mean_nre": parts[6],
                })
            elif kind == "TEMP" and len(parts) >= 5:
                dr = _fix_locale_float(parts, 4)
                rows["temporal.csv"].append({
                    "seed": seed_val,
                    "phase": parts[3],
                    "det_rate": _norm_float(dr),
                })
            elif kind == "MODE" and len(parts) >= 7:
                if len(parts) >= 9:
                    # French locale with variant: METRIC,MODE,0,MAIN,Full,0,0000,0,0000,5
                    variant = parts[3]
                    mode_str = parts[4]
                    dr = f"{parts[5]}.{parts[6]}"
                    fpr_val = f"{parts[7]}.{parts[8]}"
                    cpu = parts[9] if len(parts) > 9 else 0
                elif len(parts) >= 8:
                    # Normal locale with variant: METRIC,MODE,0,MAIN,Full,0.0000,0.0000,5
                    variant = parts[3]
                    mode_str = parts[4]
                    dr = _norm_float(parts[5])
                    fpr_val = _norm_float(parts[6])
                    cpu = parts[7]
                else:
                    # Old format without variant: METRIC,MODE,0,Full,0.0000,0.0000,5
                    variant = meta.get("variant", "MAIN")
                    mode_str = parts[3]
                    dr = _norm_float(parts[4])
                    fpr_val = _norm_float(parts[5])
                    cpu = parts[6]
                rows["modes.csv"].append({
                    "seed": seed_val,
                    "variant": variant,
                    "mode": mode_str,
                    "det_rate": dr,
                    "fpr": fpr_val,
                    "cpu_overhead_pct": cpu,
                })
    return rows


def write_csv(out_dir: Path, name: str, rows: list[dict]) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    fields = CSV_SPECS[name]
    path = out_dir / name
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        for row in rows:
            w.writerow(row)


def write_manifest(out_dir: Path, log_paths: list[Path]) -> None:
    manifest = out_dir / "campaign_manifest.tsv"
    with manifest.open("w", encoding="utf-8") as f:
        f.write("log_file\tvariant\ttopology\tnodes\tscenario\tseed\n")
        for p in log_paths:
            meta = parse_log_meta(p)
            f.write(
                f"{p.name}\t{meta['variant']}\t{meta['topo']}\t"
                f"{meta['nodes']}\t{meta['scenario']}\t{meta['seed']}\n"
            )


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--logs", type=Path, required=True, help="Directory of Cooja .log files")
    ap.add_argument("--out", type=Path, required=True, help="Output directory (sim/ids_campaign/)")
    args = ap.parse_args()

    args.out.mkdir(parents=True, exist_ok=True)
    handles: dict[str, typing.IO] = {}
    writers: dict[str, csv.DictWriter] = {}

    for name, fields in CSV_SPECS.items():
        path = args.out / name
        f = path.open("w", newline="", encoding="utf-8")
        handles[name] = f
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        writers[name] = w

    log_paths = sorted(args.logs.glob("*.log"))

    for lp in log_paths:
        for name, rows in parse_log(lp).items():
            w = writers[name]
            for row in rows:
                w.writerow(row)

    for f in handles.values():
        f.close()

    stats_dir = args.out / "stats"
    stats_dir.mkdir(parents=True, exist_ok=True)
    write_manifest(args.out, log_paths)
    print(f"Parsed {len(log_paths)} logs -> {args.out}")


if __name__ == "__main__":
    main()
