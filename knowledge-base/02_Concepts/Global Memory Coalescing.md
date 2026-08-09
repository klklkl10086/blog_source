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

# Global Memory Coalescing

## 一句话

合并访存指 warp 内线程访问连续地址时，硬件可把访问合并成少量内存事务。

## 为什么需要

- 原文把全局内存访问效率和 memory transaction 数量直接关联。
- Reduction 0 使用 global memory 会产生大量显存访问请求。

## 核心机制

- 当 Warp 内 32 个线程访问连续地址时，硬件只需少量事务。
- 地址散乱时可能触发多次独立事务，有效带宽下降。

## 容易误解

- 原文只说明了连续访问和散乱访问的性能差异；具体事务大小与架构关系需要人工审核。

## Related

- [[Warp]]
- [[Parallel Reduction]]
- [[CUDA Memory Hierarchy]]

## Source

- `source/_posts/cuda编程入门.md`
- `source/_posts/Reduction-规约.md`

自动抽取状态：从原博客中的标题、段落和代码说明压缩而来；未做外部资料补充。
