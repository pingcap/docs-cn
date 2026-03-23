---
title: Hugging Face 向量嵌入
summary: 了解如何在 TiDB Cloud 中使用 Hugging Face 向量嵌入模型。
aliases: ['/zh/tidbcloud/vector-search-auto-embedding-huggingface/']
---

# Hugging Face 向量嵌入

本文档介绍如何在 TiDB Cloud 中结合 [Auto Embedding](/ai/integrations/vector-search-auto-embedding-overview.md) 使用 Hugging Face 向量嵌入模型，通过文本查询实现语义搜索。

> **注意：**
>
> [Auto Embedding](/ai/integrations/vector-search-auto-embedding-overview.md) 仅适用于托管在 AWS 上的 TiDB Cloud Starter 集群。

## 可用模型

如果你自带 [Hugging Face Inference API](https://huggingface.co/docs/inference-providers/index) 密钥（BYOK），则可以通过 `huggingface/` 前缀使用 Hugging Face 模型。

为方便起见，以下章节以几个流行模型为例。完整可用模型列表请参见 [Hugging Face models](https://huggingface.co/models?library=sentence-transformers&inference_provider=hf-inference&sort=trending)。请注意，并非所有模型都可通过 Hugging Face Inference API 获取，或都能稳定运行。

## multilingual-e5-large

- 名称：`huggingface/intfloat/multilingual-e5-large`
- 维度：1024
- 距离度量：Cosine，L2
- 价格：由 Hugging Face 收费
- TiDB Cloud 托管：❌
- Bring Your Own Key（BYOK，由用户自行提供 API 密钥）：✅
- 项目主页：<https://huggingface.co/intfloat/multilingual-e5-large>

示例：

```sql
SET @@GLOBAL.TIDB_EXP_EMBED_HUGGINGFACE_API_KEY = 'your-huggingface-api-key-here';

CREATE TABLE sample (
  `id`        INT,
  `content`   TEXT,
  `embedding` VECTOR(1024) GENERATED ALWAYS AS (EMBED_TEXT(
                "huggingface/intfloat/multilingual-e5-large",
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

## bge-m3

- 名称：`huggingface/BAAI/bge-m3`
- 维度：1024
- 距离度量：Cosine，L2
- 价格：由 Hugging Face 收费
- TiDB Cloud 托管：❌
- Bring Your Own Key（BYOK，由用户自行提供 API 密钥）：✅
- 项目主页：<https://huggingface.co/BAAI/bge-m3>

```sql
SET @@GLOBAL.TIDB_EXP_EMBED_HUGGINGFACE_API_KEY = 'your-huggingface-api-key-here';

CREATE TABLE sample (
  `id`        INT,
  `content`   TEXT,
  `embedding` VECTOR(1024) GENERATED ALWAYS AS (EMBED_TEXT(
                "huggingface/BAAI/bge-m3",
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

## all-MiniLM-L6-v2

- 名称：`huggingface/sentence-transformers/all-MiniLM-L6-v2`
- 维度：384
- 距离度量：Cosine，L2
- 价格：由 Hugging Face 收费
- TiDB Cloud 托管：❌
- Bring Your Own Key（BYOK，由用户自行提供 API 密钥）：✅
- 项目主页：<https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2>

示例：

```sql
SET @@GLOBAL.TIDB_EXP_EMBED_HUGGINGFACE_API_KEY = 'your-huggingface-api-key-here';

CREATE TABLE sample (
  `id`        INT,
  `content`   TEXT,
  `embedding` VECTOR(384) GENERATED ALWAYS AS (EMBED_TEXT(
                "huggingface/sentence-transformers/all-MiniLM-L6-v2",
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

## all-mpnet-base-v2

- 名称：`huggingface/sentence-transformers/all-mpnet-base-v2`
- 维度：768
- 距离度量：Cosine，L2
- 价格：由 Hugging Face 收费
- TiDB Cloud 托管：❌
- Bring Your Own Key（BYOK，由用户自行提供 API 密钥）：✅
- 项目主页：<https://huggingface.co/sentence-transformers/all-mpnet-base-v2>

```sql
SET @@GLOBAL.TIDB_EXP_EMBED_HUGGINGFACE_API_KEY = 'your-huggingface-api-key-here';

CREATE TABLE sample (
  `id`        INT,
  `content`   TEXT,
  `embedding` VECTOR(768) GENERATED ALWAYS AS (EMBED_TEXT(
                "huggingface/sentence-transformers/all-mpnet-base-v2",
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

## Qwen3-Embedding-0.6B

> **注意：**
>
> Hugging Face Inference API 在该模型上可能不稳定。

- 名称：`huggingface/Qwen/Qwen3-Embedding-0.6B`
- 维度：1024
- 距离度量：Cosine，L2
- 最大输入文本 tokens：512
- 价格：由 Hugging Face 收费
- TiDB Cloud 托管：❌
- Bring Your Own Key（BYOK，由用户自行提供 API 密钥）：✅
- 项目主页：<https://huggingface.co/Qwen/Qwen3-Embedding-0.6B>

```sql
SET @@GLOBAL.TIDB_EXP_EMBED_HUGGINGFACE_API_KEY = 'your-huggingface-api-key-here';

CREATE TABLE sample (
  `id`        INT,
  `content`   TEXT,
  `embedding` VECTOR(1024) GENERATED ALWAYS AS (EMBED_TEXT(
                "huggingface/Qwen/Qwen3-Embedding-0.6B",
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

## Python 使用示例

本示例展示如何创建向量表、插入文档，并使用 Hugging Face 向量嵌入模型进行相似度搜索。

### 步骤 1：连接数据库

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

### 步骤 2：配置 API 密钥

如果你使用私有模型或需要更高的速率限制，可以配置你的 Hugging Face API token。你可以在 [Hugging Face Token Settings](https://huggingface.co/settings/tokens) 页面创建 token：

通过 TiDB Client 为 Hugging Face 模型配置 API token：

```python
tidb_client.configure_embedding_provider(
    provider="huggingface",
    api_key="{your-huggingface-token}",
)
```

### 步骤 3：创建向量表

创建一个包含向量字段的表，使用 Hugging Face 模型生成向量嵌入：

```python
from pytidb.schema import TableModel, Field
from pytidb.embeddings import EmbeddingFunction
from pytidb.datatype import TEXT

class Document(TableModel):
    __tablename__ = "sample_documents"
    id: int = Field(primary_key=True)
    content: str = Field(sa_type=TEXT)
    embedding: list[float] = EmbeddingFunction(
        model_name="huggingface/sentence-transformers/all-MiniLM-L6-v2"
    ).VectorField(source_field="content")

table = tidb_client.create_table(schema=Document, if_exists="overwrite")
```

> **提示：**
>
> 向量维度取决于你选择的模型。例如，`huggingface/sentence-transformers/all-MiniLM-L6-v2` 生成 384 维向量，而 `huggingface/sentence-transformers/all-mpnet-base-v2` 生成 768 维向量。

### 步骤 4：向表中插入数据

使用 `table.insert()` 或 `table.bulk_insert()` API 添加数据：

```python
documents = [
    Document(id=1, content="Machine learning algorithms can identify patterns in data."),
    Document(id=2, content="Deep learning uses neural networks with multiple layers."),
    Document(id=3, content="Natural language processing helps computers understand text."),
    Document(id=4, content="Computer vision enables machines to interpret images."),
    Document(id=5, content="Reinforcement learning learns through trial and error."),
]
table.bulk_insert(documents)
```

### 步骤 5：搜索相似文档

使用 `table.search()` API 进行向量搜索：

```python
results = table.search("How do neural networks work?") \
    .limit(3) \
    .to_list()

for doc in results:
    print(f"ID: {doc.id}, Content: {doc.content}")
```

## 另请参阅

- [Auto Embedding 概览](/ai/integrations/vector-search-auto-embedding-overview.md)
- [向量搜索](/ai/concepts/vector-search-overview.md)
- [向量函数与运算符](/ai/reference/vector-search-functions-and-operators.md)
- [混合搜索](/ai/guides/vector-search-hybrid-search.md)
