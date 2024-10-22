---
title: 使用 Python 开始向量搜索
summary: 了解如何使用 Python 和 TiDB 向量搜索快速开发可执行语义搜索的人工智能应用程序。
---

# 使用 Python 开始向量搜索

本文将展示如何开发一个简单的 AI 应用，这个 AI 应用实现了简单的**语义搜索**功能。不同于传统的关键字搜索，语义搜索可以智能地理解你的输入，返回更相关的结果。例如，在“狗”、“鱼”和“树”这三条内容中搜索“一种会游泳的动物”时，语义搜索会将“鱼”作为最相关的结果返回。

在本文中，你将使用 [TiDB 向量搜索](/vector-search-overview.md)、Python、[TiDB Vector Python SDK](https://github.com/pingcap/tidb-vector-python) 和 AI 大模型完成这个 AI 应用的开发。

> **警告：**
>
> 向量搜索目前为实验特性，不建议在生产环境中使用。该功能可能会在未事先通知的情况下发生变化。如果发现 bug，请在 GitHub 上提 [issue](https://github.com/pingcap/tidb/issues) 反馈。

## 前置需求

为了能够顺利完成本文中的操作，你需要提前：

- 在你的机器上安装 [Python 3.8](https://www.python.org/downloads/) 或更高版本
- 在你的机器上安装 [Git](https://git-scm.com/downloads)
- 准备一个 TiDB 集群

如果你还没有 TiDB 集群，可以按照以下任一种方式创建：

- 参考[部署本地测试 TiDB 集群](/quick-start-with-tidb.md#部署本地测试集群)或[部署正式 TiDB 集群](/production-deployment-using-tiup.md)，创建本地集群。
- 参考[创建 TiDB Cloud Serverless 集群](/develop/dev-guide-build-cluster-in-cloud.md#第-1-步创建-tidb-cloud-serverless-集群)，创建 TiDB Cloud 集群。

## 快速开始

以下为从零开始构建这个应用的详细步骤，你也可以从 [pingcap/tidb-vector-python](https://github.com/pingcap/tidb-vector-python/blob/main/examples/python-client-quickstart) 开源代码库获取到完整代码，直接运行示例。

### 第 1 步：新建一个 Python 项目

在你的本地目录中，新建一个 Python 项目和一个名为 `example.py` 的文件：

```shell
mkdir python-client-quickstart
cd python-client-quickstart
touch example.py
```

### 第 2 步：安装所需的依赖

在该项目的目录下，运行以下命令安装所需的软件包：

```shell
pip install sqlalchemy pymysql sentence-transformers tidb-vector python-dotenv
```

- `tidb-vector`：用于与 TiDB 向量搜索交互的 Python 客户端。
- [`sentence-transformers`](https://sbert.net)：提供预训练模型的 Python 库，用于从文本生成[向量嵌入](/vector-search-overview.md#向量嵌入)。

### 第 3 步：配置 TiDB 集群的连接字符串

根据不同的 TiDB 集群部署方式，配置集群的连接字符串。

<SimpleTab>

<div label="本地部署 TiDB">

对于本地部署的 TiDB，请在 Python 项目的根目录下新建一个 `.env` 文件，将以下内容复制到 `.env` 文件中，并根据集群的连接参数修改环境变量值为 TiDB 实际对应的值：

```dotenv
TIDB_DATABASE_URL="mysql+pymysql://<USER>:<PASSWORD>@<HOST>:<PORT>/<DATABASE>"
# 例如：TIDB_DATABASE_URL="mysql+pymysql://root@127.0.0.1:4000/test"
```

如果你在本机运行 TiDB，`<HOST>` 默认为 `127.0.0.1`。`<PASSWORD>` 初始密码为空，若你是第一次启动集群，则无需带上此字段。

以下为各参数的解释：

- `<USER>`：连接 TiDB 集群的用户名。
- `<PASSWORD>`：连接 TiDB 集群的密码。
- `<HOST>`：TiDB 集群的主机号。
- `<PORT>`：TiDB 集群的端口。
- `<DATABASE>`：要连接的数据库名称。

</div>

<div label="TiDB Cloud Serverless">

对于 TiDB Cloud Serverless 集群，请按照以下步骤获取集群的连接字符串，然后配置环境变量：

1. 在 TiDB Cloud 的 [**Clusters**](https://tidbcloud.com/console/clusters) 页面，单击你的 TiDB Cloud Serverless 集群名，进入集群的 **Overview** 页面。

2. 点击右上角的 **Connect** 按钮，将会弹出连接对话框。

3. 确认对话框中的配置和你的运行环境一致。

    - **Connection Type** 为 `Public`。
    - **Branch** 选择 `main`。
    - **Connect With** 选择 `SQLAlchemy`。
    - **Operating System** 为你的运行环境。

    > **Tip:**
    >
    > 如果你的程序在 Windows Subsystem for Linux (WSL) 中运行，请切换为对应的 Linux 发行版。

4. 单击 **PyMySQL** 选项卡，复制连接字符串。

    > **Tip:**
    >
    > 如果你还没有设置密码，点击 **Generate Password** 生成一个随机密码。

5. 在 Python 项目的根目录下新建一个 `.env` 文件，将连接字符串粘贴到其中。

    以下为 macOS 的示例：

    ```dotenv
    TIDB_DATABASE_URL="mysql+pymysql://<prefix>.root:<password>@gateway01.<region>.prod.aws.tidbcloud.com:4000/test?ssl_ca=/etc/ssl/cert.pem&ssl_verify_cert=true&ssl_verify_identity=true"
    ```

</div>

</SimpleTab>

### 第 4 步：初始化嵌入模型

[嵌入模型](/vector-search-overview.md#嵌入模型)用于将数据转换为[向量嵌入](/vector-search-overview.md#向量嵌入)。本示例将使用预训练模型 [**msmarco-MiniLM-L12-cos-v5**](https://huggingface.co/sentence-transformers/msmarco-MiniLM-L12-cos-v5) 将文本数据转换为向量嵌入。该模型为一个轻量级模型，由 `sentence-transformers` 库提供，可将文本数据转换为 384 维的向量嵌入。

将以下代码复制到 `example.py` 文件中，完成模型的设置。这段代码初始化了一个 `SentenceTransformer` 实例，并定义了一个 `text_too_embedding()` 函数用于将文本数据转换为向量数据。

```python
from sentence_transformers import SentenceTransformer

print("Downloading and loading the embedding model...")
embed_model = SentenceTransformer("sentence-transformers/msmarco-MiniLM-L12-cos-v5", trust_remote_code=True)
embed_model_dims = embed_model.get_sentence_embedding_dimension()

def text_to_embedding(text):
    """Generates vector embeddings for the given text."""
    embedding = embed_model.encode(text)
    return embedding.tolist()
```

### 第 5 步：连接到 TiDB 集群

使用 `TiDBVectorClient` 类连接到 TiDB 集群，并创建一个包含向量列的表 `embedded_documents`。

> **Note**
>
> 请确保你创建的表中向量列的维度与嵌入模型生成的向量维度一致。例如，**msmarco-MiniLM-L12-cos-v5** 模型生成的向量有 384 个维度，`embedded_documents` 的向量列维度也应为 384。

```python
import os
from tidb_vector.integrations import TiDBVectorClient
from dotenv import load_dotenv

# 从 .env 文件加载连接配置信息
load_dotenv()

vector_store = TiDBVectorClient(
   # embedded_documents 表将用于存储向量数据
   table_name='embedded_documents',
   # 指定 TiDB 集群的连接字符串
   connection_string=os.environ.get('TIDB_DATABASE_URL'),
   # 指定嵌入模型生成的向量的维度
   vector_dimension=embed_model_dims,
   # 如果表已经存在，则重新创建该表
   drop_existing_table=True,
)
```

### 第 6 步：将文本数据转换为向量嵌入，并向表中插入数据

准备一些文本数据，比如 `"dog"`、`"fish"` 和 `"tree"`。以下代码将使用 `text_to_embedding()` 函数将这些文本数据转换为向量嵌入，然后将向量嵌入插入到 `embedded_documents` 表中：

```python
documents = [
    {
        "id": "f8e7dee2-63b6-42f1-8b60-2d46710c1971",
        "text": "dog",
        "embedding": text_to_embedding("dog"),
        "metadata": {"category": "animal"},
    },
    {
        "id": "8dde1fbc-2522-4ca2-aedf-5dcb2966d1c6",
        "text": "fish",
        "embedding": text_to_embedding("fish"),
        "metadata": {"category": "animal"},
    },
    {
        "id": "e4991349-d00b-485c-a481-f61695f2b5ae",
        "text": "tree",
        "embedding": text_to_embedding("tree"),
        "metadata": {"category": "plant"},
    },
]

vector_store.insert(
    ids=[doc["id"] for doc in documents],
    texts=[doc["text"] for doc in documents],
    embeddings=[doc["embedding"] for doc in documents],
    metadatas=[doc["metadata"] for doc in documents],
)
```

### 第 7 步：执行语义搜索

查询一个与已有文档 `documents` 中任何单词都不匹配的关键词，比如 "a swimming animal"。

以下的代码会再次使用 `text_to_embedding()` 函数将查询文本转换为向量嵌入，然后使用该嵌入进行查询，找出最匹配的前三个词。

```python
def print_result(query, result):
   print(f"Search result (\"{query}\"):")
   for r in result:
      print(f"- text: \"{r.document}\", distance: {r.distance}")

query = "a swimming animal"
query_embedding = text_to_embedding(query)
search_result = vector_store.query(query_embedding, k=3)
print_result(query, search_result)
```

运行 `example.py` 文件，输出结果如下：

```plain
Search result ("a swimming animal"):
- text: "fish", distance: 0.4562914811223072
- text: "dog", distance: 0.6469335836410557
- text: "tree", distance: 0.798545178640937
```

搜索结果中的三个词按它们与查询向量的距离排序：距离越小，对应的 `document` 越相关。

因此，从输出结果来看，会游泳的动物很可能是一条鱼 (`fish`)，或者是一只有游泳天赋的狗 (`dog`)。

## 另请参阅

- [向量数据类型](/vector-search-data-types.md)
- [向量搜索索引](/vector-search-index.md)