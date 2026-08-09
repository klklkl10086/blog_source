---
type: concept
status: extracted
domain:
  - systems
  - linux
  - cpp
source:
  - blog
source_post:
  - "source/_posts/CPP网络编程基础.md"
created: 2026-08-09
---

# Socket API

## 一句话

原文把 Linux C++ 网络服务端流程概括为创建 socket、bind、listen、accept 以及 recv/send。

## 为什么需要

- Socket API 是 C++ 网络编程基础。

## 核心机制

- `socket()` 创建通信端点。
- `bind()` 绑定地址。
- `listen()` 进入监听。
- `accept()` 接受连接。
- `recv`/`send` 进行数据收发。
- `AF_INET`、`SOCK_STREAM`、`SOCK_DGRAM` 分别出现在原文参数解释中。

## 容易误解

- 原文还区分 PF/AF、TCP/UDP 等参数语义，需要后续人工拆分。

## Related

- [[Linux File Descriptor]]
- [[C++ Thread Basics]]

## Source

- `source/_posts/CPP网络编程基础.md`

自动抽取状态：从原博客中的标题、段落和代码说明压缩而来；未做外部资料补充。
