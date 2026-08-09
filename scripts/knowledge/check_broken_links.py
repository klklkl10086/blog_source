import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import KB, markdown_files, note_index, wikilinks, markdown_links


def resolve_wikilink(target, index):
    if target in index:
        return True
    if target + ".md" in index:
        return True
    return False


def main():
    index = note_index()
    broken = []
    for path in markdown_files():
        text = path.read_text(encoding="utf-8", errors="replace")
        for target in wikilinks(text):
            if not resolve_wikilink(target, index):
                broken.append((path, f"[[{target}]]"))
        for target in markdown_links(text):
            clean = target.split("#", 1)[0]
            candidate = (path.parent / clean).resolve()
            try:
                candidate.relative_to(KB.resolve())
            except ValueError:
                continue
            if clean and not candidate.exists():
                broken.append((path, target))

    if broken:
        print("Broken links found:")
        for path, target in broken:
            print(f"- {path.relative_to(KB)} -> {target}")
        return 1
    print("No broken knowledge-base links found.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
