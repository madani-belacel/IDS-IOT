# Cooja scenario templates

Place generated `.csc` files here. Generate with:

```bash
python3 ../scripts/generate_campaign_csc.py --nodes 50 --seed 20260601 --out ids-grid-50.csc
python3 ../scripts/generate_campaign_csc.py --nodes 3 --seed 1 --out ids-smoke-3nodes.csc
```

After building firmware (`make TARGET=cooja IDS_VARIANT=MAIN`), open the `.csc` in Cooja and bind the motetype to `clusterids-node.c`.
