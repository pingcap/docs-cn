---
title: 结合 Jina AI 嵌入模型 API 使用 TiDB 向量搜索
summary: 了解如何结合 Jina AI 嵌入模型 API 使用 TiDB 向量搜索，以存储向量嵌入信息并执行语义搜索。
---

# 结合 Jina AI 嵌入模型 API 使用 TiDB 向量搜索

本文档将展示如何使用 [Jina AI](https://jina.ai/) 为文本数据生成向量嵌入，然后将向量嵌入存储在 TiDB 中，并根据向量嵌入搜索相似文本。

## 前置需求

To complete this tutorial, you need:

- 推荐 [Python 3.8](https://www.python.org/downloads/) 及以上版本。
- [Git](https://git-scm.com/downloads)。
- TiDB 集群，如果你还没有 TiDB 集群，可以按照以下方式创建：
  - TiDB Serverless 集群。如果没有 TiDB Cloud 集群，请按照 [创建 TiDB Serverless集群](https://dev.mysql.com/doc/refman/8.4/en/mysql.html) 创建自己的 TiDB Cloud 集群。
  - 本地部署的 TiDB 集群。如果没有集群，请按照 [使用 TiUP 部署 TiDB 集群](/production-deployment-using-tiup.md) 创建自己的 TiDB 集群。

## 运行示例程序

您可以通过以下步骤快速了解如何结合 Jina AI 嵌入模型 API 使用 TiDB 向量搜索。

### 步骤 1. 克隆代码库

将 `tidb-vector-python` 仓库克隆到本地：

```shell
git clone https://github.com/pingcap/tidb-vector-python.git
```

### 步骤 2. 创建虚拟环境

为项目创建虚拟环境：

```bash
cd tidb-vector-python/examples/jina-ai-embeddings-demo
python3 -m venv .venv
source .venv/bin/activate
```

### 步骤 3. 安装所需的依赖项

安装项目所需的依赖项：

```bash
pip install -r requirements.txt
```

### 步骤 4. 配置环境变量

#### 4.1 获取 Jina AI API 密钥

从 [Jina AI Embeddings API](https://jina.ai/embeddings/) 页面获取 Jina AI API 密钥。

<SimpleTab>

<div label="TiDB Serverless 集群部署">

#### 4.2 获取 TiDB 连接参数

1. 在 [**Cluster**](https://tidbcloud.com/console/clusters) 界面，单击目标群集的名称进入其概览页面。

2. 单击右上角的**Connect**。此时将显示连接对话框。

3. 确保连接对话框中的配置符合您的运行环境。

   - **Connection Type** 设置为 `Public`.
   - **Branch** 设置为 `main`.
   - **Connect With** 设置为 `SQLAlchemy`.
   - **Operating System** 与你的系统环境相匹配.

   > **Tip:**
   >
   > 如果程序在 Windows Subsystem for Linux (WSL) 中运行，请切换到相应的 Linux 发行版。


4. 点击 **PyMySQL** 标签，复制连接字符串。

   > **Tip:**
   >
   > 如果尚未设置密码，请单击**Generate Password**生成一个随机密码。

#### 4.3 设置环境变量

在终端中设置环境变量，或创建一个包含上述环境变量的 `.env` 文件。


```dotenv
JINAAI_API_KEY="****"
TIDB_DATABASE_URL="{tidb_connection_string}"
```

例如，macOS 上的连接字符串如下所示：

```dotenv
TIDB_DATABASE_URL="mysql+pymysql://<prefix>.root:<password>@gateway01.<region>.prod.aws.tidbcloud.com:4000/test?ssl_ca=/etc/ssl/cert.pem&ssl_verify_cert=true&ssl_verify_identity=true"
```

</div>

<div label="本地部署 TiDB">

#### 4.2 设置 TiDB 连接参数

- 创建一个包含如下环境变量的 `.env` 文件：
  - TIDB_HOST='{host}'
  - TIDB_PORT='4000'
  - TIDB_USER='root'
  - TIDB_PASSWORD='{password}'
  - TIDB_DB_NAME='test'

    注意替换 {} 中的占位符为你的 TiDB 对应的值，并删除 CA_PATH 这行。如果你在本机运行 TiDB，默认 Host 地址为 127.0.0.1，密码为空。

- 在终端中设置环境变量

    ```dotenv
    JINAAI_API_KEY="****"
    TIDB_DATABASE_URL="{tidb_connection_string}"
    ```
    例如，macOS 上的连接字符串如下所示：
    ```dotenv
    TIDB_DATABASE_URL="mysql+pymysql://<prefix>.root:<password>@gateway01.<region>.prod.aws.tidbcloud.com:4000/test?ssl_ca=/etc/ssl/cert.pem&ssl_verify_cert=true&ssl_verify_identity=true"
    ```
    注意替换为你的 TiDB 实际对应的值。
</div>

</SimpleTab>

### 步骤 5. 运行示例

```bash
python jina-ai-embeddings-demo.py
```

示例输出：

```text
- Inserting Data to TiDB...
  - Inserting: Jina AI offers best-in-class embeddings, reranker and prompt optimizer, enabling advanced multimodal AI.
  - Inserting: TiDB is an open-source MySQL-compatible database that supports Hybrid Transactional and Analytical Processing (HTAP) workloads.
- List All Documents and Their Distances to the Query:
  - distance: 0.3585317326132522
    content: Jina AI offers best-in-class embeddings, reranker and prompt optimizer, enabling advanced multimodal AI.
  - distance: 0.10858102967720984
    content: TiDB is an open-source MySQL-compatible database that supports Hybrid Transactional and Analytical Processing (HTAP) workloads.
- The Most Relevant Document and Its Distance to the Query:
  - distance: 0.10858102967720984
    content: TiDB is an open-source MySQL-compatible database that supports Hybrid Transactional and Analytical Processing (HTAP) workloads.
```

## 示例代码片段

### 从 Jina AI 获取嵌入信息

定义一个 `generate_embeddings` 函数，用于调用 Jina AI 的嵌入 API：

```python
import os
import requests
import dotenv

dotenv.load_dotenv()

JINAAI_API_KEY = os.getenv('JINAAI_API_KEY')

def generate_embeddings(text: str):
    JINAAI_API_URL = 'https://api.jina.ai/v1/embeddings'
    JINAAI_HEADERS = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {JINAAI_API_KEY}'
    }
    JINAAI_REQUEST_DATA = {
        'input': [text],
        'model': 'jina-embeddings-v2-base-en'  # with dimension 768.
    }
    response = requests.post(JINAAI_API_URL, headers=JINAAI_HEADERS, json=JINAAI_REQUEST_DATA)
    return response.json()['data'][0]['embedding']
```

### 连接至 TiDB Serverless

通过 SQLAlchemy 连接 TiDB Serverless：

```python
import os
import dotenv

from tidb_vector.sqlalchemy import VectorType
from sqlalchemy.orm import Session, declarative_base

dotenv.load_dotenv()

TIDB_DATABASE_URL = os.getenv('TIDB_DATABASE_URL')
assert TIDB_DATABASE_URL is not None
engine = create_engine(url=TIDB_DATABASE_URL, pool_recycle=300)
```

### 定义向量表模式

创建名为 `jinaai_tidb_demo_documents` 的表，其中的 `content` 列用于存储文本，名为 `content_vec` 的向量列用于存储向量嵌入：

```python
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Document(Base):
    __tablename__ = "jinaai_tidb_demo_documents"

    id = Column(Integer, primary_key=True)
    content = Column(String(255), nullable=False)
    content_vec = Column(
        # DIMENSIONS is determined by the embedding model,
        # for Jina AI's jina-embeddings-v2-base-en model it's 768.
        VectorType(dim=768),
        comment="hnsw(distance=cosine)"
```

> **Note:**
>
> - 向量列的维度必须与嵌入模型生成的向量嵌入维度相匹配。
> - 在本例中，`jina-embeddings-v2-base-en` 模型生成的向量嵌入维度是 “768”。

### 使用 Jina AI 生成向量嵌入并存入 TiDB 

使用 Jina AI 嵌入 API 为每个文本生成向量嵌入，并将这些向量存储在 TiDB 中：

```python
TEXTS = [
   'Jina AI offers best-in-class embeddings, reranker and prompt optimizer, enabling advanced multimodal AI.',
   'TiDB is an open-source MySQL-compatible database that supports Hybrid Transactional and Analytical Processing (HTAP) workloads.',
]
data = []

for text in TEXTS:
    # Generate embeddings for the texts via Jina AI API.
    embedding = generate_embeddings(text)
    data.append({
        'text': text,
        'embedding': embedding
    })

with Session(engine) as session:
   print('- Inserting Data to TiDB...')
   for item in data:
      print(f'  - Inserting: {item["text"]}')
      session.add(Document(
         content=item['text'],
         content_vec=item['embedding']
      ))
   session.commit()
```

### 使用 Jina AI 生成的向量嵌入在 TiDB 中执行语义搜索

通过 Jina AI 嵌入 API 生成查询文本的向量嵌入，然后根据查询向量嵌入和文档向量嵌入之间的余弦距离搜索最相关的文档：

```python
query = 'What is TiDB?'
# 通过 Jina AI API 生成查询向量嵌入
query_embedding = generate_embeddings(query)

with Session(engine) as session:
    print('- The Most Relevant Document and Its Distance to the Query:')
    doc, distance = session.query(
        Document,
        Document.content_vec.cosine_distance(query_embedding).label('distance')
    ).order_by(
        'distance'
    ).limit(1).first()
    print(f'  - distance: {distance}\n'
          f'    content: {doc.content}')
```

## 另请参阅

- [向量数据类型](/vector-search-data-types.md)