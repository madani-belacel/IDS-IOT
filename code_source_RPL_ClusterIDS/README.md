# RPL-ClusterIDS — Firmware de référence Contiki-NG

Implémentation de référence pour l'évaluation Cooja d'un IDS distribué
avec clustering adaptatif, 4 lignes de base (B1–B3 + MAIN),
5 scénarios d'attaque, et logging structuré `METRIC,...`.

**Statut (juin 2026) :** compile sur Ubuntu 22.04 + Contiki-NG ;
campagne de validation terminée (voir `SIMULATION_CAMPAIGN_READY/`).

## Modules principaux

| Fichier | Rôle |
|---------|------|
| `clusterids-node.c` | Trafic UDP (C0–C3), racine RPL, orchestre la couche IDS |
| `clus_form.c` / `.h` | Affinité de cluster (Eq. 1), re-clustering (Eq. 2) |
| `ch_elect.c` / `.h` | Fitness CH (Eq. 3), rotation |
| `ids_member.c` / `.h` | Règles R1–R4, LAS (Eq. 4), rapports membres |
| `ids_ch.c` / `.h` | Agrégation LAS, confirmation au niveau CH |
| `ctx_policy.c` / `.h` | Modes Full / Balanced / Eco |
| `ids_attack.c` / `.h` | Générateurs d'attaques (rank, sel.fwd, wormhole, DAO flood, mixed) |
| `ids_campaign_log.c` / `.h` | Lignes `METRIC,...` pour le pipeline de parsing |
| `variants/` | Présets Makefile (B1, B2, B3, MAIN, ablations) |

## Compilation (Cooja)

Depuis ce répertoire (avec `CONTIKI` pointant vers votre arbre Contiki-NG) :

```bash
export CONTIKI=/chemin/vers/contiki-ng
make clean
make TARGET=cooja IDS_VARIANT=MAIN IDS_CONF_CAMPAIGN_METRICS=1
```

Utilisez `simulations/scripts/build_variant.sh` pour les 7 variantes.

## Déploiement Ubuntu

```bash
export IDS_ROOT=/chemin/vers/IDS_IOT
export IDS_CODE=$IDS_ROOT/code_source_RPL_ClusterIDS
cd $IDS_CODE
make TARGET=cooja IDS_VARIANT=MAIN IDS_CONF_CAMPAIGN_METRICS=1
```

Test rapide (3 seeds, timeout 90s) :

```bash
NUM_SEEDS=3 SIM_TIMEOUT_MS=90000 ./simulations/scripts/run_ids_campaign.sh smoke
```

## Documentation liée

- `simulations/README_CAMPAIGNS.md` — plan de campagne
- `simulations/metrics/LOG_FORMAT.md` — schéma des logs structurés
