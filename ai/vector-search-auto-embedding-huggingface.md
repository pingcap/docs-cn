---
title: HuggingFace Embeddings
summary: 了解如何在 TiDB Cloud 中使用 HuggingFace 嵌入模型。
---

# HuggingFace Embeddings <!-- Draft translated by AI -->

本文档介绍如何在 TiDB Cloud 中结合 [Auto Embedding](/ai/vector-search-auto-embedding-overview.md) 使用 HuggingFace 嵌入模型，从文本查询中执行语义搜索。

> **Note:**
>
> [Auto Embedding](/ai/vector-search-auto-embedding-overview.md) 仅在托管于 AWS 的 TiDB Cloud Starter 集群上可用。

## 可用模型

如果你自带 [HuggingFace Inference API](https://huggingface.co/docs/inference-providers/index) 密钥（BYOK），则可以通过 `huggingface/` 前缀使用 HuggingFace 模型。

为方便起见，以下章节以几个流行模型为例，展示如何结合 Auto Embedding 使用它们。完整可用模型列表请参见 [HuggingFace Models](https://huggingface.co/models?library=sentence-transformers&inference_provider=hf-inference&sort=trending)。请注意，并非所有模型都由 HuggingFace Inference API 提供，或始终可用。

## multilingual-e5-large

- 名称: `huggingface/intfloat/multilingual-e5-large`
- 维度: 1024
- 距离度量: Cosine, L2
- 价格: 由 HuggingFace 收费
- TiDB Cloud 托管: ❌
- 支持自带密钥: ✅
- 项目主页: <https://huggingface.co/intfloat/multilingual-e5-large>

示例：

```sql
SET @@GLOBAL.TIDB_EXP_EMBED_HUGGINGFACE_API_KEY = 'your-huggingface-api-key-here';

CREATE TABLE sample (
  `id`        INT,
  `content`   TEXT,
  `embedding` VECTOR(1024) GENERATED ALWAYS AS (EMBED_TEXT(
                "huggingface/intfloat/multilingual-e5-large",
                `content`
              )) STORED
);


INSERT INTO sample
    (`id`, `content`)
VALUES
    (1, "Java: Object-oriented language for cross-platform development."),
    (2, "Java coffee: Bold Indonesian beans with low acidity."),
    (3, "Java island: Densely populated, home to Jakarta."),
    (4, "Java's syntax is used in Android apps."),
    (5, "Dark roast Java beans enhance espresso blends.");


SELECT `id`, `content` FROM sample
ORDER BY
  VEC_EMBED_COSINE_DISTANCE(
    embedding,
    "How to start learning Java programming?"
  )
LIMIT 2;
```

## bge-m3

- 名称: `huggingface/BAAI/bge-m3`
- 维度: 1024
- 距离度量: Cosine, L2
- 价格: 由 HuggingFace 收费
- TiDB Cloud 托管: ❌
- 支持自带密钥: ✅
- 项目主页: <https://huggingface.co/BAAI/bge-m3>

```sql
SET @@GLOBAL.TIDB_EXP_EMBED_HUGGINGFACE_API_KEY = 'your-huggingface-api-key-here';

CREATE TABLE sample (
  `id`        INT,
  `content`   TEXT,
  `embedding` VECTOR(1024) GENERATED ALWAYS AS (EMBED_TEXT(
                "huggingface/BAAI/bge-m3",
                `content`
              )) STORED
);


INSERT INTO sample
    (`id`, `content`)
VALUES
    (1, "Java: Object-oriented language for cross-platform development."),
    (2, "Java coffee: Bold Indonesian beans with low acidity."),
    (3, "Java island: Densely populated, home to Jakarta."),
    (4, "Java's syntax is used in Android apps."),
    (5, "Dark roast Java beans enhance espresso blends.");


SELECT `id`, `content` FROM sample
ORDER BY
  VEC_EMBED_COSINE_DISTANCE(
    embedding,
    "How to start learning Java programming?"
  )
LIMIT 2;
```

## all-MiniLM-L6-v2

- 名称: `huggingface/sentence-transformers/all-MiniLM-L6-v2`
- 维度: 384
- 距离度量: Cosine, L2
- 价格: 由 HuggingFace 收费
- TiDB Cloud 托管: ❌
- 支持自带密钥: ✅
- 项目主页: <https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2>

示例：

```sql
SET @@GLOBAL.TIDB_EXP_EMBED_HUGGINGFACE_API_KEY = 'your-huggingface-api-key-here';

CREATE TABLE sample (
  `id`        INT,
  `content`   TEXT,
  `embedding` VECTOR(384) GENERATED ALWAYS AS (EMBED_TEXT(
                "huggingface/sentence-transformers/all-MiniLM-L6-v2",
                `content`
              )) STORED
);


INSERT INTO sample
    (`id`, `content`)
VALUES
    (1, "Java: Object-oriented language for cross-platform development."),
    (2, "Java coffee: Bold Indonesian beans with low acidity."),
    (3, "Java island: Densely populated, home to Jakarta."),
    (4, "Java's syntax is used in Android apps."),
    (5, "Dark roast Java beans enhance espresso blends.");


SELECT `id`, `content` FROM sample
ORDER BY
  VEC_EMBED_COSINE_DISTANCE(
    embedding,
    "How to start learning Java programming?"
  )
LIMIT 2;
```

## all-mpnet-base-v2

- 名称: `huggingface/sentence-transformers/all-mpnet-base-v2`
- 维度: 768
- 距离度量: Cosine, L2
- 价格: 由 HuggingFace 收费
- TiDB Cloud 托管: ❌
- 支持自带密钥: ✅
- 项目主页: <https://huggingface.co/sentence-transformers/all-mpnet-base-v2>

```sql
SET @@GLOBAL.TIDB_EXP_EMBED_HUGGINGFACE_API_KEY = 'your-huggingface-api-key-here';

CREATE TABLE sample (
  `id`        INT,
  `content`   TEXT,
  `embedding` VECTOR(768) GENERATED ALWAYS AS (EMBED_TEXT(
                "huggingface/sentence-transformers/all-mpnet-base-v2",
                `content`
              )) STORED
);


INSERT INTO sample
    (`id`, `content`)
VALUES
    (1, "Java: Object-oriented language for cross-platform development."),
    (2, "Java coffee: Bold Indonesian beans with low acidity."),
    (3, "Java island: Densely populated, home to Jakarta."),
    (4, "Java's syntax is used in Android apps."),
    (5, "Dark roast Java beans enhance espresso blends.");


SELECT `id`, `content` FROM sample
ORDER BY
  VEC_EMBED_COSINE_DISTANCE(
    embedding,
    "How to start learning Java programming?"
  )
LIMIT 2;
```

## Qwen3-Embedding-0.6B

> **Note:**
>
> HuggingFace Inference API 对该模型可能不稳定。

- 名称: `huggingface/Qwen/Qwen3-Embedding-0.6B`
- 维度: 1024
- 距离度量: Cosine, L2
- 最大输入文本 tokens 数: 512
- 价格: 由 HuggingFace 收费
- TiDB Cloud 托管: ❌
- 支持自带密钥: ✅
- 项目主页: <https://huggingface.co/Qwen/Qwen3-Embedding-0.6B>

```sql
SET @@GLOBAL.TIDB_EXP_EMBED_HUGGINGFACE_API_KEY = 'your-huggingface-api-key-here';

CREATE TABLE sample (
  `id`        INT,
  `content`   TEXT,
  `embedding` VECTOR(1024) GENERATED ALWAYS AS (EMBED_TEXT(
                "huggingface/Qwen/Qwen3-Embedding-0.6B",
                `content`
              )) STORED
);


INSERT INTO sample
    (`id`, `content`)
VALUES
    (1, "Java: Object-oriented language for cross-platform development."),
    (2, "Java coffee: Bold Indonesian beans with low acidity."),
    (3, "Java island: Densely populated, home to Jakarta."),
    (4, "Java's syntax is used in Android apps."),
    (5, "Dark roast Java beans enhance espresso blends.");


SELECT `id`, `content` FROM sample
ORDER BY
  VEC_EMBED_COSINE_DISTANCE(
    embedding,
    "How to start learning Java programming?"
  )
LIMIT 2;
```

## Python 使用示例

参见 [PyTiDB Documentation](https://pingcap.github.io/ai/guides/auto-embedding/)。

## 参见

- [Auto Embedding 概览](/ai/vector-search-auto-embedding-overview.md)
- [向量检索](/vector-search/vector-search-overview.md)
- [向量函数与操作符](/vector-search/vector-search-functions-and-operators.md)
- [混合检索](/ai/vector-search-hybrid-search.md)
