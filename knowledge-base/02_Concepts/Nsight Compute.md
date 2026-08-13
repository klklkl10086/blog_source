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

# Nsight Compute

## 一句话

Nsight Compute 用来深入分析单个 CUDA kernel 的性能原因，例如 memory、compute、occupancy 和 instruction 层面的瓶颈。

## 为什么需要

- GPU MODE 笔记把 ncu 用作回答“某一个 kernel 为什么慢”的工具。
- 当 PyTorch Profiler 或 nsys 已经定位到具体 kernel 后，需要 ncu 进一步判断优化方向。

## 核心机制

- 分析 memory 相关指标，判断访存是否成为瓶颈。
- 分析 compute 相关指标，判断计算吞吐是否被打满。
- 分析 occupancy，判断 SM 上是否有足够多 active warps 隐藏延迟。
- 分析 instruction，观察指令层面的执行特征。

## 容易误解

- ncu 的入口通常应是已被定位的目标 kernel；直接对整个程序做微观分析容易被无关 kernel 干扰。

## Related

- [[AI Infra Map]]
- [[CUDA Kernel Profiling]]
- [[Nsight Systems]]
- [[GPU Occupancy]]
- [[Streaming Multiprocessor]]

## Source

- `knowledge-base/GPU_MODE/Lesson01-04.md`

自动抽取状态：从 GPU MODE Lesson01-04 原始学习笔记整理而来；未做外部资料补充。
