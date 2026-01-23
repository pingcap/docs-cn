---
title: OpenAI Embeddings
summary: Learn how to use OpenAI embedding models in TiDB Cloud.
---

# OpenAI Embeddings

This document describes how to use OpenAI embedding models with [Auto Embedding](/ai/vector-search-auto-embedding-overview.md) in TiDB Cloud to perform semantic searches from text queries.

> **Note:**
>
> [Auto Embedding](/ai/vector-search-auto-embedding-overview.md) is only available on {{{ .starter }}} clusters hosted on AWS.

## Available models

All OpenAI models are available for use with the `openai/` prefix if you bring your own OpenAI API key (BYOK). For example:

**text-embedding-3-small**

- Name: `openai/text-embedding-3-small`
- Dimensions: 512-1536 (default: 1536)
- Distance metric: Cosine, L2
- Price: Charged by OpenAI
- Hosted by TiDB Cloud: ❌
- Bring Your Own Key: ✅

**text-embedding-3-large**

- Name: `openai/text-embedding-3-large`
- Dimensions: 256-3072 (default: 3072)
- Distance metric: Cosine, L2
- Price: Charged by OpenAI
- Hosted by TiDB Cloud: ❌
- Bring Your Own Key: ✅

For a full list of available models, see [OpenAI Documentation](https://platform.openai.com/docs/guides/embeddings).

## SQL usage example

To use OpenAI models, you must specify an [OpenAI API key](https://platform.openai.com/api-keys) as follows:

> **Note:**
>
> Replace `'your-openai-api-key-here'` with your actual OpenAI API key.

```sql
SET @@GLOBAL.TIDB_EXP_EMBED_OPENAI_API_KEY = 'your-openai-api-key-here';

CREATE TABLE sample (
  `id`        INT,
  `content`   TEXT,
  `embedding` VECTOR(1536) GENERATED ALWAYS AS (EMBED_TEXT(
                "openai/text-embedding-3-small",
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

All [OpenAI embedding options](https://platform.openai.com/docs/api-reference/embeddings/create) are supported via the `additional_json_options` parameter of the `EMBED_TEXT()` function.

**Example: Use an alternative dimension for text-embedding-3-large**

```sql
CREATE TABLE sample (
  `id`        INT,
  `content`   TEXT,
  `embedding` VECTOR(1024) GENERATED ALWAYS AS (EMBED_TEXT(
                "openai/text-embedding-3-large",
                `content`,
                '{"dimensions": 1024}'
              )) STORED
);
```

For all available options, see [OpenAI Documentation](https://platform.openai.com/docs/api-reference/embeddings/create).

## Python usage example

See [PyTiDB Documentation](https://pingcap.github.io/ai/guides/auto-embedding/).

## See also

- [Auto Embedding Overview](/ai/vector-search-auto-embedding-overview.md)
- [Vector Search](/ai/vector-search-overview.md)
- [Vector Functions and Operators](/ai/vector-search-functions-and-operators.md)
- [Hybrid Search](/ai/vector-search-hybrid-search.md)
