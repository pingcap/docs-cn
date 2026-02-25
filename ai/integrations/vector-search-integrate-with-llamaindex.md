---
title: 集成向量搜索与 LlamaIndex
summary: 学习如何将 TiDB 向量搜索与 LlamaIndex 集成。
aliases: ['/zh/tidb/stable/vector-search-integrate-with-llamaindex/','/zh/tidb/dev/vector-search-integrate-with-llamaindex/','/zh/tidbcloud/vector-search-integrate-with-llamaindex/']
---

# 集成向量搜索与 LlamaIndex

本教程演示如何将 [TiDB 向量搜索](/ai/concepts/vector-search-overview.md) 与 [LlamaIndex](https://www.llamaindex.ai) 集成。

> **注意：**
>
> - 向量搜索功能目前为 beta 版本，可能会在未提前通知的情况下发生变更。如果你发现了 bug，可以在 GitHub 上提交 [issue](https://github.com/pingcap/tidb/issues)。
> - 向量搜索功能适用于 [TiDB 自托管](/overview.md)、[TiDB Cloud Starter](https://docs.pingcap.com/zh/tidbcloud/select-cluster-tier/#starter)、[TiDB Cloud Essential](https://docs.pingcap.com/zh/tidbcloud/select-cluster-tier/#essential) 和 [TiDB Cloud Dedicated](https://docs.pingcap.com/zh/tidbcloud/select-cluster-tier/#tidb-cloud-dedicated)。对于 TiDB 自托管和 TiDB Cloud Dedicated，TiDB 版本需为 v8.4.0 或更高（推荐 v8.5.0 或更高）。

> **提示**
>
> 你可以在 Jupyter Notebook 中查看完整的 [示例代码](https://github.com/run-llama/llama_index/blob/main/docs/docs/examples/vector_stores/TiDBVector.ipynb)，或直接在 [Colab](https://colab.research.google.com/github/run-llama/llama_index/blob/main/docs/docs/examples/vector_stores/TiDBVector.ipynb) 在线环境中运行。

## 前置条件

完成本教程，你需要：

- 已安装 [Python 3.8 或更高版本](https://www.python.org/downloads/)。
- 已安装 [Jupyter Notebook](https://jupyter.org/install)。
- 已安装 [Git](https://git-scm.com/downloads)。
- 一个 TiDB 集群。

**如果你还没有 TiDB 集群，可以按如下方式创建：**

- （推荐）参照 [创建 TiDB Cloud Starter 集群](/develop/dev-guide-build-cluster-in-cloud.md) 创建属于你自己的 TiDB Cloud 集群。
- 参照 [部署本地测试 TiDB 集群](/quick-start-with-tidb.md#deploy-a-local-test-cluster) 或 [部署生产环境 TiDB 集群](/production-deployment-using-tiup.md) 创建本地集群。

## 快速开始

本节将提供分步指导，帮助你将 TiDB 向量搜索与 LlamaIndex 集成，实现语义搜索。

### 步骤 1. 新建 Jupyter Notebook 文件

在根目录下新建一个名为 `integrate_with_llamaindex.ipynb` 的 Jupyter Notebook 文件：

```shell
touch integrate_with_llamaindex.ipynb
```

### 步骤 2. 安装所需依赖

在你的项目目录下，运行以下命令安装所需的依赖包：

```shell
pip install llama-index-vector-stores-tidbvector
pip install llama-index
```

在 Jupyter Notebook 中打开 `integrate_with_llamaindex.ipynb` 文件，并添加以下代码以导入所需包：

```python
import textwrap

from llama_index.core import SimpleDirectoryReader, StorageContext
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.tidbvector import TiDBVectorStore
```

### 步骤 3. 配置环境变量

根据你选择的 TiDB 部署方式，配置环境变量。

<SimpleTab>
<div label="TiDB Cloud Starter or Essential">

对于 TiDB Cloud Starter 集群，按以下步骤获取集群连接字符串并配置环境变量：

1. 进入 [**Clusters**](https://tidbcloud.com/console/clusters) 页面，点击目标集群名称进入其概览页面。

2. 点击右上角的 **Connect**，弹出连接对话框。

3. 确认连接对话框中的配置与你的运行环境一致。

    - **Connection Type** 设置为 `Public`。
    - **Branch** 设置为 `main`。
    - **Connect With** 设置为 `SQLAlchemy`。
    - **Operating System** 与你的环境一致。

4. 点击 **PyMySQL** 标签页，复制连接字符串。

    > **提示：**
    >
    > 如果你还未设置密码，可点击 **Generate Password** 生成随机密码。

5. 配置环境变量。

    本文档以 [OpenAI](https://platform.openai.com/docs/introduction) 作为嵌入模型提供方。在此步骤中，你需要提供上一步获取的连接字符串和你的 [OpenAI API key](https://platform.openai.com/docs/quickstart/step-2-set-up-your-api-key)。

    运行以下代码配置环境变量。你将被提示输入连接字符串和 OpenAI API key：

    ```python
    # 使用 getpass 在终端安全地输入环境变量。
    import getpass
    import os

    # 从 TiDB Cloud 控制台复制你的连接字符串。
    # 连接字符串格式："mysql+pymysql://<USER>:<PASSWORD>@<HOST>:4000/<DB>?ssl_ca=/etc/ssl/cert.pem&ssl_verify_cert=true&ssl_verify_identity=true"
    tidb_connection_string = getpass.getpass("TiDB Connection String:")
    os.environ["OPENAI_API_KEY"] = getpass.getpass("OpenAI API Key:")
    ```

</div>
<div label="TiDB 自托管" value="tidb">

本文档以 [OpenAI](https://platform.openai.com/docs/introduction) 作为嵌入模型提供方。在此步骤中，你需要提供 TiDB 集群的连接字符串和你的 [OpenAI API key](https://platform.openai.com/docs/quickstart/step-2-set-up-your-api-key)。

运行以下代码配置环境变量。你将被提示输入连接字符串和 OpenAI API key：

```python
# 使用 getpass 在终端安全地输入环境变量。
import getpass
import os

# 连接字符串格式："mysql+pymysql://<USER>:<PASSWORD>@<HOST>:4000/<DB>?ssl_ca=/etc/ssl/cert.pem&ssl_verify_cert=true&ssl_verify_identity=true"
tidb_connection_string = getpass.getpass("TiDB Connection String:")
os.environ["OPENAI_API_KEY"] = getpass.getpass("OpenAI API Key:")
```

以 macOS 为例，集群连接字符串如下：

```dotenv
TIDB_DATABASE_URL="mysql+pymysql://<USERNAME>:<PASSWORD>@<HOST>:<PORT>/<DATABASE_NAME>"
# 例如：TIDB_DATABASE_URL="mysql+pymysql://root@127.0.0.1:4000/test"
```

你需要根据自己的 TiDB 集群修改连接字符串中的参数。如果你在本地运行 TiDB，`<HOST>` 默认为 `127.0.0.1`。初始 `<PASSWORD>` 为空，因此首次启动集群时可以省略该字段。

各参数说明如下：

- `<USERNAME>`：连接 TiDB 集群的用户名。
- `<PASSWORD>`：连接 TiDB 集群的密码。
- `<HOST>`：TiDB 集群的主机。
- `<PORT>`：TiDB 集群的端口。
- `<DATABASE>`：你要连接的数据库名称。

</div>

</SimpleTab>

### 步骤 4. 加载示例文档

#### 步骤 4.1 下载示例文档

在你的项目目录下，新建 `data/paul_graham/` 目录，并从 [run-llama/llama_index](https://github.com/run-llama/llama_index) GitHub 仓库下载示例文档 [`paul_graham_essay.txt`](https://github.com/run-llama/llama_index/blob/main/docs/docs/examples/data/paul_graham/paul_graham_essay.txt)。

```shell
!mkdir -p 'data/paul_graham/'
!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt'
```

#### 步骤 4.2 加载文档

使用 `SimpleDirectoryReader` 类从 `data/paul_graham/paul_graham_essay.txt` 加载示例文档。

```python
documents = SimpleDirectoryReader("./data/paul_graham").load_data()
print("Document ID:", documents[0].doc_id)

for index, document in enumerate(documents):
   document.metadata = {"book": "paul_graham"}
```

### 步骤 5. 嵌入并存储文档向量

#### 步骤 5.1 初始化 TiDB 向量存储

以下代码将在 TiDB 中创建一个名为 `paul_graham_test` 的表，并针对向量搜索进行了优化。

```python
tidbvec = TiDBVectorStore(
   connection_string=tidb_connection_string,
   table_name="paul_graham_test",
   distance_strategy="cosine",
   vector_dimension=1536,
   drop_existing_table=False,
)
```

执行成功后，你可以在 TiDB 数据库中直接查看和访问 `paul_graham_test` 表。

#### 步骤 5.2 生成并存储嵌入向量

以下代码将解析文档、生成嵌入向量，并将其存储到 TiDB 向量存储中。

```python
storage_context = StorageContext.from_defaults(vector_store=tidbvec)
index = VectorStoreIndex.from_documents(
   documents, storage_context=storage_context, show_progress=True
)
```

预期输出如下：

```plain
Parsing nodes: 100%|██████████| 1/1 [00:00<00:00,  8.76it/s]
Generating embeddings: 100%|██████████| 21/21 [00:02<00:00,  8.22it/s]
```

### 步骤 6. 执行向量搜索

以下代码基于 TiDB 向量存储创建查询引擎，并执行语义相似度搜索。

```python
query_engine = index.as_query_engine()
response = query_engine.query("What did the author do?")
print(textwrap.fill(str(response), 100))
```

> **注意**
>
> `TiDBVectorStore` 仅支持 [`default`](https://docs.llamaindex.ai/en/stable/api_reference/storage/vector_store/?h=vectorstorequerymode#llama_index.core.vector_stores.types.VectorStoreQueryMode) 查询模式。

预期输出如下：

```plain
The author worked on writing, programming, building microcomputers, giving talks at conferences,
publishing essays online, developing spam filters, painting, hosting dinner parties, and purchasing
a building for office use.
```

### 步骤 7. 使用元信息过滤器进行搜索

为了进一步优化搜索结果，你可以使用元信息过滤器，仅搜索符合过滤条件的最近邻结果。

#### 使用 `book != "paul_graham"` 过滤器查询

以下示例将排除 `metadata` 字段 `book` 为 `"paul_graham"` 的结果：

```python
from llama_index.core.vector_stores.types import (
   MetadataFilter,
   MetadataFilters,
)

query_engine = index.as_query_engine(
   filters=MetadataFilters(
      filters=[
         MetadataFilter(key="book", value="paul_graham", operator="!="),
      ]
   ),
   similarity_top_k=2,
)
response = query_engine.query("What did the author learn?")
print(textwrap.fill(str(response), 100))
```

预期输出如下：

```plain
Empty Response
```

#### 使用 `book == "paul_graham"` 过滤器查询

以下示例仅返回 `metadata` 字段 `book` 为 `"paul_graham"` 的文档：

```python
from llama_index.core.vector_stores.types import (
   MetadataFilter,
   MetadataFilters,
)

query_engine = index.as_query_engine(
   filters=MetadataFilters(
      filters=[
         MetadataFilter(key="book", value="paul_graham", operator="=="),
      ]
   ),
   similarity_top_k=2,
)
response = query_engine.query("What did the author learn?")
print(textwrap.fill(str(response), 100))
```

预期输出如下：

```plain
The author learned programming on an IBM 1401 using an early version of Fortran in 9th grade, then
later transitioned to working with microcomputers like the TRS-80 and Apple II. Additionally, the
author studied philosophy in college but found it unfulfilling, leading to a switch to studying AI.
Later on, the author attended art school in both the US and Italy, where they observed a lack of
substantial teaching in the painting department.
```

### 步骤 8. 删除文档

从索引中删除第一个文档：

```python
tidbvec.delete(documents[0].doc_id)
```

检查文档是否已被删除：

```python
query_engine = index.as_query_engine()
response = query_engine.query("What did the author learn?")
print(textwrap.fill(str(response), 100))
```

预期输出如下：

```plain
Empty Response
```

## 另请参阅

- [向量数据类型](/ai/reference/vector-search-data-types.md)
- [向量搜索索引](/ai/reference/vector-search-index.md)
