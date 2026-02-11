---
title: OpenAI-Compatible Embeddings
summary: 了解如何将 TiDB 向量搜索与 OpenAI 兼容的 embedding 模型集成，以存储 embedding 并执行语义搜索。
---

# OpenAI-Compatible Embeddings

本教程演示如何使用 OpenAI 兼容的 embedding 服务生成文本 embedding，将其存储到 TiDB，并执行语义搜索。

> **注意：**
>
> 目前，[Auto Embedding](/ai/integrations/vector-search-auto-embedding-overview.md) 仅在托管于 AWS 的 TiDB Cloud Starter 集群上可用。

## OpenAI 兼容的 embedding 服务

由于 OpenAI Embedding API 被广泛使用，许多提供商都提供兼容的 API，例如：

- [Ollama](https://ollama.com/)
- [vLLM](https://vllm.ai/)

TiDB Python SDK [pytidb](https://github.com/pingcap/pytidb) 提供了 `EmbeddingFunction` 类，用于集成 OpenAI 兼容的 embedding 服务。

## 使用示例

本示例展示如何创建向量表、插入文档，并使用 OpenAI 兼容的 embedding 模型进行相似度搜索。

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

### 步骤 2：定义 embedding 函数

要集成 OpenAI 兼容的 embedding 服务，需要初始化 `EmbeddingFunction` 类，并将 `model_name` 参数设置为带有 `openai/` 前缀的值。

```python
from pytidb.embeddings import EmbeddingFunction

openai_like_embed = EmbeddingFunction(
    model_name="openai/{model_name}",
    api_base="{your-api-base}",
    api_key="{your-api-key}",
)
```

参数说明：

- `model_name`：指定要使用的模型。格式为 `openai/{model_name}`。
- `api_base`：你的 OpenAI 兼容 embedding API 服务的基础 URL。
- `api_key`：用于认证 embedding API 服务的 API 密钥。

**示例：使用 Ollama 的 `nomic-embed-text` 模型**

```python
openai_like_embed = EmbeddingFunction(
    model_name="openai/nomic-embed-text",
    api_base="http://localhost:11434/v1",
)
```

**示例：使用 vLLM 的 `intfloat/e5-mistral-7b-instruct` 模型**

```python
openai_like_embed = EmbeddingFunction(
    model_name="openai/intfloat/e5-mistral-7b-instruct",
    api_base="http://localhost:8000/v1"
)
```

### 步骤 3：创建向量表

创建一个包含向量字段的表，使用 Ollama 和 `nomic-embed-text` 模型。

```python
from pytidb.schema import TableModel, Field
from pytidb.embeddings import EmbeddingFunction
from pytidb.datatype import TEXT

openai_like_embed = EmbeddingFunction(
    model_name="openai/nomic-embed-text",
    api_base="{your-api-base}",
)

class Document(TableModel):
    __tablename__ = "sample_documents"
    id: int = Field(primary_key=True)
    content: str = Field(sa_type=TEXT)
    embedding: list[float] = openai_like_embed.VectorField(source_field="content")

table = tidb_client.create_table(schema=Document, if_exists="overwrite")
```

### 步骤 4：向表中插入数据

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

启用 [Auto Embedding](/ai/integrations/vector-search-auto-embedding-overview.md) 后，TiDB 会在插入数据时自动生成向量值。

### 步骤 5：搜索相似文档

使用 `table.search()` API 执行向量搜索：

```python
results = table.search("How to start learning Java programming?") \
    .limit(2) \
    .to_list()
print(results)
```

启用 [Auto Embedding](/ai/integrations/vector-search-auto-embedding-overview.md) 后，TiDB 会在向量搜索时自动为查询文本生成 embedding。