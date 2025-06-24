---
title: 将 TiDB 向量搜索与 Jina AI Embeddings API 集成
summary: 了解如何将 TiDB 向量搜索与 Jina AI Embeddings API 集成以存储嵌入向量并执行语义搜索。
---

# 将 TiDB 向量搜索与 Jina AI Embeddings API 集成

本教程将指导你如何使用 [Jina AI](https://jina.ai/) 为文本数据生成嵌入向量，然后将这些嵌入向量存储在 TiDB 向量存储中并基于嵌入向量搜索相似文本。

> **注意**
>
> TiDB 向量搜索仅适用于 TiDB Self-Managed（TiDB >= v8.4）和 [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)。它不适用于 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)。

## 前提条件

要完成本教程，你需要：

- 安装 [Python 3.8 或更高版本](https://www.python.org/downloads/)。
- 安装 [Git](https://git-scm.com/downloads)。
- 一个 TiDB Cloud Serverless 集群。如果你还没有，请按照[创建 TiDB Cloud Serverless 集群](/tidb-cloud/create-tidb-cluster-serverless.md)的说明创建你自己的 TiDB Cloud 集群。

## 运行示例应用

你可以按照以下步骤快速了解如何将 TiDB 向量搜索与 JinaAI Embedding 集成。

### 步骤 1. 克隆代码仓库

将 `tidb-vector-python` 代码仓库克隆到本地：

```shell
git clone https://github.com/pingcap/tidb-vector-python.git
```

### 步骤 2. 创建虚拟环境

为你的项目创建一个虚拟环境：

```bash
cd tidb-vector-python/examples/jina-ai-embeddings-demo
python3 -m venv .venv
source .venv/bin/activate
```

### 步骤 3. 安装所需依赖

安装示例项目所需的依赖：

```bash
pip install -r requirements.txt
```

### 步骤 4. 配置环境变量

从 [Jina AI Embeddings API](https://jina.ai/embeddings/) 页面获取 Jina AI API 密钥。然后，获取集群连接字符串并按如下方式配置环境变量：

1. 导航到[**集群**](https://tidbcloud.com/project/clusters)页面，然后点击目标集群的名称进入其概览页面。

2. 点击右上角的**连接**。将显示一个连接对话框。

3. 确保连接对话框中的配置与你的操作环境匹配。

   - **连接类型**设置为 `Public`
   - **分支**设置为 `main`
   - **连接方式**设置为 `SQLAlchemy`
   - **操作系统**与你的环境匹配。

   > **提示：**
   >
   > 如果你的程序在 Windows Subsystem for Linux (WSL) 中运行，请切换到相应的 Linux 发行版。

4. 切换到 **PyMySQL** 标签页，点击**复制**图标复制连接字符串。

   > **提示：**
   >
   > 如果你还没有设置密码，请点击**创建密码**生成一个随机密码。

5. 在终端中设置 Jina AI API 密钥和 TiDB 连接字符串作为环境变量，或创建一个包含以下环境变量的 `.env` 文件：

   ```dotenv
   JINAAI_API_KEY="****"
   TIDB_DATABASE_URL="{tidb_connection_string}"
   ```

   以下是 macOS 的示例连接字符串：

   ```dotenv
   TIDB_DATABASE_URL="mysql+pymysql://<prefix>.root:<password>@gateway01.<region>.prod.aws.tidbcloud.com:4000/test?ssl_ca=/etc/ssl/cert.pem&ssl_verify_cert=true&ssl_verify_identity=true"
   ```

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

### 从 Jina AI 获取嵌入向量

定义一个 `generate_embeddings` 辅助函数来调用 Jina AI embeddings API：

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

### 连接到 TiDB 集群

通过 SQLAlchemy 连接到 TiDB 集群：

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

创建一个名为 `jinaai_tidb_demo_documents` 的表，其中包含用于存储文本的 `content` 列和用于存储嵌入向量的 `content_vec` 列：

```python
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Document(Base):
    __tablename__ = "jinaai_tidb_demo_documents"

    id = Column(Integer, primary_key=True)
    content = Column(String(255), nullable=False)
    content_vec = Column(
        # DIMENSIONS 由嵌入模型决定，
        # 对于 Jina AI 的 jina-embeddings-v2-base-en 模型，它是 768。
        VectorType(dim=768),
        comment="hnsw(distance=cosine)"
```

> **注意：**
>
> - 向量列的维度必须与嵌入模型生成的嵌入向量的维度匹配。
> - 在本例中，`jina-embeddings-v2-base-en` 模型生成的嵌入向量维度为 `768`。

### 使用 Jina AI 创建嵌入向量并存储在 TiDB 中

使用 Jina AI Embeddings API 为每段文本生成嵌入向量，并将嵌入向量存储在 TiDB 中：

```python
TEXTS = [
   'Jina AI offers best-in-class embeddings, reranker and prompt optimizer, enabling advanced multimodal AI.',
   'TiDB is an open-source MySQL-compatible database that supports Hybrid Transactional and Analytical Processing (HTAP) workloads.',
]
data = []

for text in TEXTS:
    # 通过 Jina AI API 为文本生成嵌入向量。
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

### 在 TiDB 中使用 Jina AI 嵌入向量执行语义搜索

通过 Jina AI embeddings API 为查询文本生成嵌入向量，然后基于**查询文本的嵌入向量**和**向量表中的每个嵌入向量**之间的余弦距离搜索最相关的文档：

```python
query = 'What is TiDB?'
# 通过 Jina AI API 为查询生成嵌入向量。
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

- [向量数据类型](/tidb-cloud/vector-search-data-types.md)
- [向量搜索索引](/tidb-cloud/vector-search-index.md)
