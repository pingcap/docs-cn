---
title: 使用 Python 进行全文检索
summary: 全文检索允许你根据精确的关键词检索文档。在 RAG（检索增强生成）场景中，你可以将全文检索与向量检索结合使用，以提升检索质量。
aliases: ['/tidb/stable/vector-search-full-text-search-python']
---

# 使用 Python 进行全文检索 <!-- Draft translated by AI -->

与关注语义相似度的 [向量检索](/vector-search/vector-search-overview.md) 不同，全文检索允许你根据精确的关键词检索文档。在 RAG（检索增强生成）场景中，你可以将全文检索与向量检索结合使用，以提升检索质量。

TiDB 的全文检索功能提供以下能力：

- **直接查询文本数据**：你可以直接在任意字符串列上进行检索，无需进行嵌入处理。

- **多语言支持**：无需指定语言即可获得高质量检索。TiDB 支持在同一张表中存储多种语言的文档，并会为每个文档自动选择最佳的文本分析器。

- **按相关性排序**：检索结果可以使用被广泛采用的 [BM25 排序](https://en.wikipedia.org/wiki/Okapi_BM25) 算法按相关性排序。

- **完全兼容 SQL**：所有 SQL 功能，如预过滤、后过滤、分组和关联查询，都可以与全文检索结合使用。

> **提示：**
>
> 有关 SQL 用法，参见 [使用 SQL 进行全文检索](/ai/vector-search-full-text-search-sql.md)。
>
> 如需在 AI 应用中同时使用全文检索和向量检索，参见 [混合检索](/ai/vector-search-hybrid-search.md)。

## 前提条件

全文检索目前仍处于早期阶段，我们正在持续向更多用户开放。目前，全文检索仅在以下区域的 TiDB Cloud Starter 和 TiDB Cloud Essential 上可用：

- AWS：`法兰克福 (eu-central-1)` 和 `新加坡 (ap-southeast-1)`

要完成本教程，请确保你在支持的区域拥有一个 TiDB Cloud Starter 集群。如果还没有，请按照 [创建 TiDB Cloud Starter 集群](/develop/dev-guide-build-cluster-in-cloud.md) 创建。

## 快速开始

### 步骤 1. 安装 [pytidb](https://github.com/pingcap/pytidb) Python SDK

[pytidb](https://github.com/pingcap/pytidb) 是 TiDB 官方的 Python SDK，旨在帮助开发者高效构建 AI 应用。该 SDK 内置了对向量检索和全文检索的支持。

安装 SDK，请运行以下命令：

```shell
pip install pytidb

# （可选）如需使用内置的 embedding 函数和 reranker：
# pip install "pytidb[models]"

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

   对应的 Python 代码如下：

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

### 步骤 3. 创建表和全文索引

以创建名为 `chunks` 的表为例，包含以下字段：

- `id` (int)：分块的 ID。
- `text` (text)：分块的文本内容。
- `user_id` (int)：创建该分块的用户 ID。

```python
from pytidb.schema import TableModel, Field

class Chunk(TableModel, table=True):
    __tablename__ = "chunks"

    id: int = Field(primary_key=True)
    text: str = Field()
    user_id: int = Field()

table = db.create_table(schema=Chunk)

if not table.has_fts_index("text"):
    table.create_fts_index("text")   # 👈 在 text 列上创建全文索引。
```

### 步骤 4. 插入数据

```python
table.bulk_insert(
    [
        Chunk(id=2, text="the quick brown", user_id=2),
        Chunk(id=3, text="fox jumps", user_id=3),
        Chunk(id=4, text="over the lazy dog", user_id=4),
    ]
)
```

### 步骤 5. 执行全文检索

插入数据后，你可以按如下方式进行全文检索：

```python
df = (
  table.search("brown fox", search_type="fulltext")
    .limit(2)
    .to_pandas() # optional
)

#    id             text  user_id
# 0   3        fox jumps        3
# 1   2  the quick brown        2
```

完整示例参见 [pytidb full-text search demo](https://github.com/pingcap/pytidb/blob/main/examples/fulltext_search)。

## 相关链接

- [pytidb Python SDK 文档](https://github.com/pingcap/pytidb)

- [混合检索](/ai/vector-search-hybrid-search.md)

## 反馈与帮助

全文检索目前仍处于早期阶段，开放范围有限。如果你希望在尚未开放的区域体验全文检索，或有任何反馈和帮助需求，欢迎联系我们：

<CustomContent platform="tidb">

- [加入我们的 Discord](https://discord.gg/zcqexutz2R)

</CustomContent>

<CustomContent platform="tidb-cloud">

- [加入我们的 Discord](https://discord.gg/zcqexutz2R)
- [访问我们的支持门户](https://tidb.support.pingcap.com/)

</CustomContent>
