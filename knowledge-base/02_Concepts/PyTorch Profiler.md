---
type: concept
status: extracted
domain:
  - ai-infra
  - cuda
  - pytorch
source:
  - gpu-mode
created: 2026-08-13
---

# PyTorch Profiler

## 一句话

PyTorch Profiler 用来把 Python/PyTorch 程序中的 op 调用和对应的 CPU、CUDA 时间消耗列出来，帮助定位慢 op 和碎片化 kernel。

## 为什么需要

- GPU MODE 笔记用 `torch.profiler.profile()` 对手写 GELU 表达式做分析，发现多个逐元素 op 会发射多个 CUDA kernel。
- profiler 表可以帮助判断耗时来自 CPU 自身、CUDA 执行，还是大量小调用带来的调度开销。

## 核心机制

- `Self CPU` 表示该操作自身 CPU 时间，不包含子调用。
- `CPU total` 包含该操作自身和子调用的 CPU 时间。
- `Self CUDA` 表示该操作自身对应的 CUDA 执行时间。
- `CUDA time avg` 和 `# of Calls` 可用于识别小 kernel 是否过多。
- `aten::mul`、`aten::add`、`aten::tanh`、`aten::pow` 等是 PyTorch 算子层，下面还会对应真正的 CUDA kernel。

## 容易误解

- `aten::*` 行不是硬件执行的最终形态；它们可能通过 `cudaLaunchKernel` 发射底层 CUDA kernel。
- profiling 本身和 kernel launch 都可能带来 CPU 侧开销，尤其在微小逐元素 kernel 上更明显。

## Related

- [[AI Infra Map]]
- [[CUDA Kernel Profiling]]
- [[CUDA Kernel Launch Overhead]]
- [[Operator Fusion]]

## Source

- `knowledge-base/GPU_MODE/Lesson01-04.md`

自动抽取状态：从 GPU MODE Lesson01-04 原始学习笔记整理而来；未做外部资料补充。
