# Metric Definitions — RPL-ClusterIDS Campaign

**Status:** `READY_FOR_SIMULATION`

All metrics are computed from Cooja serial logs (`METRIC,...` lines) parsed by
`code_source_RPL_ClusterIDS/simulations/scripts/parse_cooja_ids_metrics.py`.

| Metric | Symbol | Unit | Definition |
|--------|--------|------|------------|
| Detection Rate | DR | ratio | TP / (TP + FN) over injected attack events |
| False Positive Rate | FPR | ratio | FP / (FP + TN) on benign intervals |
| Detection Latency | $L_{\mathrm{det}}$ | seconds | Attack onset → confirmed cluster alert |
| Energy Overhead | $\Delta E$ | % | Energest delta vs no-IDS baseline |
| CPU Overhead | $\Delta_{\mathrm{CPU}}$ | % | Contiki-NG profiling delta |
| RAM Overhead | $\Delta_{\mathrm{RAM}}$ | KB | Peak heap delta vs baseline |
| Alert Overhead | $O_{\mathrm{alert}}$ | pkt/h | IDS alert packets per hour |
| Control Overhead | $O_{\mathrm{ctrl}}$ | pkt/h | Inter-cluster control packets per hour |
| Network Lifetime | $T_{\mathrm{life}}$ | hours | Time until first node depletion |
| Cluster Stability | $S_{\mathrm{clust}}$ | — | Mean CH tenure / reclustering rate |

Log format details: `code_source_RPL_ClusterIDS/simulations/metrics/LOG_FORMAT.md`.
