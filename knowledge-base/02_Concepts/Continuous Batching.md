---
type: concept
status: extracted
domain:
  - ai-infra
  - llm-inference
source:
  - blog
source_post:
  - "source/_posts/kv_cache.md"
created: 2026-08-09
---

# Continuous Batching

## 一句话

原文描述了一种按一次迭代或一个 token 生成作为最小单位进行调度的思路。

## 为什么需要

- Batch Decode 能提高算术强度，但请求长度和到达时间不同会带来 padding 和等待问题。
- 原文提出降低调度粒度，不再只按请求整体调度。

## 核心机制

- Batch Decode 把多个请求当前 token 组成 batch。
- 底层计算从 GEMV 变成 GEMM。
- 按 token/iteration 调度可以减少等待，但仍有 KV Cache 管理和长度不确定问题。

## 容易误解

- 原文没有直接使用 Continuous Batching 术语；本 note 名称来自迁移计划，需要人工确认。

## Related

- [[KV Cache]]
- [[PagedAttention]]

## Source

- `source/_posts/kv_cache.md`

自动抽取状态：从原博客中的标题、段落和代码说明压缩而来；未做外部资料补充。
