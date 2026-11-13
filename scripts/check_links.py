#!/usr/bin/env python3
"""Check that local links in the generated site resolve to real files."""

from __future__ import annotations

import argparse
import sys
import tomllib
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse

CONFIG = Path("config/_default/hugo.toml")


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        for attribute in ("href", "src"):
            value = values.get(attribute)
            if value:
                self.links.append(value)


def base_path_from_config() -> str:
    if not CONFIG.exists():
        return "/"
    data = tomllib.loads(CONFIG.read_text())
    return urlparse(data.get("baseURL", "/")).path or "/"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("site", nargs="?", default="public", help="built site directory")
    parser.add_argument("--base-path", help="path prefix the site is published under")
    args = parser.parse_args()

    site = Path(args.site)
    if not site.is_dir():
        print(f"error: {site} does not exist; run the build first", file=sys.stderr)
        return 1

    base_path = args.base_path or base_path_from_config()
    if not base_path.endswith("/"):
        base_path += "/"

    errors: list[tuple[str, str, str]] = []

    for html in sorted(site.rglob("*.html")):
        link_parser = LinkParser()
        link_parser.feed(html.read_text(errors="ignore"))

        for link in link_parser.links:
            if not link or link.startswith(("#", "mailto:", "tel:", "javascript:", "data:")):
                continue

            parsed = urlparse(link)
            if parsed.scheme or parsed.netloc:
                continue

            path = unquote(parsed.path)
            if path.startswith("/"):
                if not path.startswith(base_path):
                    errors.append((str(html), link, "outside configured base path"))
                    continue
                relative = path[len(base_path) :]
            else:
                relative = str((html.parent / path).relative_to(site))

            target = site / relative
            if relative == "" or relative.endswith("/"):
                target = target / "index.html"

            if not target.exists():
                errors.append((str(html), link, f"missing {target}"))

    if errors:
        print(f"{len(errors)} broken local link(s):", file=sys.stderr)
        for source, link, reason in errors:
            print(f"  {source}: {link} ({reason})", file=sys.stderr)
        return 1

    print(f"Checked local links in {len(list(site.rglob('*.html')))} HTML files: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
