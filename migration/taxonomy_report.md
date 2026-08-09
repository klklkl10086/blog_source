# Taxonomy Report

## Current Categories

- `class`: 7
- `AI Infra`: 6
- `CPP开发`: 3
- `研究生补完`: 3
- `算法`: 3
- `Agent`: 1
- `Agent开发`: 1
- `CPP`: 1
- `Python`: 1
- `["AI Infra"]`: 1
- `前端`: 1
- `后端开发`: 1
- `大模型算法`: 1

## Current Tags

- `CPP`: 9
- `LLM`: 5
- `CUDA`: 4
- `Linux`: 3
- `Agent`: 1
- `FastAPI`: 1
- `Fine-Tuning`: 1
- `JavaScript`: 1
- `Machine Learning`: 1
- `Post-Traning`: 1
- `Python`: 1
- `Pytorch`: 1
- `RAG`: 1
- `SQL`: 1
- `Transformer`: 1
- `codeforces`: 1
- `css`: 1
- `html5`: 1
- `javaSE`: 1
- `thread`: 1
- `实习`: 1
- `微积分`: 1
- `微调`: 1
- `操作系统`: 1
- `数据结构`: 1
- `深度学习`: 1
- `算法`: 1
- `蓝桥杯`: 1
- `质因数分解`: 1
- `题解`: 1

## Problems

### 1. Duplicate or overlapping categories

- `AI Infra` and `大模型算法` are both LLM-related but represent different dimensions: infrastructure vs model algorithm/training.
- `Agent` and `Agent开发` are close in meaning but inconsistent in granularity.
- `CPP` and `CPP开发` both exist.
- `class` and `研究生补完` describe source/status rather than domain.
- `Python`, `前端`, and `后端开发` are technology/domain labels mixed with source labels such as `class`.

### 2. Tag semantics are mixed

- `CPP` appears as both category and tag.
- `LLM` crosses AI Infra, graduate catch-up, model algorithm and Agent categories.
- `Post-Traning` is likely a spelling issue; normalize to `Post-Training`.
- `Machine Learning` uses English while most labels use Chinese or abbreviations.
- `Sgemm单精度矩阵乘法.md` has category parsed as the literal string `["AI Infra"]`, which suggests a local front matter format issue.

### 3. Domain, type and status are mixed

The same category level currently contains domain labels, content source labels, study-stage labels and application-direction labels. This makes future migration decisions ambiguous.

## Proposed Three-Dimension Scheme

### domain

Candidate values: `ai-infra`, `llm-algorithm`, `agent`, `cpp`, `systems`, `networking`, `algorithm`, `machine-learning`, `database`, `backend`, `frontend`, `python`, `java`, `math`.

### type

Candidate values: `concept`, `tutorial`, `experiment`, `project`, `paper-note`, `course-note`, `collection`, `journal`.

### status

Candidate values: `active`, `frozen`, `draft`, `archive`, `extracting`.

## Mapping Suggestions

- `AI Infra` -> domain: `ai-infra`
- `大模型算法` -> domain: `llm-algorithm`
- `Agent` / `Agent开发` -> domain: `agent`; type should be article-specific
- `CPP` / `CPP开发` -> domain: `cpp`
- `class` -> type: `course-note`; most should use status `frozen`
- `研究生补完` -> status or source metadata, not category
- `算法` -> domain: `algorithm`
- `前端` -> domain: `frontend`
- `后端开发` -> domain: `backend`

## Blog Repository Recommendation

Keep existing categories/tags in published posts for now to avoid breaking category pages, tag pages and theme behavior. For new posts, introduce clearer metadata only after theme compatibility is verified.
