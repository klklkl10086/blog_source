# Knowledge Extraction Plan

This plan designs the future `knowledge-base` repository only. It does not create knowledge notes, move posts, or rewrite blog history.

## Future Knowledge Repository Structure

```text
knowledge-base/
├── 00_Inbox/
├── 01_Maps/
├── 02_Concepts/
├── 03_Sources/
├── 04_Projects/
├── 05_Experiments/
├── 06_Questions/
└── 90_Blog_Drafts/
```

## First-Batch Migration Principle

Prioritize knowledge with long-term compounding value. Do not start with screenshot-heavy course review notes, contest logs, or journals. The first batch should focus on AI Infra, LLM, CUDA, C++ Systems, and Systems fundamentals.

## First-Batch Articles And Concept Splits

### cuda programming intro

Source: `source/_posts/cuda编程入门.md`. Reason: the largest and most complete GPU/CUDA spine.

Concept Notes: GPU Architecture, SM and CUDA Core, CUDA Compilation Pipeline, CUDA Kernel Function, CUDA Thread Model, Grid Block Thread Indexing, Warp, CUDA Memory Hierarchy, Shared Memory, Global Memory Coalescing, Bank Conflict, CUDA Occupancy, CUDA Error Handling.

### Reduction

Source: `source/_posts/Reduction-规约.md`. Reason: already an optimization experiment article.

Concept Notes: Parallel Reduction, Reduction with Global Memory, Reduction with Shared Memory, Warp Divergence, Bank Conflict, Thread Coarsening, Tree Reduction, CUDA Benchmarking.

### KV Cache

Source: `source/_posts/kv_cache.md`. Reason: core LLM inference topic.

Concept Notes: KV Cache, Autoregressive Decoding, Continuous Batching, PagedAttention, Prefix Cache, Rolling KV Cache, KV Cache Memory Fragmentation, LLM Inference Scheduling.

### Transformer from scratch

Source: `source/_posts/从0实现LLM.md`. Reason: project-style implementation article.

Concept Notes: Transformer from Scratch, Tokenization Pipeline, Dataset Windowing, Embedding Layer, Positional Encoding, Self-Attention Implementation, Causal Mask, Language Modeling Loss, Training Loop, Model Checkpoint.

### RAG basics

Source: `source/_posts/RAG初步.md`. Reason: seed for Agent/RAG knowledge flow.

Concept Notes: RAG Pipeline, Document Parsing, Chunking Strategy, Embedding Retrieval, Vector Index, Retrieval Evaluation, Generation with Context.

### Post-Training and Fine-Tuning

Source: `source/_posts/Post-Training.md`. Reason: should be separated from infra and placed in LLM algorithm/application knowledge.

Concept Notes: Supervised Fine-Tuning, Instruction Dataset, Fine-Tuning Objective, Post-Training, Evaluation after Fine-Tuning.

### Flash Attention

Source: `source/_posts/Flash-Attention.md`. Reason: thin current content, but key AI Infra topic.

Concept Notes: FlashAttention, IO-Aware Attention, Tiled Attention, Online Softmax, Attention Kernel Memory Access.

### SGEMM

Source: `source/_posts/Sgemm单精度矩阵乘法.md`. Reason: GEMM is central to GPU kernel work.

Concept Notes: SGEMM, Matrix Multiplication Kernel, Tiling, Shared Memory GEMM, Register Blocking, Tensor Core GEMM.

### Linux environment programming

Source: `source/_posts/Linux环境编程.md`. Reason: C++ and Systems foundation.

Concept Notes: GCC Compilation Pipeline, Static Linking and Dynamic Linking, Process Model, Fork and Exec, File Descriptor, Pipe, Signal, pthread, Mutex and Condition Variable, IO Multiplexing.

### C++ network programming

Source: `source/_posts/CPP网络编程基础.md`. Reason: bridge between C++, Linux, and networking.

Concept Notes: Socket API, TCP Server Lifecycle, Network Byte Order, Blocking IO, TCP Connection State, UDP Socket, File IO in Linux.

### C++11 features

Source: `source/_posts/cpp11新特性.md`. Reason: large survey that should be split.

Concept Notes: Lvalue and Rvalue, Move Semantics, Perfect Forwarding, Lambda Expression, auto Type Deduction, nullptr, Smart Pointer, Function Object, Variadic Template.

### C++ threading

Source: `source/_posts/cpp11-多线程.md`. Reason: focused concurrency material.

Concept Notes: std::thread, join and detach, std::mutex, Deadlock, std::lock_guard, std::unique_lock, std::call_once.

### C++ training notes

Source: `source/_posts/训练营c++知识.md`. Reason: mixed article that should be split before publication reuse.

Concept Notes: C++ Memory Layout, Pointer and Reference Pitfalls, STL Container Selection, Iterator Invalidation, Template Basics, RAII, Tensor Broadcasting.

### Computer networking

Source: `source/_posts/计算机网络.md`. Reason: Systems Map networking spine.

Concept Notes: Network Layering, HTTP, DNS, TCP Reliability, Congestion Control, Routing, NAT, Network Delay and Throughput.

### Data structures

Source: `source/_posts/数据结构.md`. Reason: Algorithm Map foundation.

Concept Notes: Linear List, Stack and Queue, Binary Tree, Heap, Graph Representation, Graph Traversal, Union Find, Hash Table.

### Machine learning course note

Source: `source/_posts/机器学习B.md`. Reason: traditional ML foundation.

Concept Notes: Linear Regression, Logistic Regression, Bias Variance, Regularization, Decision Tree, SVM, Clustering, Model Evaluation.

## Not In First Batch

Freeze or archive first: `Linux安装教程.md`, `Database.md`, `Python.md`, `java基础.md`, `前端-html5-css.md`, `cf.md`, `蓝桥杯.md`, `实习日志.md`, `微积分A3.md`.
