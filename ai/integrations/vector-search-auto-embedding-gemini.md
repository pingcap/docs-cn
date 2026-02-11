---
title: Gemini 向量嵌入
summary: 了解如何在 TiDB Cloud 中使用 Google Gemini 向量嵌入模型。
aliases: ['/zh/tidbcloud/vector-search-auto-embedding-gemini/']
---

# Gemini 向量嵌入

本文档介绍如何在 TiDB Cloud 中结合 [Auto Embedding](/ai/integrations/vector-search-auto-embedding-overview.md) 使用 Gemini 向量嵌入模型，通过文本查询实现语义搜索。

> **注意：**
>
> [Auto Embedding](/ai/integrations/vector-search-auto-embedding-overview.md) 仅适用于托管在 AWS 上的 TiDB Cloud Starter 集群。

## 可用模型

如果你自带 Gemini API 密钥（BYOK），则所有 Gemini 模型均可通过 `gemini/` 前缀使用。例如：

**gemini-embedding-001**

- 名称：`gemini/gemini-embedding-001`
- 维度：128–3072（默认：3072）
- 距离度量：Cosine，L2
- 最大输入文本 token 数：2,048
- 价格：由 Google 收费
- 由 TiDB Cloud 托管：❌
- 支持 Bring Your Own Key（BYOK，由用户自行提供 API 密钥）：✅

完整可用模型列表请参见 [Gemini 文档](https://ai.google.dev/gemini-api/docs/embeddings)。

## 使用示例

以下示例展示如何创建向量表、插入文档，并使用 Google Gemini 向量嵌入模型进行相似度搜索。

### 步骤 1：连接数据库

<SimpleTab groupId="language">
<div label="Python" value="python">

```python
from pytidb import TiDBClient

tidb_client = TiDBClient.connect(
    host="{gateway-region}.prod.aws.tidbcloud.com",
    port=4000,
    username="{prefix}.root",
    password="{password}",
    database="{database}",
    ensure_db=True,
)
```

</div>
<div label="SQL" value="sql">

```bash
mysql -h {gateway-region}.prod.aws.tidbcloud.com \
    -P 4000 \
    -u {prefix}.root \
    -p{password} \
    -D {database}
```

</div>
</SimpleTab>

### 步骤 2：配置 API 密钥

在 [Google AI Studio](https://makersuite.google.com/app/apikey) 创建你的 API 密钥，并自带密钥（BYOK）以使用向量嵌入服务。

<SimpleTab groupId="language">
<div label="Python" value="python">

使用 TiDB Client 配置 Google Gemini 向量嵌入提供方的 API 密钥：

```python
tidb_client.configure_embedding_provider(
    provider="google_gemini",
    api_key="{your-google-api-key}",
)
```

</div>
<div label="SQL" value="sql">

通过 SQL 设置 Google Gemini 向量嵌入提供方的 API 密钥：

```sql
SET @@GLOBAL.TIDB_EXP_EMBED_GEMINI_API_KEY = "{your-google-api-key}";
```

</div>
</SimpleTab>

### 步骤 3：创建向量表

创建一个包含向量字段的表，使用 `gemini-embedding-001` 模型生成 3072 维（默认）向量：

<SimpleTab groupId="language">
<div label="Python" value="python">

```python
from pytidb.schema import TableModel, Field
from pytidb.embeddings import EmbeddingFunction
from pytidb.datatype import TEXT

class Document(TableModel):
    __tablename__ = "sample_documents"
    id: int = Field(primary_key=True)
    content: str = Field(sa_type=TEXT)
    embedding: list[float] = EmbeddingFunction(
        model_name="gemini-embedding-001"
    ).VectorField(source_field="content")

table = tidb_client.create_table(schema=Document, if_exists="overwrite")
```

</div>
<div label="SQL" value="sql">

```sql
CREATE TABLE sample_documents (
    `id`        INT PRIMARY KEY,
    `content`   TEXT,
    `embedding` VECTOR(3072) GENERATED ALWAYS AS (EMBED_TEXT(
        "gemini-embedding-001",
        `content`
    )) STORED
);
```

</div>
</SimpleTab>

### 步骤 4：向表中插入数据

<SimpleTab groupId="language">
<div label="Python" value="python">

使用 `table.insert()` 或 `table.bulk_insert()` API 添加数据：

```python
documents = [
    Document(id=1, content="Java: Object-oriented language for cross-platform development."),
    Document(id=2, content="Java coffee: Bold Indonesian beans with low acidity."),
    Document(id=3, content="Java island: Densely populated, home to Jakarta."),
    Document(id=4, content="Java's syntax is used in Android apps."),
    Document(id=5, content="Dark roast Java beans enhance espresso blends."),
]
table.bulk_insert(documents)
```

</div>
<div label="SQL" value="sql">

使用 `INSERT INTO` 语句插入数据：

```sql
INSERT INTO sample_documents (id, content)
VALUES
    (1, "Java: Object-oriented language for cross-platform development."),
    (2, "Java coffee: Bold Indonesian beans with low acidity."),
    (3, "Java island: Densely populated, home to Jakarta."),
    (4, "Java's syntax is used in Android apps."),
    (5, "Dark roast Java beans enhance espresso blends.");
```

</div>
</SimpleTab>

### 步骤 5：搜索相似文档

<SimpleTab groupId="language">
<div label="Python" value="python">

使用 `table.search()` API 进行向量搜索：

```python
results = table.search("How to start learning Java programming?") \
    .limit(2) \
    .to_list()
print(results)
```

</div>
<div label="SQL" value="sql">

使用 `VEC_EMBED_COSINE_DISTANCE` 函数基于余弦距离进行向量搜索：

```sql
SELECT
    `id`,
    `content`,
    VEC_EMBED_COSINE_DISTANCE(embedding, "How to start learning Java programming?") AS _distance
FROM sample_documents
ORDER BY _distance ASC
LIMIT 2;
```

</div>
</SimpleTab>

## 自定义向量嵌入维度

`gemini-embedding-001` 模型通过 Matryoshka Representation Learning (MRL) 支持灵活的维度。你可以在向量嵌入函数中指定所需的维度：

<SimpleTab groupId="language">
<div label="Python" value="python">

```python
# 1536 维
embedding: list[float] = EmbeddingFunction(
    model_name="gemini-embedding-001",
    dimensions=1536
).VectorField(source_field="content")

# 768 维
embedding: list[float] = EmbeddingFunction(
    model_name="gemini-embedding-001",
    dimensions=768
).VectorField(source_field="content")
```

</div>
<div label="SQL" value="sql">

```sql
-- 1536 维
`embedding` VECTOR(1536) GENERATED ALWAYS AS (EMBED_TEXT(
    "gemini-embedding-001",
    `content`,
    '{"embedding_config": {"output_dimensionality": 1536}}'
)) STORED

-- 768 维
`embedding` VECTOR(768) GENERATED ALWAYS AS (EMBED_TEXT(
    "gemini-embedding-001",
    `content`,
    '{"embedding_config": {"output_dimensionality": 768}}'
)) STORED
```

</div>
</SimpleTab>

请根据你的性能需求和存储约束选择合适的维度。更高的维度可以提升准确性，但会占用更多存储和计算资源。

## 选项

所有 [Gemini 选项](https://ai.google.dev/gemini-api/docs/embeddings) 均可通过 `EMBED_TEXT()` 函数的 `additional_json_options` 参数进行设置。

**示例：指定任务类型以提升质量**

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

**示例：使用不同维度**

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

所有可用选项请参见 [Gemini 文档](https://ai.google.dev/gemini-api/docs/embeddings)。

## 另请参阅

- [Auto Embedding 概览](/ai/integrations/vector-search-auto-embedding-overview.md)
- [向量搜索](/ai/concepts/vector-search-overview.md)
- [向量函数与操作符](/ai/reference/vector-search-functions-and-operators.md)
- [混合搜索](/ai/guides/vector-search-hybrid-search.md)
