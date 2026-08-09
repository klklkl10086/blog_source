---
type: concept
status: extracted
domain:
  - cpp
  - systems
source:
  - blog
source_post:
  - "source/_posts/cpp11-多线程.md"
created: 2026-08-09
---

# C++ Thread Basics

## 一句话

原文围绕 `std::thread`、`join`、`detach`、`joinable`、mutex、lock_guard、unique_lock 和 call_once 展开。

## 为什么需要

- 多线程是 C++ 系统编程和服务端程序的基础。

## 核心机制

- `std::thread` 创建线程。
- `join()` 等待线程结束。
- `detach()` 分离线程。
- `joinable()` 判断线程是否可 join。
- mutex 用于保护临界区。
- lock_guard 和 unique_lock 用于管理锁。

## 容易误解

- 原文单独写了互斥量死锁，说明多锁顺序和锁管理需要人工审核。

## Related

- [[C++ Move Semantics]]
- [[Linux File Descriptor]]

## Source

- `source/_posts/cpp11-多线程.md`

自动抽取状态：从原博客中的标题、段落和代码说明压缩而来；未做外部资料补充。
