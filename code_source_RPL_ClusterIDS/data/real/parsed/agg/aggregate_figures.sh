#!/usr/bin/env bash
# Pre-aggregate CSV data for PGFPlots figures 4-11
# Single-pass aggregation with LC_NUMERIC=C for dot decimals
set -euo pipefail
cd "$(dirname "$0")"
export LC_NUMERIC=C

# Fig 4: detection_rate — exclude 'none' scenario
awk -F, '
  BEGIN { print "variant,scenario,mean_det_rate" }
  NR>1 && $3!="none" { k=$1","$3; sum[k]+=$7; n[k]++ }
  END {
    for(k in sum) printf "%s,%.4f\n", k, sum[k]/n[k]
  }
' ../detection_rate.csv > fig4_detection_rate.csv

# Fig 5: latency — exclude 'none' scenario
awk -F, '
  BEGIN { print "variant,scenario,mean_latency_s" }
  NR>1 && $3!="none" { k=$1","$3; sum[k]+=$4; n[k]++ }
  END {
    for(k in sum) printf "%s,%.2f\n", k, sum[k]/n[k]
  }
' ../latency.csv > fig5_latency.csv

# Fig 6: fpr
awk -F, '
  BEGIN { print "variant,class,fpr" }
  NR>1 { k=$1","$4; sum[k]+=$5; n[k]++ }
  END {
    for(k in sum) printf "%s,%.4f\n", k, sum[k]/n[k]
  }
' ../fpr.csv > fig6_fpr.csv

# Fig 7: energy — cols: variant(1), seed(2), role(3), mode(4), cpu_pct(5), ram_kb(6), energest_delta(7), nodes(8)
awk -F, '
  BEGIN { print "variant,role,cpu_pct,energest_delta_pct" }
  NR>1 { k=$1","$3; cpusum[k]+=$5; enersum[k]+=$7; n[k]++ }
  END {
    for(k in cpusum) printf "%s,%.2f,%.2f\n", k, cpusum[k]/n[k], enersum[k]/n[k]
  }
' ../energy.csv > fig7_energy.csv

# Fig 8: alerts
awk -F, '
  BEGIN { print "variant,nodes,mean_alerts_per_hour,mean_ctrl_pkts_per_hour" }
  NR>1 { k=$1","$3; asum[k]+=$4; csum[k]+=$5; n[k]++ }
  END {
    for(k in asum) printf "%s,%.2f,%.2f\n", k, asum[k]/n[k], csum[k]/n[k]
  }
' ../alerts.csv > fig8_alerts.csv

# Fig 9: stability — cols: seed(1), time_min(2), ch_tenure_s_mean(3), recluster_events(4), mean_nre(5)
awk -F, '
  BEGIN { print "time_min,mean_ch_tenure_s,mean_recluster_events,mean_nre" }
  NR>1 { tm=$2; tenure_sum[tm]+=$3; rec_sum[tm]+=$4; nre_sum[tm]+=$5; n[tm]++ }
  END {
    for(tm in tenure_sum) printf "%s,%.2f,%.2f,%.0f\n", tm, tenure_sum[tm]/n[tm], rec_sum[tm]/n[tm], nre_sum[tm]/n[tm]
  }
' ../stability.csv | sort -t, -k1 -n > fig9_stability.csv

# Fig 10: temporal
awk -F, '
  BEGIN { print "phase,mean_det_rate" }
  NR>1 { k=$2; sum[k]+=$3; n[k]++ }
  END {
    for(k in sum) printf "%s,%.4f\n", k, sum[k]/n[k]
  }
' ../temporal.csv > fig10_temporal.csv

# Fig 11: modes — only standard modes (Full/Balanced/Eco)
# modes.csv has no variant column; all rows are CLUSTERIDS
awk -F, '
  BEGIN { print "mode,mean_det_rate,mean_fpr,mean_cpu" }
  NR>1 && ($2=="Full" || $2=="Balanced" || $2=="Eco") {
    k=$2; drsum[k]+=$3; fprsum[k]+=$4; cpusum[k]+=$5; n[k]++
  }
  END {
    for(k in drsum) printf "%s,%.4f,%.4f,%.2f\n", k, drsum[k]/n[k], fprsum[k]/n[k], cpusum[k]/n[k]
  }
' ../modes.csv > fig11_modes.csv

echo "All aggregations complete."
wc -l fig*.csv
