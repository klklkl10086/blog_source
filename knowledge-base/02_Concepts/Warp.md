---
type: concept
status: extracted
domain:
  - ai-infra
  - cuda
source:
  - blog
source_post:
  - "source/_posts/cuda编程入门.md"
  - "source/_posts/Reduction-规约.md"
created: 2026-08-09
---

# Warp

## 一句话

Warp 是原文中反复出现的 GPU 线程束粒度，包含 32 个线程，是硬件执行和指令分发的重要单位。

## 为什么需要

- 原文用 Warp 解释合并访存、Bank Conflict、Warp Divergence 和 Reduction 优化。
- CUDA 线程模型只有理解到 Warp 粒度，才能解释为什么某些分支和访存模式会慢。

## 核心机制

- 原文描述 Warp 包含 32 个线程。
- 当 Warp 内线程访问连续地址时，全局内存访问可以合并。
- `if-else` 可能导致 Warp Divergence，使线程轮流执行。
- Shuffle 优化允许同一个 Warp 内线程直接读取彼此寄存器数据。

## 容易误解

- 原文强调硬件执行和调度常以 Warp 为单位，不应只从单个线程理解性能。
- Warp 相关细节仍需结合具体 CUDA 架构人工审核。

## Related

- [[CUDA Thread Model]]
- [[Global Memory Coalescing]]
- [[Bank Conflict]]
- [[Parallel Reduction]]

## Source

- `source/_posts/cuda编程入门.md`
- `source/_posts/Reduction-规约.md`

自动抽取状态：从原博客中的标题、段落和代码说明压缩而来；未做外部资料补充。
