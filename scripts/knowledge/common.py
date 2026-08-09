from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[2]
KB = ROOT / "knowledge-base"
BLOG_POSTS = ROOT / "source" / "_posts"


def markdown_files():
    return [
        path
        for path in KB.rglob("*.md")
        if ".obsidian" not in path.parts
    ]


def parse_frontmatter(text):
    if not text.startswith("---"):
        return {}, text
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", text, re.S)
    if not match:
        return {}, text
    raw, body = match.group(1), match.group(2)
    data = {}
    current = None
    for line in raw.splitlines():
        if not line.strip():
            continue
        key_value = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if key_value:
            current = key_value.group(1)
            value = key_value.group(2).strip()
            if value == "":
                data[current] = []
            elif value.startswith("[") and value.endswith("]"):
                data[current] = [
                    item.strip().strip("\"'")
                    for item in value[1:-1].split(",")
                    if item.strip()
                ]
            else:
                data[current] = value.strip("\"'")
            continue
        item = re.match(r"^\s*-\s*(.+)$", line)
        if item and current:
            if not isinstance(data.get(current), list):
                data[current] = [data[current]] if data.get(current) else []
            data[current].append(item.group(1).strip().strip("\"'"))
    return data, body


def note_index():
    index = {}
    for path in markdown_files():
        rel = path.relative_to(KB).as_posix()
        index[path.stem] = path
        index[rel] = path
        index[rel[:-3] if rel.endswith(".md") else rel] = path
    return index


def wikilinks(text):
    for match in re.finditer(r"\[\[([^\]]+)\]\]", text):
        target = match.group(1).split("|", 1)[0].split("#", 1)[0].strip()
        if target:
            yield target


def markdown_links(text):
    for match in re.finditer(r"(?<!!)\[[^\]]+\]\(([^)]+)\)", text):
        target = match.group(1).strip()
        if target and not re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target):
            if not target.startswith("#"):
                yield target
