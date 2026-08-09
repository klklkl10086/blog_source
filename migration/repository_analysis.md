# Repository Analysis

Generated on 2026-08-09. Scope: Git root `D:/MYBLOG`. This phase only analyzes and plans; it does not modify Hexo config, workflows, theme files, or posts.

## Current Repository Tree

```text
MYBLOG/
├── .github/
│   ├── dependabot.yml
│   └── workflows/
│       └── deploy.yml
├── scaffolds/
│   ├── draft.md
│   ├── page.md
│   └── post.md
├── source/
│   ├── _posts/
│   │   ├── 33 markdown posts
│   │   └── per-post asset folders, mostly images
│   ├── about/
│   ├── categories/
│   ├── Gallery/
│   └── tags/
├── themes/
│   ├── .gitkeep
│   └── butterfly/
│       ├── _config.yml
│       ├── layout/
│       ├── scripts/
│       └── source/
├── .gitignore
├── _config.landscape.yml
├── _config.yml
├── db.json
├── package-lock.json
└── package.json
```

## Hexo Core Files

- `_config.yml`: main Hexo config. Key fields: `source_dir: source`, `public_dir: public`, `theme: butterfly`, `post_asset_folder: true`, `future: true`, `deploy.type: git`.
- `package.json` / `package-lock.json`: Node and Hexo dependency surface. Scripts: `build`, `clean`, `deploy`, `server`.
- `scaffolds/`: Hexo templates for draft/page/post.
- `source/`: Hexo content input directory.
- `themes/butterfly/`: active theme, including layout, scripts, theme source and theme config.
- `.gitignore`: ignores generated/cache directories such as `node_modules/`, `public/`, `.deploy*/`, and `db.json`.

## Workflow Files

- `.github/workflows/deploy.yml`: main deployment workflow.
- `.github/dependabot.yml`: dependency maintenance config.
- `themes/butterfly/.github/workflows/*`: theme upstream files; not the active repository workflow entry points.

## Theme

The active theme is `butterfly` at `themes/butterfly/`. Its package metadata reports version `4.9.0`. The theme's `layout/`, `scripts/`, and `source/` directories directly affect rendering, styles, tag plugins, and front-end behavior.

## source/_posts

- Markdown posts: 33.
- Files under `_posts`: 1201 total, including 1136 `.png`, 29 `.jpg`, 2 `.bmp`, 1 `.webp`, and 33 `.md` files.
- `post_asset_folder: true` makes per-post asset directories and relative image references a major stability concern.

## Scripts

- There is no root-level `scripts/` directory.
- NPM scripts live in `package.json`.
- Theme scripts live under `themes/butterfly/scripts/`.

## Config

- Site config: `_config.yml`.
- Theme config: `themes/butterfly/_config.yml`.
- Empty file: `_config.landscape.yml`.
- Post front matter is the current source for categories and tags.

## Package Dependencies

Core dependencies include Hexo 7.3.0, `hexo-deployer-git`, archive/category/feed/index/sitemap/tag generators, ejs/markdown-it/pug/stylus renderers, `hexo-server`, and `markdown-it-anchor`.

## Current Blog Publishing Flow

```text
git push to main
  ↓
GitHub Actions: .github/workflows/deploy.yml
  ↓
actions/checkout@v4
  ↓
setup-node@v4, Node.js 20, npm cache
  ↓
Install Pandoc
  ↓
npm install
  ↓
configure git identity and token URL rewrite
  ↓
sed attempts to rewrite _config.yml repo field
  ↓
npx hexo clean
  ↓
npx hexo generate
  ↓
npx hexo deploy
  ↓
publish generated site to klklkl10086.github.io repository, branch master
```

## Directory Ownership

### A. Blog Publishing System

`.github/workflows/deploy.yml`, `.github/dependabot.yml`, `_config.yml`, `_config.landscape.yml`, `package.json`, `package-lock.json`, `scaffolds/`, `themes/`, `.gitignore`.

### B. Content System

`source/_posts/*.md`, `source/_posts/<post-name>/` asset directories, `source/about/`, `source/categories/`, `source/tags/`, `source/Gallery/`.

### C. Can Migrate To Knowledge Base

Candidate semantic areas: CUDA, KV Cache, Reduction, LLM implementation, RAG, Post-Training, Linux/C++ systems programming, networking, data structures, machine learning, and PyTorch. Migration should extract/copy meaning only; do not move the published source files.

## Risk Points

- Do not auto-modify `.github/workflows/deploy.yml`.
- Do not auto-modify `_config.yml`.
- Do not auto-modify `themes/butterfly/`.
- Do not batch rewrite `source/_posts/*.md`.
- Do not move `source/_posts/<post-name>/` asset directories.
- The workflow uses `sed -i "s|repo:.*|...|g" _config.yml`, while the current config uses `deploy.repository`; do not change this without build/deploy verification.
- Some Chinese comments in `_config.yml` display as mojibake, so bulk formatting config files is risky.
