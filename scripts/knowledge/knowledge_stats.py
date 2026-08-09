from collections import Counter
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import KB, markdown_files, parse_frontmatter


def main():
    files = markdown_files()
    by_type = Counter()
    by_status = Counter()
    by_domain = Counter()
    total_words = 0

    for path in files:
        text = path.read_text(encoding="utf-8", errors="replace")
        fm, body = parse_frontmatter(text)
        by_type[fm.get("type", "<missing>")] += 1
        by_status[fm.get("status", "<missing>")] += 1
        domains = fm.get("domain", [])
        if not isinstance(domains, list):
            domains = [domains]
        for domain in domains:
            by_domain[domain] += 1
        total_words += len(body.split())

    print(f"Knowledge base: {KB}")
    print(f"Markdown notes: {len(files)}")
    print(f"Approx words: {total_words}")
    print("\nBy type:")
    for key, value in sorted(by_type.items()):
        print(f"- {key}: {value}")
    print("\nBy status:")
    for key, value in sorted(by_status.items()):
        print(f"- {key}: {value}")
    print("\nBy domain:")
    for key, value in sorted(by_domain.items()):
        print(f"- {key}: {value}")


if __name__ == "__main__":
    main()
