---
title: Auto Embedding
summary: 了解如何在你的应用程序中使用 Auto Embedding 功能。
---

# Auto Embedding

Auto Embedding 功能会为你的文本数据自动生成向量嵌入。

> **注意：**
>
> 有关 Auto Embedding 的完整示例，请参见 [Auto Embedding Example](/ai/examples/auto-embedding-with-pytidb.md)。

## 基本用法

本文档使用 TiDB Cloud 托管的嵌入模型进行演示。有关支持的全部提供商列表，请参见 [Auto Embedding Overview](/ai/integrations/vector-search-auto-embedding-overview.md#available-text-embedding-models)。

### 第 1 步. 定义嵌入函数

定义一个嵌入函数，用于为你的文本数据生成向量嵌入。

```python
from pytidb.embeddings import EmbeddingFunction

embed_func = EmbeddingFunction(
    model_name="tidbcloud_free/amazon/titan-embed-text-v2",
)
```

### 第 2 步. 创建表和向量字段

使用 `embed_func.VectorField()` 在表结构中创建一个向量字段。

要启用 Auto Embedding，请将 `source_field` 设置为你想要嵌入的字段。

```python hl_lines="7"
from pytidb.schema import TableModel, Field
from pytidb.datatype import TEXT

class Chunk(TableModel):
    id: int = Field(primary_key=True)
    text: str = Field(sa_type=TEXT)
    text_vec: list[float] = embed_func.VectorField(source_field="text")

table = client.create_table(schema=Chunk, if_exists="overwrite")
```

你无需指定 `dimensions` 参数，因为嵌入模型会自动确定维度。

不过，你也可以设置 `dimensions` 参数来覆盖默认维度。

### 第 3 步. 插入一些示例数据

向表中插入一些示例数据。

```python
table.bulk_insert([
    Chunk(text="TiDB is a distributed database that supports OLTP, OLAP, HTAP and AI workloads."),
    Chunk(text="PyTiDB is a Python library for developers to connect to TiDB."),
    Chunk(text="LlamaIndex is a Python library for building AI-powered applications."),
])
```

插入数据时，`text_vec` 字段会自动被由 `text` 生成的嵌入向量填充。

### 第 4 步. 执行向量查询

你可以将查询文本直接传递给 `search()` 方法。查询文本会被 Auto Embedding，然后用于向量查询。

```python
table.search("HTAP database").limit(3).to_list()
```