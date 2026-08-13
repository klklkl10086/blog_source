---
title: CPP拾遗
date: 2026-08-01 22:57:24
categories:
  - C++
tags:
  - C++
description: C++ 内存、STL、模板与张量广播相关知识拾遗。
---

# C++ 内存、STL、模板与张量广播笔记

##  C++ 基础与内存操作

###  `sizeof` 运算符

#### 基本含义

`sizeof` 返回类型或对象所占用的字节数，返回值类型为 `std::size_t`。

#### 编译时求值

对于标准 C++ 类型，`sizeof` 的结果通常是编译期常量，可以用于：

* 数组长度
* 模板参数
* `static_assert`
* `constexpr` 表达式

```cpp
static_assert(sizeof(int) >= 2);

int buffer[sizeof(double)];
```

`sizeof` 的操作数通常处于未求值上下文，表达式不会真正执行。

```cpp
int x = 1;
std::size_t n = sizeof(++x);

// x 仍然为 1
```

#### 静态类型大小

`sizeof(expression)` 根据表达式的静态类型计算大小。

```cpp
struct Base {
    virtual ~Base() = default;
};

struct Derived : Base {
    int data[100];
};

Derived d;
Base& ref = d;

sizeof(ref);      // sizeof(Base)
sizeof(d);        // sizeof(Derived)
```

动态类型需要通过虚函数机制或 RTTI 判断，`sizeof` 本身只处理编译期类型信息。

#### 数组与指针

真正的数组对象保存全部元素，因此 `sizeof` 返回整个数组的大小。

```cpp
int arr[10];

sizeof(arr);          // 10 * sizeof(int)
sizeof(arr[0]);       // sizeof(int)

std::size_t count = sizeof(arr) / sizeof(arr[0]); // 10
```

指针只保存地址。

```cpp
int* ptr = arr;

sizeof(ptr);          // 指针大小，常见 64 位系统上为 8
sizeof(*ptr);         // sizeof(int)
```

数组作为 `sizeof` 的直接操作数时会保留数组类型，不发生数组到指针的转换。

#### 结构体内存对齐

结构体成员通常按照各自的对齐要求放置。编译器可能在成员之间和结构体末尾插入填充字节。

```cpp
struct A {
    char c;
    int i;
};
```

一种常见布局：

```text
偏移 0：char c，占 1 字节
偏移 1~3：填充
偏移 4~7：int i
```

因此：

```cpp
sizeof(A); // 常见结果为 8
```

成员顺序会影响结构体大小。

```cpp
struct B {
    char c1;
    int i;
    char c2;
};

struct C {
    int i;
    char c1;
    char c2;
};
```

常见结果：

```cpp
sizeof(B); // 12
sizeof(C); // 8
```

结构体大小通常满足以下规律：

1. 每个成员的起始地址满足自身对齐要求。
2. 结构体整体对齐值通常等于成员中的最大对齐值。
3. 结构体总大小通常是整体对齐值的整数倍。
4. 具体布局由编译器、ABI 和编译选项决定。

可以使用 `alignof` 查看对齐要求：

```cpp
alignof(int);
alignof(A);
```

#### `sizeof(std::vector)` 与迭代器大小

`std::vector<T>` 对象本身保存管理信息，元素存储在动态内存中。

常见实现使用三个指针或等价信息：

```text
begin        指向第一个元素
end          指向最后一个有效元素之后
capacity_end 指向已分配空间末尾
```

因此在部分 64 位标准库实现中：

```cpp
sizeof(std::vector<int>) == 3 * sizeof(void*)
```

这个结果属于实现细节，C++ 标准未规定 `vector` 的对象布局。

```cpp
std::vector<int> v(1'000'000);

sizeof(v); // 只计算 vector 管理对象
```

元素数量不会直接改变 `sizeof(v)`。

迭代器是独立类型，其大小和 `vector` 对象大小没有固定关系。

```cpp
sizeof(v);
sizeof(v.begin());
```

发布模式下，普通 `vector<T>::iterator` 经常封装一个 `T*`。调试模式可能额外保存：

* 所属容器指针
* 边界检查信息
* 迭代器链表节点
* 调试状态

因此下面的断言缺乏可移植性：

```cpp
static_assert(
    sizeof(std::vector<int>) == 3 * sizeof(void*)
);
```

---

###  `memcpy` 原理与优化

#### 基本用途

`std::memcpy` 将一段内存中的字节复制到另一段内存。

```cpp
#include <cstring>

int source[4] = {1, 2, 3, 4};
int destination[4];

std::memcpy(destination, source, sizeof(source));
```

函数原型概念上类似：

```cpp
void* memcpy(void* destination,
             const void* source,
             std::size_t count);
```

基础实现可以理解为逐字节复制：

```cpp
void* simple_memcpy(void* destination,
                    const void* source,
                    std::size_t count) {
    auto* dst = static_cast<unsigned char*>(destination);
    auto* src = static_cast<const unsigned char*>(source);

    for (std::size_t i = 0; i < count; ++i) {
        dst[i] = src[i];
    }

    return destination;
}
```

实际标准库实现通常根据数据大小、地址对齐和处理器特性选择更高效的复制方式。

#### 类型限制

对于任意对象类型，直接按字节复制需要关注对象语义。

`memcpy` 适合：

* 基本数值类型
* 指针值的底层复制
* 字节缓冲区
* 可平凡复制类型
* `std::is_trivially_copyable_v<T>` 为真的类型

```cpp
#include <type_traits>

template<class T>
void copy_objects(T* dst, const T* src, std::size_t count) {
    static_assert(std::is_trivially_copyable_v<T>);
    std::memcpy(dst, src, count * sizeof(T));
}
```

带有自定义复制逻辑、虚函数、动态资源或复杂不变量的类型适合使用：

```cpp
std::copy_n(source, count, destination);
```

#### 对齐处理与批量传输

高性能实现通常包含几个阶段：

1. 复制少量前缀字节，使目标地址达到合适的对齐边界。
2. 使用机器字、向量寄存器或缓存行大小进行批量复制。
3. 处理末尾不足一个批次的剩余字节。

概念性示例：

```cpp
while (count > 0 && address_not_aligned(dst)) {
    *dst++ = *src++;
    --count;
}

while (count >= block_size) {
    copy_one_block(dst, src);
    dst += block_size;
    src += block_size;
    count -= block_size;
}

while (count > 0) {
    *dst++ = *src++;
    --count;
}
```

现代编译器常将固定长度的 `memcpy` 直接展开成若干条加载和存储指令。

```cpp
struct Data {
    std::uint64_t a;
    std::uint64_t b;
};

Data copy(Data value) {
    Data result;
    std::memcpy(&result, &value, sizeof(Data));
    return result;
}
```

这类代码可能直接编译为寄存器移动，无需真正调用库函数。

#### SIMD 优化

SIMD 指令可以一次处理多个字节，例如：

* SSE
* AVX
* AVX2
* AVX-512
* ARM NEON

典型实现会使用运行时 CPU 特性检测，根据平台选择优化版本。

对于较小内存块，函数调用和复杂分支的开销可能高于复制本身。编译器通常会内联固定长度复制。

#### 非临时存储

非临时存储指令可以减少大块复制对 CPU 缓存的污染，适合：

* 数据量远大于缓存
* 写入后短期内不会再次读取
* 连续的大块内存复制

对于小数据或即将被读取的数据，普通缓存写入通常更合适。

#### 重叠内存与 `memmove`

`memcpy` 要求源区域和目标区域互不重叠。区域重叠时，程序行为未定义。

```cpp
char buffer[] = "abcdef";

std::memcpy(buffer + 1, buffer, 5); // 区域重叠
```

`std::memmove` 支持重叠区域。

```cpp
std::memmove(buffer + 1, buffer, 5);
```

常见实现根据地址关系选择复制方向：

```cpp
if (destination < source) {
    // 从前向后复制
} else {
    // 从后向前复制
}
```

明确不存在重叠时优先使用 `memcpy`，编译器和标准库拥有更大的优化空间。

---

###  数组退化与形参传递

#### 函数形参中的数组调整

函数参数中的数组声明会调整为指针类型。

```cpp
void process(int arr[10]);
```

编译器按下面的形式处理：

```cpp
void process(int* arr);
```

数组长度 `10` 不属于参数类型的一部分。

```cpp
void process(int arr[10]) {
    sizeof(arr); // sizeof(int*)
}
```

即使传入真正的数组，函数内部的 `arr` 仍然是指针参数。

#### 真数组中的 `sizeof`

```cpp
int values[10];

sizeof(values); // 10 * sizeof(int)
```

传入函数后：

```cpp
void test(int values[]) {
    sizeof(values); // sizeof(int*)
}
```

#### 保留数组长度

使用数组引用模板可以保留长度：

```cpp
template<class T, std::size_t N>
constexpr std::size_t array_size(const T (&)[N]) {
    return N;
}

int values[10];

static_assert(array_size(values) == 10);
```

也可以直接将数组引用作为函数参数：

```cpp
template<class T, std::size_t N>
void process(T (&arr)[N]) {
    static_assert(N > 0);
}
```

#### 使用 `std::array`

```cpp
#include <array>

void process(const std::array<int, 10>& arr) {
    std::size_t n = arr.size();
}
```

#### 显式传递长度

```cpp
void process(const int* data, std::size_t size);
```

C++20 可以使用 `std::span` 表达连续但不拥有的数据：

```cpp
#include <span>

void process(std::span<const int> data) {
    for (int value : data) {
        // ...
    }
}
```

---

##  STL 容器

###  `std::array`

`std::array<T, N>` 是固定长度数组的标准库封装。

```cpp
#include <array>

std::array<int, 4> values = {1, 2, 3, 4};
```

#### 主要特点

* 长度在编译期确定
* 数据连续存储
* 没有额外动态分配
* 支持值语义
* 提供标准容器接口
* 通常与内置数组具有相同的存储开销

常用接口：

```cpp
values.size();
values.data();
values.begin();
values.end();
values.front();
values.back();
values.at(2);
values[2];
```

#### 与内置数组的区别

内置数组无法直接赋值：

```cpp
int a[3] = {1, 2, 3};
int b[3];

// b = a; // 编译错误
```

`std::array` 支持整体复制：

```cpp
std::array<int, 3> a = {1, 2, 3};
std::array<int, 3> b;

b = a;
```

内置数组在大量表达式中会退化为指针。`std::array` 作为类对象传递，不会自动退化。

```cpp
void use(const std::array<int, 3>& values);
```

需要原始指针时显式调用：

```cpp
int* ptr = values.data();
```

---

###  `std::vector` 详解

#### 内存模型

`std::vector<T>` 管理一段连续动态内存。

逻辑上维护三个边界：

```text
data begin     第一个元素
data end       最后一个有效元素之后
storage end    已分配空间末尾
```

由此得到：

```cpp
size     = data_end - data_begin
capacity = storage_end - data_begin
```

对应接口：

```cpp
v.size();
v.capacity();
v.data();
```

关系始终满足：

```text
size <= capacity
```

`vector` 对象通常存放在栈上或其他对象内部，元素缓冲区通常位于动态存储区。

#### 容量增长规则

当插入元素导致 `size() > capacity()` 时，`vector` 通常执行：

1. 分配更大的连续内存。
2. 将旧元素移动或复制到新内存。
3. 销毁旧元素。
4. 释放旧内存。
5. 插入新元素。

常见标准库可能使用约 1.5 倍或 2 倍增长策略。具体增长倍率由标准库实现决定。

C++ 标准主要保证连续存储和 `push_back` 的摊还常数复杂度。

#### `reserve`

`reserve(n)` 请求至少容纳 `n` 个元素的容量。

```cpp
std::vector<int> values;
values.reserve(1000);

for (int i = 0; i < 1000; ++i) {
    values.push_back(i);
}
```

作用：

* 减少重复分配
* 减少元素移动或复制
* 提高批量插入性能
* 提高容量范围内迭代器和指针的稳定性

`reserve` 改变容量，不改变元素数量。

```cpp
values.reserve(100);

values.size();     // 0
values.capacity(); // 至少为 100
```

#### `resize`

`resize(n)` 改变元素数量。

```cpp
std::vector<int> values;

values.resize(10);
```

当 `n > size()`：

* 创建新元素
* 必要时重新分配

当 `n < size()`：

* 销毁末尾元素
* 通常保留原有容量

```cpp
values.resize(5);

values.size();     // 5
values.capacity(); // 通常保持原值
```

#### 移动语义的影响

移动整个 `vector` 时，标准库通常可以直接转移内部缓冲区的所有权。

```cpp
std::vector<int> a(1'000'000);
std::vector<int> b = std::move(a);
```

在分配器条件允许时，这通常只需转移内部管理信息。

扩容过程中，元素类型的移动构造函数是否标记为 `noexcept` 会影响策略。

```cpp
struct Item {
    Item(const Item&);
    Item(Item&&) noexcept;
};
```

为了维护异常安全保证，`vector` 在部分情况下会优先复制可能抛异常的移动类型。

#### `clear` 与 `erase`

`clear()` 销毁全部元素并将 `size()` 设为零，通常保留容量。

```cpp
values.clear();

values.size();     // 0
values.capacity(); // 通常不变
```

`erase()` 删除指定元素，后续元素会向前移动，容量通常保持不变。

```cpp
values.erase(values.begin() + 3);
```

#### `shrink_to_fit`

`shrink_to_fit()` 请求释放未使用容量。

```cpp
values.shrink_to_fit();
```

它属于非强制性请求。实现可以：

* 重新分配到接近 `size()` 的容量
* 保持原容量
* 使迭代器、引用和指针失效

C++11 之前常使用临时对象交换：

```cpp
std::vector<int>(values).swap(values);
```

这个技巧通过创建紧凑副本后交换缓冲区来释放多余容量，但会产生复制或移动成本。

#### 迭代器失效

发生重新分配时，指向旧缓冲区的以下对象全部失效：

* 指针
* 引用
* 迭代器

```cpp
std::vector<int> values = {1, 2, 3};

int* ptr = &values[0];
values.push_back(4);

// 如果发生扩容，ptr 已失效
```

无重新分配的尾部插入通常保留已有元素的引用和迭代器，但 `end()` 会变化。

`erase` 会使删除位置及其后的迭代器失效。

#### `vector<bool>` 特化

`std::vector<bool>` 是标准库针对布尔值的空间压缩特化。

多个布尔值通常压缩存放在机器字的不同位中：

```text
普通 bool 数组：每个元素通常至少占 1 字节
vector<bool>：每个元素通常占 1 位
```

单个位通常无法提供普通 `bool&`，因此：

```cpp
std::vector<bool>::reference
```

是代理对象。它内部可能保存：

* 指向机器字的指针
* 位掩码或位索引

```cpp
std::vector<bool> flags = {true, false};

auto value = flags[0];
```

此时 `value` 通常推导为代理类型，仍然关联 `flags` 的底层存储。

需要独立布尔值时显式转换：

```cpp
bool value = flags[0];
```

修改元素可以使用代理引用：

```cpp
flags[0] = false;
```

保存代理对象后再让 `vector` 扩容、移动或销毁，代理对象可能悬垂。

```cpp
auto ref = flags[0];

flags.push_back(true); // 可能重新分配

// ref 的底层地址可能已经失效
```

---

###  迭代器与容器对象大小

#### 常规迭代器

在发布模式下，连续容器的迭代器经常封装原始指针：

```cpp
std::vector<int>::iterator
std::array<int, 10>::iterator
```

概念上可能类似：

```cpp
class iterator {
    int* ptr;
};
```

因此常见结果为：

```cpp
sizeof(std::vector<int>::iterator) == sizeof(int*)
```

标准只规定迭代器行为和能力，不规定其内部布局。

#### 调试模式迭代器

调试标准库可能给迭代器增加：

* 容器身份
* 边界信息
* 有效性状态
* 调试链表
* 线程或版本信息

因此调试模式下迭代器可能明显大于一个指针。

#### `vector<bool>::iterator`

`vector<bool>` 以位为单位访问元素，迭代器通常需要保存：

* 指向存储块的指针
* 当前位偏移

因此它通常无法直接表示为 `bool*`。

#### 关于三个指针断言

下面的断言依赖具体标准库实现：

```cpp
static_assert(
    sizeof(std::vector<int>) == 3 * sizeof(void*)
);
```

适合分析当前编译器实现，不适合作为可移植程序逻辑。

可靠结论包括：

* `vector` 元素连续存储。
* `data()` 指向首元素存储。
* `size()` 返回有效元素数量。
* `capacity()` 返回当前可容纳元素数量。
* 容器对象大小由实现决定。

---

##  模板与类设计

###  类模板基础

类模板允许同一数据结构适配不同元素类型。

```cpp
template<class T>
class Tensor4D {
public:
    using value_type = T;
};
```

使用方式：

```cpp
Tensor4D<float> a;
Tensor4D<double> b;
Tensor4D<int> c;
```

模板定义通常需要放在头文件中，因为编译器实例化模板时需要看到完整定义。

---


下面的示例使用固定四维形状和动态元素存储。

```cpp
#include <algorithm>
#include <array>
#include <cstddef>
#include <memory>
#include <stdexcept>
#include <type_traits>

template<class T>
class Tensor4D {
public:
    explicit Tensor4D(
        const std::size_t shape[4],
        const T* source = nullptr
    ) {
        std::copy_n(shape, 4, shape_);

        size_ = 1;

        for (std::size_t dim : shape_) {
            if (dim == 0) {
                throw std::invalid_argument(
                    "Tensor dimension must be greater than zero"
                );
            }

            size_ *= dim;
        }

        compute_strides();

        data_ = std::make_unique<T[]>(size_);

        if (source != nullptr) {
            std::copy_n(source, size_, data_.get());
        }
    }

    ~Tensor4D() = default;

    Tensor4D(const Tensor4D&) = delete;
    Tensor4D& operator=(const Tensor4D&) = delete;

    Tensor4D(Tensor4D&&) = delete;
    Tensor4D& operator=(Tensor4D&&) = delete;

    std::size_t size() const noexcept {
        return size_;
    }

    const std::size_t* shape() const noexcept {
        return shape_;
    }

    T* data() noexcept {
        return data_.get();
    }

    const T* data() const noexcept {
        return data_.get();
    }

private:
    void compute_strides() noexcept {
        strides_[3] = 1;
        strides_[2] = shape_[3];
        strides_[1] = shape_[2] * strides_[2];
        strides_[0] = shape_[1] * strides_[1];
    }

    std::size_t shape_[4]{};
    std::size_t strides_[4]{};
    std::size_t size_{};
    std::unique_ptr<T[]> data_;
};
```

#### 形状数组的深拷贝

```cpp
std::copy_n(shape, 4, shape_);
```

对于 `std::size_t` 这类可平凡复制类型，也可以使用：

```cpp
std::memcpy(shape_, shape, sizeof(shape_));
```

`std::copy_n` 更容易适配泛型代码和复杂类型。

#### 元素数据分配

```cpp
data_ = std::make_unique<T[]>(size_);
```

`std::unique_ptr<T[]>` 会在对象析构时自动调用 `delete[]`，并能提高构造异常时的资源安全性。

使用原始指针时需要手动管理：

```cpp
T* data_ = nullptr;

data_ = new T[size_];

~Tensor4D() {
    delete[] data_;
}
```

#### 禁止复制与移动

```cpp
Tensor4D(const Tensor4D&) = delete;
Tensor4D& operator=(const Tensor4D&) = delete;

Tensor4D(Tensor4D&&) = delete;
Tensor4D& operator=(Tensor4D&&) = delete;
```

适用场景：

* 对象绑定不可转移资源
* 对象地址必须稳定
* 内部存在外部注册关系
* 复制成本过高
* 设计上要求唯一实例

一般拥有动态资源的值类型也可以实现深拷贝和移动语义。禁止复制与移动会限制对象在标准容器和函数返回值中的使用。


---

##  算法：张量广播

###  广播规则

对于相同维数的两个张量，每个维度需要满足：

```text
shape_a[d] == shape_b[d]
或
shape_a[d] == 1
或
shape_b[d] == 1
```

输出维度通常取两者中的较大值：

```cpp
output_shape[d] = std::max(shape_a[d], shape_b[d]);
```

例如：

```text
A: [2, 3, 4, 5]
B: [1, 3, 1, 5]
输出: [2, 3, 4, 5]
```

`B` 在第 0 维和第 2 维广播。

###  四维连续张量步长

对于行主序连续布局：

```text
shape = [D0, D1, D2, D3]
```

步长为：

```text
stride[3] = 1
stride[2] = D3
stride[1] = D2 × D3
stride[0] = D1 × D2 × D3
```

坐标 `(i, j, k, l)` 的线性偏移：

```cpp
offset =
    i * stride[0] +
    j * stride[1] +
    k * stride[2] +
    l * stride[3];
```

###  手动广播索引

广播维度始终读取下标 0：

```cpp
std::size_t ai = shape_a[0] == 1 ? 0 : i;
std::size_t aj = shape_a[1] == 1 ? 0 : j;
std::size_t ak = shape_a[2] == 1 ? 0 : k;
std::size_t al = shape_a[3] == 1 ? 0 : l;
```

完整偏移：

```cpp
std::size_t offset_a =
    ai * stride_a[0] +
    aj * stride_a[1] +
    ak * stride_a[2] +
    al * stride_a[3];
```

###  使用有效步长优化

广播维度的坐标变化不会改变源数据位置，因此可以将对应步长设置为 0。

```cpp
std::size_t effective_stride_a[4];

for (int d = 0; d < 4; ++d) {
    effective_stride_a[d] =
        shape_a[d] == 1 ? 0 : stride_a[d];
}
```

随后直接计算：

```cpp
std::size_t offset_a =
    i * effective_stride_a[0] +
    j * effective_stride_a[1] +
    k * effective_stride_a[2] +
    l * effective_stride_a[3];
```

这会消除内层循环中的条件判断。

###  四层循环实现

```cpp
template<class T>
void add_broadcast_4d(
    const T* a,
    const std::size_t shape_a[4],
    const std::size_t stride_a[4],
    const T* b,
    const std::size_t shape_b[4],
    const std::size_t stride_b[4],
    T* output,
    const std::size_t output_shape[4]
) {
    std::size_t stride_a_effective[4];
    std::size_t stride_b_effective[4];

    for (int d = 0; d < 4; ++d) {
        const bool compatible =
            shape_a[d] == shape_b[d] ||
            shape_a[d] == 1 ||
            shape_b[d] == 1;

        if (!compatible) {
            throw std::invalid_argument(
                "Incompatible broadcast shapes"
            );
        }

        stride_a_effective[d] =
            shape_a[d] == 1 ? 0 : stride_a[d];

        stride_b_effective[d] =
            shape_b[d] == 1 ? 0 : stride_b[d];
    }

    std::size_t output_index = 0;

    for (std::size_t i = 0; i < output_shape[0]; ++i) {
        for (std::size_t j = 0; j < output_shape[1]; ++j) {
            for (std::size_t k = 0; k < output_shape[2]; ++k) {
                for (std::size_t l = 0; l < output_shape[3]; ++l) {
                    const std::size_t offset_a =
                        i * stride_a_effective[0] +
                        j * stride_a_effective[1] +
                        k * stride_a_effective[2] +
                        l * stride_a_effective[3];

                    const std::size_t offset_b =
                        i * stride_b_effective[0] +
                        j * stride_b_effective[1] +
                        k * stride_b_effective[2] +
                        l * stride_b_effective[3];

                    output[output_index++] =
                        a[offset_a] + b[offset_b];
                }
            }
        }
    }
}
```

###  单循环与除模反推

也可以使用单层循环遍历全部输出元素，再根据输出步长恢复四维坐标。

```cpp
for (std::size_t linear = 0; linear < total; ++linear) {
    std::size_t remaining = linear;

    std::size_t i = remaining / output_stride[0];
    remaining %= output_stride[0];

    std::size_t j = remaining / output_stride[1];
    remaining %= output_stride[1];

    std::size_t k = remaining / output_stride[2];
    remaining %= output_stride[2];

    std::size_t l = remaining;
}
```

优点：

* 代码结构统一
* 容易扩展为动态维数
* 便于并行划分线性区间

性能成本主要来自循环中的整数除法和取模运算。

固定四维场景通常适合：

* 嵌套循环
* 预计算有效步长
* 内层连续访问
* 将最连续维度放在最内层



###  PyTorch 广播机制原理

PyTorch 张量通常由以下信息描述：

* 数据存储
* 形状 `sizes`
* 步长 `strides`
* 存储偏移
* 数据类型
* 设备信息

广播视图可以通过修改元数据实现。

原始张量：

```text
shape  = [1, 3, 1, 5]
stride = [15, 5, 5, 1]
```

扩展为：

```text
shape  = [2, 3, 4, 5]
stride = [0, 5, 0, 1]
```

第 0 维和第 2 维步长为 0，因此这些维度的任意坐标都指向同一批底层元素。

这类扩展通常只创建视图，不复制元素数据。

手动实现中的：

```cpp
index = shape[d] == 1 ? 0 : output_index;
```

与零步长机制表达相同的地址映射关系。

#### `TensorIterator`

PyTorch 的许多逐元素运算通过统一迭代框架处理：

* 广播
* 数据类型转换
* 多输入和多输出
* 连续维度合并
* CPU 并行
* 向量化
* GPU 内核索引
* 不同内存布局

概念流程：

1. 检查输入形状是否兼容。
2. 计算共同输出形状。
3. 为广播维度生成零步长。
4. 合并可连续遍历的维度。
5. 根据设备和类型选择内核。
6. 并行遍历输出元素。

手动四维实现适合学习索引原理。通用框架通过统一元数据和内核调度处理更多数据类型、维度和设备。

---

##  现代 C++ 最佳实践与陷阱

###  `auto` 类型推导

#### 普通 `auto`

```cpp
const int value = 10;
const int& ref = value;

auto a = value; // int
auto b = ref;   // int
```

普通 `auto` 会剥离：

* 顶层 `const`
* 顶层引用

底层 `const` 通常会保留：

```cpp
const int* ptr = &value;

auto p = ptr; // const int*
```

#### `auto&`

```cpp
int value = 10;

auto& ref = value;
ref = 20;
```

`auto&` 保留引用关系。

对于只读访问：

```cpp
const auto& ref = value;
```

这可以避免大型对象复制，并延长临时对象生命周期。

```cpp
const auto& result = create_large_object();
```

#### `auto&&`

在类型推导上下文中，`auto&&` 可以绑定左值和右值。

```cpp
auto&& a = value;
auto&& b = create_object();
```

范围循环中常用：

```cpp
for (auto&& element : container) {
    // 同时适配普通引用和代理引用
}
```

#### `vector<bool>` 代理对象

```cpp
std::vector<bool> flags = {true, false};

auto x = flags[0];
```

`x` 可能是 `std::vector<bool>::reference`，继续关联容器存储。

需要独立值时：

```cpp
bool x = flags[0];
```

需要修改元素时：

```cpp
auto reference = flags[0];
reference = false;
```

范围遍历 `vector<bool>` 时，可以使用：

```cpp
for (auto&& bit : flags) {
    bit = true;
}
```

---

###  内存安全与生命周期

#### 常见悬垂来源

返回局部变量引用：

```cpp
const int& bad() {
    int value = 10;
    return value;
}
```

保存 `vector` 元素地址后触发扩容：

```cpp
int* ptr = &values[0];
values.push_back(42);
```

保存临时对象内部地址：

```cpp
const char* ptr = std::string("abc").c_str();
```

保存 `vector<bool>` 代理后改变底层存储：

```cpp
auto bit = flags[0];
flags.reserve(1000);
```

#### 生命周期管理原则

* 明确对象所有权。
* 使用 RAII 管理资源。
* 优先使用标准容器。
* 将只读非拥有访问表示为引用、指针或 `std::span`。
* 将独占所有权表示为 `std::unique_ptr`。
* 将共享所有权限制在确实需要共享生命周期的场景。
* 容器扩容后重新获取元素指针、引用和迭代器。

---

###  值语义与禁止复制

#### 值语义

值语义类型可以像普通数值一样复制、赋值和返回。

```cpp
std::vector<int> create_values() {
    return {1, 2, 3};
}
```

值语义通常带来：

* 清晰的所有权
* 易组合的接口
* 容器兼容性
* 异常安全
* 更简单的生命周期管理

#### 使用 `= delete`

```cpp
class Resource {
public:
    Resource(const Resource&) = delete;
    Resource& operator=(const Resource&) = delete;
};
```

适用对象包括：

* 锁
* 文件映射
* 操作系统句柄包装
* 注册到外部系统的对象
* 地址必须固定的对象
* 单例或作用域守卫

#### 移动语义

移动语义允许将资源所有权从一个对象转移到另一个对象。

```cpp
class Buffer {
public:
    explicit Buffer(std::size_t size)
        : size_(size),
          data_(std::make_unique<int[]>(size)) {}

    Buffer(const Buffer&) = delete;
    Buffer& operator=(const Buffer&) = delete;

    Buffer(Buffer&&) noexcept = default;
    Buffer& operator=(Buffer&&) noexcept = default;

private:
    std::size_t size_;
    std::unique_ptr<int[]> data_;
};
```

移动后，源对象仍然处于有效且可析构的状态，其具体内容由类型约定决定。

#### Rule of Zero

优先让标准库资源类型负责析构、复制和移动。

```cpp
class Tensor {
private:
    std::array<std::size_t, 4> shape_;
    std::vector<float> data_;
};
```

编译器可以自动生成正确的：

* 析构函数
* 复制构造函数
* 复制赋值运算符
* 移动构造函数
* 移动赋值运算符

这类设计通常比直接管理 `new[]` 和 `delete[]` 更安全。

---
