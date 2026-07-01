#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

echo "[git] Checking repository status..."
git status

echo "[git] Staging changes..."
git add .

commit_message="${1:-chore: update project artifacts}"
echo "[git] Creating commit: $commit_message"
git commit -m "$commit_message"

if [ -n "${GITHUB_TOKEN:-}" ]; then
  echo "[git] Pushing to GitHub..."
  git push
else
  echo "[git] GITHUB_TOKEN is not set. Export it before pushing."
fi
