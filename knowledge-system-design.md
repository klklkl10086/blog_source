# Knowledge System Design

This document defines the long-term maintenance system for the current `knowledge-base` and Hexo blog.

## Goals

- Keep `knowledge-base/` as the long-term thinking and note-making system.
- Keep the Hexo blog as the publishing system.
- Preserve the existing blog deployment logic.
- Make publishing one-way: knowledge draft to blog post, never blog post back to knowledge base.

## Repository Boundaries

### knowledge-base

Owns:

- Atomic concept notes.
- Maps of content.
- Source notes.
- Project notes.
- Experiments.
- Questions.
- Blog drafts in `90_Blog_Drafts`.

Does not own:

- Hexo theme.
- GitHub Actions deployment.
- Published blog history.

### blog

Owns:

- Hexo website source.
- Published Markdown posts in `source/_posts`.
- Post asset folders.
- Theme and config.
- Existing GitHub Actions workflow.

Does not own:

- Long-term note graph.
- Atomic note maintenance.
- Obsidian workflows.

## Note Types

Allowed values for `type`:

- `map`: domain map and navigation note.
- `concept`: one stable idea or mechanism.
- `source`: note about a paper, video, book, doc, course, or original blog post.
- `project`: project state, decisions, and implementation history.
- `experiment`: benchmark, lab, reproduction, or investigation.
- `question`: unresolved question.
- `draft`: blog draft staged for publishing.
- `index`: maintenance index or operational note.

## Note Status

Allowed values for `status`:

- `inbox`: captured but not processed.
- `extracted`: extracted from blog/source material and not verified.
- `draft`: actively being written.
- `active`: maintained by the author.
- `frozen`: preserved with only small corrections.
- `archived`: historical reference only.

AI-generated or mechanically extracted notes must stay `extracted`. They must not be marked `verified`.

## Frontmatter Rules

Minimum note frontmatter:

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

Rules:

- Every Markdown note in `knowledge-base` should have frontmatter.
- Every extracted note should include `source`.
- Every note extracted from a blog article should include `source_post`.
- Use arrays for `domain`, `source`, and `source_post`.

## Naming Rules

- Use stable domain concepts: `PagedAttention.md`, not `kv_cache 第二节.md`.
- Use `Title Case.md` for English concept notes.
- Keep canonical acronyms and symbols: `C++`, `CUDA`, `KV`, `RAG`, `SGEMM`.
- Do not date-prefix concept notes.
- Use one concept per note.
- Blog drafts can use readable draft titles; the publish script copies them to Hexo posts without reverse synchronization.

## Backlink Rules

- Use Obsidian links: `[[KV Cache]]`.
- Concept notes should link to related concepts in `## Related`.
- Maps should link to their domain concepts.
- Source paths stay in frontmatter as `source_post`.
- Do not modify old blog posts to create backlinks.
- Run `python scripts/knowledge/check_broken_links.py` before publishing.

## Maintenance Scripts

Scripts live in `scripts/knowledge/`.

```text
scripts/knowledge/
├── check_broken_links.py
├── check_frontmatter.py
├── find_orphan_notes.py
├── knowledge_stats.py
└── publish_blog.py
```

Recommended routine:

```powershell
python scripts/knowledge/check_frontmatter.py
python scripts/knowledge/check_broken_links.py
python scripts/knowledge/find_orphan_notes.py
python scripts/knowledge/knowledge_stats.py
```

## Blog Publishing Flow

The flow is one-way:

```text
knowledge-base/90_Blog_Drafts
  ↓
source/_posts
  ↓
existing GitHub Actions workflow
  ↓
Website
```

### Publishing Steps

1. Write or stage a draft in `knowledge-base/90_Blog_Drafts`.
2. Ensure the draft has Hexo-compatible frontmatter.
3. Run checks:

```powershell
python scripts/knowledge/check_frontmatter.py
python scripts/knowledge/check_broken_links.py
python scripts/knowledge/publish_blog.py --dry-run
```

4. Review the output.
5. Publish with:

```powershell
python scripts/knowledge/publish_blog.py --apply
```

6. Review `git diff`.
7. Commit the new post and any required assets.

### Publishing Constraints

- Single direction only: draft to blog.
- No reverse sync.
- No automatic rewrite of historical posts.
- No automatic deletion in `source/_posts`.
- No changes to `.github/workflows/deploy.yml`.
- No changes to `_config.yml`.
- No changes to `themes/`.

## Review Gates

Manual review is required when:

- A note is a stub with only a source link.
- A requested concept has no source text.
- A blog draft includes images or assets.
- A draft would overwrite an existing post.
- A concept note contains claims beyond the source material.
