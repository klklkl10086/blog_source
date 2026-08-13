---
type: concept
status: extracted
domain:
  - ai-infra
  - cuda
source:
  - gpu-mode
created: 2026-08-13
---

# Streaming Multiprocessor

## 一句话

Streaming Multiprocessor（SM）是 NVIDIA GPU 上执行 thread block 和 warp 的核心计算单元，内部包含 warp scheduler、register file、L1/shared memory 和多类执行 pipeline。

## 为什么需要

- GPU MODE Lesson04 把现代 GPU 理解为由大量 SM 组成、围绕数据吞吐设计的并行计算机器。
- CUDA 性能优化的核心问题之一，是有没有让足够多的 SM 持续工作。

## 核心机制

- CUDA runtime 会把 thread block 分配给不同 SM。
- 一个 block 被调度到某个 SM 后，其线程就在该 SM 上执行。
- SM 内可能同时 resident 多个 block 和多个 active warps。
- Warp scheduler 会不断选择 ready warp 发射指令，用其他 warp 的执行隐藏数据移动或依赖等待。
- SM 内部资源包括 register file、shared memory/L1、CUDA Core、Tensor Core、LD/ST units 和 SFU。

## 容易误解

- SM 不是只执行一个 thread 或一个 warp；它通过多个 resident block/warp 提供并行度和延迟隐藏。
- 让 SM 忙起来不仅取决于 block 数量，还会受到寄存器、shared memory、warp 数和具体 kernel 行为约束。

## Related

- [[AI Infra Map]]
- [[GPU Architecture]]
- [[Warp]]
- [[CUDA Thread Model]]
- [[GPU Occupancy]]
- [[CUDA Memory Hierarchy]]

## Source

- `knowledge-base/GPU_MODE/Lesson01-04.md`

自动抽取状态：从 GPU MODE Lesson01-04 原始学习笔记整理而来；未做外部资料补充。
