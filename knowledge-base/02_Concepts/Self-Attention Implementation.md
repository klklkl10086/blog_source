---
type: concept
status: extracted
domain:
  - llm
  - transformer
source:
  - blog
source_post:
  - "source/_posts/从0实现LLM.md"
created: 2026-08-09
---

# Self-Attention Implementation

## 一句话

原文的 TransformerBlock 中包含 multi-head attention、feedforward network、残差连接和 LayerNorm。

## 为什么需要

- 自注意力实现是从零实现 Transformer 的核心模块。

## 核心机制

- MultiHeadAttention 由多个 ScaledDotProductAttention head 组成。
- 多个 head 输出 concat 后经过 projection layer。
- TransformerBlock 中 attention 和 FFN 后接残差与 LayerNorm。

## 容易误解

- 原文中有 Post-LayerNorm 与 Pre-LayerNorm 对比；具体实现采用哪一种需要结合代码版本人工审核。

## Related

- [[Transformer from Scratch]]
- [[Tokenization Pipeline]]
- [[FlashAttention]]

## Source

- `source/_posts/从0实现LLM.md`

自动抽取状态：从原博客中的标题、段落和代码说明压缩而来；未做外部资料补充。
