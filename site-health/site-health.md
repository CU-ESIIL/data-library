# Site Health Checks

The Data Library has two lightweight health systems:

- Python structural checks for Data Library rules.
- Playwright browser checks for the built site experience.

Together they answer a practical question: can a human navigate and use this site without hitting obvious problems?

## What Playwright Checks

The Playwright tests in `tests/site.spec.ts` check that:

- The homepage loads.
- The page has a real title and visible body.
- Core navigation links resolve.
- The homepage does not look like a 404 page.
- A small sample of local homepage links does not return obvious HTTP errors.

Navigation and link problems are reported as warnings where possible. The intent is to surface issues without blocking pull requests for every legacy edge case.

## What These Tests Do Not Check

The Playwright tests do not:

- Execute notebooks.
- Run R or Python dataset examples.
- Download datasets.
- Validate every dataset page.
- Check external links exhaustively.
- Replace manual review of scientific accuracy or access constraints.

Use `scripts/check_data_library_health.py` for structural checks related to dataset-page completeness, no-key access expectations, likely secrets, and hosted-data warnings.

## Run Locally

Install documentation dependencies and build the static site:

```bash
pip install -r requirements.txt
mkdocs build --clean --site-dir site
```

Install Playwright:

```bash
npm install
npx playwright install chromium
```

Run the browser health checks:

```bash
npm test
```

For interactive debugging:

```bash
npm run test:ui
```

The Playwright config serves the already-built `site/` directory at `http://localhost:8000`.

## Interpret Results

- A failed homepage load usually means the site did not build or the local server did not start.
- A 404-like homepage failure usually means the built site output is missing the root page.
- Navigation warnings point to links that deserve review but may not block a pull request immediately.
- Link warnings should be triaged before release, especially when they affect top-level guides, dataset discovery, or event highlight pages.

Keep these tests small and dependable. Add focused checks only when they protect a real user path.
