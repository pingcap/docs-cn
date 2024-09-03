---
title: 使用Python开始向量搜索
summary: 了解如何使用 Python 和 TiDB 向量搜索快速开发可执行语义搜索的人工智能应用程序。
---

# 使用 Python 开始向量搜索

本文展示如何开发一个简单的人工智能应用程序，并实现简单的**语义搜索**功能。不同于传统的关键字搜索，语义搜索可以获得与你输入的查询更加相关的结果。比如，你有标题为 “狗”、“鱼 ”和 “树 ”的文档，而你想搜索 “一种会游泳的动物”，那么语义搜索会将 “鱼 ”识别为最相关的结果。

在本文中，你将使用 [TiDB 向量搜索](/vector-search-overview.md)、Python、[TiDB Vector SDK for Python](https://github.com/pingcap/tidb-vector-python) 和人工智能模型构建人工智能应用程序。


## 准备
1. 在开始之前，你需要确定 TiDB 集群的部署方式以及以下内容被正确安装，

    <SimpleTab>

    <div label="TiDB Serverless 集群部署">

    - [Python 3.8 or higher](https://www.python.org/downloads/)
    - [Git](https://git-scm.com/downloads) 
    - TiDB Serverless集群。如果没有 TiDB Cloud 集群，请按照[创建 TiDB Serverless集群]([/create-tidb-cluster-serverless.md](https://dev.mysql.com/doc/refman/8.4/en/mysql.html))创建自己的 TiDB Cloud 集群。

    </div>

    <div label="TiDB Self-hosted 集群部署">

    - [Python 3.8 or higher](https://www.python.org/downloads/)
    - [Git](https://git-scm.com/downloads) 
    - TiDB 集群。如果没有集群，请按照[使用 TiUP 部署 TiDB 集群](/production-deployment-using-tiup.md)创建自己的 TiDB 集群。

    </div>

    </SimpleTab>

## 开始

如果你想要查看完整的代码，可以参考 [pingcap/tidb-vector-python](https://github.com/pingcap/tidb-vector-python/blob/main/examples/python-client-quickstart) 代码库。

### 步骤 1. 创建一个新的 Python 项目

创建一个新 Python 项目和一个名为 `example.py` 的文件：

```shell
mkdir python-client-quickstart
cd python-client-quickstart
touch example.py
```

### 步骤 2. 安装所需的依赖项

在项目目录下，运行以下命令安装所需的软件包：

```shell
pip install sqlalchemy pymysql sentence-transformers tidb-vector python-dotenv
```

- `tidb-vector`：用于与 TiDB 中的向量搜索交互的 Python 客户端。
- [`sentence-transformers`](https://sbert.net): 一个提供预训练模型的 Python 库，用于从文本生成 [向量嵌入](/vector-search-overview.md#vector-embedding)。

### 步骤 3. 配置 TiDB 群集的连接字符串
1. 根据不同的 TiDB 集群部署方式，配置集群的连接字符串
    <SimpleTab>

    <div label="TiDB Serverless 集群部署">

    1. 在 [**群集**](https://tidbcloud.com/console/clusters) 页面，单击目标群集的名称进入其概览页面。

    2. 单击右上角的**连接**。此时将显示连接对话框。

    3. 检查连接对话框中的配置，根据你的运行环境为其设置相应的值。

        - **Endpoint Type** 设置为 `Public`.
        - **Branch** 设置为 `main`.
        - **Connect With** 设置为 `SQLAlchemy`.
        - **Operating System** 与机器环境相匹配.

        > **Tip:**
        >
        > 如果程序在 Windows Subsystem for Linux (WSL) 中运行，请切换到相应的 Linux 发行版。

    4. 单击 **PyMySQL** 标签，复制连接字符串。

        > **Tip:**
        >
        > 如果尚未设置密码，单击**生成密码**生成一个随机密码。

    5. 在 Python 项目的根目录下创建一个 `.env` 文件，将连接字符串粘贴到其中。

        以下是 MacOS 的示例：

        ```dotenv
        TIDB_DATABASE_URL="mysql+pymysql://<prefix>.root:<password>@gateway01.<region>.prod.aws.tidbcloud.com:4000/test?ssl_ca=/etc/ssl/cert.pem&ssl_verify_cert=true&ssl_verify_identity=true"
        ```

    </div>

    <div label="TiDB Self-hosted 集群部署">
    
    在 Python 项目的根目录下创建一个 `.env` 文件，并根据启动的集群参数修改相应的环境变量中。

    - `HOST`: TiDB 集群的主机。
    - `PORT`: TiDB 集群的端口。
    - `USERNAME`: 连接 TiDB 集群的用户名。
    - `PASSWORD`: 连接 TiDB 集群的密码。
    - `DATABASE`: 要连接的数据库名称。
    - `CA_PATH`: 根证书文件的路径。
  
    以下是 MacOS 的示例：

    ```dotenv
    TIDB_DATABASE_URL="mysql+pymysql://<prefix>.root:<password>@<host>:4000/test?ssl_ca=/etc/ssl/cert.pem&ssl_verify_cert=true&ssl_verify_identity=true"
    ```

    </div>
    </SimpleTab>

### 步骤 4. 初始化嵌入模型

[嵌入模型](/vector-search-overview.md#embedding-model) 将数据转换为[向量嵌入](/vector-search-overview.md#vector-embedding)。本示例使用预训练模型 [**msmarco-MiniLM-L12-cos-v5**](https://huggingface.co/sentence-transformers/msmarco-MiniLM-L12-cos-v5) 将文本数据转换为向量嵌入。这个轻量级模型由 `sentence-transformers` 库提供，可将文本数据转换为 384 维向量嵌入。

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

### 步骤 5. 连接到 TiDB 集群

使用 `TiDBVectorClient` 类连接到 TiDB 集群，并创建一个带有向量列的表 `embedded_documents` 。

> **Note**
>
> 创建的表中，向量列的维度需要与嵌入模型生成的向量维度一致。如，**msmarco-MiniLM-L12-cos-v5** 模型生成的向量有 384 个维度， `embedded_documents` 的向量列维度也为384。

```python
import os
from tidb_vector.integrations import TiDBVectorClient
from dotenv import load_dotenv

# 从 .env 文件加载连接配置信息
load_dotenv()

vector_store = TiDBVectorClient(
   # embedded_documents表存储向量数据
   table_name='embedded_documents',
   # TiDB 集群的连接字符串。
   connection_string=os.environ.get('TIDB_DATABASE_URL'),
   # 嵌入模型生成的向量的维度。
   vector_dimension=embed_model_dims,
   # 如果表已经存在，则重新创建该表。
   drop_existing_table=True,
)
```

### 步骤 6. 向 **embedded_documents** 表中插入数据

你需要准备好文本数据，比如 “狗”、“鱼 ”和 “树”。 以下代码使用 `text_to_embedding()` 函数将这些文本数据转换为向量嵌入，然后将向量嵌入插入到 `embedded_documents` 表中。

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

在这一步中，假如你查询与现有文档中的任何单词都不匹配的内容，比如： “一种会游泳的动物”。

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

从输出结果来看，会游泳的动物很可能是一条鱼，或者是一只有游泳天赋的狗。

本文展示了向量搜索如何高效地找到最相关的文档，搜索结果按向量的远近排列：距离越小，文档越相关。

## 另请参阅

- [Vector Data Types](/tidb-cloud/vector-search-data-types.md)