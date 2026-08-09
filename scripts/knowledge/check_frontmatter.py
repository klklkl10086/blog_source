import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import KB, markdown_files, parse_frontmatter


ALLOWED_TYPES = {
    "map",
    "concept",
    "source",
    "project",
    "experiment",
    "question",
    "draft",
    "index",
}
ALLOWED_STATUS = {
    "inbox",
    "extracted",
    "draft",
    "active",
    "frozen",
    "archived",
}
REQUIRED = {"type", "status", "domain", "created"}


def as_list(value):
    if value is None:
        return []
    return value if isinstance(value, list) else [value]


def main():
    errors = []
    for path in markdown_files():
        text = path.read_text(encoding="utf-8", errors="replace")
        fm, _ = parse_frontmatter(text)
        rel = path.relative_to(KB)
        missing = sorted(REQUIRED - set(fm))
        if missing:
            errors.append(f"{rel}: missing {', '.join(missing)}")
            continue
        if fm.get("type") not in ALLOWED_TYPES:
            errors.append(f"{rel}: invalid type {fm.get('type')}")
        if fm.get("status") not in ALLOWED_STATUS:
            errors.append(f"{rel}: invalid status {fm.get('status')}")
        if not as_list(fm.get("domain")):
            errors.append(f"{rel}: domain must not be empty")
        if fm.get("status") == "extracted" and not as_list(fm.get("source")):
            errors.append(f"{rel}: extracted note must include source")
        if "blog" in as_list(fm.get("source")) and not as_list(fm.get("source_post")):
            errors.append(f"{rel}: blog-sourced note must include source_post")
        if fm.get("status") == "verified":
            errors.append(f"{rel}: status verified is not allowed for generated notes")

    if errors:
        print("Frontmatter issues found:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Knowledge-base frontmatter looks good.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
