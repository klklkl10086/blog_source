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

# KV Cache

## 一句话

KV Cache 缓存 decode 阶段会重复用到的 K、V，从而复用之前的计算结果并提升推理速度。

## 为什么需要

- Transformer 推理分为 Prefill 和 Decode。
- Decode 阶段会把新生成 token 和 prompt 合并后反复计算。
- 原文由此提出缓存 K、V 的必要性。

## 核心机制

- Prefill 计算 prompt 直到生成第一个 token。
- Decode 自回归生成，每一步会用到历史 K、V。
- 缓存 K、V 后，问题转向如何高效管理显存中的 KV Cache。

## 容易误解

- 原文强调 KV Cache 管理难点来自不确定大小和不确定生命周期。

## Related

- [[PagedAttention]]
- [[Rolling KV Cache]]
- [[Continuous Batching]]

## Source

- `source/_posts/kv_cache.md`

自动抽取状态：从原博客中的标题、段落和代码说明压缩而来；未做外部资料补充。
