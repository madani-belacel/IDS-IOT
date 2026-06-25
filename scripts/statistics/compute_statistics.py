#!/usr/bin/env python3
"""
Compute statistical validation from aggregated campaign CSVs.
Fills Table IX structure: mean, SD, 95% bootstrap CI, t-test, Mann-Whitney U.

Usage:
  python compute_statistics.py --input data/real/parsed --output data/real/statistics
  python compute_statistics.py --input data/estimated/parsed --dry-run
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np
from scipy import stats

REQUIRED_COLUMNS = [
    "variant",
    "seed",
    "attack",
    "mode",
    "nodes",
    "detection_rate",
    "fpr",
    "detection_latency_s",
    "energy_overhead_pct",
    "alert_overhead_pkt_h",
]

VARIANT_COMPARISONS = [
    ("CLUSTERIDS", "B1", "detection_rate"),
    ("CLUSTERIDS", "B2", "detection_rate"),
    ("CLUSTERIDS", "B3", "detection_rate"),
    ("CLUSTERIDS", "B1", "fpr"),
    ("CLUSTERIDS", "B2", "fpr"),
    ("CLUSTERIDS", "B3", "fpr"),
    ("CLUSTERIDS", "B2", "alert_overhead_pkt_h"),
]

MODE_COMPARISON = ("full", "eco", "detection_rate")

DEFAULT_FILTERS = {
    "attack": "mixed",
    "nodes": "50",
    "mode": "balanced",
}


@dataclass
class ComparisonResult:
    comparison: str
    metric: str
    group_a: str
    group_b: str
    n_a: int
    n_b: int
    mean_a: float
    mean_b: float
    sd_a: float
    sd_b: float
    ci_a_low: float
    ci_a_high: float
    ci_b_low: float
    ci_b_high: float
    t_stat: float
    t_p: float
    mwu_stat: float
    mwu_p: float


def load_runs(path: Path) -> list[dict[str, str]]:
    summary = path / "summary_runs.csv"
    if not summary.exists():
        return []
    with summary.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def validate_schema(rows: list[dict[str, str]]) -> list[str]:
    if not rows:
        return ["summary_runs.csv is empty"]
    missing = [c for c in REQUIRED_COLUMNS if c not in rows[0]]
    return [f"Missing column: {c}" for c in missing]


def to_float(rows: list[dict[str, str]], metric: str) -> np.ndarray:
    values = []
    for row in rows:
        try:
            values.append(float(row[metric]))
        except (KeyError, ValueError, TypeError):
            continue
    return np.array(values, dtype=float)


def bootstrap_ci(
    data: np.ndarray,
    n_bootstrap: int = 5000,
    ci: float = 0.95,
    seed: int = 42,
) -> tuple[float, float]:
    if len(data) == 0:
        return float("nan"), float("nan")
    if len(data) == 1:
        v = float(data[0])
        return v, v
    rng = np.random.default_rng(seed)
    means = np.empty(n_bootstrap)
    n = len(data)
    for i in range(n_bootstrap):
        sample = data[rng.integers(0, n, size=n)]
        means[i] = float(np.mean(sample))
    alpha = (1.0 - ci) / 2.0
    return float(np.quantile(means, alpha)), float(np.quantile(means, 1.0 - alpha))


def filter_rows(
    rows: list[dict[str, str]],
    *,
    variant: str | None = None,
    mode: str | None = None,
    attack: str | None = None,
    nodes: str | None = None,
) -> list[dict[str, str]]:
    out = rows
    if variant is not None:
        out = [r for r in out if r.get("variant") == variant]
    if mode is not None:
        out = [r for r in out if r.get("mode", "").lower() == mode.lower()]
    if attack is not None:
        out = [r for r in out if r.get("attack") == attack]
    if nodes is not None:
        out = [r for r in out if str(r.get("nodes")) == str(nodes)]
    return out


def compare_groups(
    a: np.ndarray,
    b: np.ndarray,
    comparison_label: str,
    metric: str,
    group_a: str,
    group_b: str,
) -> ComparisonResult:
    if len(a) < 2 or len(b) < 2:
        t_stat, t_p = float("nan"), float("nan")
        mwu_stat, mwu_p = float("nan"), float("nan")
    else:
        t_res = stats.ttest_ind(a, b, equal_var=False, nan_policy="omit")
        t_stat, t_p = float(t_res.statistic), float(t_res.pvalue)
        try:
            mwu_res = stats.mannwhitneyu(a, b, alternative="two-sided")
            mwu_stat, mwu_p = float(mwu_res.statistic), float(mwu_res.pvalue)
        except ValueError:
            mwu_stat, mwu_p = float("nan"), float("nan")

    ci_a = bootstrap_ci(a)
    ci_b = bootstrap_ci(b)
    return ComparisonResult(
        comparison=comparison_label,
        metric=metric,
        group_a=group_a,
        group_b=group_b,
        n_a=len(a),
        n_b=len(b),
        mean_a=float(np.mean(a)) if len(a) else float("nan"),
        mean_b=float(np.mean(b)) if len(b) else float("nan"),
        sd_a=float(np.std(a, ddof=1)) if len(a) > 1 else 0.0,
        sd_b=float(np.std(b, ddof=1)) if len(b) > 1 else 0.0,
        ci_a_low=ci_a[0],
        ci_a_high=ci_a[1],
        ci_b_low=ci_b[0],
        ci_b_high=ci_b[1],
        t_stat=t_stat,
        t_p=t_p,
        mwu_stat=mwu_stat,
        mwu_p=mwu_p,
    )


def run_comparisons(rows: list[dict[str, str]]) -> list[ComparisonResult]:
    results: list[ComparisonResult] = []
    base = filter_rows(
        rows,
        attack=DEFAULT_FILTERS["attack"],
        nodes=DEFAULT_FILTERS["nodes"],
        mode=DEFAULT_FILTERS["mode"],
    )

    for var_a, var_b, metric in VARIANT_COMPARISONS:
        a_rows = filter_rows(base, variant=var_a)
        b_rows = filter_rows(base, variant=var_b)
        a = to_float(a_rows, metric)
        b = to_float(b_rows, metric)
        label = f"{var_a} vs {var_b}"
        results.append(compare_groups(a, b, label, metric, var_a, var_b))

    mode_rows = filter_rows(
        rows,
        variant="CLUSTERIDS",
        attack=DEFAULT_FILTERS["attack"],
        nodes=DEFAULT_FILTERS["nodes"],
    )
    full_rows = filter_rows(mode_rows, mode="full")
    eco_rows = filter_rows(mode_rows, mode="eco")
    mode_a, mode_b, metric = MODE_COMPARISON
    results.append(
        compare_groups(
            to_float(full_rows, metric),
            to_float(eco_rows, metric),
            f"CLUSTERIDS {mode_a} vs {mode_b}",
            metric,
            mode_a,
            mode_b,
        )
    )
    return results


def write_pairwise_csv(results: list[ComparisonResult], out_path: Path) -> None:
    fieldnames = list(asdict(results[0]).keys()) if results else []
    with out_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in results:
            writer.writerow(asdict(r))


def write_summary_json(results: list[ComparisonResult], out_path: Path) -> None:
    payload = {
        "n_comparisons": len(results),
        "comparisons": [asdict(r) for r in results],
    }
    out_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def dry_run_report(input_dir: Path, rows: list[dict[str, str]]) -> int:
    schema_errors = validate_schema(rows)
    if schema_errors:
        print("[DRY-RUN] Schema issues:", file=sys.stderr)
        for e in schema_errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    variants = sorted({r.get("variant", "?") for r in rows})
    seeds = sorted({r.get("seed", "?") for r in rows})
    print(f"[DRY-RUN] Input: {input_dir}")
    print(f"[DRY-RUN] Rows: {len(rows)} | Variants: {variants} | Seeds: {len(seeds)}")
    print(f"[DRY-RUN] Would compute {len(VARIANT_COMPARISONS) + 1} comparisons")
    return 0


def main() -> None:
    ap = argparse.ArgumentParser(description="RPL-ClusterIDS statistics")
    ap.add_argument("--input", type=Path, required=True)
    ap.add_argument("--output", type=Path, default=None)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    rows = load_runs(args.input)
    if not rows:
        msg = f"No summary_runs.csv in {args.input}"
        if args.dry_run:
            print(f"[DRY-RUN] {msg}", file=sys.stderr)
            sys.exit(1)
        print(f"[ERROR] {msg}", file=sys.stderr)
        print("Run campaign or: python scripts/python/generate_synthetic_csv.py", file=sys.stderr)
        sys.exit(1)

    if args.dry_run:
        sys.exit(dry_run_report(args.input, rows))

    schema_errors = validate_schema(rows)
    if schema_errors:
        for e in schema_errors:
            print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)

    results = run_comparisons(rows)
    out = args.output or (args.input / "statistics")
    out.mkdir(parents=True, exist_ok=True)

    write_pairwise_csv(results, out / "pairwise_tests.csv")
    write_summary_json(results, out / "summary.json")

    print(f"[REAL_RESULT] Wrote {len(results)} comparisons to {out}")
    for r in results:
        print(
            f"  {r.comparison} ({r.metric}): "
            f"mean {r.mean_a:.3f} vs {r.mean_b:.3f}, t_p={r.t_p:.4f}, mwu_p={r.mwu_p:.4f}"
        )


if __name__ == "__main__":
    main()
