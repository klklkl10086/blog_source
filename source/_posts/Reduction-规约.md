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



# Reduction 0: Global Memory

## 思考路径

![Capture_20260406_200922](Capture_20260406_200922-1775477401521-2.jpg)



```cpp
/*
baseline:global memory
*/


#include <stdio.h>
#include <stdlib.h>
const int ThreadPerBlock = 256;

const int N = 32*1024*1024;

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

### Warp Divergence

```cpp
if(threadIdx.x%(len*2)==0)//len*2是步长
{
	a[tidx]+=a[tidx+len];
}
```

**同一个Wrap中只有部分并且分散的线程在工作     ----------->      考虑换成集中的一部分线程工作**



### 合并访问

> 在硬件层面，GPU 访问全局内存不是一个字节一个字节读的，而是**按块（Transaction）读取**的（通常是 32 字节或 128 字节的内存段）。当一个 Warp 的 32 个线程发起内存读取请求时，硬件会检查这 32 个地址。如果这些地址正好落在一个或两个连续的内存段内，硬件就会把它们**合并（Coalesce）**成 1 到 2 次内存事务（Memory Transaction）。

```cpp
if(threadIdx.x%(len*2)==0)//len*2是步长
{
	a[tidx]+=a[tidx+len];
}
```

**当len==1的时，会发现一个线程束的访存是间隔的，一次访存事务只有一半的数据有用。**



# Reduction 1: Shared Memory
