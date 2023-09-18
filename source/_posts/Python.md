---
layout: pose
title: Python
date: 2023-08-02 15:15:19
tags: Python
---





```python
# 字面量（有空格）
print("hello world")
print(12)
print(1.0)
# 我是单行注释（有空格）
"""我是多行注释一般用于开头解释类和程序"""


"""定义变量"""
money = 15
print("钱包还有：", money)
"""逗号贴近后引号与money有空格"""
money = money-10
print("还剩：", money, "元")

"""查看变量所存储的数据类型，变量没有类型"""
print(type("str"))
str_type = (type("123456"))
# 返回值为变量存储的数据类型
print(type(str_type))
name = "heima"
name_type = type(name)
print(name_type)

"""类型转换"""
# int(x)
# float(X)
# str(x)
# 上述函数都有返回值

# 数字转字符串
num_str = str(11)
print(type(num_str), num_str)
float_str = str(111.34)
print(type(float_str), float_str)
# 任何数据都可以转字符串

# 字符串转数字 只有都是数字才可以转
num = int("11")
int_num = type(num)
print(type(num), num)
# 浮点数转整数 丢失精度去尾
int_float = int(11.5)
print(type(int_float), int_float)

"""标识符命名  只允许出现 英文中文数字下划线，数字不可开头 
不可使用关键字 """


"""常见运算符"""
# + - * / %
# // 取整除
# ** 指数
# += -= /= *= //= **=

""" 字符串扩展"""

"""定义方式"""
# name='hhhh'
# name= "hhhh"
# name = """hhh"""
name = 'hhhhhh1'
name2 = "hhhhhh2"
name3 = """hhhhh
hhh3"""
print(name, name2, name3)

"""字符串中包含双引号"""
name = '"123456'
name = "'12345'"
name = "\"123456"

"""字符串拼接"""
print("123"+"456")
name = "987"
print("12345" + name + "564")
tel = 132456
# print("111111" + tel +"454") error

```

#### 字符串格式化

##### 方法一：

eg：

```python
name = "kjkjk"
where = "at kl"
message = "abced%s%s" % (name, where)
print(message)
```

输出： abcedkjkjkat kl

**通过占位的形式完成拼接，%表示占位，s表示将变量变成字符串放入占位的地方**



| 格式符号 | 转化           |
| ---- | ------------ |
| %s   | 转化为字符串放入占位位置 |
| %d   | 转化为整数放入占位位置  |
| %f   | 转化为浮点放入占位位置  |

##### 方法二：



**不限数据类型，不做精度控制，适合对精度没有要求时快速使用**

```python
f"...{变量} "
```

eg

```python
num1=11
name = "klklklk"

print(f"my name is {name} ,and age is {num1}")
```

输出：
my name is klklklk ,and age is 11





#### 格式化的精度控制



**m.n控制数度的宽度和精度，m控制宽度，<u>但当宽度小于自身时不生效</u>，n控制精度会进行<u>四舍五入</u>**



```python
num1=11
num2=11.345

print("数字11宽度5：%5d\n" % num1)
print("数字11宽度1：%1d\n" % num1)
print("数字11.345宽度7，精度2：%7.2f\n" % num2)
print("数字11.345宽度不限，精度2: %.2f" % num2)
print("数字11.345精度不限，宽度2: %2f" % num2)
```

输出：

数字11宽度5：   11

数字11宽度1：11

数字11.345宽度7，精度2：  11.35



数字11.345宽度不限，精度2: 11.35
数字11.345精度不限，宽度2: 11.345000





#### 对表达式进行格式化



表达式：一条具有明确执行结果的代码语句



```python
print("1 * 1 = %d" % (1*1))
print(f"1 * 2 = {1*2}")
print("字符串在python的类型名是：%s" % type("字符串"))
```

输出:
1 * 1 = 1
1 * 2 = 2
字符串在python的类型名是：<class 'str'>



#### 数据输入



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



**<u>input语句不管输入什么都统统当作字符串看待，可自行进行数据转换</u>**



```python
age = input("what is your age?\n")
print("age is", type(age))
```

输出：

what is your age?
<u>18</u>
age is <class 'str'>

#### 判断语句



##### 布尔类型和比较运算符

布尔类型的字面量：

True ：表示真

False：表示假



比较运算符：

== , > , < , >= ,<= ,!=



eg:

```python
bool_1 = True
bool_2 = False
print(f"bool1 is{type(bool_1)},bool2 is {type(bool_2)}")
```

输出：

bool1 is<class 'bool'>,bool2 is <class 'bool'>





```python
num1 = 10
num2 = 10
num3 = 15
print(f"num1 == num2 is {num1 == num2}")
print(f"num1 != num3 is {num1 != num3}")
```

输出：
num1 == num2 is True
num1 != num3 is True



**字符串也可以进行 == ，! = 比较**



##### if语句的基本格式



if  条件：

<u>   </u> 条件成立时执行的内容



eg：

```python
age = 18
print(f"my age is {age}")
if age >= 18:
    print("i am a adult")
    print("i will go to university")
print("time fly quickly!")
```

输出：

my age is 18
i am a adult
i will go to university
time fly quickly!



**缩进！！！**



```python
age = 10
print(f"my age is {age}")
if age >= 18:
    print("i am a adult")
    print("i will go to university")
print("time fly quickly!")
```

输出：
my age is 10
time fly quickly!



##### if else语句

if 条件：

<u>   </u> 条件成立时执行的内容

else：

<u>    </u>条件不满足时执行的内容



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
```

输出：
my age is 10
i am a child.
i am going to senior high school.
time fly quickly!





##### if elif else判断语句



if 条件：

<u>   </u> 条件1成立时执行的内容

elif 条件2:

    条件2成立时执行的内容

....

elif 条件n：
    条件 n成立时执行的内容

else：

<u>    </u>条件都不满足时执行的内容



eg：

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



eg：



```python
if int(input("请输入你的身高（cm）："))<120:
    print("小于120cm 可以免费")
elif int(input("您的vip等级是："))>3:
    print("vip>3 可以免费")
else:
    print("收费10元")
```
