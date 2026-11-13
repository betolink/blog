#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/.."

if ! command -v exiftool >/dev/null 2>&1; then
  echo "error: exiftool is required. Run this through Pixi or install exiftool." >&2
  exit 1
fi

files=()
while IFS= read -r -d '' file; do
  files+=("${file}")
done < <(find content static assets -type f \
  \( -iname '*.jpg' -o -iname '*.jpeg' -o -iname '*.png' -o -iname '*.webp' -o -iname '*.tif' -o -iname '*.tiff' -o -iname '*.heic' \) \
  -print0)

if [ "${#files[@]}" -eq 0 ]; then
  echo "No images found under content, static, or assets."
  exit 0
fi

for file in "${files[@]}"; do
  exiftool -q -overwrite_original -all= \
    -tagsfromfile @ -Orientation -ColorSpaceTags "${file}"

  if exiftool -q -s -GPSLatitude -GPSLongitude -GPSPosition "${file}" | grep -q .; then
    echo "error: GPS metadata remains in ${file}" >&2
    exit 1
  fi
done

echo "Stripped metadata from ${#files[@]} image(s)."
