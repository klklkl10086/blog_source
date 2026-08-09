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

# CUDA Memory Hierarchy

## 一句话

CUDA 内存模型包含寄存器、本地内存、共享内存、全局内存、常量内存、纹理内存以及 L1/L2 缓存。

## 为什么需要

- 原文把内存层次作为 CUDA 性能理解的核心部分。
- 不同内存有不同作用域、生命周期、延迟和带宽。

## 核心机制

- 寄存器是线程私有的最快存储单元。
- 共享内存由同一线程块内线程共享。
- 全局内存容量最大但延迟高。
- 常量内存在 warp 内访问同一地址时可广播。

## 容易误解

- 原文只抽取了各类内存的性质；具体容量和架构差异需要人工审核。

## Related

- [[Shared Memory]]
- [[Global Memory Coalescing]]
- [[Bank Conflict]]

## Source

- `source/_posts/cuda编程入门.md`

自动抽取状态：从原博客中的标题、段落和代码说明压缩而来；未做外部资料补充。
