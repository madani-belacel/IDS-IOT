# raw/stats — REMOVED

Previously contained pairwise_tests.csv and summary.json with corrupt/invalid values:
- B3 comparisons had n_b=1 (single observation), impossible t-test
- "full vs eco" had n_a=0, n_b=0, all NaN
- B1/B2/B2 means were 0.0 with sd=0.0
- mwu_p was NaN for alert_overhead

These files have been removed. Regenerate after running the full simulation campaign:

    python scripts/statistics/compute_statistics.py \
        --input data/estimated/aggregated \
        --output data/raw/stats

(Real data in data/real/parsed/ has a different schema and requires an aggregation step to produce summary_runs.csv first.)

See scripts/statistics/compute_statistics.py for details.
