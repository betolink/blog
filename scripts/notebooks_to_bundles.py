#!/usr/bin/env python3
"""Convert flat Quarto output into Hugo leaf page bundles.

Quarto writes ``name.md`` plus a sibling ``name_files/`` directory. Hugo only
publishes those assets automatically when they live inside a page bundle, so
this script moves each notebook to ``content/notebooks/<name>/index.md``.
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

CONTENT_ROOT = Path("content/notebooks")


def main() -> int:
    if not CONTENT_ROOT.exists():
        print(f"error: {CONTENT_ROOT} does not exist", file=sys.stderr)
        return 1

    notebooks = [
        path
        for path in sorted(CONTENT_ROOT.rglob("*.md"))
        if path.name != "_index.md" and path.name != "index.md"
    ]

    seen: dict[str, Path] = {}

    for source in notebooks:
        slug = source.stem
        if slug in seen:
            print(
                f"error: duplicate notebook slug {slug!r}: {seen[slug]} and {source}",
                file=sys.stderr,
            )
            return 1
        seen[slug] = source

        target = CONTENT_ROOT / slug
        if target.exists():
            shutil.rmtree(target)
        target.mkdir(parents=True)

        assets = source.parent / f"{slug}_files"
        if assets.exists():
            shutil.move(str(assets), str(target / assets.name))

        shutil.move(str(source), str(target / "index.md"))
        print(f"  {source} -> {target / 'index.md'}")

    for directory in sorted(
        (path for path in CONTENT_ROOT.rglob("*") if path.is_dir()),
        key=lambda path: len(path.parts),
        reverse=True,
    ):
        if directory == CONTENT_ROOT:
            continue
        try:
            directory.rmdir()
        except OSError:
            pass

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
