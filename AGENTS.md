# AGENTS.md for CU-ESIIL/data-library

This repository is the ESIIL Data Library. It is not a data host. It is a curated library of reusable, copy-and-paste-ready scripts that help people discover, access, stream, summarize, and visualize public environmental datasets.

The primary goal of this repo is to help users quickly answer the question: "Can I use this dataset for my work, and how do I get started?"

Agents working in this repository should optimize for clarity, reproducibility, low friction, and honest dataset access constraints.

---

## Core rule: do not host data here

This repository should not store raw datasets, large derived datasets, rasters, archives, model outputs, or bulk tabular data.

Allowed in this repo:

- Dataset documentation pages
- Small metadata examples
- Small screenshots or figures used for documentation
- R scripts that access public data
- Python scripts that access public data
- Lightweight example notebooks only when necessary
- Small static example outputs used to illustrate documentation
- Configuration files for the site

Not allowed in this repo:

- Raw environmental datasets
- Large CSV, Parquet, GeoTIFF, NetCDF, HDF5, Zarr, or shapefile collections
- Downloaded copies of source datasets
- Cached API responses beyond tiny examples
- Model outputs or intermediate analysis products
- Credential files, tokens, API keys, `.env` files, or secrets

If a workflow requires large outputs, the documentation should explain where those outputs should go, for example persistent storage, cloud object storage, or a user's local machine. GitHub should remain the place for documentation and scripts, not data storage.

---

## Dataset inclusion rule: no keys, passwords, or secrets

The Data Library should prioritize datasets that work without authentication.

A dataset is a good fit if a user can copy the R or Python function, paste it into a clean session, run it, and retrieve useful data without creating an account, requesting a token, storing a secret, or logging into a service.

Do not add new primary dataset entries if access requires:

- API keys
- Passwords
- Personal accounts
- OAuth flows
- Paid accounts
- Human approval
- Secrets stored in environment variables
- Institutional credentials
- Hidden browser cookies
- Manual download after login

This rule applies even when the dataset is technically "free." Free but key-gated datasets are not currently invited as standard Data Library entries because they break the copy-and-paste onboarding promise.

If a scientifically important dataset requires credentials, do not add it as a normal entry. Instead, place it in a clearly marked future-consideration or excluded-access note if such a page exists. Explain that the dataset is not currently included because it requires authentication.

Preferred access patterns:

- Public HTTPS files
- Public STAC catalogs
- Public Cloud-Optimized GeoTIFFs
- Public Zarr stores
- Public cloud buckets that allow anonymous read access
- Public APIs that do not require keys
- Public package functions that work without secrets

---

## Every dataset should have R and Python access scripts

For every dataset entry, provide both:

- One R script
- One Python script

Each script should define a reusable function that retrieves or streams data and produces a minimum viable plot.

The goal is not to build a full analysis. The goal is to prove that the dataset can be accessed, subsetted, summarized, and visualized with minimal friction.

Each script should be copy-and-paste ready. A user should be able to paste the full code into R or Python and run it with minimal setup.

If a dataset cannot reasonably support both R and Python, document why. Do not silently omit one language.

---

## Function requirements

Each dataset script should expose one clear function.

The function should:

- Accept a simple area of interest when relevant
- Accept a simple date or date range when relevant
- Access or stream the dataset from its public source
- Return a useful object, such as a table, spatial object, raster-like object, xarray object, or summary dictionary
- Create a minimum viable plot
- Avoid writing large files by default
- Avoid hidden dependencies on local paths
- Avoid credentials, secrets, or user-specific configuration
- Include clear comments explaining what the code does

The function should not:

- Require a pre-downloaded file unless the file is tiny and public
- Require a private path on the author's machine
- Require a login or API key
- Store large files in the repo
- Run a long or expensive global download by default
- Hide important assumptions

Preferred function names should be descriptive, for example:

```r
get_prism_temperature <- function(aoi, start_date, end_date) {
  # Access data.
  # Summarize data.
  # Make a minimum viable plot.
  # Return results.
}
```

```python
def get_prism_temperature(aoi, start_date, end_date):
    """Access data, summarize it, make a minimum viable plot, and return results."""
    # Access data.
    # Summarize data.
    # Make a minimum viable plot.
    # Return results.
```

---

## Minimum viable plot rule

Every access function should make a minimum viable plot. This is a core Data Library requirement.

The plot should show that the data retrieval worked and give the user immediate intuition about the dataset.

Examples:

- A map of a raster subset
- A time series for an area of interest
- A histogram of values
- A simple point or polygon map
- A small summary chart by date, region, or class

The plot does not need to be publication quality. It does need to be clear, labeled, and useful.

Plots should avoid custom styling unless necessary. Favor simple, dependable code that works in many environments.

---

## Copy-and-paste readiness

Scripts should be written so users can copy them directly into RStudio, a Jupyter notebook, Google Colab, or a JupyterHub environment.

Requirements:

- Include required library imports at the top
- Include package-install notes only if needed
- Avoid relying on files elsewhere in the repo unless clearly documented
- Avoid hidden state
- Avoid interactive prompts
- Avoid secrets
- Include a small example call at the bottom, preferably commented out if it may take time
- Keep examples small enough to run quickly

Do not write scripts that only work when run from a specific repo root unless that is explicitly documented and necessary.

---

## Streaming-first and subset-first design

Prefer streaming, cloud-native, and subset-first workflows.

Good patterns:

- Read only the area of interest
- Read only selected bands, variables, dates, or columns
- Use STAC metadata to find assets
- Use Cloud-Optimized GeoTIFF reads with bounding boxes
- Use xarray/Zarr lazy loading when appropriate
- Use server-side filters when available

Avoid workflows that download entire national, continental, or global datasets just to make a small example plot.

If a dataset cannot be streamed and requires downloading, make that clear and keep the example small.

---

## Dataset documentation template

Each dataset page should use a consistent structure so users can browse and search the library easily.

Recommended sections:

```markdown
# Dataset Name

## Why this dataset is useful

Short explanation of what the dataset helps users study.

## What it contains

Variables, spatial coverage, temporal coverage, resolution, file types, and update frequency.

## Access pattern

How the data are accessed, for example public STAC, public HTTPS, public API without key, public cloud bucket, or package function.

## Access constraints

State clearly whether the dataset requires no authentication. If any access limitation exists, explain it.

## R example

Link to or embed the R function.

## Python example

Link to or embed the Python function.

## Minimum viable plot

Show or describe what the example plot demonstrates.

## Suggested uses

A few short examples of research, teaching, or synthesis questions this dataset can support.

## Limitations and cautions

Known caveats, missingness, scale issues, uncertainty, licensing, or citation requirements.

## Tags

Structured tags used by the Data Library.

## Citation

How to cite the source dataset and, when relevant, the access package or tool.
```

---

## Tagging system requirements

The Data Library needs a strong tagging system so entries are searchable in a broad, Google-like way, not only by exact word matches.

Every dataset page should include structured tags in front matter if the site supports it, or in a visible `## Tags` section if not.

Tags should include synonyms, related concepts, and likely search terms. Do not only tag the official dataset name.

Recommended tag categories:

Theme tags:

- climate
- weather
- hydrology
- vegetation
- biodiversity
- land cover
- fire
- disturbance
- agriculture
- soils
- water
- drought
- snow
- air quality
- carbon
- ecosystems
- human dimensions

Data type tags:

- raster
- vector
- tabular
- time series
- point observations
- polygons
- remote sensing
- model output
- reanalysis
- in situ
- satellite

Spatial tags:

- global
- continental
- United States
- North America
- Colorado
- watershed
- site-level
- gridded

Temporal tags:

- daily
- monthly
- annual
- historical
- near real time
- long-term record
- forecast

Access tags:

- no key required
- public access
- STAC
- COG
- Zarr
- API no key
- cloud native
- package access
- download required

Workflow tags:

- R example
- Python example
- streaming
- subset by bounding box
- subset by date
- minimum viable plot
- beginner friendly

Synonym and discovery tags:

- precipitation, rain, rainfall
- temperature, heat, air temperature
- NDVI, greenness, vegetation index
- wildfire, fire, burn, burned area
- streamflow, discharge, river flow
- evapotranspiration, ET, water use
- land cover, land use, LULC

The goal is findability. Tags should help users discover relevant datasets even when they do not know the exact dataset name.

---

## Front matter recommendations

When possible, use structured front matter like this:

```yaml
---
title: PRISM Climate Data
description: Public gridded climate data with copy-and-paste R and Python examples for accessing and plotting precipitation and temperature.
tags:
  - climate
  - weather
  - precipitation
  - rain
  - rainfall
  - temperature
  - gridded
  - raster
  - United States
  - daily
  - monthly
  - no key required
  - public access
  - R example
  - Python example
  - minimum viable plot
access: no-key
languages:
  - R
  - Python
data_types:
  - raster
  - time series
spatial_extent: United States
temporal_resolution:
  - daily
  - monthly
---
```

Adapt this to the site's actual metadata system. Do not break MkDocs rendering.

---

## Search and database design

When adding or editing dataset entries, think of each page as both human-readable documentation and a database record.

A good entry should support:

- Keyword search
- Tag filtering
- Browsing by theme
- Browsing by data type
- Browsing by access pattern
- Browsing by language support
- Future automated indexing

Do not bury critical metadata only in prose. Important fields should be represented as tags or structured metadata where possible.

---

## Dataset acceptance checklist

Before adding a dataset, confirm:

- The data source is public.
- The example access path does not require keys, accounts, passwords, tokens, cookies, or secrets.
- The source can be accessed from R and Python.
- The example can be run on a small area or small time range.
- The code retrieves or streams data rather than relying on a local copy.
- The code makes a minimum viable plot.
- The dataset page includes tags and citation information.
- The dataset page explains limitations and cautions.
- No large data files are committed to the repo.

If any of these are not true, either fix the entry or clearly mark the dataset as not currently suitable for the standard Data Library.

---

## Code style for examples

Prioritize boring, readable, dependable code.

R examples should:

- Use common packages where possible
- Include all `library()` calls
- Use explicit function arguments
- Return useful objects
- Avoid excessive tidyverse complexity when base R or simple package calls are clearer
- Avoid hidden local paths

Python examples should:

- Include all imports
- Use common packages where possible
- Include docstrings
- Use explicit function arguments
- Return useful objects
- Avoid hidden local paths
- Avoid complex environment setup

Both R and Python examples should include comments explaining non-obvious steps.

---

## Error handling and user guidance

Examples should fail clearly.

When possible, include simple checks for:

- Missing packages
- Unavailable URLs
- Invalid date ranges
- Empty spatial subsets
- Unsupported variables

Error messages should tell users what to change.

Avoid silent failures and avoid examples that produce empty plots without explanation.

---

## Highlight pages

Highlight pages should be current and event-relevant.

If the site still highlights datasets for the 2025 Innovation Summit, update or replace that page for the 2026 Innovation Summit when requested.

A highlight page should not be a static list. It should guide users toward good starting points.

For each highlighted dataset, include:

- Why it matters for the event theme
- What kinds of questions it can support
- Link to the dataset page
- Link to R and Python examples
- Tags that improve discovery
- Any major limitations

Do not highlight datasets that violate the no-key/no-password rule unless clearly marked as not part of the standard copy-and-paste library.

---

## Visual and aesthetic guidance

Follow the current OASIS visual language when updating the site.

Preferred image style:

- Flat composition
- Square button or tile format when used for navigation
- Screen-print texture
- Strong but slightly muted colors
- Minimal perspective
- No glossy app-icon look
- No circular POV-style buttons unless the site has explicitly retained that older style

Keep user-editable pages in Markdown. Use CSS and templates for visual polish where possible.

Do not add complex HTML into dataset pages.

---

## Prompt log requirement

This repo should maintain a prompt log, for example:

```text
docs/prompt-log.md
```

When making substantial agent-assisted changes, update the prompt log with:

- Date
- Agent or tool used, if known
- Purpose of the change
- Files changed
- Major decisions
- Any unresolved TODOs

The prompt log should help future contributors understand why the library changed, not just what changed.

---

## Testing and validation

When adding or editing dataset scripts, agents should try to validate that examples are syntactically correct and structurally runnable.

At minimum:

- Check that Markdown renders.
- Check that links are not obviously broken.
- Check that R and Python code blocks are complete.
- Check that functions include imports and example calls.
- Check that no secrets or local paths are present.
- Check that no large data files were added.

If the repo has automated tests, run them. If not, suggest lightweight future tests such as:

- Checking required dataset-page sections
- Checking required tags
- Checking that every dataset has R and Python examples
- Checking that no disallowed file types exceed size limits
- Checking for words like `API_KEY`, `TOKEN`, `PASSWORD`, `.env`, or `Sys.getenv()` in dataset examples unless explicitly flagged as disallowed or not currently invited

---

## Language and tone

Write for scientists, students, and synthesis teams who want to use data, not for software engineers alone.

Good tone:

- Direct
- Practical
- Friendly
- Honest about limitations
- Focused on getting users to a first working plot

Avoid:

- Vague dataset praise
- Overpromising ease or completeness
- Unexplained jargon
- Hidden access requirements
- Long theoretical introductions

The best Data Library entry should feel like a helpful colleague saying: "Here is what this dataset is, here is why you might use it, here is the smallest working function to get started, and here is what to watch out for."

---

## Final reminder

This repository does not host data. It hosts well-documented, low-friction pathways to data.

A dataset is not ready for the Data Library until a user can copy the R or Python example, run it without secrets, retrieve a small useful subset, and see a minimum viable plot.
