---
title: Auto Embedding 概述
summary: 了解如何使用 Auto Embedding 通过纯文本而非向量进行语义搜索。
---

# Auto Embedding 概述 <!-- Draft translated by AI -->

Auto Embedding 功能允许你直接使用纯文本进行向量搜索，无需自行提供向量。通过该功能，你可以直接插入文本数据，并使用文本查询进行语义搜索，TiDB 会在后台自动将文本转换为向量。

要使用 Auto Embedding，基本流程如下：

1. **定义一张表**，包含一个文本列和一个使用 `EMBED_TEXT()` 生成的向量列。
2. **插入文本数据** —— 向量会自动生成并同时存储。
3. **使用文本进行查询** —— 使用 `VEC_EMBED_COSINE_DISTANCE()` 或 `VEC_EMBED_L2_DISTANCE()` 查找语义相似的内容。

> **注意：**
>
> Auto Embedding 仅在托管于 AWS 的 TiDB Cloud Starter 集群上可用。

## 快速入门示例

> **提示：**
>
> 有关 Python 的用法，请参见 [PyTiDB 文档](https://pingcap.github.io/ai/guides/auto-embedding/)。

以下示例展示了如何使用 Auto Embedding 结合余弦距离进行语义搜索。此示例无需 API key。

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

输出如下：

```
+----+--------------------------------------------------------------+
| id | content                                                      |
+----+--------------------------------------------------------------+
|  2 | Solar panels convert sunlight into renewable energy.         |
|  1 | Electric vehicles reduce air pollution in cities.            |
|  4 | Deep learning algorithms improve medical diagnosis accuracy. |
+----+--------------------------------------------------------------+
```

上述示例使用了 Amazon Titan 模型。关于其他模型，请参见 [可用的文本嵌入模型](#available-text-embedding-models)。

## Auto Embedding + 向量索引

Auto Embedding 可与 [向量索引](/vector-search/vector-search-index.md) 配合使用，以提升查询性能。你可以在生成的向量列上定义向量索引，系统会自动使用该索引：

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

> **注意：**
>
> - 定义向量索引时，使用 `VEC_COSINE_DISTANCE()` 或 `VEC_L2_DISTANCE()`。
> - 查询时，使用 `VEC_EMBED_COSINE_DISTANCE()` 或 `VEC_EMBED_L2_DISTANCE()`。

## 可用的文本嵌入模型

TiDB Cloud 支持多种嵌入模型。请选择最适合你需求的模型：

| 嵌入模型      | 文档                                                                                  | TiDB Cloud 托管 <sup>1</sup> | BYOK <sup>2</sup> |
| ------------- | ------------------------------------------------------------------------------------- | ---------------------------- | ----------------- |
| Amazon Titan  | [Amazon Titan Embeddings](/ai/vector-search-auto-embedding-amazon-titan.md)   | ✅                           |                   |
| Cohere        | [Cohere Embeddings](/ai/vector-search-auto-embedding-cohere.md)               | ✅                           | ✅                |
| Jina AI       | [Jina AI Embeddings](/ai/vector-search-auto-embedding-jina-ai.md)             |                              | ✅                |
| OpenAI        | [OpenAI Embeddings](/ai/vector-search-auto-embedding-openai.md)               |                              | ✅                |
| Gemini        | [Gemini Embeddings](/ai/vector-search-auto-embedding-gemini.md)               |                              | ✅                |

你还可以通过 TiDB Cloud 支持的以下推理服务，使用开源嵌入模型：

| 嵌入模型             | 文档                                                                                  | TiDB Cloud 托管 <sup>1</sup> | BYOK <sup>2</sup> | 示例支持的模型                  |
| -------------------- | ------------------------------------------------------------------------------------- | ---------------------------- | ----------------- | ------------------------------- |
| HuggingFace Inference| [HuggingFace Embeddings](/ai/vector-search-auto-embedding-huggingface.md)     |                              | ✅                | `bge-m3`, `multilingual-e5-large`|
| NVIDIA NIM           | [NVIDIA NIM Embeddings](/ai/vector-search-auto-embedding-nvidia-nim.md)       |                              | ✅                | `bge-m3`, `nv-embed-v1`          |

&#8203;<sup>1</sup> 托管模型由 TiDB Cloud 托管，无需任何 API key。目前这些托管模型可免费使用，但可能会施加一定的使用限制，以保证所有用户的可用性。

&#8203;<sup>2</sup> BYOK（Bring Your Own Key）模型需要你从相应的嵌入服务商处提供自己的 API key。TiDB Cloud 不会对 BYOK 模型的使用收费。你需要自行管理和监控使用这些模型所产生的费用。

## Auto Embedding 的工作原理

Auto Embedding 使用 [`EMBED_TEXT()`](#embed_text) 函数，结合你选择的嵌入模型，将文本转换为向量嵌入。生成的向量存储在 `VECTOR` 列中，并可通过 [`VEC_EMBED_COSINE_DISTANCE()`](#vec_embed_cosine_distance) 或 [`VEC_EMBED_L2_DISTANCE()`](#vec_embed_l2_distance) 使用纯文本进行查询。

在内部，[`VEC_EMBED_COSINE_DISTANCE()`](#vec_embed_cosine_distance) 和 [`VEC_EMBED_L2_DISTANCE()`](#vec_embed_l2_distance) 实际执行的是 [`VEC_COSINE_DISTANCE()`](/vector-search/vector-search-functions-and-operators.md#vec_cosine_distance) 和 [`VEC_L2_DISTANCE()`](/vector-search/vector-search-functions-and-operators.md#vec_l2_distance)，文本查询会自动转换为向量嵌入。

## 关键函数

### `EMBED_TEXT()`

将文本转换为向量嵌入：

```sql
EMBED_TEXT("model_name", text_content[, additional_json_options])
```

在 `GENERATED ALWAYS AS` 子句中使用该函数，可在插入或更新文本数据时自动生成嵌入。

### `VEC_EMBED_COSINE_DISTANCE()`

计算向量列中已存储向量与文本查询之间的余弦相似度：

```sql
VEC_EMBED_COSINE_DISTANCE(vector_column, "query_text")
```

在 `ORDER BY` 子句中使用该函数，可按余弦距离对结果进行排序。其计算方式与 [`VEC_COSINE_DISTANCE()`](/vector-search/vector-search-functions-and-operators.md#vec_cosine_distance) 相同，但会自动为查询文本生成嵌入。

### `VEC_EMBED_L2_DISTANCE()`

计算已存储向量与文本查询之间的 L2（欧氏）距离：

```sql
VEC_EMBED_L2_DISTANCE(vector_column, "query_text")
```

在 `ORDER BY` 子句中使用该函数，可按 L2 距离对结果进行排序。其计算方式与 [`VEC_L2_DISTANCE()`](/vector-search/vector-search-functions-and-operators.md#vec_l2_distance) 相同，但会自动为查询文本生成嵌入。

## 在 Python 中使用 Auto Embedding

参见 [PyTiDB 文档](https://pingcap.github.io/ai/guides/auto-embedding/)。

## 参见

- [向量数据类型](/vector-search/vector-search-data-types.md)
- [向量函数与操作符](/vector-search/vector-search-functions-and-operators.md)
- [向量搜索索引](/vector-search/vector-search-index.md)
