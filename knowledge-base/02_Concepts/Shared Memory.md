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

# Shared Memory

## 一句话

Shared Memory 是同一线程块内线程共享的片上存储，原文用它解决 Reduction 0 的全局内存访存问题。

## 为什么需要

- 原文把共享内存用于数据复用、规约和降低全局内存访问。
- 在 Reduction 中，把数据搬到共享内存后再做块内求和。

## 核心机制

- 用 `__shared__` 声明共享内存。
- 线程把全局内存中的数据写入 `shared[threadIdx.x]`。
- 使用 `__syncthreads()` 等待线程块内数据加载完成。

## 容易误解

- 原文指出共享内存仍可能遇到 Bank Conflict；不是使用 shared memory 就一定高效。

## Related

- [[Parallel Reduction]]
- [[Bank Conflict]]
- [[CUDA Memory Hierarchy]]

## Source

- `source/_posts/cuda编程入门.md`
- `source/_posts/Reduction-规约.md`

自动抽取状态：从原博客中的标题、段落和代码说明压缩而来；未做外部资料补充。
