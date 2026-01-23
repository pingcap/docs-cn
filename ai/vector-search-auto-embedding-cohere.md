---
title: Cohere Embeddings
summary: Learn how to use Cohere embedding models in TiDB Cloud.
---

# Cohere Embeddings

This document describes how to use Cohere embedding models with [Auto Embedding](/ai/vector-search-auto-embedding-overview.md) in TiDB Cloud to perform semantic searches from text queries.

> **Note:**
>
> [Auto Embedding](/ai/vector-search-auto-embedding-overview.md) is only available on {{{ .starter }}} clusters hosted on AWS.

## Available models

TiDB Cloud provides the following [Cohere](https://cohere.com/) embedding models natively. No API key is required.

**Cohere Embed v3 model**

- Name: `tidbcloud_free/cohere/embed-english-v3`
- Dimensions: 1024
- Distance metric: Cosine, L2
- Languages: English
- Maximum input text tokens: 512 (about 4 characters per token)
- Maximum input text characters: 2,048
- Price: Free
- Hosted by TiDB Cloud: ✅ `tidbcloud_free/cohere/embed-english-v3`
- Bring Your Own Key: ✅ `cohere/embed-english-v3.0`

**Cohere Multilingual Embed v3 model**

- Name: `tidbcloud_free/cohere/embed-multilingual-v3`
- Dimensions: 1024
- Distance metric: Cosine, L2
- Languages: 100+ languages
- Maximum input text tokens: 512 (about 4 characters per token)
- Maximum input text characters: 2,048
- Price: Free
- Hosted by TiDB Cloud: ✅ `tidbcloud_free/cohere/embed-multilingual-v3`
- Bring Your Own Key: ✅ `cohere/embed-multilingual-v3.0`

Alternatively, all Cohere models are available for use with the `cohere/` prefix if you bring your own Cohere API key (BYOK). For example:

**Cohere Embed v4 model**

- Name: `cohere/embed-v4.0`
- Dimensions: 256, 512, 1024, 1536 (default)
- Distance metric: Cosine, L2
- Maximum input text tokens: 128,000
- Price: Charged by Cohere
- Hosted by TiDB Cloud: ❌
- Bring Your Own Key: ✅

For a full list of Cohere models, see [Cohere Documentation](https://docs.cohere.com/docs/cohere-embed).

## SQL usage example (TiDB Cloud hosted)

The following example shows how to use the Cohere embedding model hosted by TiDB Cloud with Auto Embedding.

```sql
CREATE TABLE sample (
  `id`        INT,
  `content`   TEXT,
  `embedding` VECTOR(1024) GENERATED ALWAYS AS (EMBED_TEXT(
                "tidbcloud_free/cohere/embed-multilingual-v3",
                `content`,
                '{"input_type": "search_document", "input_type@search": "search_query"}'
              )) STORED
);
```

> **Note:**
>
> - For the Cohere embedding model, you must specify `input_type` in the `EMBED_TEXT()` function when defining the table. For example, `'{"input_type": "search_document", "input_type@search": "search_query"}'` means that `input_type` is set to `search_document` for data insertion and `search_query` is automatically applied during vector searches.
> - The `@search` suffix indicates that the field takes effect only during vector search queries, so you do not need to specify `input_type` again when writing a query.

Insert and query data:

```sql
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

## Options (TiDB Cloud hosted)

Both the **Embed v3** and **Multilingual Embed v3** models support the following options, which you can specify via the `additional_json_options` parameter of the `EMBED_TEXT()` function.

- `input_type` (required): prepends special tokens to indicate the purpose of the embedding. You must use the same input type consistently when generating embeddings for the same task, otherwise embeddings will be mapped to different semantic spaces and become incompatible. The only exception is semantic search, where documents are embedded with `search_document` and queries are embedded with `search_query`.

    - `search_document`: generates embeddings from documents to store in a vector database.
    - `search_query`: generates embeddings from queries to search against stored embeddings in a vector database.
    - `classification`: generates embeddings to be used as input for a text classifier.
    - `clustering`: generates embeddings for clustering tasks.

- `truncate` (optional): controls how the API handles inputs longer than the maximum token length. You can specify one of the following values:

    - `NONE` (default): returns an error when the input exceeds the maximum input token length.
    - `START`: discards text from the beginning until the input fits.
    - `END`: discards text from the end until the input fits.

## SQL usage example (BYOK)

To use Bring Your Own Key (BYOK) Cohere models, you must specify a Cohere API key as follows:

> **Note**
>
> Replace `'your-cohere-api-key-here'` with your actual Cohere API key. You can obtain an API key from the [Cohere Dashboard](https://dashboard.cohere.com/).

```sql
SET @@GLOBAL.TIDB_EXP_EMBED_COHERE_API_KEY = 'your-cohere-api-key-here';

CREATE TABLE sample (
  `id`        INT,
  `content`   TEXT,
  `embedding` VECTOR(1024) GENERATED ALWAYS AS (EMBED_TEXT(
                "cohere/embed-v4.0",
                `content`,
                '{"input_type": "search_document", "input_type@search": "search_query"}'
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

## Options (BYOK)

All [Cohere embedding options](https://docs.cohere.com/v2/reference/embed) are supported via the `additional_json_options` parameter of the `EMBED_TEXT()` function.

**Example: Specify different `input_type` for search and insert operations**

Use the `@search` suffix to indicates that the field takes effect only during vector search queries.

```sql
CREATE TABLE sample (
  `id`        INT,
  `content`   TEXT,
  `embedding` VECTOR(1024) GENERATED ALWAYS AS (EMBED_TEXT(
                "cohere/embed-v4.0",
                `content`,
                '{"input_type": "search_document", "input_type@search": "search_query"}'
              )) STORED
);
```

**Example: Use an alternative dimension**

```sql
CREATE TABLE sample (
  `id`        INT,
  `content`   TEXT,
  `embedding` VECTOR(512) GENERATED ALWAYS AS (EMBED_TEXT(
                "cohere/embed-v4.0",
                `content`,
                '{"output_dimension": 512}'
              )) STORED
);
```

For all available options, see [Cohere Documentation](https://docs.cohere.com/v2/reference/embed).

## Python usage example

See [PyTiDB Documentation](https://pingcap.github.io/ai/guides/auto-embedding/).

## See also

- [Auto Embedding Overview](/ai/vector-search-auto-embedding-overview.md)
- [Vector Search](/ai/vector-search-overview.md)
- [Vector Functions and Operators](/ai/vector-search-functions-and-operators.md)
- [Hybrid Search](/ai/vector-search-hybrid-search.md)
