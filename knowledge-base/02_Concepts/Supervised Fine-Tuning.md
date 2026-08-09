---
type: concept
status: extracted
domain:
  - llm
  - fine-tuning
source:
  - blog
source_post:
  - "source/_posts/Post-Training.md"
  - "source/_posts/从0实现LLM.md"
created: 2026-08-09
---

# Supervised Fine-Tuning

## 一句话

原文把 SFT 作为 Post-Training and Fine-Tuning 下的主题，并在 Transformer 文章中列出微调步骤。

## 为什么需要

- 微调用于把基础模型适配到特定任务或数据。

## 核心机制

- 准备任务数据集。
- 加载预训练模型和分词器。
- 配置微调参数。
- 执行训练。
- 评估与保存。

## 容易误解

- 原文只是学习笔记层面的步骤摘要；训练数据格式和评估标准需要人工审核。

## Related

- [[Transformer from Scratch]]
- [[RAG Pipeline]]

## Source

- `source/_posts/Post-Training.md`
- `source/_posts/从0实现LLM.md`

自动抽取状态：从原博客中的标题、段落和代码说明压缩而来；未做外部资料补充。
