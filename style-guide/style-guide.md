# ESIIL/OASIS Style Guide for the Data Library

This guide keeps the ESIIL Data Library visually consistent with the current OASIS family of sites while protecting the library's core purpose: helping people find public environmental datasets and run small, copy-and-paste-ready access examples.

Use this page when updating the homepage, dataset entries, navigation tiles, screenshots, figures, and supporting documentation.

## Design principles

- Make the first path to data obvious.
- Keep pages practical, scannable, and honest about access constraints.
- Use visual polish to improve orientation, not to hide missing metadata.
- Keep user-editable content in Markdown whenever possible.
- Do not imply that this repository hosts datasets directly.

## ESIIL color system

Use these shared variables for Data Library styling.

```css
--esiil-primary-blue: #234A65;
--esiil-accent-blue: #42BCDC;
--esiil-accent-green: #007135;
--esiil-light-green: #007135;
--esiil-body-text: #161A19;
--esiil-gray-relief: #E3E3E3;
```

Recommended uses:

| Variable | Use |
| --- | --- |
| `--esiil-primary-blue` | Header, navigation emphasis, strong headings, footer accents |
| `--esiil-accent-blue` | Links, buttons, active states, navigation tiles |
| `--esiil-accent-green` | Secondary accents, success states, dataset access signals |
| `--esiil-light-green` | Green accent mapping retained for OASIS compatibility |
| `--esiil-body-text` | Main body text |
| `--esiil-gray-relief` | Borders, dividers, quiet backgrounds, card relief |

Avoid building a one-note page from only blue or only green. Use the palette with white space, readable text, and small accents.

## Typography

The Data Library should feel confident and readable, but it still lives inside MkDocs Material. Do not force oversized type where the layout cannot support it cleanly.

Intended hierarchy:

| Element | Target use |
| --- | --- |
| H1 | Large page banners, roughly `3.5rem` where layout allows |
| H2 | Strong section titles, roughly `2.5rem` where layout allows |
| H3 | Section subtitles, roughly `1.5rem` |
| H4 | Card titles, roughly `1.5rem` |
| Body | Readable `1rem` baseline |

Guidance:

- Use one clear H1 per page.
- Keep dataset-page headings descriptive and predictable.
- Do not use hero-scale headings inside compact cards, callouts, tables, or sidebars.
- Favor short headings that help users scan for access, examples, limitations, and citation.

## Buttons and navigation tiles

Visual navigation elements should be:

- Square or rectangular, not circular.
- Flat, not perspective or 3D.
- Screen-print inspired.
- Bold but not glossy.
- Aligned with the ESIIL blue and green palette.
- Readable at small sizes.
- Visually consistent across the site.

Preferred button treatment:

- Linear gradient from accent blue to green where appropriate.
- Bold label text.
- Clean rectangular form.
- Enough padding and spacing for readability.
- Clear hover and keyboard focus states.

Use buttons and tiles for meaningful navigation, such as "Browse datasets," "Try an example," or "How to use the library." Avoid decorative button grids that do not help users decide where to go.

## Image guidance

Dataset and navigation images should make the library easier to scan.

Use:

- Flat composition or flat-lay style.
- Slightly muted bright colors.
- Square button or tile crops when images are used for navigation.
- Symbolic images that are easy to understand at small sizes.
- Consistent file names and useful alt text.

Avoid:

- POV scenes.
- Deep perspective.
- Shiny app-icon effects.
- Glossy 3D treatments.
- Images that imply the repository hosts data directly.
- Images without context, captions, or alt text.

When an image represents a dataset, it should communicate the dataset theme or access pattern, not pretend to be a sample of hosted data unless the file is a small documentation figure.

## Dataset-page layout

Dataset pages should help users answer: "Can I use this dataset for my work, and how do I get started?"

Recommended page rhythm:

1. Plain-language dataset summary.
2. What it contains.
3. Access pattern and access constraints.
4. R example.
5. Python example.
6. Minimum viable plot.
7. Suggested uses.
8. Limitations and cautions.
9. Tags.
10. Citation.

Use tables when they clarify access constraints or dataset metadata, for example spatial coverage, temporal coverage, update frequency, file type, and authentication status.

Avoid walls of links without context. Each important link should tell users what they will get when they click it.

## Markdown and layout rules

- Keep user-editable pages in Markdown.
- Do not add complex HTML into Markdown pages.
- Use CSS and templates for visual polish where possible.
- Keep dataset pages scannable but not skeletal.
- Prefer stable Markdown structures over one-off visual hacks.
- Use callouts sparingly for important access constraints, limitations, or safety notes.

Small inline HTML can be acceptable for legacy pages, but new work should not depend on custom HTML blocks for basic layout.

## Cloud Triangle note

The Data Library should reinforce this division of responsibility:

| Layer | Role |
| --- | --- |
| GitHub | Scripts, documentation, examples, metadata, and small documentation figures |
| Data source | Public external repositories, APIs, STAC catalogs, cloud buckets, or package-accessed services |
| Compute | The user's laptop, JupyterHub, Google Colab, cloud notebooks, or other analysis environments |

The repository should not store raw datasets, large derived datasets, model outputs, or bulk tabular data.

## Accessibility

- Use descriptive link text.
- Provide alt text for meaningful images.
- Keep contrast readable against blue and green backgrounds.
- Make navigation tiles keyboard reachable.
- Do not rely on color alone to communicate access status.
- Keep labels short enough to work on mobile screens.

## Maintenance checklist

Before merging a visual or content update, check:

- The page still explains where the data live.
- No credentials, secrets, or key-gated access paths were added as standard entries.
- Navigation labels are practical and short.
- Images have useful alt text.
- Markdown does not contain complex layout HTML.
- Dataset pages still include both R and Python access paths or clearly explain why one is not possible.
- The health check passes or reports only known legacy warnings.
