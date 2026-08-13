---
title: KV Cache
date: 2026-08-07 13:46:44
tags: ["Transformer"]
categories: ["AI Infra"]
description: kv cache发展简单总结
mathjax: true
typora-root-url: ./kv_cache
---


> 前置阅读 : [从0实现LLM](https://klklkl10086.github.io/2025/12/07/%E4%BB%8E0%E5%AE%9E%E7%8E%B0LLM/)
> 
> 相关论文：
[Efficient Memory Management for Large Language Model Serving with PagedAttention](https://arxiv.org/abs/2309.06180)

**为什么要缓存KV？**

Transformer计算分为两个阶段：
1. Prefill阶段：对输入的Prompt计算直到生成第一个Token，这段时间被称为TTFT。
2. Decode阶段（自回归生成阶段）：生成的首Token和一开始的Prompt合并，作为新的输入再次计算，循环往复，直到达到max token或者生成结束符号。

从上述过程，我们很容易可以得到：在decode阶段，会重复用到之前计算过的K、V。因此，通过缓存K、V，可以重复利用之前的计算结果，从而大大提升推理速度。

随之而来的问题是，**如何高效管理KV Cache？**

显存是一个很昂贵且稀有的空间，如何管理KV Cache才能充分利用显存空间？

# 连续内存分配
很直接的想法就是**连续、静态分配**，一个request想要缓存自己的KV内容，需要提前申请，说明自己需要多大的空间，然后我们将空间分给它。

```python
import torch

class TraditionalKVCache:
    def __init__(self, batch_size, max_seq_len, num_heads, head_dim, device):
        # 致命缺陷：必须预先静态分配最大长度（max_seq_len）的连续显存
        # 即使请求只生成了 10 个 token，这块连续大显存也会被完全占用到请求结束
        self.key_cache = torch.zeros(
            (batch_size, num_heads, max_seq_len, head_dim), device=device
        )
        self.value_cache = torch.zeros(
            (batch_size, num_heads, max_seq_len, head_dim), device=device
        )
        self.cur_seq_lens = torch.zeros(batch_size, dtype=torch.long, device=device)

    def update(self, k_new, v_new, batch_idx):
        """
        k_new, v_new: 当前步新生成的 token 的 KV，形状为 (num_heads, 1, head_dim)
        """
        seq_len = self.cur_seq_lens[batch_idx]
        
        # 连续内存写入：将新 Token 直接写入对应连续显存的下一个位置
        self.key_cache[batch_idx, :, seq_len : seq_len + 1, :] = k_new
        self.value_cache[batch_idx, :, seq_len : seq_len + 1, :] = v_new
        
        # 更新当前序列长度指针
        self.cur_seq_lens[batch_idx] += 1
        
        # 传给 Attention 计算时，直接切片取用从 0 到当前实际长度的连续段
        return (
            self.key_cache[batch_idx, :, :seq_len + 1, :],
            self.value_cache[batch_idx, :, :seq_len + 1, :]
        )
```



这个想法很顺理成章，如果你想用公共空间，那就预约，给出你要用的大小和时间，我们就可以很好的进行安排。但是KV内容无法做到确定性，它是不确定大小(与生成长度相关)、不确定生命周期的存在。因此，这种死板的分配管理方式很容易造成大量的碎片，无论是内部还是外部。

如果学过操作系统，很容易会联想到操作系统对内存空间的管理发展史


# Paged Attention


现有管理方式缺点：
1. 存在内部和外部碎片，没有充分利用显存空间
2. 无法共享，一些复杂的解码策略如：Beam search 可以共享kv cache，但是这种静态的连续的内存管理方式没有办法实现KV cache的共享。
3. 上面两点导致推理速度受显存空间的约束，简单粗放的管理方式限制了**batch decode**并行的数
目。


### Batch Decode
> Batch Decode 的核心思想是“拼车”。系统同时收集 $N$ 个请求当前生成的 Token，组成一个 Batch（形状为 [N, 1]），然后一次性喂给模型。这样，底层计算就从矩阵-向量乘法（GEMV）变成了矩阵-矩阵乘法（GEMM）。模型权重只需要从显存搬运一次，就可以同时对这 $N$ 个 Token 进行计算。这极大地提高了“算术强度（Arithmetic Intensity，即每次显存读取对应的计算量）”，将算力利用率提升到了较高水平。


```python
import torch
import torch.nn.functional as F

class SimpleBatchedLLM:
    def __init__(self, vocab_size, hidden_dim, num_heads):
        self.vocab_size = vocab_size
        self.hidden_dim = hidden_dim
        self.num_heads = num_heads
        self.head_dim = hidden_dim // num_heads
        
        # 简化的线性层权重模拟
        self.q_proj = torch.nn.Linear(hidden_dim, hidden_dim)
        self.k_proj = torch.nn.Linear(hidden_dim, hidden_dim)
        self.v_proj = torch.nn.Linear(hidden_dim, hidden_dim)
        self.o_proj = torch.nn.Linear(hidden_dim, hidden_dim)
        self.lm_head = torch.nn.Linear(hidden_dim, vocab_size)

    def batch_decode_step(self, current_tokens_embeds, batch_kv_cache):
        """
        执行单步 Batch Decode
        :param current_tokens_embeds: 当前批次最新生成的 Token 向量，形状: [batch_size, 1, hidden_dim]
        :param batch_kv_cache: 历史 KV 缓存，包含了元组 (K_cache, V_cache)
                               K_cache 形状: [batch_size, num_heads, seq_len, head_dim]
        :return: (next_logits, updated_kv_cache)
        """
        batch_size = current_tokens_embeds.shape[0]
        K_cache, V_cache = batch_kv_cache

        # 1. 计算当前一步的 Q, K, V (基于刚刚输入的那 1 个 Token)
        # 形状均变为: [batch_size, 1, hidden_dim]
        q = self.q_proj(current_tokens_embeds)
        k_new = self.k_proj(current_tokens_embeds)
        v_new = self.v_proj(current_tokens_embeds)

        # 调整形状以适应多头注意力机制
        # 形状: [batch_size, num_heads, 1, head_dim]
        q = q.view(batch_size, 1, self.num_heads, self.head_dim).transpose(1, 2)
        k_new = k_new.view(batch_size, 1, self.num_heads, self.head_dim).transpose(1, 2)
        v_new = v_new.view(batch_size, 1, self.num_heads, self.head_dim).transpose(1, 2)

        # 2. KV Cache 更新：将当前步的新 K, V 拼接到历史 Cache 中
        # (注：在 PagedAttention 中这里是非连续块写入，此处用 torch.cat 模拟传统连续缓存)
        # 更新后形状: [batch_size, num_heads, seq_len + 1, head_dim]
        K_cache = torch.cat([K_cache, k_new], dim=2)
        V_cache = torch.cat([V_cache, v_new], dim=2)

        # 3. Batch Attention 计算
        # Q 与 完整的 K_cache 进行点积计算
        # q: [batch_size, num_heads, 1, head_dim]
        # K_cache.transpose: [batch_size, num_heads, head_dim, seq_len + 1]
        # scores 形状: [batch_size, num_heads, 1, seq_len + 1]
        scores = torch.matmul(q, K_cache.transpose(-2, -1)) / (self.head_dim ** 0.5)
        
        # Softmax 归一化注意力权重
        attn_weights = F.softmax(scores, dim=-1)

        # 权重乘以 V_cache
        # attn_weights: [batch_size, num_heads, 1, seq_len + 1]
        # V_cache: [batch_size, num_heads, seq_len + 1, head_dim]
        # context 形状: [batch_size, num_heads, 1, head_dim]
        context = torch.matmul(attn_weights, V_cache)

        # 4. 恢复形状并经过输出映射
        context = context.transpose(1, 2).contiguous().view(batch_size, 1, self.hidden_dim)
        hidden_states = self.o_proj(context)

        # 5. 生成 Logits 用于后续采样下一个词汇
        # logits 形状: [batch_size, vocab_size]
        logits = self.lm_head(hidden_states).squeeze(1)

        return logits, (K_cache, V_cache)

# --- 模拟执行调度 ---
def simulate_continuous_batching():
    batch_size = 4
    hidden_dim = 128
    num_heads = 4
    seq_len = 10 # 假设之前已经生成了 10 个 token
    
    model = SimpleBatchedLLM(vocab_size=10000, hidden_dim=hidden_dim, num_heads=num_heads)
    
    # 模拟上一步刚生成的 4 个请求的新 Token 的 Embeddings
    current_tokens = torch.randn(batch_size, 1, hidden_dim)
    
    # 模拟这 4 个请求的历史 KV Cache (已经有 10 个 token)
    k_cache_hist = torch.randn(batch_size, num_heads, seq_len, hidden_dim // num_heads)
    v_cache_hist = torch.randn(batch_size, num_heads, seq_len, hidden_dim // num_heads)
    
    # 执行单步 Batch Decode
    logits, updated_kv = model.batch_decode_step(
        current_tokens_embeds=current_tokens, 
        batch_kv_cache=(k_cache_hist, v_cache_hist)
    )
    
    # 采样获取下方的 token ids (此处取 argmax 简化)
    next_token_ids = torch.argmax(logits, dim=-1)
    
    print(f"输入 Batch 形状: {current_tokens.shape}")
    print(f"输出 Logits 形状: {logits.shape}")
    print(f"生成的下一个 Token IDs: {next_token_ids.tolist()}")
    print(f"更新后的 KV Cache 长度: {updated_kv[0].shape[2]}") # 预期变为 11

simulate_continuous_batching()
```


decode阶段的瓶颈在于访存速度，一个解决方式就是一次访存多次计算来均摊成本，但是在合并多个请求计算时，有以下问题：
1. 每个请求需要的生成长度长短不一，如果一起进行计算，就要进行填充，会浪费GPU的计算资源。
2. 不同的请求到达时间不同，最简单的解决方式就是等待，攒够一定数目的请求再进行计算，但是这样会让先来的等待时间很长。
   

其实有一个解决方式是降低粒度，即我们不再根据请求进行调度，而是根据一次迭代，或者说一个token的生成为最小单位进行调度。但是这种方式依旧存在很多问题：
1. 批处理带来了巨大的KV Cache开销，如何高效管理显存
2. decode具有不同的算法，对显存管理造成了困难
3. 无法确定输入和输出的长度，无法进行准确、高效的调度

----

**解决方式**：向计算机操作系统中的虚拟内存学习，采用虚拟内存的思想，将显存空间分为大小相等的块，给每个请求分若干个块，这样就解决了外部碎片的问题，每个请求的显存分配情况通过块表进行记录、管理，通过更改块表可以轻松实现KV Cache块的共享。

## 思想
![PagedAttention algorithm](./image.png)

![PagedAttention algorithm example](./image-2.png)

学过OS就很容易理解了，块表的作用就是把KV块的逻辑号映射到真实的存储地址，这样就可以实现逻辑上连续但是物理上不连续了。


# Rolling KV Cache

