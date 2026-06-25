# Ablation Variants — Build Commands

**Matrix rows:** 30–33 in `campaign_matrix.tsv`
**Baseline (Full):** row 22 — `CLUSTERIDS`, mixed, balanced

## Variant Mapping

| Matrix `variant` | Table VIII row | Build command (Phase 2) |
|------------------|----------------|-------------------------|
| `CLUSTERIDS` + mode `full`/`balanced`/`eco` | Full RPL-ClusterIDS | `make TARGET=cooja IDS_VARIANT=CLUSTERIDS IDS_CONF_CAMPAIGN_METRICS=1` |
| `CLUSTERIDS_NOCLUS` | Without clustering | `make TARGET=cooja IDS_VARIANT=CLUSTERIDS_NOCLUS IDS_CONF_CAMPAIGN_METRICS=1` |
| `CLUSTERIDS_NOML` | Without ML (members only) | `make TARGET=cooja IDS_VARIANT=CLUSTERIDS_NOML IDS_CONF_CAMPAIGN_METRICS=1` |
| `CLUSTERIDS_NOCTX` | Without context adaptation | `make TARGET=cooja IDS_VARIANT=CLUSTERIDS_NOCTX IDS_CONF_CAMPAIGN_METRICS=1` |
| `CLUSTERIDS_NOENR` | Without energy awareness | `make TARGET=cooja IDS_VARIANT=CLUSTERIDS_NOENR IDS_CONF_CAMPAIGN_METRICS=1` |

## Compile-Time Defines (in Makefile)

| Variant | Defines added |
|---------|--------------|
| `CLUSTERIDS_NOCLUS` / `NOCLUS` | `-DIDS_VARIANT_CLUSTERIDS=1 -DIDS_ABLATION_NOCLUS=1` + `imacros-NOCLUS.h` |
| `CLUSTERIDS_NOML` / `NOML` | `-DIDS_VARIANT_CLUSTERIDS=1 -DIDS_ABLATION_NOML=1` + `imacros-NOML.h` |
| `CLUSTERIDS_NOCTX` / `NOCTX` | `-DIDS_VARIANT_CLUSTERIDS=1 -DIDS_ABLATION_NOCTX=1` + `imacros-NOCTX.h` |
| `CLUSTERIDS_NOENR` / `NOENR` | `-DIDS_VARIANT_CLUSTERIDS=1 -DIDS_ABLATION_NOENR=1` + `imacros-NOENR.h` |

## Campaign Execution

```bash
export CONTIKI_NG=/home/madani/contiki-ng
cd code_source_RPL_ClusterIDS/simulations/scripts

# Pilot (3 seeds)
NUM_SEEDS=3 ./run_ids_campaign.sh batch 30-33

# Full (20 seeds)
./run_ids_campaign.sh batch 30-33
```
