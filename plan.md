
# Technical Blog Implementation Specification

## 1. Project objective

Build a personal technical blog for software engineering, scientific computing, Earth observation, open-source development, and computational experiments.

The website should support:

- Traditional technical articles.
- Code snippets with syntax highlighting.
- Jupyter notebooks with rendered outputs.
- Scientific plots, equations, and tables.
- Project documentation and experiment collections.
- GitHub-authenticated comments.
- Search.
- A retro-computing visual identity.

The website must be statically generated and published through GitHub Pages using GitHub Actions.

No application server, database, or custom backend is required.

## 2. Technology stack

| Layer | Technology | Responsibility |
|---|---|---|
| Static site generator | Hugo | Website generation |
| Hugo theme | betolink/rewired | Base layouts and visual design |
| Computational publishing | Quarto | Notebook execution and conversion |
| Notebook format | Jupyter/IPYNB | Computational content |
| Primary editor | LazyVim | Daily development and editing |
| Alternative IDE | Positron | Quarto and notebook authoring |
| Python environment | Pixi | Reproducible dependencies |
| Source control | GitHub | Source repository |
| CI/CD | GitHub Actions | Build and deployment |
| Hosting | GitHub Pages | Static hosting |
| Comments | Giscus | GitHub Discussions integration |
| Search | Pagefind | Client-side search |
| Styling | SCSS/CSS | Retro customization |

## 3. Hugo theme

Use the following repository as the actual theme baseline:

https://github.com/betolink/rewired

Do not replace it with another theme.

Clone or add it as a Git submodule, following the repository's recommended installation procedure.

First inspect:
- Theme configuration.
- Existing layouts and partials.
- Header and navigation implementation.
- Existing logo handling.
- Existing CSS/SCSS.
- Responsive behavior.
- Content and taxonomy structure.

Preserve the existing theme's functionality and extend it rather than rebuilding it unnecessarily.

The theme is the starting point for the website's visual identity.

## 4. Logo preparation

There is an existing logo in the repository:

`~/logo.jpg`

Use this file as the source asset.

Requirements:

1. Inspect the original image.
2. Identify the actual logo and its background.
3. Extract the logo and remove the background.
4. Preserve the original proportions and recognizable appearance.
5. Convert it to a transparent PNG.
6. Optimize the resulting PNG for web use.
7. Store the final image in the theme's appropriate static asset directory.
8. Configure it to appear in the upper-right area of the header.

Suggested destination:

`static/images/logo.png`

Do not overwrite or delete the original JPG.

Do not redraw or replace the logo with a different design.

For background removal, use an appropriate image-processing method. If the background is not uniformly colored, inspect the result carefully for artifacts around the logo edges.

Check the logo against both dark and light backgrounds.

The logo should:
- Preserve transparency.
- Scale proportionally.
- Remain legible at small sizes.
- Never stretch.
- Have appropriate spacing from navigation elements.

## 5. Authoring workflow and editors

### Primary editor: LazyVim

LazyVim is the primary development environment.

Support:
- Markdown editing.
- YAML front matter.
- Hugo templates and configuration.
- HTML/CSS/SCSS.
- Python.
- Quarto `.qmd` files.
- Git operations.
- Terminal-based Hugo and Quarto commands.

Provide useful optional LSP and syntax support for these formats.

Do not require Positron or VS Code to maintain the website.

### Optional IDE: Positron

Positron is the dedicated alternative for computational authoring.

Use it when working with:
- `.qmd` files.
- `.ipynb` files.
- Python and R execution.
- Interactive plots.
- Quarto document previews.

Official website: https://positron.posit.co/

Quarto documentation: https://quarto.org/docs/tools/positron/

Positron is optional, not a build dependency.

## 6. Content organization

Use Hugo as the final website generator.

Suggested structure:

```text
blog/
├── .github/
│   └── workflows/
│       └── publish.yml
├── config/
│   └── _default/
│       └── hugo.toml
├── content/
│   ├── _index.md
│   ├── about/
│   │   └── index.md
│   ├── posts/
│   ├── notebooks/
│   └── projects/
├── notebooks/
│   ├── earthdata/
│   └── xarray/
├── quarto/
│   └── _quarto.yml
├── layouts/
├── assets/
│   └── scss/
├── static/
│   ├── images/
│   │   └── logo.png
│   └── fonts/
├── scripts/
│   └── render-notebooks.sh
├── themes/
│   └── rewired/
├── pixi.toml
├── .gitignore
└── README.md
```

Adjust the layout based on the actual theme conventions.

Separate original notebook files from generated Markdown and generated assets.

Do not commit generated build output unless required by the selected deployment workflow.

## 7. Quarto and Jupyter integration

Use Quarto to process computational content.

Support:
- `.qmd` documents.
- `.ipynb` notebooks.
- Python execution.
- Markdown cells.
- Code cell outputs.
- Scientific plots.
- Tables.
- Mathematical equations.
- HTML outputs.

Use Quarto's `hugo-md` output format to convert computational content into Hugo-compatible Markdown.

The resulting content must have:
- Valid Hugo front matter.
- Stable URL paths.
- Correct image references.
- Correct code block rendering.
- Correct notebook output formatting.

Notebook outputs must be available as static content without a running Jupyter server.

### Execution policy

| Content | Execution |
|---|---|
| Small Python examples | Local or CI |
| Small notebooks | GitHub Actions |
| Large scientific analyses | Dedicated compute |
| NASA Earthdata requiring credentials | Dedicated secure workflow |
| Historical experiments | Frozen outputs |

Use Quarto freeze/cache features where appropriate.

Never commit credentials or tokens into the repository.

Keep original `.ipynb` files downloadable from the published website.

## 8. Visual identity

Preserve the existing Rewired theme's terminal-inspired appearance and customize it toward a retro-computing aesthetic.

Inspiration:
- Commodore 64.
- 1980s home computers.
- CRT displays.
- Old Unix terminals.
- Retro scientific workstations.
- Vintage technical manuals.

Implement three selectable color schemes:

### Commodore (default)

- Deep blue.
- Cyan.
- Lavender.
- Pixel-inspired decorative elements.

### CRT

- Near-black background.
- Phosphor green.
- Amber accents.
- Optional subtle scanlines.

### Sepia

- Warm paper background.
- Dark brown typography.
- Vintage technical-journal appearance.

Theme switching must work client-side and persist using localStorage.

Typography:
- IBM Plex Mono or Fira Code for body/code.
- JetBrains Mono as an alternative.
- VT323 or Press Start 2P for decorative headings only.

Keep scientific plots, notebook outputs, equations, and tables readable.

Do not introduce excessive visual effects or unnecessary JavaScript.

Respect accessibility and reduced-motion preferences.

## 9. Comments

Integrate Giscus.

Official website: https://giscus.app/

Use GitHub Discussions for comments.

Requirements:
- Separate public repository for comments if practical.
- One discussion per article.
- Associate articles by pathname.
- Enable reactions and threaded replies.
- Support dynamic website theme changes.
- Only display comments on individual articles.

Do not invent GitHub repository IDs or category IDs.

Use the official Giscus configuration generator.

## 10. Search

Use Pagefind.

Requirements:
- Search articles.
- Search notebook descriptions and rendered content.
- Client-side search.
- No external search backend.
- Style the interface to match Rewired.

## 11. GitHub Actions CI/CD

GitHub Actions is the only publishing mechanism.

On pushes to `main`:

1. Check out the repository and theme.
2. Install pinned Hugo Extended.
3. Install pinned Quarto.
4. Set up Pixi/Python.
5. Execute or render computational content according to the execution policy.
6. Convert Quarto content to Hugo-compatible Markdown.
7. Run Hugo.
8. Generate the Pagefind index.
9. Upload the generated site as a GitHub Pages artifact.
10. Deploy through the GitHub Pages deployment action.

Also support manual deployment using `workflow_dispatch`.

Use:
- `contents: read`
- `pages: write`
- `id-token: write`

Use reviewed commit SHAs for third-party GitHub Actions.

Configure GitHub Pages through repository Settings → Pages → GitHub Actions.

Ensure correct base URL handling for:

`https://USERNAME.github.io/REPOSITORY/`

Support custom domains as an optional configuration.

## 12. Local development

Provide simple commands for local development.

Expected workflow:

```bash
# Set up the environment
pixi install

# Process computational content
quarto render

# Build the website
hugo --minify

# Start the local server
hugo server -D
```

Adapt the actual commands to the implemented Quarto/Hugo integration.

Document the complete workflow in README.md.

## 13. Implementation phases

### Phase 1: Theme and branding

- Inspect betolink/rewired.
- Install the theme.
- Inspect and convert `~/logo.jpg` into transparent PNG.
- Integrate logo in the upper-right header.
- Customize the Commodore default palette.
- Add CRT and Sepia themes.
- Verify responsive behavior.

### Phase 2: Content and publishing

- Create blog and project sections.
- Configure article layouts.
- Configure syntax highlighting.
- Add code copy buttons.
- Configure RSS.
- Set up GitHub Actions.
- Deploy to GitHub Pages.

### Phase 3: Computational publishing

- Integrate Quarto.
- Configure Jupyter support.
- Add Python environment through Pixi.
- Test notebook execution and static rendering.
- Test scientific plots and equations.
- Add notebook download links.

### Phase 4: Community and search

- Integrate Giscus.
- Implement dynamic Giscus theme synchronization.
- Add Pagefind.
- Style search to match Rewired.

### Phase 5: Polish

- Accessibility.
- SEO.
- Performance.
- Link checking.
- Documentation.
- Security and dependency updates.

## 14. Acceptance criteria

The project is complete when:

1. The website uses `betolink/rewired` as its Hugo theme baseline.
2. The original logo is preserved.
3. A transparent PNG logo appears in the upper-right header.
4. LazyVim is sufficient for the normal development workflow.
5. Positron can be used optionally for Quarto and Jupyter.
6. Markdown articles render correctly.
7. Python code blocks have syntax highlighting and copy buttons.
8. Jupyter notebooks render with outputs.
9. Scientific plots and equations render correctly.
10. Three visual themes work and persist.
11. Giscus comments work on individual articles.
12. Pagefind searches articles and notebooks.
13. GitHub Actions deploys automatically to GitHub Pages.
14. No custom server or database is required.
15. The local development workflow is documented.

## Overall design principle

Keep the infrastructure simple and the publishing workflow reproducible.

Hugo owns the website. Quarto owns computational publishing. Jupyter owns notebook authoring. GitHub Actions owns deployment.

The result should look like a retro computing environment while behaving like a modern scientific and engineering publication.
