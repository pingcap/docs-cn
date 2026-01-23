---
title: Jina AI Embeddings
summary: Learn how to use Jina AI embedding models in TiDB Cloud.
---

# Jina AI Embeddings

This document describes how to use Jina AI embedding models with [Auto Embedding](/ai/vector-search-auto-embedding-overview.md) in TiDB Cloud to perform semantic searches from text queries.

> **Note:**
>
> [Auto Embedding](/ai/vector-search-auto-embedding-overview.md) is only available on {{{ .starter }}} clusters hosted on AWS.

## Available models

All Jina AI models are available for use with the `jina_ai/` prefix if you bring your own Jina AI API key (BYOK). For example:

**jina-embeddings-v4**

- Name: `jina_ai/jina-embeddings-v4`
- Dimensions: 2048
- Distance metric: Cosine, L2
- Maximum input text tokens: 32,768
- Price: Charged by Jina AI
- Hosted by TiDB Cloud: ❌
- Bring Your Own Key: ✅

**jina-embeddings-v3**

- Name: `jina_ai/jina-embeddings-v3`
- Dimensions: 1024
- Distance metric: Cosine, L2
- Maximum input text tokens: 8,192
- Price: Charged by Jina AI
- Hosted by TiDB Cloud: ❌
- Bring Your Own Key: ✅

For a full list of available models, see [Jina AI Documentation](https://jina.ai/embeddings/).

## SQL usage example

To use Jina AI models, you must specify a [Jina AI API key](https://jina.ai/) as follows:

> **Note:**
>
> Replace `'your-jina-ai-api-key-here'` with your actual Jina AI API key.

```sql
SET @@GLOBAL.TIDB_EXP_EMBED_JINA_AI_API_KEY = 'your-jina-ai-api-key-here';

CREATE TABLE sample (
  `id`        INT,
  `content`   TEXT,
  `embedding` VECTOR(1024) GENERATED ALWAYS AS (EMBED_TEXT(
                "jina_ai/jina-embeddings-v4",
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

Result:

```
+------+----------------------------------------------------------------+
| id   | content                                                        |
+------+----------------------------------------------------------------+
|    1 | Java: Object-oriented language for cross-platform development. |
|    4 | Java's syntax is used in Android apps.                         |
+------+----------------------------------------------------------------+
```

## Options

All [Jina AI options](https://jina.ai/embeddings/) are supported via the `additional_json_options` parameter of the `EMBED_TEXT()` function.

**Example: Specify "downstream task" for better performance**

```sql
CREATE TABLE sample (
  `id`        INT,
  `content`   TEXT,
  `embedding` VECTOR(2048) GENERATED ALWAYS AS (EMBED_TEXT(
                "jina_ai/jina-embeddings-v4",
                `content`,
                '{"task": "retrieval.passage", "task@search": "retrieval.query"}'
              )) STORED
);
```

**Example: Use an alternative dimension**

```sql
CREATE TABLE sample (
  `id`        INT,
  `content`   TEXT,
  `embedding` VECTOR(768) GENERATED ALWAYS AS (EMBED_TEXT(
                "jina_ai/jina-embeddings-v3",
                `content`,
                '{"dimensions":768}'
              )) STORED
);
```

For all available options, see [Jina AI Documentation](https://jina.ai/embeddings/).

## Python usage example

See [PyTiDB Documentation](https://pingcap.github.io/ai/integrations/embedding-jinaai/).

## See Also

- [Auto Embedding Overview](/ai/vector-search-auto-embedding-overview.md)
- [Vector Search](/ai/vector-search-overview.md)
- [Vector Functions and Operators](/ai/vector-search-functions-and-operators.md)
- [Hybrid Search](/ai/vector-search-hybrid-search.md)
