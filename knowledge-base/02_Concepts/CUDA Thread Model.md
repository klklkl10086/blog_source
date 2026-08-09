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

# CUDA Thread Model

## 一句话

CUDA 线程模型用 Grid、Block、Thread 组织并行任务，原文用 `threadIdx`、`blockIdx`、`blockDim` 计算全局线程编号。

## 为什么需要

- 把数据拆给不同线程处理，是从 C++ 代码转向 CUDA kernel 的基础。
- 原文的一维和多维线程例子都围绕线程索引计算展开。

## 核心机制

- 线程在线程块内有 `threadIdx`。
- 线程块在网格内有 `blockIdx`。
- 常见一维全局索引是 `blockIdx.x * blockDim.x + threadIdx.x`。

## 容易误解

- 原文强调多维线程也要转换为全局索引；具体维度映射需要人工审核后再拆。

## Related

- [[GPU Architecture]]
- [[Warp]]
- [[Shared Memory]]

## Source

- `source/_posts/cuda编程入门.md`

自动抽取状态：从原博客中的标题、段落和代码说明压缩而来；未做外部资料补充。
