---
title: Reduction:求和
date: 2026-03-27 22:55:07
tags: ["CUDA","CPP"]
categories: ["AI Infra"]
description: 规约求和
typora-root-url: ./Reduction-规约
---

> 参考资料:
> [英伟达官方资料](https://developer.download.nvidia.com/assets/cuda/files/reduction.pdf)
>
> [视频【CUDA】Reduce规约求和]( https://www.bilibili.com/video/BV1HvBSY2EJW/?p=2&share_source=copy_web&vd_source=777aaa8a415b68222e598d976e64642c)
>
> [【CUDA】硬件与工具探索合集（更新ing）]( https://www.bilibili.com/video/BV1haBZYDEmj/?p=2&share_source=copy_web&vd_source=777aaa8a415b68222e598d976e64642c)



# Reduction 0: Global Memory

## 思考路径

![Capture_20260406_200922](Capture_20260406_200922-1775477401521-2.jpg)



```cpp
/*
baseline:global memory
*/


#include <stdio.h>
#include <stdlib.h>
#define ThreadPerBlock  256
#define N  32*1024*1024

__global__ void reduction(float* a,float* res)//一个block的线程应该怎么做,
{
    int tidx = blockIdx.x*blockDim.x + threadIdx.x;//负责数组里面第几个数字
    
    for(int len=1;len<blockDim.x;len*=2)
    {
        if(threadIdx.x%(len*2)==0)//len*2是步长
        {
            a[tidx]+=a[tidx+len];
        }
        __syncthreads();
    }
    if(threadIdx.x==0)
            res[blockIdx.x]=a[blockIdx.x*blockDim.x];
}

void check(float* a,float*b,int n)
{
    for(int i=0;i<n;i++)
    {
        if(fabs(a[i]-b[i])>0.0001)
            printf("%lf",b[i]);
    }
}
int main()
{
    
    float* input,*output,*cuda_res;
    float* c_input,*c_output;

    int BlockNum = N/ThreadPerBlock;


    input = (float*)malloc(sizeof(float)*N);
    output = (float*)malloc(sizeof(float)*BlockNum);
    cuda_res = (float*)malloc(sizeof(float)*BlockNum);

    cudaMalloc((void**)&c_input,sizeof(float)*N);
    cudaMalloc((void**)&c_output,sizeof(float)*BlockNum);

    for(int i=0;i<N;i++)
    {
        input[i] = rand() % 100; 
    }

    cudaMemcpy(c_input,input,N*sizeof(float),cudaMemcpyHostToDevice);
    //GPU
    reduction<<<BlockNum,ThreadPerBlock>>>(c_input,c_output);

    cudaMemcpy(cuda_res,c_output,sizeof(float)*BlockNum,cudaMemcpyDeviceToHost);
    //CPU
    for(int i=0;i<BlockNum;i++)
    {
        float s=0;
        for(int j=0;j<ThreadPerBlock;j++)
        {
            int idx = i*ThreadPerBlock+j;
            s+=input[idx];
        } 
        output[i]=s;
    }

    check(output,cuda_res,BlockNum);

    free(input);
    free(output);
    free(cuda_res);
    cudaFree(c_input);
    cudaFree(c_output);


    return 0;
}
```



## 存在的性能问题

### 访存问题

| 内存类型     | 物理位置                | 作用域               | 生命周期           | 访问特性                         |
| ------------ | ----------------------- | -------------------- | ------------------ | -------------------------------- |
| 寄存器       | 片上                    | 线程私有             | 线程执行期间       | 最快，无延迟，无冲突             |
| **共享内存** | **片上**                | **线程块内所有线程** | **线程块执行期间** | **快，可编程缓存，有 bank 冲突** |
| L2 缓存      | 片上                    | 所有线程             | 全局               | 自动缓存全局/本地/常量/纹理访问  |
| 本地内存     | 片外（显存）            | 线程私有             | 线程执行期间       | 慢，但编译器自动管理             |
| 常量内存     | 片外（但被 L1/L2 缓存） | 所有线程             | 全局               | 只读，广播机制，延迟低           |
| 纹理内存     | 片外（但被 L1/L2 缓存） | 所有线程             | 全局               | 只读，硬件滤波，地址对齐         |
| **全局内存** | **片外（显存）**        | **所有线程**         | **全局**           | **容量大，延迟高，需合并访问**   |

我们采用global memory实现规约求和，会导致大量的访问显存请求，因此时间会很长。

### Warp Divergence

```cpp
if(threadIdx.x%(len*2)==0)//len*2是步长
{
	a[tidx]+=a[tidx+len];
}
```

**同一个Wrap中只有部分并且分散的线程在工作     ----------->      考虑换成集中的一部分线程工作**



### Bank Conflict

> 为了提高内存读写带宽，共享内存被分为了32块等大，每一块称为Bank，由于一个wrap也有32个线程，因此可以一个线程对应一个Bank。
>
> 在硬件层面，GPU 访问全局内存不是一个字节一个字节读的，而是**按块读取**的（通常是 32 字节或 128 字节的内存段）。当一个 Warp 的 32 个线程发起内存读取请求时，硬件会检查这 32 个地址。如果这些地址正好落在一个或两个连续的内存段内，硬件就会把它们**合并（Coalesce）**成 1 到 2 次内存事务（Memory Transaction）。

```cpp
if(threadIdx.x%(len*2)==0)//len*2是步长
{
	a[tidx]+=a[tidx+len];
}
```

**当len==1的时，会发现一个线程束的访存是间隔的，一次访存事务只有一半的数据有用。**



# Reduction 1: Shared Memory

解决Reduction 0 的访存问题，改用`shared memory`实现

```cpp
/*reduction 1 : shared memory*/

__global__ void reduction(float* a,float* res)//一个block的线程应该怎么做,
{
    __shared__ float shared[ThreadsPerBlock];
    
    int tidx = blockIdx.x*blockDim.x + threadIdx.x;//负责数组里面第几个数字
    shared[threadIdx.x] = a[tidx];//每个线程负责将自己需要操作的数据搬运到共享内存中
    __syncthreads();
    for(int len=1;len<blockDim.x;len*=2)//归并处理块内的数据
    {
        if(threadIdx.x%(len*2)==0)//len*2是步长
        {
            shared[threadIdx.x]+=shared[threadIdx.x+len];
        }
        __syncthreads();
    }
    if(threadIdx.x==0)
            res[blockIdx.x]=shared[threadIdx.x];
}
```

**只改善了reduction 0 的访存问题**

---------------------



# Wrap Divergence 与 Bank Conflict

> **它们的本质，都是“多个并行执行单元，同时请求访问同一个无法并行处理的资源”所导致的串行化现象。**



## Warp Divergence：控制冲突

>  现象：在一个Warp（32个线程）中，如果遇到 `if-else` 或循环等分支语句，不同线程走了不同的路径。GPU会先执行 `if` 路径（此时走 `else` 的线程闲置），再执行 `else` 路径（此时走 `if` 的线程闲置）。这导致这32个线程实际上是**串行**执行了两次，而非并行。

**造成上面现象的原因是SIMD（单指令多数据）执行模型与分支预测的缺失**

- GPU的核心是一个**控制单元**同时驱动**32个算术逻辑单元**（SIMD）。在任何一个时钟周期，所有32个单元只能执行**同一条指令**，而,Wrap是SIMD的执行单元。
- 当遇到分支时，硬件无法让一部分单元执行A指令，另一部分执行B指令。唯一的办法就是**时间上串行**：先让所有单元都执行A（不相关的单元静默），再让所有单元都执行B。
- 所以，冲突的资源是 **“控制逻辑/指令分发单元”** 。多个线程不同的控制流需求，争抢同一个指令发射端口，导致串行化。
- Wrap是执行单元，block是资源分配与管理单元。wrap里面的线程要执行同一条指令，但是block的多个wrap可以执行不同的指令，因此解决wrap divergence的其中一个方式就是，尽量让分支条件**按 Warp 对齐**



## Bank Conflict：内存冲突

> **现象：**共享内存被划分为32个同样大小的Bank（存储体）。当一个Warp中的多个线程同时访问**同一个Bank中不同地址**的数据时，这些访问会被串行化。如果32个线程访问的是32个不同Bank，则一次完成；如果都访问同一个Bank，则32次串行完成。

- **本质**：**多端口存储器的物理限制与高带宽需求的矛盾。**

  - 为了提供高带宽，共享内存被设计成**多Bank交叉访问**。理想情况下，每个Bank可以独立、并行地响应一个请求。
  - 但物理上，**每个Bank只有一个读/写端口**。如果一个Bank在同一时刻收到多个请求（即使地址不同），它无法同时处理。唯一的办法就是**时间上串行**。
  - 所以，冲突的资源是 **“Bank的访问端口”** 。多个线程并发的内存请求，争抢同一个存储体的物理端口，导致串行化。

  



------------------



# Reduction 2: Wrap Divergence

## 我的做法

通过将分支条件按照wrap对齐，解决wrap divergence

<img src="Capture_20260411_200308.jpg" alt="wrap_divergence" style="zoom:50%;" />

**由于block中有256/32=8个wrap,我们可以让分支条件按照wrap对齐,即将block分为等大的两部分,让其中一部分A负责与另一部分B求和,然后对A同样处理**

```cpp
/*
reduction 2 : wrap divergence
*/
__global__ void reduction(float* a,float* res)//一个block的线程应该怎么做,
{
    __shared__ float shared[ThreadsPerBlock];
    
    int tidx = blockIdx.x*blockDim.x + threadIdx.x;//负责数组里面第几个数字
    shared[threadIdx.x] = a[tidx];//每个线程负责将自己需要操作的数据搬运到共享内存中
    __syncthreads();

    // reduction2:分支按照wrap对齐

    for(int len = ThreadsPerBlock/2; len>=1 ;len/=2)
    {
        if(threadIdx.x<len)
        {
            shared[threadIdx.x]+=shared[threadIdx.x+len];
        }
        __syncthreads();
    }
    if(threadIdx.x==0)
            res[blockIdx.x]=shared[threadIdx.x];
}
```



## 官方做法

采用交错规约，步长从1到ThreadsPerBlock/2

```cpp
__global__ void reduction(float* a,float* res)//一个block的线程应该怎么做,
{
    __shared__ float shared[ThreadsPerBlock];
    
    int tidx = blockIdx.x*blockDim.x + threadIdx.x;//负责数组里面第几个数字
    shared[threadIdx.x] = a[tidx];//每个线程负责将自己需要操作的数据搬运到共享内存中
    __syncthreads();

    // reduction2:分支按照wrap对齐 交错相加

    for (int len = 1; len < blockDim.x; len *= 2) //步长,只让前面的线程工作后面的不工作
    {
        int index = 2 * len * threadIdx.x;//线程要负责处理的位置 2*len表示一组有多少 threadIdx.x是组数
        if (index < blockDim.x) {
            shared[index] += shared[index + len];
    }
    __syncthreads();
}
    if(threadIdx.x==0)
            res[blockIdx.x]=shared[threadIdx.x];
}
```



----------------



# Reduction 3: Bank Conflict

`Reduction1`中的**官方做法**存在`bank conflict`

- 官方做法`shared[index] += shared[index + len],index = 2 * len * threadIdx.x` 
  - 在第一次循环中0号和16号发生`bank conflict`

然后就改成了`reduction2我的做法` ~~原来我是天才来着~~

```cpp
/*
reduction 3 : Bank Conflict
*/
__global__ void reduction(float* a,float* res)//一个block的线程应该怎么做,
{
    __shared__ float shared[ThreadsPerBlock];
    
    int tidx = blockIdx.x*blockDim.x + threadIdx.x;//负责数组里面第几个数字
    shared[threadIdx.x] = a[tidx];//每个线程负责将自己需要操作的数据搬运到共享内存中
    __syncthreads();

    // reduction2:分支按照wrap对齐

    for(int len = ThreadsPerBlock/2; len>=1 ;len/=2)
    {
        if(threadIdx.x<len)
        {
            shared[threadIdx.x]+=shared[threadIdx.x+len];
        }
        __syncthreads();
    }
    if(threadIdx.x==0)
            res[blockIdx.x]=shared[threadIdx.x];
```





# Reduction 4: Idle Thread

