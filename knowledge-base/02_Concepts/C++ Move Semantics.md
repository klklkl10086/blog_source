---
type: concept
status: extracted
domain:
  - cpp
source:
  - blog
source_post:
  - "source/_posts/cpp11新特性.md"
created: 2026-08-09
---

# C++ Move Semantics

## 一句话

移动语义通过右值引用和移动构造/移动赋值，把临时对象资源从源对象转移到目标对象，避免深拷贝。

## 为什么需要

- 原文指出 C++11 之前处理临时对象可能触发昂贵深拷贝。
- 右值引用使程序能接管临时对象资源。

## 核心机制

- 右值引用使用 `&&`。
- `std::move` 不在运行时移动，只在编译期做类型转换。
- 右值引用变量本身有名字，因此它是左值。
- 完美转发用 `std::forward<T>()` 保持参数左右值属性。

## 容易误解

- 原文特别强调 `std::move` 本身不执行移动操作。

## Related

- [[C++ Thread Basics]]
- [[Socket API]]

## Source

- `source/_posts/cpp11新特性.md`

自动抽取状态：从原博客中的标题、段落和代码说明压缩而来；未做外部资料补充。
