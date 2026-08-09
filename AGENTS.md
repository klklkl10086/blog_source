# AGENTS.md

This repository contains two systems with different responsibilities:

- `knowledge-base/`: long-term Obsidian-style personal knowledge base.
- Hexo blog project: `source/`, `themes/`, `_config.yml`, `package.json`, `.github/workflows/`.

The default rule is: protect the blog publishing system. Do not edit Hexo config, GitHub Actions, theme files, or published posts unless the user explicitly asks for that exact change.

## Knowledge Base Rules

### Note Types

Allowed `type` values:

- `map`: map of content, domain overview, navigation note.
- `concept`: atomic concept note.
- `source`: source note for papers, books, videos, docs, courses, or original blog posts.
- `project`: project/work log with decisions and implementation context.
- `experiment`: reproducible experiment, benchmark, lab, or investigation.
- `question`: open question or research thread.
- `draft`: blog draft staged for publication.
- `index`: operational index or maintenance note.

### Note Status

Allowed `status` values:

- `inbox`: captured but not processed.
- `extracted`: generated or extracted from an existing source; not verified.
- `draft`: actively being written.
- `active`: maintained by the author.
- `frozen`: kept as-is except for fixes.
- `archived`: historical value only.

AI-generated or mechanically extracted notes must use `status: extracted`. Do not mark generated notes as `verified`.

### Frontmatter

Every knowledge-base Markdown note should use YAML frontmatter:

```yaml
---
type: concept
status: extracted
domain:
  - ai-infra
source:
  - blog
source_post:
  - "source/_posts/kv_cache.md"
created: 2026-08-09
---
```

Required fields for all notes: `type`, `status`, `domain`, `created`.

Required for extracted notes: `source`.

Required for notes extracted from the Hexo blog: `source_post`.

### Naming Rules

- Use stable concept names, not transient article titles.
- Prefer `Title Case.md` for English technical concepts: `KV Cache.md`, `CUDA Thread Model.md`.
- Preserve canonical acronyms: `CUDA`, `KV`, `RAG`, `SGEMM`, `C++`.
- Use one concept per note.
- Do not add date prefixes to concept notes.
- Blog drafts may use descriptive slugs, but final Hexo filenames are produced during publishing.
- Avoid renaming published blog posts as part of knowledge maintenance.

### Backlink Rules

- Concept notes should link upward to at least one map when practical.
- Map notes should link to the main concept notes in that domain.
- Use Obsidian wikilinks for knowledge-base links: `[[KV Cache]]`.
- Use `source_post` for original blog files, not a wikilink.
- Do not create backlinks by editing old Hexo posts automatically.
- Broken wikilinks must be fixed before publishing a draft.

## Blog Publishing Rules

The blog publishing direction is one-way:

```text
knowledge-base/90_Blog_Drafts
  ↓
source/_posts
  ↓
existing Hexo workflow
```

Never reverse-sync from `source/_posts` into `knowledge-base`.

Publishing is manual and reviewed:

1. Compose or stage a draft in `knowledge-base/90_Blog_Drafts`.
2. Run knowledge checks from `scripts/knowledge/`.
3. Run `python scripts/knowledge/publish_blog.py --dry-run`.
4. Review the planned copy.
5. Run `python scripts/knowledge/publish_blog.py --apply`.
6. Commit the new blog post and any required assets.
7. Let the existing GitHub Actions workflow deploy the blog.

Do not modify `.github/workflows/deploy.yml`, `_config.yml`, `themes/`, or `package-lock.json` as part of publishing.
