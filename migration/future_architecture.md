# Future Architecture

Target structure: `knowledge-base` owns long-term Obsidian knowledge production, and `blog` owns Hexo publishing and automated deployment.

## Repository 1: knowledge-base

```text
knowledge-base/
├── 00_Inbox/
├── 01_Maps/
│   ├── AI Infra Map.md
│   ├── C++ Map.md
│   ├── Agent Map.md
│   ├── Algorithm Map.md
│   └── Systems Map.md
├── 02_Concepts/
├── 03_Sources/
├── 04_Projects/
├── 05_Experiments/
├── 06_Questions/
└── 90_Blog_Drafts/
```

Responsibilities: store Obsidian Markdown notes, MOCs, source notes, project notes, experiments, questions and future blog drafts. It should not contain Hexo theme code or run deployment workflows.

## Repository 2: blog

```text
blog/
├── .github/
│   └── workflows/
│       └── deploy.yml
├── scaffolds/
├── source/
│   ├── _posts/
│   ├── about/
│   ├── categories/
│   ├── tags/
│   └── Gallery/
├── themes/
├── _config.yml
├── package.json
└── package-lock.json
```

Responsibilities: keep Hexo source, published posts, image assets, theme, dependencies and GitHub Actions deployment.

## Keeping Hexo Workflow Stable

- Preserve `.github/workflows/deploy.yml`.
- Preserve `_config.yml`.
- Preserve `themes/butterfly/`.
- Preserve `package-lock.json`.
- Keep publishing through `git push main -> GitHub Actions -> hexo clean/generate/deploy`.

## Migration Path

### Phase 0: Freeze Current Blog Baseline

Record a commit/tag and keep the current blog intact.

### Phase 1: Create Empty knowledge-base Repository

Create the folder structure, then add MOCs and concept notes first. Do not copy every old blog post.

### Phase 2: Extract, Do Not Move

Extract meaning from `source/_posts`; leave published posts and assets in place. Each concept note should point back with `source_blog` metadata.

### Phase 3: Add Publishing Interface

```text
knowledge-base/90_Blog_Drafts/*.md
  ↓ manually reviewed publish script
blog/source/_posts/*.md
  ↓ git push main
GitHub Actions
  ↓ Hexo deploy
Website
```

The future script should only publish reviewed new drafts and transform front matter. It should not batch rewrite historical posts.

## Asset Strategy

Current blog assets rely on `post_asset_folder: true`. Future publishing should copy required draft assets into `blog/source/_posts/<post-name>/` and translate Obsidian image links to Hexo-friendly relative links. Existing blog assets should not be moved.

## Non-Actions

Do not split existing posts in this phase. Do not modify workflow, Hexo config, theme, old posts, old assets, or Git history.
