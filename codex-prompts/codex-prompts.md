# Data Library Codex Prompts

Use these prompts to evolve `CU-ESIIL/data-library` while enforcing `AGENTS.md` rules.

---

## 1. Modernize the Data Library

One-time structural upgrade.

Edit the `CU-ESIIL/data-library` repository to align with current OASIS standards while preserving its role as a data access library, not a workflow or working group repo.

### Goals

- Add missing infrastructure: `AGENTS.md` exists; add prompt log and usage guide.
- Update aesthetics to match current OASIS style.
- Replace outdated content: 2025 highlight to 2026.
- Improve usability and discoverability.
- Do not change the core purpose: scripts to access data, not host data.

### Do not

- Do not add AI/sustainability conceptual pages.
- Do not add working group lifecycle pages.
- Do not add specialty tracks.
- Do not host datasets.
- Do not require keys or secrets.

### Tasks

1. Add infrastructure:
   - `docs/prompt-log.md`
   - `docs/how-to-use.md`: what this library is, how to run R/Python, copy-paste promise, where data lives
2. Replace 2025 highlight page with a 2026 Innovation Summit page:
   - Curated starting datasets
   - Each entry: why it matters, link to dataset page, link to R/Python examples, a guiding question
3. Update aesthetic to match OASIS:
   - Square, flat, screen-print style buttons
   - Consistent palette, spacing, typography
   - No HTML in Markdown pages
4. Improve navigation:
   - Start here
   - Browse datasets
   - Try an example
   - How to use the library
   - Minimal changes to `mkdocs.yml`
5. Add a lightweight Cloud Triangle note:
   - GitHub = scripts/docs
   - Data lives externally
   - Compute elsewhere
6. Validate:
   - Build MkDocs
   - Check links
   - Ensure no large files or secrets added

### Output

Summarize files added/updated, highlight page changes, aesthetic changes, and TODOs.

---

## 2. Add a new dataset

Strict dataset addition.

Add a new dataset entry following `AGENTS.md`.

Reject if:

- Requires API key, login, token, or manual download behind auth
- Cannot be accessed via both R and Python
- Cannot produce a minimum viable plot

### Requirements

1. Create page: `docs/datasets/<dataset-name>.md`
2. Include sections:
   - Why useful
   - What it contains
   - Access pattern
   - Access constraints, which must say no key
   - R example
   - Python example
   - Minimum viable plot
   - Suggested uses
   - Limitations
   - Tags
   - Citation
3. R function:
   - Single function
   - Retrieves or streams data
   - Subsets data
   - Plots data
   - Returns an object
   - Uses no keys, no local files, and no large downloads
4. Python function:
   - Same rules as the R function
5. Strong tags:
   - Theme
   - Data type
   - Spatial
   - Temporal
   - Access
   - Workflow
   - Synonyms
6. Copy-paste usability:
   - Imports included
   - Runs in a clean session
   - Small example call

### Checks

- No secrets
- No large files
- Functions complete
- Plot present
- Tags strong

### Output

Summarize the dataset added, scripts added, tags, and limitations.

---

## 3. Audit or fix an existing dataset page

### Check

- Key or login required? Flag or remove.
- Missing R or Python? Add the missing language.
- Not organized as functions? Refactor.
- No plot? Add one.
- Local file dependency? Fix it.
- Too large a download? Subset it.

### Improve

- Access pattern clarity
- Limitations
- Suggested uses
- Readability
- Code robustness

### Tags

Add synonyms and multiple discovery paths.

### Output

Summarize issues found, fixes made, and remaining concerns.

---

## 4. Improve tagging system

Library-wide tagging improvement.

### Goals

- Google-like discoverability
- Multiple paths to find datasets

### Actions

For each dataset, add:

- Theme tags
- Synonym tags
- Data type tags
- Spatial tags
- Temporal tags
- Access tags

### Examples

- Precipitation: precipitation, rain, rainfall
- NDVI: NDVI, vegetation index, greenness

### Output

Summarize the number of datasets updated, tag categories added, and gaps.

---

## 5. Generate example scripts for a dataset

### Requirements

- Copy-paste runnable
- No keys or secrets
- Subset data
- Minimum viable plot
- Return useful object

### Provide

- R function
- Python function
- Brief explanation of the plot

---

## 6. Rewrite 2026 highlight page

### Goals

- Guided entry point, not a list
- Connect datasets to questions

### Structure

For each dataset:

- Why it matters
- Question it helps answer
- Link to dataset page
- Link to R/Python examples

### Tone

- Inviting
- Practical
- Non-generic

### Output

Summarize datasets selected, themes, and gaps.

---

## Notes

- Always follow `AGENTS.md`.
- Never add key-gated datasets as standard entries.
- Prefer streaming and subsetting.
- Keep Markdown clean; no HTML in user-editable pages.
- Update `docs/prompt-log.md` for major changes.
