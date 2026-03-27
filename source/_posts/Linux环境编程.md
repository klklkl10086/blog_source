---
title: Linux环境编程
date: 2026-01-31 20:51:35
tags: ["Linux","CPP"]
categories: ["CPP开发"]
description: CPP开发基础知识
---

> [参考课程](https://www.bilibili.com/video/BV1wG411k7tm/?share_source=copy_web&vd_source=777aaa8a415b68222e598d976e64642c)
>
> 参考书目：《UNIX环境高级编程》

# gcc/g++编译命令

基本编译流程：**预处理 → 编译 → 汇编 → 链接**

1. 预处理：处理宏、头文件、条件编译等 
   - 展开所有宏定义
   - 处理所有`#include`指令
   - 处理条件编译指令(`#ifdef`, `#ifndef`, `#if`, `#else`, `#endif`)
   - 删除所有注释
   - 添加行号和文件名标识（可使用`-P`去除）
   - 保留`#pragma`指令
2. 编译：将预处理后的代码转换为汇编语言
   - 词法分析和语法分析
   - 语义分析
   - 中间代码生成
   - 代码优化
   - 生成目标平台的汇编代码
3. 汇编：将汇编代码转换为机器码（目标文件）
   - 将汇编指令翻译为机器指令
   - 生成可重定位的目标文件(.o文件)
   - 生成符号表
   - 处理标签和地址引用
4. 链接：将多个**目标文件**和**库文件**连接成**可执行文件**
   - 符号解析（解决未定义的引用）
   - 重定位（调整地址引用）
   - 合并代码和数据段
   - 链接启动代码和库文件
   - 生成最终的可执行文件格式



- gcc：c语言的编译工具
- g++：cpp的编译工具

## 命令选项

| 选项          | 描述                 | 示例                                |
| :------------ | :------------------- | :---------------------------------- |
| `-o <file>`   | 指定输出文件名       | `gcc -o program main.c`             |
| `-E`          | 只预处理，不编译     | `gcc -E main.c -o main.i`           |
| `-S`          | 生成汇编代码         | `gcc -S main.c -o main.s`           |
| `-c`          | 编译生成机器码不链接 | `gcc -c main.c -o main.o`           |
| `-save-temps` | 保存所有中间文件     | `gcc -save-temps main.c -o program` |
| `-pipe`       | 使用管道代替临时文件 | `gcc -pipe main.c -o program`       |

**优化级别选项：**

| 选项     | 描述             | 效果                           |
| :------- | :--------------- | :----------------------------- |
| `-O0`    | 不优化（默认）   | 编译快，调试方便               |
| `-O1`    | 基本优化         | 减少代码大小和执行时间         |
| `-O2`    | 更多优化（推荐） | 包括所有不涉及空间换时间的优化 |
| `-O3`    | 激进优化         | 包括向量化等高级优化           |
| `-Os`    | 优化代码大小     | 优先减小可执行文件大小         |
| `-Ofast` | 快速优化         | 可能违反严格标准               |
| `-Og`    | 优化调试体验     | 在保持可调试性的同时优化       |

如果使用了优化选项：

- 编译的时间将更长；
- 目标程序不可调试；
- 有效果，但是不可能显著提升程序的性能。(关键还是要看源代码的实现)

## 目标文件 vs 可执行文件

| 特性             | 目标文件 (.o/.obj)             | 可执行文件                      |
| :--------------- | :----------------------------- | :------------------------------ |
| **文件扩展名**   | .o (Unix/Linux) .obj (Windows) | 无扩展名 (Linux) .exe (Windows) |
| **文件类型**     | 可重定位目标文件               | 可执行目标文件                  |
| **链接状态**     | 未链接                         | 已完全链接                      |
| **能否直接运行** | ❌ 不能直接执行                 | ✅ 可以直接运行                  |
| **地址引用**     | 相对地址/未解析符号            | 绝对地址/已解析符号             |
| **包含内容**     | 单个模块的代码和数据           | 完整程序的所有代码和数据        |
| **段结构**       | 需要重定位的段                 | 加载到内存的最终段              |
| **依赖关系**     | 依赖其他目标文件/库            | 可能依赖动态库，但独立运行      |





示例：将hello.c编译为可执行文件hello

```bash
# 第1步：预处理
gcc -E hello.c -o hello.i

# 第2步：编译为汇编
gcc -S hello.i -o hello.s

# 第3步：汇编为目标文件
gcc -c hello.s -o hello.o

# 第4步：链接为可执行文件
gcc hello.o -o hello
# 运行程序
./hello

# 一步完成所有步骤（对比）
gcc hello.c -o hello_one_step
```



# 静态库、动态库

> 一般来讲，通用的函数和类不提供源代码文件，而是编译成二进制文件。

库的**二进制文件**：

- 静态库
- 动态库

**如果动态库和静态库同时存在，编译器将优先使用动态库。**

## 静态库

- **文件扩展名**: `.a` (Unix/Linux), `.lib` (Windows)
- **本质**: 多个目标文件(`.o`)的归档文件
- **链接时机**: **编译/链接时**
- **特点**: 
  - 程序在编译时会把库文件的二进制代码链接到目标程序中
  - 库代码被复制到最终的可执行文件中
  - 如果多个程序中用到了同一静态库中的函数或类，就会存在多份拷贝
  - 静态库的链接是在编译时期完成的，执行的时候代码加载速度快。
  - 生成的目标程序的可执行文件比较大，浪费空间。
  - 程序的更新和发布不方便，如果某一个静态库更新了，所有使用它的程序都需要重新编译



### 创建方式

```bash
g++ -c -o lib库名.a 源代码文件清单
```

```bash
g++ -c -o libpublic.a  public.cpp
#会生成libpublic.a  是一个二进制文件
```



### 使用方式

```bash
g++ 选项 源代码文件名清单 -l库名 -L库文件所在的目录名
```

```bash
g++ -o demo01 demo01.cpp -lpublic -L/home/wucz/tools
```





## 动态库

- **文件扩展名**: `.so` (Unix/Linux), `.dll` (Windows), `.dylib` (macOS)
- **本质**: 独立的可执行代码模块
- **链接时机**: **运行时**
- **特点**:
  -  可执行文件只包含引用，**运行时动态加载**
  - 如果多个进程中用到了同一动态库中的函数或类，那么在内存中只有一份，避免了空间浪费问题
  - 程序在运行的过程中，需要用到动态库的时候才把动态库的二进制代码载入内存。
  - 可以实现进程之间的代码共享，因此动态库也称为共享库。
  - 程序升级比较简单，不需要重新编译程序，只需要更新(重新制作)动态库就行了。



### 创建方式

```
g++ -fPIC -shared -o lib库名.so 源代码文件清单
```

```bash
g++ -fPIC -shared -o libpublic.so public.cpp
gcc -fPIC -shared -o libmath.so mathlib.c
```

| 选项      | 全称                      | 含义                 | 作用阶段     |
| :-------- | :------------------------ | :------------------- | :----------- |
| `-fPIC`   | Position Independent Code | 生成位置无关代码     | **编译阶段** |
| `-shared` | Shared Library            | 生成共享库（动态库） | **链接阶段** |

### 使用方式

运行可执行程序的时候，**需要提前设置LD_LIBRARY_PATH环境变量**，即指定动态库的目录

```
g++ 选项 源代码文件名清单 -l库名 -L库文件所在的目录名
```

```bash
g++ -o demo01  demo01.cpp -lpublic -L/home/wucz/tools
```





# Makefile

**Makefile** 是一个用于自动化构建程序的脚本文件，由 `make` 工具解析执行。它定义了：

- 项目的编译规则
- 文件的依赖关系
- 如何生成目标文件

## 编写规则

```
target: prerequisites
    recipe
```

**组成部分**：

- **target（目标）**：要生成的文件名或操作名
- **prerequisites（依赖）**：生成目标所需的文件列表
- **recipe（命令）**：生成目标的具体命令（必须用 **Tab** 缩进）



示例:

```bash
#定义变量
#-I 选项用于指定头文件的搜索路径
INCLUDEDIR=-I/home/wucz/tools -I/home/wucz/api
LIBDIR=-L/home/wucz/tools -L/home/wucz/api
#要生成的可执行文件
all:demo01 demo02 demo03
#每一个可执行文件所依赖的文件
demo01:demo01.cpp#接下来是TAB键
        g++ -o demo01 demo01.cpp $(INCLUDEDIR) $(LIBDIR) -lpublic -lmyapi

demo02:demo02.cpp
        g++ -o demo02 demo02.cpp $(INCLUDEDIR) $(LIBDIR) -lpublic -lmyapi

demo03:demo03.cpp
        g++ -o demo03 demo03.cpp $(INCLUDEDIR) $(LIBDIR) -lpublic -lmyapi

clean:
        rm -f demo01 demo02 demo03

```





# main函数的参数

```cpp
int main()
int main(int argc, char* argv[]) // int main(int argc, char** argv)
int main(int argc, char* argv[], char* envp[])//int main(int argc, char** argv, char** envp)
```

1. **argc**（Argument Count）

   - 类型：`int`
   - 含义：命令行参数的数量（包括程序名本身）
   - 至少为1（程序名本身）

2. **argv**（Argument Vector）

   - 类型：`char*[]` 或 `char**`
   - 含义：字符串指针数组，存储所有命令行参数
   - `argv[0]`：程序名称（可能包含路径）
   - `argv[1]` 到 `argv[argc-1]`：用户传入的参数
   - `argv[argc]`：总是一个空指针（NULL）

3. **envp**（Environment Pointer）

   用于接收操作系统的**环境变量**。虽然这不是C++标准规定的，但在大多数编译器和平台上都支持。

   - 类型：`char*[]` 或 `char**`
   - 含义：指向环境变量字符串数组的指针
   - 每个字符串格式：`变量名=值`
   - 数组以 `NULL` 指针结尾
   - 典型环境变量：
     - `PATH`：系统路径
     - `HOME`：用户主目录（Unix/Linux）
     - `USERNAME`：用户名（Windows）
     - `TEMP`/`TMP`：临时目录
     - `OS`：操作系统类型

```cpp
#include<iostream>
using namespace std;
int main(int argc,char** argv,char** envp)
{
    cout<<"传入参数数目:"<<argc<<endl;
    for(int i=0;i<argc;i++)
    {
        cout<<"第"<<i+1<<"个参数是:"<<argv[i]<<endl;
    }
    int i=0;
    while(envp[i]!=NULL)
    {
        cout<<"第"<<i+1<<"个环境变量是:"<<envp[i]<<endl;
        i++;
    }
    return 0;
}
```

```bash
lizy@ubuntu-Z11PA-U12-Series:~/cppProject$ g++ -o demo1 demo1.cpp
lizy@ubuntu-Z11PA-U12-Series:~/cppProject$ ./demo1 a b c
传入参数数目:4
第1个参数是:./demo1
第2个参数是:a
第3个参数是:b
第4个参数是:c
第1个环境变量是:SHELL=/bin/bash
第2个环境变量是:COLORTERM=truecolor
第3个环境变量是:VSCODE_DEBUGPY_ADAPTER_ENDPOINTS=/home/lizy/.vscode-server/extensions/ms-python.debugpy-2025.18.0-linux-x64/.noConfigDebugAdapterEndpoints/endpoint-d64e1ff25f5b81f8.txt
第4个环境变量是:TERM_PROGRAM_VERSION=1.109.0
第5个环境变量是:CONDA_EXE=/home/lizy/miniconda3/bin/conda
第6个环境变量是:_CE_M=
第7个环境变量是:PYDEVD_DISABLE_FILE_VALIDATION=1
第8个环境变量是:PWD=/home/lizy/cppProject
第9个环境变量是:LOGNAME=lizy
第10个环境变量是:XDG_SESSION_TYPE=tty
第11个环境变量是:CONDA_PREFIX=/home/lizy/miniconda3
第12个环境变量是:CXX=/usr/bin/g++-12
第13个环境变量是:BUNDLED_DEBUGPY_PATH=/home/lizy/.vscode-server/extensions/ms-python.debugpy-2025.18.0-linux-x64/bundled/libs/debugpy
第14个环境变量是:VSCODE_GIT_ASKPASS_NODE=/home/lizy/.vscode-server/cli/servers/Stable-bdd88df003631aaa0bcbe057cb0a940b80a476fa/server/node
第15个环境变量是:HOME=/home/lizy
第16个环境变量是:LANG=zh_CN.UTF-8
第17个环境变量是:LS_COLORS=rs=0:di=01;34:ln=01;36:mh=00:pi=40;33:so=01;35:do=01;35:bd=40;33;01:cd=40;33;01:or=40;31;01:mi=00:su=37;41:sg=30;43:ca=00:tw=30;42:ow=34;42:st=37;44:ex=01;32:*.tar=01;31:*.tgz=01;31:*.arc=01;31:*.arj=01;31:*.taz=01;31:*.lha=01;31:*.lz4=01;31:*.lzh=01;31:*.lzma=01;31:*.tlz=01;31:*.txz=01;31:*.tzo=01;31:*.t7z=01;31:*.zip=01;31:*.z=01;31:*.dz=01;31:*.gz=01;31:*.lrz=01;31:*.lz=01;31:*.lzo=01;31:*.xz=01;31:*.zst=01;31:*.tzst=01;31:*.bz2=01;31:*.bz=01;31:*.tbz=01;31:*.tbz2=01;31:*.tz=01;31:*.deb=01;31:*.rpm=01;31:*.jar=01;31:*.war=01;31:*.ear=01;31:*.sar=01;31:*.rar=01;31:*.alz=01;31:*.ace=01;31:*.zoo=01;31:*.cpio=01;31:*.7z=01;31:*.rz=01;31:*.cab=01;31:*.wim=01;31:*.swm=01;31:*.dwm=01;31:*.esd=01;31:*.avif=01;35:*.jpg=01;35:*.jpeg=01;35:*.mjpg=01;35:*.mjpeg=01;35:*.gif=01;35:*.bmp=01;35:*.pbm=01;35:*.pgm=01;35:*.ppm=01;35:*.tga=01;35:*.xbm=01;35:*.xpm=01;35:*.tif=01;35:*.tiff=01;35:*.png=01;35:*.svg=01;35:*.svgz=01;35:*.mng=01;35:*.pcx=01;35:*.mov=01;35:*.mpg=01;35:*.mpeg=01;35:*.m2v=01;35:*.mkv=01;35:*.webm=01;35:*.webp=01;35:*.ogm=01;35:*.mp4=01;35:*.m4v=01;35:*.mp4v=01;35:*.vob=01;35:*.qt=01;35:*.nuv=01;35:*.wmv=01;35:*.asf=01;35:*.rm=01;35:*.rmvb=01;35:*.flc=01;35:*.avi=01;35:*.fli=01;35:*.flv=01;35:*.gl=01;35:*.dl=01;35:*.xcf=01;35:*.xwd=01;35:*.yuv=01;35:*.cgm=01;35:*.emf=01;35:*.ogv=01;35:*.ogx=01;35:*.aac=00;36:*.au=00;36:*.flac=00;36:*.m4a=00;36:*.mid=00;36:*.midi=00;36:*.mka=00;36:*.mp3=00;36:*.mpc=00;36:*.ogg=00;36:*.ra=00;36:*.wav=00;36:*.oga=00;36:*.opus=00;36:*.spx=00;36:*.xspf=00;36:*~=00;90:*#=00;90:*.bak=00;90:*.crdownload=00;90:*.dpkg-dist=00;90:*.dpkg-new=00;90:*.dpkg-old=00;90:*.dpkg-tmp=00;90:*.old=00;90:*.orig=00;90:*.part=00;90:*.rej=00;90:*.rpmnew=00;90:*.rpmorig=00;90:*.rpmsave=00;90:*.swp=00;90:*.tmp=00;90:*.ucf-dist=00;90:*.ucf-new=00;90:*.ucf-old=00;90:
第18个环境变量是:PYTHONSTARTUP=/home/lizy/.vscode-server/data/User/workspaceStorage/88b16e38a956df1a69e4b2550ce2cbd6/ms-python.python/pythonrc.py
第19个环境变量是:SSL_CERT_DIR=/usr/lib/ssl/certs
第20个环境变量是:CONDA_PROMPT_MODIFIER=(base) 
第21个环境变量是:GIT_ASKPASS=/home/lizy/.vscode-server/cli/servers/Stable-bdd88df003631aaa0bcbe057cb0a940b80a476fa/server/extensions/git/dist/askpass.sh
第22个环境变量是:SSH_CONNECTION=127.0.0.1 53054 127.0.0.1 2887
第23个环境变量是:CUDA_TOOLKIT_ROOT_DIR=/usr/local/cuda
第24个环境变量是:CUDAHOSTCXX=/usr/bin/g++-12
第25个环境变量是:VSCODE_GIT_ASKPASS_EXTRA_ARGS=
第26个环境变量是:VSCODE_PYTHON_AUTOACTIVATE_GUARD=1
第27个环境变量是:_CONDA_EXE=/home/lizy/miniconda3/bin/conda
第28个环境变量是:LESSCLOSE=/usr/bin/lesspipe %s %s
第29个环境变量是:_CONDA_ROOT=/home/lizy/miniconda3
第30个环境变量是:XDG_SESSION_CLASS=user
第31个环境变量是:TERM=xterm-256color
第32个环境变量是:PYTHON_BASIC_REPL=1
第33个环境变量是:_CE_CONDA=
第34个环境变量是:CPLUS_INCLUDE_PATH=/usr/local/cuda/include:/usr/local/cuda/include:
第35个环境变量是:LESSOPEN=| /usr/bin/lesspipe %s
第36个环境变量是:USER=lizy
第37个环境变量是:VSCODE_GIT_IPC_HANDLE=/run/user/1018/vscode-git-ade07bf709.sock
第38个环境变量是:CUDA_PATH=/usr/local/cuda
第39个环境变量是:CONDA_SHLVL=1
第40个环境变量是:SHLVL=1
第41个环境变量是:XDG_SESSION_ID=190645
第42个环境变量是:CONDA_PYTHON_EXE=/home/lizy/miniconda3/bin/python
第43个环境变量是:LD_LIBRARY_PATH=/usr/local/cuda/lib64:/usr/local/cuda/lib64:
第44个环境变量是:CMAKE_CUDA_FLAGS=-allow-unsupported-compiler
第45个环境变量是:XDG_RUNTIME_DIR=/run/user/1018
第46个环境变量是:SSL_CERT_FILE=/usr/lib/ssl/cert.pem
第47个环境变量是:SSH_CLIENT=127.0.0.1 53054 2887
第48个环境变量是:CONDA_DEFAULT_ENV=base
第49个环境变量是:DEBUGINFOD_URLS=https://debuginfod.ubuntu.com 
第50个环境变量是:VSCODE_GIT_ASKPASS_MAIN=/home/lizy/.vscode-server/cli/servers/Stable-bdd88df003631aaa0bcbe057cb0a940b80a476fa/server/extensions/git/dist/askpass-main.js
第51个环境变量是:CUDA_HOME=/usr/local/cuda
第52个环境变量是:XDG_DATA_DIRS=/usr/share/gnome:/usr/local/share:/usr/share:/var/lib/snapd/desktop
第53个环境变量是:BROWSER=/home/lizy/.vscode-server/cli/servers/Stable-bdd88df003631aaa0bcbe057cb0a940b80a476fa/server/bin/helpers/browser.sh
第54个环境变量是:PATH=/usr/local/cuda/bin:/home/lizy/.vscode-server/data/User/globalStorage/github.copilot-chat/debugCommand:/home/lizy/.vscode-server/data/User/globalStorage/github.copilot-chat/copilotCli:/home/lizy/.vscode-server/cli/servers/Stable-bdd88df003631aaa0bcbe057cb0a940b80a476fa/server/bin/remote-cli:/usr/local/cuda/bin:/home/lizy/miniconda3/bin:/home/lizy/miniconda3/condabin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:/home/lizy/.vscode-server/extensions/ms-python.debugpy-2025.18.0-linux-x64/bundled/scripts/noConfigScripts
第55个环境变量是:CC=/usr/bin/gcc-12
第56个环境变量是:DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1018/bus
第57个环境变量是:C_INCLUDE_PATH=/usr/local/cuda/include:/usr/local/cuda/include:
第58个环境变量是:CUDAToolkit_ROOT=/usr/local/cuda
第59个环境变量是:OLDPWD=/home/lizy
第60个环境变量是:TERM_PROGRAM=vscode
第61个环境变量是:VSCODE_IPC_HOOK_CLI=/run/user/1018/vscode-ipc-3076a989-0529-4170-af8a-7af6f1a49691.sock
第62个环境变量是:_=./demo1
```

# 操作环境变量

## 设置环境变量

```cpp
int setenv(const char *name, const char *value, int overwrite);
```

`setenv` 是一个 POSIX 标准（如 POSIX.1-2001）中定义的 C 语言库函数，用于修改或添加环境变量。它通常在 `<stdlib.h>` 头文件中声明。

`setenv` 函数将环境变量 `name` 的值设置为 `value`。如果环境变量 `name` 已存在，其行为取决于 `overwrite` 参数：

- 若 `overwrite` 非零，则覆盖已有的值。
- 若 `overwrite` 为零，则不修改已有的值（函数仍返回成功，但环境变量保持不变）。

环境变量是一组字符串，形式为 `名称=值`，它们影响进程的行为，如查找可执行文件的路径、设置语言区域等。`setenv` 允许程序在运行时动态地修改自己的环境变量，这些变更通常会传递给**该进程创建的子进程**（通过 `fork`/`exec` 继承）。

**参数详解**

- **`name`**：要设置的环境变量名称。不能包含等号 `=` 字符，否则行为未定义（某些实现可能直接返回错误）。
- **`value`**：要赋给环境变量的字符串值。可以包含任意字符，通常不包含空字符（C 字符串以 `\0` 结尾）。
- **`overwrite`**：整型标志，决定当变量已存在时的行为：
  - 非零：覆盖现有值。
  - 零：保留现有值，函数成功返回但不做任何更改。

**返回值**

- 成功时返回 **0**。
- 出错时返回 **-1**，并设置 `errno` 以指示错误类型。可能的 `errno` 值包括：
  - `ENOMEM`：内存不足，无法分配新的环境字符串。
  - `EINVAL`：`name` 为空指针，或指向的字符串为空，或包含 `=` 字符（某些实现可能检测并返回此错误）。



## 获取环境变量

```cpp
char *getenv(const char *name);
```

`getenv` 是 C 标准库（ISO C 和 POSIX）中定义的函数，用于检索当前进程环境变量的值。它在 `<stdlib.h>` 头文件中声明。

**功能描述**

`getenv` 在进程的环境变量列表中查找名为 `name` 的变量。如果找到，则返回指向对应值字符串的指针；如果未找到，则返回空指针（`NULL`）。

环境变量通常以 `名称=值` 的形式存储，例如 `PATH=/usr/bin:/bin`。`getenv` 允许程序读取这些值，以便根据运行环境调整行为（例如读取配置文件路径、调试标志等）。

**参数**

- **`name`**：以空字符结尾的字符串，表示要查询的环境变量名称。名称中不应包含等号 `=`，因为环境变量的键名本身不含等号（等号用于分隔名称和值）。如果 `name` 为空指针或空字符串，行为由实现定义（通常返回 `NULL`）。

**返回值**

- 成功：返回指向环境变量 **值** 的字符串的指针。该字符串以空字符结尾，例如，对于 `PATH=/usr/bin`，返回的指针指向 `"/usr/bin"` 部分（不包括名称和等号）。
- 失败：如果指定的环境变量不存在，返回 `NULL`。

**注意事项**

1. **返回指针的生命周期**：返回的指针指向的环境变量字符串实际存储在进程的环境空间（通常是全局的 `environ` 数组所指向的内存）中。该内存由系统管理，**不应被调用者修改**（尝试修改可能导致未定义行为，甚至破坏环境）。如果需要修改字符串，应先复制一份副本。
2. **线程安全**：在 POSIX 环境中，`getenv` 本身是线程安全的，因为它只读取环境变量。但是，如果其他线程同时调用修改环境的函数（如 `setenv`、`putenv`、`unsetenv`），则可能产生竞争条件，导致返回的指针指向的数据被改变或释放。因此，在多线程程序中，建议在访问环境变量时进行适当的同步（例如使用互斥锁），或避免在读取期间修改环境。
3. **环境变量的持久性**：`getenv` 返回的值反映的是**当前进程的环境**。如果之后调用 `setenv` 或 `putenv` 修改了同一变量，之前获取的指针可能仍然有效（如果修改是就地替换且未释放原内存），但内容可能已改变；某些实现（如 glibc）可能会重新分配内存，导致原指针指向已释放的内存，从而造成悬垂指针。因此，强烈建议**不要长期持有 `getenv` 返回的指针，而是在每次需要时重新调用 `getenv`**。
4. **名称大小写**：环境变量名称在 Unix-like 系统中是大小写敏感的（例如 `PATH` 和 `path` 是不同的变量）。但在某些系统（如 Windows）中可能不敏感，但为了可移植性，应假设大小写敏感。
5. **空值处理**：环境变量的值可以是空字符串（例如 `FOO=`），此时 `getenv` 返回指向空字符串的指针（`""`），而不是 `NULL`。调用者应能区分变量存在但值为空 和 变量不存在两种情况。

补充：`perror()`

```cpp
#include <stdio.h>  // 必须包含该头文件
void perror(const char *s);//perror 会读取全局变量 errno（定义在 <errno.h>）的值，根据该值输出对应的错误信息
```

- 参数 `s`：自定义提示字符串（可以为 `NULL`），最终输出时会和系统错误描述拼接；
- 返回值：无（`void`）



示例：

```cpp
#include <stdlib.h>
#include <stdio.h>

int main() {
    // 设置环境变量 PATH 为 /usr/bin:/bin
    if (setenv("PATH", "/usr/bin:/bin", 1) != 0) {
        perror("setenv");
        return 1;
    }

    // 尝试设置已存在的变量，但不覆盖
    if (setenv("PATH", "/dangerous/path", 0) != 0) {
        perror("setenv");
        return 1;
    }
    // 此时 PATH 仍然是 /usr/bin:/bin，因为 overwrite = 0

    // 获取并打印环境变量
    char *path = getenv("PATH");
    if (path) {
        printf("PATH = %s\n", path);
    }

    return 0;
}
```



# GDB调试程序



## GDB常用命令

> 如果希望程序可调试，编译时需要加-g选项，并且，不能使用-O的优化选项。

```bash
gdb 目标程序
```



| **命令** | **简写** | **命令说明**                                                 |
| -------- | -------- | ------------------------------------------------------------ |
| set args |          | 设置程序运行的参数。  例如：./demo 张三 西施 我是一只傻傻鸟  设置参数的方法是：  set args 张三 西施 我是一只傻傻鸟 |
| break    | b        | 设置断点，b 20 表示在第20行设置断点，可以设置多个断点。      |
| run      | r        | 开始运行程序, 程序运行到断点的位置会停下来，如果没有遇到断点，程序一直运行下去。 |
| next     | n        | 执行当前行语句，如果该语句为函数调用，不会进入函数内部。 VS的F10 |
| step     | s        | 执行当前行语句，如果该语句为函数调用，则进入函数内部。VS的F11  注意了，如果函数是库函数或第三方提供的函数，用s也是进不去的，因为没有源代码，如果是自定义的函数，只要有源码就可以进去。 |
| print    | p        | 显示变量或表达式的值，如果p后面是表达式，会执行这个表达式。  |
| continue | c        | 继续运行程序，遇到下一个断点停止，如果没有遇到断点，程序将一直运行。  VS的F5 |
| set var  |          | 设置变量的值。  假设程序中定义了两个变量：  int ii;   char name[21];  set var ii=10 把ii的值设置为10；  set var name="西施"。 |
| quit     | q        | 退出gdb。                                                    |



```bash
(base) lizy@ubuntu-Z11PA-U12-Series:~/cppProject$ gdb demo
GNU gdb (Ubuntu 15.0.50.20240403-0ubuntu1) 15.0.50.20240403-git
Copyright (C) 2024 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
Type "show copying" and "show warranty" for details.
This GDB was configured as "x86_64-linux-gnu".
Type "show configuration" for configuration details.
For bug reporting instructions, please see:
<https://www.gnu.org/software/gdb/bugs/>.
Find the GDB manual and other documentation resources online at:
    <http://www.gnu.org/software/gdb/documentation/>.

For help, type "help".
Type "apropos word" to search for commands related to "word"...
Reading symbols from demo...
(gdb) set arg me you 520
(gdb) show arg
Argument list to give program being debugged when it is started is "me you 520".
(gdb) b 17
Breakpoint 1 at 0x1291: demo1.cpp:17. (3 locations)
(gdb) i b
Num     Type           Disp Enb Address            What
1       breakpoint     keep y   <MULTIPLE>         
1.1                         y   0x0000000000001291 in main(int, char**, char**) at demo1.cpp:38
1.2                         y   0x00000000000012a5 in __static_initialization_and_destruction_0(int, int) at demo1.cpp:38
1.3                         y   0x00000000000012e8 in _GLOBAL__sub_I_main() at demo1.cpp:38
(gdb) b 4
Breakpoint 2 at 0x11c0: file demo1.cpp, line 6.
(gdb) d 1
(gdb) i b
Num     Type           Disp Enb Address            What
2       breakpoint     keep y   0x00000000000011c0 in main(int, char**, char**) at demo1.cpp:6
(gdb) r
Starting program: /home/lizy/cppProject/demo me you 520

This GDB supports auto-downloading debuginfo from the following URLs:
  <https://debuginfod.ubuntu.com>
Enable debuginfod for this session? (y or [n]) y
Debuginfod has been enabled.
To make this setting permanent, add 'set debuginfod enabled on' to .gdbinit.
Downloading separate debug info for system-supplied DSO at 0x7ffff7fc3000
Downloading separate debug info for /lib/x86_64-linux-gnu/libstdc++.so.6                                                                                           
[Thread debugging using libthread_db enabled]                                                                                                                      
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".
Downloading separate debug info for /lib/x86_64-linux-gnu/libgcc_s.so.1
                                                                                                                                                                   
Breakpoint 2, main (argc=4, argv=0x7fffffffd828, envp=0x7fffffffd850) at demo1.cpp:6
warning: Source file is more recent than executable.
6         if (argc!=4)
(gdb) next
12        cout << argv[1] << "开始向" << argv[2] << "表白。\n";
(gdb) n
me开始向you表白。
13        cout << argv[3] << endl;
(gdb) n
520
14        cout << argv[1] << "表白完成。\n";
(gdb) b 15
Breakpoint 3 at 0x55555555528c: file demo1.cpp, line 16.
(gdb) c
Continuing.
me表白完成。

Breakpoint 3, main (argc=4, argv=0x7fffffffd828, envp=0x7fffffffd850) at demo1.cpp:16
16        return 0;
(gdb) p argv
$1 = (char **) 0x7fffffffd828
(gdb) p argv[0]
$2 = 0x7fffffffdbe3 "/home/lizy/cppProject/demo"
(gdb) q
A debugging session is active.

        Inferior 1 [process 2931696] will be killed.

Quit anyway? (y or n) y
```

**改变变量的值:**

- p命令执行表达式
- set var命令

## 知识拾遗——core文件

在 Linux 系统中，**core 文件**（又称核心转储文件）是当进程异常终止（例如发生段错误、非法指令等）时，操作系统将该进程的内存映像（包括堆栈、寄存器、程序计数器等信息）保存到磁盘上的一个文件。它本质上是进程在崩溃瞬间的“快照”，主要用于事后调试，帮助开发者定位程序崩溃的原因。

###  生成条件

core 文件并不是每次程序崩溃都会生成，需要满足以下条件：

- **资源限制允许**：shell 或系统对 core 文件大小有限制。使用 `ulimit -c` 查看，若结果为 0 则不生成。可以通过 `ulimit -c unlimited` 解除限制（仅在当前 shell 有效）。
- **信号未被捕获或忽略**：导致进程终止的信号（如 SIGSEGV、SIGABRT 等）没有被程序自己捕获处理，或者处理函数没有阻止 core dump。
- **文件系统可写**：进程的工作目录（或指定的 core 存放目录）有写权限，且磁盘空间充足。
- **设置了适当的 core 模式**：通过 `/proc/sys/kernel/core_pattern` 可以控制 core 文件的命名和存放路径。

### 命名与位置

传统上，core 文件生成在进程的工作目录下，文件名为 `core`。但现代 Linux 系统通过 `/proc/sys/kernel/core_pattern` 进行灵活配置：

- 默认可能为 `core` 或 `core.%p`（%p 表示 PID）。
- 可以设置为包含更多信息的格式，如 `core.%e.%p.%t`（可执行文件名、PID、时间戳）。
- 也可以指定绝对路径，例如 `/var/crash/core.%e.%p`。

相关文件 `/proc/sys/kernel/core_uses_pid` 若为 1，则总是在 core 文件名后附加 PID。

### 作用与分析方法

core 文件的主要用途是**事后调试**。配合可执行程序和调试信息（编译时加 `-g` 选项），可以使用 GDB 加载 core 文件来重现崩溃现场：

bash

```
gdb ./a.out core
(gdb) bt          # 查看崩溃时的函数调用栈
(gdb) info locals # 查看局部变量
(gdb) frame 2     # 切换到指定栈帧
```



通过分析堆栈和变量值，开发者可以快速定位导致崩溃的代码行。

###  配置与管理

- **查看当前限制**：`ulimit -a` 或 `ulimit -c`
- **临时设置 unlimited**：`ulimit -c unlimited`
- **永久设置**：编辑 `/etc/security/limits.conf`，添加 `* soft core unlimited`
- **修改 core 模式**：`echo "/tmp/core.%e.%p" > /proc/sys/kernel/core_pattern`（需要 root）
- **禁用 core 生成**：`ulimit -c 0` 或设置 `core_pattern` 为 `/dev/null`

###  注意事项

- core 文件可能包含敏感数据（密码、密钥等），调试完毕后应及时删除。
- 生产环境通常限制或禁用 core 生成，以免磁盘被写满或泄露信息。
- 对于守护进程，可能需要修改其工作目录或 core 模式，确保有权限写入。
- 使用 `file` 命令可以查看 core 文件的基本信息（如所属程序、架构等）。

### 与其他系统的对比

Windows 上的类似机制是“用户转储文件”（.dmp），可以通过 WinDbg 等工具分析。macOS 也支持 core 文件，行为与 Linux 类似。

总之，core 文件是 Linux 下不可或缺的调试利器，合理配置和使用它可以极大地提高问题排查效率。



## GDB调试内核文件

如果程序在运行的过程中发生了内存泄漏，会被内核强行终止，提示“段错误（吐核）”，内存的状态将保存在core文件中，方便程序员进一步分析。

**Linux缺省不会生成core文件，需要修改系统参数。**

调试core文件的步骤如下：

1. 用ulimit -a查看当前用户的资源限制参数；
2. 用ulimit -c unlimited把core file size改为unlimited；
3. 运行程序，产生core文件；
4. 运行gdb 程序名 core文件名；
5. 在gdb中，用`bt`查看函数调用栈



```bash
lizy@ubuntu-Z11PA-U12-Series:~/cppProject$ ulimit -a
real-time non-blocking time  (microseconds, -R) unlimited
core file size              (blocks, -c) 0
data seg size               (kbytes, -d) unlimited
scheduling priority                 (-e) 0
file size                   (blocks, -f) unlimited
pending signals                     (-i) 255057
max locked memory           (kbytes, -l) 8179340
max memory size             (kbytes, -m) unlimited
open files                          (-n) 1048576
pipe size                (512 bytes, -p) 8
POSIX message queues         (bytes, -q) 819200
real-time priority                  (-r) 0
stack size                  (kbytes, -s) 8192
cpu time                   (seconds, -t) unlimited
max user processes                  (-u) 255057
virtual memory              (kbytes, -v) unlimited
file locks                          (-x) unlimited
lizy@ubuntu-Z11PA-U12-Series:~/cppProject$ ulimit -c unlimited
lizy@ubuntu-Z11PA-U12-Series:~/cppProject$ g++ -g -o demo demo1.cpp
lizy@ubuntu-Z11PA-U12-Series:~/cppProject$ ./demo
段错误 (核心已转储)
```

由于乌班图的额外设置,导致无法复现对内核文件的操作







## GDB调试正在运行中的程序

```bash
gdb 程序名 -p 进程编号
```

使用ps命令查看进程编号

使用gdb进行调试正在运行的程序时,程序会暂时停止运行

# Linux时间操作

> UNIX操作系统根据计算机产生的年代把1970年1月1日作为UNIX的纪元时间，1970年1月1日是时间的中间点，将从1970年1月1日起经过的秒数用一个整数存放。

## time_t

`time_t`用于表示时间类型，它是一个`long`类型的别名，在`<time.h>`文件中定义，表示从1970年1月1日0时0分0秒到现在的秒数。

```cpp
typedef long time_t;
```



## time()库函数

> time()库函数用于获取操作系统的当前时间。

`time()` 是 C 标准库中用于获取当前日历时间的函数，定义在 `<time.h>` 头文件中。

```c
time_t time(time_t *tloc);
```

**功能**

返回从 **1970-01-01 00:00:00 UTC**（称为 Unix 纪元）到当前时刻所经过的秒数，即 Unix 时间戳。

**参数**

- `tloc`：如果非 `NULL`，函数会将返回值也存储到 `tloc` 指向的 `time_t` 变量中。

**返回值**

- 成功：返回当前时间戳（`time_t` 类型，通常是整数）。
- 失败：返回 `(time_t)-1`。

**注意事项**

- `time_t` 通常实现为 32 位或 64 位有符号整数。32 位的 `time_t` 在 **2038 年 1 月 19 日**会溢出，这是著名的“2038 年问题”。现代系统逐渐采用 64 位 `time_t` 以避免该问题。
- 得到时间戳后，常配合 `localtime()`、`gmtime()` 将其转换为可读的日期时间结构 `struct tm`，或使用 `ctime()` 直接生成字符串。

`time()` 是最基础的时间函数，许多其他时间操作（如定时、日志、随机数种子等）都依赖它。

```cpp
//有两种调用方法：

time_t now=time(0);       // 将空地址传递给time()函数，并将time()返回值赋给变量now。

//或

time_t now; time(&now);  // 将变量now的地址作为参数传递给time()函数。
```



## tm结构体

`tm` 结构体是 C 语言中用于表示分解时间（broken-down time）的标准结构，定义在 `<time.h>` 头文件中。它将一个时间戳（`time_t`）拆解成年、月、日、时、分、秒等便于人类理解和操作的字段。

```cpp
struct tm {
    int tm_sec;    // 秒 – 取值范围 [0, 60]（60 表示闰秒，实际很少用）
    int tm_min;    // 分 – [0, 59]
    int tm_hour;   // 时 – [0, 23]
    int tm_mday;   // 一个月中的第几天 – [1, 31]
    int tm_mon;    // 月份（从一月开始，0 表示一月） – [0, 11]
    int tm_year;   // 年份（自 1900 年起的年数）
    int tm_wday;   // 一周中的第几天（从周日开始，0 表示周日） – [0, 6]
    int tm_yday;   // 一年中的第几天（从 1 月 1 日开始，0 表示 1 月 1 日） – [0, 365]
    int tm_isdst;  // 夏令时标志,很少使用
};
```

**成员详细说明**

| 成员     | 含义                     | 取值范围/说明                                                |
| :------- | :----------------------- | :----------------------------------------------------------- |
| tm_sec   | 秒                       | 0~60（60 为闰秒，通常只用 0~59）                             |
| tm_min   | 分钟                     | 0~59                                                         |
| tm_hour  | 小时                     | 0~23                                                         |
| tm_mday  | 月份中的日期             | 1~31                                                         |
| tm_mon   | 月份（从 0 开始）        | 0 表示一月，11 表示十二月                                    |
| tm_year  | 年份（从 1900 开始计数） | 例如 2024 年表示为 124（因为 2024-1900 = 124）               |
| tm_wday  | 星期几（从周日开始）     | 0 周日，1 周一，…，6 周六                                    |
| tm_yday  | 一年中的第几天           | 0 表示 1 月 1 日，365 表示 12 月 31 日（闰年可能为 366）     |
| tm_isdst | 夏令时标志               | 正数表示夏令时生效；0 表示非夏令时；负数表示信息不可用（由系统自动判断） |

## `tm`结构体与 `time_t` 的相互转换

### `time_t` → `struct tm`

有两个常用函数：

- **`localtime(const time_t  *timep)`**
  将 `time_t` 时间戳转换为 **本地时区** 的 `tm` 结构。返回指向静态内部缓冲区的**指针**（不可重入），可重入版本为 `localtime_r()`。
- **`gmtime(const time_t  *timep)`**
  将 `time_t` 转换为 **UTC（协调世界时）** 的 `tm` 结构。

```cpp
#include<iostream>
#include<ctime>
using namespace std;

int main()
{
	time_t now = time(0);
	cout<<"Now time is :"<<now<<endl;
    
	//t_time --> tm
	struct tm* s_now=localtime(&now);
	cout<<"Now time is :"<<endl;
	cout<<s_now->tm_year+1900<<"year"<<endl;
	cout<<s_now->tm_mon+1<<"month"<<endl;
	cout<<s_now->tm_mday<<"day"<<endl;
	cout<<s_now->tm_hour<<"hour"<<endl;
	cout<<s_now->tm_min<<"minute"<<endl;
	cout<<s_now->tm_sec<<"second"<<endl;
	cout<<s_now->tm_wday<<"wenkend"<<endl;
	return 0;
}
```



### `struct tm` → `time_t`

使用 **`mktime(struct tm *tm)`** 函数。它将一个本地时间表示的 `tm` 结构转换为 `time_t` 时间戳，返回值为tm结构体同时会**规范化** `tm` 结构（自动调整溢出字段，并填充 `tm_wday` 和 `tm_yday`）。

**示例**：构建一个指定日期，获取时间戳

```cpp
#include <stdio.h>
#include <time.h>

int main() {
    struct tm t = {0};
    t.tm_year = 2024 - 1900;   // 2024 年
    t.tm_mon  = 1 - 1;          // 一月
    t.tm_mday = 20;             // 20 日
    t.tm_hour = 10;             // 10 时
    t.tm_min  = 30;             // 30 分
    t.tm_sec  = 0;              // 0 秒
    t.tm_isdst = -1;            // 让系统判断夏令时

    time_t ts = mktime(&t);
    if (ts == -1) {
        perror("mktime");
        return 1;
    }

    printf("时间戳: %ld\n", ts);
    printf("对应日期: %s", ctime(&ts));
    return 0;
}
```



**注意**：

- `mktime` 假设输入的 `tm` 是**本地时间**，而不是 UTC。
- 如果要将 UTC 时间转为时间戳，可以先用 `timegm()`（非标准，但许多系统提供）或自行转换（如设置 TZ 环境变量为 UTC）。



该函数主要用于**时间的运算**，例如：把2022-03-01 00:00:25加30分钟。

思路：

1. 解析字符串格式的时间，转换成tm结构体；
2. 用`mktime()`把`tm结构体`转换成`time_t`时间；
3. 把`time_t`时间加30*60秒；
4. 用`localtime_r()`把`time_t`时间转换成`tm结构体`；
5. 把`tm结构体`转换成字符串





## gettimeofday()库函数

`gettimeofday()` 是一个 POSIX 标准函数，用于获取当前时间，精度达到**微秒（µs）**级别。它比 C 标准库的 `time()` 函数（精度秒）更精细，常用于需要测量短时间间隔或记录高精度时间戳的场景。

```cpp
#include <sys/time.h>

int gettimeofday(struct timeval *tv, struct timezone *tz);
```

**参数**

- **`tv`**：指向 `struct timeval` 结构的指针，用于接收当前时间（从 1970-01-01 00:00:00 UTC 至今的秒数和微秒数）。不能为 `NULL`。
- **`tz`**：指向 `struct timezone` 结构的指针，用于获取时区信息。**该参数已废弃**，在 Linux 中应始终设为 `NULL` 以保证可移植性。如果传入非空指针，行为取决于系统，但通常返回的时区信息不可靠。

**返回值**

- 成功返回 **0**。
- 失败返回 **-1**，并设置 `errno` 以指示错误（常见错误如 `EFAULT` 表示指针无效）。



### `struct timeval`

```c
struct timeval {
    time_t      tv_sec;   /* 秒（自纪元起） */
    suseconds_t tv_usec;  /* 微秒（0～999999） */
};
```

- `tv_sec` 与 `time()` 返回值含义相同。
- `tv_usec` 表示微秒部分，与 `tv_sec` 共同组成一个完整的当前时间戳。

### `struct timezone`（已废弃）

```c
struct timezone {
    int tz_minuteswest; /* 比 UTC 向西的分钟数 */
    int tz_dsttime;     /* 夏令时类型 */
};
```

在现代 Linux 系统中，`gettimeofday` 忽略该参数，直接返回而不填充任何有用信息。因此**总是传递 `NULL`**。

------

**示例:测量过程时间**

```cpp
#include <iostream>
#include <sys/time.h>  // gettimeofday()需要的头文件。
using namespace std;

int main()
{
  timeval start,end;

  gettimeofday(&start, 0 ); // 计时开始。

  for (int ii=0;ii<1000000000;ii++);

  gettimeofday(&end, 0 );   // 计时结束。

  // 计算消耗的时长。
  timeval tv;
  tv.tv_usec=end.tv_usec-start.tv_usec;
  tv.tv_sec=end.tv_sec-start.tv_sec;
  if (tv.tv_usec<0)
  {
    tv.tv_usec=1000000-tv.tv_usec;
    tv.tv_sec--;
  }

  cout << "耗时：" << tv.tv_sec << "秒和" << tv.tv_usec << "微秒。\n";
}
```



------

### 精度与特性

- **微秒精度**：`tv_usec` 提供微秒级分辨率，但实际精度受硬件和内核定时器限制（通常可达几十微秒到几毫秒）。
- **系统时间影响**：返回的是**挂钟时间（wall-clock time）**，即系统当前时间。如果系统时间被管理员或 NTP 调整，两次调用 `gettimeofday` 得到的差值可能包含跳跃，不适合测量短时段间隔（除非使用单调时钟）。
- **线程安全**：`gettimeofday` 将结果写入用户提供的缓冲区，不维护内部静态数据，因此是**可重入**且线程安全的。但若多个线程同时读取，可能看到不同的系统时间（取决于内核调度）。

------

### 注意事项与局限

1. **时区参数必须为 NULL**：为保持可移植性，永远传递 `tz = NULL`。
2. **微秒含义**：`tv_usec` 是秒内的小数部分，范围 0~999999，不能单独解释为从纪元开始的微秒数。
3. **系统时间可变**：时间可能因 NTP 同步或管理员手动设置而发生跳跃。若需要稳定递增的时间间隔，应使用 **`clock_gettime(CLOCK_MONOTONIC, ...)`**。
4. **2038 年问题**：`tv_sec` 是 `time_t` 类型，若为 32 位，将在 2038 年溢出。现代系统已逐渐迁移到 64 位 `time_t`。
5. **POSIX 要求 vs 实际支持**：`gettimeofday` 在 SUSv2 中标记为“历史遗留”，POSIX.1-2008 已将其废弃，推荐使用 `clock_gettime`。

------

## 现代替代方案：`clock_gettime`

`clock_gettime` 是 POSIX.1-2001 引入的更强大的时间获取函数，支持多种时钟源：

```c
#include <time.h>

int clock_gettime(clockid_t clk_id, struct timespec *tp);
```

- `struct timespec` 包含 `tv_sec`（秒）和 `tv_nsec`（纳秒），精度更高。
- 常用时钟 ID：
  - **`CLOCK_REALTIME`**：系统实时时间（同 `gettimeofday`，但纳秒级）。
  - **`CLOCK_MONOTONIC`**：单调时间，不受系统时间跳变影响，适合测量间隔。
  - **`CLOCK_PROCESS_CPUTIME_ID`**：进程 CPU 时间。
  - **`CLOCK_THREAD_CPUTIME_ID`**：线程 CPU 时间。

```c
struct timespec ts;
clock_gettime(CLOCK_REALTIME, &ts);
printf("秒: %ld, 纳秒: %ld\n", ts.tv_sec, ts.tv_nsec);
```

因此，在新代码中推荐使用 `clock_gettime`，它更灵活且避免了 `gettimeofday` 的废弃问题。

------

**总结**

- `gettimeofday` 是获取微秒级挂钟时间的传统 POSIX 函数。
- 使用时将 `tz` 参数置 `NULL`，并注意其时间可能跳跃。
- 对于需要稳定递增的时间测量，请改用 `clock_gettime(CLOCK_MONOTONIC, ...)`。
- 尽管已被标记为废弃，但由于历史兼容性，它在许多代码库中仍然广泛存在。理解其用法有助于阅读和维护现有代码。



## 补充

> “不可重入”（Non-reentrant）是编程中的一个重要概念，通常用来描述**函数或代码段在并发执行时是否安全**。如果一个函数被设计成“不可重入”，那么当它在执行过程中被再次调用（例如在多线程环境、信号处理程序或递归调用中），就可能导致数据错乱、程序崩溃或其他不可预期的行为。也可以被叫做线程安全

### 为什么会不可重入？

函数不可重入的根本原因是它**使用了共享资源且没有妥善保护**。常见的罪魁祸首有：

1. **静态或全局变量**
   函数内部使用了静态（`static`）变量或全局变量，这些变量在内存中只有一份副本。如果第一次调用正在修改该变量，第二次调用突然闯入，也会去读写同一个变量，就会造成数据竞争和状态混乱。
2. **返回指向内部静态缓冲区的指针**
   典型例子：`localtime()`、`ctime()`、`gethostbyname()` 等旧版 C 库函数。它们将结果存储在一个内部的静态缓冲区中，然后返回该缓冲区的地址。如果两次调用之间没有同步，第二次调用就会覆盖第一次的结果，导致第一次获取的数据损坏。
3. **使用了不可重入的库函数**
   如果一个函数内部调用了其他不可重入的函数，那它自己也变成不可重入的。
4. **缺乏锁机制**
   即使使用了全局变量，如果能用互斥锁保护，也可以实现“线程安全”，但这通常不叫“可重入”，而是“线程安全”。可重入要求函数**即使在执行过程中被中断并重新进入，也能正确运行**，这对锁的要求更高（例如不能使用会导致死锁的锁）。

------

### 可重入函数的特点

一个可重入函数通常具备以下特征：

- 只使用局部变量（存储在栈上，每个调用都有独立副本）。
- 不依赖静态或全局数据。
- 如果必须访问全局数据，会用原子操作或禁止中断的方式保证完整性，或者由调用者提供缓冲区（例如 `localtime_r` 要求传入 `struct tm *` 指针）。
- 不调用任何不可重入的函数。

------

### 具体例子：`localtime` 与 `localtime_r`

C 标准库中，`localtime(const time_t *timep)` 是一个典型的**不可重入**函数。它内部使用了一个静态的 `struct tm` 对象，每次调用都会把结果填充到这个静态对象中，并返回它的地址。

```cpp
#include <time.h>
#include <stdio.h>
#include <pthread.h>

void* thread_func(void* arg) {
    time_t t = time(NULL);
    struct tm* info = localtime(&t);  // 可能被其他线程覆盖
    printf("Thread: %s", asctime(info));
    return NULL;
}
```



如果两个线程同时执行这段代码，`info` 指向的静态缓冲区可能被另一个线程的 `localtime` 调用篡改，导致打印出混乱的结果。

为了解决这个问题，POSIX 标准提供了可重入版本 **`localtime_r`**：

```
struct tm *localtime_r(const time_t *timep, struct tm *result);
```

它要求调用者自己分配一个 `struct tm` 变量（通常是在栈上），并将指针传入。函数将结果写入这个外部提供的缓冲区，从而避免了内部静态数据的冲突。这样即使多个线程同时调用，只要每个线程使用自己的 `result` 缓冲区，就不会互相干扰。

```cpp
void* thread_func(void* arg) {
    time_t t = time(NULL);
    struct tm result;          // 每个线程私有的缓冲区
    localtime_r(&t, &result);  // 安全
    // ... 使用 result ...
    return NULL;
}
```



------

### 何时需要关注可重入性？

- **多线程编程**：多个线程可能同时调用同一个函数。可重入函数可以在不加锁的情况下安全使用，而不可重入函数则需要外部加锁保护。
- **信号处理程序**：信号处理程序可能在主程序的任何地方异步执行。在信号处理程序中调用不可重入函数（如 `printf`、`malloc`、`localtime`）非常危险，因为它们可能修改主程序正在使用的数据，导致程序崩溃。所以信号处理程序只能调用异步信号安全的函数（即可重入函数）。
- **递归调用**：如果一个函数在递归调用中依赖于静态数据，也可能出问题。

------

| 特性                     | 线程安全                                     | 可重入                                       |
| :----------------------- | :------------------------------------------- | :------------------------------------------- |
| **关注点**               | 多个线程同时执行                             | 单个线程被中断后重新执行                     |
| **数据依赖**             | 可以使用全局/静态数据，但需用锁保护          | 不能使用任何共享的可变数据（包括全局、静态） |
| **锁的使用**             | 允许，但需小心死锁                           | 禁止使用锁（因可能导致死锁）                 |
| **异步信号安全**         | 不一定                                       | 通常是异步信号安全的前提                     |
| **举例**                 | `printf`（线程安全，因内部有锁）             | `strtok_r`、`localtime_r`                    |
| **可重入必然线程安全？** | 可重入函数一定是线程安全的（因为不共享状态） | 线程安全函数不一定是可重入的（如 `printf`）  |

### 总结

- **不可重入**：函数不能安全地并发执行，通常因为使用了共享静态数据。
- **可重入**：函数可以被多个执行流同时调用，且不依赖外部同步机制也能保证正确性。
- 实际开发中，优先使用函数的可重入版本（如 `localtime_r` 替代 `localtime`，`strtok_r` 替代 `strtok` 等），或在调用不可重入函数时加锁保护。

## 程序睡眠

`sleep()` 和 `usleep()` 是 Unix/Linux 系统中常用的让程序（或线程）暂停执行一段时间的函数。它们都定义在 `<unistd.h>` 头文件中，但在精度、行为和标准化程度上有所不同。

### `sleep()` 函数

```c
#include <unistd.h>
unsigned int sleep(unsigned int seconds);
```

使调用进程（或线程）挂起至少 `seconds` 秒，直到：

- 指定的时间过去；
- 或者被一个信号中断（且信号处理函数返回）。

**返回值**

- 如果休眠了完整的 `seconds` 秒，返回 **0**。
- 如果被信号提前唤醒，返回 **剩余未休眠的秒数**（请求时间减去实际已休眠时间）。

**tips:**

- **精度**：秒级，实际休眠时间可能因系统调度略长于请求值。
- **信号影响**：`sleep()` 是可中断的，如果进程在休眠期间收到信号，`sleep()` 会提前返回，并返回剩余秒数。这为处理异步事件提供了可能，但也意味着不能保证精确的定时。
- **线程安全**：在 POSIX 系统中，`sleep()` 是线程安全的，但多线程程序中通常不建议使用，因为它会使整个线程挂起（而非进程），不过 `sleep()` 只会影响调用它的线程。
- **可移植性**：`sleep()` 是 POSIX.1 标准的一部分，几乎所有 Unix-like 系统都支持。



### `usleep()` 函数

```c
#include <unistd.h>
int usleep(useconds_t usec);
```

使调用进程（或线程）挂起至少 `usec` 微秒（1 微秒 = 1/1,000,000 秒）。

**参数**

- `usec`：要休眠的微秒数，类型 `useconds_t` 在 Linux 上通常是 `unsigned int`。

**返回值**

- 成功返回 **0**。
- 失败返回 **-1**，并设置 `errno` 指示错误（例如 `EINTR` 表示被信号中断，`EINVAL` 表示参数无效）。

```c
#include <stdio.h>
#include <unistd.h>

int main() {
    printf("开始休眠 500000 微秒（0.5 秒）...\n");
    if (usleep(500000) == 0) {
        printf("休眠完成\n");
    } else {
        perror("usleep");
    }
    return 0;
}
```

**特点与注意事项**

- **精度**：微秒级，但实际精度受内核定时器限制（通常为几十微秒到几毫秒）。
- **信号影响**：`usleep()` 也可能被信号中断，此时返回 -1 并设置 `errno = EINTR`。
- **已废弃**：`usleep()` 在 **POSIX.1-2001** 中仍被支持，但在 **POSIX.1-2008** 中被标记为废弃，并从规范中移除。原因包括：
  - 历史实现中对 `usec` 的值有限制（如某些系统要求 `usec < 1,000,000`，即不能超过 1 秒）。
  - 与 `nanosleep()` 相比，功能重叠但精度更低，且缺乏对纳秒和高精度时钟的支持。
- **线程安全**：通常是线程安全的，但依赖于实现。
- **可移植性**：尽管被废弃，许多 Linux 系统仍然提供该函数以兼容旧代码。但新代码不应再使用它。

# Linux目录、文件操作

## 获取当前目录

```c
#include <unistd.h>
char *getcwd(char *buf, size_t size);
```

- **功能**：将当前工作目录的绝对路径名存入 `buf` 中。
- **参数**：
  - `buf`：存放路径的缓冲区，若为 `NULL`，函数会使用 `malloc` 分配足够空间（需自行 `free`）。
  - `size`：缓冲区大小。
- **返回值**：成功返回 `buf`；失败返回 `NULL`。

---------



```c
#define _GNU_SOURCE          // 必须定义此特性测试宏
#include <unistd.h>

char *get_current_dir_name(void);
```

- **特性测试宏**：由于该函数是 GNU 扩展，在包含头文件前需要定义 `_GNU_SOURCE`，否则函数可能不可见。

返回当前进程的**当前工作目录**的**绝对路径名**。它内部通过 `getcwd()` 实现，但无需调用者提供缓冲区，函数会使用 `malloc(3)` 动态分配足够大的缓冲区来存储路径。

**返回值**

- **成功**：返回一个指向以 null 结尾的字符串的指针，该字符串包含当前目录的绝对路径。该内存是通过 `malloc` 分配的，因此**必须由调用者使用 `free(3)` 释放**。
- **失败**：返回 `NULL`，并设置 `errno` 以指示错误。

可能发生的错误（通过 `errno`）与 `getcwd()` 类似，例如：

- `EACCES`：搜索权限不足
- `ENOMEM`：内存不足
- `ERANGE`：路径长度超过内核支持的最大值（但此函数自动分配，通常不会出现，除非底层 `getcwd` 报告该错误）



```cpp
#include <iostream>
#include <unistd.h>
#include<cstdio>
using namespace std;

int main()
{
  char path1[256];//linux目录最大长度是256
  getcwd(path1,256);
  cout<<path1<<endl;
  
  char* path2;
  path2 = get_current_dir_name();
  printf("%s\n",path2);
  free(path2);//一定要释放内存
  return 0;
}
```



## 切换工作目录

```c
#include <unistd.h>
int chdir(const char *path);
```

**返回值：**

- 0  成功
- 其它   失败（目录不存在或没有权限）。

```cpp
#include <iostream>
#include <unistd.h>
#include<cstdio>
using namespace std;
int main()
{
  char path1[256];
  getcwd(path1,256);
  cout<<path1<<endl;
  
  int res = chdir("/mnt/c");
  getcwd(path1,256);
  if(res!=0) cout<<"erro!"<<endl;
  else cout<<path1<<endl;
  return 0;
}

```



## 创建目录

```cpp
int mkdir(const char *pathname, mode_t mode);
```

**参数**：

- `pathname`：要创建的目录路径。
- `mode`：新目录的权限（如 `0755`），受 `umask` 影响。一定是4位数
  - 写 `0755` 是因为 C 语言要求八进制常量以 `0` 开头，实际有效权限是 `755`。
  - 如果确实需要设置特殊权限，可以使用四位完整数字（如 `4755`）。

- 在 Linux 权限体系中，权限确实可以用**四位八进制数**完整描述：
  - **第一位**：特殊权限位（setuid、setgid、sticky bit）
  - **后三位**：标准权限位（所有者、组、其他）

**返回值**：

- 成功返回 0
- 失败返回 -1

**注意**：父目录必须存在且进程有写权限。

```cpp
#include <sys/stat.h>
#include <unistd.h>
#include <iostream>
using namespace std;

int main()
{
  char path1[256];
  getcwd(path1,256);
  cout<<path1<<endl;
  //创建目录
  int res = mkdir("./pro",0755);
  if(res!=0) cout<<"error!"<<endl;
  return 0;
}
```

## 删除目录

```cpp
#include <unistd.h>
int rmdir(const char *path);
```

**功能**：删除一个**空目录**。

**返回值**：

- 成功返回 0
- 失败返回 -1

**注意**：目录必须为空（仅包含 `.` 和 `..` 不算空），否则会失败。



## 获取目录中的内容

文件存放在目录中，在处理文件之前，必须先知道目录中有哪些文件，所以要获取目录中文件的列表。

**步骤:**

1. 打开目录
2. 读取目录
3. 关闭目录

### 打开目录

```c
#include <sys/types.h>
#include <dirent.h>

DIR *opendir(const char *name);
```

- **功能**：打开一个目录，返回指向目录流的指针（`DIR *`）。
- **参数**：`name` 是要打开的目录路径。
- **返回值**：成功返回目录流指针；失败返回 `NULL`，并设置 `errno`。



### 读取目录

```c
#include <dirent.h>
struct dirent *readdir(DIR *dirp);
```

- **功能**：从目录流 `dirp` 中读取下一个目录项，返回指向 `struct dirent` 结构的指针。

- **返回值**：成功返回下一个目录项的信息；到达目录末尾或出错返回 `NULL`（需要通过 `errno` 区分）。

- **struct dirent** 至少包含以下成员（因系统而异，POSIX 标准定义）：

  - `ino_t d_ino` – 文件的 inode 号

  - `char d_name[]` – 文件名（以 null 结尾）

  - `unsigned char d_type` – 文件类型（Linux 支持），常见值：

    - `DT_REG` 普通文件  8
    - `DT_DIR` 目录  4
    - `DT_LNK` 符号链接
    - `DT_UNKNOWN` 未知（需要使用 `stat` 进一步判断）

  - ```c
    struct dirent
    {
       long d_ino;                    			// inode number 索引节点号。
       off_t d_off;                   			// offset to this dirent 在目录文件中的偏移。
       unsigned short d_reclen;     		// length of this d_name 文件名长度。
       unsigned char d_type;         		// the type of d_name 文件类型。
       char d_name [NAME_MAX+1];    // file name文件名，最长255字符。
    };
    ```

    

### 关闭目录

```c
#include <dirent.h>

int closedir(DIR *dirp);
```

- **功能**：关闭目录流，释放资源。
- **返回值**：成功返回 0；失败返回 -1。





### 示例:读取目录的内容

```cpp
#include <sys/stat.h>
#include <dirent.h>
#include <iostream>
using namespace std;

int main(int argc,char* argv[])
{
 if(argc!=2) 
 {
 	cout<<"para's count is error"<<endl;
 	return -1;
 }
  DIR* dir;//定义目录指针
	   //打开目录
   if((dir=opendir(argv[1]))==NULL) return -1;
   //用于存放读取的目录内容
   struct dirent* stdinfo = NULL;
   while(1)
   {
    //读取目录
   	if((stdinfo=readdir(dir))==NULL)break;
   	cout<<"file name is:"<<stdinfo->d_name<<endl;
    cout<<"file type is:"<<(int)stdinfo->d_type<<endl;
   }
    //关闭目录指针
   closedir(dir);
  return 0;
}

```



## 补充

### `DIR` 的本质

`DIR` 是 C 语言中用于目录操作的一个数据类型，定义在头文件 `<dirent.h>` 中。它代表一个**目录流**，类似于文件操作中的 `FILE` 类型。通过 `DIR`，程序可以打开一个目录，然后逐个读取其中的目录项（包括文件和子目录）。

- **不透明数据类型**：`DIR` 是一个结构体类型，但其内部成员对程序员不可见（即不透明）。这种设计强制程序员只能通过标准库函数来操作目录流，而不能直接访问或修改其内部字段，保证了封装性和可移植性。
- **目录流**：打开一个目录后，系统会建立一个目录流，记录当前读取位置等信息。`DIR *` 指针指向这个流。
- **类比 `FILE`**：类似于 `FILE` 用于文件操作，`DIR` 用于目录操作。但目录流只能用于读取目录项列表，不能像文件那样写入数据（目录的创建、删除等操作使用其他函数如 `mkdir`、`rmdir`）。



### umask

> `umask`（用户文件创建掩码，User File Creation Mask）是 Unix 和 Linux 系统中一个非常重要的概念，它决定了新创建的文件和目录的**默认权限**。umask 是一个**进程属性**，它指定了在创建新文件或目录时，哪些权限位应该被**自动关闭**（即从默认权限中移除）。
>
> 每个进程（包括 shell）都有自己的 umask 值，通常由父进程继承。当你登录系统时，shell 会从一个系统配置文件（如 `/etc/profile` 或 `~/.bashrc`）中获取默认的 umask 设置。

umask 的值通常用**八进制数**表示，每一位对应一类用户（所有者、组、其他）的权限。umask 中为 1 的位表示**要禁止的权限**，为 0 的位表示**保留的权限**。

**最终权限计算公式**：
```
实际权限 = 默认基础权限 & (~umask)
默认基础权限:文件-666（rw-rw-rw-）目录-777(rwxrwxrwx)
```
其中 `&` 是按位与，`~` 是按位取反。

### 示例
假设 umask = **022**（八进制），二进制表示为 `000 010 010`：
- 所有者：0 → 不移除任何权限（保留所有权限）。
- 组：2 → 移除写权限（`rwx` 中的 `w` 被移除）。
- 其他：2 → 移除写权限。

#### 创建文件
默认基础权限 666（`rw-rw-rw-`）与 `~022` 按位与：
- 所有者：`rw-` & `rw-` = `rw-`（6）
- 组：`rw-` & `r--` = `r--`（4）
- 其他：`rw-` & `r--` = `r--`（4）
最终文件权限为 **644**（`rw-r--r--`）。

#### 创建目录
默认基础权限 777（`rwxrwxrwx`）与 `~022` 按位与：
- 所有者：`rwx` & `rwx` = `rwx`（7）
- 组：`rwx` & `r-x` = `r-x`（5）
- 其他：`rwx` & `r-x` = `r-x`（5）
最终目录权限为 **755**（`rwxr-xr-x`）。

---

**常见的 umask 值及其效果**

| umask | 文件权限 | 目录权限 | 说明                                    |
| ----- | -------- | -------- | --------------------------------------- |
| 022   | 644      | 755      | 最常用，所有者可读写，其他人只读/执行   |
| 002   | 664      | 775      | 组可写，适用于共享目录                  |
| 077   | 600      | 700      | 仅所有者可访问，最严格                  |
| 027   | 640      | 750      | 所有者完全控制，组可读/执行，其他无权限 |
| 000   | 666      | 777      | 无限制（危险，不推荐）                  |

**Tips:**

1. **umask 只影响新创建的文件**，对已存在的文件权限无影响。
2. **root 用户的典型 umask 是 022**，普通用户也可能是 022 或 002，取决于发行版配置。
3. **子进程继承父进程的 umask**，因此在脚本中设置 umask 会影响脚本中运行的所有命令。
4. **符号链接的权限不受 umask 影响**，因为符号链接的权限总是 777（但实际访问权限由目标文件决定）。
5. **使用 `mkdir` 或 `open` 等函数时，可以显式指定权限，但最终权限仍会与 umask 进行“与”运算**。例如：
   
   ```c
   creat("file", 0666);  // 实际权限 = 0666 & ~umask
   mkdir("dir", 0777);   // 实际权限 = 0777 & ~umask
   ```
   如果你想完全忽略 umask，可以在创建后立即用 `chmod` 修改权限，或者在调用前临时设置 umask 为 0（但需谨慎）。
   
6. **安全建议**：除非必要，不要将 umask 设为 000。在编写需要创建敏感文件的程序时，可以临时设置严格的 umask（如 077），创建完成后再恢复。



# Linux的系统错误

## 库函数与系统调用



| 特性           | 系统调用                                    | 库函数                                         |
| :------------- | :------------------------------------------ | :--------------------------------------------- |
| **运行级别**   | 内核态（通过陷阱指令进入内核）              | 用户态                                         |
| **上下文切换** | 涉及用户态到内核态的切换，开销较大          | 无上下文切换，开销小                           |
| **功能**       | 提供操作系统核心服务（进程、文件、网络等）  | 提供更高级、更易用的功能（格式化、缓冲、算法） |
| **接口**       | 通常由操作系统定义，较底层                  | 由库的设计者定义，更抽象                       |
| **可移植性**   | 依赖特定操作系统，不同系统间差异大          | 可移植性更好（如 C 标准库几乎所有平台都有）    |
| **错误处理**   | **失败时设置全局 `errno`，返回 -1 或 NULL** | **可能设置 `errno`，也可能返回其他错误指示**   |
| **缓冲**       | 无缓冲，直接操作内核对象                    | 常带缓冲（如 `stdio` 的流缓冲），提高性能      |
| **示例**       | `read()`、`write()`、`open()`               | `fread()`、`fwrite()`、`fopen()`、`printf()`   |



## errno

> `errno` 是 Linux/Unix 环境编程中用于报告错误的核心机制，它是一个由系统调用和某些库函数在出错时设置的全局（实为线程局部）变量，用来指示具体的错误原因。

- **定义**：`errno` 是一个由 POSIX 和 ISO C 标准定义的**整数左值表达式**（lvalue），当系统调用或库函数失败时，内核或库会为其赋予一个正整数的错误码，用以标识具体的错误类型。
- **声明位置**：`#include <errno.h>`
- **初始值**：程序启动时，`errno` 的值为 0。但没有任何标准库函数会将其清零，因此必须通过检查函数的返回值来判断是否发生错误，再查看 `errno`。
- 并不是全部的库函数在调用失败时都会设置errno的值，以man手册为准（一般来说，不属于系统调用的函数不会设置errno，属于系统调用的函数才会设置errno）。

## 使用 `errno` 的正确规则

### **必须先检查返回值，再使用 `errno`**
函数成功时不会修改 `errno`，其值可能是前一次失败留下的，因此**绝对不能用 `errno` 来判断是否出错**。正确模式：
```c
#include <iostream>
#include <sys/stat.h>
#include <string.h>
using namespace std;

int main()
{
  char path1[256]="tmp/aaa/bbb";
  char msg[256];
  int res1 = mkdir(path1,0755);
  perror(msg);
  cout<<res1<<endl;
  cout<<"1th:"<<errno<<endl;
  cout<<msg;
  
  char path2[256]="./pro";
  int res2 = mkdir(path2,0755);
  perror(msg);
  cout<<res2<<endl;
  cout<<"2th:"<<errno<<endl;
  cout<<msg<<endl;
  return 0;
}
```

```bash
No such file or directory
-1
1th:2
No such file or directory
0
2th:2 			#第二次成功了但是errno保持原状

```



### **及时保存 `errno`**

因为任何库函数（包括 `fprintf`、`strerror` 等）都可能修改 `errno`，所以一旦检测到错误，应立即将 `errno` 的值保存到局部变量中。

### **不要假设函数成功会清零 `errno`**
标准规定：函数成功时，`errno` 保持不变。因此不能依赖 `errno` 为 0 来断言成功。

### **信号处理函数中需保存和恢复 `errno`**
信号处理程序可能调用某些异步信号安全的函数，这些函数可能修改 `errno`。因此，信号处理函数入口应保存原 `errno`，返回前恢复：
```c
void handler(int sig) {
    int saved_errno = errno;
    // ... 使用异步信号安全函数 ...
    errno = saved_errno;
}
```

###  **`errno` 的值仅在函数明确指出失败时才有效**
只有当一个函数的标准文档中说明它在失败时设置 `errno`，那么当该函数返回错误指示时，`errno` 才包含有效信息。



## 常见错误码分类及示例

错误码通常以 `E` 开头的宏定义，如 `ENOENT`。以下是一些常见错误码的分类和含义（完整列表可通过 `man errno` 查看）：

| 错误码        | 值   | 含义                             | 常见场景                                    |
| ------------- | ---- | -------------------------------- | ------------------------------------------- |
| **文件/目录** |      |                                  |                                             |
| ENOENT        | 2    | No such file or directory        | 打开不存在的文件                            |
| EACCES        | 13   | Permission denied                | 对文件没有读/写/执行权限                    |
| EEXIST        | 17   | File exists                      | 创建文件时文件已存在且指定了 O_EXCL         |
| ENOTDIR       | 20   | Not a directory                  | 路径中的某部分不是目录                      |
| EISDIR        | 21   | Is a directory                   | 试图写入一个目录                            |
| **进程/资源** |      |                                  |                                             |
| EAGAIN        | 11   | Resource temporarily unavailable | 非阻塞模式下无数据可读/写，或 fork 资源不足 |
| ENOMEM        | 12   | Out of memory                    | 内存分配失败                                |
| EBUSY         | 16   | Device or resource busy          | 尝试删除正在使用的设备或挂载点              |
| **参数/状态** |      |                                  |                                             |
| EINVAL        | 22   | Invalid argument                 | 给系统调用传入了无效参数                    |
| EINTR         | 4    | Interrupted system call          | 系统调用被信号中断，通常需要重试            |
| EFAULT        | 14   | Bad address                      | 指针指向非法地址                            |
| **网络相关**  |      |                                  |                                             |
| ECONNREFUSED  | 111  | Connection refused               | 连接被服务器拒绝                            |
| ETIMEDOUT     | 110  | Connection timed out             | 连接超时                                    |

---

## 与 `errno` 相关的函数

### **`perror` – 打印错误消息到 stderr**
```c
#include <stdio.h>
void perror(const char *s);
```
- 输出：`s: 错误描述`，自动换行。例如 `perror("open")` 可能输出 `open: No such file or directory`。
- 用于在控制台显示最近一次系统错误的详细信息，在实际开发中，服务程序在后台运行，通过控制台显示错误信息意义不大。（对调试程序略有帮助）

示例：

```cpp
#include <iostream>
#include <sys/stat.h>
#include <string.h>
using namespace std;

int main()
{
  char path[256]="tmp/aaa/bbb";
  char msg[256];
  int res = mkdir(path,0755);
  perror(msg);
  cout<<msg;
  return 0;
}
```

```bash
No such file or directory
```



### **`strerror` – 将错误码转换为描述字符串**
```c
#include <string.h>
char *strerror(int errnum);
int strerror_r(int errnum, char *buf, size_t buflen);	
```
- 返回一个指向静态分配的字符串的指针（不可重入）。线程安全版本 `strerror_r` 可将结果写入用户提供的缓冲区。
- 注意：不应修改返回的字符串。

**示例：**

```cpp
#include <iostream>
#include <errno.h>
#include <string.h>
using namespace std;
int main()
{
  for(int i=0;i<200;i++)
  	cout<<i<<":"<<strerror(i)<<endl;
  return 0;
}
```

```bash
0:Success
1:Operation not permitted
2:No such file or directory
3:No such process
4:Interrupted system call
5:Input/output error
6:No such device or address
7:Argument list too long
8:Exec format error
9:Bad file descriptor
10:No child processes
11:Resource temporarily unavailable
12:Cannot allocate memory
13:Permission denied
14:Bad address
15:Block device required
16:Device or resource busy
17:File exists
18:Invalid cross-device link
19:No such device
20:Not a directory
21:Is a directory
22:Invalid argument
23:Too many open files in system
24:Too many open files
25:Inappropriate ioctl for device
26:Text file busy
27:File too large
28:No space left on device
29:Illegal seek
30:Read-only file system
31:Too many links
32:Broken pipe
33:Numerical argument out of domain
34:Numerical result out of range
35:Resource deadlock avoided
36:File name too long
37:No locks available
38:Function not implemented
39:Directory not empty
40:Too many levels of symbolic links
41:Unknown error 41
42:No message of desired type
43:Identifier removed
44:Channel number out of range
45:Level 2 not synchronized
46:Level 3 halted
47:Level 3 reset
48:Link number out of range
49:Protocol driver not attached
50:No CSI structure available
51:Level 2 halted
52:Invalid exchange
53:Invalid request descriptor
54:Exchange full
55:No anode
56:Invalid request code
57:Invalid slot
58:Unknown error 58
59:Bad font file format
60:Device not a stream
61:No data available
62:Timer expired
63:Out of streams resources
64:Machine is not on the network
65:Package not installed
66:Object is remote
67:Link has been severed
68:Advertise error
69:Srmount error
70:Communication error on send
71:Protocol error
72:Multihop attempted
73:RFS specific error
74:Bad message
75:Value too large for defined data type
76:Name not unique on network
77:File descriptor in bad state
78:Remote address changed
79:Can not access a needed shared library
80:Accessing a corrupted shared library
81:.lib section in a.out corrupted
82:Attempting to link in too many shared libraries
83:Cannot exec a shared library directly
84:Invalid or incomplete multibyte or wide character
85:Interrupted system call should be restarted
86:Streams pipe error
87:Too many users
88:Socket operation on non-socket
89:Destination address required
90:Message too long
91:Protocol wrong type for socket
92:Protocol not available
93:Protocol not supported
94:Socket type not supported
95:Operation not supported
96:Protocol family not supported
97:Address family not supported by protocol
98:Address already in use
99:Cannot assign requested address
100:Network is down
101:Network is unreachable
102:Network dropped connection on reset
103:Software caused connection abort
104:Connection reset by peer
105:No buffer space available
106:Transport endpoint is already connected
107:Transport endpoint is not connected
108:Cannot send after transport endpoint shutdown
109:Too many references: cannot splice
110:Connection timed out
111:Connection refused
112:Host is down
113:No route to host
114:Operation already in progress
115:Operation now in progress
116:Stale file handle
117:Structure needs cleaning
118:Not a XENIX named type file
119:No XENIX semaphores available
120:Is a named type file
121:Remote I/O error
122:Disk quota exceeded
123:No medium found
124:Wrong medium type
125:Operation canceled
126:Required key not available
127:Key has expired
128:Key has been revoked
129:Key was rejected by service
130:Owner died
131:State not recoverable
132:Operation not possible due to RF-kill
133:Memory page has hardware error
134:Unknown error 134
135:Unknown error 135
.....
```



```cpp
#include <iostream>
#include <sys/stat.h>
#include <string.h>
using namespace std;

int main()
{
  char path[256]="tmp/aaa/bbb";
  int res = mkdir(path,0755);
  cout<<res<<endl;
  cout<<strerror(errno)<<endl;

  return 0;
}
```

```bash
-1
No such file or directory
```



### **`errno` 相关的可重入函数**
- `strerror_r`（POSIX 和 GNU 两种版本，用法不同）。
- `perror` 本身不是线程安全的，因为它使用全局流 stderr，但通常输出是原子的。

---

## 线程安全与可重入性

- **`errno` 本身是线程安全的**：因为现代实现采用线程局部存储。
- **但某些函数可能间接导致问题**：例如 `strerror` 返回的字符串可能指向一个静态缓冲区，多次调用会互相覆盖，因此它是不可重入的。应优先使用 `strerror_r`。
- 信号处理程序中只能调用**异步信号安全的函数**（async-signal-safe）。这些函数包括 `write`、`read`、`_exit` 等，通常不包含 `perror` 或 `strerror`（因为它们可能使用锁）。因此信号处理程序中处理错误的方式有限：可以保存 `errno` 或使用简单的 `write` 输出预定义的字符串。

## 常见误区总结

1. **用 `errno` 判断是否出错**：错误！应该用函数返回值判断。
2. **未及时保存 `errno`**：在 `printf` 等函数后 `errno` 可能已被改变。
3. **在信号处理程序中调用非异步信号安全的函数**：可能导致死锁或数据损坏。
4. **假设 `errno` 为 0 表示成功**：不可靠。
5. **混淆 `errno` 和返回值的意义**：例如 `read` 返回 0 表示 EOF，不是错误，此时 `errno` 无意义。



# 目录、文件的更多操作

## access() 库函数

`access()` 用于检查调用进程对指定文件或目录是否具有某种权限（或判断文件是否存在）。它是基于进程的**实际用户 ID** 和**实际组 ID** 进行权限检查的，而不是有效用户 ID（与 `open` 等函数不同）。这在某些需要以特权身份运行的程序中很有用，可以临时检查实际用户的权限。

```c
#include <unistd.h>
int access(const char *pathname, int mode);
```

- **pathname**：文件或目录的路径。
- **mode**：要检查的权限掩码，可取以下值（定义在 `<unistd.h>`）：
  - `F_OK` (0)：测试文件是否存在。
  - `R_OK` (4)：测试是否有读权限。
  - `W_OK` (2)：测试是否有写权限。
  - `X_OK` (1)：测试是否有执行权限（对于目录则是搜索权限）。
  这些值可以通过按位或（`|`）组合，例如 `R_OK | W_OK` 表示同时检查读写权限。

**返回值**

- 成功（满足所有检查的权限）返回 **0**。
- 失败（至少一项不满足或发生错误）返回 **-1**，并设置 `errno` 以指示具体错误。

**常见错误**

- `EACCES`：权限不足（例如文件存在但无读权限）。
- `ENOENT`：文件不存在。
- `ENOTDIR`：路径中的某个部分不是目录。
- `EROFS`：文件在只读文件系统上，但检查写权限。



```c
#include <stdio.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>

int main() {
    const char *path = "/etc/passwd";

    if (access(path, F_OK) == 0) {
        printf("文件存在\n");
    } else {
        printf("文件不存在: %s\n", strerror(errno));
    }

    if (access(path, R_OK) == 0) {
        printf("有读权限\n");
    } else {
        printf("无读权限: %s\n", strerror(errno));
    }

    return 0;
}
```

**Tips:**

- `access()` 使用的是实际用户 ID，而不是有效用户 ID。对于设置了 set-user-ID 的程序，它可能产生与预期不同的结果。
- 在多线程程序中，`access()` 的结果可能不可靠，因为权限可能在检查和实际使用之间发生变化。通常建议直接尝试打开文件并处理错误，而不是先检查权限再操作（即“先试后问”原则）。
- 对于符号链接，`access()` 会检查链接指向的目标文件，而非链接本身。



### 补充:实际用户ID 有效用户ID

**实际用户 ID（Real UID）**

- **是谁启动了进程**：实际用户 ID 是运行该进程的用户的真实身份，由登录会话确定，通常不会改变（除非通过 `setuid()` 等函数显式修改）。
- **作用**：主要用于**记账和统计**，例如记录哪个用户创建了进程，以及发送信号时检查权限（如向另一个进程发送信号时，需要实际用户 ID 匹配或具有特权）。

**有效用户 ID（Effective UID）**

- **进程以谁的身份执行**：有效用户 ID 是内核在进行**权限检查**时使用的用户 ID。例如，当进程尝试打开一个文件时，内核会检查该文件权限是否允许有效用户 ID 执行此操作。
- **作用**：决定进程当前拥有的**访问权限**。



**示例：`passwd` 命令**

- 普通用户需要修改自己的密码，但密码通常存储在 `/etc/shadow` 文件中，该文件只有 `root` 用户可读写。
- `passwd` 程序被设置了 **setuid 位**（可通过 `ls -l /usr/bin/passwd` 查看，其权限为 `-rwsr-xr-x`，其中 `s` 表示 setuid）当一个可执行文件设置了 setuid 位时，任何用户运行该文件，**进程的有效用户 ID（effective UID）会被设置为文件所有者的 UID**（通常是 root），而不是运行者的实际用户 ID。这使得普通用户能够临时获得文件所有者的权限来执行特定任务。
- 当普通用户执行 `passwd` 时：
  - **实际用户 ID** 仍为该普通用户的 ID（比如 1000）。
  - **有效用户 ID** 被临时提升为文件所有者（这里是 `root`，ID 0）。
- 因此，进程在运行期间具有 `root` 权限，可以修改 `/etc/shadow`；但内核仍知道实际用户是谁，以便进行适当的记录或限制（例如，不允许该进程越权访问其他用户的文件）。

这样既让普通用户完成了需要特权的操作，又避免了赋予其永久的 `root` 权限，提高了系统安全性。



**总结**

- **实际用户 ID**：你是谁（启动进程的人）。
- **有效用户 ID**：你看起来是谁（权限检查的依据）。
- 这种区分使得普通用户可以**临时获得特权**执行特定任务，而不会永久提升权限，是现代操作系统安全机制的重要基石。



## stat() 库函数

`struct stat` 用于存储文件或目录的详细信息，定义在 `<sys/stat.h>` 中。其成员较多，但常用的是以下几个：

```c
struct stat {
    dev_t     st_dev;         // 文件的设备编号
    ino_t     st_ino;         // 文件的 inode 号
    mode_t    st_mode;        // 文件类型和权限（位掩码）
    nlink_t   st_nlink;       // 硬链接数
    uid_t     st_uid;         // 所有者用户 ID
    gid_t     st_gid;         // 所有者组 ID
    dev_t     st_rdev;        // 如果文件是设备文件，则为其设备号
    off_t     st_size;        // 文件大小（字节）
    blksize_t st_blksize;     // I/O 块大小（文件系统首选）
    blkcnt_t  st_blocks;      // 占用 512 字节块数
    time_t    st_atime;       // 最后访问时间
    time_t    st_mtime;       // 最后修改时间
    time_t    st_ctime;       // 最后状态更改时间
};
```

**重点成员**：
- **st_mode**：不仅包含文件权限，还包含文件类型。可使用以下宏判断文件类型（这些宏也定义在 `<sys/stat.h>`）：
  - `S_ISREG(st_mode)`：是否为普通文件
  - `S_ISDIR(st_mode)`：是否为目录
  - `S_ISCHR(st_mode)`：是否为字符设备
  - `S_ISBLK(st_mode)`：是否为块设备
  - `S_ISFIFO(st_mode)`：是否为 FIFO（命名管道）
  - `S_ISLNK(st_mode)`：是否为符号链接
  - `S_ISSOCK(st_mode)`：是否为套接字
- **st_size**：文件大小，对于普通文件是字节数；对于目录，通常是 4096 或其倍数，具体含义因文件系统而异。
- **st_mtime**：最后修改时间，为 `time_t` 类型，可通过 `ctime()` 或 `localtime()` 转换为可读格式。

###  stat() 函数族
有三个相关的函数：
```c
#include <sys/stat.h>

int stat(const char *pathname, struct stat *statbuf);
int fstat(int fd, struct stat *statbuf);
int lstat(const char *pathname, struct stat *statbuf);
```
- **stat()**：通过路径名获取文件属性，会跟随符号链接（即获取链接指向的目标文件属性）。
- **fstat()**：通过已打开的文件描述符获取文件属性。
- **lstat()**：与 `stat()` 类似，但当文件是符号链接时，返回的是链接本身的信息，而非目标文件。

**返回值**

- 成功返回 **0**。
- 失败返回 **-1**，并设置 `errno`。



```c
#include <stdio.h>
#include <sys/stat.h>
#include <time.h>
#include <string.h>
#include <errno.h>

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <file>\n", argv[0]);
        return 1;
    }

    struct stat st;
    if (stat(argv[1], &st) == -1) {
        perror("stat");
        return 1;
    }

    // 判断文件类型
    if (S_ISREG(st.st_mode))
        printf("普通文件\n");
    else if (S_ISDIR(st.st_mode))
        printf("目录\n");
    else
        printf("其他类型\n");

    printf("文件大小: %ld 字节\n", st.st_size);
    printf("最后修改时间: %s", ctime(&st.st_mtime));
    return 0;
}
```



**Tips:**

- `stat()` 会穿透符号链接，若需获取符号链接本身的信息，应使用 `lstat()`。
- `st_size` 对于目录、设备文件等可能没有意义，但仍会返回一个值。
- 时间字段是 `time_t`，通常为自 1970-01-01 00:00:00 UTC 以来的秒数。可使用 `ctime()`、`localtime()` 转换为字符串，或使用 `strftime()` 格式化。
- `st_mode` 的低 9 位是文件权限，可用常规的八进制掩码提取（如 `st.st_mode & 0777`），但直接使用 `chmod` 等函数时需要注意与权限宏的配合。

---

## utime() 库函数

`utime()` 用于修改文件的最后访问时间（`st_atime`）和最后修改时间（`st_mtime`）。它可以设置成指定时间，也可以设置为当前时间。

```c
#include <sys/types.h>
#include <utime.h>

int utime(const char *filename, const struct utimbuf *times);
```
其中 `struct utimbuf` 定义如下：
```c
struct utimbuf {
    time_t actime;  // 新的访问时间
    time_t modtime; // 新的修改时间
};
```



- **filename**：要修改时间的文件路径。
- **times**：指向 `utimbuf` 结构的指针。如果为 `NULL`，则将文件的访问时间和修改时间设置为当前时间。如果非空，则分别设置为 `actime` 和 `modtime` 指定的时间。

**返回值**

- 成功返回 **0**。
- 失败返回 **-1**，并设置 `errno`。



```c
#include <stdio.h>
#include <utime.h>
#include <errno.h>
#include <string.h>

int main() {
    const char *file = "test.txt";

    // 将文件的 atime 和 mtime 设置为当前时间
    if (utime(file, NULL) == -1) {
        perror("utime");
        return 1;
    }

    // 设置为指定的时间（例如 2024-01-01 00:00:00）
    struct utimbuf new_times;
    new_times.actime = 1704067200;   // 2024-01-01 00:00:00 UTC
    new_times.modtime = 1704067200;

    if (utime(file, &new_times) == -1) {
        perror("utime");
        return 1;
    }

    printf("文件时间修改成功\n");
    return 0;
}
```



**Tips:**

- 修改文件时间需要适当的权限：要么进程的有效用户 ID 等于文件的所有者，要么具有超级用户权限。如果 `times` 为 `NULL`，则要求进程对文件有写权限（或适当权限）。
- `utime()` 不会修改 `st_ctime`（状态更改时间），该字段会自动更新为当前时间。
- 有些系统提供了更精确的 `utimes()` 函数（支持微秒），以及 POSIX 标准的 `futimens()`、`utimensat()` 等，支持纳秒级精度和更细的控制。

---

## rename() 库函数

`rename()` 用于重命名文件或目录，也可以将其移动到另一个目录（相当于 `mv` 命令）。如果新路径已经存在，则根据具体情况进行替换。

```c
#include <stdio.h>

int rename(const char *oldpath, const char *newpath);
```

- **oldpath**：原路径名。
- **newpath**：新路径名。

**返回值**

- 成功返回 **0**。
- 失败返回 **-1**，并设置 `errno`。

**Tips:**

- 如果 `newpath` 已存在，则将其覆盖（要求类型一致，且权限允许）。
- 若 `oldpath` 和 `newpath` 指向同一文件（即硬链接），则什么也不做，成功返回。
- 重命名操作是原子的，即不会出现中间状态（例如其他进程无法在重命名期间看到一个不存在的文件或一个被部分覆盖的文件）。
- 对于目录，`newpath` 要么不存在，要么必须为空目录；并且 `oldpath` 和 `newpath` 必须在同一文件系统内。





```c
#include <stdio.h>
#include <errno.h>
#include <string.h>

int main() {
    if (rename("old.txt", "new.txt") == -1) {
        perror("rename");
        return 1;
    }
    printf("重命名成功\n");
    return 0;
}
```

**注意:**

- 跨文件系统的重命名不支持，如果需要在不同文件系统间移动，必须先复制再删除原文件。
- 重命名目录时，`newpath` 不能是 `oldpath` 的子目录（避免循环）。
- 对特殊文件（如设备文件、管道）同样适用。
- 需要适当权限：对包含 `oldpath` 和 `newpath` 的目录需要有写权限，以及相应的文件权限。

## remove() 库函数

`remove()` 用于删除文件或空目录，类似于 `rm` 命令。它是 ISO C 标准定义的函数，兼具 `unlink()` 和 `rmdir()` 的功能。

```c
#include <stdio.h>

int remove(const char *pathname);
```

- **pathname**：要删除的文件或目录路径。

**返回值**

- 成功返回 **0**。
- 失败返回 **-1**，并设置 `errno`。

**tips:**

- 如果 `pathname` 是一个文件，`remove()` 调用 `unlink()`。
- 如果 `pathname` 是一个目录，`remove()` 调用 `rmdir()`。
- 对于符号链接，`remove()` 会删除链接本身，而不是它指向的文件。



```c
#include <stdio.h>

int main() {
    if (remove("test.txt") == -1) {
        perror("remove");
        return 1;
    }
    printf("文件删除成功\n");
    return 0;
}
```

**注意:**

- 只能删除**空目录**，否则会失败并置 `errno` 为 `ENOTEMPTY` 或 `EEXIST`。
- 删除文件时，`unlink()` 只是删除目录项，文件实际内容在最后一个硬链接被删除且没有进程打开它时才会被释放。
- 权限要求：对包含该文件的目录需要有写和执行权限，且文件本身若无写权限，会询问（但 `remove` 本身不提示，直接尝试删除，如果目录权限允许，即使文件只读也可删除，因为删除操作修改的是目录，而不是文件内容）。
- 跨平台：`remove()` 是 C 标准库函数，在 Windows 下也可用，但行为可能略有差异（例如 Windows 上删除目录要求目录为空，且不能删除正在使用的文件）。





# 信号

> 信号（signal）是软件中断，是进程之间相互传递消息的一种方法，用于通知进程发生了事件，但是，不能给进程传递任何数据。

信号产生的原因有很多，在Shell中，可以用`kill`和`killall`命令发送信号：

```bash
kill -信号的类型 进程编号

killall -信号的类型 进程名
```

## 信号种类

| 信号名      | 信号值 | 默认处理动作 | 发出信号的原因                                         |
| ----------- | ------ | ------------ | ------------------------------------------------------ |
| SIGHUP      | 1      | A            | 终端挂起或者控制进程终止                               |
| **SIGINT**  | **2**  | **A**        | **键盘中断Ctrl+c**                                     |
| SIGQUIT     | 3      | C            | 键盘的退出键被按下                                     |
| SIGILL      | 4      | C            | 非法指令                                               |
| SIGABRT     | 6      | C            | 由abort(3)发出的退出指令                               |
| SIGFPE      | 8      | C            | 浮点异常                                               |
| **SIGKILL** | **9**  | **AEF**      | **采用kill  -9 进程编号 强制杀死程序。**               |
| **SIGSEGV** | **11** | **CEF**      | **无效的内存引用（数组越界、操作空指针和野指针等）。** |
| SIGPIPE     | 13     | A            | 管道破裂，写一个没有读端口的管道。                     |
| **SIGALRM** | **14** | **A**        | **由闹钟alarm()函数发出的信号。**                      |
| **SIGTERM** | **15** | **A**        | **采用“kill  进程编号”或“killall 程序名”通知程序。**   |
| SIGUSR1     | 10     | A            | 用户自定义信号1                                        |
| SIGUSR2     | 12     | A            | 用户自定义信号2                                        |
| **SIGCHLD** | **17** | **B**        | **子进程结束信号**                                     |
| SIGCONT     | 18     |              | 进程继续（曾被停止的进程）                             |
| SIGSTOP     | 19     | DEF          | 终止进程                                               |
| SIGTSTP     | 20     | D            | 控制终端（tty）上按下停止键                            |
| SIGTTIN     | 21     | D            | 后台进程企图从控制终端读                               |
| SIGTTOU     | 22     | D            | 后台进程企图从控制终端写                               |
| 其它        | <=64   | A            | 自定义信号                                             |

**注:处理动作一项中的字母含义如下**

- A 缺省的动作是终止进程。
- B 缺省的动作是忽略此信号，将该信号丢弃，不做处理。
- C 缺省的动作是终止进程并进行内核映像转储（core dump）。
- D 缺省的动作是停止进程，进入停止状态的程序还能重新继续，一般是在调试的过程中。
- E 信号不能被捕获。
- F 信号不能被忽略。



## 信号处理

进程对信号的处理方法有三种：

1. 对该信号的处理采用系统的默认操作，大部分的信号的默认操作是终止进程。
2. 设置信号的处理函数，收到信号后，由该函数来处理。
3. 忽略某个信号，对该信号不做任何处理，就像未发生过一样。

**signal函数(注册信号处理函数)可以设置程序对信号的处理方式。**

```cpp
#include <signal.h>
sighandler_t signal(int signum, sighandler_t handler);
```

参数：

- `signum`：要处理的信号编号（如 `SIGINT`、`SIGQUIT`）
- `handler`信号处理函数指针，可选值：
  - 自定义函数（如 `void func(int)`）
  - `SIG_IGN`：忽略该信号
  - `SIG_DFL`：恢复系统默认



## 信号的作用

服务程序运行在后台，如果想让中止它，杀掉不是个好办法，因为进程被杀的时候，是突然死亡，没有安排善后工作。

- 如果向服务程序发送一个信号，服务程序收到信号后，调用一个函数，在函数中编写善后的代码，程序就可以有计划的退出。
- 如果向服务程序发送0的信号，可以检测程序是否存活。

示例：

```cpp
#include <iostream>
#include <unistd.h>
#include <signal.h>
using namespace std;

void EXIT(int sig)
{
  cout << "收到了信号：" << sig << endl;
  cout << "正在释放资源，程序将退出......\n";

  // 以下是释放资源的代码。

  cout << "程序退出。\n";
  exit(0);  // 进程退出。
}

int main(int argc,char *argv[])
{
  // 忽略全部的信号，防止程序被信号异常中止。
  for (int ii=1;ii<=64;ii++) signal(ii,SIG_IGN);//将所有信号注册为忽略

  // 如果收到2和15的信号（Ctrl+c和kill、killall），本程序将主动退出。
  signal(2,EXIT);  signal(15,EXIT);

  while (true)
  {
    cout << "执行了一次任务。\n";
    sleep(1);
  }
}

```



## 发送信号

Linux操作系统提供了kill和killall命令向进程发送信号，在程序中，可以用`kill()`函数向其它进程发送信号。

```cpp
int kill(pid_t pid, int sig);
//kill()函数将参数sig指定的信号给参数pid 指定的进程。
```

参数:

- pid
  - pid>0 将信号传给进程号为pid 的进程。
  - pid=0 将信号传给和当前进程相同进程组的所有进程，常用于父进程给子进程发送信号，注意，发送信号者进程也会收到自己发出的信号。
  - pid=-1 将信号广播传送给系统内所有的进程，例如系统关机时，会向所有的登录窗口广播关机信息。
- sig：准备发送的信号代码，假如其值为0则没有任何信号送出，但是系统会执行错误检查，通常会利用sig值为零来检验某个进程是否仍在运行。

返回值:

成功执行时，返回0；失败返回-1，errno被设置。



# 进程终止

有8种方式可以中止进程，其中5种为**正常终止**，它们是：

1. 在main()函数用return返回；
2. 在任意函数中调用`exit()`函数；
3. 在任意函数中调用`_exit()`或`_Exit()`函数；
4. 最后一个线程从其启动例程（线程主函数）用return返回
5. 在最后一个线程中调用`pthread_exit()`返回

**异常终止**有3种方式，它们是：

1. 调用abort()函数中止；类似于接受一个信号
2. 接收到一个信号；
3. 最后一个线程对取消请求做出响应。



## 进程终止的状态

在main()函数中，return的返回值即终止状态，如果没有return语句或调用exit()，那么该进程的终止状态是0。

在Shell中，查看进程终止的状态：

```bash
echo $?
```



```cpp
//正常终止进程的3个函数（exit()和_Exit()是由ISO C说明的，_exit()是由POSIX说明的）。
void exit(int status);

void _exit(int status);

void _Exit(int status);
//status也是进程终止的状态。
```

如果进程被异常终止，终止状态为非0。  



## 资源释放的问题

- `retun`表示函数返回，会调用局部对象的析构函数，**main()函数中的**`return`还会调用全局对象的析构函数。
- `exit()`表示终止进程，不会调用局部对象的析构函数，只调用全局对象的析构函数。
- `exit()`会执行清理工作，然后退出，`_exit()`和`_Exit()`直接退出，不会执行任何清理工作。



| 特性维度                 | `return`                                                     | `exit(int status)`                                           | `_exit(int status)`（POSIX）                                 | `_Exit(int status)`（C 标准）                                |
| ------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| **本质**                 | C 语言关键字（函数返回语句）                                 | 标准库函数（`<stdlib.h>`）                                   | 系统调用封装（`<unistd.h>`）                                 | C 标准库函数（`<stdlib.h>`），是 `_exit()` 的标准化封装      |
| **作用范围**             | 1. 普通函数：仅退出当前函数，返回到调用者2. `main()` 函数：等价于 `exit(status)`，终止整个进程 | 终止**整个进程**（无论在哪个函数中调用）                     | 直接终止整个进程（底层实现，无任何中间逻辑）                 | 行为与 `_exit()` 一致（标准化版本），直接终止进程            |
| **退出前清理逻辑**       | 1. 普通函数：无任何清理，仅返回2. `main()` 函数：触发与 `exit()` 相同的清理逻辑 | 执行完整的进程退出清理：1. 调用 `atexit()`/`on_exit()` 注册的回调函数2. 刷新所有打开的标准 I/O 缓冲区（如 `printf` 缓冲区）3. 关闭所有打开的文件描述符4. 删除进程创建的临时文件 | 无任何用户态清理逻辑：1. 不执行 `atexit` 回调2. 不刷新标准 I/O 缓冲区3. 仅内核层面释放进程资源（内存、文件描述符等） | 与 `_exit()` 完全一致（C 标准统一接口），无用户态清理，仅内核层面释放资源 |
| **返回状态传递**         | 1. 普通函数：将值返回给调用者2. `main()`：将 `status` 传给父进程（通过 `wait()` 获取） | 将 `status` 传给父进程（低 8 位有效）                        | 将 `status` 传给父进程（低 8 位有效）                        | 将 `status` 传给父进程（低 8 位有效）                        |
| **可重入性（信号场景）** | 普通函数中安全；信号处理函数中 `return` 仅退出处理函数，无风险 | 不安全：清理逻辑可能调用 `malloc`/`printf` 等非可重入函数，信号处理函数中禁用 | 安全：无用户态清理，仅内核操作，信号处理函数中推荐使用       | 安全：与 `_exit()` 一致，信号处理函数中可使用                |
| **跨平台性**             | 完全跨平台（C 语言基础特性）                                 | 完全跨平台（C 标准库）                                       | 仅 POSIX 系统（Linux/Unix），Windows 无此接口                | 完全跨平台（C99 及以上标准）                                 |
| **底层依赖**             | `main()` 中最终调用 `exit()`                                 | 最终调用 `_exit()` 完成内核层面的进程终止                    | 直接调用内核的 `exit_group` 系统调用                         | 底层映射到对应系统的退出接口（Linux 下等价于 `_exit()`）     |
| **典型使用场景**         | 1. 普通函数返回结果 / 终止执行2. `main()` 函数终止进程（推荐） | 1. 非信号场景下主动终止进程2. 需要执行退出清理逻辑时（如刷新日志、释放临时资源） | 1. 信号处理函数中终止进程2. 不需要清理缓冲区 / 执行回调的场景（如子进程退出） | 跨平台场景下替代 `_exit()`，需要无清理的进程终止             |



## 进程终止函数

进程可以用`atexit()`函数登记终止函数（最多32个），这些函数将由`exit()`自动调用。

```CPP
#include <stdlib.h>
int atexit(void (*function)(void));
```

exit()调用终止函数的顺序与登记时**相反**。 进行进程退出前的收尾工作





# 调用可执行函数

Linux提供了`system()`函数和`exec函数族`，在C++程序中，可以执行其它的程序（二进制文件、操作系统命令或Shell脚本）。

## system()函数

```cpp
#include <stdlib.h>
int system(const char *command);
```

参数:

command为需要执行的命令字符串

返回值:

- 如果执行的程序不存在，system()函数返回非0；
- 如果执行程序成功，并且被执行的程序终止状态是0，system()函数返回0；
- 如果执行程序成功，并且被执行的程序终止状态不是0，system()函数返回非0。

```cpp
#include<iostream>
#include<stdlib.h>
using namespace std;
int main()
{
	//执行的程序不存在
	int res = system("/aaa/bb ./tmp");//开发中建议使用绝对路径
	cout<<"res="<<res<<endl;
	return 0;
}
```

```bash
sh: 1: /aaa/bb: not found
res=32512
```

```cpp
#include<iostream>
#include<stdlib.h>
using namespace std;
int main()
{
	//执行的程序成功,被执行的程序终止状态为0
	int res = system("/bin/ls ./");//开发中建议使用绝对路径
	cout<<"res="<<res<<endl;
	return 0;
}
```

```bash
root@LAPTOP-P5RJLSIB:/mnt/d/桌面# ./demo
 1228-刘老师分享          cpp不足.png      summeraize.txt                              学习
 2504.05897v1.pdf         cuda文档        '~$220103 李智莹.docx'                      '毕业论文（设计）开题报告(1).doc'
 C++网络编程基础.docx     demo            '~$2实验报告5_学号_姓名 (对应Unit7）.docx'   毕业设计
 Linux环境高级编程.docx   demo.cpp        '~$nux环境高级编程.docx'                     论文
 Profile                  desktop.ini     '~$智能报告 (已自动恢复).docx'               项目
'XMind 2021 64位'         epoll原理.docx   大模型学习路线.doc
res=0
```

```cpp
#include<iostream>
#include<stdlib.h>
using namespace std;
int main()
{
	//执行的程序成功,但是被执行的程序终止状态不是0
	int res = system("/bin/ls ./aaa");//开发中建议使用绝对路径
	cout<<"res="<<res<<endl;
	return 0;
}
```

```bash
/bin/ls: cannot access './aaa': No such file or directory
res=512
```



## exec函数族

```cpp
#include <unistd.h>
int execl(const char *path, const char *arg, ...);
int execlp(const char *file, const char *arg, ...);
int execle(const char *path, const char *arg,...,char * const envp[]);
int execv(const char *path, char *const argv[]);
int execvp(const char *file, char *const argv[]);
int execvpe(const char *file, char *const argv[],char *const envp[]);
```

常用是:`execl()`和`execv()`

tips:

1. 如果执行程序失败则直接返回-1，失败原因存于errno中。
2. 新进程的进程编号与原进程相同，但是，**新进程取代了原进程的代码段、数据段和堆栈**
3. 如果执行成功则函数不会返回，当在主程序中成功调用exec后，被调用的程序将取代调用者程序，也就是说，exec函数之后的代码都不会被执行。

```cpp
#include <iostream>
#include <string.h>
#include <unistd.h>
using namespace std;

int main(int argc,char *argv[])
{
  int ret=execl("/bin/ls","/bin/ls","-lt","/tmp",0);  // 最后一个参数0不能省略。
  cout << "ret=" << ret << endl;
  perror("execl");

  /*
  char *args[10];
  args[0]="/bin/ls";
  args[1]="-lt";
  args[2]="/tmp";
  args[3]=0;     // 这行代码不能省略。

  int ret=execv("/bin/ls",args);
  cout << "ret=" << ret << endl;
  perror("execv");
  */
}

```







# 创建进程







# 僵尸进程







# 多进程与信号
