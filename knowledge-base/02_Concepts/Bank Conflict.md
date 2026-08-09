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

# Bank Conflict

## 一句话

Bank Conflict 是同一 warp 中多个线程访问同一 shared-memory bank 的不同地址，导致访问串行化。

## 为什么需要

- 原文把它列为共享内存性能关键问题。
- Reduction 文章把 Bank Conflict 作为优化阶段之一。

## 核心机制

- 共享内存被划分为 32 个 bank。
- 同一地址可广播，无冲突。
- 访问同一 bank 的不同地址会增加延迟。
- 原文给出 padding/调整访问模式作为方向。

## 容易误解

- 访问同一地址和访问同一 bank 的不同地址不是一回事；原文明确前者可广播。

## Related

- [[Shared Memory]]
- [[Warp]]
- [[Parallel Reduction]]

## Source

- `source/_posts/cuda编程入门.md`
- `source/_posts/Reduction-规约.md`

自动抽取状态：从原博客中的标题、段落和代码说明压缩而来；未做外部资料补充。
