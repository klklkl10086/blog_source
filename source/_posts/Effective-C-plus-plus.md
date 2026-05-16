---
title: Effective C plus plus
date: 2026-05-16 21:10:10
tags: ["CPP"]
typora-root-url: ./Effective-C-plus-plus
---

> 又一次试图阅读并理解《Effective C++》 

# 条款01:视C++为一个语言联邦

**C++:**

- C
- C++面向对象
- template 泛型编程
- STL



# 条款02:尽量以`const`、`enum`、`inline`替换`#define`

> 即让预处理的活尽量转移给编译器

## 指针

```cpp
const char* const str [] ="effective c plus plus";
```

定义为string更好

```cpp
const std::string str("effective c plus plus");
```



## 类

相对于`define`不重视作用域，`const`可以在类中修饰类的成员



## enum hack

> 一个属于枚举类型的变量可以被当做`int`使用

优秀的编译器不会为 **整数类型常量**分配另外的存储空间（除非**创建指针或者引用**指向这个变量），但是并非所有编译器都是如此，enum hack类似于`define`，二者都**不可以取地址**，可以**阻止取地址**这种行为



## 宏定义函数

> 转换为`template inline 函数`

```c
#define CALL_WITH_MAX(a,b) f((a)>(b) ? (a) : (b))
```

转换为

```cpp
template<typename T>
inline void callWithMax(const  T& a,const T& b)
{
	f(a>b ? a:b);
}
```



# 条款03:尽可能使用`const`

> 只要某值不变是事实，就应该使用`const`，从而获得编译器的帮助，建立约束
>
> 对于编译器，`const`是***physical***，但是我们书写代码应该保证是***logical***

## 指针



## 函数





## 成员函数
