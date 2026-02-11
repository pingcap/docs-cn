---
title: Cohere 向量嵌入
summary: 了解如何在 TiDB Cloud 中使用 Cohere 向量嵌入模型。
aliases: ['/zh/tidbcloud/vector-search-auto-embedding-cohere/']
---

# Cohere 向量嵌入

本文档介绍如何在 TiDB Cloud 中结合 [Auto Embedding](/ai/integrations/vector-search-auto-embedding-overview.md) 使用 Cohere 向量嵌入模型，通过文本查询实现语义搜索。

> **注意：**
>
> [Auto Embedding](/ai/integrations/vector-search-auto-embedding-overview.md) 仅适用于托管在 AWS 上的 TiDB Cloud Starter 集群。

## 可用模型

TiDB Cloud 原生提供以下 [Cohere](https://cohere.com/) 向量嵌入模型，无需 API 密钥。

**Cohere Embed v3 模型**

- 名称：`tidbcloud_free/cohere/embed-english-v3`
- 维度：1024
- 距离度量：Cosine，L2
- 语言：英语
- 最大输入文本 token 数：512（约每个 token 4 个字符）
- 最大输入文本字符数：2,048
- 价格：免费
- 由 TiDB Cloud 托管：✅ `tidbcloud_free/cohere/embed-english-v3`
- 自带密钥（BYOK）：✅ `cohere/embed-english-v3.0`

**Cohere Multilingual Embed v3 模型**

- 名称：`tidbcloud_free/cohere/embed-multilingual-v3`
- 维度：1024
- 距离度量：Cosine，L2
- 语言：100+ 种语言
- 最大输入文本 token 数：512（约每个 token 4 个字符）
- 最大输入文本字符数：2,048
- 价格：免费
- 由 TiDB Cloud 托管：✅ `tidbcloud_free/cohere/embed-multilingual-v3`
- 自带密钥（BYOK）：✅ `cohere/embed-multilingual-v3.0`

另外，如果你自带 Cohere API 密钥（BYOK），也可以通过 `cohere/` 前缀使用所有 Cohere 模型。例如：

**Cohere Embed v4 模型**

- 名称：`cohere/embed-v4.0`
- 维度：256、512、1024、1536（默认）
- 距离度量：Cosine，L2
- 最大输入文本 token 数：128,000
- 价格：由 Cohere 收费
- 由 TiDB Cloud 托管：❌
- 自带密钥（BYOK）：✅

完整 Cohere 模型列表请参见 [Cohere Documentation](https://docs.cohere.com/docs/cohere-embed)。

## SQL 使用示例（TiDB Cloud 托管）

以下示例展示了如何结合 Auto Embedding 使用 TiDB Cloud 托管的 Cohere 向量嵌入模型。

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

> **注意：**
>
> - 对于 Cohere 向量嵌入模型，定义表时必须在 `EMBED_TEXT()` 函数中指定 `input_type`。例如，`'{"input_type": "search_document", "input_type@search": "search_query"}'` 表示插入数据时 `input_type` 设为 `search_document`，而在向量搜索时会自动应用 `search_query`。
> - `@search` 后缀表示该字段仅在向量搜索查询时生效，因此在查询时无需再次指定 `input_type`。

插入和查询数据：

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

结果：

```
+------+----------------------------------------------------------------+
| id   | content                                                        |
+------+----------------------------------------------------------------+
|    1 | Java: Object-oriented language for cross-platform development. |
|    4 | Java's syntax is used in Android apps.                         |
+------+----------------------------------------------------------------+
```

## 选项（TiDB Cloud 托管）

**Embed v3** 和 **Multilingual Embed v3** 两个模型均支持以下选项，你可以通过 `EMBED_TEXT()` 函数的 `additional_json_options` 参数进行指定。

- `input_type`（必填）：在嵌入前添加特殊 token，用于指示嵌入的用途。对于同一任务，生成嵌入时必须始终使用相同的 input_type，否则嵌入会被映射到不同的语义空间，导致不兼容。唯一的例外是语义搜索，文档嵌入使用 `search_document`，查询嵌入使用 `search_query`。

    - `search_document`：从文档生成嵌入，用于存储到向量数据库。
    - `search_query`：从查询生成嵌入，用于在向量数据库中搜索已存储的嵌入。
    - `classification`：生成嵌入，作为文本分类器的输入。
    - `clustering`：生成嵌入，用于聚类任务。

- `truncate`（可选）：控制 API 如何处理超出最大 token 长度的输入。可选值如下：

    - `NONE`（默认）：当输入超过最大 token 长度时返回错误。
    - `START`：从开头截断文本，直到输入长度符合要求。
    - `END`：从结尾截断文本，直到输入长度符合要求。

## 使用示例（BYOK）

本示例展示如何使用自带密钥（BYOK）的 Cohere 模型创建向量表、插入文档并进行相似度搜索。

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

在 [Cohere Dashboard](https://dashboard.cohere.com/api-keys) 创建你的 API 密钥，并自带密钥（BYOK）使用嵌入服务。

<SimpleTab groupId="language">
<div label="Python" value="python">

使用 TiDB Client 配置 Cohere 嵌入提供方的 API 密钥：

```python
tidb_client.configure_embedding_provider(
    provider="cohere",
    api_key="{your-cohere-api-key}",
)
```

</div>
<div label="SQL" value="sql">

通过 SQL 设置 Cohere 嵌入提供方的 API 密钥：

```sql
SET @@GLOBAL.TIDB_EXP_EMBED_COHERE_API_KEY = "{your-cohere-api-key}";
```

</div>
</SimpleTab>

### 步骤 3：创建向量表

创建一个包含向量字段的表，使用 `cohere/embed-v4.0` 模型生成 1536 维（默认维度）向量：

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
        model_name="cohere/embed-v4.0"
    ).VectorField(source_field="content")

table = tidb_client.create_table(schema=Document, if_exists="overwrite")
```

</div>
<div label="SQL" value="sql">

```sql
CREATE TABLE sample_documents (
    `id`        INT PRIMARY KEY,
    `content`   TEXT,
    `embedding` VECTOR(1536) GENERATED ALWAYS AS (EMBED_TEXT(
        "cohere/embed-v4.0",
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
    Document(id=1, content="Python: High-level programming language for data science and web development."),
    Document(id=2, content="Python snake: Non-venomous constrictor found in tropical regions."),
    Document(id=3, content="Python framework: Django and Flask are popular web frameworks."),
    Document(id=4, content="Python libraries: NumPy and Pandas for data analysis."),
    Document(id=5, content="Python ecosystem: Rich collection of packages and tools."),
]
table.bulk_insert(documents)
```

</div>
<div label="SQL" value="sql">

使用 `INSERT INTO` 语句插入数据：

```sql
INSERT INTO sample_documents (id, content)
VALUES
    (1, "Python: High-level programming language for data science and web development."),
    (2, "Python snake: Non-venomous constrictor found in tropical regions."),
    (3, "Python framework: Django and Flask are popular web frameworks."),
    (4, "Python libraries: NumPy and Pandas for data analysis."),
    (5, "Python ecosystem: Rich collection of packages and tools.");
```

</div>
</SimpleTab>

### 步骤 5：搜索相似文档

<SimpleTab groupId="language">
<div label="Python" value="python">

使用 `table.search()` API 进行向量搜索：

```python
results = table.search("How to learn Python programming?") \
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
    VEC_EMBED_COSINE_DISTANCE(embedding, "How to learn Python programming?") AS _distance
FROM sample_documents
ORDER BY _distance ASC
LIMIT 2;
```

</div>
</SimpleTab>

## 选项（BYOK）

所有 [Cohere 嵌入选项](https://docs.cohere.com/v2/reference/embed) 均可通过 `EMBED_TEXT()` 函数的 `additional_json_options` 参数进行设置。

**示例：为搜索和插入操作分别指定不同的 `input_type`**

使用 `@search` 后缀，表示该字段仅在向量搜索查询时生效。

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

**示例：使用不同的维度**

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

所有可用选项请参见 [Cohere Documentation](https://docs.cohere.com/v2/reference/embed)。

## 另请参阅

- [Auto Embedding 概览](/ai/integrations/vector-search-auto-embedding-overview.md)
- [向量搜索](/ai/concepts/vector-search-overview.md)
- [向量函数与运算符](/ai/reference/vector-search-functions-and-operators.md)
- [混合搜索](/ai/guides/vector-search-hybrid-search.md)
