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

# GPU Occupancy

## 一句话

GPU occupancy 描述 SM 上可同时驻留并参与调度的活跃 warp/block 程度，是判断能否隐藏延迟和保持 SM 工作的重要指标之一。

## 为什么需要

- GPU MODE 笔记在 ncu 分析项中列出 occupancy，并在 SM 章节强调 active warps 和 resident blocks。
- 当部分 warp 等待内存或依赖时，足够的 ready warp 可以让 SM 继续发射其他指令。

## 核心机制

- 一个 thread block 会被调度到某个 SM 上执行。
- 一个 SM 上可能同时 resident 多个 block。
- 每个 block 包含多个 warp，例如 256 threads 可以拆成 8 个 warp。
- active warps 越多，warp scheduler 越可能找到 ready warp 来隐藏等待。

## 容易误解

- occupancy 高不自动等于性能高；它只是判断延迟隐藏能力的一个指标，仍需结合 memory、compute 和 instruction 指标看瓶颈。

## Related

- [[AI Infra Map]]
- [[Streaming Multiprocessor]]
- [[Warp]]
- [[Nsight Compute]]
- [[CUDA Kernel Profiling]]

## Source

- `knowledge-base/GPU_MODE/Lesson01-04.md`

自动抽取状态：从 GPU MODE Lesson01-04 原始学习笔记整理而来；未做外部资料补充。
