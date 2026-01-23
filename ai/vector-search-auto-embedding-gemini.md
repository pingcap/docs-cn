---
title: Gemini Embeddings
summary: Learn how to use Google Gemini embedding models in TiDB Cloud.
---

# Gemini Embeddings

This document describes how to use Gemini embedding models with [Auto Embedding](/ai/vector-search-auto-embedding-overview.md) in TiDB Cloud to perform semantic searches from text queries.

> **Note:**
>
> [Auto Embedding](/ai/vector-search-auto-embedding-overview.md) is only available on {{{ .starter }}} clusters hosted on AWS.

## Available models

All Gemini models are available for use with the `gemini/` prefix if you bring your own Gemini API key (BYOK). For example:

**gemini-embedding-001**

- Name: `gemini/gemini-embedding-001`
- Dimensions: 128–3072 (default: 3072)
- Distance metric: Cosine, L2
- Maximum input text tokens: 2,048
- Price: Charged by Google
- Hosted by TiDB Cloud: ❌
- Bring Your Own Key: ✅

For a full list of available models, see [Gemini documentation](https://ai.google.dev/gemini-api/docs/embeddings).

## SQL usage example

To use Gemini models, you must specify a [Gemini API key](https://ai.google.dev/gemini-api/docs/api-key) as follows:

> **Note:**
>
> Replace `'your-gemini-api-key-here'` with your actual Gemini API key.

```sql
SET @@GLOBAL.TIDB_EXP_EMBED_GEMINI_API_KEY = 'your-gemini-api-key-here';

CREATE TABLE sample (
  `id`        INT,
  `content`   TEXT,
  `embedding` VECTOR(3072) GENERATED ALWAYS AS (EMBED_TEXT(
                "gemini/gemini-embedding-001",
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

All [Gemini options](https://ai.google.dev/gemini-api/docs/embeddings) are supported via the `additional_json_options` parameter of the `EMBED_TEXT()` function.

**Example: Specify the task type to improve quality**

```sql
CREATE TABLE sample (
  `id`        INT,
  `content`   TEXT,
  `embedding` VECTOR(1024) GENERATED ALWAYS AS (EMBED_TEXT(
                "gemini/gemini-embedding-001",
                `content`,
                '{"task_type": "SEMANTIC_SIMILARITY"}'
              )) STORED
);
```

**Example: Use an alternative dimension**

```sql
CREATE TABLE sample (
  `id`        INT,
  `content`   TEXT,
  `embedding` VECTOR(768) GENERATED ALWAYS AS (EMBED_TEXT(
                "gemini/gemini-embedding-001",
                `content`,
                '{"output_dimensionality": 768}'
              )) STORED
);
```

For all available options, see [Gemini documentation](https://ai.google.dev/gemini-api/docs/embeddings).

## Python usage example

See [PyTiDB Documentation](https://pingcap.github.io/ai/guides/auto-embedding/).

## See also

- [Auto Embedding Overview](/ai/vector-search-auto-embedding-overview.md)
- [Vector Search](/ai/vector-search-overview.md)
- [Vector Functions and Operators](/ai/vector-search-functions-and-operators.md)
- [Hybrid Search](/ai/vector-search-hybrid-search.md)
