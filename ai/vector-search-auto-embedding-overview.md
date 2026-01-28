---
title: Auto Embedding 概览
summary: 了解如何使用 Auto Embedding 功能通过纯文本进行语义搜索，而无需自行提供向量。
---

# Auto Embedding 概览

Auto Embedding 功能允许你直接使用纯文本执行向量搜索，无需手动提供向量。你可以直接插入文本数据，并通过文本查询进行语义搜索，TiDB 会在后台自动将文本转换为向量。

使用 Auto Embedding 的基本流程如下：

1. **创建一张表**：包含一个文本列和一个使用 `EMBED_TEXT()` 生成的向量列。
2. **插入文本数据**：该表的向量会自动生成并同时存储。
3. **使用文本进行查询**：使用 `VEC_EMBED_COSINE_DISTANCE()` 或 `VEC_EMBED_L2_DISTANCE()` 查找语义相似的内容。

> **注意：**
>
> 目前，仅 AWS 上的 TiDB Cloud Starter 集群支持 Auto Embedding 功能。

## 快速开始

> **建议：**
>
> 有关 Python 的用法，请参见 [PyTiDB 文档](https://pingcap.github.io/ai/guides/auto-embedding/)。

以下示例展示了如何使用 Auto Embedding 结合余弦距离进行语义搜索，无需 API key。

```sql
-- 创建支持 Auto Embedding 功能的表
-- 向量列的维度必须与嵌入模型维度匹配，否则在插入数据时会报错。
CREATE TABLE documents (
    id INT PRIMARY KEY AUTO_INCREMENT,
    content TEXT,
    content_vector VECTOR(1024) GENERATED ALWAYS AS (
        EMBED_TEXT("tidbcloud_free/amazon/titan-embed-text-v2", content)
    ) STORED
);

-- 插入文本数据（向量会自动生成）
INSERT INTO documents (content) VALUES
    ("Electric vehicles reduce air pollution in cities."),
    ("Solar panels convert sunlight into renewable energy."),
    ("Plant-based diets lower carbon footprints significantly."),
    ("Deep learning algorithms improve medical diagnosis accuracy."),
    ("Blockchain technology enhances data security systems.");

-- 使用文本查找语义相似的内容
SELECT id, content FROM documents
ORDER BY VEC_EMBED_COSINE_DISTANCE(
    content_vector,
    "Renewable energy solutions for environmental protection"
)
LIMIT 3;
```

查询结果：

```
+----+--------------------------------------------------------------+
| id | content                                                      |
+----+--------------------------------------------------------------+
|  2 | Solar panels convert sunlight into renewable energy.         |
|  1 | Electric vehicles reduce air pollution in cities.            |
|  4 | Deep learning algorithms improve medical diagnosis accuracy. |
+----+--------------------------------------------------------------+
```

上述示例使用了 Amazon Titan 模型。更多模型，请参见 [可用的文本嵌入模型](#available-text-embedding-models)。

## Auto Embedding + 向量索引

为提升查询性能，你可以结合 Auto Embedding 与[向量索引](/vector-search/vector-search-index.md) 功能，在 Auto Embedding 生成的向量列上创建向量索引，系统会自动使用该索引进行查询：

```sql
-- 创建支持 Auto Embedding 和向量索引功能的表
CREATE TABLE documents (
    id INT PRIMARY KEY AUTO_INCREMENT,
    content TEXT,
    content_vector VECTOR(1024) GENERATED ALWAYS AS (
        EMBED_TEXT("tidbcloud_free/amazon/titan-embed-text-v2", content)
    ) STORED,
    VECTOR INDEX ((VEC_COSINE_DISTANCE(content_vector)))
);

-- 插入文本数据（向量会自动生成）
INSERT INTO documents (content) VALUES
    ("Electric vehicles reduce air pollution in cities."),
    ("Solar panels convert sunlight into renewable energy."),
    ("Plant-based diets lower carbon footprints significantly."),
    ("Deep learning algorithms improve medical diagnosis accuracy."),
    ("Blockchain technology enhances data security systems.");

-- 使用相同的 VEC_EMBED_COSINE_DISTANCE() 函数，在向量索引上使用文本查询语义相似的内容
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

TiDB Cloud 支持多种嵌入模型，可根据需求选择：

| 嵌入模型      | 文档                                                                                  | 由 TiDB Cloud 托管 <sup>1</sup> | 需要用户自行提供 API key (BYOK) <sup>2</sup> |
| ------------- | ------------------------------------------------------------------------------------- | ---------------------------- | ----------------- |
| Amazon Titan  | [Amazon Titan Embeddings](/ai/vector-search-auto-embedding-amazon-titan.md)   | ✅                           |                   |
| Cohere        | [Cohere Embeddings](/ai/vector-search-auto-embedding-cohere.md)               | ✅                           | ✅                |
| Jina AI       | [Jina AI Embeddings](/ai/vector-search-auto-embedding-jina-ai.md)             |                              | ✅                |
| OpenAI        | [OpenAI Embeddings](/ai/vector-search-auto-embedding-openai.md)               |                              | ✅                |
| Gemini        | [Gemini Embeddings](/ai/vector-search-auto-embedding-gemini.md)               |                              | ✅                |

你还可以通过 TiDB Cloud 支持的以下推理服务，使用开源嵌入模型：

| 嵌入模型             | 文档                                                                                  | 由 TiDB Cloud 托管 <sup>1</sup> | 需要用户自行提供 API key (BYOK) <sup>2</sup> | 示例支持的模型                  |
| -------------------- | ------------------------------------------------------------------------------------- | ---------------------------- | ----------------- | ------------------------------- |
| HuggingFace Inference| [HuggingFace Embeddings](/ai/vector-search-auto-embedding-huggingface.md)     |                              | ✅                | `bge-m3`, `multilingual-e5-large`|
| NVIDIA NIM           | [NVIDIA NIM Embeddings](/ai/vector-search-auto-embedding-nvidia-nim.md)       |                              | ✅                | `bge-m3`, `nv-embed-v1`          |

&#8203;<sup>1</sup> 模型由 TiDB Cloud 托管，无需任何 API key。目前这些托管模型可免费使用，但可能有些限制以保障所有用户体验。

&#8203;<sup>2</sup> BYOK（Bring Your Own Key）模型需要你提供从相应的嵌入服务商处获取的 API key。TiDB Cloud 不对 BYOK 模型的使用收费。你需要自行管理和监控这些模型所产生的费用。

## Auto Embedding 的工作原理

Auto Embedding 使用 [`EMBED_TEXT()`](#embed_text) 函数调用你选择的嵌入模型，将文本转换为向量嵌入，并存储在 `VECTOR` 列中。你可以在 [`VEC_EMBED_COSINE_DISTANCE()`](#vec_embed_cosine_distance) 或 [`VEC_EMBED_L2_DISTANCE()`](#vec_embed_l2_distance) 函数中使用纯文本进行查询。

内部实现机制上，[`VEC_EMBED_COSINE_DISTANCE()`](#vec_embed_cosine_distance) 和 [`VEC_EMBED_L2_DISTANCE()`](#vec_embed_l2_distance) 在实际执行时会转换为 [`VEC_COSINE_DISTANCE()`](/vector-search/vector-search-functions-and-operators.md#vec_cosine_distance) 和 [`VEC_L2_DISTANCE()`](/vector-search/vector-search-functions-and-operators.md#vec_l2_distance)，既文本查询会自动转换为向量嵌入执行计算。

## 关键函数

### `EMBED_TEXT()`

将文本转换为向量嵌入：

```sql
EMBED_TEXT("model_name", text_content[, additional_json_options])
```

如需在插入或更新文本数据时自动生成嵌入，可以在 `GENERATED ALWAYS AS` 子句中使用该函数。

### `VEC_EMBED_COSINE_DISTANCE()`

计算向量列中已存储向量与文本查询之间的余弦相似度：

```sql
VEC_EMBED_COSINE_DISTANCE(vector_column, "query_text")
```

如需按余弦距离对结果进行排序，可以在 `ORDER BY` 子句中使用该函数。其计算方式与 [`VEC_COSINE_DISTANCE()`](/vector-search/vector-search-functions-and-operators.md#vec_cosine_distance) 相同，但会自动为查询文本生成嵌入。

### `VEC_EMBED_L2_DISTANCE()`

计算已存储向量与文本查询之间的 L2（欧氏）距离：

```sql
VEC_EMBED_L2_DISTANCE(vector_column, "query_text")
```

如需按 L2 距离对结果进行排序，可以在 `ORDER BY` 子句中使用该函数。其计算方式与 [`VEC_L2_DISTANCE()`](/vector-search/vector-search-functions-and-operators.md#vec_l2_distance) 相同，但会自动为查询文本生成嵌入。

## 在 Python 中使用 Auto Embedding

参见 [PyTiDB 文档](https://pingcap.github.io/ai/guides/auto-embedding/)。

## 参见

- [向量数据类型](/vector-search/vector-search-data-types.md)
- [向量函数与操作符](/vector-search/vector-search-functions-and-operators.md)
- [向量搜索索引](/vector-search/vector-search-index.md)
