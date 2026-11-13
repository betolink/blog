#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/.."

PAGEFIND_VERSION="${PAGEFIND_VERSION:-1.6.0}"

if ! command -v hugo >/dev/null 2>&1; then
  echo "error: hugo is required. Install Hugo Extended from https://gohugo.io/installation/" >&2
  exit 1
fi

bash scripts/render-notebooks.sh

bash scripts/ingest-images.sh

bash scripts/strip-image-metadata.sh

echo "==> Building site with Hugo"
hugo --minify --gc --cleanDestinationDir

if command -v npx >/dev/null 2>&1; then
  echo "==> Generating Pagefind index"
  npx --yes "pagefind@${PAGEFIND_VERSION}" --site public
else
  echo "warning: npx not found; skipping Pagefind index" >&2
  echo "warning: search will report that the index is unavailable" >&2
fi

echo "==> Checking local links"
python3 scripts/check_links.py public

echo "==> Build complete: public/"
