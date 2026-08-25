# Prompt Log

This log records substantial agent-assisted changes to the ESIIL Data Library so future contributors can understand why changes were made.

## 2026-08-25

### ECOSTRESS discoverability fix

- Agent/tool used: Codex
- Purpose: Make the new ECOSTRESS dataset entry discoverable in MkDocs search and topic/tag browsing.
- Files changed:
  - `docs/remote_sensing/ECOSTRESS/ecostress.md`
  - `docs/remote_sensinge/ECOSTRESS/ecostress.md`
  - `docs/topic/remote_sensing.md`
  - `docs/tags.md`
  - `docs/prompt-log.md`
- Major decisions:
  - Moved the page from the misspelled `remote_sensinge` directory into the existing `remote_sensing` collection.
  - Added front matter, a clear H1 title, standard Data Library sections, fenced R/Python examples, and stronger discovery tags.
  - Linked the entry from the remote sensing topic page and static tag index.
- Unresolved TODOs:
  - Verify the deployed GitHub Pages search index after the change is committed, pushed, and Pages finishes rebuilding.

## 2026-04-29

### Playwright site health

- Agent/tool used: Codex
- Purpose: Add a lightweight Playwright browser health system using the generic OASIS pattern.
- Files changed:
  - `package.json`
  - `playwright.config.ts`
  - `tests/site.spec.ts`
  - `.github/workflows/site-health.yml`
  - `docs/site-health.md`
  - `README.md`
  - `mkdocs.yml`
  - `.gitignore`
  - `docs/prompt-log.md`
- Major decisions:
  - Added Playwright without removing the existing Python/static Data Library health checks.
  - Configured Playwright to serve the already-built `site/` directory so tests do not execute notebooks or data pipelines.
  - Kept navigation and homepage link concerns as warnings where possible to avoid brittle PR failures.
- Unresolved TODOs:
  - Decide over time which warnings should become blocking failures after legacy link issues are triaged.

### ESIIL style and health system

- Agent/tool used: Codex
- Purpose: Add a practical ESIIL/OASIS style guide and lightweight Data Library health-check system.
- Files changed:
  - `docs/style-guide.md`
  - `docs/stylesheets/extra.css`
  - `mkdocs.yml`
  - `scripts/check_data_library_health.py`
  - `scripts/check_site_smoke.py`
  - `.github/workflows/data-library-health.yml`
  - `docs/prompt-log.md`
- Major decisions:
  - Added shared ESIIL color variables to the existing custom CSS instead of creating a parallel stylesheet.
  - Linked the style guide under a new Guides navigation group.
  - Updated the stale Innovation Summit navigation target from 2025 to the existing 2026 page.
  - Added health checks that report legacy dataset-page and hosted-data issues without downloading data or executing examples.
  - Added a dependency-free built-site smoke check to catch missing key pages, broken local links, missing images, and absent style variables after MkDocs builds.
- Unresolved TODOs:
  - Decide when to make health warnings strict after legacy hosted-data and dataset-page completeness issues are triaged.

### Codex prompt reference

- Agent/tool used: Codex
- Purpose: Add reusable Codex prompts for future Data Library modernization, dataset additions, audits, tagging work, example generation, and highlight-page rewrites.
- Files changed:
  - `docs/codex-prompts.md`
  - `docs/prompt-log.md`
- Major decisions:
  - Stored the prompts as a maintainer reference page rather than changing user-facing navigation.
  - Normalized formatting to clean Markdown without embedded HTML.
- Unresolved TODOs:
  - None.

### Repository agent guidance

- Agent/tool used: Codex
- Purpose: Add repository-level agent guidance for maintaining the ESIIL Data Library.
- Files changed:
  - `AGENTS.md`
  - `docs/prompt-log.md`
- Major decisions:
  - Established the repo as a curated script and documentation library, not a data host.
  - Documented the no-key/no-password dataset inclusion rule.
  - Required R and Python access examples with minimum viable plots for dataset entries.
  - Added expectations for tags, front matter, validation, tone, highlight pages, and future prompt-log updates.
- Unresolved TODOs:
  - None.
