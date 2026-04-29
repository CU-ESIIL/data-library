#!/usr/bin/env python3
"""Lightweight structural health checks for the ESIIL Data Library.

The checks are intentionally conservative: they do not download datasets,
execute examples, or mutate files. By default the script reports legacy
warnings while failing only for high-confidence errors such as broken MkDocs
navigation or likely committed secrets. Use --strict to fail on warnings too.
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

try:
    import yaml
except ImportError:  # pragma: no cover - useful when run before dependencies.
    yaml = None


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
MKDOCS = ROOT / "mkdocs.yml"

EXCLUDED_DOC_DIRS = {
    "assets",
    "stylesheets",
    "topic",
}

MAINTENANCE_PAGES = {
    "codex-prompts.md",
    "homepage-design-guidelines.md",
    "index.md",
    "innovation-summit-2026.md",
    "prompt-log.md",
    "style-guide.md",
    "tags.md",
}

DATASET_PARENT_DIRS = {
    "AI",
    "data",
    "datasets",
    "education",
    "ethics",
    "food",
    "forecasting",
    "harmonization",
    "hazards",
    "indian_country",
    "justice",
    "librarian",
    "library",
    "maka-sitomniya",
    "math",
    "policy",
    "remote_sensing",
    "scale",
    "solutions",
    "vegetation",
    "water",
}

REQUIRED_SECTION_PATTERNS = {
    "why useful": r"##\s+.*(why|overview|summary|useful|matters)",
    "what it contains": r"##\s+.*(what|contains|variables|source|metadata)",
    "access pattern": r"##\s+.*(access pattern|access|source|download|stream)",
    "access constraints": r"##\s+.*(access constraints|authentication|constraints|limitations)",
    "R example": r"##\s+.*\bR\b|\n```r",
    "Python example": r"##\s+.*(python)|\n```python",
    "minimum viable plot": r"##\s+.*(plot|visual|figure|map|chart)|\bplot\(",
    "suggested uses": r"##\s+.*(suggested uses|use cases|applications)",
    "limitations": r"##\s+.*(limitations|cautions|known issues|uncertainty)",
    "tags": r"(^---[\s\S]*?tags\s*:)|##\s+.*tags",
    "citation": r"##\s+.*(citation|references|cite)",
}

DISALLOWED_DATA_EXTENSIONS = {
    ".csv",
    ".dbf",
    ".geojson",
    ".gpkg",
    ".h5",
    ".hdf",
    ".hdf5",
    ".nc",
    ".parquet",
    ".rdata",
    ".rdb",
    ".rdx",
    ".shp",
    ".shx",
    ".tif",
    ".tiff",
    ".zip",
}

GENERATED_OR_CACHE_MARKERS = (
    "_cache",
    "_files",
    "/cache/",
    "/temp/",
    "/rawData/",
    "/data_raw/",
    "__MACOSX",
)

SECRET_PATTERNS = {
    "AWS access key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "GitHub token": re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{30,}\b"),
    "OpenAI key": re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    "private key": re.compile(r"-----BEGIN (?:RSA |OPENSSH |EC |DSA )?PRIVATE KEY-----"),
    "assigned credential": re.compile(
        r"(?i)\b(api[_-]?key|token|password|secret)\b\s*[:=]\s*['\"][^'\"\s]{12,}['\"]"
    ),
}

PLACEHOLDER_WORDS = {
    "example",
    "placeholder",
    "your",
    "replace",
    "changeme",
    "xxxx",
    "dummy",
}


@dataclass
class Finding:
    severity: str
    path: str
    message: str


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def add(findings: list[Finding], severity: str, path: Path | str, message: str) -> None:
    findings.append(Finding(severity, rel(path) if isinstance(path, Path) else path, message))


def iter_dataset_pages() -> Iterable[Path]:
    if not DOCS.exists():
        return
    for path in sorted(DOCS.rglob("*.md")):
        relative = path.relative_to(DOCS)
        parts = relative.parts
        if not parts:
            continue
        if parts[0] in EXCLUDED_DOC_DIRS:
            continue
        if len(parts) == 1 and parts[0] in MAINTENANCE_PAGES:
            continue
        if parts[0] not in DATASET_PARENT_DIRS:
            continue
        if any(marker.strip("/") in parts for marker in ("cache", "temp", "rawData", "data_raw")):
            continue
        yield path


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def has_front_matter_tags(content: str) -> bool:
    match = re.match(r"^---\n(?P<front>.*?)\n---\n", content, flags=re.DOTALL)
    return bool(match and re.search(r"(?m)^tags\s*:", match.group("front")))


def check_dataset_pages(findings: list[Finding]) -> None:
    pages = list(iter_dataset_pages() or [])
    if not pages:
        add(findings, "warning", DOCS, "No dataset-like Markdown pages were found.")
        return

    for path in pages:
        content = read_text(path)
        lower = content.lower()
        for label, pattern in REQUIRED_SECTION_PATTERNS.items():
            if label == "tags" and has_front_matter_tags(content):
                continue
            if not re.search(pattern, content, flags=re.IGNORECASE | re.MULTILINE):
                add(findings, "warning", path, f"Dataset page may be missing section or evidence for: {label}.")

        if "no key" not in lower and "no authentication" not in lower and "without authentication" not in lower:
            add(findings, "warning", path, "Access constraints should clearly state whether no key/authentication is required.")

        if re.search(r"(?i)\b(sys\.getenv|os\.environ|getenv|api[_-]?key|token|password)\b", content):
            add(findings, "warning", path, "Dataset page mentions credentials or environment variables; confirm this is not a standard key-gated entry.")

        if "<div" in lower or "<script" in lower or "<style" in lower:
            add(findings, "warning", path, "Dataset page contains layout HTML; prefer Markdown plus shared CSS for new work.")


def check_large_or_hosted_data(findings: list[Finding], max_bytes: int) -> None:
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file():
            continue
        if ".git" in path.parts:
            continue
        suffix = path.suffix.lower()
        if suffix not in DISALLOWED_DATA_EXTENSIONS:
            continue
        try:
            size = path.stat().st_size
        except OSError:
            continue
        normalized = rel(path)
        is_cache_like = any(marker in normalized for marker in GENERATED_OR_CACHE_MARKERS)
        if size > max_bytes:
            add(
                findings,
                "warning",
                path,
                f"Large data-like file is present ({size / 1024 / 1024:.1f} MB). The repo should document external storage instead of hosting data.",
            )
        elif not is_cache_like and path.is_relative_to(DOCS):
            add(
                findings,
                "warning",
                path,
                "Data-like file is committed under docs; keep only tiny metadata/examples and avoid raw datasets.",
            )


def check_secrets(findings: list[Finding]) -> None:
    text_extensions = {
        ".css",
        ".html",
        ".js",
        ".json",
        ".md",
        ".py",
        ".qmd",
        ".r",
        ".txt",
        ".yaml",
        ".yml",
    }
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or ".git" in path.parts or path.suffix.lower() not in text_extensions:
            continue
        content = read_text(path)
        for label, pattern in SECRET_PATTERNS.items():
            for match in pattern.finditer(content):
                snippet = match.group(0).lower()
                if any(word in snippet for word in PLACEHOLDER_WORDS):
                    continue
                add(findings, "error", path, f"Possible committed secret detected: {label}.")


def flatten_nav(nav: object) -> Iterable[str]:
    if isinstance(nav, str):
        yield nav
    elif isinstance(nav, list):
        for item in nav:
            yield from flatten_nav(item)
    elif isinstance(nav, dict):
        for value in nav.values():
            yield from flatten_nav(value)


def check_mkdocs_nav(findings: list[Finding]) -> None:
    if not MKDOCS.exists():
        add(findings, "error", MKDOCS, "mkdocs.yml is missing.")
        return
    mkdocs_text = read_text(MKDOCS)
    if yaml is None:
        nav_targets = re.findall(r":[ \t]+([^#\n]+\.md)\s*$", mkdocs_text, flags=re.MULTILINE)
        extra_css_targets = re.findall(r"^\s*-\s+([^#\n]+\.css)\s*$", mkdocs_text, flags=re.MULTILINE)
        for target in nav_targets:
            target_path = DOCS / target.strip()
            if not target_path.exists():
                add(findings, "error", MKDOCS, f"Navigation target does not exist: {target.strip()}")
        for css in extra_css_targets:
            css_path = DOCS / css.strip()
            if not css_path.exists():
                add(findings, "error", MKDOCS, f"extra_css target does not exist: {css.strip()}")
        return
    config = yaml.safe_load(mkdocs_text) or {}
    nav = config.get("nav", [])
    for target in flatten_nav(nav):
        if re.match(r"^[a-z]+://", target):
            continue
        target_path = DOCS / target
        if not target_path.exists():
            add(findings, "error", MKDOCS, f"Navigation target does not exist: {target}")

    extra_css = config.get("extra_css", [])
    for css in extra_css:
        css_path = DOCS / css
        if not css_path.exists():
            add(findings, "error", MKDOCS, f"extra_css target does not exist: {css}")


def summarize(findings: list[Finding], limit: int) -> int:
    errors = [f for f in findings if f.severity == "error"]
    warnings = [f for f in findings if f.severity == "warning"]
    print("Data Library health check")
    print(f"Errors: {len(errors)}")
    print(f"Warnings: {len(warnings)}")
    print()
    for finding in findings[:limit]:
        print(f"[{finding.severity.upper()}] {finding.path}: {finding.message}")
    remaining = len(findings) - limit
    if remaining > 0:
        print(f"... {remaining} additional finding(s) hidden. Re-run with --limit 0 to show all.")
    if not findings:
        print("No findings.")
    return len(errors)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--strict", action="store_true", help="Fail when warnings are present.")
    parser.add_argument(
        "--max-data-mb",
        type=float,
        default=5.0,
        help="Warn when data-like files exceed this size. Default: 5 MB.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=200,
        help="Maximum findings to print. Use 0 to print all findings. Default: 200.",
    )
    args = parser.parse_args(argv)

    findings: list[Finding] = []
    check_mkdocs_nav(findings)
    check_dataset_pages(findings)
    check_large_or_hosted_data(findings, int(args.max_data_mb * 1024 * 1024))
    check_secrets(findings)

    limit = len(findings) if args.limit == 0 else max(args.limit, 0)
    error_count = summarize(findings, limit)
    if error_count:
        return 1
    if args.strict and findings:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
