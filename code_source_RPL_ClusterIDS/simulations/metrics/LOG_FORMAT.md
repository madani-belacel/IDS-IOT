# Format de log structuré `METRIC,...` (campagnes Cooja IDS)

Objectif : lignes **une par événement**, préfixe **`METRIC`**, champs séparés par des **virgules**, faciles à `grep` et à ingérer en CSV.

## Préfixe

```text
METRIC,<TYPE>,...
```

## Types définis (RPL-ClusterIDS)

| TYPE | Champs (ordre) | Description |
|------|----------------|-------------|
| `DET` | `DET,<seed>,<variant>,<scenario>,<tp>,<fp>,<tn>,<fn>,<det_rate>` | Matrice de confusion agrégée |
| `LAT` | `LAT,<seed>,<variant>,<scenario>,<latency_s_mean>` | Latence moyenne de détection (s) |
| `FPR` | `FPR,<seed>,<variant>,<scenario>,<class>,<fpr>` | Faux positifs par classe C0–C3 |
| `NRG` | `NRG,<seed>,<variant>,<role>,<mode>,<cpu_pct>,<ram_kb>,<energest_delta_pct>` | Overhead ressource |
| `ALERT` | `ALERT,<seed>,<variant>,<nodes>,<alerts_per_hour>` | Charge alertes |
| `CLUST` | `CLUST,<seed>,<time_min>,<ch_tenure_s>,<recluster_rate>,<mean_nre>` | Stabilité clusters |
| `TEMP` | `TEMP,<seed>,<phase>,<det_rate>` | phase ∈ stab \| attack \| recovery |
| `MODE` | `MODE,<seed>,<mode>,<det_rate>,<fpr>,<cpu_pct>` | mode ∈ Full \| Balanced \| Eco |
| `ATTACK` | `ATTACK,<seed>,<scenario>,<event_id>,<t_start>,<t_end>` | Ground truth attaque |

## Activation

```bash
make clean
make IDS_CONF_CAMPAIGN_METRICS=1 IDS_VARIANT=MAIN \
     IDS_CAMPAIGN_SEED=20260601 IDS_CAMPAIGN_SCENARIO=rank TARGET=cooja
```

Les lignes `METRIC,...` apparaissent sur la sortie série Cooja. Le parseur `parse_cooja_ids_metrics.py` agrège vers `IDS_IOT/sim/ids_campaign/*.csv`.
