---
type: concept
status: extracted
domain:
  - llm
  - project
source:
  - blog
source_post:
  - "source/_posts/从0实现LLM.md"
  - "source/_posts/LLM-1-to-N.md"
created: 2026-08-09
---

# Transformer from Scratch

## 一句话

原文实现的是 decoder 结构的 Transformer，并包含数据读取、tokenize、模型、loss、训练、保存和生成流程。

## 为什么需要

- 该文章是从实现角度理解 Transformer 的主来源。
- 原文后续还补充了 LayerNorm、微调和 decoding strategies。

## 核心机制

- 读取文本数据。
- 把文本编码为 tokenized_text。
- 定义 TransformerBlock 和 TransformerLanguageModel。
- 计算 loss、训练、保存模型并生成文本。

## 容易误解

- 原文明确实现的是 decoder 结构而非原始 encode-decode Transformer。

## Related

- [[Tokenization Pipeline]]
- [[Self-Attention Implementation]]
- [[FlashAttention]]

## Source

- `source/_posts/从0实现LLM.md`
- `source/_posts/LLM-1-to-N.md`

自动抽取状态：从原博客中的标题、段落和代码说明压缩而来；未做外部资料补充。
