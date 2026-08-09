# Final Report

## Current Repository State

The repository is a complete Hexo blog project at Git root `D:/MYBLOG`, currently on branch `main`. It contains Hexo source, Markdown posts, theme code, dependency lock files and GitHub Actions deployment.

Key facts: Hexo 7.3.0; theme `themes/butterfly`; posts in `source/_posts`; 33 Markdown posts; 1201 files under `_posts`; about 1168 image/media assets; deployment workflow `.github/workflows/deploy.yml`; trigger branch `main`; deployment command sequence `npx hexo clean && npx hexo generate && npx hexo deploy`; target repository `klklkl10086.github.io.git`, branch `master`.

## Largest Structural Problems

1. The blog publishing system and long-term knowledge base are mixed together.
2. The taxonomy mixes domain, type, source and status in one category layer.
3. Several posts have grown into knowledge collections rather than publishable articles.
4. Image assets are tightly coupled to Hexo `post_asset_folder` behavior.
5. Workflow and Hexo config are deployment-critical and should not be touched during migration planning.

## Recommended Migration Route

Step 1: keep the blog repository stable and preserve workflow, config, theme and posts.

Step 2: create a separate `knowledge-base` repository with `00_Inbox`, `01_Maps`, `02_Concepts`, `03_Sources`, `04_Projects`, `05_Experiments`, `06_Questions`, and `90_Blog_Drafts`.

Step 3: extract AI Infra and C++ Systems first: CUDA, KV Cache, Reduction, LLM implementation, Linux/C++ systems programming.

Step 4: design a publishing bridge later. Drafts are written in knowledge-base, reviewed manually, then published into blog `source/_posts`.

Step 5: freeze historical course notes and extract only reusable concepts.

## First 20 Knowledge Topics

1. CUDA Thread Model
2. GPU Architecture
3. CUDA Memory Hierarchy
4. Shared Memory
5. Global Memory Coalescing
6. Bank Conflict
7. Parallel Reduction
8. SGEMM Tiling
9. KV Cache
10. PagedAttention
11. Rolling KV Cache
12. Continuous Batching
13. FlashAttention
14. Transformer from Scratch
15. Tokenization Pipeline
16. Self-Attention Implementation
17. RAG Pipeline
18. Supervised Fine-Tuning
19. C++ Move Semantics
20. Linux File Descriptor

## Estimated Effort

- Repository split preparation: 0.5 to 1 day.
- Initial knowledge-base structure and MOCs: 0.5 to 1 day.
- First 20 concept notes: 3 to 6 days.
- Asset strategy and publishing script design: 1 to 2 days.
- First publish-flow validation: 0.5 to 1 day.

Total: about 5 to 11 working days.

## Risks

Image breakage is the largest risk, especially in networking, data-structure, Linux course and machine-learning posts. Batch front matter edits can change category pages, tag pages and permalink behavior. Config edits can break build, theme behavior, deploy target or markdown-it anchors. Workflow edits can break GitHub Pages deployment. Directly moving course notes into Obsidian would create another archive rather than a usable knowledge base.

## Next Step

Start with a pilot extraction from `kv_cache.md`, `Reduction-规约.md`, and `cuda编程入门.md`, with 3 to 5 atomic notes from each. Validate note template, image strategy and backlinks before expanding to C++ and Systems.
