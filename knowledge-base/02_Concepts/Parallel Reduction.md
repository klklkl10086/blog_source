---
type: concept
status: extracted
domain:
  - ai-infra
  - cuda
source:
  - blog
source_post:
  - "source/_posts/Reduction-规约.md"
  - "source/_posts/cuda编程入门.md"
created: 2026-08-09
---

# Parallel Reduction

## 一句话

Reduction 文章围绕求和规约，从 global memory baseline 逐步优化到 shared memory、减少分歧、减少同步、循环展开和 shuffle。

## 为什么需要

- 原文用 Reduction 作为 CUDA kernel 优化练习。
- 它暴露访存、Warp Divergence、Bank Conflict、idle 线程和同步开销。

## 核心机制

- Reduction 0 使用 global memory。
- Reduction 1 改用 shared memory。
- 后续优化包括集中工作的线程、减少 bank conflict、展开最后一维、完全展开循环、设置 block 数量和 shuffle。

## 容易误解

- 原文中还保留了错误尝试和修正，需要人工审核代码版本再形成可运行实验。

## Related

- [[Shared Memory]]
- [[Bank Conflict]]
- [[Global Memory Coalescing]]

## Source

- `source/_posts/Reduction-规约.md`
- `source/_posts/cuda编程入门.md`

自动抽取状态：从原博客中的标题、段落和代码说明压缩而来；未做外部资料补充。
