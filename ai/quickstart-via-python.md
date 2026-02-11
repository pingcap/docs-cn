---
title: 使用 Python 快速上手 TiDB + AI
summary: 学习如何使用 Python SDK 在 TiDB 中开始向量搜索。
aliases: ['/zh/tidb/stable/vector-search-get-started-using-python/','/zh/tidb/dev/vector-search-get-started-using-python/','/zh/tidbcloud/vector-search-get-started-using-python/']
---

# 使用 Python 快速上手 TiDB + AI

本文档演示了如何使用 Python SDK 在 TiDB 中开始 [向量搜索](/ai/concepts/vector-search-overview.md)。跟随本文中的步骤，你将构建你的第一个基于 TiDB 的 AI 应用。

通过学习本教程，你将掌握：

- 使用 TiDB Python SDK 连接 TiDB。
- 利用主流嵌入模型生成文本嵌入向量。
- 将向量存储到 TiDB 表中。
- 使用向量相似度进行语义搜索。

> **注意：**
>
> - 向量搜索功能目前为 beta 版本，可能会在未提前通知的情况下发生变更。如果你发现了 bug，可以在 GitHub 上提交 [issue](https://github.com/pingcap/tidb/issues)。
> - 向量搜索功能适用于 [TiDB 自托管](/overview.md)、[TiDB Cloud Starter](https://docs.pingcap.com/zh/tidbcloud/select-cluster-tier/#starter)、[TiDB Cloud Essential](https://docs.pingcap.com/zh/tidbcloud/select-cluster-tier/#essential) 和 [TiDB Cloud Dedicated](https://docs.pingcap.com/zh/tidbcloud/select-cluster-tier/#tidb-cloud-dedicated)。对于 TiDB 自托管和 TiDB Cloud Dedicated，TiDB 版本需为 v8.4.0 或更高（推荐 v8.5.0 及以上）。

## 前置条件

- 访问 [tidbcloud.com](https://tidbcloud.com/) 免费创建一个 TiDB Cloud Starter 集群，或使用 [tiup playground](https://docs.pingcap.com/tidb/stable/quick-start-with-tidb/#deploy-a-local-test-cluster) 在本地部署一个 TiDB 集群进行测试。

## 安装

[pytidb](https://github.com/pingcap/pytidb) 是官方的 TiDB Python SDK，旨在帮助开发者高效构建 AI 应用。

安装 Python SDK，请运行以下命令：

```bash
pip install pytidb
```

如需使用内置嵌入 function，可安装 `models` 扩展（可选）：

```bash
pip install "pytidb[models]"
```

## 连接数据库

<SimpleTab>
<div label="TiDB Cloud Starter">

你可以在 [TiDB Cloud 控制台](https://tidbcloud.com/clusters) 获取这些连接参数：

1. 进入 [Clusters 页面](https://tidbcloud.com/clusters)，点击目标集群名称进入其概览页面。
2. 点击右上角的 **Connect**。此时会弹出连接对话框，显示连接参数。

例如，连接参数如下所示：

```text
HOST:     gateway01.us-east-1.prod.shared.aws.tidbcloud.com
PORT:     4000
USERNAME: 4EfqPF23YKBxaQb.root
PASSWORD: abcd1234
DATABASE: test
CA:       /etc/ssl/cert.pem
```

对应的 Python 代码如下，用于连接 TiDB Cloud Starter 集群：

```python
from pytidb import TiDBClient

client = TiDBClient.connect(
    host="gateway01.us-east-1.prod.shared.aws.tidbcloud.com",
    port=4000,
    username="4EfqPF23YKBxaQb.root",
    password="abcd1234",
    database="test",
)
```

> **注意：**
>
> 上述示例仅用于演示。你需要使用你自己的参数，并妥善保管。

</div>
<div label="TiDB 自托管">

以下是连接 TiDB 自托管的基本示例：

```python
from pytidb import TiDBClient

client = TiDBClient.connect(
    host="localhost",
    port=4000,
    username="root",
    password="",
    database="test",
    ensure_db=True,
)
```

> **注意：**
>
> 请根据你的实际部署情况 update 连接参数。

</div>
</SimpleTab>

连接成功后，你可以使用 `client` 对象进行表操作、数据查询等。

## 创建嵌入 function

在使用 [嵌入模型](/ai/concepts/vector-search-overview.md#embedding-model) 时，你可以利用嵌入 function 在插入和查询阶段自动将数据向量化。该功能原生支持 OpenAI、Jina AI、Hugging Face、Sentence Transformers 等主流嵌入模型。

<SimpleTab>
<div label="OpenAI">

前往 [OpenAI 平台](https://platform.openai.com/api-keys) 创建你的 API key 用于嵌入。

```python
from pytidb.embeddings import EmbeddingFunction

text_embed = EmbeddingFunction(
    model_name="openai/text-embedding-3-small",
    api_key="<your-openai-api-key>",
)
```

</div>
<div label="Jina AI">

前往 [Jina AI](https://jina.ai/embeddings/) 创建你的 API key 用于嵌入。

```python
from pytidb.embeddings import EmbeddingFunction

text_embed = EmbeddingFunction(
    model_name="jina/jina-embeddings-v3",
    api_key="<your-jina-api-key>",
)
```

</div>
</SimpleTab>

## 创建表

例如，创建一个名为 `chunks` 的表，包含以下字段：

- `id` (int)：chunk 的 ID。
- `text` (text)：chunk 的文本内容。
- `text_vec` (vector)：文本的向量嵌入。
- `user_id` (int)：创建该 chunk 的用户 ID。

```python hl_lines="6"
from pytidb.schema import TableModel, Field, VectorField

class Chunk(TableModel):
    id: int | None = Field(default=None, primary_key=True)
    text: str = Field()
    text_vec: list[float] = text_embed.VectorField(source_field="text")
    user_id: int = Field()

table = client.create_table(schema=Chunk, if_exists="overwrite")
```

创建完成后，你可以使用 `table` 对象插入数据、搜索数据等。

## 插入数据

现在让我们向表中添加一些示例数据。

```python
table.bulk_insert([
    # 👇 文本会被 Auto Embedding 并填充到 `text_vec` 字段中。
    Chunk(text="PyTiDB is a Python library for developers to connect to TiDB.", user_id=2),
    Chunk(text="LlamaIndex is a framework for building AI applications.", user_id=2),
    Chunk(text="OpenAI is a company and platform that provides AI models service and tools.", user_id=3),
])
```

## 搜索最近邻

要搜索给定 query 的最近邻，可以使用 `table.search()` method。该 method 默认执行 [向量搜索](/ai/guides/vector-search.md)。

```python
table.search(
    # 👇 直接传入 query 文本，会 Auto Embedding 为 query 向量。
    "A library for my artificial intelligence software"
)
.limit(3).to_list()
```

在本例中，向量搜索会将 query 向量与 `chunks` 表中 `text_vec` 字段存储的向量进行比较，并根据相似度得分返回最相关的前 3 条结果。

`_distance` 越小，表示两个向量越相似。

```json title="期望输出"
[
    {
        'id': 2,
        'text': 'LlamaIndex is a framework for building AI applications.',
        'text_vec': [...],
        'user_id': 2,
        '_distance': 0.5719928358786761,
        '_score': 0.4280071641213239
    },
    {
        'id': 3,
        'text': 'OpenAI is a company and platform that provides AI models service and tools.',
        'text_vec': [...],
        'user_id': 3,
        '_distance': 0.603133726213383,
        '_score': 0.396866273786617
    },
    {
        'id': 1,
        'text': 'PyTiDB is a Python library for developers to connect to TiDB.',
        'text_vec': [...],
        'user_id': 2,
        '_distance': 0.6202191842385758,
        '_score': 0.3797808157614242
    }
]
```

## 删除数据

要从表中删除指定行，可以使用 `table.delete()` method：

```python
table.delete({
    "id": 1
})
```

## 删除表

当你不再需要某个表时，可以使用 `client.drop_table()` method 删除：

```python
client.drop_table("chunks")
```

## 后续步骤

- 了解 TiDB 中 [向量搜索](/ai/guides/vector-search.md)、[全文搜索](/ai/guides/vector-search-full-text-search-python.md) 和 [混合搜索](/ai/guides/vector-search-hybrid-search.md) 的更多细节。