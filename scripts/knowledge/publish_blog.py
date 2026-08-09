import argparse
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import ROOT, KB, BLOG_POSTS, parse_frontmatter


DRAFTS = KB / "90_Blog_Drafts"


def validate_draft(path):
    text = path.read_text(encoding="utf-8", errors="replace")
    fm, _ = parse_frontmatter(text)
    missing = [key for key in ("title", "date") if key not in fm]
    if missing:
        return f"missing Hexo field(s): {', '.join(missing)}"
    return None


def main():
    parser = argparse.ArgumentParser(
        description="One-way publish from knowledge-base/90_Blog_Drafts to source/_posts."
    )
    parser.add_argument("--apply", action="store_true", help="copy drafts into source/_posts")
    parser.add_argument("--dry-run", action="store_true", help="show planned copies")
    parser.add_argument("--overwrite", action="store_true", help="allow overwriting existing blog posts")
    args = parser.parse_args()

    if not args.apply:
        args.dry_run = True

    BLOG_POSTS.mkdir(parents=True, exist_ok=True)
    drafts = sorted(DRAFTS.glob("*.md"))
    if not drafts:
        print(f"No drafts found in {DRAFTS.relative_to(ROOT)}")
        return 0

    planned = []
    errors = []
    for draft in drafts:
        issue = validate_draft(draft)
        if issue:
            errors.append(f"{draft.relative_to(ROOT)}: {issue}")
            continue
        dest = BLOG_POSTS / draft.name
        if dest.exists() and not args.overwrite:
            errors.append(f"{draft.relative_to(ROOT)}: destination exists: {dest.relative_to(ROOT)}")
            continue
        planned.append((draft, dest))

    if errors:
        print("Publish blocked:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("One-way publish plan:")
    for draft, dest in planned:
        print(f"- {draft.relative_to(ROOT)} -> {dest.relative_to(ROOT)}")

    if args.dry_run:
        print("Dry run only. Re-run with --apply to copy.")
        return 0

    for draft, dest in planned:
        shutil.copy2(draft, dest)
    print(f"Published {len(planned)} draft(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
