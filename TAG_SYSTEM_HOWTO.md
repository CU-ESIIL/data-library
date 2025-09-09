# Tag System Setup Guide

This guide explains how to recreate the Data Library's tag system in another repository. The process centers on a small Python script that scans Markdown documentation, builds tag index pages, and updates the navigation for a MkDocs site.

## 1. Prepare your repository

1. Organize your documentation under a top‑level `docs/` directory. Each dataset or topic should live in a nested folder inside `docs/`.
2. Add a `tags` field to the YAML front matter of each Markdown file or rely on the folder structure to derive tags. Tags should be lowercase and use hyphens for spaces, e.g.

   ```markdown
   ---
   title: Example dataset
   tags: [hazards, remote-sensing]
   ---
   ```

3. Ensure Python 3 and the [PyYAML](https://pyyaml.org/) package are available in your environment.

## 2. Copy the tag builder script

1. Copy [`scripts/build_tags.py`](scripts/build_tags.py) from this repository into the `scripts/` directory of your new project.
2. Adjust the `summit_descriptions` dictionary inside the script if you want special descriptions for particular tags. You can also edit the logic that derives tags from paths in the `derive_tags` function.

## 3. Generate tag pages

Run the script from the repository root:

```bash
python scripts/build_tags.py
```

The script will:

- Scan `docs/` for Markdown files and collect their tags.
- Create `docs/tags.md` with an index of all tags and the pages associated with each tag.
- Build a `docs/topic/` directory containing tag‑specific pages for the most common tags.
- Generate a standalone `docs/innovation-summit-2025.md` page when that tag is present.
- Rewrite `mkdocs.yml` to include the new pages in the site navigation.

Commit the generated files (`docs/tags.md`, any files under `docs/topic/`, `docs/innovation-summit-2025.md`, and the updated `mkdocs.yml`) along with your documentation.

## 4. Update your build process

Include the tag generation step in your documentation build workflow or continuous integration pipeline so that tag pages stay in sync with the Markdown sources.

## 5. Customizing the system

- **Different documentation locations**: If your docs are not in `docs/`, change the `docs_dir` variable at the top of the script.
- **Alternate navigation**: Modify the `cfg['nav']` block in the script to match your preferred MkDocs navigation structure.
- **Additional metadata**: Extend the script to read other front‑matter fields if you want more complex tagging logic.

By following these steps, any repository can implement the same automated tag pages used in the Data Library.
