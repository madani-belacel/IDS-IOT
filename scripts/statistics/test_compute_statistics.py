#!/usr/bin/env python3
"""Unit tests for compute_statistics.py using synthetic data."""
from __future__ import annotations

import csv
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "statistics"))

import compute_statistics as cs  # noqa: E402


def _write_summary(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


def _base_row(**overrides) -> dict:
    row = {
        "variant": "CLUSTERIDS",
        "seed": "1",
        "attack": "mixed",
        "mode": "balanced",
        "nodes": "50",
        "topology": "grid",
        "detection_rate": "0.92",
        "fpr": "0.04",
        "detection_latency_s": "120",
        "energy_overhead_pct": "8.5",
        "alert_overhead_pkt_h": "45",
    }
    row.update(overrides)
    return row


class TestComputeStatistics(unittest.TestCase):
    def test_bootstrap_ci_single_value(self):
        low, high = cs.bootstrap_ci(cs.np.array([0.9]))
        self.assertEqual(low, 0.9)
        self.assertEqual(high, 0.9)

    def test_compare_groups_produces_pvalues(self):
        a = cs.np.array([0.90, 0.91, 0.92, 0.93, 0.94])
        b = cs.np.array([0.70, 0.71, 0.72, 0.73, 0.74])
        r = cs.compare_groups(a, b, "test", "detection_rate", "A", "B")
        self.assertLess(r.t_p, 0.05)
        self.assertLess(r.mwu_p, 0.05)
        self.assertGreater(r.mean_a, r.mean_b)

    def test_run_comparisons_integration(self):
        rows = []
        for seed in range(1, 21):
            rows.append(_base_row(seed=str(seed), variant="CLUSTERIDS", detection_rate=str(0.90 + seed * 0.001)))
            rows.append(_base_row(seed=str(seed), variant="B1", detection_rate=str(0.75 + seed * 0.001)))
            rows.append(_base_row(seed=str(seed), variant="B2", detection_rate=str(0.78 + seed * 0.001)))
            rows.append(_base_row(seed=str(seed), variant="B3", detection_rate=str(0.80 + seed * 0.001)))
        for seed in range(1, 21):
            rows.append(_base_row(seed=str(seed), variant="CLUSTERIDS", mode="full", detection_rate="0.95"))
            rows.append(_base_row(seed=str(seed), variant="CLUSTERIDS", mode="eco", detection_rate="0.82"))

        with tempfile.TemporaryDirectory() as tmp:
            inp = Path(tmp)
            _write_summary(inp / "summary_runs.csv", rows)
            results = cs.run_comparisons(rows)
            self.assertEqual(len(results), len(cs.VARIANT_COMPARISONS) + 1)
            out = inp / "statistics"
            out.mkdir()
            cs.write_pairwise_csv(results, out / "pairwise_tests.csv")
            self.assertTrue((out / "pairwise_tests.csv").exists())

    def test_dry_run_schema_validation(self):
        with tempfile.TemporaryDirectory() as tmp:
            inp = Path(tmp)
            bad = [{"variant": "CLUSTERIDS", "seed": "1"}]
            _write_summary(inp / "summary_runs.csv", bad)
            code = cs.dry_run_report(inp, bad)
            self.assertEqual(code, 1)


if __name__ == "__main__":
    unittest.main()
