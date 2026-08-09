# Knowledge Map

Principle: do not copy Hexo categories. Organize by stable knowledge domains and concept dependency.

## AI Infra Map

### GPU
What it is: GPU architecture, SMs, warps, memory hierarchy, and execution model. Why here: AI Infra performance starts at hardware execution and memory behavior. Related posts: `cuda编程入门.md`, `CUDA调优.md`, `Reduction-规约.md`, `Sgemm单精度矩阵乘法.md`.

### Kernel
What it is: CUDA kernels, reduction, matrix multiplication, and memory optimization. Why here: kernels are the smallest performance unit behind training and inference operators. Related posts: `Reduction-规约.md`, `Sgemm单精度矩阵乘法.md`, `cuda编程入门.md`.

### Transformer
What it is: attention, tokenization, decoder-only models, training and inference basics. Why here: Transformer semantics explain many infra optimization decisions. Related posts: `从0实现LLM.md`, `kv_cache.md`, `Flash-Attention.md`, `LLM-1-to-N.md`.

### Inference Runtime
What it is: KV Cache, PagedAttention, batching, prefill/decode, scheduling. Why here: inference systems are dominated by memory management, throughput and latency tradeoffs. Related posts: `kv_cache.md`, `Flash-Attention.md`, `从0实现LLM.md`.

### Serving
What it is: model service APIs, RAG service flow, backend entrypoints and deployment. Why here: AI Infra includes serving, not only kernels. Related posts: `FastAPI.md`, `RAG初步.md`, `Post-Training.md`.

### Distributed
What it is: future multi-GPU, distributed training/inference, communication and scheduling. Why here: not mature in the current blog yet, but it is a stable top-level AI Infra branch. Related posts: none mature yet.

## C++ Map

### Modern C++
What it is: C++11 and later language features and idioms. Why here: common language foundation for systems code, CUDA host code and high-performance services. Related posts: `cpp11新特性.md`, `Effective-C-plus-plus.md`, `泛型编程.md`.

### Concurrency
What it is: thread, mutex, locks, call_once and concurrency risks. Why here: core capability for systems and services. Related posts: `cpp11-多线程.md`, `Linux环境编程.md`.

### STL and Generic Programming
What it is: containers, iterators, templates and generic abstractions. Why here: main expression layer for C++ engineering. Related posts: `训练营c++知识.md`, `泛型编程.md`, `cpp11新特性.md`.

### C++ Systems Programming
What it is: compilation/linking, file descriptors, processes, threads, sockets and Linux APIs. Why here: bridge from language to systems engineering. Related posts: `Linux环境编程.md`, `CPP网络编程基础.md`, `操作系统实验.md`.

## Agent Map

### API Layer
What it is: FastAPI, HTTP endpoints and service entrypoints. Why here: Agent/RAG systems need a stable interface layer. Related posts: `FastAPI.md`, `RAG初步.md`.

### RAG Pipeline
What it is: parsing, chunking, embeddings, retrieval and context generation. Why here: RAG connects knowledge bases to LLM applications. Related posts: `RAG初步.md`.

### Tool and Workflow Orchestration
What it is: future tool calling, planning and state management. Why here: the current blog is starting this direction but lacks structure. Related posts: `FastAPI.md`, `RAG初步.md`.

### Post-Training for Agents
What it is: SFT, fine-tuning data, task adaptation and evaluation. Why here: Agent behavior depends on model shaping as well as orchestration. Related posts: `Post-Training.md`.

## Algorithm Map

### Data Structures
What it is: lists, trees, graphs, heaps, union-find and hashes. Why here: foundation for algorithmic thinking. Related posts: `数据结构.md`, `算法基础.md`.

### Competitive Programming Patterns
What it is: binary search, prefix sums, difference arrays, recursion, number theory and solution patterns. Why here: contest practice is problem-solving pattern knowledge, not the same as domain taxonomy. Related posts: `算法基础.md`, `蓝桥杯.md`, `cf.md`.

### Graph Algorithms
What it is: graph representation, traversal, shortest paths and topological sorting. Why here: graph knowledge connects algorithms, networks and systems. Related posts: `数据结构.md`, `算法基础.md`.

### Numerical and Math Basics
What it is: high precision arithmetic, calculus and basic math tools. Why here: supports algorithms and ML without being a blog status. Related posts: `算法基础.md`, `微积分A3.md`.

## Systems Map

### Operating System
What it is: processes, threads, synchronization, filesystem and labs. Why here: OS knowledge supports C++ services, networking and AI Infra. Related posts: `操作系统实验.md`, `Linux环境编程.md`, `Linux安装教程.md`.

### Linux Programming
What it is: gcc/g++, linking, file descriptors, pipes, signals and pthreads. Why here: Linux API is the practical surface of systems engineering. Related posts: `Linux环境编程.md`, `CPP网络编程基础.md`.

### Networking
What it is: layering, HTTP, DNS, TCP/UDP, routing and congestion control. Why here: foundation for backend, Agent APIs and distributed systems. Related posts: `计算机网络.md`, `CPP网络编程基础.md`.

### Database
What it is: SQL, relational model, constraints, queries and transactions. Why here: database is part of application infrastructure. Related posts: `Database.md`.

### Backend Basics
What it is: Java, Python, FastAPI and Web/API fundamentals. Why here: application development layer, separate from low-level systems. Related posts: `java基础.md`, `Python.md`, `FastAPI.md`, `前端-html5-css.md`.
