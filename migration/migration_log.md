# Migration Log

Generated on 2026-08-09.

## Created Directories

- `knowledge-base/00_Inbox/`
- `knowledge-base/01_Maps/`
- `knowledge-base/02_Concepts/`
- `knowledge-base/03_Sources/`
- `knowledge-base/04_Projects/`
- `knowledge-base/05_Experiments/`
- `knowledge-base/06_Questions/`
- `knowledge-base/90_Blog_Drafts/`

## Created Files

- `knowledge-base/02_Concepts/CUDA Thread Model.md`
- `knowledge-base/02_Concepts/GPU Architecture.md`
- `knowledge-base/02_Concepts/CUDA Memory Hierarchy.md`
- `knowledge-base/02_Concepts/Shared Memory.md`
- `knowledge-base/02_Concepts/Global Memory Coalescing.md`
- `knowledge-base/02_Concepts/Bank Conflict.md`
- `knowledge-base/02_Concepts/Parallel Reduction.md`
- `knowledge-base/02_Concepts/SGEMM Tiling.md`
- `knowledge-base/02_Concepts/KV Cache.md`
- `knowledge-base/02_Concepts/PagedAttention.md`
- `knowledge-base/02_Concepts/Rolling KV Cache.md`
- `knowledge-base/02_Concepts/Continuous Batching.md`
- `knowledge-base/02_Concepts/FlashAttention.md`
- `knowledge-base/02_Concepts/Transformer from Scratch.md`
- `knowledge-base/02_Concepts/Tokenization Pipeline.md`
- `knowledge-base/02_Concepts/Self-Attention Implementation.md`
- `knowledge-base/02_Concepts/RAG Pipeline.md`
- `knowledge-base/02_Concepts/Supervised Fine-Tuning.md`
- `knowledge-base/02_Concepts/C++ Move Semantics.md`
- `knowledge-base/02_Concepts/C++ Thread Basics.md`
- `knowledge-base/02_Concepts/Linux File Descriptor.md`
- `knowledge-base/02_Concepts/Socket API.md`
- `knowledge-base/01_Maps/AI Infra Map.md`
- `knowledge-base/01_Maps/C++ Map.md`
- `knowledge-base/01_Maps/Systems Map.md`
- `knowledge-base/01_Maps/Algorithm Map.md`

## Source Articles Used

- `source/_posts/cuda编程入门.md`
- `source/_posts/Reduction-规约.md`
- `source/_posts/kv_cache.md`
- `source/_posts/Flash-Attention.md`
- `source/_posts/Sgemm单精度矩阵乘法.md`
- `source/_posts/从0实现LLM.md`
- `source/_posts/LLM-1-to-N.md`
- `source/_posts/RAG初步.md`
- `source/_posts/Post-Training.md`
- `source/_posts/cpp11新特性.md`
- `source/_posts/cpp11-多线程.md`
- `source/_posts/Linux环境编程.md`
- `source/_posts/CPP网络编程基础.md`

## Automatically Extracted Content

- CUDA thread hierarchy, memory hierarchy, shared memory, coalescing, bank conflict, warp-related reduction concerns.
- Reduction optimization path from global memory baseline to shared memory, divergence/bank-conflict reduction, sync reduction, unrolling and shuffle.
- KV Cache, PagedAttention, Batch Decode, token/iteration-level scheduling, and Rolling KV stub.
- Transformer-from-scratch implementation flow, tokenization pipeline, attention/module structure, LayerNorm placement notes.
- RAG stage skeleton from the existing RAG note.
- SFT/fine-tuning steps from existing Post-Training and Transformer notes.
- C++ move semantics, `std::move`, forwarding notes, thread/mutex primitives.
- Linux file descriptor and socket API basics from existing Linux/C++ network notes.

## Needs Manual Review

- SGLang: requested as P0, but no `SGLang` or `sglang` text exists in the scanned blog content. No note was created to avoid adding unsupported material.
- Rolling KV Cache: source post has only a heading; mechanism requires author review.
- FlashAttention: source post is a link-only stub; mechanism requires author review.
- SGEMM Tiling: source post is a link-only stub; tiling details require author review.
- Continuous Batching: note name comes from migration plan; source text describes Batch Decode and token/iteration scheduling but does not use the exact term.
- Source posts currently have pre-existing git changes outside this migration (`kv_cache.md`, image files, and `source/_posts/kv_cache/`); these were not modified by this migration.

## Explicit Non-Actions

- Did not modify Hexo `_config.yml`.
- Did not modify `.github/workflows/deploy.yml`.
- Did not modify `themes/`.
- Did not edit, move, delete, or rewrite `source/_posts`.
