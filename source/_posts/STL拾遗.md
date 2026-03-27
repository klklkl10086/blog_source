---
title: STL拾遗
date: 2026-01-31 20:50:18
tags: ["CPP","STL"]
categories: ["研究生补完"]
description: 复习一下stl相关的内容
---



# std::vector
**动态数组**
## 初始化
```cpp
 std::vector<int> a(10,1);//size=10  初值为1
 std::vector<std::vector<int>>b(n+1,std::vector<int>(m+1,0));//n+1 *  m+1  初值为0
 std::vector<int>c=a;
 
 //新特性
 std::vector<int> a{1,2,1,1,1};
 std::vector b(n+1,std::vector(m+1,0));
```
在局部函数中创建数组，是在栈中开空间，但是创建vector是在堆里开空间，因此不可开辟过长的数组，会爆栈。

## 方法函数

### 基本操作

| 方法 | 说明 | 示例 |
|------|------|------|
| `push_back(value)` | 末尾添加元素 | `v.push_back(10)` |
| `pop_back()` | 删除末尾元素 | `v.pop_back()` |
| `size()` | 获取元素个数 | `int n = v.size()` |
| `empty()` | 判断是否为空 | `if (v.empty())` |
| `clear()` | 清空所有元素 | `v.clear()` |

### 元素访问

| 方法 | 说明 | 示例 |
|------|------|------|
| `[index]` | 随机访问（无边界检查） | `int x = v[0]` |
| `at(index)` | 随机访问（有边界检查） | `int x = v.at(0)` |
| `front()` | 访问第一个元素 | `int first = v.front()` |
| `back()` | 访问最后一个元素 | `int last = v.back()` |

### 容量管理

| 方法 | 说明 | 示例 |
|------|------|------|
| `reserve(n)` | 预分配容量 | `v.reserve(100)` |
| `capacity()` | 获取当前容量 | `int cap = v.capacity()` |
| `shrink_to_fit()` | 释放多余容量 | `v.shrink_to_fit()` |

### 插入删除

| 方法 | 说明 | 示例 |
|------|------|------|
| `insert(pos, value)` | 指定位置插入 | `v.insert(v.begin()+2, 99)` |
| `erase(pos)` | 删除指定位置 | `v.erase(v.begin()+2)` |
| `erase(first, last)` | 删除范围 | `v.erase(v.begin(), v.begin()+3)` |
| `resize(n)` | 调整大小 | `v.resize(10)` |

### 迭代器

| 方法 | 说明 | 示例 |
|------|------|------|
| `begin()` | 起始迭代器 | `auto it = v.begin()` |
| `end()` | 结束迭代器 | `for (; it != v.end(); ++it)` |
| `rbegin()` | 反向起始 | `auto rit = v.rbegin()` |
| `rend()` | 反向结束 | `for (; rit != v.rend(); ++rit)` |

**注意事项**
1. end（）返回的时最后一个元素的最后一个位置的地址，不是最后一个元素的地址，所有STL容器都是这样
2. 使用 `vi.resize(n, v) `函数时，若 vi 之前指定过大小为 pre

    pre > n ：即数组大小变小了，数组会保存前 n 个元素，前 n 个元素值为原来的值，不是都为 v
    pre < n ：即数组大小变大了，数组会在后面插入 n - pre 个值为 v 的元素
    也就是说，这个初始值 v 只对新插入的元素生效。

**示例：** 
```cpp
#include <vector>
#include <iostream>

int main() {
    // 1. 创建vector
    std::vector<int> v = {1, 2, 3, 4, 5};
    
    // 2. 遍历（现代C++）
    for (int num : v) {
        std::cout << num << " ";
    }
    
    // 3. 添加元素
    v.push_back(6);           // 添加6到末尾
    v.emplace_back(7);        // 更高效的添加（C++11）
    
    // 4. 删除元素
    v.pop_back();            // 删除最后一个
    v.erase(v.begin() + 2);  // 删除第3个元素（下标2）
    
    // 5. 插入元素
    v.insert(v.begin() + 1, 99);  // 在第2个位置插入99
    
    // 6. 容量操作
    if (v.size() > v.capacity() / 2) {
        v.reserve(v.capacity() * 2);  // 预分配更多空间
    }
    
    // 7. 安全访问
    try {
        int val = v.at(100);  // 抛出std::out_of_range异常
    } catch (const std::out_of_range& e) {
        std::cout << "索引越界!";
    }
    
    // 8. 快速访问
    int first = v[0];  // 快速但不安全
    int last = v.back();
    
    return 0;
}
```
---


## 内存管理
vector 里面有两个变量 size （指数组实际长度大小）和 capacity（指数组分配的内存空间容量大小）。

**机制**：当长度大于容量时，vector会自动进行扩容。
**扩容规则为**：vector会重新开辟新的内存空间（大小为原来的capacity的2倍），原来的vector中存储内容先copy到新的地址空间中，然后销毁原来的地址空间。
一个减少内存拷贝的思路是：使用reserve提前分配固定的空间大小（必须知道分配空间大小的上限）

# std::stack

## 方法函数


### 1. 构造与初始化
| 方法 | 说明 | 示例 |
|------|------|------|
| `stack<T> s` | 创建空栈（默认使用deque） | `stack<int> s1;` |
| `stack<T, Container> s` | 指定底层容器 | `stack<int, vector<int>> s2;` |
| `stack<T> s(container)` | 用已有容器初始化（C++11） | `stack<int> s3(deque);` |

```cpp
#include <stack>
#include <vector>
#include <deque>

// 创建栈的不同方式
std::stack<int> s1;                     // 默认使用deque
std::stack<int, std::vector<int>> s2;   // 使用vector作为底层容器
std::stack<int, std::list<int>> s3;     // 使用list作为底层容器
```

### 2. 元素访问
| 方法 | 说明 | 时间复杂度 |
|------|------|------------|
| `top()` | 返回栈顶元素的引用 | O(1) |

```cpp
std::stack<int> s;
s.push(10);
s.push(20);
s.push(30);

int top_element = s.top();  // 返回30，但不删除
std::cout << "栈顶元素: " << top_element << std::endl;  // 输出30
```

### 3. 容量操作
| 方法 | 说明 | 时间复杂度 |
|------|------|------------|
| `empty()` | 检查栈是否为空 | O(1) |
| `size()` | 返回栈中元素个数 | O(1) |


### 4. 修改操作
| 方法 | 说明 | 时间复杂度 |
|------|------|------------|
| `push(const T& value)` | 将元素压入栈顶 | O(1) |
| `push(T&& value)` | 移动元素压入栈顶（C++11） | O(1) |
| `emplace(Args&&... args)` | 在栈顶就地构造元素（C++11） | O(1) |
| `pop()` | 移除栈顶元素（不返回值） | O(1) |

```cpp
std::stack<std::string> s;

// 压入元素
s.push("Hello");
s.push("World");

// 使用emplace（直接构造，避免拷贝）
s.emplace("C++");  // 在栈顶构造字符串"C++"

// 查看和弹出
while (!s.empty()) {
    std::cout << "栈顶: " << s.top() << std::endl;
    s.pop();  // 弹出栈顶元素
}
// 输出顺序: C++ → World → Hello
```

### 5. 交换操作
| 方法 | 说明 | 时间复杂度 |
|------|------|------------|
| `swap(stack& other)` | 交换两个栈的内容（C++11） | O(1) |

```cpp
std::stack<int> s1, s2;
s1.push(1); s1.push(2);
s2.push(3); s2.push(4);

s1.swap(s2);  // 交换两个栈的内容
// 现在s1包含3,4，s2包含1,2
```





# std::queue




## 方法函数
### 1. 元素访问
| 方法 | 说明 | 时间复杂度 | 示例 |
|------|------|------------|------|
| `front()` | 返回队头元素的引用 | O(1) | `int first = q.front();` |
| `back()` | 返回队尾元素的引用 | O(1) | `int last = q.back();` |

### 2. 容量操作
| 方法 | 说明 | 时间复杂度 | 示例 |
|------|------|------------|------|
| `empty()` | 检查队列是否为空 | O(1) | `if (q.empty())` |
| `size()` | 返回队列中元素个数 | O(1) | `int n = q.size();` |

### 3. 修改操作
| 方法 | 说明 | 时间复杂度 | 示例 |
|------|------|------------|------|
| `push(const T& value)` | 在队尾插入元素 | O(1) | `q.push(10);` |
| `push(T&& value)` | 在队尾移动插入元素（C++11） | O(1) | `q.push(std::move(obj));` |
| `emplace(Args&&... args)` | 在队尾就地构造元素（C++11） | O(1) | `q.emplace(1, 2, 3);` |
| `pop()` | 移除队头元素（不返回值） | O(1) | `q.pop();` |

### 4. 交换操作
| 方法 | 说明 | 时间复杂度 | 示例 |
|------|------|------------|------|
| `swap(queue& other)` | 交换两个队列的内容（C++11） | O(1) | `q1.swap(q2);` |

---

## 实用示例代码



###  使用 emplace 避免拷贝
```cpp
#include <queue>
#include <string>

struct Person {
    std::string name;
    int age;
    Person(std::string n, int a) : name(std::move(n)), age(a) {}
};

int main() {
    std::queue<Person> q;
    
    // push 需要拷贝构造
    Person p1("Alice", 25);
    q.push(p1);
    
    // emplace 直接构造，避免拷贝
    q.emplace("Bob", 30);  // 直接在队列中构造对象
    
    return 0;
}
```
# std::deque
首尾都可以插入或者删除的双端队列



## 方法函数

### 1. 构造与初始化
| 方法 | 说明 | 示例 |
|------|------|------|
| `deque<T> d` | 创建空deque | `deque<int> d1;` |
| `deque<T> d(n, val)` | 创建n个val的deque | `deque<int> d2(5, 10);` |
| `deque<T> d(begin, end)` | 用迭代器范围构造 | `deque<int> d3(v.begin(), v.end());` |
| `deque<T> d(init_list)` | 初始化列表构造（C++11） | `deque<int> d4{1, 2, 3};` |

### 2. 元素访问
| 方法 | 说明 | 时间复杂度 | 示例 |
|------|------|------------|------|
| `operator[]` | 随机访问（无边界检查） | O(1) | `int x = d[2];` |
| `at(index)` | 随机访问（有边界检查） | O(1) | `int x = d.at(2);` |
| `front()` | 访问第一个元素 | O(1) | `int first = d.front();` |
| `back()` | 访问最后一个元素 | O(1) | `int last = d.back();` |

### 3. 容量操作
| 方法 | 说明 | 时间复杂度 | 示例 |
|------|------|------------|------|
| `empty()` | 检查是否为空 | O(1) | `if (d.empty())` |
| `size()` | 返回元素个数 | O(1) | `int n = d.size();` |
| `max_size()` | 返回最大可能元素数 | O(1) | `int max = d.max_size();` |
| `shrink_to_fit()` | 请求减少内存使用（C++11） | O(n) | `d.shrink_to_fit();` |

### 4. 修改器 - 两端操作
| 方法 | 说明 | 时间复杂度 | 示例 |
|------|------|------------|------|
| `push_back(val)` | 在末尾添加元素 | O(1) | `d.push_back(10);` |
| `push_front(val)` | 在开头添加元素 | O(1) | `d.push_front(5);` |
| `pop_back()` | 删除末尾元素 | O(1) | `d.pop_back();` |
| `pop_front()` | 删除开头元素 | O(1) | `d.pop_front();` |
| `emplace_back(args)` | 在末尾就地构造（C++11） | O(1) | `d.emplace_back(1,2,3);` |
| `emplace_front(args)` | 在开头就地构造（C++11） | O(1) | `d.emplace_front("hello");` |

### 5. 修改器 - 中间操作
| 方法 | 说明 | 时间复杂度 | 示例 |
|------|------|------------|------|
| `insert(pos, val)` | 在指定位置插入元素 | 平均O(n) | `d.insert(d.begin()+2, 99);` |
| `erase(pos)` | 删除指定位置元素 | 平均O(n) | `d.erase(d.begin()+2);` |
| `erase(begin, end)` | 删除指定范围 | 平均O(n) | `d.erase(d.begin(), d.begin()+3);` |
| `clear()` | 清空所有元素 | O(n) | `d.clear();` |
| `resize(n)` | 调整大小 | O(n) | `d.resize(10);` |

### 6. 迭代器
| 方法 | 说明 | 示例 |
|------|------|------|
| `begin()`/`end()` | 正向迭代器 | `for (auto it = d.begin(); it != d.end(); ++it)` |
| `rbegin()`/`rend()` | 反向迭代器 | `for (auto it = d.rbegin(); it != d.rend(); ++it)` |
| `cbegin()`/`cend()` | const正向迭代器（C++11） | `auto it = d.cbegin();` |
| `crbegin()`/`crend()` | const反向迭代器（C++11） | `auto it = d.crbegin();` |

### 7. 交换操作
| 方法 | 说明 | 时间复杂度 | 示例 |
|------|------|------------|------|
| `swap(other)` | 交换两个deque的内容 | O(1) | `d1.swap(d2);` |
| `std::swap(d1, d2)` | 非成员交换函数 | O(1) | `std::swap(d1, d2);` |

---


###  基本使用
```cpp
#include <iostream>
#include <deque>

int main() {
    std::deque<int> d;
    
    // 两端插入
    d.push_back(3);     // [3]
    d.push_front(2);    // [2, 3]
    d.push_back(4);     // [2, 3, 4]
    d.push_front(1);    // [1, 2, 3, 4]
    
    // 访问元素
    std::cout << "第一个: " << d.front() << std::endl;   // 1
    std::cout << "最后一个: " << d.back() << std::endl;  // 4
    std::cout << "中间: " << d[2] << std::endl;          // 3
    
    // 两端删除
    d.pop_front();      // [2, 3, 4]
    d.pop_back();       // [2, 3]
    
    // 遍历
    for (int num : d) {
        std::cout << num << " ";  // 2 3
    }
    
    return 0;
}
```


###  插入和删除示例
```cpp
#include <iostream>
#include <deque>

int main() {
    std::deque<int> d = {10, 20, 30, 40};
    
    // 在位置2（第三个元素）插入99
    auto it = d.begin() + 2;
    d.insert(it, 99);  // [10, 20, 99, 30, 40]
    
    // 删除位置3（第四个元素）
    d.erase(d.begin() + 3);  // [10, 20, 99, 40]
    
    // 删除范围
    d.erase(d.begin() + 1, d.begin() + 3);  // [10, 40]
    
    // 调整大小
    d.resize(5, 0);  // [10, 40, 0, 0, 0]
    
    for (int num : d) {
        std::cout << num << " ";
    }
    
    return 0;
}
```



### 与vector的对比

| 特性 | std::deque | std::vector |
|------|------------|-------------|
| **存储连续性** | 分块存储，不保证连续 | 保证连续存储 |
| **随机访问** | 支持，O(1) | 支持，O(1) |
| **头部插入** | O(1) | O(n) |
| **尾部插入** | O(1) | 平均O(1)，可能重新分配 |
| **中间插入** | O(n) | O(n) |
| **内存管理** | 更复杂，分块 | 简单，连续块 |
| **迭代器失效** | 插入可能使所有迭代器失效 | 插入可能使所有迭代器失效 |

**常数因子比较大**

# std::priority_queue 优先队列

最大堆 最小堆