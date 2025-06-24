---
title: 混合搜索
summary: 结合全文搜索和向量搜索来提升检索质量。
---

# 混合搜索

通过使用全文搜索，您可以基于精确关键词检索文档。通过使用向量搜索，您可以基于语义相似度检索文档。我们能否结合这两种搜索方法来提升检索质量并处理更多场景？是的，这种方法被称为混合搜索，在 AI 应用中被广泛使用。

TiDB 中混合搜索的一般工作流程如下：

1. 使用 TiDB 进行**全文搜索**和**向量搜索**。
2. 使用**重排序器**来组合两种搜索的结果。

![混合搜索](/media/vector-search/hybrid-search-overview.svg)

本教程演示如何使用 [pytidb](https://github.com/pingcap/pytidb) Python SDK 在 TiDB 中使用混合搜索，该 SDK 内置支持嵌入和重排序功能。使用 pytidb 完全是可选的 — 您可以直接使用 SQL 执行搜索，并根据需要使用自己的重排序模型。

## 前提条件

混合搜索依赖于[全文搜索](/tidb-cloud/vector-search-full-text-search-python.md)和向量搜索。全文搜索仍处于早期阶段，我们正在持续向更多客户推出。目前，全文搜索仅适用于以下产品选项和地区：

- TiDB Cloud Serverless：`法兰克福 (eu-central-1)` 和 `新加坡 (ap-southeast-1)`

要完成本教程，请确保您在支持的地区有一个 TiDB Cloud Serverless 集群。如果您还没有，请按照[创建 TiDB Cloud Serverless 集群](/develop/dev-guide-build-cluster-in-cloud.md)的说明创建一个。

## 开始使用

### 步骤 1. 安装 [pytidb](https://github.com/pingcap/pytidb) Python SDK

```shell
pip install "pytidb[models]"

# (替代方案) 如果您不想使用内置的嵌入函数和重排序器：
# pip install pytidb

# (可选) 要将查询结果转换为 pandas DataFrame：
# pip install pandas
```

### 步骤 2. 连接到 TiDB

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

您可以从 [TiDB Cloud 控制台](https://tidbcloud.com)获取这些连接参数：

1. 导航到[**集群**](https://tidbcloud.com/project/clusters)页面，然后点击目标集群的名称进入其概览页面。

2. 点击右上角的**连接**。将显示一个连接对话框，其中列出了连接参数。

   例如，如果连接参数显示如下：

   ```text
   HOST:     gateway01.us-east-1.prod.shared.aws.tidbcloud.com
   PORT:     4000
   USERNAME: 4EfqPF23YKBxaQb.root
   PASSWORD: abcd1234
   DATABASE: test
   CA:       /etc/ssl/cert.pem
   ```

   连接到 TiDB Cloud Serverless 集群的相应 Python 代码如下：

   ```python
   db = TiDBClient.connect(
       host="gateway01.us-east-1.prod.shared.aws.tidbcloud.com",
       port=4000,
       username="4EfqPF23YKBxaQb.root",
       password="abcd1234",
       database="test",
   )
   ```

   请注意，上述示例仅用于演示目的。您需要使用自己的值填充参数并确保它们的安全性。

### 步骤 3. 创建表

作为示例，创建一个名为 `chunks` 的表，包含以下列：

- `id` (int)：块的 ID。
- `text` (text)：块的文本内容。
- `text_vec` (vector)：文本的向量表示，由 pytidb 中的嵌入模型自动生成。
- `user_id` (int)：创建该块的用户 ID。

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
        Chunk(id=2, text="bar", user_id=2),   # 👈 文本字段将被自动嵌入为向量
        Chunk(id=3, text="baz", user_id=3),   # 并存储在 "text_vec" 字段中。
        Chunk(id=4, text="qux", user_id=4),   # 
    ]
)
```

### 步骤 5. 执行混合搜索

在此示例中，使用 [jina-reranker](https://huggingface.co/jinaai/jina-reranker-m0) 模型对搜索结果进行重排序。

```python
from pytidb.rerankers import Reranker

jinaai = Reranker(model_name="jina_ai/jina-reranker-m0")

df = (
  table.search("<query>", search_type="hybrid")
    .rerank(jinaai, "text")  # 👈 使用 jinaai 模型对查询结果进行重排序。
    .limit(2)
    .to_pandas()
)
```

完整示例请参见 [pytidb 混合搜索演示](https://github.com/pingcap/pytidb/tree/main/examples/hybrid_search)。

## 另请参阅

- [pytidb Python SDK 文档](https://github.com/pingcap/pytidb)

- [使用 Python 进行全文搜索](/tidb-cloud/vector-search-full-text-search-python.md)

## 反馈与帮助

全文搜索仍处于早期阶段，可访问性有限。如果您想在尚未提供服务的地区尝试全文搜索，或者如果您有反馈或需要帮助，请随时联系我们：

<CustomContent platform="tidb">

- [加入我们的 Discord](https://discord.gg/zcqexutz2R)

</CustomContent>

<CustomContent platform="tidb-cloud">

- [加入我们的 Discord](https://discord.gg/zcqexutz2R)
- [访问我们的支持门户](https://tidb.support.pingcap.com/)

</CustomContent>
