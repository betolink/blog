---
title: "A reproducible technical blog with Hugo, Quarto, and Pixi"
date: 2026-11-12T09:00:00-06:00
description: "How this site is put together: static HTML from Hugo, computational publishing from Quarto, and reproducible environments from Pixi."
tags: ["hugo", "quarto", "pixi", "reproducibility", "static-sites"]
categories: ["software"]
math: false
draft: false
---

This site is deliberately boring infrastructure: static files generated in CI,
deployed to GitHub Pages, with no application server and no database.

## The pieces

| Layer | Tool | Responsibility |
|---|---|---|
| Site generator | Hugo | Pages, taxonomies, RSS, HTML |
| Theme | rewired | Layouts and retro terminal visual identity |
| Notebooks | Quarto | Execute and convert `.qmd`/`.ipynb` to Markdown |
| Environment | Pixi | Pinned Python and tooling |
| Search | Pagefind | Static, client-side index |
| Comments | Giscus | GitHub Discussions |

## Render pipeline

Quarto writes Hugo-compatible Markdown into `content/notebooks/`, Hugo builds the
site into `public/`, and Pagefind indexes the generated HTML.

```bash
pixi install
pixi run render-notebooks
pixi run build
pixi run serve
```

The CI workflow runs the same commands, so the local build and the published
build use the same inputs.

## Why static?

For a personal publication, the constraints are simple: content should outlive
the tooling, pages should load quickly, and the publishing path should be
auditable. Static output plus a deterministic environment gives all three.

> The best build system is the one you can still run in five years.

## Code blocks

Python examples get syntax highlighting and a copy button:

```python
from pathlib import Path

def list_notebooks(root: str = "notebooks") -> list[Path]:
    return sorted(Path(root).rglob("*.qmd"))

for path in list_notebooks():
    print(path)
```

## What is next

Notebook execution is intentionally separated from site generation. Small
notebooks run in CI; large analyses run on dedicated compute and publish frozen
outputs. Credentials never enter the repository.
