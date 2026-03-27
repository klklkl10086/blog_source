---
title: CPP网络编程基础
date: 2026-02-15 17:33:03
tags: ["Linux","CPP"]
categories: ["CPP开发"]
description: CPP开发基础知识,网络编程
---

# 简单的通信程序

**客户端**

```cpp
//客户端程序
#include <iostream>
#include <cstdio>
#include <cstring>
#include <cstdlib>
#include <unistd.h>
#include <netdb.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <arpa/inet.h>

using namespace std;
int main(int argc,char*argv[])
{
	if(argc!=3) 
	{
		cout<<"参数使用错误"<<endl;
		return -1;
	}
	//step 1.client socket
	int sockfd = socket(AF_INET,SOCK_STREAM,0);
	if(sockfd==-1)
	{
		perror("socket");
		return -1;
	}
	//step 2.send request
	struct hostent* h;
	if((h=gethostbyname(argv[1]))==0)
	{
		cout<<"获取IP失败"<<endl;
		close(sockfd);
		return -1;
	}
	struct sockaddr_in servaddr;
	memset(&servaddr,0,sizeof(servaddr));
	servaddr.sin_family = AF_INET;
	memcpy(&servaddr.sin_addr,h->h_addr,h->h_length);
	servaddr.sin_port = htons(atoi(argv[2]));
	if(connect(sockfd,(struct sockaddr*)&servaddr,sizeof(servaddr))!=0)
	{
		perror("connect");
		close(sockfd);
		return -1;
	}
	//step 3. send request
	char buffer[1024];
	for(int i=0;i<3;i++)
	{
		int iret;
		memset(buffer,0,sizeof(buffer));
		sprintf(buffer,"this is no %d request,id is %3d",i+1,i+1);
		if((iret=send(sockfd,buffer,strlen(buffer),0))<=0)
		{
			perror("send");
			break;
		}
		cout<<"send:"<<buffer<<endl;
		memset(buffer,0,sizeof(buffer));
		if((iret = recv(sockfd,buffer,sizeof(buffer),0))<=0)
		{
			cout<<"iret= "<<iret<<endl;
			break;
		}
		cout<<"receive:"<<buffer<<endl;
		sleep(1);
	}
	//step 4. close socket
	close(sockfd);
	
}
```

**服务器**

```cpp
//服务器程序
#include <iostream>
#include <cstdio>
#include <cstring>
#include <cstdlib>
#include <unistd.h>
#include <netdb.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <arpa/inet.h>


using namespace std;

int main(int argc,char* argv[])
{
	if(argc!=2)
	{
		cout<<"command format is error"<<endl;
		return -1;
	}
	//step 1. create socket
	int listenfd = socket(AF_INET,SOCK_STREAM,0);
	if(listenfd == -1)
	{
		perror("soket");return -1;
	}
	
	// step 2. bind
	struct sockaddr_in  servaddr;
	memset(&servaddr,0,sizeof servaddr);
	servaddr.sin_family = AF_INET;
	servaddr.sin_addr.s_addr = htonl(INADDR_ANY);//服务端的任意网卡的IP都可以用于通讯
	servaddr.sin_port = htons(atoi(argv[1]));
	if(bind(listenfd,(struct sockaddr*)&servaddr,sizeof(servaddr))!=0)
	{
		perror("bind");
		close(listenfd);
		return -1;
	}
	//step 3. set socket listening
	if(listen(listenfd,5)!=0)
	{
		perror("listen");
		close(listenfd);
		return -1;
	}
	//step 4. accept request from client
	int clientfd = accept(listenfd,0,0);
	if(clientfd == -1)
	{
		perror("accept");
		close(listenfd);
		return -1;
	}
	cout<<"had connected to client"<<endl;
	
	// step 5. receive
	char buffer[1024];
	while(true)
	{
		int iret;
		memset(buffer,0,sizeof buffer);
		if((iret = recv(clientfd,buffer,sizeof(buffer),0))<=0)
		{
			cout<<"iret="<<iret<<endl;
			break;
		}
		cout<<"receive"<<buffer<<endl;
		
		strcpy(buffer,"ok");
		
		if((iret=send(clientfd,buffer,strlen(buffer),0))<=0)
		{
			perror("send");
			break;
		}
		cout<<"send:"<<buffer<<endl;
		
	}
	//step 6. close
	close(listenfd);
	close(clientfd);
}
```



# 文件操作

## open函数

```cpp
#include <fcntl.h>

int open(const char *path, int flags);
int open(const char *path, int flags, mode_t mode);
```

**参数:**

- **path**：要打开或创建的文件的路径（C 风格字符串）。
- **flags**：文件访问模式及行为控制标志（通过位或 `|` 组合）。
  - **访问模式（必须指定且只能选一个）**
    - `O_RDONLY`：只读打开。
    - `O_WRONLY`：只写打开。
    - `O_RDWR`：读写打开。
  - **可选标志（可与访问模式按位或）**
    - `O_CREAT`：若文件不存在则创建它。需要同时提供 `mode` 参数。
    - `O_TRUNC`：若文件已存在且以写方式打开，则将其长度截断为 0（清空内容）。
    - `O_APPEND`：每次写入时，数据追加到文件末尾（原子操作）。
    - `O_EXCL`：与 `O_CREAT` 一起使用时，如果文件已存在，则 `open` 失败。可用于确保独占创建。
    - `O_NONBLOCK`：以非阻塞方式打开文件（适用于设备文件、管道等）。
    - `O_SYNC`：以同步写入方式打开，每次 `write` 都会等待物理 I/O 完成。
    - `O_CLOEXEC`：设置执行时关闭标志，防止子进程继承该文件描述符。
- **mode**：当 `flags` 中包含 `O_CREAT` 时，需要用此参数指定新文件的权限（如 `0644`）。
  - 该值通常用八进制数表示，例如：
    - `0644`：所有者可读写，组用户和其他用户只读。
    - `0755`：所有者可读写执行，组用户和其他用户可读执行。
  - 实际权限还受到进程的 **umask** 影响：最终权限 = `mode & ~umask`。

**返回值：**成功时返回一个**文件描述符**（非负整数）；失败时返回 `-1`，并设置全局变量 `errno` 以指示错误类型。



## write函数

```cpp
#include <unistd.h>

ssize_t write(int fd, const void *buf, size_t count);
```

**参数:**

- **fd**：文件描述符，通常由 `open` 返回，也可以是标准输出（`STDOUT_FILENO`，值为 1）或标准错误（`STDERR_FILENO`，值为 2）。
- **buf**：指向要写入数据的缓冲区的指针。类型为 `const void*`，因此可以传入任何类型的指针（C++ 中通常需要强制转换或直接使用 `char*`）。
- **count**：请求写入的**字节数**。

**返回值：**

- **成功**：返回实际写入的字节数（`ssize_t` 类型，可能小于 `count`，称为“部分写入”）。
- **失败**：返回 `-1`，并设置全局变量 `errno` 以指示错误。

**返回值详解**

`ssize_t` 是一个有符号整型，通常为 `long`。

- 返回 `0` 通常表示没有写入任何字节（例如 `count` 为 0 时）。
- 返回正数表示实际写入的字节数，该值可能小于请求的字节数，原因可能是磁盘已满、管道缓冲区满、信号中断等。
- 返回 `-1` 表示出错，需检查 `errno`。



## read函数

```cpp
#include <unistd.h>

ssize_t read(int fd, void *buf, size_t count);
```

**参数:**

- **fd**：文件描述符，通常由 `open` 返回，也可以是标准输入（`STDIN_FILENO`，值为 0）。
- **buf**：指向接收数据的内存缓冲区的指针。类型为 `void*`，可以接受任何类型的指针，但通常使用 `char*` 或 `unsigned char*`。
- **count**：请求读取的**最大字节数**（缓冲区大小）。

**返回值：**

- **成功**：返回实际读取的字节数（`ssize_t`）。这个值可能小于 `count`，例如读到文件末尾时返回 0。

- **失败**：返回 `-1`，并设置全局变量 `errno` 以指示错误。

- 返回值详解

  - **正数**：实际读取的字节数。如果请求读取 100 字节，但文件只剩 50 字节，则返回 50。

  - **0**：表示已到达文件末尾（EOF），没有更多数据可读。

  - **-1**：发生错误，具体原因需查看 `errno`。
  - **注意**：`read` 返回 0 仅当文件偏移量已经到达文件末尾。如果是一个空文件，第一次调用就会返回 0。



------

## **示例1: 创建并写入文件**

```cpp
//服务器程序
#include <iostream>
#include <cstdio>
#include <cstring>
#include <fcntl.h>
#include <unistd.h>
using namespace std;

int main()
{
	int fd;

	fd = open("data.txt",O_RDWR|O_CREAT|O_TRUNC);
	if(fd==-1)
	{
		perror("open(data.txt)");
		return -1;
	}
	printf("文件描述符fd=%d\n",fd);

	char buffer[1024];
	strcpy(buffer,"文档中的内容");

	if(write(fd,buffer,strlen(buffer))==-1)
	{
		perror("write");
		return -1;
	}
	close(fd);

}
```

```sh
root@LAPTOP-P5RJLSIB:/mnt/d/桌面/cpp# g++ -std=gnu++11 server.cpp -o demo
root@LAPTOP-P5RJLSIB:/mnt/d/桌面/cpp# ./demo
文件描述符fd=3
root@LAPTOP-P5RJLSIB:/mnt/d/桌面/cpp# cat data.txt
文档中的内容root
```



## 示例2:读取文件

```cpp
//服务器程序
#include <iostream>
#include <cstdio>
#include <cstring>
#include <fcntl.h>
#include <unistd.h>
using namespace std;

int main(int argc,char* argv[])
{
	if(argc!=2)
	{
		printf("using error\n");
		return -1;
	}

	int fd;

	fd = open(argv[1],O_RDONLY);
	if(fd==-1)
	{
		perror("open");
		return -1;
	}
	printf("文件描述符fd=%d\n",fd);

	char buffer[1024];
	memset(buffer,0,sizeof buffer);
	if(read(fd,buffer,sizeof(buffer))==-1)
	{
		perror("read");
		return -1;
	}
	printf("内容:%s",buffer);
	close(fd);

}
```

```sh
root@LAPTOP-P5RJLSIB:/mnt/d/桌面/cpp# g++ -std=gnu++11 server.cpp -o demo
root@LAPTOP-P5RJLSIB:/mnt/d/桌面/cpp# ./demo
using error
root@LAPTOP-P5RJLSIB:/mnt/d/桌面/cpp# ./demo data.txt
文件描述符fd=3
内容:文档中的内容
```



# socket函数

`socket` 是 Linux/Unix 系统网络编程中最基础的函数，用于创建一个通信端点（套接字）。

```cpp
#include <sys/socket.h>

int socket(int domain, int type, int protocol);
```

**返回值:**

- **成功**：返回一个**非负整数的文件描述符**，代表新创建的套接字。
- **失败**：返回 `-1`，并设置全局变量 `errno` 以指示具体错误原因。

> 网络编程中绝大多数函数在失败时都返回 `-1` 并设置 `errno`，这是 UNIX 系统调用的惯例。

## 参数详解

### `domain`（协议族）

指定套接字使用的协议族（又称地址族）。常用值：

| 宏定义      | 含义                     | 说明                               |
| :---------- | :----------------------- | :--------------------------------- |
| `AF_INET`   | IPv4 协议族              | 最广泛使用的互联网协议             |
| `AF_INET6`  | IPv6 协议族              | 下一代互联网协议，尚未完全普及     |
| `AF_UNIX`   | 本地通信（Unix域套接字） | 用于同一主机上的进程间通信，效率高 |
| `AF_PACKET` | 底层包接口               | 直接访问链路层，常用于抓包工具     |
| `AF_IPX`    | IPX Novell 协议族        | 已过时，几乎不再使用               |

> **历史小知识**：早期 BSD 网络实现中，`AF_`（地址族）和 `PF_`（协议族）有细微区别，但现在 Linux 中 `AF_XXX` 和 `PF_XXX` 的值完全相等，通常混用。建议使用 `AF_` 系列。

### `type`（套接字类型）

指定套接字的通信语义。常用值：

| 宏定义           | 含义                     | 特点                                                         |
| :--------------- | :----------------------- | :----------------------------------------------------------- |
| `SOCK_STREAM`    | 面向连接的可靠流式套接字 | 提供有序、可靠、双向的字节流，无记录边界（典型协议：TCP）    |
| `SOCK_DGRAM`     | 无连接的数据报套接字     | 提供固定最大长度的数据报，可能丢失、乱序（典型协议：UDP）    |
| `SOCK_RAW`       | 原始套接字               | 允许直接访问底层协议（如 ICMP），需要 root 权限              |
| `SOCK_SEQPACKET` | 有序可靠的数据报套接字   | 与流式类似但保留消息边界（如 SCTP）                          |
| `SOCK_NONBLOCK`  | 与 `O_NONBLOCK` 类似     | 可与 `SOCK_*` 类型按位或，使新建套接字非阻塞（Linux 2.6.27+） |
| `SOCK_CLOEXEC`   | 设置 `FD_CLOEXEC` 标志   | 执行 exec 时自动关闭该套接字（避免泄漏，Linux 2.6.27+）      |

### `protocol`（具体协议）

指定实际使用的传输协议。**在给定的协议族和套接字类型下，通常只有一个协议支持，此时可以填 `0`，让系统自动选择**。常见组合：

- `socket(AF_INET, SOCK_STREAM, 0)` → 自动选择 TCP（等同于 `IPPROTO_TCP`）
- `socket(AF_INET, SOCK_DGRAM, 0)` → 自动选择 UDP（等同于 `IPPROTO_UDP`）
- 显式指定协议值：
  - `IPPROTO_TCP` (6)
  - `IPPROTO_UDP` (17)
  - `IPPROTO_ICMP` (1) 常用于原始套接字

> 对于 `SOCK_RAW` 类型，`protocol` 通常指定要处理的 IP 协议号（如 `IPPROTO_ICMP`）。

------

## 资源限制与注意事项

### 文件描述符限制

套接字在 Unix 中是一种**文件描述符**，因此受进程文件描述符数量限制：

- 查看当前限制：`ulimit -n`
- 修改限制（临时）：`ulimit -n 4096`
- 系统级限制：`/etc/security/limits.conf`

每个进程能打开的套接字数量有限，务必在不用时调用 `close` 关闭。

### 常见编程模式

- **TCP 流式套接字**：通常用于客户端/服务器模型，后续需要 `bind`、`listen`、`accept`（服务器）或 `connect`（客户端）。
- **UDP 数据报套接字**：无连接，可直接 `sendto` / `recvfrom`，也可 `connect` 后使用 `send` / `recv` 简化操作。
- **原始套接字**：用于实现自定义协议或网络诊断（如 ping 命令）。

###  地址族与协议族的可移植性

虽然 Linux 中 `AF_` 和 `PF_` 等价，但为保持可移植性，建议：

- `socket` 的第一个参数使用 `PF_` 系列（协议族），
- `bind` 和 `connect` 中的地址结构使用 `AF_` 系列（地址族）。

不过在现代系统中，两者完全一致，直接使用 `AF_` 更常见。

### 高级标志位

Linux 允许在 `type` 参数中按位或上以下标志（无需额外 `fcntl` 调用）：

- `SOCK_NONBLOCK`：直接创建非阻塞套接字。
- `SOCK_CLOEXEC`：设置执行时关闭标志。

例如：

```
int sock = socket(AF_INET, SOCK_STREAM | SOCK_NONBLOCK | SOCK_CLOEXEC, 0);
```





# 主机字节序与网络字节序

在计算机系统中，多字节数据（如 `short`、`int`、`long` 等）在内存中的存储顺序称为**字节序（Byte Order）**。不同架构的 CPU 采用不同的字节序，这给跨平台网络通信带来了挑战。为了统一，网络协议规定了**网络字节序（Network Byte Order）**，所有参与通信的主机必须将自己的数据转换为网络字节序后再发送。

---

## 字节序的分类

如果数据类型占用的内存空间大于 1 字节，CPU 将数据存放在内存中的方式有两种：

### 大端序（Big Endian）
- **高位字节存放在低地址，低位字节存放在高地址**。
- 即按照人类阅读的顺序存储：数据的高位部分放在内存的开始位置。

### 小端序（Little Endian）
- **低位字节存放在低地址，高位字节存放在高地址**。
- 即数据的低位部分放在内存的开始位置，看起来像是“颠倒”的。

#### 示例
假设从内存地址 `0x00000001` 处开始存储十六进制数 `0x12345678`（共 4 字节），两种字节序的布局如下：

| 内存地址   | 大端序 | 小端序 |
| ---------- | ------ | ------ |
| 0x00000001 | 0x12   | 0x78   |
| 0x00000002 | 0x34   | 0x56   |
| 0x00000003 | 0x56   | 0x34   |
| 0x00000004 | 0x78   | 0x12   |

- **大端序**：数据 `0x12 0x34 0x56 0x78` 顺序存放。
- **小端序**：数据 `0x78 0x56 0x34 0x12` 顺序存放。

#### 常见 CPU 字节序
- **Intel x86、x86_64 系列**：小端序。
- **ARM 系列**：可配置（通常运行于小端序，但支持大端）。
- **PowerPC、SPARC、Motorola 68000 等**：大端序。
- **网络协议**：规定使用大端序。

---

## 为什么需要网络字节序

网络编程中，数据最终通过套接字（Socket）发送，而套接字本质上是文件描述符，数据写入套接字相当于写入文件。如果发送方和接收方的主机字节序不同，直接传输多字节数据会导致接收方解析错误。例如：
- 发送方（小端）将整数 `0x12345678` 以内存原始字节发送，实际发送的字节序列是 `0x78 0x56 0x34 0x12`。
- 接收方（大端）收到后按大端序解释，得到 `0x78563412`，与原始数据完全不同。

为了解决这一歧义，**TCP/IP 协议栈规定所有协议头中的多字节整数（如端口号、IP 地址）必须使用大端序（网络字节序）传输**。应用程序在填充协议数据结构（如 `sockaddr_in`）或发送二进制数据时，也应当遵循这一约定。

---

## 字节序转换函数

C 语言标准库（`<arpa/inet.h>` 或 `<netinet/in.h>`）提供了四个函数，用于在主机字节序和网络字节序之间转换：

```c
#include <arpa/inet.h>

uint32_t htonl(uint32_t hostlong);      // 32位主机字节序 → 网络字节序
uint16_t htons(uint16_t hostshort);     // 16位主机字节序 → 网络字节序
uint32_t ntohl(uint32_t netlong);       // 32位网络字节序 → 主机字节序
uint16_t ntohs(uint16_t netshort);      // 16位网络字节序 → 主机字节序
```

### 命名规则
- **h**：host（主机）
- **to**：转换到
- **n**：network（网络）
- **s**：short（16位，对应 `uint16_t`）
- **l**：long（32位，对应 `uint32_t`，注意这里的 long 在历史上是 32 位）

### 使用说明
- 这些函数在主机字节序为小端时执行实际转换；如果主机本身就是大端（网络字节序），则函数被定义为空宏，直接返回原值，无性能开销。
- 参数类型明确，避免了符号扩展问题。
- **注意**：转换的是**整数数值**，而不是字节数组。对于已经按网络字节序组织的数据（如从网络接收的字节流），不应再次调用这些函数。

---

## IP 地址与端口号的字节序

### 端口号
端口号是 16 位无符号整数（0~65535），在 `sockaddr_in` 结构体中用 `sin_port` 字段存储。**必须使用网络字节序**。

```c
struct sockaddr_in addr;
addr.sin_port = htons(8080);  // 将主机字节序的 8080 转为网络字节序
```

### IPv4 地址
IPv4 地址本质上是 32 位无符号整数（如 `192.168.1.1` 对应 `0xC0A80101`）。在 `sockaddr_in` 中，`sin_addr.s_addr` 字段也**必须使用网络字节序**。

通常我们使用以下函数进行转换：
- `inet_aton()` / `inet_pton()`：将点分十进制字符串转换为网络字节序的二进制值。
- `inet_ntoa()` / `inet_ntop()`：将网络字节序的二进制值转换为点分十进制字符串。

这些函数内部已经处理了字节序，返回的 `s_addr` 直接就是网络字节序，无需再调用 `htonl`。

```c
struct sockaddr_in addr;
inet_pton(AF_INET, "192.168.1.1", &addr.sin_addr);  // addr.sin_addr.s_addr 已是网络字节序
```

如果手动构造地址（例如使用 `INADDR_ANY`），需要注意：
```c
addr.sin_addr.s_addr = htonl(INADDR_ANY);  // INADDR_ANY 是主机字节序的 0，但转换后仍为 0，无影响
addr.sin_addr.s_addr = htonl(0xC0A80101);  // 将 0xC0A80101 转网络字节序，若主机为小端则实际变成 0x0101A8C0
```

---

## 实际编程中的注意事项

### 自动转换机制
- **数据收发时**：`send()` / `recv()` 处理的是字节流，应用程序需自行保证多字节数据的字节序正确。TCP 不提供任何自动转换，UDP 同样如此。
- **协议头填充**：如自定义协议中的长度字段、序列号等，在填充前必须调用 `hton` 系列函数。
- **地址结构填充**：只有向 `sockaddr_in` 的 `sin_port` 和 `sin_addr.s_addr` 赋值时才需要显式转换。其他情况下（如使用 `inet_pton` 或 `getaddrinfo`），库函数已处理。

### 何时不需要转换
- 单字节数据（`char` 数组）不受字节序影响，直接传输即可。
- 如果通信双方约定使用特定字节序（例如都使用小端），可以省去转换，但会丧失可移植性。强烈建议遵循网络字节序标准。

###  检测主机字节序
若需在程序中判断当前主机是大端还是小端，可以使用联合体（union）技巧：

```c
#include <stdio.h>

int main() {
    union {
        short s;
        char c[sizeof(short)];
    } un;
    un.s = 0x0102;
    if (sizeof(short) == 2) {
        if (un.c[0] == 1 && un.c[1] == 2)
            printf("大端序\n");
        else if (un.c[0] == 2 && un.c[1] == 1)
            printf("小端序\n");
        else
            printf("未知\n");
    }
    return 0;
}
```

### 常见错误
- 对 IP 地址字符串直接赋值给 `sin_addr.s_addr` 后忘记转换（例如 `addr.sin_addr.s_addr = 0xC0A80101;` 在小端机上错误）。
- 对端口号直接赋值（例如 `addr.sin_port = 8080;`）而不使用 `htons`。
- 重复转换：例如先 `inet_pton` 得到网络字节序，又调用 `htonl`，导致字节序错误。
- 混淆 `htonl` 和 `htons` 的参数类型（例如将 32 位地址用 `htons` 转换）。



## 总结

| 概念       | 说明                                                         |
| ---------- | ------------------------------------------------------------ |
| 大端序     | 高位字节在低地址，低位字节在高地址（网络字节序采用此方式）   |
| 小端序     | 低位字节在低地址，高位字节在高地址（Intel x86 系列采用）     |
| 网络字节序 | TCP/IP 协议规定的字节序（大端），所有协议头中的多字节数必须为此格式 |
| 转换函数   | `htonl`、`htons`、`ntohl`、`ntohs`，用于主机与网络字节序之间的转换 |
| 应用场景   | 填充 `sockaddr_in` 的 `sin_port` 和 `sin_addr.s_addr` 时必须转换 |
| 注意事项   | 字符数组无需转换；使用 `inet_pton` 等函数自动处理地址转换    |







# Socket 地址结构详解

在网络编程中，标识一个通信端点需要协议族、IP 地址和端口号。这些信息被封装在特定的结构体中，供 `bind`、`connect`、`accept` 等函数使用。

---

## 通用地址结构 `sockaddr`

早期 BSD Unix 定义了通用的套接字地址结构 `sockaddr`，用于统一不同协议族的地址表示。其定义如下：

```c
struct sockaddr {
    unsigned short sa_family;   // 协议族，如 AF_INET
    char           sa_data[14]; // 14字节的协议地址（包含IP和端口）
};
```

- **sa_family**：地址族，与 `socket()` 函数的 `domain` 参数一致，通常填 `AF_INET`。
- **sa_data**：存放具体的协议地址，对于 IPv4，前 2 字节是端口号（网络字节序），后 4 字节是 IP 地址，剩余字节填充 0。

这种设计的优点是接口通用，所有地址结构都可以强制转换为 `struct sockaddr *` 传递给系统调用。但缺点是用户需要手动填充 `sa_data`，非常不便。因此，更专用的 `sockaddr_in` 结构被引入。

---

## IPv4 专用地址结构 `sockaddr_in`

`sockaddr_in` 专门用于 IPv4，其大小与 `sockaddr` 相同（16 字节），可以互相转换。它清晰地将协议族、端口和 IP 地址分开，极大方便了编程。

```c
struct sockaddr_in {
    unsigned short   sin_family;   // 协议族，AF_INET
    unsigned short   sin_port;     // 16位端口号，网络字节序
    struct in_addr   sin_addr;     // 32位IPv4地址，网络字节序
    unsigned char    sin_zero[8];  // 填充，使总大小与 sockaddr 一致
};

struct in_addr {
    unsigned int s_addr;           // 32位IPv4地址，网络字节序
};
```

### 使用要点
- **sin_family**：必须设置为 `AF_INET`。
- **sin_port**：端口号需要用 `htons()` 转换为网络字节序。
- **sin_addr.s_addr**：IP 地址需要用 `htonl()` 或相关函数转换为网络字节序。
- **sin_zero**：仅用于填充，一般初始化为 0（可用 `bzero` 或 `memset` 置零）。

### 示例
```c
struct sockaddr_in servaddr;
servaddr.sin_family = AF_INET;
servaddr.sin_port = htons(8080);
servaddr.sin_addr.s_addr = htonl(INADDR_ANY); // 或 inet_addr("192.168.1.1")
memset(servaddr.sin_zero, 0, sizeof(servaddr.sin_zero));
```



## 主机名解析函数 `gethostbyname`

在客户端程序中，我们常常需要通过域名（如 `www.example.com`）或主机名获取 IP 地址。`gethostbyname` 是一个传统的解析函数，它返回一个 `hostent` 结构。

```c
#include <netdb.h>
struct hostent *gethostbyname(const char *name);
```

### `hostent` 结构
```c
struct hostent {
    char  *h_name;            // 官方主机名
    char **h_aliases;         // 别名列表
    int    h_addrtype;        // 地址类型（AF_INET 或 AF_INET6）
    int    h_length;          // 地址长度（IPv4为4，IPv6为16）
    char **h_addr_list;       // 地址列表（网络字节序）
};
#define h_addr h_addr_list[0] // 兼容旧代码，指向第一个地址
```

### 使用方法
1. 调用 `gethostbyname`，传入域名或字符串 IP。
2. 检查返回值是否为 `NULL`（出错，可用 `h_errno` 获取错误码）。
3. 从 `h_addr_list` 中取出所需地址（通常是第一个）。
4. 将地址复制到 `sockaddr_in.sin_addr` 中。

```c
struct hostent *h = gethostbyname("www.example.com");
if (h == NULL) {
    herror("gethostbyname error");
    return -1;
}
memcpy(&servaddr.sin_addr, h->h_addr, h->h_length);
```

### 注意事项
- `gethostbyname` 不支持 IPv6，且线程不安全（返回静态数据）。
- 现代编程推荐使用 **`getaddrinfo`**，它同时支持 IPv4 和 IPv6，且线程安全。

---

## 字符串 IP 与大端序 IP 的转换

服务端程序常常需要处理点分十进制 IP 字符串（如 `"192.168.1.1"`）与二进制大端序 IP 之间的转换。C 标准库提供了一组函数。

- n->network
- a->assic

### `inet_addr`（简单但有限）
```c
in_addr_t inet_addr(const char *cp);
```
- 将字符串 IP 转换为 32 位网络字节序的整数。
- 成功返回转换后的值，失败返回 `INADDR_NONE`（通常是 `-1`，即 `255.255.255.255`）。
- **缺点**：无法区分有效地址 `255.255.255.255` 和错误，且不支持更多格式。

### `inet_aton`（推荐）
```c
int inet_aton(const char *cp, struct in_addr *inp);
```
- 将字符串 IP 转换为网络字节序，结果存入 `inp` 指向的结构。
- 成功返回非 0，失败返回 0。
- 更安全，能正确处理 `255.255.255.255`。

### `inet_ntoa`（IP 转字符串）
```c
char *inet_ntoa(struct in_addr in);
```
- 将网络字节序的 IP 地址转换为点分十进制字符串。
- 返回的字符串指向静态缓冲区，后续调用会覆盖，因此不是线程安全的。如需保留，应拷贝出来。

### 现代替代函数
- **`inet_pton`** 和 **`inet_ntop`**：支持 IPv4 和 IPv6，线程安全，推荐使用。
```c
int inet_pton(int af, const char *src, void *dst);
const char *inet_ntop(int af, const void *src, char *dst, socklen_t size);
```

---

## 总结

| 结构/函数          | 作用                                 | 注意事项                                        |
| ------------------ | ------------------------------------ | ----------------------------------------------- |
| `sockaddr`         | 通用地址结构，作为参数类型统一接口   | 实际使用中需强制转换为具体协议族的专用结构      |
| `sockaddr_in`      | IPv4 专用地址结构，包含端口和 IP     | 填充时需注意字节序转换（`htons`/`htonl`）       |
| `gethostbyname`    | 根据主机名获取 IP 地址列表（已过时） | 线程不安全，不支持 IPv6；建议改用 `getaddrinfo` |
| `inet_addr`        | 字符串 IP → 网络字节序整数（旧）     | 无法表示错误，不推荐使用                        |
| `inet_aton`        | 字符串 IP → `in_addr` 结构（安全）   | 成功返回非 0，失败返回 0                        |
| `inet_ntoa`        | 网络字节序 IP → 字符串 IP            | 返回静态缓冲区，非线程安全                      |
| `inet_pton`/`ntop` | 现代地址转换函数，支持 IPv4/IPv6     | 线程安全，推荐使用                              |

| 函数        | 全称                          | 作用对象          | 转换方向                                 | 典型用途                             |
| :---------- | :---------------------------- | :---------------- | :--------------------------------------- | :----------------------------------- |
| `inet_ntoa` | Internet **Network to ASCII** | IPv4 地址（32位） | 网络字节序的二进制 IP → 点分十进制字符串 | 将 IP 显示给人看（如打印客户端地址） |
| `htons`     | **Host TO Network Short**     | 端口号（16位）    | 主机字节序 → 网络字节序                  | 将端口号填入 `sockaddr_in` 结构      |



在 Linux C++ 网络编程中，创建套接字（`socket`）之后，服务端通常需要经历绑定地址（`bind`）、监听（`listen`）、接受连接（`accept`）以及数据收发（`recv`/`send`）等步骤。下面详细介绍这些函数。

------

## bind 函数

将套接字与特定的本地地址（IP 和端口）绑定。

```cpp
#include <sys/socket.h>

int bind(int sockfd, const struct sockaddr *addr, socklen_t addrlen);
```

**参数**

- **sockfd**：由 `socket` 函数返回的文件描述符。
- **addr**：指向协议地址结构的指针（如 `struct sockaddr_in`），包含要绑定的 IP 和端口。
- **addrlen**：地址结构的长度，通常使用 `sizeof(struct sockaddr_in)`。

**返回值**

- 成功返回 0。
- 失败返回 -1，并设置 `errno`。

**注意事项**

1. **端口占用**：绑定的端口可能已被其他进程使用，此时会返回 `EADDRINUSE` 错误。可设置 `SO_REUSEADDR` 选项允许重用处于 `TIME_WAIT` 状态的端口。

   ```cpp
   int opt = 1;
   setsockopt(sockfd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));
   ```

   

2. **地址通配符**：若希望接受任何本地接口的连接，可使用 `INADDR_ANY`（IPv4）或 `in6addr_any`（IPv6）。

   ```cpp
   struct sockaddr_in addr;
   addr.sin_addr.s_addr = htonl(INADDR_ANY);
   ```

   

3. **端口号**：若指定端口为 0，系统会自动分配一个临时端口（常用于客户端）。

4. **权限**：绑定低于 1024 的端口通常需要超级用户权限。

------

## listen 函数

将套接字从主动变为被动，使其可以接受客户端的连接请求。

```cpp
#include <sys/socket.h>

int listen(int sockfd, int backlog);
```

**参数**

- **sockfd**：已绑定的套接字描述符。
- **backlog**：等待连接队列的最大长度。表示内核为此套接字排队的最大已完成连接（已完成三次握手）和未完成连接（尚未完成三次握手）的数量总和。具体含义与系统实现有关，通常设置为 5~128 之间的值。

**返回值**

- 成功返回 0。
- 失败返回 -1，并设置 `errno`。

**注意事项**

1. **backlog 大小**：现代 Linux 系统，`backlog` 参数会受到 `/proc/sys/net/core/somaxconn` 和 `net.ipv4.tcp_max_syn_backlog` 的限制，实际值可能被截断。
2. **仅用于 TCP**：`listen` 仅适用于面向连接的流式套接字（`SOCK_STREAM`）。
3. **多次调用**：通常在调用 `bind` 之后立即调用，不可对已连接的套接字调用。
4. **连接队列**：若队列满，客户端可能收到 `ECONNREFUSED` 或连接超时。

------

## accept 函数

从已完成连接队列中取出第一个连接，创建一个新的套接字用于与客户端通信。

```cpp
#include <sys/socket.h>

int accept(int sockfd, struct sockaddr *addr, socklen_t *addrlen);
```

**参数**

- **sockfd**：监听套接字（由 `socket` 创建并经过 `bind` 和 `listen`）。
- **addr**：指向一个地址结构，用于存放客户端的协议地址。如果不关心客户端地址，可设为 `NULL`。
- **addrlen**：值-结果参数。调用前应初始化为 `addr` 指向的缓冲区大小；返回时包含实际存入的地址长度。

**返回值**

- 成功返回一个新的套接字描述符（已连接套接字），用于与特定客户端通信。
- 失败返回 -1，并设置 `errno`。

**注意事项**

1. **阻塞与非阻塞**：默认情况下，若无连接请求，`accept` 会阻塞直到有连接到达。可通过设置监听套接字为非阻塞模式（`O_NONBLOCK`）来避免阻塞。
2. **继承属性**：新返回的套接字会继承监听套接字的属性（如阻塞状态、套接字选项等）。
3. **信号中断**：如果被信号中断，`accept` 可能返回 -1 且 `errno` 为 `EINTR`，此时通常应重新调用。
4. **并发模型**：典型的并发服务器会为每个 `accept` 返回的套接字创建一个新进程或线程来处理通信。
5. **地址获取**：若需要获取客户端 IP 和端口，可通过 `addr` 参数获得。也可使用 `getpeername` 函数在之后获取。



----



## recv 函数

```cpp
#include <sys/socket.h>

ssize_t recv(int sockfd, void *buf, size_t len, int flags);
```

**参数**

- **sockfd**：已连接套接字描述符。
- **buf**：接收数据缓冲区。
- **len**：缓冲区大小。
- **flags**：控制标志，常用值为 0。其他如 `MSG_PEEK`（窥读数据而不移除）、`MSG_WAITALL`（等待直到接收满 len 字节）等。

**返回值**

- 成功返回实际接收到的字节数。若对端关闭连接，返回 0。
- 失败返回 -1，并设置 `errno`。

## send 函数

```cpp
#include <sys/socket.h>

ssize_t send(int sockfd, const void *buf, size_t len, int flags);
```

**参数**

- **sockfd**：已连接套接字描述符。
- **buf**：待发送数据的缓冲区。
- **len**：要发送的字节数。
- **flags**：控制标志，常用 0。例如 `MSG_DONTWAIT`（非阻塞发送）、`MSG_NOSIGNAL`（禁止产生 `SIGPIPE` 信号）。

**返回值**

- 成功返回实际发送的字节数（可能小于 `len`，需循环发送）。
- 失败返回 -1，并设置 `errno`。

**注意事项（recv/send 通用）**

1. **部分收发**：`recv` 和 `send` 不能保证一次收发所有请求的字节数。对于 `recv`，若对端发送数据较少，可能返回少于 `len` 的数据；对于 `send`，若内核缓冲区不足，可能只发送部分数据。因此通常需要循环调用。
2. **阻塞模式**：默认是阻塞的。若套接字设为非阻塞，无数据时 `recv` 返回 -1 且 `errno` 为 `EAGAIN` 或 `EWOULDBLOCK`；发送缓冲区满时 `send` 同样返回该错误。
3. **连接关闭**：
   - `recv` 返回 0 表示对端已关闭连接（FIN）。
   - 向已关闭的套接字发送数据会产生 `SIGPIPE` 信号（默认终止进程），可设置 `MSG_NOSIGNAL` 标志或使用 `send` 并忽略信号，然后通过 `errno` 为 `EPIPE` 判断。
4. **flags 使用**：一般填 0。特殊需求可参考手册。
5. **缓冲区大小**：可通过 `setsockopt` 调整收发缓冲区大小。
6. **与 read/write 的关系**：`recv`/`send` 专门用于套接字，支持 flags 参数。对于 TCP，`read`/`write` 也可用于套接字，但功能较弱。
