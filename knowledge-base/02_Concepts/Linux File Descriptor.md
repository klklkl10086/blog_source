---
type: concept
status: extracted
domain:
  - systems
  - linux
source:
  - blog
source_post:
  - "source/_posts/CPP网络编程基础.md"
  - "source/_posts/Linux环境编程.md"
created: 2026-08-09
---

# Linux File Descriptor

## 一句话

原文在文件 IO 与 socket API 中都把 fd/sockfd 作为系统调用操作对象，打开文件或创建 socket 成功会返回非负整数描述符。

## 为什么需要

- Linux 文件、目录、网络 socket 操作都围绕系统调用和返回值/errno 展开。
- 网络编程中 `socket()` 返回的 `sockfd` 继续传给 bind/listen/accept/send/recv 等接口。

## 核心机制

- `open()` 成功返回文件描述符，失败返回 -1 并设置 errno。
- `write(int fd, ...)` 和 `read(int fd, ...)` 使用 fd。
- `socket()` 创建通信端点并返回 sockfd。

## 容易误解

- 原文强调必须先检查返回值，再使用 errno；不能假设成功会清零 errno。

## Related

- [[Socket API]]
- [[C++ Thread Basics]]

## Source

- `source/_posts/CPP网络编程基础.md`
- `source/_posts/Linux环境编程.md`

自动抽取状态：从原博客中的标题、段落和代码说明压缩而来；未做外部资料补充。
