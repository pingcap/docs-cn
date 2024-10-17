---
title: 在 LlamaIndex 中使用 TiDB 向量搜索
summary: 了解如何在 LlamaIndex 中使用 TiDB 向量搜索。
---

# 在 LlamaIndex 中使用 TiDB 向量搜索

本文档将展示如何在 [LlamaIndex](https://www.llamaindex.ai) 中使用 [TiDB 向量搜索](/vector-search-overview.md)。

> **警告：**
>
> 向量搜索目前为实验特性，不建议在生产环境中使用。该功能可能会在未事先通知的情况下发生变化。如果发现 bug，请在 GitHub 上提 [issue](https://github.com/pingcap/tidb/issues) 反馈。

> **Tip**
>
> 你可以在 Jupyter Notebook 上查看完整的[示例代码](https://github.com/run-llama/llama_index/blob/main/docs/docs/examples/vector_stores/TiDBVector.ipynb)，或直接在 [Colab](https://colab.research.google.com/github/run-llama/llama_index/blob/main/docs/docs/examples/vector_stores/TiDBVector.ipynb) 在线环境中运行示例代码。

## 前置需求

为了能够顺利完成本文中的操作，你需要提前：

- 在你的机器上安装 [Python 3.8](https://www.python.org/downloads/) 或更高版本
- 在你的机器上安装 [Jupyter Notebook](https://jupyter.org/install)
- 在你的机器上安装 [Git](https://git-scm.com/downloads)
- 准备一个 TiDB 集群

如果你还没有 TiDB 集群，可以按照以下任一种方式创建：

- 参考[部署本地测试 TiDB 集群](/quick-start-with-tidb.md#部署本地测试集群)或[部署正式 TiDB 集群](/production-deployment-using-tiup.md)，创建本地集群。
- 参考[创建 TiDB Cloud Serverless 集群](/develop/dev-guide-build-cluster-in-cloud.md#第-1-步创建-tidb-cloud-serverless-集群)，创建 TiDB Cloud 集群。

## 快速开始

本节将详细介绍如何将 TiDB 的向量搜索功能与 LlamaIndex 结合使用，以实现语义搜索。

### 第 1 步：新建 Jupyter Notebook 文件

在根目录下，新建一个名为 `integrate_with_llamaindex.ipynb` 的 Jupyter Notebook 文件：

```shell
touch integrate_with_llamaindex.ipynb
```

### 第 2 步：安装所需的依赖

在你的项目目录下，运行以下命令安装所需的软件包：

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

### 第 3 步：配置环境变量

根据 TiDB 集群的部署方式不同，选择对应的环境变量配置方式。

<SimpleTab>

<div label="本地部署 TiDB">

本文档使用 [OpenAI](https://platform.openai.com/docs/introduction) 作为嵌入模型生成向量嵌入。在此步骤中，你需要提供集群的连接字符串和 [OpenAI API 密钥](https://platform.openai.com/docs/quickstart/step-2-set-up-your-api-key)。

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

以 macOS 为例，集群的连接字符串如下所示：

```dotenv
TIDB_DATABASE_URL="mysql+pymysql://<USERNAME>:<PASSWORD>@<HOST>:<PORT>/<DATABASE_NAME>"
# 例如： TIDB_DATABASE_URL="mysql+pymysql://root@127.0.0.1:4000/test"
```

请替换连接字符串中的参数为你的 TiDB 实际对应的值。如果你在本机运行 TiDB，默认 `<HOST>` 地址为 `127.0.0.1`。`<PASSWORD>` 初始密码为空，若你是第一次启动集群，则无需带上此字段。

以下为各参数的解释：

- `<USERNAME>`：连接 TiDB 集群的用户名。
- `<PASSWORD>`：连接 TiDB 集群的密码。
- `<HOST>`：TiDB 集群的主机地址。
- `<PORT>`：TiDB 集群的端口号。
- `<DATABASE>`：要连接的数据库名称。

</div>

<div label="TiDB Cloud Serverless">

对于 TiDB Cloud Serverless 集群，请按照以下步骤获取 TiDB 集群的连接字符串，然后配置环境变量：

1. 在 TiDB Cloud 的 [**Clusters**](https://tidbcloud.com/console/clusters) 页面，单击你的 TiDB Cloud Serverless 集群名，进入集群的 **Overview** 页面。

2. 点击右上角的 **Connect** 按钮，将会弹出连接对话框。

3. 确认对话框中的配置和你的运行环境一致。

     - **Connection Type** 为 `Public`。
     - **Branch** 选择 `main`。
     - **Connect With** 选择 `SQLAlchemy`。
     - **Operating System** 为你的运行环境。

4. 点击 **PyMySQL** 选项卡，复制连接字符串。

     > **Tip:**
     >
     > 如果你还没有设置密码，点击 **Generate Password** 生成一个随机密码。

5. 配置环境变量。

    本文档使用 [OpenAI](https://platform.openai.com/docs/introduction) 作为嵌入模型生成向量嵌入。在此步骤中，你需要提供从上一步中获取的连接字符串和 [OpenAI API 密钥](https://platform.openai.com/docs/quickstart/step-2-set-up-your-api-key)。

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

</SimpleTab>

### 第 4 步：加载样本文档

#### 4.1 下载样本文档

在你的项目目录中创建一个名为 `data/paul_graham/` 的目录，然后从 [run-llama/llama_index](https://github.com/run-llama/llama_index) GitHub 代码库中下载样本文档 [`paul_graham_essay.txt`](https://github.com/run-llama/llama_index/blob/main/docs/docs/examples/data/paul_graham/paul_graham_essay.txt)：

```shell
mkdir -p 'data/paul_graham/'
wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt'
```

#### 4.2 加载文档

使用 `SimpleDirectoryReader` 从 `data/paul_graham/paul_graham_essay.txt` 中加载示例文档：

```python
documents = SimpleDirectoryReader("./data/paul_graham").load_data()
print("Document ID:", documents[0].doc_id)

for index, document in enumerate(documents):
   document.metadata = {"book": "paul_graham"}
```

### 第 5 步：生成并存储文档向量

#### 5.1 初始化 TiDB 向量存储

以下代码将在 TiDB 中创建一个 `paul_graham_test` 表，该表针对向量搜索进行了优化。

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

#### 5.2 生成并存储向量嵌入

以下代码将解析文档以生成向量嵌入，并将向量嵌入存储到 TiDB 向量存储中。

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

### 第 6 步：执行向量搜索

以下代码将基于 TiDB 向量存储创建一个查询引擎，并执行语义相似性搜索。

```python
query_engine = index.as_query_engine()
response = query_engine.query("What did the author do?")
print(textwrap.fill(str(response), 100))
```

> **注意：**
>
> `TiDBVectorStore` 只支持 [`default`](https://docs.llamaindex.ai/en/stable/api_reference/storage/vector_store/?h=vectorstorequerymode#llama_index.core.vector_stores.types.VectorStoreQueryMode) 查询模式。

预期输出如下：

```plain
The author worked on writing, programming, building microcomputers, giving talks at conferences,
publishing essays online, developing spam filters, painting, hosting dinner parties, and purchasing
a building for office use.
```

### 第 7 步：使用元数据过滤器进行搜索

为了优化搜索，你可以使用元数据过滤器来筛选出符合特定条件的近邻结果。

#### 使用 `book != “paul_graham”` 过滤器查询

以下示例的查询将排除掉 `book` 元数据字段为 `paul_graham` 的结果：

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

#### Query with `book == "paul_graham"` filter

以下示例的查询将筛选出 `book` 元数据字段为 `paul_graham` 的结果：

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

### 第 8 步：删除文档

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

- [向量数据类型](/vector-search-data-types.md)
- [向量搜索索引](/vector-search-index.md)