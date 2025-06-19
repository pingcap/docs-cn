---
title: 使用 Python 进行全文搜索
summary: 全文搜索允许您检索精确关键词的文档。在检索增强生成（RAG）场景中，您可以将全文搜索与向量搜索结合使用，以提高检索质量。
---

# 使用 Python 进行全文搜索

与专注于语义相似性的[向量搜索](/tidb-cloud/vector-search-overview.md)不同，全文搜索允许您检索精确关键词的文档。在检索增强生成（RAG）场景中，您可以将全文搜索与向量搜索结合使用，以提高检索质量。

TiDB 的全文搜索功能提供以下能力：

- **直接查询文本数据**：您可以直接搜索任何字符串列，无需进行嵌入处理。

- **支持多种语言**：无需指定语言即可进行高质量搜索。TiDB 支持在同一个表中存储多种语言的文档，并自动为每个文档选择最佳的文本分析器。

- **按相关性排序**：搜索结果可以使用广泛采用的 [BM25 排序](https://en.wikipedia.org/wiki/Okapi_BM25)算法按相关性排序。

- **完全兼容 SQL**：所有 SQL 功能，如预过滤、后过滤、分组和连接，都可以与全文搜索一起使用。

> **提示：**
>
> 关于 SQL 用法，请参见[使用 SQL 进行全文搜索](/tidb-cloud/vector-search-full-text-search-sql.md)。
>
> 要在 AI 应用中同时使用全文搜索和向量搜索，请参见[混合搜索](/tidb-cloud/vector-search-hybrid-search.md)。

## 前提条件

全文搜索仍处于早期阶段，我们正在持续向更多客户推出。目前，全文搜索仅适用于以下产品选项和地区：

- TiDB Cloud Serverless：`法兰克福 (eu-central-1)` 和 `新加坡 (ap-southeast-1)`

要完成本教程，请确保您在支持的地区有一个 TiDB Cloud Serverless 集群。如果您还没有，请按照[创建 TiDB Cloud Serverless 集群](/develop/dev-guide-build-cluster-in-cloud.md)的说明创建一个。

## 开始使用

### 步骤 1. 安装 [pytidb](https://github.com/pingcap/pytidb) Python SDK

[pytidb](https://github.com/pingcap/pytidb) 是 TiDB 的官方 Python SDK，旨在帮助开发者高效构建 AI 应用。它内置支持向量搜索和全文搜索。

要安装 SDK，请运行以下命令：

```shell
pip install pytidb

# （替代方案）要使用内置的嵌入函数和重排序器：
# pip install "pytidb[models]"

# （可选）要将查询结果转换为 pandas DataFrame：
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

2. 点击右上角的**连接**。将显示一个连接对话框，列出连接参数。

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

### 步骤 3. 创建表和全文索引

以下是一个示例，创建一个名为 `chunks` 的表，包含以下列：

- `id` (int)：块的 ID。
- `text` (text)：块的文本内容。
- `user_id` (int)：创建块的用户 ID。

```python
from pytidb.schema import TableModel, Field

class Chunk(TableModel, table=True):
    __tablename__ = "chunks"

    id: int = Field(primary_key=True)
    text: str = Field()
    user_id: int = Field()

table = db.create_table(schema=Chunk)

if not table.has_fts_index("text"):
    table.create_fts_index("text")   # 👈 在文本列上创建全文索引。
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

### 步骤 5. 执行全文搜索

插入数据后，您可以按如下方式执行全文搜索：

```python
df = (
  table.search("brown fox", search_type="fulltext")
    .limit(2)
    .to_pandas() # 可选
)

#    id             text  user_id
# 0   3        fox jumps        3
# 1   2  the quick brown        2
```

完整示例请参见 [pytidb 全文搜索演示](https://github.com/pingcap/pytidb/blob/main/examples/fulltext_search)。

## 另请参阅

- [pytidb Python SDK 文档](https://github.com/pingcap/pytidb)

- [混合搜索](/tidb-cloud/vector-search-hybrid-search.md)

## 反馈与帮助

全文搜索仍处于早期阶段，可用性有限。如果您想在尚未提供服务的地区尝试全文搜索，或者如果您有反馈或需要帮助，请随时联系我们：

<CustomContent platform="tidb">

- [加入我们的 Discord](https://discord.gg/zcqexutz2R)

</CustomContent>

<CustomContent platform="tidb-cloud">

- [加入我们的 Discord](https://discord.gg/zcqexutz2R)
- [访问我们的支持门户](https://tidb.support.pingcap.com/)

</CustomContent>
