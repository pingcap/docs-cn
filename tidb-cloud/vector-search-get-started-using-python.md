---
title: 通过 Python 开始使用 TiDB + AI
summary: 学习如何使用 Python 和 TiDB Vector Search 快速开发一个进行语义搜索的 AI 应用。
---

# 通过 Python 开始使用 TiDB + AI

本教程演示如何开发一个提供**语义搜索**功能的简单 AI 应用。与传统的关键词搜索不同，语义搜索能够智能地理解查询背后的含义并返回最相关的结果。例如，如果你有标题为"dog"（狗）、"fish"（鱼）和"tree"（树）的文档，当你搜索"a swimming animal"（一个会游泳的动物）时，应用会识别出"fish"（鱼）是最相关的结果。

在本教程中，你将使用 [TiDB Vector Search](/tidb-cloud/vector-search-overview.md)、Python、[TiDB Vector SDK for Python](https://github.com/pingcap/tidb-vector-python) 和 AI 模型来开发这个 AI 应用。

> **注意**
>
> TiDB Vector Search 仅适用于 TiDB Self-Managed（TiDB >= v8.4）和 [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)。它不适用于 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)。

## 前提条件

要完成本教程，你需要：

- 安装 [Python 3.8 或更高版本](https://www.python.org/downloads/)。
- 安装 [Git](https://git-scm.com/downloads)。
- 一个 TiDB Cloud Serverless 集群。如果你还没有，请按照[创建 TiDB Cloud Serverless 集群](/tidb-cloud/create-tidb-cluster-serverless.md)的说明创建你自己的 TiDB Cloud 集群。

## 开始使用

以下步骤展示如何从头开始开发应用。如果想直接运行演示，你可以在 [pingcap/tidb-vector-python](https://github.com/pingcap/tidb-vector-python/blob/main/examples/python-client-quickstart) 仓库中查看示例代码。

### 步骤 1. 创建新的 Python 项目

在你选择的目录中，创建一个新的 Python 项目和一个名为 `example.py` 的文件：

```shell
mkdir python-client-quickstart
cd python-client-quickstart
touch example.py
```

### 步骤 2. 安装所需依赖

在你的项目目录中，运行以下命令安装所需的包：

```shell
pip install sqlalchemy pymysql sentence-transformers tidb-vector python-dotenv
```

- `tidb-vector`：用于与 TiDB Vector Search 交互的 Python 客户端。
- [`sentence-transformers`](https://sbert.net)：一个提供预训练模型的 Python 库，用于从文本生成[向量嵌入](/tidb-cloud/vector-search-overview.md#vector-embedding)。

### 步骤 3. 配置到 TiDB 集群的连接字符串

1. 导航到 [**Clusters**](https://tidbcloud.com/project/clusters) 页面，然后点击目标集群的名称进入其概览页面。

2. 点击右上角的 **Connect**。将显示一个连接对话框。

3. 确保连接对话框中的配置与你的操作环境匹配。

   - **Connection Type** 设置为 `Public`。
   - **Branch** 设置为 `main`。
   - **Connect With** 设置为 `SQLAlchemy`。
   - **Operating System** 与你的环境匹配。

   > **提示：**
   >
   > 如果你的程序在 Windows Subsystem for Linux (WSL) 中运行，请切换到相应的 Linux 发行版。

4. 点击 **PyMySQL** 标签并复制连接字符串。

   > **提示：**
   >
   > 如果你还没有设置密码，请点击 **Generate Password** 生成一个随机密码。

5. 在你的 Python 项目的根目录中，创建一个 `.env` 文件并将连接字符串粘贴到其中。

   以下是 macOS 的示例：

   ```dotenv
   TIDB_DATABASE_URL="mysql+pymysql://<prefix>.root:<password>@gateway01.<region>.prod.aws.tidbcloud.com:4000/test?ssl_ca=/etc/ssl/cert.pem&ssl_verify_cert=true&ssl_verify_identity=true"
   ```

### 步骤 4. 初始化嵌入模型

[嵌入模型](/tidb-cloud/vector-search-overview.md#embedding-model)将数据转换为[向量嵌入](/tidb-cloud/vector-search-overview.md#vector-embedding)。本示例使用预训练模型 [**msmarco-MiniLM-L12-cos-v5**](https://huggingface.co/sentence-transformers/msmarco-MiniLM-L12-cos-v5) 进行文本嵌入。这个由 `sentence-transformers` 库提供的轻量级模型可以将文本数据转换为 384 维的向量嵌入。

要设置模型，将以下代码复制到 `example.py` 文件中。这段代码初始化了一个 `SentenceTransformer` 实例，并定义了一个供后续使用的 `text_to_embedding()` 函数。

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

使用 `TiDBVectorClient` 类连接到你的 TiDB 集群，并创建一个带有向量列的表 `embedded_documents`。

> **注意**
>
> 确保表中向量列的维度与嵌入模型生成的向量维度匹配。例如，**msmarco-MiniLM-L12-cos-v5** 模型生成 384 维的向量，所以 `embedded_documents` 中向量列的维度也应该是 384。

```python
import os
from tidb_vector.integrations import TiDBVectorClient
from dotenv import load_dotenv

# 从 .env 文件加载连接字符串
load_dotenv()

vector_store = TiDBVectorClient(
   # 'embedded_documents' 表将存储向量数据。
   table_name='embedded_documents',
   # 到 TiDB 集群的连接字符串。
   connection_string=os.environ.get('TIDB_DATABASE_URL'),
   # 嵌入模型生成的向量维度。
   vector_dimension=embed_model_dims,
   # 如果表已存在则重新创建。
   drop_existing_table=True,
)
```

### 步骤 6. 嵌入文本数据并存储向量

在这一步中，你将准备包含单个词的示例文档，如"dog"（狗）、"fish"（鱼）和"tree"（树）。以下代码使用 `text_to_embedding()` 函数将这些文本文档转换为向量嵌入，然后将它们插入到向量存储中。

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

在这一步中，你将搜索"a swimming animal"（一个会游泳的动物），这个词组与现有文档中的任何词都不直接匹配。

以下代码再次使用 `text_to_embedding()` 函数将查询文本转换为向量嵌入，然后使用该嵌入查询找到最接近的三个匹配项。

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

搜索结果中的三个词按照它们与查询向量的距离排序：距离越小，相应的 `document` 越相关。

因此，根据输出，这个会游泳的动物最可能是鱼，或者是一只有游泳天赋的狗。

## 另请参阅

- [向量数据类型](/tidb-cloud/vector-search-data-types.md)
- [向量搜索索引](/tidb-cloud/vector-search-index.md)
