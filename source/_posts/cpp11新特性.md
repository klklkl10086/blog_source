---
title: C++现代特性之CPP 11
date: 2026-03-12 21:58:36
tags: ["CPP"]
categories: ["CPP开发"]
description: CPP现代常用的特性
---

> 参考资料:
>
> [c++11实用特性]( https://www.bilibili.com/video/BV1bX4y1G7ks/?share_source=copy_web&vd_source=777aaa8a415b68222e598d976e64642c)
>
> 《C++ Primer Plus》
>
> deepseek
>
> Gemini

- 内存管理：移动语义、右值引用、智能指针
- 并发编程: 见cpp多线程
- 泛型编程: 模板
- 语法糖

-------------



# 左值右值

1. **左值**
   - 指向内存中明确位置、具有持久状态（有名字、能取地址）的对象
   - 可以出现在赋值号 `=` 的左边或右边
   - **示例**：变量名、解引用表达式 `*p`、返回左值引用的函数调用。
2. **右值**
   - 不具有内存实体（或即将被销毁的临时对象）、没有名字、无法取地址的值。
   - 只能出现在赋值号 `=` 的右边。
   - 字面常量（如 `42`）、算术表达式（如 `a + b`）、返回非引用的函数调用。

---------



# 原始字面量

在 C++11 标准中，引入了**原始字面量**（Raw String Literal），用于简化字符串中反斜杠 `\` 和引号 `"` 等特殊字符的处理。它让字符串内容可以“原样”呈现，无需转义，特别适合正则表达式、文件路径、多行文本等场景。

## 基本语法

原始字面量的格式为：

```cpp
R"delimiter(raw_characters)delimiter"
```

- `R` 表示原始字面量前缀。
- `delimiter` 是可选的**定界符序列**（长度不超过 16 个字符的自定义字符序列，不能包含反斜杠、空格和括号）用于唯一标识字符串的结束位置。当字符串内容本身包含 `)"` 时，避免编译器误认为字面量提前结束。
- `( raw_characters )` 中是真正的字符串内容，可以包含任何字符（包括换行、引号、反斜杠等），**无需转义**。

如果省略定界符，简写为 `R"(...)"`。

## 关键特性

- **不处理转义序列**：例如 `\n`、`\t`、`\"` 等均作为普通字符对待。
- **允许换行**：字符串可以直接跨越多行，换行符会被保留为字符串的一部分。
- **允许引号**：无需转义即可包含 `"` 字符。
- **允许反斜杠**：`\` 就是普通反斜杠，不会引起转义。

## 示例

### 普通字符串 vs 原始字面量

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

### 多行字符串

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

### 正则表达式场景

正则表达式中经常出现大量反斜杠，原始字面量可以显著提高可读性。

```cpp
#include <regex>
#include <string>

// 匹配形如 \d{3}-\d{4} 的电话号码
std::regex phone_normal("\\d{3}-\\d{4}");   // 需要双重转义
std::regex phone_raw(R"(\d{3}-\d{4})");      // 更清晰
```

### 文件路径

```cpp
std::string path = R"(C:\Users\Name\Documents\file.txt)";
// 等价于 "C:\\Users\\Name\\Documents\\file.txt"
```

## 注意事项

- 原始字面量中唯一需要留意的字符是 **`)"`** 序列（如果未使用定界符）或 **`)delimiter"`**（如果使用了定界符）。只要字符串内容不包含该精确序列，就可以安全使用。
- 定界符可以是任意可见字符（除了反斜杠、空格和括号），通常使用一个短单词或下划线，如 `R"tag(...)tag"`。
- 原始字面量仍然是标准 `std::string`（或字符数组），与普通字符串字面量完全兼容。
- 原始字面量也支持宽字符、UTF-8/16/32 前缀，例如 `u8R"(...)"`、`LR"(...)"` 等。



-----------



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



----------------

#  Lambda 表达式







# `override`与` final`







# 统一初始化与列表初始化



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
-   **声明指针/引用**：`auto` 会自动剥离**顶层** `const` 和`volatile`，除非显示声明。
    
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



> 底层:**表示指针（或引用）所指的对象是常量**，即通过该指针/引用不能修改所指对象的值。
>
> - 对于**指针**，底层 `const` 出现在 `*` 的左边，例如 `const int*`。
>
> - 对于**引用**，所有 `const` 引用（`const T&`）都是底层 `const`，因为引用本身不是对象，无法被设为“引用本身不可改”，所以 `const` 修饰的是所指对象。
>
> 
> - ```cpp
>   const int* p = &x;       //p是指向常量的指针，因此 p 是底层 const：不能通过 p 修改 x
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
3. **指针推导**：当初始值是一个指针时，`auto` 和 `auto*` 都可以正确推断出指针类型，两者的效果通常是等价的。但 `auto*` 会强制要求初始值必须是一个指针。
   ```cpp
    int val = 42;
    auto p1 = &val;  // p1 推导为 int*
    auto* p2 = &val; // p2 推导为 int*
   
    // auto* p3 = val; // 编译错误：val 不是指针，无法匹配 auto*
   ```
4. **数组退化**: 当用数组初始化` auto `变量时，数组会“退化”为指向其首元素的指针。如果使用 `auto&`，则不会退化，而是推导为数组的引用。
   ```cpp
    int arr[] = {1, 2, 3};
   
    auto arr_ptr = arr;    // arr_ptr 的类型是 int* (数组退化为指针)
    auto& arr_ref = arr;   // arr_ref 的类型是 int(&)[3] (对长度为3的数组的引用)
   ```
### 例子

```cpp
int temp = 110;
auto *a = &temp;//a是int*,auto推测的类型是int
auto b = &temp;	//b是int*, auto推测的类型是int*
auto &c = temp;	//c是int&, auto推测的类型是int
auto d = temp;	//d是int , auto推测的类型是int

int tmp = 250;
const auto a1 = tmp;	//显示声明了const a1是const int , auto推测为int
auto a2 = a1;			//顶层const 则剥离 因此a2是int , auto推测为int
const auto &a3 = tmp;	//a3是const int & , auto推测为int
auto &a4 = a3;			// 底层const 保留，因此a4是const int& , auto推测为const int


作者: 苏丙榅
链接: https://subingwen.cn/cpp/autotype/#1-1-%E6%8E%A8%E5%AF%BC%E8%A7%84%E5%88%99
来源: 爱编程的大丙
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
```

### 限制
1. **不能作为函数的参数直接使用。因为只有在函数调用的时候才会给函数参数传递实参,`auto`要求必须要给修饰的变量赋值,因此矛盾**
2. **不能用于类的非静态成员变量的初始化**
```cpp
    class Test
        {
            auto v1 = 0;                    // error
            static auto v2 = 0;             // error,类的静态非常量成员不允许在类内部直接初始化
            static const auto v3 = 10;      // ok
        }


        作者: 苏丙榅
        链接: https://subingwen.cn/cpp/autotype/#1-2-auto%E7%9A%84%E9%99%90%E5%88%B6
        来源: 爱编程的大丙
        著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

```

3. **无法使用auto推导出模板参数**
   
   ```cpp
   template <typename T>
    struct Test{}
   
    int func()
    {
        Test<double> t;
        Test<auto> t1 = t;           // error, 无法推导出模板类型
        return 0;
    }







### 常用场景
1. **遍历stl容器**
2. **泛型编程,使用模板时,很多时候不知道变量应该定义为什么类型**

   ```cpp
   //不用auto
   #include <iostream>
   #include <string>
   using namespace std;
   
   class T1
   {
   public:
       static int get()
       {
           return 0;
       }
   };
   
   class T2
   {
   public:
       static string get()
       {
           return "hello, world";
       }
   };
   
   template <class A>        // 添加了模板参数 B
   void func(void)
   {
       auto val = A::get();
       cout << "val: " << val << endl;
   }
   
   int main()
   {
       func<T1>();                  
       func<T2>();              
       return 0;
   }
   ```

​		

```CPP
//不用auto
#include <iostream>
#include <string>
using namespace std;

class T1
{
public:
    static int get()
    {
        return 0;
    }
};

class T2
{
public:
    static string get()
    {
        return "hello, world";
    }
};

template <class A, typename B>        // 添加了模板参数 B
void func(void)
{
    B val = A::get();
    cout << "val: " << val << endl;
}

int main()
{
    func<T1, int>();                  // 手动指定返回值类型 -> int
    func<T2, string>();               // 手动指定返回值类型 -> string
    return 0;
}
```


    作者: 苏丙榅
    链接: https://subingwen.cn/cpp/autotype/#1-3-auto%E7%9A%84%E5%BA%94%E7%94%A8
    来源: 爱编程的大丙
    著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
    ```


## `decltype`
 > decltype（全称：Declared Type）,作用是向编译器发出查询：“这个表达式的类型是什么？”,与 auto 必须绑定变量初始化不同，decltype 只是**静态地在编译期分析表达式的类型**，绝不会真正计算（求值）该表达式。在**模板元编程和泛型编程**中，我们经常需要知道某个表达式的结果究竟是什么类型，但又不能或者不想真正去执行这个表达式，这时候 decltype 就成为了不可或缺的工具。
 > ` auto `与 `decltype` 
 >
 > 1. 精确推导：与 auto 会丢弃引用和顶层 const 不同，decltype **保留所有类型修饰符**（包括引用和 CV 限定符）。
 > 2. 零运行时开销：`auto` 和 `decltype` 同样在编译阶段完成，不会生成任何对应的汇编指令。

### 推导规则
`decltype(expr)` 的推导结果极其依赖于表达式的形式以及它的值类别。C++ 标准将其推导规则严格分为以下几类：
1. **未加括号的标识符或成员访问:**
   如果`e` 是一个没有被多余括号包围的**变量名、函数名**，或者是**类成员访问表达式**（如 obj.member 或 ptr->member），那么 `decltype(e)`推导出的就是该实体在代码中声明时的精确类型。

    ```cpp
    const int ci = 0;
    int x = 10;
    int& ref_x = x;
    struct Point { double x; double y; };
    Point pt;
   
    decltype(ci) a = 1;      // a 的类型是 const int (完美保留 const)
    decltype(ref_x) b = x;   // b 的类型是 int& (完美保留引用)
    decltype(pt.x) c = 0.0;  // c 的类型是 double
    ```

2. **其他表达式的值类别:**
   如果不符合`1`的条件(例如它是一个算术表达式、函数调用，或者被括号 () 包围的变量),编译器将根据表达式 e 的**值类别**来决定类型。假设表达式 e 的基础类型为 T：

   - `e`是左值:`decltype(e)` 为` T&`
   - `e`是将亡值: `decltype(e)` 为 **`T&&`**
   - `e`是纯右值:`decltype(e)` 为 **`T`**

   ```cpp
   int i = 42;
   int* p = &i;
   
   // 函数调用
   int f();
   int& g();
   decltype(f()) x1 = 1;    // x1 是 int (纯右值)
   decltype(g()) x2 = i;    // x2 是 int& (左值)
   
   // 算术表达式
   decltype(i + 0) x3 = 5;  // x3 是 int (i+0 产生纯右值)
   
   // 解引用表达式
   decltype(*p) x4 = i;     // x4 是 int& (*p 返回左值，可以被赋值)
   ```



---------
# 右值引用与移动语义

> 在 C++11 之前，C++ 在处理临时对象（比如函数返回的大型容器、字符串拼接产生的中间结果）时，往往会触发昂贵的**深拷贝 (Deep Copy)**。为了解决这个性能瓶颈，C++11 引入了**右值引用**，它使得程序能够“窃取”临时对象的内存资源，从而实现零拷贝的**移动语义 (Move Semantics)**。



## 右值引用

> 传统 C++ 中的引用（现在称为**左值引用**）使用 `&` 符号；C++11 引入的**右值引用**使用 `&&` 符号。

### 绑定规则

1. 右值引用只能绑定到右值上，不能直接绑定到左值。它的核心目的是**延长临时对象的生命周期**，或者接管临时对象的资源。

 ```cpp
   int a = 10;          // a 是左值
   int& ref_a = a;      // 正确：左值引用绑定到左值
   
   // int&& rref_a = a; // 错误：不能将右值引用绑定到左值
   int&& rref_1 = 20;   // 正确：20 是纯右值
   int&& rref_2 = a + 5;// 正确：a+5 产生一个临时纯右值
 ```

2. 右值引用变量本身是**左值**,上述代码中`rref_1 `的类型是右值引用,但它是左值

```cpp
void process(int& x) { /* 处理左值 */ }
void process(int&& x) { /* 处理右值 */ }

void test() {
    int&& r = 100;
    // 下面这行会调用 process(int& x)，而不是 process(int&& x)！
    // 因为 r 作为变量传递时，它是一个有名字的左值。
    process(r); 
}
```



## 移动语义

> 移动语义是右值引用最大的价值所在。通过编写**移动构造函数**和**移动赋值运算符**，我们可以将资源（如动态分配的内存）从源对象直接转移到目标对象，而不是进行深拷贝。

### `std::move`

如果想把一个左值当作右值来处理（即明确告诉编译器：“我不再需要这个左值了，你可以把它的资源拿走”），可以使用 `std::move()`。 

**注意：`std::move` 并在运行时不执行任何实际的移动操作，它仅仅是在`编译期`执行了类型转换（`static_cast<T&&>`），将左值强制转换为右值引用（将亡值）。**

```cpp
#include <iostream>
#include <cstring>

class MyString {
private:
    char* data;
    size_t size;

public:
    // 1. 普通构造函数
    MyString(const char* str) {
        size = std::strlen(str);
        data = new char[size + 1];
        std::strcpy(data, str);
        std::cout << "Constructed\n";
    }

    // 2. 拷贝构造函数 (深拷贝 - 极其昂贵)
    // 绑定到左值
    MyString(const MyString& other) {
        size = other.size;
        data = new char[size + 1];
        std::strcpy(data, other.data);
        std::cout << "Copy Constructed (Deep Copy)\n";
    }

    // 3. 移动构造函数 (浅拷贝/资源窃取 - 极速)
    // 绑定到右值 (临时对象或 std::move)
    // 注意加上 noexcept，向 STL 保证移动过程不会抛出异常
    MyString(MyString&& other) noexcept {
        // 窃取源对象的指针和大小
        data = other.data;
        size = other.size;

        // 将源对象置于“有效但未指定”的空状态，防止其析构函数释放这块内存
        other.data = nullptr;
        other.size = 0;
        
        std::cout << "Move Constructed (Zero Copy)\n";
    }

    ~MyString() {
        delete[] data;
    }
};

int main() {
    MyString str1("Hello"); // 调用普通构造
    
    // 场景 A：必须深拷贝，因为 str1 后面可能还要用
    MyString str2 = str1;   // 调用拷贝构造函数
    
    // 场景 B：我们确定 str1 以后不再使用了，使用 std::move 榨干它的资源
    MyString str3 = std::move(str1); // 调用移动构造函数！
    
    // 此时 str1.data 已经被置为 nullptr，它的资源现在属于 str3
    return 0;
}
```



## 完美转发

> 当我们在编写模板函数时，常常需要将参数原封不动地传递给内部的另一个函数。所谓“原封不动”，指的是**保持参数的左值或右值属性不变**，以及保持 `const` 属性不变。

### 万能引用

在**模板**中，如果参数类型写为 `T&&`（且 `T` 是需要推导的模板参数），那么它就不再是普通的右值引用，而是**万能引用**。

- 如果传入左值，`T&&` 会被推导为左值引用（发生引用折叠）。
- 如果传入右值，`T&&` 会保持为右值引用。

### `std::forward`

右值引用作为形参进入函数体后，由于有了名字，就变成了左值。为了在继续向下传递时恢复它原本的“左右值”属性，必须使用 `std::forward<T>()`。

```cpp
void process(int& x)  { std::cout << "Lvalue processed\n"; }
void process(int&& x) { std::cout << "Rvalue processed\n"; }

// 这是一个工厂/包装函数模板
template <typename T>
void wrapper(T&& arg) {
    // 错误做法：arg 在此处是左值，将永远调用 process(int&)，失去右值属性
    // process(arg); 
    
    // 正确做法：完美转发。
    // 如果外部传入的是左值，forward 传递左值；传入的是右值，forward 传递右值。
    process(std::forward<T>(arg)); 
}

int main() {
    int a = 5;
    wrapper(a);       // 传入左值，输出: Lvalue processed
    wrapper(42);      // 传入纯右值，输出: Rvalue processed
    wrapper(std::move(a)); // 传入将亡值，输出: Rvalue processed
}
```





> C++11 将右值进一步细分为：
>
> 1. **纯右值 (Prvalue)**：非引用返回的临时变量、运算表达式产生的临时变量、原始字面量。
> 2. **将亡值 (Xvalue)**：与右值引用相关的表达式，比如 `std::move(x)` 的返回值，或者返回右值引用的函数调用。它标志着某个对象的资源可以被安全地“移动”。
>
> 

----------


# 智能指针

> 在传统 C++（C++98/03）中，内存管理完全由程序员负责。这种“裸指针”模式面临三大痛点：
>
> 1. **内存泄漏**：申请了内存但忘记释放。
> 2. **悬垂指针**：指向的对象已释放，但指针仍在使用。
> 3. **二次释放**：对同一块内存调用两次 `delete` 导致崩溃。
>
> C++11 引入了智能指针，其核心思想是 **RAII **：通过一个栈上的对象来管理堆上的资源。当栈对象生命周期结束析构时，自动释放其管理的堆资源。

## RAII

> RAII(Resource Acquisition Is Initialization，资源获取即初始化)：**将资源的生命周期与对象的生命周期绑定**，在对象构造时获取资源（如动态内存、文件句柄、互斥锁、数据库连接等），在对象析构时自动释放资源。

### 原理

- **构造函数**：负责获取资源（分配内存、打开文件、加锁等）。
- **析构函数**：负责释放资源（释放内存、关闭文件、解锁等）。
- 当对象离开作用域时（包括正常结束、抛出异常等），C++ 保证析构函数会被自动调用，从而确保资源被正确释放。

```cpp
#include <iostream>
#include <fstream>

class FileHandle {
public:
    FileHandle(const char* filename) : file(fopen(filename, "r")) {
        if (!file) throw std::runtime_error("打开文件失败");
    }
    ~FileHandle() { 
        if (file) fclose(file);
    }
    // 禁止拷贝构造和拷贝赋值  避免出现多个对象共享同一资源并重复释放的错误。
    FileHandle(const FileHandle&) = delete;
    FileHandle& operator=(const FileHandle&) = delete;
private:
    FILE* file;
};
```

### 优势

1. **异常安全**：即使发生异常，对象析构依然会被调用，资源不会泄漏。
2. **防止忘记释放资源**：不需要手动写 `delete`、`fclose` 等代码。
3. **代码简洁清晰**：资源管理逻辑集中在构造/析构函数中。



## `std::unique_ptr`

> 最常用、性能最高的智能指针,保证同一时间内只有一个指针拥有该对象。

- **禁止拷贝**：不能通过赋值或构造进行拷贝。如果允许会出现两个指针指向同一个资源,发生重复释放
- **允许移动**：可以通过 `std::move` 转移所有权。因为禁止了拷贝所以只能通过移动来转移所有权
- **零开销**：在运行时，其大小与裸指针完全一致，没有任何性能损失。

```cpp
#include <memory>
#include <iostream>

struct Resource {
    Resource() { std::cout << "资源已创建\n"; }
    ~Resource() { std::cout << "资源已释放\n"; }
    void use() { std::cout << "正在使用资源\n"; }
};

void test_unique() {
    // 1. 创建 unique_ptr (建议使用 C++14 的 std::make_unique)
    std::unique_ptr<Resource> ptr1(new Resource()); 

    // 2. ptr2 = ptr1; // 错误！禁止拷贝

    // 3. 转移所有权
    std::unique_ptr<Resource> ptr2 = std::move(ptr1); 
    if (!ptr1) std::cout << "ptr1 现在为空\n";

    ptr2->use();
} // 函数结束时，ptr2 析构，资源自动释放
```

## `std::shared_ptr`

> `std::shared_ptr` 允许多个指针同时指向同一个对象。对象内部维护一个**引用计数 **。
>
> 对象内部通常包含两个指针：
>
> - 指向管理对象的指针
> - 指向控制块的指针（包含引用计数、弱引用计数、删除器等）

1. **引用计数**：每增加一个指向该对象的 `shared_ptr`，计数加 1；每有一个指针失效，计数减 1。
2. **自动析构**：当计数降为 0 时，自动销毁对象并释放内存。
3. **线程安全**：引用计数操作是线程安全的，但**对象本身**和**它指向的资源**需要程序员额外处理同步。”

```cpp
void test_shared() {
    // 使用 std::make_shared 是更高效且安全的方式
    auto ptr1 = std::make_shared<Resource>();
    std::cout << "当前计数: " << ptr1.use_count() << "\n"; // 1

    {
        auto ptr2 = ptr1; // 拷贝：计数加 1
        std::cout << "当前计数: " << ptr1.use_count() << "\n"; // 2
    } // ptr2 离开作用域，计数减 1

    std::cout << "当前计数: " << ptr1.use_count() << "\n"; // 1
} // ptr1 离开作用域，计数归 0，释放资源
```



## `std::weak_ptr`

>  `std::weak_ptr`是一种不控制对象生命周期的智能指针，它是 `std::shared_ptr` 的观察者。



- **不增加计数**：指向对象但不参与所有权。
- **安全性**：在使用前必须调用 `lock()` 升级为 `shared_ptr`，如果对象已销毁，`lock()` 返回空指针。
- **打破循环引用**：这是它最重要的用途。



### 循环引用陷阱

当两个对象互相持有对方的` shared_ptr` 时，引用计数永远不会归零，导致内存泄漏。

```cpp
struct B;
struct A { std::shared_ptr<B> b_ptr; ~A() { std::cout << "A 析构\n"; } };
struct B { std::shared_ptr<A> a_ptr; ~B() { std::cout << "B 析构\n"; } };

void leak_demo() {
    // 步骤 1：在堆上创建 A 对象。
    // 栈上有一个局部变量 a 指向它。
    auto a = std::make_shared<A>(); 
    // 【当前状态】对象 A 计数 = 1

    // 步骤 2：在堆上创建 B 对象。
    // 栈上有一个局部变量 b 指向它。
    auto b = std::make_shared<B>(); 
    // 【当前状态】对象 B 计数 = 1

    // 步骤 3：A 对象内部的 b_ptr 也指向了 B 对象。
    // 现在有局部变量 b 和 a->b_ptr 两个指针同时指向 B 对象。
    a->b_ptr = b; 
    // 【当前状态】对象 B 计数 = 2

    // 步骤 4：B 对象内部的 a_ptr 也指向了 A 对象。
    // 现在有局部变量 a 和 b->a_ptr 两个指针同时指向 A 对象。
    b->a_ptr = a; 
    // 【当前状态】对象 A 计数 = 2

} // <--- 关键点：函数结束，右大括号！
```

在 C++ 中，当离开作用域（即遇到 `}`）时，栈上的局部变量会按照**后进先出**的顺序被自动销毁。

1. **销毁局部变量 `b`**：栈上的 `b` 指针不复存在了。因此，**对象 B 的引用计数减 1 （从 2 变成了 1）**。
2. **销毁局部变量 `a`**：栈上的 `a` 指针也不复存在了。因此，**对象 A 的引用计数减 1 （从 2 变成了 1）**。

现在，函数已经彻底执行完毕，栈被清空了，但我们在堆上留下了两个对象：

- **对象 A** 的计数是 1，因为虽然局部变量 `a` 死了，但**对象 B 内部的 `b->a_ptr` 仍然指着它**。
- **对象 B** 的计数是 1，因为虽然局部变量 `b` 死了，但**对象 A 内部的 `a->b_ptr` 仍然指着它**。

因为引用计数都没有降到 0，所以它们的析构函数（`~A()` 和 `~B()`）永远不会被触发，这两块堆内存就永远挂在空中，造成了**内存泄漏**。

如果我们将其中一个结构体内部的指针换成 `std::weak_ptr`，它在上述步骤 3 或 4 中就不会增加引用计数（最高只能是 1），那么在函数结束销毁局部变量时，计数就会顺利降为 0，从而触发链式反应，完美释放内存。

### 安全性:`lock()`

**`weak_ptr` 没有重载 `->` 和 `*` 运算符**。你在代码里根本无法直接写出 `wp->value` 这样的代码，编译器会直接报错。它强迫你必须使用 `lock()`。

既然不能直接用，那就必须把 `weak_ptr` 变成 `shared_ptr` 才能用。这个过程就叫做**升级 (Upgrade)**。

调用 `wp.lock()` 时，底层其实在做一个**极其严谨且线程安全（原子性）的操作**：

1. **检查控制块**：它去查看该对象当前的“强引用计数（shared count）”是否大于 0。
2. **分支 A（对象还活着）**：如果大于 0，说明对象还在。`lock()` 会**立刻将强引用计数加 1**，并返回一个有效的 `shared_ptr`。
   - *为什么叫安全？* 因为一旦拿到了这个临时的 `shared_ptr`，引用计数就增加了。就算此时其他线程全都不管这个对象了，**只要你手里的这个临时 `shared_ptr` 还没死，对象就绝对不会被销毁**。你可以放心大胆地用。
3. **分支 B（对象已死亡）**：如果强引用计数等于 0，说明对象已经被释放了。`lock()` 会返回一个**空的（Null）`shared_ptr`**。你的程序可以通过 `if` 判断安全地跳过操作，避免了崩溃。



## 使用手册

1. **优先使用 `unique_ptr`**：如果不需要共享所有权，默认使用它，因为它性能最优。

2. **始终使用工厂函数**：优先用 `std::make_unique` (C++14) 和 `std::make_shared` (C++11)。它们能提高性能（减少内存分配次数）并防止由于异常导致的内存泄漏。

3. **不要将裸指针直接初始化**：尽量写成 `auto p = std::make_shared<T>()`。

4. **接口传递**：

   - 只读访问：传递 `const T&`。

   - 转移所有权：传递 `std::unique_ptr<T>&&` 或值传递。

   - 共享所有权：传递 `std::shared_ptr<T>`。



---------------------

# 可变参数模板