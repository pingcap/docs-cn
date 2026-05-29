---
title: 混合搜索
summary: 同时使用全文搜索和向量搜索，以提升搜索质量。
aliases: ['/zh/tidbcloud/vector-search-hybrid-search/']
---

# 混合搜索

通过使用全文搜索，你可以基于精确关键字搜索文档。通过使用向量搜索，你可以基于语义相似性搜索文档。我们能否将这两种搜索方法结合起来，以提升搜索质量并应对更多场景？答案是肯定的，这种方法被称为混合搜索（hybrid search），并在 AI 应用中被广泛采用。

在 TiDB 中，混合搜索的一般工作流程如下：

1. 使用 TiDB 进行**全文搜索**和**向量搜索**。
2. 使用**重排序器**（reranker）将两种搜索的结果进行融合。

![Hybrid Search](/media/vector-search/hybrid-search-overview.svg)

本教程演示如何在 TiDB 中使用 [pytidb](https://github.com/pingcap/pytidb) Python SDK 实现混合搜索，该 SDK 内置了 embedding 和重排序支持。使用 pytidb 并非强制要求——你也可以直接使用 SQL 进行搜索，并根据需要使用自定义的重排序模型。

## 前提条件

全文搜索目前仍处于早期阶段，我们正在持续向更多用户开放。目前，全文搜索仅在以下区域的 TiDB Cloud Starter 和 TiDB Cloud Essential 上可用：

- AWS: `Frankfurt (eu-central-1)` 和 `Singapore (ap-southeast-1)`

要完成本教程，请确保你在受支持的区域拥有一个 TiDB Cloud Starter 实例。如果还没有，请参阅[创建 TiDB Cloud Starter 实例](/develop/dev-guide-build-cluster-in-cloud.md)进行创建。

## 快速开始

### 步骤 1. 安装 [pytidb](https://github.com/pingcap/pytidb) Python SDK

```shell
pip install "pytidb[models]"

# （可选）如果你不想使用内置 embedding 函数和重排序器：
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

你可以通过以下方式在 [TiDB Cloud 控制台](https://tidbcloud.com) 获取这些连接参数：

1. 进入 [**My TiDB**](https://tidbcloud.com/tidbs) 页面，然后点击目标 TiDB Cloud Starter 或 Essential 实例名称，进入其概览页面。

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

   连接到 TiDB Cloud Starter 实例的 Python 代码如下：

   ```python
   db = TiDBClient.connect(
       host="gateway01.us-east-1.prod.shared.aws.tidbcloud.com",
       port=4000,
       username="4EfqPF23YKBxaQb.root",
       password="abcd1234",
       database="test",
   )
   ```

   注意，上述示例仅用于演示。你需要用自己的参数替换，并妥善保管这些信息。

### 步骤 3. 创建表

以创建名为 `chunks` 的表为例，包含以下字段：

- `id`（int）：chunk 的 ID。
- `text`（text）：chunk 的文本内容。
- `text_vec`（vector）：文本的向量表示，由 pytidb 中的 embedding model 自动生成。
- `user_id`（int）：创建该 chunk 的用户 ID。

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
    )  # 👈 定义向量字段。
    user_id: int = Field()

table = db.create_table(schema=Chunk)
```

### 步骤 4. 插入数据

```python
table.bulk_insert(
    [
        Chunk(id=2, text="bar", user_id=2),   # 👈 text 字段会被自动 embedding，
        Chunk(id=3, text="baz", user_id=3),   # 并以向量形式存储到 "text_vec" 字段
        Chunk(id=4, text="qux", user_id=4),   # 中。
    ]
)
```

### 步骤 5. 执行混合搜索

本例中，使用 [jina-reranker](https://huggingface.co/jinaai/jina-reranker-m0) 模型对搜索结果进行重排序。

```python
from pytidb.rerankers import Reranker

jinaai = Reranker(model_name="jina_ai/jina-reranker-m0")

df = (
  table.search("<query>", search_type="hybrid")
    .rerank(jinaai, "text")  # 👈 使用 jinaai 模型对查询结果重排序。
    .limit(2)
    .to_pandas()
)
```

完整示例请参见 [pytidb hybrid search demo](https://github.com/pingcap/pytidb/tree/main/examples/hybrid_search)。

## 融合方法

融合方法将向量（语义）搜索和全文（关键字）搜索的结果合并为统一的排序结果。这确保最终结果既考虑语义相关性，也兼顾关键字匹配。

`pytidb` 支持两种融合方法：

- `rrf`：倒数排名融合（Reciprocal Rank Fusion，默认）
- `weighted`：加权分数融合

你可以根据实际场景选择最适合的融合方法，以优化混合搜索结果。

### 倒数排名融合（RRF）

倒数排名融合（Reciprocal Rank Fusion，RRF）是一种利用文档在多个结果集中的排名来评估搜索结果的算法。

详细信息请参见 [RRF 论文](https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf)。

通过在 `.fusion()` 方法中将 `method` 参数指定为 `"rrf"`，即可启用倒数排名融合。

```python
results = (
    table.search(
        "AI database", search_type="hybrid"
    )
    .fusion(method="rrf")
    .limit(3)
    .to_list()
)
```

参数说明：

- `k`：常数（默认值：60），用于防止除零错误，并控制高排名文档的影响。

### 加权分数融合

加权分数融合通过加权求和的方式，将向量搜索和全文搜索的分数结合起来：

```python
final_score = vs_weight * vector_score + fts_weight * fulltext_score
```

通过在 `.fusion()` 方法中将 `method` 参数指定为 `"weighted"`，即可启用加权分数融合。

例如，如需让向量搜索权重更高，可将 `vs_weight` 设置为 0.7，`fts_weight` 设置为 0.3：

```python
results = (
    table.search(
        "AI database", search_type="hybrid"
    )
    .fusion(method="weighted", vs_weight=0.7, fts_weight=0.3)
    .limit(3)
    .to_list()
)
```

参数说明：

- `vs_weight`：向量搜索分数的权重。
- `fts_weight`：全文搜索分数的权重。

## 重排序方法

混合搜索还支持使用特定模型进行重排序。

通过 `rerank()` 方法，可以指定重排序器，根据 query 与文档之间的相关性对搜索结果进行排序。

**示例：使用 Jina AI Reranker 对混合搜索结果重排序**

```python
reranker = Reranker(
    # 使用 `jina-reranker-m0` 模型
    model_name="jina_ai/jina-reranker-m0",
    api_key="{your-jinaai-api-key}"
)

results = (
    table.search(
        "AI database", search_type="hybrid"
    )
    .fusion(method="rrf", k=60)
    .rerank(reranker, "text")
    .limit(3)
    .to_list()
)
```

如需查看更多重排序模型，请参见 [Reranking](/ai/guides/reranking.md)。

## 另请参阅

- [pytidb Python SDK 文档](https://github.com/pingcap/pytidb)

- [使用 Python 进行全文搜索](/ai/guides/vector-search-full-text-search-python.md)

## 反馈与帮助

全文搜索目前仍处于早期阶段，开放范围有限。如果你希望在尚未开放的区域体验全文搜索，或有任何反馈或需要帮助，欢迎联系我们：

- 在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 社区提问。
- [提交 TiDB Cloud 支持工单](https://tidb.support.pingcap.com/servicedesk/customer/portals)
