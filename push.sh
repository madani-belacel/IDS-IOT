#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
if [ -z "${GITHUB_TOKEN:-}" ]; then
  echo "Set GITHUB_TOKEN before pushing." >&2
  exit 1
fi
git add .
git commit -m "Update - $(date '+%Y-%m-%d %H:%M')"
git push "https://x-access-token:${GITHUB_TOKEN}@github.com/madani-belacel/IDS-IOT.git" main
