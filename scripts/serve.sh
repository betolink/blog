#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/.."

bash scripts/render-notebooks.sh

exec hugo server -D --bind 0.0.0.0 "$@"
