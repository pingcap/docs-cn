---
title: 将向量搜索与 LlamaIndex 集成
summary: 了解如何将 TiDB 向量搜索与 LlamaIndex 集成。
---

# 将向量搜索与 LlamaIndex 集成

本教程演示如何将 TiDB 的[向量搜索](/tidb-cloud/vector-search-overview.md)功能与 [LlamaIndex](https://www.llamaindex.ai) 集成。

> **注意**
>
> TiDB 向量搜索仅适用于 TiDB Self-Managed（TiDB >= v8.4）和 [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)。它不适用于 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)。

> **提示**
>
> 你可以在 Jupyter Notebook 上查看完整的[示例代码](https://github.com/run-llama/llama_index/blob/main/docs/docs/examples/vector_stores/TiDBVector.ipynb)，或直接在 [Colab](https://colab.research.google.com/github/run-llama/llama_index/blob/main/docs/docs/examples/vector_stores/TiDBVector.ipynb) 在线环境中运行示例代码。

## 前提条件

要完成本教程，你需要：

- 安装 [Python 3.8 或更高版本](https://www.python.org/downloads/)。
- 安装 [Jupyter Notebook](https://jupyter.org/install)。
- 安装 [Git](https://git-scm.com/downloads)。
- 一个 TiDB Cloud Serverless 集群。如果你没有 TiDB Cloud 集群，请按照[创建 TiDB Cloud Serverless 集群](/tidb-cloud/create-tidb-cluster-serverless.md)的说明创建自己的 TiDB Cloud 集群。

## 开始使用

本节提供将 TiDB 向量搜索与 LlamaIndex 集成以执行语义搜索的分步说明。

### 步骤 1. 创建新的 Jupyter Notebook 文件

在根目录中，创建一个名为 `integrate_with_llamaindex.ipynb` 的新 Jupyter Notebook 文件：

```shell
touch integrate_with_llamaindex.ipynb
```

### 步骤 2. 安装所需依赖

在项目目录中，运行以下命令安装所需的包：

```shell
pip install llama-index-vector-stores-tidbvector
pip install llama-index
```

在 Jupyter Notebook 中打开 `integrate_with_llamaindex.ipynb` 文件，并添加以下代码以导入所需的包：

```python
import textwrap

from llama_index.core import SimpleDirectoryReader, StorageContext
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.tidbvector import TiDBVectorStore
```

### 步骤 3. 配置环境变量

按照以下步骤获取集群连接字符串并配置环境变量：

1. 导航到[**集群**](https://tidbcloud.com/project/clusters)页面，然后点击目标集群的名称进入其概览页面。

2. 点击右上角的**连接**。将显示一个连接对话框。

3. 确保连接对话框中的配置与你的操作环境匹配。

   - **连接类型**设置为 `Public`。
   - **分支**设置为 `main`。
   - **连接方式**设置为 `SQLAlchemy`。
   - **操作系统**与你的环境匹配。

4. 点击 **PyMySQL** 标签并复制连接字符串。

   > **提示：**
   >
   > 如果你还没有设置密码，点击**生成密码**以生成一个随机密码。

5. 配置环境变量。

   本文档使用 [OpenAI](https://platform.openai.com/docs/introduction) 作为嵌入模型提供者。在此步骤中，你需要提供从上一步获取的连接字符串和你的 [OpenAI API 密钥](https://platform.openai.com/docs/quickstart/step-2-set-up-your-api-key)。

   要配置环境变量，运行以下代码。系统将提示你输入连接字符串和 OpenAI API 密钥：

   ```python
   # 使用 getpass 在终端中安全地提示输入环境变量。
   import getpass
   import os

   # 从 TiDB Cloud 控制台复制你的连接字符串。
   # 连接字符串格式："mysql+pymysql://<USER>:<PASSWORD>@<HOST>:4000/<DB>?ssl_ca=/etc/ssl/cert.pem&ssl_verify_cert=true&ssl_verify_identity=true"
   tidb_connection_string = getpass.getpass("TiDB Connection String:")
   os.environ["OPENAI_API_KEY"] = getpass.getpass("OpenAI API Key:")
   ```

### 步骤 4. 加载示例文档

#### 步骤 4.1 下载示例文档

在项目目录中，创建一个名为 `data/paul_graham/` 的目录，并从 [run-llama/llama_index](https://github.com/run-llama/llama_index) GitHub 仓库下载示例文档 [`paul_graham_essay.txt`](https://github.com/run-llama/llama_index/blob/main/docs/docs/examples/data/paul_graham/paul_graham_essay.txt)。

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

### 步骤 5. 嵌入和存储文档向量

#### 步骤 5.1 初始化 TiDB 向量存储

以下代码在 TiDB 中创建一个名为 `paul_graham_test` 的表，该表针对向量搜索进行了优化。

```python
tidbvec = TiDBVectorStore(
   connection_string=tidb_connection_url,
   table_name="paul_graham_test",
   distance_strategy="cosine",
   vector_dimension=1536,
   drop_existing_table=False,
)
```

成功执行后，你可以直接在 TiDB 数据库中查看和访问 `paul_graham_test` 表。

#### 步骤 5.2 生成和存储嵌入

以下代码解析文档，生成嵌入，并将它们存储在 TiDB 向量存储中。

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

以下代码基于 TiDB 向量存储创建查询引擎并执行语义相似度搜索。

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

### 步骤 7. 使用元数据过滤器搜索

要优化搜索，你可以使用元数据过滤器来检索与应用的过滤器匹配的特定最近邻结果。

#### 使用 `book != "paul_graham"` 过滤器查询

以下示例排除 `book` 元数据字段为 `"paul_graham"` 的结果：

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

以下示例过滤结果以仅包含 `book` 元数据字段为 `"paul_graham"` 的文档：

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

- [向量数据类型](/tidb-cloud/vector-search-data-types.md)
- [向量搜索索引](/tidb-cloud/vector-search-index.md)
