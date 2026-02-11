---
title: 使用 Python 快速入门 TiDB + AI
summary: 学习如何使用 Python 和 TiDB 向量搜索快速开发一个实现语义搜索的 AI 应用。
aliases: ['/zh/tidb/stable/vector-search-get-started-using-python/','/zh/tidb/dev/vector-search-get-started-using-python/','/zh/tidbcloud/vector-search-get-started-using-python/']
---

# 使用 Python 快速入门 TiDB + AI

本教程演示如何开发一个简单的 AI 应用，提供 **语义搜索** 功能。与传统的关键字搜索不同，语义搜索能够智能理解你的查询背后的含义，并返回最相关的结果。例如，如果你有标题为 "dog"、"fish" 和 "tree" 的文档，当你搜索 "a swimming animal" 时，应用会识别出 "fish" 是最相关的结果。

在本教程中，你将使用 [TiDB 向量搜索](/ai/concepts/vector-search-overview.md)、Python、[TiDB Vector SDK for Python](https://github.com/pingcap/tidb-vector-python) 以及 AI 模型来开发该 AI 应用。

> **注意：**
>
> - 向量搜索功能目前为 beta 版本，可能会在不提前通知的情况下发生变更。如果你发现了 bug，可以在 GitHub 上提交 [issue](https://github.com/pingcap/tidb/issues)。
> - 向量搜索功能适用于 [TiDB 自托管](/overview.md)、[TiDB Cloud Starter](https://docs.pingcap.com/zh/tidbcloud/select-cluster-tier/#starter)、[TiDB Cloud Essential](https://docs.pingcap.com/zh/tidbcloud/select-cluster-tier/#essential) 和 [TiDB Cloud Dedicated](https://docs.pingcap.com/zh/tidbcloud/select-cluster-tier/#tidb-cloud-dedicated)。对于 TiDB 自托管和 TiDB Cloud Dedicated，TiDB 版本需为 v8.4.0 或更高（推荐 v8.5.0 或更高）。

## 前置条件

完成本教程，你需要：

- 已安装 [Python 3.8 或更高版本](https://www.python.org/downloads/)。
- 已安装 [Git](https://git-scm.com/downloads)。
- 一个 TiDB 集群。

**如果你还没有 TiDB 集群，可以按如下方式创建：**

- （推荐）参考 [创建 TiDB Cloud Starter 集群](/develop/dev-guide-build-cluster-in-cloud.md) 创建属于你自己的 TiDB Cloud 集群。
- 参考 [部署本地测试 TiDB 集群](/quick-start-with-tidb.md#deploy-a-local-test-cluster) 或 [部署生产环境 TiDB 集群](/production-deployment-using-tiup.md) 创建本地集群。

## 快速开始

以下步骤展示了如何从零开发该应用。如果你想直接运行示例，可以在 [pingcap/tidb-vector-python](https://github.com/pingcap/tidb-vector-python/blob/main/examples/python-client-quickstart) 仓库中查看示例代码。

### 步骤 1. 创建新的 Python 项目

在你喜欢的目录下，创建一个新的 Python 项目，并新建名为 `example.py` 的文件：

```shell
mkdir python-client-quickstart
cd python-client-quickstart
touch example.py
```

### 步骤 2. 安装所需依赖

在你的项目目录下，运行以下命令安装所需的依赖包：

```shell
pip install sqlalchemy pymysql sentence-transformers tidb-vector python-dotenv
```

- `tidb-vector`：用于与 TiDB 向量搜索交互的 Python 客户端。
- [`sentence-transformers`](https://sbert.net)：一个 Python 库，提供用于从文本生成 [向量嵌入](/ai/concepts/vector-search-overview.md#vector-embedding) 的预训练模型。

### 步骤 3. 配置 TiDB 集群连接字符串

根据你选择的 TiDB 部署方式，配置集群连接字符串。

<SimpleTab>
<div label="TiDB Cloud Starter or Essential">

对于 TiDB Cloud Starter 集群，按以下步骤获取集群连接字符串并配置环境变量：

1. 进入 [**Clusters**](https://tidbcloud.com/console/clusters) 页面，点击目标集群名称进入集群概览页。

2. 点击右上角的 **Connect**，弹出连接对话框。

3. 确认连接对话框中的配置与你的运行环境一致。

    - **Connection Type** 设置为 `Public`。
    - **Branch** 设置为 `main`。
    - **Connect With** 设置为 `SQLAlchemy`。
    - **Operating System** 与你的环境一致。

    > **提示：**
    >
    > 如果你的程序运行在 Windows Subsystem for Linux (WSL) 中，请切换到对应的 Linux 发行版。

4. 点击 **PyMySQL** 标签页，复制连接字符串。

    > **提示：**
    >
    > 如果你还未设置密码，可点击 **Generate Password** 生成随机密码。

5. 在你的 Python 项目根目录下，创建 `.env` 文件，并将连接字符串粘贴进去。

    以下为 macOS 示例：

    ```dotenv
    TIDB_DATABASE_URL="mysql+pymysql://<prefix>.root:<password>@gateway01.<region>.prod.aws.tidbcloud.com:4000/test?ssl_ca=/etc/ssl/cert.pem&ssl_verify_cert=true&ssl_verify_identity=true"
    ```

</div>
<div label="TiDB 自托管" value="tidb">

对于 TiDB 自建集群，在你的 Python 项目根目录下创建 `.env` 文件。将以下内容复制到 `.env` 文件中，并根据你的 TiDB 集群连接参数修改环境变量的值：

```dotenv
TIDB_DATABASE_URL="mysql+pymysql://<USER>:<PASSWORD>@<HOST>:<PORT>/<DATABASE>"
# 例如：TIDB_DATABASE_URL="mysql+pymysql://root@127.0.0.1:4000/test"
```

如果你在本地机器上运行 TiDB，`<HOST>` 默认为 `127.0.0.1`。初始 `<PASSWORD>` 为空，因此如果是首次启动集群，可以省略该字段。

各参数说明如下：

- `<USER>`：连接 TiDB 集群的用户名。
- `<PASSWORD>`：连接 TiDB 集群的密码。
- `<HOST>`：TiDB 集群的主机。
- `<PORT>`：TiDB 集群的端口。
- `<DATABASE>`：你要连接的数据库名称。

</div>

</SimpleTab>

### 步骤 4. 初始化嵌入模型

[嵌入模型](/ai/concepts/vector-search-overview.md#embedding-model) 用于将数据转换为 [向量嵌入](/ai/concepts/vector-search-overview.md#vector-embedding)。本示例使用预训练模型 [**msmarco-MiniLM-L12-cos-v5**](https://huggingface.co/sentence-transformers/msmarco-MiniLM-L12-cos-v5) 进行文本嵌入。该轻量级模型由 `sentence-transformers` 库提供，可将文本数据转换为 384 维的向量嵌入。

要设置模型，将以下代码复制到 `example.py` 文件中。该代码初始化了一个 `SentenceTransformer` 实例，并定义了后续使用的 `text_to_embedding()` 函数。

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

### 步骤 5. 连接 TiDB 集群

使用 `TiDBVectorClient` 类连接 TiDB 集群，并创建包含向量列的 `embedded_documents` 表。

> **注意**
>
> 请确保表中向量列的维度与嵌入模型生成的向量维度一致。例如，**msmarco-MiniLM-L12-cos-v5** 模型生成的向量为 384 维，因此 `embedded_documents` 表中向量列的维度也应为 384。

```python
import os
from tidb_vector.integrations import TiDBVectorClient
from dotenv import load_dotenv

# Load the connection string from the .env file
load_dotenv()

vector_store = TiDBVectorClient(
   # The 'embedded_documents' table will store the vector data.
   table_name='embedded_documents',
   # The connection string to the TiDB cluster.
   connection_string=os.environ.get('TIDB_DATABASE_URL'),
   # The dimension of the vector generated by the embedding model.
   vector_dimension=embed_model_dims,
   # Recreate the table if it already exists.
   drop_existing_table=True,
)
```

### 步骤 6. 嵌入文本数据并存储向量

本步骤将准备包含单词的示例文档，如 "dog"、"fish" 和 "tree"。以下代码使用 `text_to_embedding()` 函数将这些文本文档转换为向量嵌入，并插入到向量存储中。

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

### 步骤 7. 执行语义搜索

本步骤将搜索 "a swimming animal"，该查询与现有文档中的单词并不直接匹配。

以下代码再次使用 `text_to_embedding()` 函数将查询文本转换为向量嵌入，并用该嵌入向量查询，找出距离最近的前三个结果。

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

运行 `example.py` 文件，输出如下：

```plain
Search result ("a swimming animal"):
- text: "fish", distance: 0.4562914811223072
- text: "dog", distance: 0.6469335836410557
- text: "tree", distance: 0.798545178640937
```

搜索结果中的三个词根据与查询向量的距离进行排序：距离越小，`document` 越相关。

因此，根据输出，最有可能的游泳动物是 fish，或者是一只擅长游泳的 dog。

## 另请参阅

- [向量数据类型](/ai/reference/vector-search-data-types.md)
- [向量搜索索引](/ai/reference/vector-search-index.md)
