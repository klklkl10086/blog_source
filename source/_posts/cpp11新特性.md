---
title: cpp11新特性
date: 2026-03-12 21:58:36
tags: ["CPP"]
categories: ["CPP开发"]
description: CPP11常用的特性
---

> 参考资料:
>
> [c++11实用特性]( https://www.bilibili.com/video/BV1bX4y1G7ks/?share_source=copy_web&vd_source=777aaa8a415b68222e598d976e64642c)
>
> 《C++ Primer Plus》
>
> deepseek

# 原始字面量

在 C++11 标准中，引入了**原始字面量**（Raw String Literal），用于简化字符串中反斜杠 `\` 和引号 `"` 等特殊字符的处理。它让字符串内容可以“原样”呈现，无需转义，特别适合正则表达式、文件路径、多行文本等场景。

### 基本语法

原始字面量的格式为：

```cpp
R"delimiter(raw_characters)delimiter"
```

- `R` 表示原始字面量前缀。
- `delimiter` 是可选的**定界符序列**（长度不超过 16 个字符的自定义字符序列，不能包含反斜杠、空格和括号）用于唯一标识字符串的结束位置。当字符串内容本身包含 `)"` 时，避免编译器误认为字面量提前结束。
- `( raw_characters )` 中是真正的字符串内容，可以包含任何字符（包括换行、引号、反斜杠等），**无需转义**。

如果省略定界符，简写为 `R"(...)"`。

### 关键特性

- **不处理转义序列**：例如 `\n`、`\t`、`\"` 等均作为普通字符对待。
- **允许换行**：字符串可以直接跨越多行，换行符会被保留为字符串的一部分。
- **允许引号**：无需转义即可包含 `"` 字符。
- **允许反斜杠**：`\` 就是普通反斜杠，不会引起转义。

### 示例

#### 普通字符串 vs 原始字面量

```cpp
#include <iostream>
#include <string>

int main() {
    // 普通字符串：需要转义反斜杠和引号
    std::string normal = "C:\\Program Files\\\"MyApp\"";
    
    // 原始字面量：无需转义
    std::string raw = R"(C:\Program Files\"MyApp")";
    
    std::cout << "Normal: " << normal << std::endl;
    std::cout << "Raw:    " << raw << std::endl;
    // 两者输出相同： C:\Program Files\"MyApp"
}
```

#### 多行字符串

```cpp
std::string multi = R"(第一行
第二行
第三行)";

std::cout << multi;
// 输出：
// 第一行
// 第二行
// 第三行
```

#### 包含括号的情况（使用定界符）

如果字符串本身包含 `)"` 序列，就需要自定义定界符来避免歧义。

```cpp
// 字符串内容为：Hello )" World
// 不加定界符会提前结束：R"(Hello )" World)"  ← 错误，第一个 )" 就结束了字面量

std::string with_delim = R"delim(Hello )" World)delim";
// 正确，定界符 delim 使编译器正确匹配结束符 )delim"
```

#### 正则表达式场景

正则表达式中经常出现大量反斜杠，原始字面量可以显著提高可读性。

```cpp
#include <regex>
#include <string>

// 匹配形如 \d{3}-\d{4} 的电话号码
std::regex phone_normal("\\d{3}-\\d{4}");   // 需要双重转义
std::regex phone_raw(R"(\d{3}-\d{4})");      // 更清晰
```

#### 文件路径

```cpp
std::string path = R"(C:\Users\Name\Documents\file.txt)";
// 等价于 "C:\\Users\\Name\\Documents\\file.txt"
```

### 注意事项

- 原始字面量中唯一需要留意的字符是 **`)"`** 序列（如果未使用定界符）或 **`)delimiter"`**（如果使用了定界符）。只要字符串内容不包含该精确序列，就可以安全使用。
- 定界符可以是任意可见字符（除了反斜杠、空格和括号），通常使用一个短单词或下划线，如 `R"tag(...)tag"`。
- 原始字面量仍然是标准 `std::string`（或字符数组），与普通字符串字面量完全兼容。
- 原始字面量也支持宽字符、UTF-8/16/32 前缀，例如 `u8R"(...)"`、`LR"(...)"` 等。





# nullptr

`nullptr` 代表一个**空指针字面量**（null pointer literal）。它的类型是 `std::nullptr_t`（定义在 `<cstddef>` 中），可以隐式转换为任意指针类型或成员指针类型，但**不能转换为整数类型**。

## 作用

在 C++11 之前，程序员通常用 `NULL` 或直接使用 `0` 表示空指针。例如：

```cpp
int* p = NULL;   // NULL 通常被定义为 0 或 (void*)0
int* q = 0;
```

这种做法存在两个主要问题：

- **类型模糊**：`NULL` 本质上是整数 0（或 `(void*)0`），在函数重载时会导致意外行为。
- **与整数混用**：由于 0 既可以表示整数也可以表示空指针，编译器在重载决议时可能选择错误的版本。

例如，考虑以下重载：

```cpp
void func(int);
void func(char*);

func(NULL);   // 调用 func(int) 还是 func(char*)？
```

在不同的实现中，`NULL` 可能是 `0` 或 `0L`，因此调用 `func(NULL)` 会匹配到 `func(int)`，而不是预期的 `func(char*)`，造成逻辑错误。

## `nullptr` 的类型与特性

- `nullptr` 的类型是 `std::nullptr_t`（可视为一种特殊的“指针类型”）。
- `std::nullptr_t` 的实例（如 `nullptr`）可以隐式转换为**任何指针类型**（包括成员指针）和 `bool` 类型（转换为 `false`）。
- `nullptr` **不能**隐式转换为整数类型（如 `int`、`long` 等）。
- 所有类型为 `std::nullptr_t` 的对象（实际上只有 `nullptr` 是标准定义的）彼此相等，且与任何空指针值相等。

##  使用示例

### 基本用法

```cpp
int* p = nullptr;        // 指向 int 的空指针
double* q = nullptr;     // 指向 double 的空指针
void (*fp)() = nullptr;  // 函数指针空值

if (p == nullptr) {      // 与 nullptr 比较
    // p 为空
}
```

### 解决重载歧义

```cpp
void func(int) { std::cout << "int version\n"; }
void func(char*) { std::cout << "char* version\n"; }

func(0);      // 调用 func(int)
func(NULL);   // 可能调用 func(int) （取决于 NULL 的定义）
func(nullptr); // 一定调用 func(char*) —— 因为 nullptr 只能匹配指针
```

### 与模板配合

```cpp
template<typename T>
void foo(T* ptr) {
    if (ptr == nullptr) {
        // 安全的空指针检查
    }
}

foo(nullptr); // 推导 T 为某个类型，但实际不实例化对象
```

## `nullptr` 与 `NULL` 的对比

| 特性               | `nullptr`        | `NULL`                         |
| ------------------ | ---------------- | ------------------------------ |
| 类型               | `std::nullptr_t` | 整数（通常为 `int` 或 `long`） |
| 可转换为指针       | 是（隐式）       | 是（通过整数转换）             |
| 可转换为整数       | 否               | 是                             |
| 重载时优先匹配指针 | 是               | 否（优先整数）                 |
| 类型安全           | 高               | 低                             |

##  注意事项

- `nullptr` 可以赋值给指针，但不能赋值给整型变量（需要显式转换如 `int n = reinterpret_cast<int>(nullptr);`，但通常不应该这样做）。
- 在条件判断中，`nullptr` 可转换为 `bool` 的 `false`，因此 `if (!ptr)` 依然有效。
- `nullptr` 的引入并不强制废弃 `NULL`，但现代 C++ 推荐使用 `nullptr` 以提升代码清晰度和类型安全。
- 使用 `nullptr` 时需要包含 `<cstddef>` 来获取 `std::nullptr_t` 的定义（不过许多编译器头文件已间接包含，且 `nullptr` 本身是关键字，不需要头文件即可使用）。





--------



# `constexpr`

`constexpr`（常量表达式）是 C++11 引入的关键字，用于**在编译期求值**的表达式或函数。它允许程序员显式要求某个变量、函数或构造函数在编译阶段完成计算，从而提升性能并支持编译期元编程。

## 基本概念

- **常量表达式**：指值在编译阶段就可以确定，且不会改变的表达式。
- `constexpr` 变量：必须用常量表达式初始化，且本身是 `const` 的（但 `constexpr` 隐含了 `const` 语义，对指针略有不同）。
- `constexpr` 函数：其返回值或参数可以是常量表达式，当传入常量参数时在编译期求值，否则退化为普通函数。
- `constexpr` 构造函数：允许创建编译期的用户自定义类型对象。

## `constexpr` 变量

语法：`constexpr 类型 变量名 = 常量表达式;`

```cpp
constexpr int max_size = 100;          // 编译期常量
constexpr double pi = 3.1415926;
constexpr int arr[max_size];           // 可用于数组大小

int x = 10;
// constexpr int y = x;                // 错误：x 不是常量表达式
```

### 与 `const` 的区别
- `const` 表示“运行期只读”，不保证编译期已知。
- `constexpr` 表示“编译期常量”，一定在编译期求值，且隐含 `const` 属性。

```cpp
int a = 5;
const int b = a;        // 合法，b 是运行期常量（只读）
// constexpr int c = a; // 错误，a 不是常量表达式
```

##  `constexpr` 函数

函数可以声明为 `constexpr`，此时被称为常量表达式函数，当所有参数都是常量表达式时，函数在编译期求值；否则像普通函数一样在运行期执行。

### 限制
- 函数体不能出现常量表达式以外的内容，但是`using `、`typedef`、`static_assert`、`return`除外 。
- 返回值类型必须是常量表达式。
- 函数体不能有 `try` 块或 `asm` 声明。

```cpp
constexpr int square(int x) {
    return x * x;         
}

constexpr int val = square(5);   // 编译期求值 val = 25
int y = 3;
int z = square(y);               // 运行期调用，y 不是常量
```

```cpp
constexpr int factorial(int n) {
    return n <= 1 ? 1 : n * factorial(n - 1);
}

constexpr int f5 = factorial(5); // 编译期求值 120
```

##  修饰构造函数

用户自定义类型可以通过 `constexpr` 构造函数创建编译期对象。该类必须满足：

- 函数体必须为空，采用初始化列表方式为各个成员变量赋值
- 至少有一个 `constexpr` 构造函数。
- 析构函数不能是用户自定义的（C++11 中默认或隐式即可）。

```cpp
class Point {
public:
    constexpr Point(double x, double y) : x_(x), y_(y) {}
    constexpr double x() const { return x_; }
    constexpr double y() const { return y_; }
private:
    double x_, y_;
};

constexpr Point origin(0.0, 0.0);
constexpr double ox = origin.x();   // 编译期求值
```

##  修饰模板函数

`constexpr` 经常与模板结合，实现编译期计算和元编程。

```cpp
template<int N>
constexpr int fib() {
    return fib<N-1>() + fib<N-2>();
}
template<>
constexpr int fib<0>() { return 0; }
template<>
constexpr int fib<1>() { return 1; }

int arr[fib<10>()];   // 数组大小为 55
```

### 局限性（C++11）

- **函数体限制严格**：只能有一条 `return`，不能用循环、局部变量（C++14 放宽）。
- **不能修改参数**：所有参数都是 `const` 的（按值传递可修改副本，但意义不大）。
- **构造函数不能有函数体**（C++11 中 `constexpr` 构造函数必须为空，成员通过初始化列表初始化）。
- **不能有虚函数**。



# 自动类型推导

C++11 引入了 `auto` 和 `decltype` 两种自动类型推导机制。



## `auto`

`auto` 让编译器根据变量的**初始值**来推导其类型。

### 基本用法
-   **声明变量**：`auto x = 5;` （`x` 为 `int`）
-   **声明指针/引用**：`auto` 会自动剥离顶层 `const` 和引用，除非显示声明或者包含引用、指针。
    
    ```cpp
    int a = 10;
    int& ref = a;
    const int ca = 20;
    
    auto b = ref;   // b 是 int（引用被忽略）
    auto c = ca;    // c 是 int（顶层 const 被忽略）
    auto& d = ref;  // d 是 int&（显式引用保留）
    const auto e = ca; // e 是 const int（显式 const 保留）
    ```

### 推导规则

> 顶层:**表示对象本身是常量**，即该对象的值不可修改。
>
> - 对于**非指针/非引用**的类型，`const` 总是顶层。
>
> - 对于**指针**，顶层 `const` 修饰的是指针本身（即指针变量存储的地址不可变）
>
> - ```cpp
>   const int ci = 42;       // ci 是顶层 const：ci 本身不可修改
>   int* const p = &x;       // p 是顶层 const：p 的指向不可变（但 *p 可修改）
>   const int* const cp = &x; // cp 既是顶层 const（指针本身）又是底层 const（指向 const int）
>   ```
>
> 底层:**表示指针（或引用）所指的对象是常量**，即通过该指针/引用不能修改所指对象的值。
>
> - 对于**指针**，底层 `const` 出现在 `*` 的左边，例如 `const int*`。
>
> - 对于**引用**，所有 `const` 引用（`const T&`）都是底层 `const`，因为引用本身不是对象，无法被设为“引用本身不可改”，所以 `const` 修饰的是所指对象。
>
> - ```cpp
>   const int* p = &x;       // p 是底层 const：不能通过 p 修改 x
>   int const* p2 = &x;      // 同上，底层 const
>   const int& r = x;        // r 是底层 const：不能通过 r 修改 x
>   ```
>
>   

1. `auto` 会**丢弃**初始化表达式的**引用**和**顶层 `const`/`volatile`**，但保留**底层 `const`/`volatile`**

   - 如果希望保留引用或顶层 const，需要显式使用 `auto&` 或 `const auto` 等

2. **列表初始化**：`auto` 可推导 `std::initializer_list`。

   ```cpp
   auto lst = {1, 2, 3}; // lst 类型为 std::initializer_list<int>
   // auto lst2{1, 2, 3}; // C++17 起：错误，直接列表初始化只能单元素
   ```

### 例子

```cpp
int temp = 110;
auto *a = &temp;//a是int*,auto推测的类型是int
auto b = &temp;	//b是int*, auto推测的类型是int*
auto &c = temp;	//c是int&, auto推测的类型是int
auto d = temp;	//d是int , auto推测的类型是int

int tmp = 250;
const auto a1 = tmp;	//a1是const int , auto推测为int
auto a2 = a1;			//a2是int , auto推测为int
const auto &a3 = tmp;	//a3是const int & , auto推测为int
auto &a4 = a3;			// a4是const int& , auto推测为const int


作者: 苏丙榅
链接: https://subingwen.cn/cpp/autotype/#1-1-%E6%8E%A8%E5%AF%BC%E8%A7%84%E5%88%99
来源: 爱编程的大丙
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
```

### 限制
