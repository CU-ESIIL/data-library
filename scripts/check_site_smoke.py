#!/usr/bin/env python3
"""Static, Playwright-style smoke checks for a built MkDocs site.

This is intentionally dependency-free. It does not replace browser tests, but
it catches common breakage after `mkdocs build`: missing key pages, empty
documents, broken local links, missing images, and absent style assets.
"""

from __future__ import annotations

import argparse
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse


REQUIRED_PAGES = (
    "index.html",
    "innovation-summit-2026/index.html",
    "style-guide/index.html",
    "tags/index.html",
)


class LinkImageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []
        self.images: list[tuple[str, str]] = []
        self.stylesheets: list[str] = []
        self.text_chunks: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = {name: value or "" for name, value in attrs}
        if tag == "a" and attr.get("href"):
            self.links.append(attr["href"])
        if tag == "img" and attr.get("src"):
            self.images.append((attr["src"], attr.get("alt", "")))
        if tag == "link" and attr.get("rel") == "stylesheet" and attr.get("href"):
            self.stylesheets.append(attr["href"])

    def handle_data(self, data: str) -> None:
        if data.strip():
            self.text_chunks.append(data.strip())


def local_target_exists(site_dir: Path, current_file: Path, target: str) -> bool:
    if target == "..." or target.startswith("data:"):
        return True
    parsed = urlparse(target)
    if parsed.scheme or parsed.netloc or target.startswith("mailto:") or target.startswith("tel:"):
        return True
    if not parsed.path or parsed.path.startswith("#"):
        return True
    path = unquote(parsed.path)
    if path.startswith("/"):
        candidate = site_dir / path.lstrip("/")
        if not candidate.exists():
            parts = Path(path.lstrip("/")).parts
            if len(parts) > 1:
                candidate = site_dir.joinpath(*parts[1:])
    else:
        candidate = current_file.parent / path
    if candidate.is_dir():
        candidate = candidate / "index.html"
    return candidate.exists()


def check_site(site_dir: Path, all_pages: bool, check_alt: bool) -> list[str]:
    findings: list[str] = []
    if not site_dir.exists():
        return [f"Built site directory does not exist: {site_dir}"]

    for required in REQUIRED_PAGES:
        page = site_dir / required
        if not page.exists():
            findings.append(f"Required built page is missing: {required}")

    if all_pages:
        html_files = sorted(site_dir.rglob("*.html"))
    else:
        html_files = [site_dir / page for page in REQUIRED_PAGES if (site_dir / page).exists()]
    if not html_files:
        findings.append("No HTML files found in built site.")
        return findings

    for html_file in html_files:
        parser = LinkImageParser()
        parser.feed(html_file.read_text(encoding="utf-8", errors="replace"))
        visible_text = " ".join(parser.text_chunks)
        if len(re.sub(r"\s+", " ", visible_text).strip()) < 80:
            findings.append(f"Built page has very little visible text: {html_file.relative_to(site_dir)}")

        for href in parser.links:
            if not local_target_exists(site_dir, html_file, href):
                findings.append(f"Broken local link in {html_file.relative_to(site_dir)}: {href}")

        for src, alt in parser.images:
            if not local_target_exists(site_dir, html_file, src):
                findings.append(f"Missing image in {html_file.relative_to(site_dir)}: {src}")
            if check_alt and not alt.strip():
                findings.append(f"Image is missing alt text in {html_file.relative_to(site_dir)}: {src}")

    css_candidates = list(site_dir.rglob("extra*.css"))
    css_text = "\n".join(path.read_text(encoding="utf-8", errors="replace") for path in css_candidates)
    if "--esiil-primary-blue" not in css_text:
        findings.append("Built CSS does not include ESIIL style variables.")

    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("site_dir", nargs="?", default="site", help="Built MkDocs site directory.")
    parser.add_argument("--all-pages", action="store_true", help="Check every built HTML page, including legacy dataset pages.")
    parser.add_argument("--check-alt", action="store_true", help="Report images without alt text.")
    args = parser.parse_args(argv)

    site_dir = Path(args.site_dir).resolve()
    findings = check_site(site_dir, args.all_pages, args.check_alt)
    print("Built-site smoke check")
    print(f"Findings: {len(findings)}")
    for finding in findings:
        print(f"[SMOKE] {finding}")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
