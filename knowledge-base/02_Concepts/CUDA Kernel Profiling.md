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

# CUDA Kernel Profiling

## 一句话

CUDA kernel profiling 是从 PyTorch op、CPU/GPU 时间线和单个 kernel 微观指标逐层定位性能瓶颈的过程。

## 为什么需要

- GPU MODE Lesson 1 把 profiling 放在自定义 kernel 之前：先发现慢的 kernel，再理解为什么慢，最后改写或融合 kernel。
- 仅看 Python 代码无法判断慢点来自 CPU launch、kernel 排队、内存访问、计算吞吐还是 occupancy。

## 核心机制

- [[PyTorch Profiler]] 用来回答哪个 PyTorch op 或 CUDA kernel 慢。
- [[Nsight Systems]] 用来观察 CPU 和 GPU 在时间轴上的调度、空洞和 launch 频率。
- [[Nsight Compute]] 用来分析单个 kernel 的 memory、compute、occupancy 和 instruction 指标。
- 分析路径可以从 Python/PyTorch 一直向下追到 CUDA runtime、CUDA kernel、PTX、SASS 和 GPU hardware。

## 容易误解

- profiler 表里的 PyTorch op 不一定就是最终跑在 GPU 上的 kernel；真实执行层可能是 `vectorized_elementwise_kernel` 等 CUDA kernel。
- 小 kernel 的实际 GPU 计算时间可能很短，整体耗时却被 CPU 侧 profiler/launch 开销放大。

## Related

- [[AI Infra Map]]
- [[PyTorch Profiler]]
- [[Nsight Systems]]
- [[Nsight Compute]]
- [[CUDA Kernel Launch Overhead]]
- [[Operator Fusion]]

## Source

- `knowledge-base/GPU_MODE/Lesson01-04.md`

自动抽取状态：从 GPU MODE Lesson01-04 原始学习笔记整理而来；未做外部资料补充。
