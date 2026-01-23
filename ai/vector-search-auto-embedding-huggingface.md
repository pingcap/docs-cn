---
title: HuggingFace Embeddings
summary: Learn how to use HuggingFace embedding models in TiDB Cloud.
---

# HuggingFace Embeddings

This document describes how to use HuggingFace embedding models with [Auto Embedding](/ai/vector-search-auto-embedding-overview.md) in TiDB Cloud to perform semantic searches from text queries.

> **Note:**
>
> [Auto Embedding](/ai/vector-search-auto-embedding-overview.md) is only available on {{{ .starter }}} clusters hosted on AWS.

## Available models

HuggingFace models are available for use with the `huggingface/` prefix if you bring your own [HuggingFace Inference API](https://huggingface.co/docs/inference-providers/index) key (BYOK).

For your convenience, the following sections take several popular models as examples to show how to use them with Auto Embedding. For a full list of available models, see [HuggingFace Models](https://huggingface.co/models?library=sentence-transformers&inference_provider=hf-inference&sort=trending). Note that not all models are provided by HuggingFace Inference API or always working.

## multilingual-e5-large

- Name: `huggingface/intfloat/multilingual-e5-large`
- Dimensions: 1024
- Distance metric: Cosine, L2
- Price: Charged by HuggingFace
- Hosted by TiDB Cloud: ❌
- Bring Your Own Key: ✅
- Project home: <https://huggingface.co/intfloat/multilingual-e5-large>

Example:

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

- Name: `huggingface/BAAI/bge-m3`
- Dimensions: 1024
- Distance metric: Cosine, L2
- Price: Charged by HuggingFace
- Hosted by TiDB Cloud: ❌
- Bring Your Own Key: ✅
- Project home: <https://huggingface.co/BAAI/bge-m3>

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

- Name: `huggingface/sentence-transformers/all-MiniLM-L6-v2`
- Dimensions: 384
- Distance metric: Cosine, L2
- Price: Charged by HuggingFace
- Hosted by TiDB Cloud: ❌
- Bring Your Own Key: ✅
- Project home: <https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2>

Example:

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

- Name: `huggingface/sentence-transformers/all-mpnet-base-v2`
- Dimensions: 768
- Distance metric: Cosine, L2
- Price: Charged by HuggingFace
- Hosted by TiDB Cloud: ❌
- Bring Your Own Key: ✅
- Project home: <https://huggingface.co/sentence-transformers/all-mpnet-base-v2>

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
> HuggingFace Inference API might be not stable for this model.

- Name: `huggingface/Qwen/Qwen3-Embedding-0.6B`
- Dimensions: 1024
- Distance metric: Cosine, L2
- Maximum input text tokens: 512
- Price: Charged by HuggingFace
- Hosted by TiDB Cloud: ❌
- Bring Your Own Key: ✅
- Project home: <https://huggingface.co/Qwen/Qwen3-Embedding-0.6B>

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

## Python usage example

See [PyTiDB Documentation](https://pingcap.github.io/ai/guides/auto-embedding/).

## See also

- [Auto Embedding Overview](/ai/vector-search-auto-embedding-overview.md)
- [Vector Search](/ai/vector-search-overview.md)
- [Vector Functions and Operators](/ai/vector-search-functions-and-operators.md)
- [Hybrid Search](/ai/vector-search-hybrid-search.md)
