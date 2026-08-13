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

# CUDA Kernel Launch Overhead

## 一句话

CUDA kernel launch overhead 是 CPU 侧发射 GPU kernel 的调度成本；当程序由大量很小的 kernel 组成时，它可能比真正 GPU 计算更显眼。

## 为什么需要

- GPU MODE 的 GELU 例子里，手写 PyTorch 表达式会触发多个逐元素 kernel。
- 笔记观察到 GPU 真正计算时间约为微秒级，但 CPU 侧 profiler/launch 等开销明显更大。

## 核心机制

- Python/PyTorch 调用会进入 CUDA runtime，再通过 `cudaLaunchKernel` 发射底层 CUDA kernel。
- 每个 `aten::*` 逐元素 op 都可能变成一次独立 kernel launch。
- 当单个 kernel 很小，launch 次数过多会造成碎片化，GPU 时间线也可能出现空洞。

## 容易误解

- GPU kernel 本身快不代表整体表达式快；多个小 kernel 的 launch、同步和中间张量读写会一起影响性能。

## Related

- [[AI Infra Map]]
- [[PyTorch Profiler]]
- [[Nsight Systems]]
- [[Operator Fusion]]
- [[CUDA Kernel Profiling]]

## Source

- `knowledge-base/GPU_MODE/Lesson01-04.md`

自动抽取状态：从 GPU MODE Lesson01-04 原始学习笔记整理而来；未做外部资料补充。
