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

# Operator Fusion

## 一句话

Operator Fusion 是把多个相邻操作合并到一个 kernel 或执行单元里，以减少 kernel launch、中间内存读写和逐元素操作碎片化。

## 为什么需要

- GPU MODE 笔记把“融合多个操作到一个操作”作为 memory access bottleneck 下的重要优化思路。
- 手写 GELU 表达式会产生 `mul`、`add`、`tanh`、`pow` 等多个逐元素 op，导致多个小 kernel 和中间结果访问。

## 核心机制

- 将多个 elementwise 操作融合，可以减少 CUDA kernel launch 次数。
- 融合后可减少中间张量写回 global memory 再读出的成本。
- 对 memory-bound 逐元素表达式，减少数据搬运通常比单纯增加算术吞吐更关键。

## 容易误解

- fusion 不是所有瓶颈的答案；如果单个融合 kernel 内部已经受寄存器压力、访存模式或 occupancy 限制，还需要继续用 profiler 分析。

## Related

- [[AI Infra Map]]
- [[CUDA Kernel Launch Overhead]]
- [[PyTorch Profiler]]
- [[CUDA Memory Hierarchy]]
- [[CUDA Kernel Profiling]]

## Source

- `knowledge-base/GPU_MODE/Lesson01-04.md`

自动抽取状态：从 GPU MODE Lesson01-04 原始学习笔记整理而来；未做外部资料补充。
