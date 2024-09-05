---
title: 在 LlamaIndex 中使用 TiDB 向量搜索
summary: 展示如何在 LlamaIndex 中使用 TiDB 向量搜索
---

# 在 LlamaIndex 中使用 TiDB 向量搜索

本文档展示如何在 [LlamaIndex](https://www.llamaindex.ai) 中使用 [TiDB 向量搜索](/vector-search-overview.md)。

> **Note**
>
> - 您可以在 Jupyter Notebook 上查看完整的 [示例代码](https://github.com/run-llama/llama_index/blob/main/docs/docs/examples/vector_stores/TiDBVector.ipynb)，或直接在 [Colab](https://colab.research.google.com/github/run-llama/llama_index/blob/main/docs/docs/examples/vector_stores/TiDBVector.ipynb) 在线环境中运行示例代码。

## 前置需求

- 推荐 [Python 3.8](https://www.python.org/downloads/) 及以上版本。
- [Jupyter Notebook](https://jupyter.org/install)。
- [Git](https://git-scm.com/downloads)。
- TiDB 集群，如果你还没有 TiDB 集群，可以按照以下方式创建：
  - TiDB Serverless 集群。如果没有 TiDB Cloud 集群，请按照 [创建 TiDB Serverless集群](https://dev.mysql.com/doc/refman/8.4/en/mysql.html) 创建自己的 TiDB Cloud 集群。
  - 本地部署的 TiDB 集群。如果没有集群，请按照 [使用 TiUP 部署 TiDB 集群](/production-deployment-using-tiup.md) 创建自己的 TiDB 集群。

## 开始

本节将逐步说明如何在 LlamaIndex 中使用 TiDB 向量搜索进行语义搜索。

### 步骤 1. 创建新的 Jupyter Notebook 文件

在根目录下新建一个名为 `integrate_with_llamaindex.ipynb` 的 Jupyter Notebook 文件：

```shell
touch integrate_with_llamaindex.ipynb
```

### 步骤 2. 安装所需依赖

在项目目录下运行以下命令安装所需的软件包：

```shell
pip install llama-index-vector-stores-tidbvector
pip install llama-index
```

在 Jupyter Notebook 中打开 `integrate_with_llamaindex.ipynb` 文件，添加以下代码以导入所需的软件包：

```python
import textwrap

from llama_index.core import SimpleDirectoryReader, StorageContext
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.tidbvector import TiDBVectorStore
```

### 步骤 3. 设置环境

<SimpleTab>

<div label="TiDB Serverless 集群部署">

#### 步骤 3.1 获取 TiDB 群集的连接字符串

  1. 在 [**Cluster**](https://tidbcloud.com/console/clusters) 界面，单击目标群集的名称进入其概览页面。

  2. 单击右上角的**Connect**。此时将显示连接对话框。

  3. 确保连接对话框中的配置符合您的运行环境。

     - **Connection Type** 设置为 `Public`.
     - **Branch** 设置为 `main`.
     - **Connect With** 设置为 `SQLAlchemy`.
     - **Operating System** 与你的系统环境相匹配.

  4. 点击 **PyMySQL** 标签，复制连接字符串。

     > **Tip:**
     >
     > 如果尚未设置密码，请单击**Generate Password**生成一个随机密码。

#### 步骤 3.2 配置环境变量

要建立安全高效的数据库连接，请使用 TiDB 提供的标准连接方法。

本文档使用 [OpenAI](https://platform.openai.com/docs/introduction) 作为嵌入模型生成向量嵌入。在此步骤中，你需要提供从步骤 3.1 中获取的连接字符串和 [OpenAI API 密钥](https://platform.openai.com/docs/quickstart/step-2-set-up-your-api-key)。

运行以下代码，配置环境变量。代码运行后，系统会提示输入连接字符串和 OpenAI API 密钥：

```python
# Use getpass to securely prompt for environment variables in your terminal.
import getpass
import os

# Copy your connection string from the TiDB Cloud console.
# Connection string format: "mysql+pymysql://<USER>:<PASSWORD>@<HOST>:4000/<DB>?ssl_ca=/etc/ssl/cert.pem&ssl_verify_cert=true&ssl_verify_identity=true"
tidb_connection_string = getpass.getpass("TiDB Connection String:")
os.environ["OPENAI_API_KEY"] = getpass.getpass("OpenAI API Key:")
```

</div>

<div label="本地部署 TiDB">

#### 步骤 3.1 配置环境变量

要建立安全高效的数据库连接，请使用 TiDB 提供的标准连接方法。

本文档使用 [OpenAI](https://platform.openai.com/docs/introduction) 作为嵌入模型生成向量嵌入。在此步骤中，你需要提供从步骤 3.1 中获取的连接字符串和 [OpenAI API 密钥](https://platform.openai.com/docs/quickstart/step-2-set-up-your-api-key)。

运行以下代码，配置环境变量。代码运行后，系统会提示输入连接字符串和 OpenAI API 密钥：

```python
# Use getpass to securely prompt for environment variables in your terminal.
import getpass
import os

# Copy your connection string from the TiDB Cloud console.
# Connection string format: "mysql+pymysql://<USER>:<PASSWORD>@<HOST>:4000/<DB>?ssl_ca=/etc/ssl/cert.pem&ssl_verify_cert=true&ssl_verify_identity=true"
tidb_connection_string = getpass.getpass("TiDB Connection String:")
os.environ["OPENAI_API_KEY"] = getpass.getpass("OpenAI API Key:")
```

例如，macOS 上的连接字符串如下所示：

```dotenv
TIDB_DATABASE_URL="mysql+pymysql://<prefix>.root:<password>@gateway01.<region>.prod.aws.tidbcloud.com:4000/test?ssl_ca=/etc/ssl/cert.pem&ssl_verify_cert=true&ssl_verify_identity=true"
```
注意替换为你的 TiDB 实际对应的值。

</div>

</SimpleTab>

### 步骤 4. 加载样本文件

#### 步骤 4.1 下载样本文件

在项目目录中创建名为 `data/paul_graham/` 的目录，并从 [run-llama/llama_index](https://github.com/run-llama/llama_index) 代码库中下载示例文档 [`paul_graham_essay.txt`](https://github.com/run-llama/llama_index/blob/main/docs/docs/examples/data/paul_graham/paul_graham_essay.txt)。

```shell
!mkdir -p 'data/paul_graham/'
!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt'
```

#### 步骤 4.2 加载文件

使用 `SimpleDirectoryReader` 从 `data/paul_graham/paul_graham_essay.txt` 中加载示例文档。

```python
documents = SimpleDirectoryReader("./data/paul_graham").load_data()
print("Document ID:", documents[0].doc_id)

for index, document in enumerate(documents):
   document.metadata = {"book": "paul_graham"}
```

### 步骤 5. 向量的生成和存储

#### 步骤 5.1 初始化 TiDB 向量存储

以下代码在 TiDB 中创建了一个名为 `paul_graham_test` 的表，该表针对向量搜索进行了优化。

```python
tidbvec = TiDBVectorStore(
   connection_string=tidb_connection_url,
   table_name="paul_graham_test",
   distance_strategy="cosine",
   vector_dimension=1536,
   drop_existing_table=False,
)
```

执行成功后，你可以直接查看和访问 TiDB 数据库中的 `paul_graham_test` 表。

#### 步骤 5.2 生成并存储向量

下面的代码会解析文档、生成向量嵌入并将其存储到 TiDB 向量存储中。

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

下面将基于 TiDB 向量存储创建一个查询引擎，并执行语义相似性搜索。

```python
query_engine = index.as_query_engine()
response = query_engine.query("What did the author do?")
print(textwrap.fill(str(response), 100))
```

> **Note**
>
> `TiDBVectorStore` 只支持 [`default`](https://docs.llamaindex.ai/en/stable/api_reference/storage/vector_store/?h=vectorstorequerymode#llama_index.core.vector_stores.types.VectorStoreQueryMode) 查询模式。

预期输出如下:

```plain
The author worked on writing, programming, building microcomputers, giving talks at conferences,
publishing essays online, developing spam filters, painting, hosting dinner parties, and purchasing
a building for office use.
```

### 步骤 7. 使用元数据过滤器搜索

为了优化搜索，你可以使用元数据筛选器来获取符合所设置筛选条件的特定近邻结果。

#### 使用 `book != “paul_graham”` 过滤器查询

以下示例查询了去除 `book` 元数据字段为 `paul_graham` 后的结果：

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

预期输出如下

```plain
Empty Response
```

#### Query with `book == "paul_graham"` filter

以下示例查询了 `book` 元数据字段为 `paul_graham` 的结果：

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

### 步骤 8. 删除文件

从索引中删除第一个文件：

```python
tidbvec.delete(documents[0].doc_id)
```

检查文件是否已被删除：

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