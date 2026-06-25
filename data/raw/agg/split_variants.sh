#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
export LC_NUMERIC=C

# Split a CSV by column N value
split_var() {
  local base="$1" prefix="$2" col="$3"
  for var in B1 B2 B3 CLUSTERIDS; do
    head -1 "${base}.csv" > "${base}_${var}.csv"
    awk -F, -v c="$col" -v v="$var" '$c==v' "${base}.csv" >> "${base}_${var}.csv"
  done
}

split_var fig4_detection_rate fig4 1
split_var fig5_latency fig5 1

# fig6: split by variant, add C-prefix to class column
for var in B1 B2 B3 CLUSTERIDS; do
  printf "variant,label,fpr\n" > fig6_${var}.csv
  awk -F, -v v="$var" '$1==v { printf "%s,C%c,%s\n", $1, 48+$2, $3 }' fig6_fpr.csv >> fig6_${var}.csv
done

# fig7: split by role (0=member, 1=CH), relabel CLUSTERIDS -> RPL-ClusterIDS
for role in 0 1; do
  rname="member"
  [ "$role" = "1" ] && rname="ch"
  printf "variant,energest_delta_pct\n" > fig7_${rname}.csv
  awk -F, -v r="$role" '$2==r {
    v = $1;
    if(v=="CLUSTERIDS") v="RPL-ClusterIDS";
    printf "%s,%s\n", v, $4
  }' fig7_energy.csv >> fig7_${rname}.csv
done

split_var fig8_alerts fig8 1

echo "Split complete."
wc -l fig4_*.csv fig5_*.csv fig6_*.csv fig7_*.csv fig8_*.csv
