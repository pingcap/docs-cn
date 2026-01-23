---
title: Auto Embedding Overview
summary: Learn how to use Auto Embedding to perform semantic searches with plain text instead of vectors.
---

# Auto Embedding Overview

The Auto Embedding feature lets you perform vector searches directly with plain text, without providing your own vectors. With this feature, you can insert text data directly and perform semantic searches using text queries, while TiDB automatically converts the text into vectors behind the scenes.

To use Auto Embedding, the basic workflow is as follows:

1. **Define a table** with a text column and a generated vector column using `EMBED_TEXT()`.
2. **Insert text data** — vectors are automatically generated and stored concurrently.
3. **Query using text** — use `VEC_EMBED_COSINE_DISTANCE()` or `VEC_EMBED_L2_DISTANCE()` to find semantically similar content.

> **Note:**
>
> Auto Embedding is only available on {{{ .starter }}} clusters hosted on AWS.

## Quick start example

> **Tip:**
>
> For Python usage, see [PyTiDB Documentation](https://pingcap.github.io/ai/guides/auto-embedding/).

The following example shows how to use Auto Embedding with cosine distance to perform a semantic search. No API key is required in this example.

```sql
-- Create a table with auto-embedding
-- The dimension of the vector column must match the dimension of the embedding model,
-- otherwise TiDB returns an error when inserting data.
CREATE TABLE documents (
    id INT PRIMARY KEY AUTO_INCREMENT,
    content TEXT,
    content_vector VECTOR(1024) GENERATED ALWAYS AS (
        EMBED_TEXT("tidbcloud_free/amazon/titan-embed-text-v2", content)
    ) STORED
);

-- Insert text data (vectors are generated automatically)
INSERT INTO documents (content) VALUES
    ("Electric vehicles reduce air pollution in cities."),
    ("Solar panels convert sunlight into renewable energy."),
    ("Plant-based diets lower carbon footprints significantly."),
    ("Deep learning algorithms improve medical diagnosis accuracy."),
    ("Blockchain technology enhances data security systems.");

-- Search for semantically similar content using text query
SELECT id, content FROM documents
ORDER BY VEC_EMBED_COSINE_DISTANCE(
    content_vector,
    "Renewable energy solutions for environmental protection"
)
LIMIT 3;
```

The output is as follows:

```
+----+--------------------------------------------------------------+
| id | content                                                      |
+----+--------------------------------------------------------------+
|  2 | Solar panels convert sunlight into renewable energy.         |
|  1 | Electric vehicles reduce air pollution in cities.            |
|  4 | Deep learning algorithms improve medical diagnosis accuracy. |
+----+--------------------------------------------------------------+
```

The preceding example uses the Amazon Titan model. For other models, see [Available text embedding models](#available-text-embedding-models).

## Auto Embedding + Vector index

Auto Embedding is compatible with [Vector index](/ai/vector-search-index.md) for better query performance. You can define a vector index on the generated vector column, and it will be used automatically:

```sql
-- Create a table with auto-embedding and a vector index
CREATE TABLE documents (
    id INT PRIMARY KEY AUTO_INCREMENT,
    content TEXT,
    content_vector VECTOR(1024) GENERATED ALWAYS AS (
        EMBED_TEXT("tidbcloud_free/amazon/titan-embed-text-v2", content)
    ) STORED,
    VECTOR INDEX ((VEC_COSINE_DISTANCE(content_vector)))
);

-- Insert text data (vectors are generated automatically)
INSERT INTO documents (content) VALUES
    ("Electric vehicles reduce air pollution in cities."),
    ("Solar panels convert sunlight into renewable energy."),
    ("Plant-based diets lower carbon footprints significantly."),
    ("Deep learning algorithms improve medical diagnosis accuracy."),
    ("Blockchain technology enhances data security systems.");

-- Search for semantically similar content with a text query on the vector index using the same VEC_EMBED_COSINE_DISTANCE() function
SELECT id, content FROM documents
ORDER BY VEC_EMBED_COSINE_DISTANCE(
    content_vector,
    "Renewable energy solutions for environmental protection"
)
LIMIT 3;
```

> **Note:**
>
> - When defining a vector index, use `VEC_COSINE_DISTANCE()` or `VEC_L2_DISTANCE()`.
> - When running queries, use `VEC_EMBED_COSINE_DISTANCE()` or `VEC_EMBED_L2_DISTANCE()`.

## Available text embedding models

TiDB Cloud supports various embedding models. Choose the one that best fits your needs:

| Embedding model | Documentation                                                                       | Hosted by TiDB Cloud <sup>1</sup> | BYOK <sup>2</sup> |
| --------------- | ----------------------------------------------------------------------------------- | --------------------------------- | ----------------- |
| Amazon Titan    | [Amazon Titan Embeddings](/ai/vector-search-auto-embedding-amazon-titan.md) | ✅                                |                   |
| Cohere          | [Cohere Embeddings](/ai/vector-search-auto-embedding-cohere.md)             | ✅                                | ✅                |
| Jina AI         | [Jina AI Embeddings](/ai/vector-search-auto-embedding-jina-ai.md)           |                                   | ✅                |
| OpenAI          | [OpenAI Embeddings](/ai/vector-search-auto-embedding-openai.md)             |                                   | ✅                |
| Gemini          | [Gemini Embeddings](/ai/vector-search-auto-embedding-gemini.md)             |                                   | ✅                |

You can also use open-source embedding models through the following inference services that TiDB Cloud supports:

| Embedding model       | Documentation                                                                     | Hosted by TiDB Cloud <sup>1</sup> | BYOK <sup>2</sup> | Example supported models          |
| --------------------- | --------------------------------------------------------------------------------- | --------------------------------- | ----------------- | --------------------------------- |
| HuggingFace Inference | [HuggingFace Embeddings](/ai/vector-search-auto-embedding-huggingface.md) |                                   | ✅                | `bge-m3`, `multilingual-e5-large` |
| NVIDIA NIM            | [NVIDIA NIM Embeddings](/ai/vector-search-auto-embedding-nvidia-nim.md)   |                                   | ✅                | `bge-m3`, `nv-embed-v1`           |

&#8203;<sup>1</sup> Hosted models are hosted by TiDB Cloud and do not require any API keys. Currently, these hosted models are free to use, but certain usage limits might be applied to keep them available to everyone.

&#8203;<sup>2</sup> BYOK (Bring Your Own Key) models require you to provide your own API keys from the corresponding embedding provider. TiDB Cloud does not charge for the usage of BYOK models. You are responsible for managing and monitoring the costs associated with using these models.

## How Auto Embedding works

Auto Embedding uses the [`EMBED_TEXT()`](#embed_text) function to convert text into vector embeddings with your chosen embedding model. The generated vectors are stored in `VECTOR` columns and can be queried with plain text using [`VEC_EMBED_COSINE_DISTANCE()`](#vec_embed_cosine_distance) or [`VEC_EMBED_L2_DISTANCE()`](#vec_embed_l2_distance).

Internally, [`VEC_EMBED_COSINE_DISTANCE()`](#vec_embed_cosine_distance) and [`VEC_EMBED_L2_DISTANCE()`](#vec_embed_l2_distance) are executed as [`VEC_COSINE_DISTANCE()`](/ai/vector-search-functions-and-operators.md#vec_cosine_distance) and [`VEC_L2_DISTANCE()`](/ai/vector-search-functions-and-operators.md#vec_l2_distance), with the text query automatically converted into a vector embedding.

## Key functions

### `EMBED_TEXT()`

Converts text to vector embeddings:

```sql
EMBED_TEXT("model_name", text_content[, additional_json_options])
```

Use this function in `GENERATED ALWAYS AS` clauses to automatically generate embeddings when inserting or updating text data.

### `VEC_EMBED_COSINE_DISTANCE()`

Calculates cosine similarity between a stored vector in the vector column and a text query:

```sql
VEC_EMBED_COSINE_DISTANCE(vector_column, "query_text")
```

Use this function in `ORDER BY` clauses to rank results by cosine distance. It uses the same calculation as [`VEC_COSINE_DISTANCE()`](/ai/vector-search-functions-and-operators.md#vec_cosine_distance), but automatically generates the embedding for the query text.

### `VEC_EMBED_L2_DISTANCE()`

Calculates L2 (Euclidean) distance between a stored vector and a text query:

```sql
VEC_EMBED_L2_DISTANCE(vector_column, "query_text")
```

Use this function in `ORDER BY` clauses to rank results by L2 distance. It uses the same calculation as [`VEC_L2_DISTANCE()`](/ai/vector-search-functions-and-operators.md#vec_l2_distance), but automatically generates the embedding for the query text.

## Use Auto Embedding in Python

See [PyTiDB Documentation](https://pingcap.github.io/ai/guides/auto-embedding/).

## See also

- [Vector Data Types](/ai/vector-search-data-types.md)
- [Vector Functions and Operators](/ai/vector-search-functions-and-operators.md)
- [Vector Search Index](/ai/vector-search-index.md)
