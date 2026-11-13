# betolink

Personal technical blog for software engineering, scientific computing, Earth
observation, open-source development, and computational experiments.

The site is a static Hugo build with computational notebooks rendered by Quarto.
It is published to GitHub Pages by GitHub Actions. There is no application
server and no database.

## Stack

- **Hugo Extended** — static site generation.
- **rewired** — Hugo theme, included as a Git submodule at `themes/rewired`.
- **Quarto** — executes `.qmd`/`.ipynb` notebooks and writes Hugo Markdown.
- **Pixi** — reproducible Python environment for notebook execution.
- **Pagefind** — client-side search index generated after the Hugo build.
- **Giscus** — comments backed by GitHub Discussions.
- **GitHub Actions** — the only publishing mechanism.

## Requirements

- [Hugo Extended](https://gohugo.io/installation/) 0.160 or newer.
- [Quarto](https://quarto.org/docs/get-started/) 1.5 or newer.
- [Pixi](https://pixi.sh/).
- Node.js 20 or newer (for Pagefind via `npx`).
- Git with submodule support.

Positron and VS Code are optional. LazyVim with Markdown, YAML, TOML, HTML,
SCSS, Python, and Quarto syntax support is sufficient for normal maintenance.

## Local development

```bash
git clone --recurse-submodules https://github.com/betolink/blog.git
cd blog

# Install the Python environment
pixi install

# Render notebooks, build Hugo, and generate the Pagefind index
pixi run build

# Or work interactively
pixi run render-notebooks          # incremental
pixi run render-notebooks-full     # force every notebook
pixi run serve
```

Notebook rendering is content-hash based. The state lives in
`.cache/notebook-render-state.json`; generated pages live in
`content/notebooks/`. Both are ignored by git. CI restores the same cache with
`actions/cache`, so an unchanged notebook is not executed again on a travel-post
or article-only change.

`pixi run build` is equivalent to:

```bash
bash scripts/render-notebooks.sh
hugo --minify --gc --cleanDestinationDir
npx --yes pagefind@1.6.0 --site public
python3 scripts/check_links.py public
```

The generated site is written to `public/`.

`scripts/serve.sh` runs the incremental notebook renderer, then starts
`hugo server -D`. Hugo uses its fast render mode, so editing a Markdown page only
rebuilds that page. Notebook sources are checked by content hash: unchanged
notebooks are not re-executed. If you edit a notebook while the server is
running, run `pixi run render-notebooks` in another terminal; Hugo will reload
the changed page. Because the deployment is a project site, the local server is
at <http://localhost:1313/blog/>.

If Quarto is not installed on your `PATH`, install it or use the Pixi task from
an environment where it is available. Quarto is installed separately in CI so
the site build does not depend on a particular local editor.

## Content

```text
content/
├── _index.md            # home page data
├── about/index.md       # /about/
├── posts/               # traditional articles
├── notebooks/           # generated notebook pages (ignored by git)
├── projects/            # project cards
└── search/_index.md     # Pagefind search page
```

### Write an article

Create `content/posts/my-article.md`:

```yaml
---
title: "My article"
date: 2026-11-12T09:00:00-06:00
description: "One sentence for listings, search, and social metadata."
tags: ["python", "earth-observation"]
categories: ["science"]
math: true
draft: false
---
```

Set `math: true` to load KaTeX. Use `$$ ... $$` or `\[ ... \]` for display math
and `\( ... \)` for inline math.

### Add a notebook

Notebook sources live outside the Hugo content directory:

```text
notebooks/
├── earthdata/my-analysis.qmd
└── xarray/my-other-analysis.ipynb
```

Add front matter to the source so the generated page has useful metadata:

```yaml
---
title: "My analysis"
description: "What this notebook demonstrates."
date: 2026-11-12
author: "Luis López"
categories: ["earth-observation"]
tags: ["xarray", "python"]
notebook_source: "notebooks-src/earthdata/my-analysis.qmd"
format: hugo-md
jupyter: python3
---
```

Then run:

```bash
pixi run render-notebooks
```

The script:

1. Cleans generated pages under `content/notebooks/` (keeping `_index.md`).
2. Renders `notebooks/**/*.qmd` and `notebooks/**/*.ipynb` with Quarto.
3. Converts each flat Markdown result into a Hugo page bundle at
   `content/notebooks/<slug>/index.md`, so plots and generated assets are
   published correctly.
4. Copies the original sources to `static/notebooks-src/` for download links.

Generated notebook pages and downloadable sources are intentionally ignored by
git. The source notebooks are the source of truth.

### Execution policy

| Content | Execution location |
|---|---|
| Small Python examples | Local or CI |
| Small notebooks | GitHub Actions |
| Large scientific analyses | Dedicated compute |
| NASA Earthdata requiring credentials | Dedicated secure workflow |
| Historical experiments | Frozen outputs |

Quarto is configured with `freeze: auto` and `cache: true` in
`quarto/_quarto.yml`. Commit `quarto/_freeze` if a notebook is intentionally
frozen; never commit credentials or tokens.

## Images, travel posts, and galleries

Images are ingested before every build. Ingest resizes photos to at most
1600 px on the long edge, converts them to sRGB JPEG at quality 95, and enforces
a 900 KiB ceiling (lowering quality slightly only when necessary). It also
strips EXIF, GPS, camera details, and other identifying tags:

```bash
pixi run ingest-images
pixi run strip-image-metadata
```

`scripts/build.sh` runs both tasks in CI before Hugo, so a published build cannot
include oversized or geolocated images. Run `pixi run ingest-images` locally
before committing new photos. Source images are committed in their web-ready
form; keep private backups elsewhere if you need the originals.

Travel posts live in their own section:

```text
content/travel/
├── _index.md
└── joshua-tree/
    ├── index.md
    └── images/
```

Add a gallery to a post with front matter and the shortcode:

```yaml
gallery:
  - src: "images/photo.jpg"
    alt: "Description for screen readers"
    caption: "Visible caption"
```

```markdown
{{< gallery >}}
```

Hugo generates resized thumbnails and a larger lightbox image from each page
resource. The gallery is a responsive grid with keyboard-accessible navigation.

## Self-hosted assets

Fonts, icons, and math rendering are served from the repository, not a CDN:

- Fira Code and VT323 are under `static/vendor/fonts/`.
- Font Awesome Free is under `static/vendor/fontawesome/`.
- KaTeX is under `static/vendor/katex/`.

License files are in `static/vendor/licenses/`. The site renders without network
access for typography, icons, and equations. Two features are inherently
external: the X timeline embed and Giscus comments.

## Visual themes

Three client-side themes are available and persist in `localStorage`:

- **Sepia** (default) — warm paper, dark brown type, vintage technical-journal look.
- **Commodore** — deep blue, cyan, lavender, pixel grid.
- **CRT** — near-black phosphor green with amber accents and scanlines.

The switcher is in the site header. The selected theme is applied before paint
by an inline script in `layouts/_partials/head.html`, and is synchronized with
Giscus. Reduced-motion preferences disable cursor blinking and transitions.

Palette definitions and component overrides live in `assets/css/retro.css`. The
upstream theme is not modified.

## Logo

The original `logo.jpg` is preserved at the repository root. The transparent,
cropped web asset is `static/images/logo.png`. It appears in the upper-right of
the header through `layouts/_partials/nav.html`.

To regenerate the PNG after changing the source image, use an image editor or
ImageMagick/Pillow to remove the white background, crop with a small transparent
margin, resize proportionally (512 px tall is sufficient), and save with
transparency.

## GeoJupyter Story Maps

The default Pixi environment includes the JupyterGIS stack for future
GeoJupyter Story Map posts:

- `jupytergis` for Story Maps and collaborative GIS documents
- `jupyter-tiler` for lazy visualization of xarray datasets
- `openeo` and `stackstac` for remote-sensing workflows
- `jupyterlab` for authoring in the Jupyter editor

Start it with:

```bash
pixi run lab
```

Story Maps and `.jGIS` documents are authored in JupyterLab. Add the resulting
notebook or exported assets to the site as usual.

## Search

Pagefind indexes the generated HTML after `hugo` completes. The search page is
`/search/` and is powered by the Pagefind UI. The build fails loudly if Pagefind
cannot run; when viewing a raw Hugo build without the Pagefind step, the search
page displays a message instead of results.

Run `pixi run build` (or the `npx pagefind` command above) before testing search
locally.

## Comments

Comments use [Giscus](https://giscus.app/) and GitHub Discussions. Configure a
public repository with Discussions enabled, install the Giscus app, then use the
official generator at <https://giscus.app/> to obtain the repository ID and
category ID.

Set the values in `config/_default/hugo.toml`:

```toml
[params]
  giscusRepo = "betolink/blog"
  giscusRepoId = "R_kgDOHRd2xg"
  giscusCategory = "General"
  giscusCategoryId = "DIC_kwDOHRd2xs4CSiKb"
  giscusMapping = "pathname"
```

The checked-in IDs come from this repository's Discussions settings and the
`General` category. Install the [Giscus GitHub App](https://github.com/apps/giscus)
on the repository before expecting visitors to be able to comment. The
comments partial only renders when all four values are non-empty. It is included
on individual article and notebook pages, never on section pages. Do not guess or
invent repository/category IDs; use <https://giscus.app/> if you change the
repository or category.

For a separate comments repository, point `giscusRepo`/`giscusRepoId` at that
repository instead.

## Deployment

`.github/workflows/publish.yml` runs on pushes to `main` and on manual
`workflow_dispatch`. It:

1. Checks out the repository and the `rewired` submodule.
2. Installs pinned Hugo Extended, Node.js, the pinned Pixi environment, and
   pinned Quarto 1.5.55.
3. Configures GitHub Pages and renders notebooks with Quarto.
4. Builds with Hugo, generates the Pagefind index, and uploads `public/`.
5. Deploys through the GitHub Pages deployment action.

In the repository settings, choose **Pages → Build and deployment → GitHub
Actions** once.

The base URL is taken from the `configure-pages` output. With the current
configuration the site is published at:

```text
https://betolink.github.io/blog/
```

No CNAME is committed, so GitHub Pages uses the project-site URL. If a custom
domain is configured later, set it in repository settings and add a
`static/CNAME` file containing the domain. The workflow will then use the custom
domain as the base URL automatically.

Third-party actions are pinned to reviewed commit SHAs.

## Scripts

| Script | Purpose |
|---|---|
| `scripts/render-notebooks.sh` | Incrementally render, bundle, and publish notebook sources |
| `scripts/render_notebooks_incremental.py` | Hash-based notebook render cache and change detection |
| `scripts/notebooks_to_bundles.py` | Convert Quarto Markdown into Hugo page bundles |
| `scripts/build.sh` | Full local/CI build including Pagefind |
| `scripts/serve.sh` | Render if needed, then run `hugo server -D` |
| `scripts/ingest-images.sh` | Resize, optimize, and enforce the 900 KiB image limit |
| `scripts/strip-image-metadata.sh` | Remove EXIF/GPS and other metadata from site images |
| `scripts/check_links.py` | Verify local links in the generated site |
| `scripts/clean.sh` | Remove generated output and caches |

## License

Site content is © Luis López. The `rewired` theme is MIT licensed in
`themes/rewired/LICENSE`.
