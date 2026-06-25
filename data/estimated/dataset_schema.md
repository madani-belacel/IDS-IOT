# ML Dataset Schema — RPL-ClusterIDS

**Status:** `READY_FOR_SIMULATION`

## Source

Cooja serial logs from benign and attack runs (all variants, all scales).

## Label classes

| Label | Description |
|-------|-------------|
| 0 | Benign |
| 1 | Rank attack |
| 2 | Selective forwarding |
| 3 | Wormhole |
| 4 | DAO flooding |
| 5 | Mixed campaign |

## Features (12 dimensions)

See Table `tab:features` in manuscript (`tables/table06_dataset.tex`).

## Split

- Training: 70%
- Validation: 15%
- Test: 15%
- Stratified by label

## Output files (Phase 2)

```
data/real/ml/
  features_train.csv
  features_val.csv
  features_test.csv
  labels_*.csv
  model_ch_gbdt.bin
```

## Sample count

`ESTIMATED` — populated after log parsing.
