#!/usr/bin/env python3
"""Generate tag front matter for markdown files and build tag index page."""
from pathlib import Path
import re
import yaml

docs_dir = Path('docs')
tag_page = docs_dir / 'tags.md'
topic_dir = docs_dir / 'topic'
mkdocs_path = Path('mkdocs.yml')

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
    parts = md_path.relative_to(docs_dir).parts
    if len(parts) > 3 or parts[0] == 'topic':
        continue
    content = md_path.read_text(encoding='utf-8')
    frontmatter_match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    if frontmatter_match:
        fm = yaml.safe_load(frontmatter_match.group(1)) or {}
        body = content[frontmatter_match.end():]
    else:
        fm = {}
        body = content
    tags = fm.get('tags') or derive_tags(md_path)
    title = read_title(content, md_path)
    for tag in tags:
        tags_map.setdefault(tag, []).append((title, md_path.relative_to(docs_dir).as_posix()))

tag_page.write_text('# Tags\n\n', encoding='utf-8')
with tag_page.open('a', encoding='utf-8') as f:
    for tag in sorted(tags_map):
        f.write(f'## {tag}\n\n')
        for title, path in sorted(tags_map[tag]):
            f.write(f'- [{title}]({path})\n')
        f.write('\n')

tag_counts = {tag: len(paths) for tag, paths in tags_map.items()}
top_tags = [
    tag
    for tag, count in sorted(tag_counts.items(), key=lambda x: (-x[1], x[0]))
    if count > 1 and not any(ch.isdigit() for ch in tag)
][:10]

topic_dir.mkdir(exist_ok=True)
for tag in top_tags:
    tag_file = topic_dir / f'{tag}.md'
    with tag_file.open('w', encoding='utf-8') as f:
        f.write(f'# {tag}\n\n')
        for title, path in sorted(tags_map.get(tag, [])):
            f.write(f'- [{title}](../{path})\n')

if mkdocs_path.exists():
    cfg = yaml.safe_load(mkdocs_path.read_text(encoding='utf-8'))
    cfg['nav'] = [
        {'Home': 'index.md'},
        {'Topics': [{tag: f'topic/{tag}.md'} for tag in top_tags]},
        {'Tags': 'tags.md'},
    ]
    mkdocs_path.write_text(yaml.dump(cfg, sort_keys=False), encoding='utf-8')
