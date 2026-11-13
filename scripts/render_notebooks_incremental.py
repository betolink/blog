#!/usr/bin/env python3
"""Render only notebooks whose sources changed since the last successful render."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = ROOT / "notebooks"
CONTENT = ROOT / "content" / "notebooks"
QUARTO_CONFIG = ROOT / "quarto" / "_quarto.yml"
STATE_FILE = ROOT / ".cache" / "notebook-render-state.json"
RENDER_VERSION = 1


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sources() -> list[Path]:
    found = list(NOTEBOOKS.rglob("*.qmd")) + list(NOTEBOOKS.rglob("*.ipynb"))
    return sorted(path for path in found if path.is_file())


def remove_generated(slug: str) -> None:
    bundle = CONTENT / slug
    if bundle.exists():
        shutil.rmtree(bundle)
    flat = CONTENT / f"{slug}.md"
    if flat.exists():
        flat.unlink()
    assets = CONTENT / f"{slug}_files"
    if assets.exists():
        shutil.rmtree(assets)


def load_state() -> dict:
    if not STATE_FILE.exists():
        return {}
    try:
        return json.loads(STATE_FILE.read_text())
    except json.JSONDecodeError:
        return {}


def save_state(state: dict) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--force", action="store_true", help="render every notebook")
    args = parser.parse_args()

    if not QUARTO_CONFIG.exists():
        print(f"error: {QUARTO_CONFIG} does not exist", file=sys.stderr)
        return 1

    if not shutil.which("quarto"):
        print("error: quarto is required. Install it from https://quarto.org/docs/get-started/", file=sys.stderr)
        return 1

    config_hash = sha256(QUARTO_CONFIG)
    state = load_state()
    previous = state.get("sources", {})
    full_render = (
        args.force
        or state.get("version") != RENDER_VERSION
        or state.get("config_hash") != config_hash
    )

    current: dict[str, dict[str, str]] = {}
    changed: list[Path] = []
    discovered = sources()

    for source in discovered:
        relative = str(source.relative_to(ROOT))
        digest = sha256(source)
        slug = source.stem
        current[relative] = {"hash": digest, "slug": slug}

        bundle = CONTENT / slug / "index.md"
        previous_entry = previous.get(relative, {})
        if (
            full_render
            or previous_entry.get("hash") != digest
            or previous_entry.get("slug") != slug
            or not bundle.exists()
        ):
            changed.append(source)

    deleted = [relative for relative in previous if relative not in current]
    for relative in deleted:
        slug = previous[relative].get("slug") or Path(relative).stem
        remove_generated(slug)
        print(f"  removed {slug} (source deleted)")

    if not changed:
        print(f"Notebooks unchanged ({len(discovered)} source(s)); skipping Quarto.")
        state.update(
            {
                "version": RENDER_VERSION,
                "config_hash": config_hash,
                "sources": current,
            }
        )
        save_state(state)
        return 0

    if full_render:
        print(f"Rendering all {len(changed)} notebook(s).")
    else:
        print(f"Rendering {len(changed)} changed notebook(s).")

    for source in changed:
        slug = source.stem
        remove_generated(slug)
        output_dir = os.path.relpath(CONTENT, source.parent)
        print(f"  {source.relative_to(ROOT)}")
        subprocess.run(
            [
                "quarto",
                "render",
                str(source.relative_to(ROOT)),
                "--to",
                "hugo-md",
                "--output-dir",
                output_dir,
            ],
            cwd=ROOT,
            check=True,
        )

    subprocess.run(
        [sys.executable, "scripts/notebooks_to_bundles.py"],
        cwd=ROOT,
        check=True,
    )

    state.update(
        {
            "version": RENDER_VERSION,
            "config_hash": config_hash,
            "sources": current,
        }
    )
    save_state(state)
    print(f"Rendered {len(changed)} notebook(s); skipped {len(discovered) - len(changed)} unchanged.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
