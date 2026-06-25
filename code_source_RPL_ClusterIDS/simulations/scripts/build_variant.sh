#!/bin/sh
# Build commands for the four IDS firmware variants.

CONTIKI="${CONTIKI:-$(cd "$(dirname "$0")/../../../../../../" && pwd)}"
IDS_DIR="$(cd "$(dirname "$0")/../.." && pwd)"

usage() {
  echo "Usage: $0 [B1 | B2 | B3 | MAIN]"
  echo "CONTIKI=$CONTIKI"
  echo "IDS_DIR=$IDS_DIR"
}

case "$1" in
  B1|B2|B3|MAIN)
    echo "cd \"$IDS_DIR\""
    echo "make clean && make TARGET=cooja IDS_VARIANT=$1 IDS_CONF_CAMPAIGN_METRICS=1"
    ;;
  "")
    usage
    ;;
  *)
    usage
    exit 1
    ;;
esac
