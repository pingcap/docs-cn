---
title: OpenAI 向量嵌入
summary: 了解如何在 TiDB Cloud 中使用 OpenAI 向量嵌入模型。
aliases: ['/zh/tidbcloud/vector-search-auto-embedding-openai/']
---

# OpenAI 向量嵌入

本文档介绍如何在 TiDB Cloud 中结合 [Auto Embedding](/ai/integrations/vector-search-auto-embedding-overview.md) 使用 OpenAI 向量嵌入模型，通过文本查询实现语义搜索。

> **注意：**
>
> [Auto Embedding](/ai/integrations/vector-search-auto-embedding-overview.md) 仅适用于托管在 AWS 上的 TiDB Cloud Starter 集群。

## 可用模型

如果你自带 OpenAI API 密钥（BYOK），则所有 OpenAI 模型均可通过 `openai/` 前缀使用。例如：

**text-embedding-3-small**

- 名称：`openai/text-embedding-3-small`
- 维度：512-1536（默认：1536）
- 距离度量：Cosine，L2
- 价格：由 OpenAI 收费
- 由 TiDB Cloud 托管：❌
- 支持 Bring Your Own Key（BYOK，由用户自行提供 API 密钥）：✅

**text-embedding-3-large**

- 名称：`openai/text-embedding-3-large`
- 维度：256-3072（默认：3072）
- 距离度量：Cosine，L2
- 价格：由 OpenAI 收费
- 由 TiDB Cloud 托管：❌
- 支持 Bring Your Own Key（BYOK，由用户自行提供 API 密钥）：✅

完整可用模型列表请参见 [OpenAI Documentation](https://platform.openai.com/docs/guides/embeddings)。

## 使用示例

本示例展示如何创建向量表、插入文档，并使用 OpenAI 向量嵌入模型进行相似度搜索。

你可以通过 AI SDK 或原生 SQL 函数，将 OpenAI 向量嵌入 API 集成到 TiDB，实现 Auto Embedding 生成。

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

在 [OpenAI API Platform](https://platform.openai.com/api-keys) 创建 API 密钥，并自带密钥（BYOK）以使用嵌入服务。

<SimpleTab groupId="language">
<div label="Python" value="python">

使用 TiDB 客户端为 OpenAI 嵌入提供方配置 API 密钥：

```python
tidb_client.configure_embedding_provider(
    provider="openai",
    api_key="{your-openai-api-key}",
)
```

</div>
<div label="SQL" value="sql">

通过 SQL 为 OpenAI 嵌入提供方设置 API 密钥：

```sql
SET @@GLOBAL.TIDB_EXP_EMBED_OPENAI_API_KEY = "{your-openai-api-key}";
```

</div>
</SimpleTab>

### 步骤 3：创建向量表

创建一个包含向量字段的表，使用 `openai/text-embedding-3-small` 模型生成 1536 维向量：

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
        model_name="openai/text-embedding-3-small"
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
        "openai/text-embedding-3-small",
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

使用 `VEC_EMBED_COSINE_DISTANCE` 函数，通过余弦距离进行向量搜索：

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

## 使用 Azure OpenAI

如需在 Azure 上使用 OpenAI 嵌入模型，请将全局变量 `TIDB_EXP_EMBED_OPENAI_API_BASE` 设置为你的 Azure 资源的 URL。例如：

```sql
SET @@GLOBAL.TIDB_EXP_EMBED_OPENAI_API_KEY = 'your-openai-api-key-here';
SET @@GLOBAL.TIDB_EXP_EMBED_OPENAI_API_BASE = 'https://<your-resource-name>.openai.azure.com/openai/v1';

CREATE TABLE sample (
  `id`        INT,
  `content`   TEXT,
  `embedding` VECTOR(3072) GENERATED ALWAYS AS (EMBED_TEXT(
                "openai/text-embedding-3-large",
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

即使你的资源 URL 形如 `https://<your-resource-name>.cognitiveservices.azure.com/`，也必须使用 `https://<your-resource-name>.openai.azure.com/openai/v1` 作为 API base，以保持 OpenAI 兼容的请求和响应格式。

如需从 Azure OpenAI 切换回 OpenAI 官方服务，将 `TIDB_EXP_EMBED_OPENAI_API_BASE` 设置为空字符串：

```sql
SET @@GLOBAL.TIDB_EXP_EMBED_OPENAI_API_BASE = '';
```

> **注意：**
>
> - 出于安全考虑，API base 只能设置为 Azure OpenAI URL 或 OpenAI URL。不允许设置为任意 base URL。
> - 如需使用其他 OpenAI 兼容的嵌入服务，请联系 [TiDB Cloud Support](https://docs.pingcap.com/zh/tidbcloud/tidb-cloud-support/)。

## 选项

所有 [OpenAI 嵌入选项](https://platform.openai.com/docs/api-reference/embeddings/create) 均可通过 `EMBED_TEXT()` 函数的 `additional_json_options` 参数支持。

**示例：为 text-embedding-3-large 使用自定义维度**

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

所有可用选项请参见 [OpenAI Documentation](https://platform.openai.com/docs/api-reference/embeddings/create)。

## 另请参阅

- [Auto Embedding 概览](/ai/integrations/vector-search-auto-embedding-overview.md)
- [向量搜索](/ai/concepts/vector-search-overview.md)
- [向量函数与操作符](/ai/reference/vector-search-functions-and-operators.md)
- [混合搜索](/ai/guides/vector-search-hybrid-search.md)