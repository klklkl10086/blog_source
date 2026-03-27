---
layout: pose
title: Python基础知识
date: 2024-01-14 15:15:19
tags: Python
categories: Python
description: python基础语法记录
---

#  基本知识

## 字面量

> 在代码中，被写下来的固定的值

**常见的字面量数据类型**

- 数字        整数  浮点数  复数 布尔
- 字符串      双引号包围 "字符串"
- 列表
- 元组
- 集合
- 字典

```python
# 字面量（有空格）
print("hello world")#字符串
print(12) #整数
print(1.0) #浮点数
print("钱包还有:", money, "收了一块钱还剩:", money+1) # 输出多个变量
```

写在print语句中的是字面量

## 注释

**单行注释**

```python
# 我是单行注释（建议有空格）
```

**多行注释**

```python
"""我是多行注释一般用于开头解释类和程序
三个引号开头，三个引号结尾，可以换行

  """
```



## 变量

> 记录数据的盒子,值可以改变 

```python
# 变量名 = 变量值
money = 52
print("钱包还有:", money, "\n收了一块钱还剩:", money+1)
money = money-10 #  + -  *  /
```



## 数据类型

> 变量没有类型，**变量中存储的数据**有类型

**type()语句**

> 用于查看**数据**的类型的函数

**使用print直接输出**

```python
print(type("str"))
money = 52
print(type(money))
```

**用变量存储返回的结果**

```python
str_type = (type("123456"))
money = 52
money_type = (type(money))
```

**数据类型的转换**

```python
# 转为整数
int(x) 
num = int("11")# 保字符串里都是数字
int_float = int(11.5)

# 转为浮点
float(x)
float_int = float(11)
# 转为字符串
str(x)
float_str = str(111.34)
```

>任何语句都可转换成字符串

## 标识符

> **名字**

**命名规则**

- 英文  大小写敏感
- 中文  不推荐使用
- 数字  不可以作为开头
- 下划线 _  
- 不可以使用关键字

## 运算符

**数学运算符**

| 运算符 |  操作  |
| :----: | :----: |
|   +    |  加法  |
|   -    |  减法  |
|   *    |  乘法  |
|   /    |  除法  |
|   //   | 取整除 |
|   %    | 取余数 |
|   **   |  指数  |

**赋值运算符**

| 运算符 | 操作 |
| :----: | :--: |
|   =    | 赋值 |

**复合赋值运算符**

| 运算符 |          操作          |
| :----: | :--------------------: |
|   +=   |   c+=a  等价于 c=c+a   |
|   -=   |   c-=a  等价于 c=c-a   |
|   *=   |  c\*=a  等价于 c=c*a   |
|   /=   |   c/=a  等价于 c=c/a   |
|   %=   |   c%=a  等价于 c=c%a   |
|  **=   | c**=a  等价于 c=c *\*a |
|  //=   |  c//=a  等价于 c=c//a  |

## 字符串

**定义**

- 单引号

  ```python
   name='hhhh'
  ```

  **可以内含双引号**

  

- 双引号

  ```python
  name2 = "hhhhhh2"
  ```

  **可以内含单引号**

  

- 三引号

  ```python
  # 和多行注释一样
  name3 = """hhhhh
  hhh3"""
  ```

>**可以用 \ 解除效用 变成普通字符串**

```python
name = '"123456'
name = "'12345'"
name = "\"123456"
```



**字符串拼接**

> 使用+号

```python
print("123"+"456")
name = "987"
print("12345" + name + "564")
tel = 132456
# print("111111" + tel +"454") error
```

**字符串没有办法和其他类型拼接**



**字符串格式化**

**方法一：**

```python
name = "kjkjk"
where = "at kl"
message = "abced %s %s" % (name, where)
print(message)

# 输出： abced kjkjk at kl
```



**通过占位的形式完成拼接，%表示占位，s表示将变量变成字符串放入占位的地方**



| 格式符号 | 转化                         |
| -------- | ---------------------------- |
| %s       | 转化为**字符串**放入占位位置 |
| %d       | 转化为**整数**放入占位位置   |
| %f       | 转化为**浮点**放入占位位置   |



**方法二:**

**不限数据类型，不做精度控制，适合对精度没有要求时快速使用**

```python
f"...{变量} "
```



```python
num1=11
name = "klklklk"

print(f"my name is {name} ,and age is {num1}")
'''
输出：
my name is klklklk ,and age is 11
'''
```



**格式化的精度控制**

>m.n 控制数度的宽度和精度，m控制宽度，**但当宽度小于自身时不生效**，n控制精度会进行**四舍五入**



```python
num1=11
num2=11.345

print("数字11宽度5：%5d\n" % num1)
print("数字11宽度1：%1d\n" % num1)
print("数字11.345宽度7，精度2：%7.2f\n" % num2)
print("数字11.345宽度不限，精度2: %.2f" % num2)
print("数字11.345精度不限，宽度2: %2f" % num2)
'''
输出：

数字11宽度5：   11

数字11宽度1：11

数字11.345宽度7，精度2：  11.35

数字11.345宽度不限，精度2: 11.35
数字11.345精度不限，宽度2: 11.345000

'''
```





**表达式格式化**

>表达式：一条具有明确执行结果的代码语句

```python
print("1 * 1 = %d" % (1*1))
print(f"1 * 2 = {1*2}")
print("字符串在python的类型名是：%s" % type("字符串"))

'''
输出:
1 * 1 = 1
1 * 2 = 2
字符串在python的类型名是：<class 'str'>
'''
```



## 数据输入



**input语句**



```python
print("what is your name?")
name = input()
print(f"you name is {name}")
```



等价于：



```python
name = input("what is your name?\n")
print(f"you name is {name}")
```

**input语句不管输入什么都统统当作字符串看待，可自行进行数据转换**



```python
age = input("what is your age?\n")
print("age is", type(age))
'''
输出：

what is your age?
 输入： 18
age is <class 'str'>
'''
```



# 判断语句



## 布尔类型和比较运算符

布尔类型的字面量：

True ：表示真

False：表示假



比较运算符：

> == , > , < , >= ,<= ,!=



```python
bool_1 = True
bool_2 = False
print(f"bool1 is{type(bool_1)},bool2 is {type(bool_2)}")
'''
输出：

bool1 is<class 'bool'>,bool2 is <class 'bool'>
'''
```



```python
num1 = 10
num2 = 10
num3 = 15
print(f"num1 == num2 is {num1 == num2}")
print(f"num1 != num3 is {num1 != num3}")
'''
输出：
num1 == num2 is True
num1 != num3 is True
'''
```



**字符串也可以进行 == ，! = 比较**

## if语句



if [条件] ：

​		条件成立时执行的内容



```python
age = 18
print(f"my age is {age}")
if age >= 18:
    print("i am a adult")
    print("i will go to university")
print("time fly quickly!")

'''
输出：

my age is 18
i am a adult
i will go to university
time fly quickly!
'''
```

**缩进！！！**



```python
age = 10
print(f"my age is {age}")
if age >= 18:
    print("i am a adult")
    print("i will go to university")
print("time fly quickly!")

'''
输出：
my age is 10
time fly quickly!
'''
```



## if else语句

>if 条件：
>
>​		条件成立时执行的内容
>
>else：
>
>​		条件不满足时执行的内容



```python
age = 10
print(f"my age is {age}")
if age >= 18:
    print("i am a adult.")
    print("i will go to university.")
else:
    print("i am a child.")
    print("i am going to senior high school.")
print("time fly quickly!")

'''
输出：
my age is 10
i am a child.
i am going to senior high school.
time fly quickly!
'''
```



## if elif else语句

>if 条件：
>
>​			 条件1成立时执行的内容
>
>elif 条件2:
>
>    		条件2成立时执行的内容
>
>elif 条件n：
>    		条件 n成立时执行的内容
>
>else：
>
>​			 上述条件都不满足时执行的内容
>
>



```python
height = int(input("请输入你的身高（cm）："))
vip_level = int(input("您的vip等级是："))

if height<120:
    print("小于120cm 可以免费")
elif vip_level>3:
    print("vip>3 可以免费")
else:
    print("收费10元")
```

**多条件判断下，条件互斥，只要有一个条件满足，则其他条件不成立，语句不执行**



```python
if int(input("请输入你的身高（cm）："))<120:
    print("小于120cm 可以免费")
elif int(input("您的vip等级是："))>3:
    print("vip>3 可以免费")
else:
    print("收费10元")
```



## 判断语句的嵌套

> if  条件1:
>
> ​				 条件1成立时执行的内容
>
> ​				 条件1成立时执行的内容
>
> ​				if 条件2:
>
> ​								 条件2成立时执行的内容
>
> ​								 条件2成立时执行的内容

not表示取反

# 循环语句

## while循环

> while 条件:
> 				条件满足要做的事情1
>
> ​				条件满足要做的事情2
>
> ​				条件满足要做的事情3

```python
i = 0
while i<10:
    print("this is %d"% i)
    i= i+1
```

```python
i = 1
sum=0
while i<=100:
    sum+=i
    i= i+1
print("sum=%d"%sum)
```

小脚本：

猜数字，猜错判断大于小于，猜对输出猜的次数

```python
import random
num = random.randint(1, 100)
i = 0
flag = True
while flag:
    i = i + 1
    guess_num = int(input("what is it?"))
    if guess_num == num:
        flag = False
        print("you are right")
    else:
        if guess_num > num:
            print("you are bigger")
        else:
            print("you are smaller")
print(f"the times is {i}")
```

**嵌套**

> while 条件1:
> 				条件1满足要做的事情1
>
> ​				条件1满足要做的事情2
>
> ​				条件1满足要做的事情3
>
> ​				.....
>
> ​				while 条件2:
> ​				条件2满足要做的事情1
>
> ​				条件2满足要做的事情2
>
> ​				条件2满足要做的事情3
>
> ​				.....

小脚本：

打印九九乘法表

前置知识：

```python
#print输出如何不换行
print("hello", end='')
```

脚本：

```python
lh = 1
rh = 1
while rh<=9:
    lh=1
    while lh<=rh:
        print("%d * %d = %d "%(lh,rh,lh*rh), end='')
        lh+=1
    rh+=1
    print()#输出空内容 换行
```



## for循环

> for **临时变量** in 待处理的数据集:
>
> ​		循环条件满足时候执行的代码

```python
name = "abcdefg"
for x in name:
	print(x)
'''
输出：
a
b
c
d
e
f
g

'''
```

**无法自定义无限循环，数据集不可能无限大**

小脚本：
统计字符串中有多少个字母a

```python
str = input("please input your str")
count = 0
for x in str:
    if x == 'a':
        count += 1
print(count)
```



**tips:**

>关于临时变量的作用范围，规范上，临时变量是不能在**for循环外部**进行访问，但是实际上，是可以访问到的



**range语句**

获得一个数字序列，搭配for循环食用

>  range(num)
>
> 获取一个从0 开始到num结束的数字序列（不包含num本身）

>  range(num1，num2)
>
> 获取一个从num1开始到num2结束的数字序列（不包含num2本身）

> range(num1，num2，step)
>
> 获取一个从num1开始到num2结束的数字序列（不包含num2本身）,数字间的步长以step为标准，step默认为1

```python
for x in range(10):
    print(x)
'''
0
1
2
3
4
'''
```

```python
for x in range(2,8):
    print(x)
'''
2
3
4
5
6
7
'''
```

```python
for x in range(2,8,2):
    print(x)
'''
2
4
6
'''
```

**for循环嵌套**

> 控制空格缩进
>
> for **临时变量1** in 待处理的数据集:
>
> ​		循环条件1满足时候执行的代码
>
> ​		for **临时变量2** in 待处理的数据集:
>
> ​		  	循环条件2满足时候执行的代码

**for循环和while循环可以互向嵌套**

小脚本：
使用for循环打印九九乘法表

```python
for rh in range(1,10):
    for lh in range(1,rh+1):
        print(f"{lh}*{rh}={lh*rh}\t", end='')
    print()
```

## 循环中断

 

**continue**

> 中断所在本层循环，直接进入下一次循环

```python
for i in range(1,100):
	语句1
    continue
    语句2

```

跳过语句2，不执行

**break**

> 直接结束所在本层循环



# 函数

封装特定功能，实现接口，避免重复性劳动，可以重复使用

```python
# 内置函数 统计字符串长度
len()

# 自定义函数 实现统计字符串长度
def my _len(data):
    count = 0
    for i in data:
        dount+=1
    print(f"字符串{data}的长度是:{count}")
    
```

## 定义

> def 函数名字(传入参数)**:**
>
> ​		函数体
>
> ​		return 返回值

```python
def say_hi():# 可以没有传入参数
    print("hi i am klklkl")
    #可以没有返回值
```

先定义，再使用，在程序中调用函数才可以进行工作

```python
def say_hi():
    print("hi i am klklkl")
    
say_hi()
'''
hi i am klklkl
'''
```

```python
def add(x,y):
	return x+y
add(4,5)
'''
9
'''
```

上述例子中，x和y是形式参数，4和5是实际参数

没有返回值，则返回值类型为NoneType，表示空，无意义，false

**None的应用**

- 函数的返回值

- if判断语句
- 声明无初始内容的变量

函数可以嵌套调用，过程类似于栈

## 多个返回值

python的函数可以实现一次性返回多个值

> return 返回值1，返回值2
>
> 变量1，变量2 = 函数

```python
def test1(x,y):
    return x-1,y+1
res1,res2 = test1(0,5)
print(res1)
print(res2)
'''
-1
6
'''
```

##  传入参数

### 位置参数

![image-20240124000603415](image-20240124000603415.png)

### 关键字参数

![image-20240124000631318](image-20240124000631318.png)

### 缺省参数

![image-20240124000828120](image-20240124000828120.png)



### 不定长参数

**位置传递的不定长**

![image-20240124001036657](image-20240124001036657.png)



**关键字传递**

![image-20240124001119731](image-20240124001119731.png)

### 函数作为参数传递

![image-20240124001429469](image-20240124001429469.png)

传递的是计算逻辑

## 匿名函数

![image-20240124001931614](image-20240124001931614.png)

> lambda 传入参数: 函数体（只能有一行代码）

![image-20240124002113484](image-20240124002113484.png)

![image-20240124002424908](image-20240124002424908.png)



# 数据容器

> 一种可以容纳多份数据的数据类型

根据特点的不同可以划分为

- 列表
- 元组
- 字符串
- 集合
- 字典

## 列表（list）

### 定义

> 变量名 = [元素1,元素2,....]

**空列表：**

> 变量名 = []
>
> 变量名 = list()

**列表中的每个数据叫作元素**

```python
name_list = ["name1", "name2", "name3"]
com_list = ["name1", 14, 2004]
none_list = []
print(name_list)
print(type(name_list))
print(com_list)
print(none_list)
'''
['name1', 'name2', 'name3']
<class 'list'>
['name1', 14, 2004]
[]
'''
```

**也可以嵌套列表**

```python
my_list = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
print(my_list)
print(type(my_list))
'''
[[1, 2, 3], [4, 5, 6], [7, 8, 9]]
<class 'list'>

'''
```

### 元素索引

> 利用下标索引进行取用
>
> 正向：从左到右，从前向后，从0开始，依次递增
>
> 负向：从右向左，从后向前，从-1开始，依次递减
>
> 不可以超出范围

```python
my_list = ["zhangsan", "lisi", "wangwu"]
print(my_list[0])
'''
zhangsan

'''
```

```python
my_list = ["zhangsan", "lisi", "wangwu"]
print(my_list[-1])
'''
wangwu

'''
```

**嵌套列表**

> 多层下标索引即可遍历,不可以超出范围

```python
my_list = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
print(my_list[0][2])
print(my_list[-1][1])
print(my_list[-2][-1])
'''
3
8
6

'''
```

### 常用方法

> class中的内置函数

#### 查询

> 查询指定元素在列表中的下标(正向索引)，如果找不到就报错
>
> 列表.index(元素)

```python
my_list = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
index = my_list.index([4,5,6])
print(index)
'''
1

'''
```

#### 修改

> 修改指定下标位置的值
>
> 列表[下标] = 值
>
> 可以正向，也可以反向

```python
my_list = ["zhangsan", "lisi", "wangwu"]
print(my_list[0])
my_list[0] = "zhangsi"
print(my_list[0])
'''
zhangsan
zhangsi
'''
```

#### 插入

> 在指定下标索引位置插入指定元素
>
> 列表.insert(下标,元素)

```python
my_list = ["zhangsan", "lisi", "wangwu"]
my_list.insert(2, "zhaoliu")
print(my_list)
'''
['zhangsan', 'lisi', 'zhaoliu', 'wangwu']

'''
```

#### 追加

> 在列表尾部添加元素

**追加一个元素：**

> 列表.append(元素)

```python
my_list = ["zhangsan", "lisi", "wangwu"]
my_list.append(1234)
print(my_list)
'''
['zhangsan', 'lisi', 'wangwu', 1234]

'''
```

```python
my_list = ["zhangsan", "lisi", "wangwu"]
new_list = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
my_list.append(new_list)
print(my_list)
'''
['zhangsan', 'lisi', 'wangwu', [[1, 2, 3], [4, 5, 6], [7, 8, 9]]]

'''
```

**追加一批元素（新的列表）：**

> 列表1.extend(列表2)

```python
my_list = ["zhangsan", "lisi", "wangwu"]
new_list = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
my_list.extend(new_list)
print(my_list)
'''
['zhangsan', 'lisi', 'wangwu', [1, 2, 3], [4, 5, 6], [7, 8, 9]]

'''
```

#### 删除

> del列表[下标]

```python
my_list = ["zhangsan", "lisi", "wangwu"]
del my_list[1]
print(my_list)
'''
['zhangsan', 'wangwu']

'''
```

> 列表.pop(下标)
>
> 会返回对应下标的元素内容

```python
my_list = ["zhangsan", "lisi", "wangwu"]
print(my_list.pop(2))
print(my_list)
'''
wangwu
['zhangsan', 'lisi']

'''
```

**删除某元素在列表中的第一个匹配项**

> 列表.remove(元素)

```python
my_list = ["zhangsan", "lisi", "wangwu", "zhangsan"]
my_list.remove("zhangsan")
print(my_list)
'''
['lisi', 'wangwu', 'zhangsan']

'''
```

**清空**

> 列表.clear()

```python
my_list = ["zhangsan", "lisi", "wangwu", "zhangsan"]
my_list.clear()
print(my_list)
'''
[]

'''
```

 **统计元素个数**

> 统计指定元素在列表中的个数
>
> 列表.count(元素)
>
> 返回值即为数量

```python
my_list = ["zhangsan", "lisi", "wangwu", "zhangsan"]
print(my_list.count("zhangsan"))
'''
2
'''
```

**列表元素的数量**

> len(列表)
>
> 返回值即为数量
>
> 不是list内部的函数

```python
my_list = ["zhangsan", "lisi", "wangwu", "zhangsan"]
print(len(my_list))
'''
4
'''
```

### 特点

1. **列表有上限，但上限很大**
2. **可以容纳不同类型的元素**
3. **数据有序存储**
4. **允许重复数据存在**
5. **可以修改**



### 循环遍历

**while循环遍历**

**下标索引**的方式进行取用元素

```python
my_list = ["zhangsan", "lisi", "wangwu", "zhangsan"]
index = 0
while index<len(my_list):
    x = my_list[index]
    print(x)
    index += 1
'''
zhangsan
lisi
wangwu
zhangsan

'''
```

**for循环遍历**

```python
my_list = ["zhangsan", "lisi", "wangwu", "zhangsan"]
for x in my_list:
	print(x)
'''
zhangsan
lisi
wangwu
zhangsan

'''
```

## 元组

> 可以存储多个不同类型的元素，但是**不可以修改**

### 定义

> 变量 =   (元素,元素,元素, ....) 

空元组：

> 变量 =   () 
>
> 变量 =   tuple()

```python
t1 = (1,"hello",True)
t2 = ()
t3 = tuple
print(f"t1={t1},type= {type(t1)}")
print(f"t2={t2},type= {type(t2)}")
print(f"t3={t3},type= {type(t3)}")
'''
t1=(1, 'hello', True),type= <class 'tuple'>
t2=(),type= <class 'tuple'>
t3=<class 'tuple'>,type= <class 'type'>
'''
```

```python
t4= ("hello")
print(f"t4={t4},type= {type(t4)}")
t5= ("hello,")
print(f"t5={t5},type= {type(t5)}")
'''
t4=hello,type= <class 'str'>
t5=('hello',),type= <class 'tuple'>
'''
```

当元组中**只有一个元素**的时候要求在其后**写上一个逗号**否则不是元组

### 嵌套元组

```python
t6= ((1,2,3),(4,5,6),(7,8))
print(f"t5={t6},type= {type(t6)}")
'''
t5=((1, 2, 3), (4, 5, 6), (7, 8)),type= <class 'tuple'>
'''
```

### 下标索引

和list一样，元组也可以通过下标索引进行取用元素，写法相同

```python
t6= ((1,2,3),(4,5,6),(7,8))
print(t6[1][2])
'''
6
'''
```

### 相关操作

#### 查找指定元素

查找并返回指定元素的下标

>元组. index(x)

```python
t6= ((1,2,3),(4,5,6),(7,8))
print(t6.index((1,2,3)))
'''
0
'''
```

#### 统计元素个数

1.统计并返回元组中**指定元素**的个数

> 元组.count()

```python
t6= ((1,2,3),(7,8),(4,5,6),(7,8))
print(t6.count((7,8)))
'''
2
'''
```

2.统计并返回**元组中的元素**个数

>len(元组)

```python
t6= ((1,2,3),(7,8),(4,5,6),(7,8))
print(len(t6))
'''
4
'''
```

#### 遍历

**for循环**

```python
t6= ((1,2,3),(7,8),(4,5,6),(7,8))
for x in t6:
    print(x)
'''
(1, 2, 3)
(7, 8)
(4, 5, 6)
(7, 8)
'''
```

**while循环**

```python
t6= ((1,2,3),(7,8),(4,5,6),(7,8))
index = 0
while index<len(t6):
    print(t6[index])
    index+=1
'''
(1, 2, 3)
(7, 8)
(4, 5, 6)
(7, 8)
'''
```

**元组里的元素不可以修改，但是在元组里嵌套的list的元素是可以修改的**

```python
t6= ((1,2,3),(7,8),[1,2,3,4,"hello"],(7,8))
print(t6[-2])
t6[-2][-1]="world"
print(t6[-2])
'''
[1, 2, 3, 4, 'hello']
[1, 2, 3, 4, 'world']
'''
```

### 特点

1. **可以容纳不同类型的元素**
2. **数据有序存储**
3. **允许重复数据存在**
4. **不可以修改**

## 字符串

> 字符的容器，一个字符串可以存放任意数量的字符

**下标索引在字符串中也可以使用，正向从0开始，负向从-1开始**

```python
str = "abcdefg"
print(str[-1])
print(str[0])
'''
g
a
'''
```

**字符串是不可修改的数据容器**，**只读**

### 常用方法

#### 查找指定元素的下标

> 查找并返回指定元素的下标：字符串.index(x)

```python
str = "abcdefg"
print(str.index("bcd"))
print(str.index("g"))
'''
1
6
'''
```

#### 字符串替换

> 将字符串中指定的内容替换成指定内容，并返回替换后新的字符串
>
> **字符串.replace(字符串1,字符串2)**  将字符串1换成2形成新的字符串

```python
str = "abcdefg"
newstr = str.replace("abcd","dcba")
print(str)
print(newstr)
'''
abcdefg
dcbaefg
'''
```

#### 字符串分割

> **字符串.split(分隔符字符串)**

> 按照指定的分隔符字符串，将字符串划分为多个字符串，并存到列表对象中

**字符串本身不变而是得到一个列表对象**

```python
str = "hello world i am klklkl"
newstr = str.split(" ")
print(str)
print(f"newstr = {newstr},type = {type(newstr)} ")
'''
hello world i am klklkl
newstr = ['hello', 'world', 'i', 'am', 'klklkl'],type = <class 'list'> 
'''
```

#### 规整操作

**去除前后空格**

> 字符串.strip()

```python
str = "   hello world i am klklkl  "
newstr = str.strip()
print(str)
print(f"newstr = {newstr} ")
'''
   hello world i am klklkl  
newstr = hello world i am klklkl 
'''
```

**去除前后指定字符串**

> 字符串.strip(字符串)    将传入的字符串划分成小串，只要**头尾**含有就去除

```python
str = "12 hello world i am klklkl 21"
newstr = str.strip("12")
print(str)
print(f"newstr = {newstr} ")
'''
12 hello world i am klklkl 21
newstr =  hello world i am klklkl  
'''
```

#### 统计指定字符串出现的次数

> 字符串.count(字符串)

#### 统计字符串的长度

> len(字符串)

#### 遍历

**for循环**

同上

**while循环**

同上

### 特点

1. **只可以存储字符串**
2. **长度有上限，取决于内存大小**
3. **数据有序存储**
4. **允许重复数据存在**
5. **不可以修改**

## 序列

>内容**连续，有序**，可以**使用下标索引**的一类**数据容器**

>列表、元组、字符串均可以视为序列

### 切片

> 从一个序列中取出一个子序列，形成一个新的序列，不修改原来的序列

**语法：**

>**序列[起始下标: 结束下标:步长]**
>
>起始下标：从何处开始，可以留空表示从头
>
>结束下标：到那里结束，不包含结束下标位置，可以留空表示截去到尾部
>
>步长：取元素的间隔，默认为1，可以省略不写

```python
my_list1 = [0,1,2,3,4,5,6]
r1 = my_list1[1:4]
print(f"r1 = {r1}")
my_tuple = (0,1,2,3,4,5,6)
r2 = my_tuple[:]
print(f"r2 = {r2}")
my_str = "0123456"
r3 = my_str[::2]
print(f"r3 = {r3}")
r4 = my_str[::-1]
print(f"r4 = {r4}")
'''
r1 = [1, 2, 3]
r2 = (0, 1, 2, 3, 4, 5, 6)
r3 = 0246
r4 = 6543210
'''
```

## 集合

> 上述介绍的数据容器：列表、元组、字符串都支持重复元素，而集合**不支持重复元素，顺序无法保证**，自带**去重**功能

### 定义

>  变量 = {元素1,元素2,元素3 ,.....}

空集合

>变量 = set()
>
>{}是空字典

```python
my_set = {1,2,3,1,2,3,4,5,6}
print(f"my_set={my_set}")
none_set= set()
print(f"none_set = {none_set}")
'''
my_set={1, 2, 3, 4, 5, 6}
none_set = set()
'''
```

### 常用操作

**不支持下标索引访问，可修改**

#### 添加

> 集合.add(元素)

```python
my_set = {1,2,3,1,2,3,4,5,6,"klklkl"}
my_set.add(10)
print(my_set)
my_set.add("klklkl")
print(my_set)
'''
{1, 2, 3, 4, 5, 6, 10, 'klklkl'}
{1, 2, 3, 4, 5, 6, 10, 'klklkl'}
'''
```

#### 移除

**从集合中移除指定元素，同时集合被修改**

> 集合.remove(元素)

```python
my_set = {1,2,3,1,2,3,4,5,6,"klklkl"}
my_set.remove("klklkl")
print(my_set)
'''
{1, 2, 3, 4, 5, 6}
'''
```

**从集合中<u>随机取出</u>一个元素，同时集合被修改，返回移除的元素，元素被移除**

>集合.pop()

```python
my_set = {1,2,3,1,2,3,4,5,6,"klklkl"}
print(my_set.pop())
print(my_set)
'''
1
{2, 3, 4, 5, 6, 'klklkl'}
'''
```

#### 清空

>集合.clear()



#### 取差集

>集合1.differrence(集合2)
>
>取出集合1和集合2的差集（**集合1有集合2没有的**），返回一个新集合

```python
set1 = {1,2,3,4,5}
set2 = {1 ,3,5,7}
print(set1.difference(set2))
'''
{2, 4}
'''
```

#### 去差集

> 集合1.difference_update(集合2)
>
> 消除集合1和集合2内相同的元素，集合1被修改集合2不变

```python
set1 = {1,2,3,4,5}
set2 = {1 ,3,5,7}
set1.difference_update(set2)
print(set1)
print(set2)
'''
{2, 4}
{1, 3, 5, 7}
'''
```

#### 集合合并

> 集合1.union(集合2)
>
> 集合1和2合并成一个新的集合，集合1和2不变

```python
set1 = {1,2,3,4,5}
set2 = {1 ,3,5,7,8,9}
set3 = set1.union(set2)
print(set1)
print(set2)
print(set3)
'''
{1, 2, 3, 4, 5}
{1, 3, 5, 7, 8, 9}
{1, 2, 3, 4, 5, 7, 8, 9}
'''
```

#### 统计元素数量

> len(集合)

#### 遍历

**不支持下标索引，因此不可以用while循环**

```python
set2 = {1 ,3,5,7,8,9}
for element in set2:
    print(f"集合的元素有 :{element}")
'''
集合的元素有 :1
集合的元素有 :3
集合的元素有 :5
集合的元素有 :7
集合的元素有 :8
集合的元素有 :9
'''
```

## 字典

含有两个数据，一个名为key，另一个为Value，字典可以通过key找到与其对应的value

**不允许元素重复，不可以使用下标索引，只可以通过key值取得对应的Value**

### 定义

```python
变量 = {key:value , key:value ,....}
#空字典
变量 = {}
变量 = dict()
```

**获取value**

通过key值取得对应的Value

>字典.[key]

```python
dict_1 = {"liming": 56, "wanglikong": 99, "zhoujielin": 88, "lindaju": 77}
print(dict_1["lindaju"])
'''
77
'''
```

**字典的嵌套**

**key不能为字典，value可以是任意数据**

```python
stu_score_date = {
    "wanglihong":{
        "yuwen": 77,
        "shuxue":66,
        "yingyu":99
    },"zhoujielun":{
        "yuwen": 87,
        "shuxue":65,
        "yingyu":89
    }
}
print(stu_score_date)
print(stu_score_date["zhoujielun"]["shuxue"])
'''
{'wanglihong': {'yuwen': 77, 'shuxue': 66, 'yingyu': 99}, 'zhoujielun': {'yuwen': 87, 'shuxue': 65, 'yingyu': 89}}
65
'''
```

### 常用操作

#### 增加元素

> 字典[key] = value
>
> 字典被修改，增加了新元素

```python
dict_1 = {"liming": 56, "wanglikong": 99, "zhoujielin": 88, "lindaju": 77}
dict_1["zhangsan"] = 88
print(dict_1)
'''
{'liming': 56, 'wanglikong': 99, 'zhoujielin': 88, 'lindaju': 77, 'zhangsan': 88}

'''
```



#### 更新元素

> 字典[key] = value
>
> 字典被修改

**如果key存在则为更新，不存在即为修改**

```python
dict_1 = {"liming": 56, "wanglikong": 99, "zhoujielin": 88, "lindaju": 77}
dict_1["liming"] = 88
print(dict_1)
'''
{'liming': 88, 'wanglikong': 99, 'zhoujielin': 88, 'lindaju': 77}
'''
```



#### 删除元素

> 字典.pop(key)
>
> 删除字典中key的内容，并返回key对应的value

```python
dict_1 = {"liming": 56, "wanglikong": 99, "zhoujielin": 88, "lindaju": 77}
dict_1.pop("wanglikong")
print(dict_1)
'''
{'liming': 56, 'zhoujielin': 88, 'lindaju': 77}
'''
```



#### 清空元素

> 字典.clear()

```python
dict_1 = {"liming": 56, "wanglikong": 99, "zhoujielin": 88, "lindaju": 77}
dict_1.clear()
print(dict_1)
```



#### 获取全部key

> 字典.keys()

```python
dict_1 = {"liming": 56, "wanglikong": 99, "zhoujielin": 88, "lindaju": 77}
keys=dict_1.keys()
print(keys)
'''
dict_keys(['liming', 'wanglikong', 'zhoujielin', 'lindaju'])
'''
```



#### 遍历字典

**方法1:**

```python
dict_1 = {"liming": 56, "wanglikong": 99, "zhoujielin": 88, "lindaju": 77}
keys=dict_1.keys()
for i in keys:
    print(f"{i}对应的键值是{dict_1[i]}")
'''
liming对应的键值是56
wanglikong对应的键值是99
zhoujielin对应的键值是88
lindaju对应的键值是77
'''
```

**方法2:**

```python
dict_1 = {"liming": 56, "wanglikong": 99, "zhoujielin": 88, "lindaju": 77}
for i in dict_1:
    print(f"{i}对应的键值是{dict_1[i]}")
'''
liming对应的键值是56
wanglikong对应的键值是99
zhoujielin对应的键值是88
lindaju对应的键值是77
'''
```

**不支持下标索引，不适用于while循环**

#### 统计元素数量

> len(字典)

### 特点

1. **可以容纳多个数据，容纳不同类型的数据。**
2. **每一份数据是keyvalue键值对**
3. **可以通过key获取value**
4. **不允许重复key存在**
5. **不支持下标索引**
6. **可以修改**
7. **支持for循环不支持while循环**

## 总结

![image-20240123161337038](image-20240123161337038.png)

![image-20240123161352170](image-20240123161352170.png)

![image-20240123161442232](image-20240123161442232.png)

## 通用操作

下面对于字典的操作基本是对于key值的操作

### len

> 统计元素个数

### max 和min

> 获取最大元素，获取最小元素

对于字典，获取的是最大或最小的key

### 类型转换

- list(容器)

  转列表

- str(容器)

  转字符串

- tuple(容器)

  转元组

- set(容器)

  转集合

### sorted

排序，并返回列表对象的结果，字典会丢失value

>sorted(容器)    正向排序，从小到大
>
>sorted(容器，reverse = True)    反向排序

![image-20240123162933181](image-20240123162933181.png)

# 文件

> 文件编码：编码的技术，记录了如何将内容翻译成二进制以及如何解密二进制，不同的编码对同一文本的翻译不同

常见文件编码：

- UTF-8  全球通用 默认编码
- GBK
- Big5

## 读取文件

1. 打开文件
2. 读写文件
3. 关闭文件

## 打开文件

> open(name,mode,encoding)
>
> name：文件的名字可以包含路径，字符串表示
>
> mode：设置打开文件的模式，只读，写入，追加等
>
> encoding：编码格式（推荐使用UFT-8）

![image-20240124003300313](image-20240124003300313.png)

```python
f = open("D:/桌面/test.txt","r",encoding = "UTF-8")
```

**encoding不是第三个参数，因此要使用关键字参数**

## 读取文件

> 文件对象.read(num)
>
> num:表示要读取的数据的长度，单位是字节，如果没有传入num，那么就表示读取文件中所有数据

```python
f = open("D:/桌面/test.txt","r",encoding = "UTF-8")
print(f.read(10))
print(f.read())#全部内容
```

**连续读取会从上一次读取的末尾开始读取**

> 文件对象.readlines()
>
> 按照行的方法把文件中的内容进行一次性读取，并返回一个列表，其中每一行的数据为一个元素

```python
f = open("D:/桌面/test.txt","r",encoding = "UTF-8")
list1 = f.readlines()
```

**可以使用for循环读取行**

```python
f = open("D:/桌面/test.txt","r",encoding = "UTF-8")
for line in f:
    print(f"每一行为{line}")
```

**连续读取会从上一次读取的末尾开始读取**

> 文件对象.readline()
>
> 一次读取一行内容

```python
f = open("D:/桌面/test.txt","r",encoding = "UTF-8")
list1 = f.readline()
```

## 写入文件

> 文件对象.write() 
>
> 把内容写入缓冲区

> 文件对象.flush()
>
> 内容刷新，写入硬盘中的文件

**close方法内置了flush功能**

```python
f = open("D:/桌面/test.txt","w",encoding = "UTF-8")
f.write("hello world")
f.flush()
f.close()
```



## 关闭文件

> 文件对象.close()

解除文件占用

> with open(name,mode,encoding) as 文件对象:
>
> ​            操作

完成操作后自动关闭文件，避免遗忘close方法

```python
with open("D:/桌面/test.txt","r",encoding = "UTF-8") as f:
    res = f.read()
    print(res)
```

# 类

## 定义

> class 类名:
>
> ​		satement1
>
> ​		satement2
>
> ​	    ......

```python
class Student:
    school = "null"

    def __init__(self, tmp_name, tmp_school, tmp_gener, tmp_id):
        self.school = tmp_school
        self.id = tmp_id
        self.name = tmp_name
        self.gener = tmp_gener

    def return_school(self):
        return self.school


s = Student("xiaoming", "guangmingzhongxue", "girl", "1992")
print(s.return_school())
'''
guangmingzhongxue
'''
```

## 初始化函数

```python
 def __init__(self, tmp_name, tmp_school, tmp_gener, tmp_id):
        self.school = tmp_school
        self.id = tmp_id
        self.name = tmp_name
        self.gener = tmp_gener
```

