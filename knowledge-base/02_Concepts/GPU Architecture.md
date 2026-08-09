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
created: 2026-08-09
---

# GPU Architecture

## 一句话

原文把 CUDA 软件层级和 GPU 硬件层级对应起来：Thread、Warp、Thread Block 与硬件调度和存储层级相关。

## 为什么需要

- 理解 GPU 架构是理解 CUDA 线程、内存、同步和性能问题的前提。

## 核心机制

- Warp 是硬件执行和指令分发的最小基本单位。
- Thread Block 内线程共享片上共享内存。
- SM/调度器负责执行线程束。

## 容易误解

- 原文强调硬件认识 Warp，不是单个线程；更细硬件细节待人工审核。

## Related

- [[CUDA Thread Model]]
- [[Warp]]
- [[CUDA Memory Hierarchy]]

## Source

- `source/_posts/cuda编程入门.md`

自动抽取状态：从原博客中的标题、段落和代码说明压缩而来；未做外部资料补充。
