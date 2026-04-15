---
title: Jina AI Embeddings
summary: 了解如何在 TiDB Cloud 中使用 Jina AI 嵌入模型。
aliases: ['/zh/tidbcloud/vector-search-auto-embedding-jina-ai/']
---

# Jina AI Embeddings

本文档介绍如何在 TiDB Cloud 中结合 [Auto Embedding](/ai/integrations/vector-search-auto-embedding-overview.md) 使用 [Jina AI 嵌入模型](https://jina.ai/embeddings/)，以便通过文本查询执行语义搜索。

> **注意：**
>
> [Auto Embedding](/ai/integrations/vector-search-auto-embedding-overview.md) 仅适用于托管在 AWS 上的 TiDB Cloud Starter 集群。

## 可用模型

Jina AI 提供高性能、多模态、多语言、长上下文的嵌入模型，适用于搜索、RAG 和智能体应用。

如果你自带 Jina AI API 密钥（BYOK），所有 Jina AI 模型均可通过 `jina_ai/` 前缀使用。例如：

**jina-embeddings-v4**

- 名称: `jina_ai/jina-embeddings-v4`
- 维度: 2048
- 距离度量: Cosine, L2
- 最大输入文本 token 数: 32,768
- 价格: 由 Jina AI 收费
- 由 TiDB Cloud 托管: ❌
- 支持 Bring Your Own Key（BYOK，由用户自行提供 API 密钥）: ✅

**jina-embeddings-v3**

- 名称: `jina_ai/jina-embeddings-v3`
- 维度: 1024
- 距离度量: Cosine, L2
- 最大输入文本 token 数: 8,192
- 价格: 由 Jina AI 收费
- 由 TiDB Cloud 托管: ❌
- 支持 Bring Your Own Key（BYOK，由用户自行提供 API 密钥）: ✅

完整可用模型列表请参见 [Jina AI 文档](https://jina.ai/embeddings/)。

## 使用示例

本示例展示如何创建向量表、插入文档，并使用 Jina AI 嵌入模型进行相似度搜索。

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

在 [Jina AI Platform](https://jina.ai/embeddings/) 创建你的 API 密钥，并自带密钥（BYOK）以使用嵌入服务。

<SimpleTab groupId="language">
<div label="Python" value="python">

使用 TiDB Client 为 Jina AI 嵌入提供方配置 API 密钥：

```python
tidb_client.configure_embedding_provider(
    provider="jina_ai",
    api_key="{your-jina-api-key}",
)
```

</div>
<div label="SQL" value="sql">

通过 SQL 为 Jina AI 嵌入提供方设置 API 密钥：

```sql
SET @@GLOBAL.TIDB_EXP_EMBED_JINA_AI_API_KEY = "{your-jina-api-key}";
```

</div>
</SimpleTab>

### 步骤 3：创建向量表

创建一个包含向量字段的表，使用 `jina_ai/jina-embeddings-v4` 模型生成 2048 维向量：

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
        model_name="jina_ai/jina-embeddings-v4"
    ).VectorField(source_field="content")

table = tidb_client.create_table(schema=Document, if_exists="overwrite")
```

</div>
<div label="SQL" value="sql">

```sql
CREATE TABLE sample_documents (
    `id`        INT PRIMARY KEY,
    `content`   TEXT,
    `embedding` VECTOR(2048) GENERATED ALWAYS AS (EMBED_TEXT(
        "jina_ai/jina-embeddings-v4",
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

使用 `VEC_EMBED_COSINE_DISTANCE` 函数基于余弦距离度量进行向量搜索：

```sql
SELECT
    `id`,
    `content`,
    VEC_EMBED_COSINE_DISTANCE(embedding, "How to start learning Java programming?") AS _distance
FROM sample_documents
ORDER BY _distance ASC
LIMIT 2;
```

结果：

```
+------+----------------------------------------------------------------+
| id   | content                                                        |
+------+----------------------------------------------------------------+
|    1 | Java: Object-oriented language for cross-platform development. |
|    4 | Java's syntax is used in Android apps.                         |
+------+----------------------------------------------------------------+
```

</div>
</SimpleTab>

## 选项

所有 [Jina AI 选项](https://jina.ai/embeddings/) 均可通过 `EMBED_TEXT()` 函数的 `additional_json_options` 参数进行设置。

**示例：为更优性能指定 “下游任务”**

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

**示例：使用其他维度**

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

所有可用选项请参见 [Jina AI 文档](https://jina.ai/embeddings/)。

## 另请参阅

- [Auto Embedding 概览](/ai/integrations/vector-search-auto-embedding-overview.md)
- [向量搜索](/ai/concepts/vector-search-overview.md)
- [向量函数与操作符](/ai/reference/vector-search-functions-and-operators.md)
- [混合搜索](/ai/guides/vector-search-hybrid-search.md)
