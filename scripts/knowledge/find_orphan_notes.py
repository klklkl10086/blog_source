import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import KB, markdown_files, parse_frontmatter, wikilinks


def main():
    inbound = {}
    paths_by_stem = {}
    for path in markdown_files():
        paths_by_stem[path.stem] = path
        inbound[path.stem] = 0

    for path in markdown_files():
        text = path.read_text(encoding="utf-8", errors="replace")
        for target in wikilinks(text):
            stem = target.split("/", 1)[-1]
            if stem in inbound and stem != path.stem:
                inbound[stem] += 1

    orphans = []
    for stem, count in inbound.items():
        path = paths_by_stem[stem]
        fm, _ = parse_frontmatter(path.read_text(encoding="utf-8", errors="replace"))
        if fm.get("type") == "map":
            continue
        if count == 0:
            orphans.append(path)

    if orphans:
        print("Orphan notes found:")
        for path in sorted(orphans):
            print(f"- {path.relative_to(KB)}")
        return 1
    print("No orphan concept/source/project notes found.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
