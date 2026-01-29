---
title: Hybrid Search
summary: 同时使用全文检索和向量检索以提升检索质量。
aliases: ['/tidb/stable/vector-search-hybrid-search','/zh/tidbcloud/vector-search-hybrid-search/']
---

# Hybrid Search <!-- Draft translated by AI -->

通过使用全文检索，你可以基于精确关键词检索文档。通过使用向量检索，你可以基于语义相似度检索文档。那么，我们能否将这两种检索方式结合起来，以提升检索质量并覆盖更多场景？答案是可以，这种方法被称为混合检索（hybrid search），并且在 AI 应用中被广泛使用。

在 TiDB 中，混合检索的一般流程如下：

1. 使用 TiDB 进行 **全文检索** 和 **向量检索**。
2. 使用 **reranker**（重排序器）对两种检索结果进行融合。

![Hybrid Search](/media/vector-search/hybrid-search-overview.svg)

本教程演示了如何在 TiDB 中使用 [pytidb](https://github.com/pingcap/pytidb) Python SDK 实现混合检索，该 SDK 内置了 embedding 和 reranking 支持。使用 pytidb 并非强制要求 —— 你也可以直接使用 SQL 进行检索，并根据需要使用自定义的 reranking 模型。

## 前置条件

全文检索目前仍处于早期阶段，我们正在持续向更多用户开放。目前，全文检索仅在以下区域的 TiDB Cloud Starter 和 TiDB Cloud Essential 上可用：

- AWS: `Frankfurt (eu-central-1)` 和 `Singapore (ap-southeast-1)`

要完成本教程，请确保你在支持的区域拥有一个 TiDB Cloud Starter 集群。如果还没有，请参考 [创建 TiDB Cloud Starter 集群](/develop/dev-guide-build-cluster-in-cloud.md) 进行创建。

## 快速开始

### 步骤 1. 安装 [pytidb](https://github.com/pingcap/pytidb) Python SDK

```shell
pip install "pytidb[models]"

# （可选）如果你不想使用内置的 embedding 函数和 reranker：
# pip install pytidb

# （可选）如需将查询结果转换为 pandas DataFrame：
# pip install pandas
```

### 步骤 2. 连接 TiDB

```python
from pytidb import TiDBClient

db = TiDBClient.connect(
    host="HOST_HERE",
    port=4000,
    username="USERNAME_HERE",
    password="PASSWORD_HERE",
    database="DATABASE_HERE",
)
```

你可以在 [TiDB Cloud 控制台](https://tidbcloud.com) 获取这些连接参数：

1. 进入 [**Clusters**](https://tidbcloud.com/project/clusters) 页面，点击目标集群名称进入集群概览页。

2. 点击右上角的 **Connect**，弹出连接对话框，显示连接参数。

   例如，连接参数如下所示：

   ```text
   HOST:     gateway01.us-east-1.prod.shared.aws.tidbcloud.com
   PORT:     4000
   USERNAME: 4EfqPF23YKBxaQb.root
   PASSWORD: abcd1234
   DATABASE: test
   CA:       /etc/ssl/cert.pem
   ```

   则连接 TiDB Cloud Starter 集群的 Python 代码如下：

   ```python
   db = TiDBClient.connect(
       host="gateway01.us-east-1.prod.shared.aws.tidbcloud.com",
       port=4000,
       username="4EfqPF23YKBxaQb.root",
       password="abcd1234",
       database="test",
   )
   ```

   注意，上述示例仅用于演示。你需要使用自己的参数，并妥善保管。

### 步骤 3. 创建数据表

以创建名为 `chunks` 的表为例，包含以下字段：

- `id` (int)：chunk 的 ID。
- `text` (text)：chunk 的文本内容。
- `text_vec` (vector)：文本的向量表示，由 pytidb 中的 embedding 模型自动生成。
- `user_id` (int)：创建该 chunk 的用户 ID。

```python
from pytidb.schema import TableModel, Field
from pytidb.embeddings import EmbeddingFunction

text_embed = EmbeddingFunction("openai/text-embedding-3-small")

class Chunk(TableModel, table=True):
    __tablename__ = "chunks"

    id: int = Field(primary_key=True)
    text: str = Field()
    text_vec: list[float] = text_embed.VectorField(
        source_field="text"
    )  # 👈 Define the vector field.
    user_id: int = Field()

table = db.create_table(schema=Chunk)
```

### 步骤 4. 插入数据

```python
table.bulk_insert(
    [
        Chunk(id=2, text="bar", user_id=2),   # 👈 The text field will be embedded to a
        Chunk(id=3, text="baz", user_id=3),   # vector and stored in the "text_vec" field
        Chunk(id=4, text="qux", user_id=4),   # automatically.
    ]
)
```

### 步骤 5. 执行混合检索

本例中，使用 [jina-reranker](https://huggingface.co/jinaai/jina-reranker-m0) 模型对检索结果进行重排序。

```python
from pytidb.rerankers import Reranker

jinaai = Reranker(model_name="jina_ai/jina-reranker-m0")

df = (
  table.search("<query>", search_type="hybrid")
    .rerank(jinaai, "text")  # 👈 Rerank the query result using the jinaai model.
    .limit(2)
    .to_pandas()
)
```

完整示例请参考 [pytidb hybrid search demo](https://github.com/pingcap/pytidb/tree/main/examples/hybrid_search)。

## 相关阅读

- [pytidb Python SDK 文档](https://github.com/pingcap/pytidb)

- [使用 Python 进行全文检索](/ai/vector-search-full-text-search-python.md)

## 反馈与帮助

全文检索目前仍处于早期阶段，开放范围有限。如果你希望在尚未开放的区域体验全文检索，或有任何反馈与帮助需求，欢迎联系我们：

<CustomContent platform="tidb">

- [加入我们的 Discord](https://discord.gg/zcqexutz2R)

</CustomContent>

<CustomContent platform="tidb-cloud">

- [加入我们的 Discord](https://discord.gg/zcqexutz2R)
- [访问我们的支持门户](https://tidb.support.pingcap.com/)

</CustomContent>