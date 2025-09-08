# Data Library Entry Style Sheet

This guide describes how to structure a dataset entry in the data library.
It expands on repository conventions and highlights preferred tooling and
presentation patterns.

## 1. Plain‑language overview
* Start every entry with a short, jargon‑free description of the dataset.
* Explain what the data represent, who created them, and why they exist.
* Describe how the data help answer real‑world questions or support
  professional decisions.

## 2. Use cases and citations
* List several ways the dataset has been or could be used.
* Whenever a concrete use case is documented, provide a verifiable link or
  citation to the study, report, or application.
* Keep claims factual; avoid unverifiable anecdotes or marketing language.

## 3. Harmonization guidance
* Note spatial/temporal resolution, coordinate reference system, units, and
  naming conventions so users can align the dataset with others.
* Mention common companion datasets and any known schema or variable
  mappings.
* Include guidance on resampling, reprojection, or transformation steps if
  harmonization requires them.

## 4. Stream‑first data access
* Provide streaming instructions before suggesting local downloads.
* Prefer [STAC](https://stacspec.org) catalogs and GDAL's virtual file
  systems (e.g., `vsicurl`, `vsis3`) for remote access.
* Document required authentication and show how to keep credentials outside
  the code (environment variables or config files).

## 5. Bilingual examples
* Every code example appears in **Python first** followed by an **R**
  translation.
* Use [lexcube](https://github.com/earthdata/lexcube) for interactive Python
  sessions when possible.
* Keep code blocks minimal, runnable, and commented.

## 6. Visual confirmation
* After a data connection is established, provide a quick visual check:
  * **Maps:** render a static PNG map that can display in the documentation.
    * Save the image in the same folder as the Markdown file and reference it with a relative path.
    * Keep images roughly 600–800 px wide so they are clear but lightweight.
    * Provide descriptive alt text and follow the image with an *italicized caption* explaining what is shown.
  * **Tables:** print the first 10 rows using `head()` or equivalent.
* Avoid interactive widgets that fail in static build environments.

## 7. Metadata, licensing, and provenance
* Record source URL, version number, change log, license, and update
  frequency.
* State any usage constraints or attribution requirements linked to the
  license.
* Provide contact or maintainer information.
* Include a data dictionary or variable table when feasible.
* Mention limitations, quality flags, or known issues.

## 8. Reproducibility resources
* Share notebooks, scripts, or workflow files that reproduce key examples.
* For large datasets, reference partial copies or recommended access paths so
  examples run quickly.
* Note software or environment prerequisites when relevant.

## 9. Accessibility and localization
* Use UTF‑8 encoding and document any multilingual fields.
* Favor color‑blind friendly palettes and include alternative text for
  figures.
* Mention any translation resources or localization considerations.

## 10. What to avoid
* Do **not** embed large binaries, proprietary data, or personally
  identifiable information in the repository.
* Avoid hard‑coded credentials, unverifiable claims, or broken links.
* Skip redundant code samples; keep examples concise and relevant.
* Refrain from relying on closed or non‑streamable formats.

## 11. Suggested entry template
````markdown
# Dataset title

## Source
- Provider: ...
- Access: STAC URL or API endpoint
- License: ...

## Why it matters
Plain‑language paragraph...

## Example usage
```python
# Python (lexcube-friendly)
```
```r
# R equivalent
```

## Visualization
![](path/to/preview.png){ width=600 }
*Short caption describing the preview image.*
<!-- or -->
```python
# show first 10 rows for tabular data
```

## Harmonization notes
How to combine with other datasets...

## References
- [Verifiable citation](https://example.com)
````

Following this style ensures entries are accessible, reproducible, and
compatible across the data library.
