#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/.."

if [ -z "${CONDA_PREFIX:-}" ]; then
  echo "warning: CONDA_PREFIX is not set; run this through Pixi" >&2
  exit 0
fi

MARKER="${CONDA_PREFIX}/.betolink-git-packages-v1"
if [ -f "${MARKER}" ]; then
  exit 0
fi

if ! command -v uv >/dev/null 2>&1; then
  echo "error: uv is required to install the earthaccess Git packages" >&2
  exit 1
fi

echo "==> Installing earthaccess virtual-plugin and plugin ecosystem"
uv pip install --python "${CONDA_PREFIX}/bin/python" --no-deps \
  "earthaccess-plugin-spec @ git+https://github.com/betolink/earthaccess-plugin-spec.git@d793d8c31cdf6f236577a73a3e0d1c7c529bf5ad" \
  "earthaccess @ git+https://github.com/betolink/earthaccess.git@463e904f2ba7b772499b7190f1dfdeafdc034a78" \
  "earthaccess-plugin-vds @ git+https://github.com/betolink/earthaccess-plugin-vds.git@566cd354cfd423ab7898145aa541f887affdef17" \
  "earthaccess-harmony @ git+https://github.com/betolink/earthaccess-plugin-harmony.git@de743b8f6bff9f60fab15b3569f458484beeb3b2" \
  "earthaccess-pydap @ git+https://github.com/betolink/earthaccess-plugin-pydap.git@fb8065cae762ff6873254a739c5ff229a91560e0" \
  "earthaccess-sliderule @ git+https://github.com/betolink/earthaccess-plugin-sliderule.git@d50526998698f63de4d7bc639a6cb02566a70175"

touch "${MARKER}"
