#!/usr/bin/env python3
"""Generate tag front matter for markdown files and build tag index page."""
from pathlib import Path
import re
import yaml

docs_dir = Path('docs')
tag_page = docs_dir / 'tags.md'

def derive_tags(md_path):
    parts = md_path.relative_to(docs_dir).parts[:-1]
    tags = []
    for i, p in enumerate(parts):
        if i < 2:
            tags.append(p.replace(' ', '-').lower())
    return tags

def read_title(content, md_path):
    lines = content.splitlines()
    if lines and lines[0].startswith('# '):
        return lines[0][2:].strip()
    if len(lines) >= 2 and set(lines[1]) == {'='}:
        return lines[0].strip()
    return md_path.stem.replace('_', ' ').strip()

tags_map = {}
for md_path in docs_dir.rglob('*.md'):
    if md_path == tag_page:
        continue
    content = md_path.read_text(encoding='utf-8')
    frontmatter_match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    if frontmatter_match:
        fm = yaml.safe_load(frontmatter_match.group(1)) or {}
        body = content[frontmatter_match.end():]
    else:
        fm = {}
        body = content
    if not fm.get('tags'):
        fm['tags'] = derive_tags(md_path)
        front = '---\n' + yaml.dump(fm, sort_keys=False).strip() + '\n---\n\n'
        content = front + body.lstrip('\n')
        md_path.write_text(content, encoding='utf-8')
    title = read_title(content, md_path)
    for tag in fm.get('tags', []):
        tags_map.setdefault(tag, []).append((title, md_path.relative_to(docs_dir).as_posix()))

tag_page.write_text('# Tags\n\n', encoding='utf-8')
with tag_page.open('a', encoding='utf-8') as f:
    for tag in sorted(tags_map):
        f.write(f'## {tag}\n\n')
        for title, path in sorted(tags_map[tag]):
            f.write(f'- [{title}]({path})\n')
        f.write('\n')
