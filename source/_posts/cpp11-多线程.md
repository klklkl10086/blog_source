---
title: thread库
date: 2025-10-01 14:51:33
tags: ["CPP","thread"]
categories: ["研究生补完"]
description: 补足一下cpp的知识
---

# cpp11--多线程

## 创建线程

```cpp
#include<iostream>
#include<thread>

void printHelloWorld()
{
    std::cout<<"Hello world"<<std::endl;
}
int main()
{
    //1.创建线程
    std::thread thread1(printHelloWorld);
    return 0;
}
```

但这个时候会报错,因为主线程先于子线程结束

## join()函数

强制主线程等待子线程结束后再结束

```cpp
#include<iostream>
#include<thread>

void printHelloWorld()
{
    std::cout<<"Hello world"<<std::endl;
}
int main()
{
    //1.创建线程
    std::thread thread1(printHelloWorld);
    //2.主程序等待线程执行完毕
    thread1.join();
    return 0;
}
```



## detach()函数

分离线程,即使主线程先于子线程结束也不会报错,此时子线程在后台运行

```cpp
#include<iostream>
#include<thread>

void printHelloWorld()
{
    std::cout<<"Hello world"<<std::endl;
}
int main()
{
    //1.创建线程
    std::thread thread1(printHelloWorld);
    //2.分离线程,即使主线程先于子线程结束也不会报错
    thread1.detach();
    return 0;
}
```



## joinable()函数

判断是否可以调用join()函数或者detach()函数,返回布尔值

```cpp
#include<iostream>
#include<thread>

void printHelloWorld()
{
    std::cout<<"Hello world"<<std::endl;
}
int main()
{
    //1.创建线程
    std::thread thread1(printHelloWorld);
    //2.判断能否调用join函数
    bool isJoin = thread1.joinable();
    if(isJoin)
    {
        thread1.join();
    }
    return 0;
}
```



## 互斥量

```cpp
#include <iostream>
#include <thread>
#include <mutex>
int a=0;
std::mutex mtx;//初始化锁
void func()
{
	for(int i=0;i<1000;i++)
	{
		mtx.lock();//加锁
		a++;
		mtx.unlock();//解锁
	}
}

int main()
{
	std::thread t1(func);
	std::thread t2(func);
	t1.join();
	t2.join();
	std::cout<<a<<std::endl;
	return 0;	
}
```

`线程安全`:多线程的程序每一次运行的结构和单线程的结构始终是一样的,那么线程就是安全的



## 互斥量死锁

```cpp
#include <iostream>
#include <thread>
#include <mutex>
#include <windows.h>
std::mutex m1,m2;
void func_1()
{
	for(int i=1;i<=50;i++)
	{
		m1.lock();
		m2.lock();
		m1.unlock();
		m2.unlock();
	}
}
void func_2()
{
	for(int i=1;i<=50;i++)
	{
		m2.lock();
		m1.lock();
		m1.unlock();
		m2.unlock();
		sleep(1);
	}
}

int main()
{
	std::thread t1(func_1);
	std::thread t2(func_2);
	t1.join();
	t2.join();
	std::cout<<"over"<<std::endl;
	return 0;	
}
```



## lock_guard与unique_lock

`Rall`原则:

- **构造时**：自动获取互斥锁。
- **析构时**：自动释放互斥锁。
  这意味着即使代码块中发生异常，锁也能被安全释放，避免了资源泄漏和死锁。

> C++11 中的 `std::lock_guard` 和 `std::unique_lock`。它们是实现 RAII（资源获取即初始化）来管理互斥锁的两种重要工具，能有效防止死锁并简化代码。

### std::lock_guard

`std::lock_guard` 是一个轻量级的、不可拷贝的 RAII 包装器，功能简单直接。

特点:

1. **简单且高效**：开销小，只提供最基本的 RAII 风格锁管理。
2. **不可手动操作**：一旦创建，就不能主动 `lock` 或 `unlock`，其生命周期完全由作用域控制。
3. **不支持延迟锁定**：构造时必须立即获得锁。
4. **不可复制和移动**:通过禁用拷贝构造和等于号实现

适用于在**某个明确的作用域(局部作用域)**内需要持有锁，且在此作用域内不需要手动释放或重新获取锁的简单情况。

```cpp
#include <iostream>
#include <thread>
#include <mutex>
#include <windows.h>
std::mutex mtx;
int shared_data=0;
void func()
{
	for(int i=1;i<=10000;i++)
	{
		std::lock_guard<std::mutex> lg(mtx);
		//自动调用构造函数加锁
		shared_data++;
		//自动调用析构函数解锁
	}
}
int main()
{
	std::thread t1(func);
	std::thread t2(func);
	t1.join();
	t2.join();
	std::cout<<shared_data<<std::endl;
	return 0;	
}
```



### std::unique_lock

`std::unique_lock` 是一个功能更全面、更灵活的 RAII 包装器。它包含了 `lock_guard` 的所有功能，并提供了额外的控制能力。

**特点:**

1. **灵活性高**：支持延迟锁定、手动解锁、条件变量等复杂场景。
2. **可手动操作**：可以在生命周期内主动调用 `lock()` 和 `unlock()`。
3. **支持所有权转移**：可以通过 `std::move` 转移锁的所有权（但不能复制）。
4. **支持多种锁定策略**：在构造时可以通过参数指定锁定行为。

**锁定策略**:

- `std::defer_lock`：不立即加锁，稍后手动加锁。
- `std::try_to_lock`：尝试获取锁，但不阻塞。
- `std::try_lock_for`: 阻塞并等待一定的时间
- `std::adopt_lock`：假设调用线程已经持有该互斥锁。

适用于所有需要锁的场景，尤其是在以下复杂情况：

- 需要与 `std::condition_variable` 配合使用。
- 需要手动释放锁（例如，在长时间操作的中间阶段）。
- 需要尝试获取锁或延迟获取锁。

```cpp
#include <iostream>
#include <thread>
#include <mutex>
#include <windows.h>
std::timed_mutex mtx;
int shared_data=0;
void func()
{
	for(int i=1;i<=10000;i++)
	{
		std::unique_lock<std::timed_mutex>lg(mtx,std::defer_lock);//延迟加锁
		lg.try_lock_for(std::chrono::seconds(5));
		//阻塞并等待5秒,若5秒后加锁失败会直接返回
		shared_data++;
		//自动调用析构函数解锁
	}
}
int main()
{
	std::thread t1(func);
	std::thread t2(func);
	t1.join();
	t2.join();
	std::cout<<shared_data<<std::endl;
	return 0;	
}
```

```cpp
#include <iostream>
#include <thread>
#include <mutex>
#include <windows.h>
std::timed_mutex mtx;
int shared_data=0;
void func()
{
	for(int i=1;i<=2;i++)
	{
		std::unique_lock<std::timed_mutex>lg(mtx,std::defer_lock);//延迟加锁
		if(lg.try_lock_for(std::chrono::seconds(2)))
		//如果获取不到就阻塞并等待2秒,若2秒后加锁失败直接返回
		{
			std::this_thread::sleep_for(std::chrono::seconds(4));
			shared_data++;
		}
		//自动调用析构函数解锁
	}
}
int main()
{
	std::thread t1(func);
	std::thread t2(func);
	t1.join();
	t2.join();
	std::cout<<shared_data<<std::endl;
	return 0;	
}
```

## std::call_once与其使用场景

> 单例设计模式:用于确保某个类只能创建一个实例,如日志类

```cpp
class Log{
	public:
		Log(){}//默认构造函数
		Log(const Log& log) = delete;//禁止拷贝构造
		Log& operator=(const Log& log) = delete;//禁止赋值
		
		static Log& GetInstance(){//static 方法：可以通过类名直接调用，无需实例
			//局部静态变量：在第一次调用时创建，程序结束时销毁
            static Log log;//懒汉模式
			return log;
		}
		void PrintLog(std::string msg)
		{
			std::cout<<msg<<std::endl;
		}
};
```

```cpp
class Log{
	public:
		Log(){}//默认构造函数
		Log(const Log& log) = delete;//禁止拷贝构造
		Log& operator=(const Log& log) = delete;//禁止赋值
		
		static Log& GetInstance(){//static 方法：可以通过类名直接调用，无需实例
			//局部静态变量：在第一次调用时创建，程序结束时销毁
            static Log* log=nullptr;//饿汉模式
			
			if(!log) log = new Log;
			return *log;
		}
		void PrintLog(std::string msg)
		{
			std::cout<<msg<<std::endl;
		}
};

```

多线程情况下会出现一下情况:

```cpp
#include <iostream>
#include <thread>
#include <mutex>
#include <string>
class Log{
	public:
		Log(){}//默认构造函数
		Log(const Log& log) = delete;//禁止拷贝构造
		Log& operator=(const Log& log) = delete;//禁止赋值
		
		static Log& GetInstance(){//static 方法：可以通过类名直接调用，无需实例
			static Log* log=nullptr;//饿汉模式
			
			if(!log) log = new Log;
			return *log;
		}
		void PrintLog(std::string msg)
		{
			std::cout<<__TIME__<<' '<<msg<<std::endl;
		}
};
void func()
{
	Log::GetInstance().PrintLog("error");
}
int main()
{
	std::thread t1(func);//t1  t2的并行会导致创建两个单例
	std::thread t2(func);
	t1.join();
	t2.join();
	return 0;
}
```

为了保证单例,使用`std::call_once`

```cpp
template<class Callable, class... Args>
void call_once(std::once_flag& flag, Callable&& func, Args&&... args);
```

1. **线程安全**：保证在多线程环境下，函数只被执行一次
2. **高效**：内部使用原子操作和锁，性能较好
3. **异常安全**：如果函数抛出异常，不算执行完成，其他线程会重试
4. 只能在线程中使用

```cpp
#include <iostream>
#include <thread>
#include <mutex>
#include <string>
class Log{
    private:

    static Log* log;  // 静态成员声明
    static std::once_flag once;

	public:
		Log(){}//默认构造函数
		Log(const Log& log) = delete;//禁止拷贝构造
		Log& operator=(const Log& log) = delete;//禁止赋值
		
		static Log& GetInstance(){
        // 使用 call_once 确保只初始化一次
        std::call_once(once, init);
        return *log;
    }
		void PrintLog(std::string msg)
		{
			std::cout<<__TIME__<<' '<<msg<<std::endl;
		}
        static void init()
        {
            log = new Log;
        }
        
};
// 静态成员定义
Log* Log::log = nullptr;
std::once_flag Log::once;
void func(){
    Log::GetInstance().PrintLog("error");
}

int main(){
    std::thread t1(func);
    std::thread t2(func);
    t1.join();
    t2.join();
    return 0;
}
```

