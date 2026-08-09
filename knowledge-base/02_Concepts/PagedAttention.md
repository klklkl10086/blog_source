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

# PagedAttention

## 一句话

PagedAttention 借鉴虚拟内存思想，把显存划分成等大块，并用块表管理 KV Cache 的逻辑到物理映射。

## 为什么需要

- 原文指出连续静态分配会造成内部/外部碎片。
- 连续静态分配也不利于复杂解码策略中的 KV Cache 共享。
- 显存管理限制 batch decode 并行数量。

## 核心机制

- 把显存空间分成大小相等的块。
- 每个请求分配若干块。
- 用块表记录和管理请求的显存分配。
- 通过修改块表可以实现 KV Cache 块共享。

## 容易误解

- 原文只抽取了思想层级；具体 block table 数据结构和 kernel 实现需要人工审核。

## Related

- [[KV Cache]]
- [[Continuous Batching]]
- [[Linux File Descriptor]]

## Source

- `source/_posts/kv_cache.md`

自动抽取状态：从原博客中的标题、段落和代码说明压缩而来；未做外部资料补充。
