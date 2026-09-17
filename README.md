# Dong-Joon Yi - Quarto Website

This repository contains a Quarto-based personal academic website.
The site is rendered to `docs/` and published at https://iverydj.github.io/.
GitHub Pages serves the `main` branch's `/docs` directory.

## Project Structure

- `_quarto.yml`: Site configuration (navigation, format, output directory)
- `styles.css`: Global visual system and responsive layout styles
- `index.qmd`: Home page (hero/contact block generated from `data/cv/profile.yml`; research keywords live here)
- `research.qmd`: Research page
- `career.qmd`: Career page
- `publications.qmd`: Publications page
- `cv.qmd` + `cv.css`: Curriculum Vitae page (paper-sheet layout with print styles; "Save as PDF" uses the browser's print dialog)
- `data/cv/*.yml`: **The single source of CV content** (profile, education, awards, skills, grants, research, publications/patents)
- `scripts/build_cv.py` + `scripts/templates/`: Generates the page fragments in `data/_gen/` from `data/cv/*.yml`
- `data/_gen/`: Generated fragments included by the `.qmd` pages (committed so `quarto render` works without Python; never edit by hand)
- `data/research_total.png`, `data/research_part1.png`, `data/research_part2.png`, `data/research_part3.png`: Research figures not currently displayed
- `docs/`: Generated HTML, search index, styles, and linked resources

## Local Preview

Prerequisite: install Quarto and ensure the `quarto` command is available in your terminal.
The current output was built with Quarto 1.9.37.

```sh
quarto preview
```

- Quarto starts a local preview server.
- Source edits are reflected automatically.

## Static Build

```sh
quarto render
```

- Output is generated in `docs/`.
- Rendering also refreshes `docs/search.json` and copies linked resources.
- Do not edit `docs/` manually; re-render from source files.

## Updating Content

- Edit `data/cv/*.yml`, then run `python3 scripts/build_cv.py` (needs `pyyaml`, `jinja2`) and `quarto render`.
  Career, Research, Publications and CV pages are all generated from these files, so one edit updates every page.
- Publications: add the new paper at the **top** of `papers:` in `data/cv/publications.yml` and save its PDF as
  `assets/pubs/<N>.pdf`, where N is the new total count. Numbering is automatic (`<ol reversed>`); the build script
  aborts if a `pdf:` path does not match the paper's position.
- Scholarships/awards and military service (`awards.yml`, `cv_notes`) appear only on the CV page, by design.
- Update `updated:` in `data/cv/profile.yml` when publishing content changes (it feeds both the Home page and the CV page).
- Every fact appears in exactly one source file. Do not copy CV data into `.qmd` files; `data/_gen/` and `docs/` are build outputs, not sources.
- The former LaTeX CV (`assets/cv_src`, removed 2026-09-07) is recoverable from git history if its design is ever needed again.

## Publish to GitHub Pages (Manual Flow)

1. Run `quarto render` locally so the latest files are in `docs/`.
2. Preview the pages and verify navigation, search, and PDF downloads.
3. Review and commit the source files and generated `docs/` output, including new generated assets.
4. Push the reviewed commit when publication is authorized.
5. Confirm that the `pages build and deployment` workflow succeeds, then check https://iverydj.github.io/.

For initial setup, choose **Deploy from a branch** in **Settings > Pages**, with branch `main` and folder `/docs`.

## Troubleshooting (Images Not Showing)

- Confirm each image path is correct and relative to the source file, for example `data/research_part1.png`.
- Confirm filename case exactly matches the file on disk.
- Re-run `quarto render` after content updates.
- Check that the rendered `docs/` output is committed and pushed before opening the live site.
