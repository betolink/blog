#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/.."

MAX_BYTES=$((900 * 1024))
MAX_DIM=1600
START_QUALITY=95
MIN_QUALITY=60

if ! command -v magick >/dev/null 2>&1; then
  echo "error: ImageMagick (magick) is required. Run this through Pixi." >&2
  exit 1
fi

if ! command -v exiftool >/dev/null 2>&1; then
  echo "error: exiftool is required. Run this through Pixi." >&2
  exit 1
fi

files=()
while IFS= read -r -d '' file; do
  files+=("${file}")
done < <(find content assets -type f \
  \( -iname '*.jpg' -o -iname '*.jpeg' \) -print0)

if [ "${#files[@]}" -eq 0 ]; then
  echo "No JPEG images found under content or assets."
  exit 0
fi

for file in "${files[@]}"; do
  read -r width height <<< "$(magick identify -format '%w %h' "${file}")"
  size=$(wc -c < "${file}" | tr -d ' ')
  metadata=$(exiftool -q -s -EXIF:all -XMP:all -IPTC:all -ICC_Profile "${file}" || true)

  if [ "${width}" -le "${MAX_DIM}" ] && [ "${height}" -le "${MAX_DIM}" ] \
    && [ "${size}" -le "${MAX_BYTES}" ] && [ -z "${metadata}" ]; then
    echo "  skip ${file} (${width}x${height}, $((size / 1024)) KiB)"
    continue
  fi

  tmp="${file%.*}.ingest.jpg"
  quality="${START_QUALITY}"

  while :; do
    magick "${file}" \
      -auto-orient \
      -resize "${MAX_DIM}x${MAX_DIM}>" \
      -colorspace sRGB \
      -strip \
      -quality "${quality}" \
      -sampling-factor 4:2:0 \
      "${tmp}"

    size=$(wc -c < "${tmp}" | tr -d ' ')

    if [ "${size}" -le "${MAX_BYTES}" ] || [ "${quality}" -le "${MIN_QUALITY}" ]; then
      break
    fi

    quality=$((quality - 5))
  done

  if [ "${size}" -gt "${MAX_BYTES}" ]; then
    echo "error: ${file} is still $((size / 1024)) KiB at quality ${quality}" >&2
    rm -f "${tmp}"
    exit 1
  fi

  read -r new_width new_height <<< "$(magick identify -format '%w %h' "${tmp}")"
  mv "${tmp}" "${file}"
  echo "  ingested ${file} (${width}x${height} -> ${new_width}x${new_height}, q${quality}, $((size / 1024)) KiB)"
done

oversized=()
while IFS= read -r -d '' file; do
  oversized+=("${file}")
done < <(find content static assets -type f \
  \( -iname '*.jpg' -o -iname '*.jpeg' -o -iname '*.png' -o -iname '*.webp' \) \
  -size +900k -print0)

if [ "${#oversized[@]}" -gt 0 ]; then
  echo "error: these images are larger than 900 KiB after ingest:" >&2
  for file in "${oversized[@]}"; do
    echo "  ${file} ($(( $(wc -c < "${file}") / 1024 )) KiB)" >&2
  done
  exit 1
fi

echo "All site images are at most 900 KiB."
