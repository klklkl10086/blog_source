---
title: cuda编程入门
date: 2026-3-1 20:46:44
tags: ["CUDA","CPP"]
categories: ["AI Infra"]
typora-root-url: ./cuda编程入门
---



>资料:
>
>[在线cuda编程网站](https://leetgpu.com/)
>
>[谭升的博客](https://face2ai.com/categories/CUDA/)
>
>《GPU高性能编程CUDA实战》



# GPU架构



![img](gpu_sm.png)

![image-20260323222725390](image-20260323222725390.png)

流式多处理器（Streaming Multiprocessor、SM）是 GPU 的基本单元，每个 GPU 都由一组 SM 构成，SM 中最重要的结构就是计算核心 Core







# nvidia-smi指令

![image-20251118210332910](image-20251118210332910.png)

更多的命令问ai吧~

# 从cpp到cuda编程

一般的程序:

```cpp
//hello.cpp
#include <stdio.h>
int main()
{
    //不能使用cout
    printf("Hello world\n");
    return 0;
}
```

```bash
g++ hello.cpp -o hello
./hello
```

nvcc:

- 安装cuda即可使用nvcc
- nvcc支持纯c++代码编译
- 编译扩展名为.cu的cuda文件

```bash
nvcc hello.cu -o hello
```

```cpp
//hello.cu
#include <stdio.h>

int main()
{
    //不能使用cout
    printf("Hello world\n");
    return 0;
}
```

```bash
root@autodl-container-6bc24a9b46-e72ce521:~/cudacode/2.1lesson# nvcc hello.cu -o hellocu
root@autodl-container-6bc24a9b46-e72ce521:~/cudacode/2.1lesson# ./hellocu
Hello world
```





# 核函数

> **核函数** 是在GPU上并行执行的函数。它是CUDA编程模型的核心，允许你将计算任务分解成成千上万个并行线程，从而利用GPU的大规模并行计算能力。

1. **执行位置**：在GPU上并行执行,具有异步性。
2. **并行方式**：通过大量线程以“单指令多线程”的模式并行执行。
3. **调用方式**：由CPU（主机）调用，但运行在GPU（设备）上。
4. **返回类型**：必须返回 `void`。
5. 只能访问GPU内存
6. 不行使用变长参数 静态变量 函数指针
7. 不支持c++的iostream

## 定义

使用 `__global__` 关键字来声明一个函数为核函数。

```cpp
// 使用 __global__ 关键字定义核函数
__global__ void myKernel(int *array, int value) {//global和void可以互换位置
    // 计算当前线程的全局索引
    int idx = threadIdx.x + blockIdx.x * blockDim.x;
    // 每个线程对数组中不同的元素进行操作
    array[idx] += value;
}
```

`执行空间说明符`:

- `__global__`：在GPU上执行，**由CPU调用**。这是我们定义核函数时使用的。
- `__device__`：在GPU上执行，**由GPU调用**（通常是从其他 `__device__` 函数或核函数中调用）。
- `__host__`：在CPU上执行，由CPU调用（就是普通的C++函数）。可以同时使用 `__host__ __device__`，使得该函数既能被CPU调用，也能被GPU编译。



**cuda程序编写流程**:

```cpp
int main(void)
{
	主机代码
	核函数调用
	主机代码
	return 0;
}
```



## 调用

调用核函数时，需要使用特殊的尖括号语法 `<<< ... >>>` 来指定**执行配置**，即如何组织线程来执行这个核函数。

```cpp
#include <stdio.h>
__global__ void hello_from_gpu()
{
    printf("Hello from gpu\n");
}
// 在主机(CPU)代码中调用核函数
int main()
{
     //执行配置 <<<网格大小, 块大小, 动态共享内存大小(可选), 流(可选)>>>
    hello_from_gpu<<<1,1>>>();//1个线程块 块中有1个线程
    
    cudaDeviceSynchronize();//同步函数,等待gpu执行完毕,主机与gpu的同步
    return 0;   
}
```

`线程 线程块 网格`

- **线程**：最基本的执行单元。
- **线程块**：一组线程的集合。
  - 一个块内的线程可以：
    - 通过**共享内存**高效地交换数据。
    - 使用 `__syncthreads()` 函数进行同步。
  - 线程块之间是**相互独立**的。它们可以以**任何顺序**、在**任何SM（流多处理器）** 上执行。
  - 一个线程块的执行不应依赖于另一个线程块的结果。这是CUDA编程模型的一个基本假设。
- **网格**：所有线程块的集合。一个核函数启动的所有线程块构成一个网格。





# CUDA线程模型

## 线程模型结构

![img](kts7mm1vzn.png)

> CUDA线程模型是一个**分层的并行编程模型**，它将并行任务分解为多个层次，从粗粒度到细粒度依次是：
> **网格(grid) → 线程块(block) → 线程束 → 线程**

`线程`:最基本的执行单元

- 每个线程是独立的执行路径
- 执行相同的核函数代码，但处理不同的数据
- 有自己的程序计数器、寄存器组和本地内存

`线程块`:协作的线程组

- **共享内存**：块内所有线程共享一块快速片上内存
- **同步能力**：通过 `__syncthreads()` 实现块内线程同步
- **独立性**：不同线程块之间相互独立，可以乱序执行
- **维度**：可以是1D、2D或3D布局

`网格`: 完整的执行单元

- 包含所有执行**同一核函数**的线程块
- 当核函数启动时，就定义了一个网格
- 网格中的线程块被调度到不同的SM上执行

**注意**:

- 线程分块是逻辑划分,物理上线程不分块
- 配置线程: <<<网格大小,线程块大小>>>
- 最大允许线程块大小1024
- 最大允许网格大小$2^{32}-1$(针对一维网格)

```cpp
#include <stdio.h>
__global__ void hello_from_gpu()
{
    printf("Hello from gpu\n");
}
int main()
{
    hello_from_gpu<<<2,4>>>();//2线程块  一个块里有4个线程
    cudaDeviceSynchronize();
    return 0;   
}
```

```bash
root@autodl-container-6bc24a9b46-e72ce521:~/cudacode/2.3lesson# nvcc ex1.cu -o ex1
root@autodl-container-6bc24a9b46-e72ce521:~/cudacode/2.3lesson# ./ex1
Hello from gpu
Hello from gpu
Hello from gpu
Hello from gpu
Hello from gpu
Hello from gpu
Hello from gpu
Hello from gpu
```



## 一维线程模型

1. 每个线程在`核函数`中都有一个**唯一的身份标识**
2. 每个线程的唯一标识由<<<grid_size,block_size>>>确定,grid_size,block_size保存在内建变量(build-in variable) **目前考虑的是一维情况**
   - gridDim.x : 该数值等于执行配置中变量grid_size的值
   - blockDim.x : 该数值等于执行配置中变量block_size的值
3. 线程索引保存为内建变量
   - blockIdx.x : 该变量指定一个线程在一个网格中的线程块索引值,范围为0~gridDim.x-1
   - threadIdx.x : 该变量指定一个线程在一个线程块中的线程索引值,范围为0~blockDim.x-1

![image-20251119182816235](image-20251119182816235.png)

```cpp
// 一维网格和块 计算线程索引
int idx = blockIdx.x * blockDim.x + threadIdx.x;
//在上述例子中,idx的范围为0~7
```

```cpp
#include <stdio.h>
__global__ void hello_from_gpu()
{
    
    const int bid = blockIdx.x;
    const int tid = threadIdx.x;

    const int id = bid*blockDim.x+tid;
    printf("Hello from block %d and thread %d, global id %d\n",bid,tid,id);
}
int main()
{
    hello_from_gpu<<<2,4>>>();//2线程块  一个块里有4个线程
    cudaDeviceSynchronize();
    return 0;   
}
```

```bash
root@autodl-container-6bc24a9b46-e72ce521:~/cudacode/2.3lesson# nvcc ex1.cu -o ex1
root@autodl-container-6bc24a9b46-e72ce521:~/cudacode/2.3lesson# ./ex1
Hello from block 1 and thread 0, global id 4
Hello from block 1 and thread 1, global id 5
Hello from block 1 and thread 2, global id 6
Hello from block 1 and thread 3, global id 7
Hello from block 0 and thread 0, global id 0
Hello from block 0 and thread 1, global id 1
Hello from block 0 and thread 2, global id 2
Hello from block 0 and thread 3, global id 3
```



## 多维线程

![image-20251119184229406](image-20251119184229406.png)

![image-20251119184244577](image-20251119184244577.png)

![image-20251119184425543](image-20251119184425543.png)

![image-20251119184524180](image-20251119184524180.png)

![image-20251119185219189](image-20251119185219189.png)

**网格和线程块的限制条件**:

![image-20251119185323653](image-20251119185323653.png)



## 线程全局索引计算方式

## 线程全局索引

**一维网格 一维线程块:**

![image-20251119185717207](image-20251119185717207.png)

**二维网格 二维线程块:**
![image-20251119191022263](image-20251119191022263.png)

**三维网格  三维线程块:**

![image-20251119191154297](image-20251119191154297.png)



# NVCC编译流程和GPU计算能力

## NVCC编译流程

> NVCC（NVIDIA CUDA Compiler）的编译流程分为多个阶段，主要处理主机端（Host，CPU）代码和设备端（Device，GPU）代码的混合编译。

![image-20251119205631454](image-20251119205631454.png)

![CUDA Compilation Trajectory](cuda-compilation-from-cu-to-executable.png)

## PTX

> PTX（Parallel Thread Execution）是CUDA平台为基于 GPU的通用计算而定义的虚拟机和指令集

- **虚拟指令集**：不直接对应具体GPU硬件，而是抽象中间表示
- **跨架构兼容**：可在不同代际的NVIDIA GPU上运行

```bash
CUDA源码 (.cu) 
    ↓ NVCC编译
PTX代码 (.ptx)           ← 跨架构中间表示
    ↓ GPU驱动JIT编译  
具体架构SASS代码          ← 特定GPU机器码
    ↓ GPU执行
```

1. nvcc编译命令总是使用两个体系结构:一个是虚拟的中间体系结构，另一个是实际的GPU体系结构
2. 虚拟架构更像是对应用所需的GPU功能的声明
3. 虚拟架构应该尽可能选择低----适配更多实际GPU 
4. 真实架构应该尽可能选择高----充分发挥GPU性能
5. 虚拟架构应低于真实架构



## GPU架构和计算能力

![image-20251119210546435](image-20251119210546435.png)

并非GPU 的计算能力越高，性能就越高



## CUDA程序兼容性问题

## 虚拟架构计算能力

![image-20251119212759966](image-20251119212759966.png)

```bash
nvcc helloworld.cu –o helloworld -arch=compute_61
#编译出的可执行文件helloworld可以在计算能力>=6.1的GPU上面执行，在计算能力小于6.1的GPU则不能执行。
```

## 真实架构计算能力

![image-20251119213013409](image-20251119213013409.png)

```bash
nvcc helloworld.cu –o helloworld -arch=compute_61 -code=sm_60
#指定的真实架构能力为6.0虚拟架构为6.1违反(3)
```

## 多个GPU版本编译

![image-20251119213142292](image-20251119213142292.png)

## NVCC即时编译

1. 在运行可执行文件时，从保留的PTX代码临时编译出cubin文件

2. 在可执行文件中保留PTX代码，nvcc编译指令指定所保留的PTX代码虚拟架构:

   ```bash
   -gencode arch=compute_XY ,code=compute_XY
   #两个计算能力都是虚拟架构计算能力
   #两个虚拟架构计算能力必须一致
   ```

   

### NVCC编译默认计算能力

不同版本CUDA编译器在编译CUDA代码时，都有一个默认计算能力

![image-20251119213458783](image-20251119213458783.png)





# CUDA程序基本框架

![image-20251119214814450](image-20251119214814450.png)





# GPU设备管理



## cudaGetDeviceCount()

获取GPU数量

```cpp
__host__ cudaError_t cudaGetDeviceCount(int *count);
```

- **参数**：`count` 是一个指向 `int` 的指针，用于接收可用 CUDA 设备的数量。
- **返回值**：返回 `cudaError_t` 类型的错误码，`cudaSuccess` 表示成功，否则表示错误。



## cudaSetDevice()

设置当前线程使用的设备。

```cpp
__host__ cudaError_t cudaSetDevice(int device);
```

- **返回值**：`cudaError_t` 类型，`cudaSuccess` 表示成功，其他值表示错误（如 `cudaErrorInvalidDevice` 表示设备索引无效）。
- **参数**：`device` 是目标设备的序号（从 0 开始）



```cpp
#include<stdio.h>
int main()
{
    //检查计算机GPU的数量
    int iDeviceCount=0;
    cudaError_t error = cudaGetDeviceCount(&iDeviceCount);
    if(error!= cudaSuccess || iDeviceCount ==0)
    {
        printf("NO CUDA campatable GPU found\n");
        exit(-1);
    }
    else
    {
        printf("The count of GPUs is %d \n",iDeviceCount);
    }

    //设置执行
    int iDev = 0;
    error = cudaSetDevice(iDev);
    if(error!=cudaSuccess)
    {
        printf("fail to set GPU 0 for computing.\n");
        exit(-1);
    }
    else
    {
        printf("set GPU 0 for computing.\n");
    }
    return 0;
}
```



## cudaDeviceProp结构体

> 它是一个在 `cuda_runtime_api.h` 中定义的结构体。你的程序不需要手动创建和填充它的每个字段，而是通过调用一个专门的函数 `cudaGetDeviceProperties()`，让 CUDA 驱动自动帮你填充好当前 GPU 的所有信息

```cpp
struct cudaDeviceProp {
    char         name[256];                 // 设备名称
    size_t       totalGlobalMem;            // 全局内存总量（字节）
    size_t       sharedMemPerBlock;         // 每个线程块可用的共享内存（字节）
    int          regsPerBlock;              // 每个线程块可用的32位寄存器数
    int          warpSize;                  // 线程束大小（一般为32）
    size_t       memPitch;                  // 内存对齐的最大间距（字节）
    int          maxThreadsPerBlock;        // 每个线程块的最大线程数
    int          maxThreadsDim[3];          // 线程块各维度的最大尺寸
    int          maxGridSize[3];            // 网格各维度的最大尺寸
    int          clockRate;                 // 时钟频率（kHz）
    size_t       totalConstMem;             // 常量内存总量（字节）
    int          major;                     // 计算能力主版本号
    int          minor;                     // 计算能力次版本号
    size_t       textureAlignment;          // 纹理对齐要求（字节）
    size_t       texturePitchAlignment;     // 纹理内存行对齐要求（字节）
    int          deviceOverlap;             // 是否支持设备与主机并行操作（已过时，功能由异步并发取代）
    int          multiProcessorCount;       // 流多处理器（SM）的数量
    int          kernelExecTimeoutEnabled;  // 内核执行是否受时间限制（用于显示设备）
    int          integrated;                // 是否为集成GPU（如 Tegra）
    int          canMapHostMemory;          // 是否支持映射主机内存（零拷贝）
    int          computeMode;               // 计算模式（默认、独占、禁止等）
    int          maxTexture1D;              // 1D纹理最大宽度
    int          maxTexture2D[2];           // 2D纹理最大尺寸
    int          maxTexture3D[3];           // 3D纹理最大尺寸
    int          maxTexture1DLayered[2];    // 分层1D纹理最大尺寸
    int          maxTexture2DLayered[3];    // 分层2D纹理最大尺寸
    int          surfaceAlignment;          // 表面内存对齐要求
    int          concurrentKernels;         // 是否支持同时执行多个核函数
    int          ECCEnabled;                // 是否启用ECC（错误校正码）
    int          pciBusID;                  // PCIe总线ID
    int          pciDeviceID;               // PCIe设备ID
    int          pciDomainID;               // PCIe域ID
    int          tccDriver;                 // 是否使用TCC驱动（Tesla计算集群）
    int          asyncEngineCount;          // 异步引擎数量（用于复制）
    int          unifiedAddressing;         // 是否支持统一地址空间
    int          memoryClockRate;           // 显存时钟频率（kHz）
    int          memoryBusWidth;            // 显存总线位宽（位）
    int          l2CacheSize;               // L2缓存大小（字节）
    int          maxThreadsPerMultiProcessor; // 每个SM的最大常驻线程数
    int          streamPrioritiesSupported; // 是否支持流优先级
    int          globalL1CacheSupported;    // 是否支持全局内存L1缓存
    int          localL1CacheSupported;     // 是否支持局部内存L1缓存
    size_t       sharedMemPerMultiprocessor; // 每个SM的共享内存大小（字节）
    int          regsPerMultiprocessor;     // 每个SM的32位寄存器数
    int          managedMemory;             // 是否支持托管内存
    int          isMultiGpuBoard;           // 是否为多GPU板卡的一部分
    int          multiGpuBoardGroupID;      // 多GPU板卡组ID
    int          hostNativeAtomicSupported; // 是否支持主机本机原子操作
    int          singleToDoublePrecisionPerfRatio; // 单精度与双精度性能比
    int          pageableMemoryAccess;      // 是否支持可分页内存访问
    int          concurrentManagedAccess;   // 是否支持并发托管内存访问
    int          computePreemptionSupported; // 是否支持计算抢占
    int          canUseHostPointerForRegisteredMem; // 能否使用主机指针注册内存
    int          cooperativeLaunch;         // 是否支持协作启动
    int          cooperativeMultiDeviceLaunch; // 是否支持多设备协作启动
    size_t       sharedMemPerBlockOptin;    // 每个线程块可选的最大共享内存（字节）
    int          pageableMemoryAccessUsesHostPageTables; // 可分页内存访问是否使用主机页表
    int          directManagedMemAccessFromHost; // 主机是否可以直接访问托管内存
};
```



| 类别         | 属性名                             | 类型        | 说明                                              |
| :----------- | :--------------------------------- | :---------- | :------------------------------------------------ |
| **基础标识** | `name`                             | `char[256]` | 设备名称（如 "NVIDIA GeForce RTX 3090"）          |
|              | `major`, `minor`                   | `int`       | 计算能力版本，例如 8.6。决定了硬件特性集          |
|              | `totalGlobalMem`                   | `size_t`    | 全局内存（显存）总容量（字节）                    |
|              | `multiProcessorCount`              | `int`       | 流多处理器（SM）的数量，是并行度的基础            |
|              | `clockRate`                        | `int`       | GPU核心时钟频率（kHz）                            |
| **线程组织** | `maxThreadsPerBlock`               | `int`       | 每个线程块允许的最大线程数（通常为1024）          |
|              | `maxThreadsDim[3]`                 | `int[3]`    | 线程块在各维度上的最大尺寸（如 1024×1024×64）     |
|              | `maxGridSize[3]`                   | `int[3]`    | 网格在各维度上的最大尺寸（如 2³¹-1）              |
|              | `warpSize`                         | `int`       | 线程束大小（固定为32）                            |
|              | `maxThreadsPerMultiProcessor`      | `int`       | 每个SM上最大可驻留的线程总数（如 1536 或 2048）   |
| **内存资源** | `sharedMemPerBlock`                | `size_t`    | 每个线程块可用的最大共享内存（字节）              |
|              | `sharedMemPerMultiprocessor`       | `size_t`    | 每个SM可用的共享内存总量（字节）                  |
|              | `regsPerBlock`                     | `int`       | 每个线程块可用的32位寄存器数                      |
|              | `regsPerMultiprocessor`            | `int`       | 每个SM可用的32位寄存器总数                        |
|              | `totalConstMem`                    | `size_t`    | 常量内存总量（64 KB）                             |
|              | `l2CacheSize`                      | `int`       | L2缓存大小（字节）                                |
| **特性支持** | `concurrentKernels`                | `int`       | 是否支持多个核函数同时执行（非零表示支持）        |
|              | `unifiedAddressing`                | `int`       | 是否支持统一地址空间（主机与设备指针相同）        |
|              | `managedMemory`                    | `int`       | 是否支持托管内存（Unified Memory）                |
|              | `concurrentManagedAccess`          | `int`       | 是否支持CPU和GPU同时访问托管内存                  |
|              | `canMapHostMemory`                 | `int`       | 是否支持映射主机内存（零拷贝）                    |
|              | `cooperativeLaunch`                | `int`       | 是否支持协作启动（`cudaLaunchCooperativeKernel`） |
|              | `hostNativeAtomicSupported`        | `int`       | 主机是否支持64位原子操作                          |
|              | `computePreemptionSupported`       | `int`       | 是否支持GPU任务抢占                               |
|              | `ECCEnabled`                       | `int`       | 是否启用ECC（错误校正码，主要见于Tesla系列）      |
| **性能优化** | `memoryClockRate`                  | `int`       | 显存时钟频率（kHz）                               |
|              | `memoryBusWidth`                   | `int`       | 显存总线位宽（位），影响带宽                      |
|              | `singleToDoublePrecisionPerfRatio` | `int`       | 单精度与双精度浮点性能比（1表示性能相同）         |
|              | `asyncEngineCount`                 | `int`       | 异步复制引擎数量（用于并发数据传输）              |
| **设备类型** | `integrated`                       | `int`       | 是否为集成GPU（如 Tegra）                         |
|              | `tccDriver`                        | `int`       | 是否使用TCC驱动（仅Tesla，不支持图形）            |
|              | `kernelExecTimeoutEnabled`         | `int`       | 内核是否受看门狗时间限制（显示卡为1）             |





## cudaGetDeviceProperties()

```cpp
__host__ cudaError_t cudaGetDeviceProperties(cudaDeviceProp *prop, int device);
```

- **`prop`**：指向 `cudaDeviceProp` 结构体的指针，函数执行后会将设备属性填入此结构体。
- **`device`**：要查询的设备序号，从 `0` 开始，最大为 `cudaGetDeviceCount() - 1`。
- **返回值**：`cudaSuccess` 表示成功，否则返回相应的错误码（如 `cudaErrorInvalidDevice` 表示设备索引无效）。
- **`cudaDeviceGetAttribute(int *value, cudaDeviceAttr attr, int device)`**：当只需要查询单个属性时，使用此函数更高效，因为它只填充一个值，避免复制整个 `cudaDeviceProp` 结构体。



```cpp
#include <stdio.h>
#include <cuda_runtime.h>

int main()
{
    int count=0;
    cudaGetDeviceCount(&count);
    if(count==0) exit(1);
    
    for(int i=0;i<count;i++)
    {
        cudaDeviceProp cuPro;
        cudaGetDeviceProperties(&cuPro,i);
        printf("%d:%s\n",i,cuPro.name);
    }

    return 0;
}
```



## cudaChooseDevice()

**根据指定的属性条件，自动选择最匹配的 CUDA 设备**

```cpp
__host__ cudaError_t cudaChooseDevice(int *device, const cudaDeviceProp *prop);
```

- **`device`**：输出参数，指向一个整数的指针，函数执行后会将选中的设备索引号存入其中。
- **`prop`**：输入参数，指向一个 `cudaDeviceProp` 结构体的指针，表示期望的设备属性条件。
- **返回值**：`cudaError_t` 类型，`cudaSuccess` 表示成功，否则返回相应的错误码。
- `cudaChooseDevice` 会在系统中所有可用的 CUDA 设备中进行搜索，返回与 `prop` 中指定的属性**最匹配**的设备
- 由于其匹配算法不透明，在需要精确控制的场景下，自行实现设备筛选逻辑是更可靠的选择。



```cpp
#include <stdio.h>
#include <cuda_runtime.h>

int main() {
    int deviceCount;
    cudaGetDeviceCount(&deviceCount);
    
    if (deviceCount == 0) {
        printf("No CUDA devices found.\n");
        return 1;
    }

    // 设置期望的设备属性：计算能力至少为 5.0
    cudaDeviceProp desiredProp;
    memset(&desiredProp, 0, sizeof(cudaDeviceProp));
    desiredProp.major = 5;
    desiredProp.minor = 0;

    int selectedDevice;
    cudaError_t err = cudaChooseDevice(&selectedDevice, &desiredProp);
    
    if (err != cudaSuccess) {
        printf("cudaChooseDevice failed: %s\n", cudaGetErrorString(err));
        return 1;
    }

    // 使用选中的设备
    cudaSetDevice(selectedDevice);
    
    // 获取并打印选中设备的信息
    cudaDeviceProp actualProp;
    cudaGetDeviceProperties(&actualProp, selectedDevice);
    printf("Selected device: %d - %s (Compute Capability: %d.%d)\n", 
           selectedDevice, actualProp.name, actualProp.major, actualProp.minor);
    
    return 0;
}
```





---------

# 内存管理

> CUDA通过内存分配 数据传递 内存初始化 内存释放进行内存管理

![image-20251119215530502](image-20251119215530502.png)



## 内存分配

```cpp
__host__ __device__ cudaError_t cudaMalloc(void** devPtr, size_t size);
```

- `devPtr`: 指向设备内存指针的指针。函数会将分配的设备内存地址存储在这个指针中。
- `size`: 要分配的内存大小（以字节为单位）。
- 返回 `cudaError_t` 类型值，表示函数执行的状态。如果成功，返回 `cudaSuccess`
- **可以将`cudaMalloc()`分配的指针传递给在设备上执行的函数。** 
- **可以在设备代码中使用`cudaMalloc()`分配的指针进行内存读写操作。** 
- **可以将`cudaMalloc()`分配的指针传递给在主机上执行的函数。**
- **不能在主机代码中使用`cudaMalloc()`分配的指针进行内存读写操作。**
- 上述限制对于主机指针有相似的条件:主机指针只能访问主机代码中的内存, 而设备指针也只能访问设备代码中的内存。但是主机可以通过调用`cudaMemcpy`来访问设备上的内存

使用 `cudaMalloc` 分配的内存必须使用` cudaFree `来释放。

## 数据拷贝

`cudaMemcpy` 用于在**主机内存**和**设备内存**之间复制数据。

```cpp
__host__ cudaError_t cudaMemcpy(void* dst, const void* src, size_t count, cudaMemcpyKind kind)
```

- `dst`: 目标内存地址
- `src`: 源内存地址
- `count`: 要复制的字节数
- `kind`: 复制方向，指定数据是从主机到设备，还是从设备到主机等。这是一个枚举类型，主要取值有：
  - `cudaMemcpyHostToHost`： 主机 → 主机
  - `cudaMemcpyHostToDevice`： 主机 → 设备
  - `cudaMemcpyDeviceToHost`： 设备 → 主机
  - `cudaMemcpyDeviceToDevice`： 设备 → 设备
  - `cudaMemcpyDefault`： 根据指针地址自动判断方向（默认方式只允许在支持统一虚拟寻址的系统上使用）



## 内存初始化

`cudaMemset` 用于设置设备内存的值，功能类似于标准 C 的 `memset` 函数。

```cpp
__host__ cudaError_t cudaMemset(void* devPtr, int value, size_t count)
```

- `devPtr`: 指向设备内存的指针
- `value`: 要设置的值（以字节为单位设置）
- `count`: 要设置的字节数

`cudaMemset` 是按**字节**操作的，这与标准 `memset` 一致。这对于初始化 `char` 数组或清零内存非常有用，但对于设置非字节类型的特定值（如将所有 `int` 设置为 `1`）则不方便。



## 内存释放

`cudaFree` 用于释放由 `cudaMalloc`、`cudaMallocManaged` 等函数分配的**设备内存**。

```cpp
__host__ __device__ cudaError_t cudaFree(void* devPtr)
```

- `devPtr`: 指向要释放的设备内存的指针

- 只能释放由 CUDA 内存分配函数分配的内存。
- 试图释放无效的指针或已经释放的指针会导致未定义行为（通常是运行时错误）。
- 在主机程序退出前释放所有分配的设备内存是一个好习惯，但现代 CUDA 驱动在程序结束时也会自动清理。

```cpp
#include <stdio.h>
#include <cuda_runtime.h>
__global__ void   add(int a,int b, int*c)
{
     *c = a+b;
}

int main()
{
    int ans;
    int * dev;
    int a=2,b=3;

    cudaMalloc(&dev,sizeof(int));
    add<<<1,1>>>(a,b,dev);
    cudaMemcpy(&ans,dev,sizeof(int),cudaMemcpyDeviceToHost);

    cudaDeviceSynchronize();

    printf("%d",ans);

    cudaFree(dev);
    return 0;
}
```



# 自定义CUDA函数

`设备函数（device function）`

-  定义只能执行在GPU设备上的函数为设备函数 
- 设备函数只能被核函数或其他设备函数调用 
- 设备函数用device修饰

`核函数（kernel function）` 

- 用global修饰的函数称为核函数，一般由主机调用，在设备中执行 
-  global 修饰符既不能和host同时使用，也不可与device 同时使用

`主机函数（host function） `

- 主机端的普通 C++ 函数可用 __host__ 修饰 
- 对于主机端的函数， __host__修饰符可省略 
- 可以用 __host__ 和 __device__ 同时修饰一个函数减少冗余代码。编译器会针对主机 和设备分别编译该函数。



# 一维矩阵加法

```cpp
#include<stdio.h>

__global__ void addFromGPU(float *A ,float *B ,float *C,const int N)
{
    const int bid = blockIdx.x;
    const int tid = threadIdx.x;
    const int id = tid+bid*blockDim.x;

    C[id]=A[id]+B[id];
}
void initialData(float *addr,int elemCount)
{
    for(int i=0;i<elemCount;i++)
    {
        addr[i]=(float)(rand()& 0xff) / 10.f;
    }
    return ;
}
void setGPU()
{
    //1.检查计算机GPU的数量
    int iDeviceCount=0;
    cudaError_t error = cudaGetDeviceCount(&iDeviceCount);
    if(error!= cudaSuccess || iDeviceCount ==0)
    {
        printf("NO CUDA campatable GPU found\n");
        exit(-1);
    }
    else
    {
        printf("The count of GPUs is %d \n",iDeviceCount);
    }

    //2.设置执行
    int iDev = 0;
    error = cudaSetDevice(iDev);
    if(error!=cudaSuccess)
    {
        printf("fail to set GPU 0 for computing.\n");
        exit(-1);
    }
    else
    {
        printf("set GPU 0 for computing.\n");
    }
}
int main()
{
   // 1.设置GPU设备
   setGPU();

   //2.分配主机内存和设备内存,并初始化
   int iElemCount = 512;        //一个矩阵的元素数目
   size_t stBytesCount = iElemCount * sizeof(float); //字节数

   //(1)分配主机内存并初始化
    float *fpHost_A,*fpHost_B,*fpHost_C;
    fpHost_A = (float*) malloc(stBytesCount);
    fpHost_B = (float*) malloc(stBytesCount);
    fpHost_C = (float*) malloc(stBytesCount);
    if(fpHost_A!=NULL&&fpHost_B!=NULL&&fpHost_C!=NULL)
    {
        //主机内存初始化为0
        memset(fpHost_A,0,stBytesCount);
        memset(fpHost_B,0,stBytesCount);
        memset(fpHost_C,0,stBytesCount);
    }
    else
    {
        printf("Fail to allocate host memory!\n");
        exit(-1);
    }
    // (2)分配设备内存 并初始化
    float *fpDevice_A,*fpDevice_B,*fpDevice_C;
    cudaMalloc((float**)&fpDevice_A,stBytesCount);
    cudaMalloc((float**)&fpDevice_B,stBytesCount);
    cudaMalloc((float**)&fpDevice_C,stBytesCount);

    if (fpDevice_A != NULL && fpDevice_B != NULL && fpDevice_C != NULL)
    {
        cudaMemset(fpDevice_A,0,stBytesCount);
        cudaMemset(fpDevice_B,0,stBytesCount);
        cudaMemset(fpDevice_C,0,stBytesCount);
    }else
    {
        printf("fail to allocate memory\n");
        free(fpHost_A);
        free(fpHost_B);
        free(fpHost_C);
        exit(-1);
    }

    //3.初始化主机中的数据
    srand(666);
    initialData(fpHost_A,iElemCount);
    initialData(fpHost_B,iElemCount);

    //4.从主机复制数据到设备
    cudaMemcpy(fpDevice_A,fpHost_A,stBytesCount,cudaMemcpyHostToDevice);
    cudaMemcpy(fpDevice_B,fpHost_B,stBytesCount,cudaMemcpyHostToDevice);
    cudaMemcpy(fpDevice_C,fpHost_C,stBytesCount,cudaMemcpyHostToDevice);

    //5.调用核函数在设备上计算
    dim3 block(32);
    dim3 grid(iElemCount/32);//保证每个线程负责一个数据


    addFromGPU<<<grid,block>>>(fpDevice_A,fpDevice_B,fpDevice_C,iElemCount);
    
    //cudaDeviceSynchronize();//保证GPU执行完之后再执行以下语句

    //6.将计算得到的数据从设备传给主机
    cudaMemcpy(fpHost_C,fpDevice_C,stBytesCount,cudaMemcpyDeviceToHost);
    //隐式保证GPU执行完之后再执行 ,因此可以省略cudaDeviceSynchronize();

    for(int i = 0;i<10;i++)
    {
        printf("idx=%2d\tmatrix_A:%.2f\tmatrix_B:%.2f\tresult=%.2f\n", i+1, fpHost_A[i], fpHost_B[i], fpHost_C[i]);
    }
    //7.释放主机与设备内存
    free(fpHost_A);
    free(fpHost_B);
    free(fpHost_C);

    cudaFree(fpDevice_A);
    cudaFree(fpDevice_B);
    cudaFree(fpDevice_C);

    cudaDeviceReset();
    return 0;
}
```

Tips:

1. 上述代码人为设置一个线程可以负责一个数据,但当数据个数由512变化为513时,`dim3 grid(iElemCount/32);`就无法保证一个线程负责一个数据,因此要改为`dim3 grid((iElemCount + block.x - 1) / 32);`,即向上取整,此时线程个数会多于矩阵元素个数,因此在GPU上的运算函数要附加if条件。

2. 上述核函数可以拆分为核函数调用设备函数的形式

3. 结合上述两条,修改后的代码如下:

   ```cpp
   #include<stdio.h>
   
   __device__  float add(const float x,const float y)
   {
       return x+y;
   }
   
   __global__ void addFromGPU(float *A ,float *B ,float *C,const int N)
   {
       const int bid = blockIdx.x;
       const int tid = threadIdx.x;
       const int id = tid+bid*blockDim.x;
   
       if(id>=N) return ;
       C[id]=add(A[id],B[id]);
   }
   void initialData(float *addr,int elemCount)
   {
       for(int i=0;i<elemCount;i++)
       {
           addr[i]=(float)(rand()& 0xff) / 10.f;
       }
       return ;
   }
   void setGPU()
   {
       //1.检查计算机GPU的数量
       int iDeviceCount=0;
       cudaError_t error = cudaGetDeviceCount(&iDeviceCount);
       if(error!= cudaSuccess || iDeviceCount ==0)
       {
           printf("NO CUDA campatable GPU found\n");
           exit(-1);
       }
       else
       {
           printf("The count of GPUs is %d \n",iDeviceCount);
       }
   
       //2.设置执行
       int iDev = 0;
       error = cudaSetDevice(iDev);
       if(error!=cudaSuccess)
       {
           printf("fail to set GPU 0 for computing.\n");
           exit(-1);
       }
       else
       {
           printf("set GPU 0 for computing.\n");
       }
   }
   int main()
   {
      // 1.设置GPU设备
      setGPU();
   
      //2.分配主机内存和设备内存,并初始化
      int iElemCount = 513;        //一个矩阵的元素数目
      size_t stBytesCount = iElemCount * sizeof(float); //字节数
   
      //(1)分配主机内存并初始化
       float *fpHost_A,*fpHost_B,*fpHost_C;
       fpHost_A = (float*) malloc(stBytesCount);
       fpHost_B = (float*) malloc(stBytesCount);
       fpHost_C = (float*) malloc(stBytesCount);
       if(fpHost_A!=NULL&&fpHost_B!=NULL&&fpHost_C!=NULL)
       {
           //主机内存初始化为0
           memset(fpHost_A,0,stBytesCount);
           memset(fpHost_B,0,stBytesCount);
           memset(fpHost_C,0,stBytesCount);
       }
       else
       {
           printf("Fail to allocate host memory!\n");
           exit(-1);
       }
       // (2)分配设备内存 并初始化
       float *fpDevice_A,*fpDevice_B,*fpDevice_C;
       cudaMalloc((float**)&fpDevice_A,stBytesCount);
       cudaMalloc((float**)&fpDevice_B,stBytesCount);
       cudaMalloc((float**)&fpDevice_C,stBytesCount);
   
       if (fpDevice_A != NULL && fpDevice_B != NULL && fpDevice_C != NULL)
       {
           cudaMemset(fpDevice_A,0,stBytesCount);
           cudaMemset(fpDevice_B,0,stBytesCount);
           cudaMemset(fpDevice_C,0,stBytesCount);
       }else
       {
           printf("fail to allocate memory\n");
           free(fpHost_A);
           free(fpHost_B);
           free(fpHost_C);
           exit(-1);
       }
   
       //3.初始化主机中的数据
       srand(666);
       initialData(fpHost_A,iElemCount);
       initialData(fpHost_B,iElemCount);
   
       //4.从主机复制数据到设备
       cudaMemcpy(fpDevice_A,fpHost_A,stBytesCount,cudaMemcpyHostToDevice);
       cudaMemcpy(fpDevice_B,fpHost_B,stBytesCount,cudaMemcpyHostToDevice);
       cudaMemcpy(fpDevice_C,fpHost_C,stBytesCount,cudaMemcpyHostToDevice);
   
       //5.调用核函数在设备上计算
       dim3 block(32);
       dim3 grid((iElemCount-1+block.x)/block.x);//保证每个线程负责一个数据
   
   
       addFromGPU<<<grid,block>>>(fpDevice_A,fpDevice_B,fpDevice_C,iElemCount);
       
   
       //6.将计算得到的数据从设备传给主机
       cudaMemcpy(fpHost_C,fpDevice_C,stBytesCount,cudaMemcpyDeviceToHost);//隐式保证GPU执行完之后再执行
   
       for(int i = 0;i<10;i++)
       {
           printf("idx=%2d\tmatrix_A:%.2f\tmatrix_B:%.2f\tresult=%.2f\n", i+1, fpHost_A[i], fpHost_B[i], fpHost_C[i]);
       }
       //7.释放主机与设备内存
       free(fpHost_A);
       free(fpHost_B);
       free(fpHost_C);
   
       cudaFree(fpDevice_A);
       cudaFree(fpDevice_B);
       cudaFree(fpDevice_C);
   
       cudaDeviceReset();
       return 0;
   }
   ```

   

# 矢量求和

> 为什么要线程块分解为线程呢?

## 并行线程块

```cpp
//并行线程块
#include<stdio.h>
#include <cuda_runtime.h>
#define N 10
__global__ void add(int* a,int* b,int*c)
{
    int idx = blockIdx.x;
    printf("%d: is running\n",idx);
    if(idx<N)
    {
        c[idx]=a[idx]+b[idx];
    }
}
int main()
{
    int a[N],b[N],c[N];
    int * dev_a,*dev_b,*dev_c;
    //GPU分配内存
    cudaMalloc(&dev_a,sizeof(int)*N);
    cudaMalloc(&dev_b,sizeof(int)*N);
    cudaMalloc(&dev_c,sizeof(int)*N);

    //初始化a b数组
    for(int i=0;i<N;i++)
    {
        a[i]=i;
        b[i]=i*i;
    }

    //copy
    cudaMemcpy(dev_a,a,N*sizeof(int),cudaMemcpyHostToDevice);
    cudaMemcpy(dev_b,b,N*sizeof(int),cudaMemcpyHostToDevice);

    add<<<N,1>>>(dev_a,dev_b,dev_c);
    
    cudaMemcpy(c,dev_c,sizeof(int)*N,cudaMemcpyDeviceToHost);
    for(int i=0;i<N;i++) 
        printf("%d ",c[i]);
    cudaFree(dev_a);
    cudaFree(dev_b);
    cudaFree(dev_c);
    return 0;
}
```

```bash
0: is running
1: is running
2: is running
3: is running
4: is running
5: is running
6: is running
7: is running
8: is running
9: is running
0 2 6 12 20 30 42 56 72 90 
```

## 并行线程

```cpp
//并行线程块
#include<stdio.h>
#include <cuda_runtime.h>
#define N 10
__global__ void add(int* a,int* b,int*c)
{
    int idx = threadIdx.x;
    printf("%d: is running\n",idx);
    if(idx<N)
    {
        c[idx]=a[idx]+b[idx];
    }
}
int main()
{
    int a[N],b[N],c[N];
    int * dev_a,*dev_b,*dev_c;
    //GPU分配内存
    cudaMalloc(&dev_a,sizeof(int)*N);
    cudaMalloc(&dev_b,sizeof(int)*N);
    cudaMalloc(&dev_c,sizeof(int)*N);

    //初始化a b数组
    for(int i=0;i<N;i++)
    {
        a[i]=i;
        b[i]=i*i;
    }

    //copy
    cudaMemcpy(dev_a,a,N*sizeof(int),cudaMemcpyHostToDevice);
    cudaMemcpy(dev_b,b,N*sizeof(int),cudaMemcpyHostToDevice);

    add<<<1,N>>>(dev_a,dev_b,dev_c);

    cudaMemcpy(c,dev_c,sizeof(int)*N,cudaMemcpyDeviceToHost);
    for(int i=0;i<N;i++) 
        printf("%d ",c[i]);
    cudaFree(dev_a);
    cudaFree(dev_b);
    cudaFree(dev_c);
    return 0;
}
```

仅仅是更改了两行代码:

- `add<<<1,N>>>(dev_a,dev_b,dev_c);`
- `int idx = threadIdx.x;`





## 线程块并行和线程并行

> 对于N = 10的矢量求和我们可以任意选择并行粒度，但是当N特别大的时候，我们不得不考虑硬件对线程块以及线程的限制。
>
> **硬件将线程块的数量限制在65535之内，线程块内的最大线程数量不能超过设备属性结构的maxThreadPerBlock的值（大部分设备的值为512），**因此我们必须将线程并行和线程块并行结合起来。
>
> 而这里面的关键就在于：**核函数中的索引计算方式和核函数的调用方式（线程块大小和网格大小）**

假设我们的线程块内线程数量最多为128，而我们要处理的向量长度为N 



如果长度N仍在最大线程数之内，我们想要启动N个线程,很自然我们会设置核函数为`<<< (N+127)/128 , 128 >>>` , `(N+127)/128`是为了向上取整 , 否则当N = 127的时候会开出0个线程块	

```cpp
 add<<< (N+127)/128 , 128>>>(dev_a,dev_b,dev_c);
__global__ void add(int* a,int* b,int*c)
{
    int idx = blockIdx.x*blockDim.x+threadIdx.x;
    printf("%d: is running\n",idx);
    if(idx<N)
    {
        c[idx]=a[idx]+b[idx];
    }
}
```

那如果N超过了最大线程数之内呢,比如$N>65535*128$ , 如果依旧按照上面的写法 , 核函数会调用失败 , 此时我们就要修改核函数的运行方式

```cpp
__global__ void add(int* a,int* b,int*c)
{
    int idx = blockIdx.x*blockDim.x+threadIdx.x;
    printf("%d: is running\n",idx);
   	while(idx<N)//让一个线程负责多个位置
    {
        c[idx]=a[idx]+b[idx];
        idx = idx + blockIdx.x*blockDim.x;
    }
}
```

完整代码:

```cpp
//并行线程块
#include<stdio.h>
#include <cuda_runtime.h>
#define N (33*1024)
__global__ void add(int* a,int* b,int*c)
{
    int idx = blockIdx.x*blockDim.x+threadIdx.x;
   	while(idx<N)//让一个线程负责多个位置
    {
        c[idx]=a[idx]+b[idx];
        idx = idx + blockIdx.x*blockDim.x;
    }
}
int main()
{
    int a[N],b[N],c[N];
    int * dev_a,*dev_b,*dev_c;
    //GPU分配内存
    cudaMalloc(&dev_a,sizeof(int)*N);
    cudaMalloc(&dev_b,sizeof(int)*N);
    cudaMalloc(&dev_c,sizeof(int)*N);

    //初始化a b数组
    for(int i=0;i<N;i++)
    {
        a[i]=i;
        b[i]=i*i;
    }
    
    //copy
    cudaMemcpy(dev_a,a,N*sizeof(int),cudaMemcpyHostToDevice);
    cudaMemcpy(dev_b,b,N*sizeof(int),cudaMemcpyHostToDevice);

    add<<<128,128>>>(dev_a,dev_b,dev_c);
    //N = 33*1024 = 2.0625*128*128
    //想像把矩阵两个网格+一小块,让一个线程负责对应位置,可能是3个位置可能是2个位置
    cudaMemcpy(c,dev_c,sizeof(int)*N,cudaMemcpyDeviceToHost);
    for(int i=0;i<N;i++) 
        {
            if(a[i]+b[i]!=c[i])
                {
                    printf("ans is incorrect\n");
                }
        }
    printf("ans is right");
    cudaFree(dev_a);
    cudaFree(dev_b);
    cudaFree(dev_c);

    return 0;
}
```

到目前为止,将线程块分解的原因仅仅是因为硬件的限制,但是还有其他原因。

---------------





# CUDA内存模型

![CUDA内存模型](2.webp)

## 内存层次结构概览

从硬件角度看，CUDA 内存分为**片上内存**和**片外内存**：

- **片上内存**（高带宽、低延迟）：寄存器、共享内存、L1/L2 缓存。
- **片外内存**（容量大、延迟高）：全局内存、本地内存、常量内存、纹理内存。

从软件视角，CUDA 将内存划分为以下类型（按访问速度从快到慢排列）：

| 内存类型 | 物理位置                | 作用域           | 生命周期       | 访问特性                        |
| -------- | ----------------------- | ---------------- | -------------- | ------------------------------- |
| 寄存器   | 片上                    | 线程私有         | 线程执行期间   | 最快，无延迟，无冲突            |
| 本地内存 | 片外（显存）            | 线程私有         | 线程执行期间   | 慢，但编译器自动管理            |
| 共享内存 | 片上                    | 线程块内所有线程 | 线程块执行期间 | 快，可编程缓存，有 bank 冲突    |
| L2 缓存  | 片上                    | 所有线程         | 全局           | 自动缓存全局/本地/常量/纹理访问 |
| 常量内存 | 片外（但被 L1/L2 缓存） | 所有线程         | 全局           | 只读，广播机制，延迟低          |
| 纹理内存 | 片外（但被 L1/L2 缓存） | 所有线程         | 全局           | 只读，硬件滤波，地址对齐        |
| 全局内存 | 片外（显存）            | 所有线程         | 全局           | 容量大，延迟高，需合并访问      |

---

## 各类内存详细介绍

### 寄存器 (Registers)

- **特性**：每个线程私有的最快存储单元，数量有限（每个线程最多 255 个 32 位寄存器，取决于架构和编译选项）。
- **生命周期**：仅在当前线程执行期间有效。
- **使用**：局部变量（如 `int x;`）默认分配在寄存器中，除非编译器因寄存器溢出而将其放入本地内存。
- **性能**：零额外延迟，无 bank 冲突。但过多寄存器使用会降低线程占用率。

### 本地内存 (Local Memory)

- **特性**：逻辑上属于线程私有，但物理上存储在显存（全局内存）中。当编译器判断寄存器不足或变量为数组、结构体等无法完全放入寄存器时，会分配本地内存。
- **生命周期**：线程执行期间。
- **性能**：访问速度与全局内存相当（慢），但通常被 L1/L2 缓存部分缓解。应尽量避免大数组或过多变量导致的本地内存使用。

###  共享内存 (Shared Memory)

- **特性**：片上 SRAM，同一线程块内所有线程共享，极低延迟（~20-30 周期），高带宽。由程序员显式管理。
- **生命周期**：从线程块开始到结束。
- **使用**：用 `__shared__` 修饰符声明，可静态或动态分配。
- **性能关键**：**Bank 冲突**（32 个 bank）会降低有效带宽。优化访问模式（如使用 padding）可避免冲突。
- **典型应用**：数据复用（矩阵分块、规约、卷积）。

### 全局内存 (Global Memory)

- **特性**：显存（DRAM），容量最大（GB 级），所有线程可见，访问延迟高（400-800 周期）。通常使用 `cudaMalloc` 分配，`__device__` 修饰的全局变量也可分配在此。
- **生命周期**：从分配到显式释放（`cudaFree`），贯穿程序运行。
- **性能关键**：**合并访问**（Coalesced Access）至关重要。同一 warp 的线程访问连续对齐的内存地址时，硬件可合并为少数几次内存事务；否则会分散为多次事务，严重降低带宽。
- **优化**：利用共享内存作为缓存，减少全局内存访问次数。

### 常量内存 (Constant Memory)

- **特性**：驻留在显存，但被 L1/L2 缓存，所有线程可读（只读）。通过 `__constant__` 修饰符定义，容量较小（64 KB）。硬件支持**广播**机制：当 warp 中所有线程访问同一地址时，只需一次内存事务。
- **生命周期**：全局，使用 `cudaMemcpyToSymbol` 写入。
- **性能**：在 warp 内访问相同地址时非常快，否则退化为全局内存访问（且串行化）。适用于存储固定参数、查找表等。

### 纹理内存 (Texture Memory)

- **特性**：只读，驻留在显存，通过纹理引用（或 C++ 中的 `cudaTextureObject_t`）访问。硬件提供空间局部性优化（对二维/三维访问友好）、自动滤波（线性插值）、地址边界处理（镜像/钳位）。
- **生命周期**：与纹理对象/引用绑定，需显式销毁。
- **性能**：对于随机访问或具有空间局部性的访问，纹理缓存的性能优于全局内存。适用于图像处理、科学计算中不规则访问模式。

### L1 / L2 缓存

- **L1 缓存**：与共享内存共享片上资源（可通过配置调整比例）。缓存全局内存和本地内存的访问。
- **L2 缓存**：更大（MB 级），服务于所有内存访问（全局、本地、常量、纹理），提高数据重用效率。

---

## 内存作用域与生命周期

| 内存类型 | 可见性                 | 生命周期               |
| -------- | ---------------------- | ---------------------- |
| 寄存器   | 单个线程               | 线程内                 |
| 本地内存 | 单个线程               | 线程内                 |
| 共享内存 | 同一线程块内的所有线程 | 线程块内               |
| 全局内存 | 所有线程 + 主机        | 显式分配/释放          |
| 常量内存 | 所有线程               | 全局（静态）           |
| 纹理内存 | 所有线程               | 全局（静态或动态绑定） |

**重要**：全局内存、常量内存、纹理内存的生命周期跨越多个核函数调用，可持久化存储数据。共享内存和寄存器则在核函数执行完后自动释放。

---

## 内存访问性能要点

### 合并访问 (Global Memory)
- **定义**：一个 warp 的 32 个线程访问全局内存时，硬件将这些访问合并为尽可能少的 32 字节（或 128 字节）内存事务。
- **最佳实践**：让线程 i 访问第 i 个元素（或连续步长），且起始地址对齐到 32 字节（或 128 字节）。
- **示例**：`int data = global[tid]` 是合并的；`int data = global[tid * 32]` 则会导致 32 次独立事务，性能极差。

### Bank 冲突 (Shared Memory)
- 共享内存被划分为 32 个 bank（每个 bank 宽度通常为 4 字节）。
- 同一 warp 中多个线程访问同一 bank 的不同地址 → 串行化，延迟增加。
- 访问同一地址 → 广播，无冲突。
- 优化：调整数组维度（padding），避免步长为 bank 数的整数倍。

### 广播与只读缓存
- 常量内存：warp 内所有线程访问同一地址时，广播加速。
- 只读缓存（`__ldg` 或 `const restrict` 指针）：对于全局内存中只读数据，编译器可将其加载到只读缓存，提高带宽。

---

## 内存一致性模型与同步

CUDA 采用**宽松一致性模型**：不同线程之间对全局内存的写操作，不保证立即对其他线程可见，除非通过显式同步或原子操作。

- **同一线程块内**：使用 `__syncthreads()` 确保块内线程对共享内存和全局内存的写操作在屏障后对其他线程可见。
- **不同线程块之间**：无法直接同步。可以通过核函数结束（即 `<<<...>>>` 返回）隐式同步，或使用原子操作（如 `atomicAdd`）保证跨块的一致性。
- **原子操作**：提供对全局内存和共享内存的原子更新（如加、减、比较交换等），是跨线程协作的重要手段。





-----------

# CUDA 与 GPU 硬件架构及线程层次

## 软硬件映射关系

GPU 的核心设计思想是**用海量的低速核心通过高并发来隐藏延迟**。软件上的抽象概念与硬件上的物理实体有着严格的映射关系。

| 软件层次 (Software)        | 硬件实体 (Hardware)         | 映射与绑定规则                                               | 核心特征与开发建议                                           |
| :------------------------- | :-------------------------- | :----------------------------------------------------------- | :----------------------------------------------------------- |
| **Grid (网格)**            | **Entire GPU (整块显卡)**   | 一个 Kernel 启动时的总任务。                                 | 作用域最大，通过全局内存（VRAM）通信。                       |
| **Block (线程块)**         | **SM (流式多处理器)**       | **物理绑定**：一个 Block 诞生时被指派给一个 SM，**绝不能跨 SM 跑**。 | SM 可以跑多个 Block。Block 的大小（线程数）直接决定 SM 的占用率（Occupancy）。 |
| **Warp (线程束 - 32线程)** | **Warp Scheduler (调度器)** | 硬件执行和指令分发的**最小基本单位**。                       | 硬件只认识 Warp，不认识单个线程。                            |
| **Thread (线程)**          | **CUDA Core / Tensor Core** | 逻辑上的最小计算单元。                                       | 独享寄存器。                                                 |




## 不同粒度线程的性质与特点

### Thread（单线程粒度）
* **存储归属**：独占**寄存器（Register）**。如果寄存器用超了，会溢出到极慢的本地内存（Local Memory）。

### Warp（线程束粒度 - 32 个线程）—— 性能优化的核心
Warp 是 GPU 硬件调度的灵魂，具有以下物理性质：

* **锁步执行（天然同步）**：32 个线程在同一个时钟周期执行同一条指令。现代架构建议使用 `__shfl_sync` 等原语显式对齐。
* **分支分歧（Warp Divergence）**：`if-else` 会导致线程轮流执行（掩码机制），性能线性下降。
* **零开销上下文切换**：利用常驻寄存器，在 1 个周期内切换就绪 Warp 以隐藏访存延迟。
* > 在 CUDA 编程中，**warp 广播机制**是 GPU 线程束（warp）内一种高效的数据交换方式，它允许一个线程将其数据直接广播给同一 warp 内的其他所有线程，而无需通过共享内存或全局内存。广播通过 **shuffle 指令** 实现。一个线程将其寄存器的值直接传递给其他线程，数据在 warp 内通过硬件级通道传输，**不经过共享内存或全局内存**，因此延迟极低。
  >
  > **关键函数**：`__shfl_sync_sync(mask, var, srcLane, width)`

#### Warp 访存的“32 × 4”法则（内存合并）
为什么我们强调访存要连续？因为硬件是以 **Cache Line（缓存行）** 为单位搬运数据的。
* **账本拆解**：**32（Warp线程数） × 4 字节（如 float/int 大小） = 128 字节**。
* **硬件逻辑**：128 字节恰好是 NVIDIA GPU 全局内存单次**内存事务（Memory Transaction）**的标准尺寸。
* **合并访问（Coalesced）**：当 Warp 内 32 个线程访问连续地址时，硬件只需 **1 次** 128 字节的事务就能喂饱全家，带宽利用率 100%。
* **非合并访问（Uncoalesced）**：如果地址散乱，硬件可能被迫发起 **32 次** 独立的内存事务，有效带宽瞬间跌至 $\frac{1}{8}$ 甚至更低。


### Thread Block
* **存储归属**：共享**片上共享内存（Shared Memory / L1）**。
* **物理限制**：目前一个 Block 最大支持 **1024** 个线程。


## GPU 存储金字塔体系

| 存储类型                     | 速度 (时钟周期)      | 作用域 (Scope)  | 核心调优心法                                                 |
| :--------------------------- | :------------------- | :-------------- | :----------------------------------------------------------- |
| **寄存器 (Register)**        | $\approx 1$          | 单个线程        | 速度最快，容量极小。                                         |
| **共享内存 (Shared Memory)** | $\approx 10 - 30$    | 线程块 (Block)  | **完全由开发者控制**。用于解决 **Bank Conflict（Bank 冲突）** 和数据复用。 |
| **L1 / L2 缓存**             | $\approx 30 - 100$   | 整个设备        | 硬件自动管理。                                               |
| **全局内存 (Global Memory)** | $\approx 400 - 800$  | 整个 Grid / CPU | 即显存（VRAM）。必须做 **Memory Coalescing（内存合并访问）**，让 32 个线程凑齐 128 字节单次读取。 |
| **主机内存 (Host Memory)**   | 极慢（受 PCIe 限制） | 系统级          | CPU 的内存。MoE 模型在显存不够时会在这里卸载（Offload）参数。 |



# 共享内存

共享内存的本质是**用户管理的缓存**：它让你可以显式地把数据从慢速的全局内存加载到快速、低延迟的共享内存中，供同一小组的线程反复使用，从而大幅减少对全局内存的访问。

- **作用域**：**线程块（Block）** 内所有线程可见。不同块之间的线程不能互相访问对方的共享内存。
- **生命周期**：在核函数启动时分配，在线程块结束时自动释放。

```cpp
__global__ void kernel(int *input) {
    // 声明一个大小为 256 的整型共享内存数组
    __shared__ int s_data[256];
    
    int tid = threadIdx.x;          // 线程在线程块内的索引
    s_data[tid] = input[tid];       // 从全局内存加载到共享内存
    
    __syncthreads();                // 等待所有线程都加载完成
    
    // 现在所有线程都可以安全地使用 s_data 中的数据
    // ...
}
```



## bank冲突

为了能同时响应多个线程的访问，共享内存的硬件被分成了 32 个**Bank**（Bank）。每个Bank一次只能处理一个请求。

- 如果 32 个线程（一个 warp）每个线程都访问**不同的Bank**，那么一次就能完成，速度最快。
- 如果多个线程访问**同一个Bank**中的**不同地址**，那么这些访问必须**串行**进行，速度就会变慢。这就叫**Bank冲突**。
- 如果多个线程访问**同一个Bank中的同一个地址**，硬件会自动广播，不会冲突

### 示例

想象共享内存有 4 个Bank（Bank 0~3）。地址按Bank交替存放：

- 地址 0 → Bank 0
- 地址 1 → Bank 1
- 地址 2 → Bank 2
- 地址 3 → Bank 3
- 地址 4 → Bank 0
- 地址 5 → Bank 1
- ...

**场景 A（无冲突）**：线程 0 访问地址 0（Bank0），线程 1 访问地址 1（Bank1），线程 2 访问地址 2（Bank2），线程 3 访问地址 3（Bank3） → 完美，一次完成。

**场景 B（冲突）**：线程 0 访问地址 0（Bank0），线程 1 访问地址 4（Bank0），线程 2 访问地址 8（Bank0），线程 3 访问地址 12（Bank0） → 所有线程都争抢Bank 0，必须分 4 次完成，效率降低。



假设我们声明了一个二维数组 `__shared__ int s[32][32];`。在 C 语言中，它是**行优先**存储的：

- `s[0][0]` 在Bank 0
- `s[0][1]` 在Bank 1
- ...
- `s[0][31]` 在Bank 31
- `s[1][0]` 又在Bank 0
- ...

共享内存的Bank映射：地址偏移 `addr` 会被映射到Bank `addr % 32`（假设 32 个Bank）

### 按行访问（同一行，不同列）

```cpp
int val = s[row][threadIdx.x];   // threadIdx.x 从 0 到 31
```

对于线程$i$,它要访问的地址的偏移量为:$row*sizeof(s[0])+i$,则会被映射到$(row*sizeof(s[0])+i)\%32$即 $i\ \%\ 32$ , 因为线程i 从 0 到 31，Bank索引也依次是 0 到 31，每个线程访问不同的Bank → **无冲突**。

###  按列访问（同一列，不同行）

```cpp
int val = s[threadIdx.x][col];   // threadIdx.x 从 0 到 31，col 固定
```

对于线程$i$,它要访问的地址的偏移量为:$i*sizeof(s[0])+col$,则会被映射到$(i*sizeof(s[0])+col)\%32$即 $col\ \%\ 32$对于所有线程都会访问同一个bank的不同地址意味着所有 32 个线程都争抢**同一个Bank** → **32 路冲突**，性能极差。

### 如何解决Bank冲突？

- **填充（Padding）**：在声明时多分配一列，比如 `__shared__ int s[32][33];`。就会被映射到$(i*33+col)\%32$，每个线程就会访问不同的bank从而避免了冲突。
- **调整访问模式**：尽量让连续线程访问连续的地址。



## 线程同步

共享内存是可读可写的，但线程的执行顺序是不确定的。假设线程 0 先把数据写入共享内存，线程 1 接着读，如果线程 1 执行时线程 0 还没写完，线程 1 就会读到旧数据或随机值。

**`__syncthreads()`** 是一个**屏障**：

- 它保证线程块内所有线程都执行到这一行后，才继续往下执行。
- 它还保证在此调用之前所有线程对共享内存的写操作，对之后的所有线程都是可见的。

```cpp
__shared__ int s[256];
s[tid] = global[tid];
__syncthreads();   // 确保所有线程都加载完毕

// 现在可以安全地使用 s 中的数据
int val = s[tid % 256];
```

**注意**：在条件分支中使用 `__syncthreads()` 要特别小心。如果某些线程没有执行到该同步点（比如分支不同），程序可能会卡死。





# 点积运算

> 利用共享内存，使得一个线程块上的线程通信与协作，从而更好的实现矩阵点积运算

点积 : 对应位置相乘最后相加

```cpp
//书上例子
#include<stdio.h>
#include<cuda_runtime.h>

#define imin(a,b)(a<b? a:b)

const int N = 33*1024;
const int thraedsPerblock = 256;
const int blocksPerGrid = imin(32,(N+thraedsPerblock-1)/thraedsPerblock);

__global__ void dot(float*a ,float*b,float*c)
{
    __shared__ double cache[thraedsPerblock];//一个线程块内的线程共享
    int tid = threadIdx.x + blockDim.x*blockIdx.x;
    int cacheidx = threadIdx.x;
    float tmp =0;
    while(tid<N)
    {
        tmp += a[tid]*b[tid];
        tid += blockDim.x*gridDim.x;
    }
    cache[cacheidx] = tmp;
    //对同一线程块的线程进行同步
    __syncthreads();

    //规约  下列代码要求threadsPerBlock为2的倍数
    /*
    如果你设置 threadsPerBlock = 300，简单的 i /= 2 逻辑就会出问题：

    第一轮： i = 150。线程 0-149 工作，加完后剩下 150 个结果。

    第二轮： i = 75。线程 0-74 工作，加完后剩下 75 个结果。

    第三轮： i = 37（整数除法 75/2）。线程0-36工作会处理索引为37-73的数据 ，索引为 74 的那个数据点被遗漏了！

    结论： i /= 2 的代码实现之所以要求 2 的幂，是为了保证每一轮折半后，剩下的元素个数永远是偶数，直到最后剩下一个。

    */
    int i =blockDim.x/2;
    while(i!=0)//步长
    {
        if(cacheidx<i)
        {
            cache[cacheidx] += cache[cacheidx + i];
        }
        __syncthreads();
        i/=2;
    }
    if(cacheidx==0)
        c[blockIdx.x]=cache[0];

}
int main()
{
    float *a,*b,c,*partial_c;
    float * dev_a,*dev_b,*dev_partial_c;

    //CUP分配内存
    a=(float* )malloc(sizeof(float)*N);
    b=(float* )malloc(sizeof(float)*N);
    partial_c=(float* )malloc(sizeof(float)*blocksPerGrid);

    //GPU分配内存
    cudaMalloc(&dev_a,sizeof(float)*N);
    cudaMalloc(&dev_b,sizeof(float)*N);
    cudaMalloc(&dev_partial_c,sizeof(float)*blocksPerGrid);

    //初始化a b数组
    for(int i=0;i<N;i++)
    {
        a[i]=i;
        b[i]=i*i;
    }

    cudaMemcpy(dev_a,a,N*sizeof(float),cudaMemcpyHostToDevice);
    cudaMemcpy(dev_b,b,N*sizeof(float),cudaMemcpyHostToDevice);
    
    dot<<<blocksPerGrid,thraedsPerblock>>>(dev_a,dev_b,dev_partial_c);

    cudaMemcpy(partial_c,dev_partial_c,blocksPerGrid*sizeof(float),cudaMemcpyDeviceToHost);

    c = 0;
    for(int i=0;i<blocksPerGrid;i++)
    {
        c+=partial_c[i];
    }

    //验证答案
    double expected = (double)((long long)(N-1)*(N-1)) * ((long long)N*N) / 4.0;
    printf("GPU Result: %f, Expected: %f\n", c, expected);

    if (abs(c - expected) < 1.0) { // float 大数求和误差较大，范围放宽
        printf("ans is right\n");
    }
    else
        printf("Diff: %e\n", c - expected);
    cudaFree(dev_a);
    cudaFree(dev_b);
    cudaFree(dev_partial_c);

    free(a);
    free(b);
    free(partial_c);
    return 0;
}
//
```

很容易可以发现我们的答案算出来并不对，这是因为精度损失造成的

-----



**经典错误:尝试更换 __syncthreads()位置**

```cpp
//书上例子+自己改进
#include<stdio.h>
#include<cuda_runtime.h>

#define imin(a,b)(a<b? a:b)

const int N = 33*1024;
const int thraedsPerblock = 256;
const int blocksPerGrid = imin(32,(N+thraedsPerblock-1)/thraedsPerblock);

__global__ void dot(float*a ,float*b,float*c)
{
    __shared__ double cache[thraedsPerblock];//一个线程块内的线程共享
    int tid = threadIdx.x + blockDim.x*blockIdx.x;
    int cacheidx = threadIdx.x;
    float tmp =0;
    while(tid<N)
    {
        tmp += a[tid]*b[tid];
        tid += blockDim.x*gridDim.x;
    }
    cache[cacheidx] = tmp;
    //对同一线程块的线程进行同步
    __syncthreads();

    //规约  下列代码要求threadsPerBlock为2的倍数
    int i =blockDim.x/2;
    while(i!=0)//步长
    {
        if(cacheidx<i)
        {
            cache[cacheidx] += cache[cacheidx + i];
            __syncthreads();//让我们尝试更换位置，看看会发生什么
        }
        
        i/=2;
    }
    if(cacheidx==0)
        c[blockIdx.x]=cache[0];

}
int main()
{
    float *a,*b,c,*partial_c;
    float * dev_a,*dev_b,*dev_partial_c;

    //CUP分配内存
    a=(float* )malloc(sizeof(float)*N);
    b=(float* )malloc(sizeof(float)*N);
    partial_c=(float* )malloc(sizeof(float)*blocksPerGrid);

    //GPU分配内存
    cudaMalloc(&dev_a,sizeof(float)*N);
    cudaMalloc(&dev_b,sizeof(float)*N);
    cudaMalloc(&dev_partial_c,sizeof(float)*blocksPerGrid);

    //初始化a b数组
    for(int i=0;i<N;i++)
    {
        a[i]=i;
        b[i]=i*i;
    }

    cudaMemcpy(dev_a,a,N*sizeof(float),cudaMemcpyHostToDevice);
    cudaMemcpy(dev_b,b,N*sizeof(float),cudaMemcpyHostToDevice);
    
    dot<<<blocksPerGrid,thraedsPerblock>>>(dev_a,dev_b,dev_partial_c);

    cudaMemcpy(partial_c,dev_partial_c,blocksPerGrid*sizeof(float),cudaMemcpyDeviceToHost);

    c = 0;
    for(int i=0;i<blocksPerGrid;i++)
    {
        c+=partial_c[i];
    }

    //验证答案
    double expected = (double)((long long)(N-1)*(N-1)) * ((long long)N*N) / 4.0;
    printf("GPU Result: %f, Expected: %f\n", c, expected);

    if (abs(c - expected) < 1.0) { // float 大数求和误差较大，范围放宽
        printf("ans is right\n");
    }
    else
        printf("Diff: %e\n", c - expected);
    cudaFree(dev_a);
    cudaFree(dev_b);
    cudaFree(dev_partial_c);

    free(a);
    free(b);
    free(partial_c);
    return 0;
}
```

> **为什么不能放在 if 内部？**
> __syncthreads() 的作用是：强制线程块（Block）中的所有线程都到达这个点，之后才允许继续执行。
>
> 同步屏障的死锁风险： 根据 CUDA 编程指南，如果 __syncthreads() 位于条件分支中，那么必须保证该分支对整个线程块的所有线程计算结果一致（即全进或全不进）。
>
>  当 i=128 时，只有 cacheidx < 128 的线程进入了 if。剩下的 128 个线程（cacheidx >= 128）跳过了 if。
>
> 结果,进入 if 的线程在等跳过 if 的线程，而跳过的线程已经执行完毕或者在等下一轮。这在逻辑上理论上会导致 永久死锁（Deadlock）。



**__syncthreads()使用示例:**

```cpp
//书上例子
#include <stdio.h>
#include <cuda_runtime.h>

#define W 512
#define H 512

// 一个简单的显卡计算核函数：生成渐变色
__global__ void render_kernel(char *ptr)
{
    __shared__ char share[16][16];
    int x = blockIdx.x * blockDim.x + threadIdx.x;
    int y = blockIdx.y * blockDim.y + threadIdx.y;
    int offset = x + y * gridDim.x * blockDim.x;
    share[threadIdx.x][threadIdx.y] = 255 - threadIdx.x * threadIdx.y;
    __syncthreads(); // 同步，只有所有线程都写完共享内存了再进行读取共享内存
    if (x < W && y < H)
    {
        ptr[offset * 4 + 0] = share[15 - threadIdx.x][15 - threadIdx.y]; // 红
        ptr[offset * 4 + 1] = 0;                                         // 绿
        ptr[offset * 4 + 2] = 0;                                         // 蓝
        ptr[offset * 4 + 3] = share[15 - threadIdx.x][15 - threadIdx.y]; // 透明
    }
}

int main()
{
    char *dev_out;
    char *host_out = (char *)malloc(W * H * sizeof(char) * 4);

    cudaMalloc(&dev_out, W * H * sizeof(char) * 4);

    dim3 blocks(W / 16, H / 16);
    dim3 threads(16, 16);
    render_kernel<<<blocks, threads>>>(dev_out);

    cudaMemcpy(host_out, dev_out, W * H * sizeof(char) * 4, cudaMemcpyDeviceToHost);
    //不用在意只是为了打印图片
    FILE *fp = fopen("output.ppm", "wb");
    if (fp)
    {
        fprintf(fp, "P6\n%d %d\n255\n", W, H); // P6 代表二进制 RGB 格式
        for (int i = 0; i < W * H; i++)
        {
            // host_out 里的数据是 R, G, B, A, R, G, B, A...
            // PPM 只需要 R, G, B 三个字节
            fwrite(&host_out[i * 4 + 0], 1, 1, fp); // R
            fwrite(&host_out[i * 4 + 1], 1, 1, fp); // G
            fwrite(&host_out[i * 4 + 2], 1, 1, fp); // B
        }
        fclose(fp);
        printf("图像已保存为 output.ppm\n");
    }

    cudaFree(dev_out);
    free(host_out);
    return 0;
}

```





# 常量内存





我们先来看一个例子:

一个简单的光线追踪代码(书上例子)

```cpp
//书上例子
#include <stdio.h>
#include <cuda_runtime.h>

#define INF 2e10f
#define DIM 512
#define SPHERES 20
#define rnd(x) (x * rnd() / RAND_MAX)
struct Sphere
{
    float r, b, g;
    float radius;
    float x, y, z;
    __device__ float hit(float ox, float oy, float *n) // 判断是否会与光相撞
    {
        float dx = ox - x;
        float dy = oy - y;
        if (dx * dx + dy * dy < radius * radius) // 会相撞
        {
            float dz = sqrt(radius * radius - dx * dx - dy * dy); // 计算光与球面交点距离球心的垂直距离
            *n = dz / radius;
            return dz + z;
        }
        return -INF;
    }
};
Sphere *s;
__global__ void kernel(char *ptr)
{
    int x = threadIdx.x + blockDim.x * blockIdx.x; // 计算线程在所有线程中的编号
    int y = threadIdx.y + blockDim.y * blockIdx.y;

    int offset = x + y * blockDim.x * gridDim.x; // 计算线程所对应的字符数组编号

    float ox = x - DIM / 2; // 初始化光线位置，光线追踪我们采用逆向法，由画布的每一个点发出光线
    float oy = y - DIM / 2;
    float r = 0, g = 0, b = 0;
    float maxz = -INF;
    for (int i = 0; i < SPHERES; i++) // 遍历球体数组，查找距离当前线程负责的位置z轴方向最近的球体
    {
        float n;
        float t = s[i].hit(ox, oy, &n);
        if (t > maxz)
        {
            float fscale = n;
            r = s[i].r * fscale;
            g = s[i].g * fscale;
            b = s[i].b * fscale;
            maxz = t;
        }
    }
    ptr[offset * 4 + 0] = int(r * 255); // 上色
    ptr[offset * 4 + 1] = int(g * 255);
    ptr[offset * 4 + 2] = int(b * 255);
    ptr[offset * 4 + 3] = 255;
}
int main()
{
    cudaEvent_t start, stop;
    cudaEventCreate(&start);
    cudaEventCreate(&stop);
    cudaEventRecord(start, 0);

    char bitmap[DIM*4][DIM*4];
    char *dev_bitmap;
    cudaMalloc(&dev_bitmap, 4 * DIM * DIM * sizeof(char)); // 存放画布数据，乘以四是因为RGBN 决定一个像素的效果
    cudaMalloc(&s, sizeof(Sphere) * SPHERES);              // 存放球体数据

    Sphere *tmp_s = (Sphere *)malloc(sizeof(Sphere) * SPHERES);
    for (int i = 0; i < SPHERES; i++)
    {
        tmp_s[i].r = rnd(1.0f);
        tmp_s[i].g = rnd(1.0f);
        tmp_s[i].b = rnd(1.0f);
        tmp_s[i].x = rnd(1000.0f) - 500;
        tmp_s[i].y = rnd(1000.0f) - 500;
        tmp_s[i].z = rnd(1000.0f) - 500;
        tmp_s[i].radius = rnd(100.0f) + 20;
    }
    cudaMemcpy(s, tmp_s, sizeof(Sphere) * SPHERES, cudaHostToDevice);
    free(tmp_s);

    dim3 grid(DIM / 16, DIM / 16);
    dim3 threads(16, 16);
    kernel<<<grid, threads>>>(dev_bitmap); // 对应画布，即将画布拆成一个个16*16的小块，每一个小块的数据由对应线程块的线程负责
    cudaMemcpy(bitmap, dev_bitmap, 4 * DIM * DIM * sizeof(char), cudaDeviceToHost);
    cudaEventRecord(stop, 0);

    cudaFree(dev_bitmap);
    cudaFree(s);
    return 0;
}

```



尝试用常量内存优化



