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
created: 2026-08-09
---

# Tokenization Pipeline

## 一句话

原文用 `encoding.encode(text)` 得到 `tokenized_text`，再转为 tensor，并按比例切分 train/valid 数据。

## 为什么需要

- 训练语言模型前需要把文本转成 token 序列。
- 原文用 token 最大值推导词表大小。

## 核心机制

- 读取文本。
- 编码为 tokenized_text。
- 转换为 torch tensor。
- 按 0.9 比例划分 train_data 和 valid_data。

## 容易误解

- 原文没有展开 tokenizer 算法本身；这里只保留实现流程。

## Related

- [[Transformer from Scratch]]
- [[Self-Attention Implementation]]

## Source

- `source/_posts/从0实现LLM.md`

自动抽取状态：从原博客中的标题、段落和代码说明压缩而来；未做外部资料补充。
