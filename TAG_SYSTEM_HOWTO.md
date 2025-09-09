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

## 2. Create the tag builder script

Create `scripts/build_tags.py` in your project and paste the following code. The `build_tag_pages` function wraps the entire tag system so it can be imported or run as a script without referring back to this repository.

```python
#!/usr/bin/env python3
"""Generate tag front matter for markdown files and build tag index page."""
from pathlib import Path
import re
import yaml


def build_tag_pages(docs_dir=Path("docs"), mkdocs_path=Path("mkdocs.yml")):
    tag_page = docs_dir / "tags.md"
    topic_dir = docs_dir / "topic"

    # Descriptions for Innovation Summit datasets
    summit_descriptions = {
        "Air data":
            "EPA county-level air quality metrics track pollution-driven tipping points.",
        "FAO":
            "Global food balance sheets reveal agricultural trends linked to ecological transitions.",
        "FIRED":
            "Wildfire event polygons highlight landscapes nearing fire-driven tipping points.",
        "NLCD":
            "National land cover maps expose land-use changes that can trigger ecosystem shifts.",
        "Phenology network":
            "Seasonal plant and animal observations signal climate-driven ecological transitions.",
        "epa water quality":
            "Water-quality monitoring helps detect aquatic systems approaching degradation thresholds.",
        "epica dome c ch4":
            "Antarctic methane records provide context for modern atmospheric tipping points.",
        "global forest change":
            "Landsat-based forest loss and gain reveal deforestation tipping points worldwide.",
        "iNaturalist":
            "Citizen-science species occurrences capture biodiversity shifts near critical thresholds.",
        "lidar canopy height":
            "NEON lidar canopy models track forest structure changes preceding regime shifts.",
        "nclimgrid":
            "NOAA gridded climate normals show trends that may push regions past climate tipping points.",
        "neon and lter":
            "Integrated macroinvertebrate data uncover aquatic community transitions.",
        "neon aquatic":
            "Sensor-based water data monitor freshwater systems for early warning signs.",
        "neon hyperspectral":
            "High-resolution spectral imagery detects vegetation stress before ecosystem tipping.",
        "neon lidar and organismal":
            "Fusing structural and biological data links habitat change to ecological thresholds.",
        "nrcs soil exploration":
            "Soil survey attributes illuminate land degradation tipping points.",
        "osm":
            "OpenStreetMap vectors map human pressures that drive ecological tipping dynamics.",
        "prism":
            "Gridded temperature and precipitation normals track climate trends toward tipping points.",
        "rap-tiles":
            "Rangeland Analysis Platform tiles reveal vegetation transitions and desertification risk.",
        "sentinel streaming":
            "Sentinel-2 quicklooks enable rapid detection of landscape changes near thresholds.",
        "usgs water services":
            "Streamflow and groundwater APIs flag hydrologic systems near critical limits.",
        "watershed boundaries":
            "Hydrologic unit maps frame catchments vulnerable to ecological shifts.",
        "weatherbench":
            "Benchmark datasets support models predicting extreme events and tipping points.",
    }

    def derive_tags(md_path):
        parts = md_path.relative_to(docs_dir).parts[:-1]
        tags = []
        for i, p in enumerate(parts):
            if i < 2:
                tags.append(p.replace(" ", "-").lower())
        return tags

    def read_title(content, md_path):
        lines = content.splitlines()
        if lines and lines[0].startswith("# "):
            return lines[0][2:].strip()
        if len(lines) >= 2 and set(lines[1]) == {"="}:
            return lines[0].strip()
        return md_path.stem.replace("_", " ").strip()

    tags_map = {}
    for md_path in docs_dir.rglob("*.md"):
        if md_path == tag_page:
            continue
        parts = md_path.relative_to(docs_dir).parts
        if len(parts) > 3 or parts[0] == "topic":
            continue
        content = md_path.read_text(encoding="utf-8")
        frontmatter_match = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)
        if frontmatter_match:
            fm = yaml.safe_load(frontmatter_match.group(1)) or {}
            body = content[frontmatter_match.end():]
        else:
            fm = {}
            body = content
        tags = fm.get("tags") or derive_tags(md_path)
        title = read_title(content, md_path)
        for tag in tags:
            tags_map.setdefault(tag, []).append((title, md_path.relative_to(docs_dir).as_posix()))

    tag_page.write_text("# Tags\n\n", encoding="utf-8")
    with tag_page.open("a", encoding="utf-8") as f:
        for tag in sorted(tags_map):
            f.write(f"## {tag}\n\n")
            if tag == "innovation-summit-2025":
                f.write("[Visit the Innovation Summit website](https://www.colorado.edu/esiil/)\n\n")
                f.write("![Innovation Summit 2025](assets/pre-summit-training-header.png)\n\n")
            for title, path in sorted(tags_map[tag]):
                desc = summit_descriptions.get(title)
                if tag == "innovation-summit-2025" and desc:
                    f.write(f"- [{title}]({path}) - {desc}\n")
                else:
                    f.write(f"- [{title}]({path})\n")
            f.write("\n")

    tag_counts = {tag: len(paths) for tag, paths in tags_map.items()}
    top_tags = [
        tag
        for tag, count in sorted(tag_counts.items(), key=lambda x: (-x[1], x[0]))
        if count > 1 and not any(ch.isdigit() for ch in tag)
    ][:10]

    topic_dir.mkdir(exist_ok=True)
    for tag in top_tags:
        tag_file = topic_dir / f"{tag}.md"
        with tag_file.open("w", encoding="utf-8") as f:
            f.write(f"# {tag}\n\n")
            for title, path in sorted(tags_map.get(tag, [])):
                f.write(f"- [{title}](../{path})\n")

    # Custom standalone page for Innovation Summit 2025 tag
    summit_page = docs_dir / "innovation-summit-2025.md"
    with summit_page.open("w", encoding="utf-8") as f:
        f.write("# Innovation Summit 2025\n\n")
        f.write("[Visit the Innovation Summit website](https://www.colorado.edu/esiil/)\n\n")
        f.write("![Innovation Summit 2025](assets/pre-summit-training-header.png)\n\n")
        for title, path in sorted(tags_map.get("innovation-summit-2025", [])):
            desc = summit_descriptions.get(title)
            if desc:
                f.write(f"- [{title}]({path}) - {desc}\n")
            else:
                f.write(f"- [{title}]({path})\n")
        f.write("\n")

    if mkdocs_path.exists():
        cfg = yaml.safe_load(mkdocs_path.read_text(encoding="utf-8"))
        cfg["nav"] = [
            {"Innovation Summit 2025": "innovation-summit-2025.md"},
            {"Home": "index.md"},
            {"Topics": [{tag: f"topic/{tag}.md"} for tag in top_tags]},
            {"Tags": "tags.md"},
        ]
        mkdocs_path.write_text(yaml.dump(cfg, sort_keys=False), encoding="utf-8")


if __name__ == "__main__":
    build_tag_pages()
```

Adjust the `summit_descriptions` dictionary or the `derive_tags` function if you need custom behavior.

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
