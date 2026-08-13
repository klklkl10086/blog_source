---
type: source
status: extracted
domain:
  - ai-infra
  - cuda
source:
  - gpu-mode
created: 2026-08-13
---

# Lesson01-How to profile CUDA kernel in pytorch

## Extracted Concepts

- [[CUDA Kernel Profiling]]
- [[PyTorch Profiler]]
- [[Nsight Systems]]
- [[Nsight Compute]]
- [[CUDA Kernel Launch Overhead]]
- [[Operator Fusion]]
- [[Streaming Multiprocessor]]
- [[GPU Occupancy]]
- [[CUDA Memory Hierarchy]]
- [[Shared Memory]]
- [[SGEMM Tiling]]


```
                GPU MODE Lesson 1
                       │
          ┌────────────┴────────────┐
          │                         │
      Profiling                Custom Kernel
          │                         │
   ┌──────┼──────┐          ┌──────┼──────┐
   │      │      │          │      │      │
torch   nsys    ncu        CUDA   Triton  Numba
profiler
   │
   ↓
发现慢的 kernel
          │
          ↓
理解 kernel 为什么慢
          │
          ↓
自己写 / 修改 kernel
          │
          ↓
接回 PyTorch
          │
          ↓
再次 profile
```


## profiler

```
PyTorch Profiler
      ↓
哪个 PyTorch op / CUDA kernel 慢？

Nsight Systems (nsys)
      ↓
CPU 和 GPU 在时间轴上如何调度？
kernel 之间有没有空洞？
launch 是否太频繁？

Nsight Compute (ncu)
      ↓
某一个 kernel 为什么慢？
memory？
compute？
occupancy？
instructions？
```


```
Python
   ↓
PyTorch
   ↓
CUDA runtime
   ↓
CUDA kernel
   ↓
PTX
   ↓
SASS
   ↓
GPU hardware
```




# Lesson04 Compute and Memory basics
FP 64很慢,因为相关的硬件比较少

## GPU结构
现代 GPU 看成一台“**由大量 SM 组成、围绕数据吞吐设计的并行计算机器**”。


```
                    Modern NVIDIA GPU
                           │
                  ┌────────┴────────┐
                  │     GPCs        │
                  │                 │
               many SMs          many SMs
                  │
     ┌────────────┼───────────────────────┐
     │            │                       │
 Warp Scheduler   Register File      Shared / L1
     │            │                       │
     ↓            └────────┬──────────────┘
 instruction               │
     │                      │ data
     ├───────────┬──────────┼───────────┐
     ↓           ↓          ↓           ↓
 CUDA Core   Tensor Core   LD/ST       SFU
     │           │          │
     │         MMA          │
     └───────────┴──────────┘
                 │
                 ↓
                L2
                 │
                 ↓
          Memory Controller
                 │
                 ↓
               HBM
```

```
                        CPU
                         │
                    PCIe / NVLink
                         │
┌────────────────────────GPU──────────────────────────┐
│                                                     │
│   ┌──────── GPC ────────┐   ┌──────── GPC ───────┐ │
│   │                     │   │                    │ │
│   │   ┌──── SM ────┐    │   │   ┌──── SM ────┐   │ │
│   │   │ Warp sched │    │   │   │ Warp sched │   │ │
│   │   │ Registers  │    │   │   │ Registers  │   │ │
│   │   │ CUDA Core  │    │   │   │ CUDA Core  │   │ │
│   │   │ Tensor Core│    │   │   │ Tensor Core│   │ │
│   │   │ LD/ST      │    │   │   │ LD/ST      │   │ │
│   │   │ SFU        │    │   │   │ SFU        │   │ │
│   │   │ L1/Shared  │    │   │   │ L1/Shared  │   │ │
│   │   └────────────┘    │   │   └────────────┘   │ │
│   │        ...          │   │        ...         │ │
│   └─────────────────────┘   └────────────────────┘ │
│                  │                │                 │
│                  └───────┬────────┘                 │
│                          ↓                          │
│                      L2 Cache                      │
│                          ↓                          │
│              Memory Controllers / NoC              │
│                          ↓                          │
│                     HBM / GDDR                     │
└─────────────────────────────────────────────────────┘
```

- GPU 由多个 Streaming Multiprocessor（SM）组成，SM 再组织到 Graphics Processing Cluster（GPC）等更高层级；
- 每个 SM 内部包含寄存器、统一 L1/Shared Memory、warp 调度器以及多种执行单元。
- L2 Cache：整颗 GPU 的共享缓存，承担跨 SM 数据复用等任务
- HBM / GDDR：GPU 的大容量主存 
![image-1786589951716.png](image-1786589951716.png)

```
register      最快
shared/L1     片上
local         地址空间在显存，缓存命中时可由 L1/L2 服务
global        地址空间在显存，缓存命中时可由 L1/L2 服务
```

### SM
![image-1786588958554.png](image-1786588958554.png)
- CUDA runtime 会把 thread block 分配给不同 SM。
- 一个 block 一旦被调度到某个 SM，其线程就在该 SM 上执行。SM 内部提供寄存器、shared memory 和各种执行 pipeline。CUDA 官方把 GPU 编程模型明确描述成由多个 SM 并行执行 thread blocks。

> GPU性能优化的核心问题:**有没有让足够多的 SM 持续工作？**

可以想成：

```
Block
├── Warp 0 : thread   0 -  31
├── Warp 1 : thread  32 -  63
├── Warp 2 : thread  64 -  95
...
└── Warp 7 : thread 224 - 255
```

然后 SM 上可能同时 resident：

```
Block 0: 8 warps
Block 1: 8 warps
Block 2: 8 warps
Block 3: 8 warps

总计 32 个 active warps
```

SM 的调度器会不断选择“已经 ready 的 warp”发射指令。
**SM 利用大量并行 warp，在部分 warp 等待数据移动或其他依赖时运行其他 warp。**

**现代SM内部结构**：
```
┌──────────────────────────── SM ────────────────────────────┐
│                                                           │
│ Instruction Cache                                         │
│        │                                                  │
│ ┌──────▼──────┐     ┌─────────────┐                       │
│ │Warp Scheduler│ →   │ Dispatch    │                       │
│ └──────┬──────┘     └──────┬──────┘                       │
│        │                    │                              │
│        ├──────────┬─────────┼────────────┐                 │
│        ↓          ↓         ↓            ↓                 │
│   CUDA Core   Tensor     LD/ST          SFU                │
│   FP/INT      Core       units                              │
│                                                           │
│                  Register File                            │
│                       │                                   │
│                       ↓                                   │
│               L1 / Shared Memory                          │
│                       │                                   │
│                       ↓                                   │
│                       L2                                  │
└───────────────────────────────────────────────────────────┘
```

- Warp scheduler / dispatch
- Register File：高速存储，每个线程都有自己的寄存器
- CUDA Core / scalar ALU：普通标量/向量算术执行 pipeline（Register pressure）
- Tensor Core：矩阵运算
- Load/Store + memory pipeline
- Shared Memory / L1：L1 data cache 和 Shared Memory 共享一部分物理资源。Block内一起使用共享内存（Bank conflict） 

pytorch查看硬件信息：
```python
torch.cuda.get_device_properties(<gpu_num>)
```



## Pytorch programs 优化

![image-1786590794016.png](image-1786590794016.png)
常见思路：
![image-1786591021716.png](image-1786591021716.png)


### memory access as bottleneck

融合多个操作到一个操作是优化重点
尽量避免local memory

例：
自己实现gelu函数与pytorch进行对比发现速度慢7-8倍
```python
import math
import torch
import timeit
def gelu(x):
    return 0.5 * x * (1+ torch.tanh((2/torch.pi)**0.5 * (x+0.044715* x**3 )))

x = torch.randn(1024,1024,device="cuda")

diff = gelu(x)-torch.nn.functional.gelu(x,approximate='tanh')
print(diff.abs().max().item())

with torch.profiler.profile() as prof:
    gelu(x)
print(prof.key_averages().table(sort_by="cuda_time_total", row_limit=15))
```

输出：
  ![image-1786592545720.png](image-1786592545720.png)

| 列               | 含义                                  | 怎么看                                         |
| --------------- | ----------------------------------- | ------------------------------------------- |
| `Name`          | 操作名称                                | 可能是 PyTorch 算子、CUDA kernel、runtime API、同步操作 |
| `Self CPU %`    | 该操作自身 CPU 时间占全部 CPU self time 的比例   | 看 CPU 侧哪里最耗时                                |
| `Self CPU`      | 该操作自身 CPU 时间                        | **不包含它调用的子操作**                              |
| `CPU total %`   | 该操作总 CPU 时间占比                       | **包含它自身和子调用**                               |
| `CPU total`     | 该操作总 CPU 时间                         | `Self CPU + 子操作 CPU 时间`                     |
| `CPU time avg`  | 每次调用平均 CPU 总时间                      | `CPU total / # Calls`                       |
| `Self CUDA`     | 该操作自身对应的 CUDA 执行时间                  | GPU 分析时最重要的列之一                              |
| `Self CUDA %`   | 该操作自身 CUDA 时间占全部 CUDA self time 的比例 | 看哪个 GPU 操作最占时间                              |
| `CUDA total`    | 该操作及其子调用累计 CUDA 时间                  | 高层 aten op 常用                               |
| `CUDA time avg` | 每次调用平均 CUDA 时间                      | 判断 kernel 是“大 kernel”还是“小 kernel”           |
| `# of Calls`    | 调用次数                                | 判断是否存在大量碎片化的小算子                             |

```
aten::mul
aten::add
aten::tanh
aten::pow
```

这是 PyTorch 算子层。

```
void at::native::vectorized_elementwise_kernel<...>
```

是对应真正跑在 GPU 上的 CUDA kernel。

```
Python/PyTorch
    ↓
aten::mul
    ↓
cudaLaunchKernel
    ↓
vectorized_elementwise_kernel
    ↓
GPU执行
```



自己实现的Glue：
	GPU 真正计算只用了约 `17.5 μs`，CPU 侧 profiler/launch 等开销明显更大
	一共发射了 8 个 CUDA kernel，而且这些都是很小的逐元素 kernel。



RoofLine Model
[[CUDA2-性能模型与逐元素优化#Roofline模型]]


### How to use shared memeory
> `tilling`: 把一个大问题切成适合片上高速存储的小块，让每次从 HBM 搬进来的数据被重复利用很多次。


eg:
Matmul $n \times n$  
利用 tilling的思想，矩阵的一部分放入shared memory 然后进行计算重用

当无法完整的分为整数块时，需要padding


# Lesson08 CUDA Performance Checklist

