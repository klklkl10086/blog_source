---
title: RAG初步
date: 2026-07-10 22:57:24
tags: ["LLM","Agent","RAG"]
categories: ["Agent"]
---

一个标准的 RAG 流程主要分为三个阶段：数据准备（离线）、检索（在线）、生成（在线）。
1. 数据准备：离线进行建库，对文档进行解析、清洗、切分、向量化、索引
2. 检索：对query处理、进行召回、rerank（optional）
3. 生成：搜索到的资料+问题拼接为prompt，发送给LLM，让LLM进行回答

# 数据准备
1. 文档解析与提取
2. 切片
3. 向量化并建立索引

## 文档解析与提取

**成熟的处理方案：**
1. 文档路由
2. 分类型解析（Parser）
3. 统一中间结构

即：
```
文件
 ↓
MIME / 文档质量识别
 ↓
Document Router
 ├─ PDF Parser
 ├─ Office Parser
 ├─ Spreadsheet Parser
 ├─ HTML Parser
 ├─ OCR / Layout Parser
 └─ Image / Multimodal Parser
 ↓
统一 Document AST / JSON
 ↓
清洗、结构恢复
 ↓
Chunk
 ↓
Embedding / Index
```
**常见文档处理方式：**
| 类型             | 主要难点            | 推荐处理方式                          |
| -------------- | --------------- | ------------------------------- |
| TXT / Markdown | 结构简单            | 原生解析，保留标题层级                     |
| HTML / 网页      | 导航、广告、DOM 噪声    | DOM 清洗，保留 heading/list/table    |
| DOCX           | 标题、段落、表格、图片     | 基于 OOXML 结构解析                   |
| PPTX           | 页面语义、文本框顺序、图表   | 按 Slide 解析，恢复元素位置关系             |
| XLSX / CSV     | 行列语义、合并单元格、公式   | 表结构解析，不要普通文本切块                  |
| 文本型 PDF        | 阅读顺序、多栏、页眉页脚    | Layout-aware 解析                 |
| 扫描 PDF         | 无文本层、倾斜、低清晰度    | OCR + Layout Analysis           |
| 图片             | OCR 信息和视觉信息并存   | OCR + VLM/Image Caption         |
| 技术/论文 PDF      | 公式、表格、多栏、引用     | Layout + Formula + Table Parser |
| 邮件             | Thread、引用、签名、附件 | 邮件结构解析 + Thread 重建              |
| JSON / XML     | 层级结构            | Schema-aware 展开                 |
| 代码             | 函数、类、模块依赖       | AST / Symbol-aware 切分           |

`Docling` 当前支持 PDF、DOCX、XLSX、PPTX、OpenDocument、Markdown、HTML、CSV 和多种图片格式，并统一转换为结构化文档表示。

`Apache Tika` 的定位则更偏向大范围文件类型检测、元数据和文本提取。

### TXT（纯文本）
- 缺点：缺乏结构化元数据，无法辨别正文和标题
- 优点：无排版，简单干净

一般选择换行符（段落）、句号问号感叹号（句子）、字词进行切分，如果文本内容毫无标点，则就按照规定的字符长度进行切分
滑动窗口（overlap），在切分时设置重叠区，保障上下文连接

### Markdown（富文本）
特点：自带语义层级结构

一般不按照token的大小进行死板切分，而是按照标题结构进行拆分，例如：
```
# 一级标题
  ## 二级标题
    ### 三级标题
      paragraph
      list
      code
```
可以解析为：
```
{
  "title": "模型部署",
  "section_path": [
    "部署文档",
    "模型部署",
    "GPU配置"
  ],
  "content": "...",
  "element_type": "paragraph"
}
```
需要保留`标题路径`
在进行chunk时就需要保留标题路径以及内容

对于特殊的区块，比如代码块、公式块、表格等，要完整提取：
- **代码块**： 通过识别md格式，将代码块完整提取
-  **表格**：使用Markdown 表格（`|---|---|`），或者将每一行转换为“键值对”的文本描述（例如：“`在[XX模型]配置下，[显存]的参数是[24GB]`”），再进行向量化，也可以转换为html格式。
-  **超链接与图片**：通常用正则表达式清洗掉图片标签 `![alt](url)`，防止无意义的 URL 干扰文本 Embedding；对于超链接 `[说明](url)`，保留中括号内的说明文字，剔除背后的链接。


# 检索



# 生成