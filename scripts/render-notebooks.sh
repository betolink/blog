#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/.."

python3 scripts/render_notebooks_incremental.py "$@"

echo "==> Publishing original notebook sources for download"
rm -rf static/notebooks-src
mkdir -p static/notebooks-src
cp -R notebooks/. static/notebooks-src/

echo "==> Notebooks ready in content/notebooks and static/notebooks-src"
