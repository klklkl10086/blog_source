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

# Nsight Systems

## 一句话

Nsight Systems 用时间线视角观察 CPU 与 GPU 的调度关系，适合定位 kernel 之间的空洞、频繁 launch 和 CPU/GPU 并行度问题。

## 为什么需要

- GPU MODE 笔记把 nsys 放在 PyTorch Profiler 之后，用来回答 CPU 和 GPU 在时间轴上如何调度。
- 当程序慢不是由单个 kernel 内部造成时，nsys 能帮助观察 GPU 是否在等待 CPU 发射任务。

## 核心机制

- 观察 kernel 之间有没有空洞。
- 观察 launch 是否过于频繁。
- 观察 CPU 工作和 GPU 工作是否形成有效流水。

## 容易误解

- nsys 更偏系统级时间线，不是分析某一个 kernel 为什么 memory-bound 或 compute-bound 的主要工具。

## Related

- [[AI Infra Map]]
- [[CUDA Kernel Profiling]]
- [[Nsight Compute]]
- [[CUDA Kernel Launch Overhead]]

## Source

- `knowledge-base/GPU_MODE/Lesson01-04.md`

自动抽取状态：从 GPU MODE Lesson01-04 原始学习笔记整理而来；未做外部资料补充。
