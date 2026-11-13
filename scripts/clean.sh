#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/.."

rm -rf public resources/_gen static/notebooks-src quarto/.quarto .quarto
if [ -d content/notebooks ]; then
  find content/notebooks -mindepth 1 -maxdepth 1 ! -name '_index.md' -exec rm -rf {} +
fi

echo "Cleaned generated build artifacts."
