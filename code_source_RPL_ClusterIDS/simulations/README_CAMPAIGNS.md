# Campagnes Cooja — RPL-ClusterIDS (B1–B3 + Ours)

Plan expérimental pour comparer **B1** (central rules), **B2** (flat distributed), **B3** (central ML), et **MAIN** (RPL-ClusterIDS complet) sous Cooja, avec export CSV vers les figures 4–11 du manuscrit.

## Principe d'équité

- **Même** modèle radio (UDGM sky), duty cycle 10 %, **mêmes** topologies (grille + aléatoire).
- **Mêmes** générateurs trafic UDP C0–C3 et **mêmes** scénarios d'attaque.
- **Graines** distinctes ; nommer les logs `log_<VARIANT>_<TOPO>_<N>nodes_<SCENARIO>_seed<SEED>.log`.

## Variantes firmware

| Tag | Description | Flag build |
|-----|-------------|------------|
| B1 | IDS rule-based centralisé (border router) | `IDS_VARIANT=B1` |
| B2 | IDS rules distribuées plates | `IDS_VARIANT=B2` |
| B3 | Hybrid ML border router, sans clustering | `IDS_VARIANT=B3` |
| MAIN | RPL-ClusterIDS complet | `IDS_VARIANT=MAIN` |

## Pipeline

```bash
# Smoke (90 s, 3 graines)
NUM_SEEDS=3 SIM_TIMEOUT_MS=90000 ./simulations/scripts/run_ids_campaign.sh smoke

# Pilote (1800 s, 5 graines)
NUM_SEEDS=5 SIM_TIMEOUT_MS=1800000 ./simulations/scripts/run_ids_campaign.sh pilot

# Publication (3 h, ≥9 graines)
NUM_SEEDS=9 SIM_TIMEOUT_MS=10800000 ./simulations/scripts/run_ids_campaign.sh full
```

1. Exporter logs Cooja → `simulations/logs/ids_campaign/`
2. `python3 simulations/scripts/parse_cooja_ids_metrics.py --logs simulations/logs/ids_campaign/ --out $IDS_ROOT/sim/ids_campaign/`
3. `python3 $IDS_ROOT/scripts/generate_ids_figures.py --csv $IDS_ROOT/sim/ids_campaign/ --out $IDS_ROOT/Figures/`

## Scénarios d'attaque

1. rank — rang artificiellement bas
2. sel_fwd — drop 60 % downstream
3. wormhole — tunnel contrôle collusion
4. dao_flood — DAO ×10
5. mixed — rank + sel.fwd sur C3

Attaque après **30 min** (`IDS_ATTACK_START_S=1800`), durée totale **3 h** (`SIM_TIMEOUT_MS=10800000`).

## Gabarits Cooja

- Générer : `python3 simulations/scripts/generate_campaign_csc.py --nodes 50 --out simulations/cooja/ids-grid-50.csc`
- Smoke 3 nœuds : `simulations/cooja/ids-smoke-3nodes.csc` (à produire après premier build)
