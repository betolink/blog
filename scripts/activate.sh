#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if [ -n "${CONDA_PREFIX:-}" ]; then
  bash "${ROOT}/scripts/install-git-packages.sh"
fi
