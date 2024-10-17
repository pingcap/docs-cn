---
title: 结合 Jina AI 嵌入模型 API 使用 TiDB 向量搜索
summary: 了解如何结合 Jina AI 嵌入模型 API 使用 TiDB 向量搜索，以存储向量嵌入信息并执行语义搜索。
---

# 结合 Jina AI 嵌入模型 API 使用 TiDB 向量搜索

本文档将展示如何使用 [Jina AI](https://jina.ai/) 为文本数据生成向量嵌入，然后将向量嵌入存储在 TiDB 中，并根据向量嵌入搜索相似文本。

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

## 运行示例应用程序

您可以通过以下步骤快速了解如何结合 Jina AI 嵌入模型 API 使用 TiDB 向量搜索。

### 第 1 步：克隆示例代码仓库

将 `tidb-vector-python` 仓库克隆到本地：

```shell
git clone https://github.com/pingcap/tidb-vector-python.git
```

### 第 2 步：创建虚拟环境

为你的项目创建虚拟环境：

```bash
cd tidb-vector-python/examples/jina-ai-embeddings-demo
python3 -m venv .venv
source .venv/bin/activate
```

### 第 3 步：安装所需的依赖

安装项目所需的依赖：

```bash
pip install -r requirements.txt
```

### 第 4 步：配置环境变量

从 [Jina AI Embeddings API](https://jina.ai/embeddings/) 页面获取 Jina AI API 密钥，然后根据 TiDB 集群的部署方式不同，选择对应的环境变量配置方式。

<SimpleTab>

<div label="本地部署 TiDB">

对于本地部署的 TiDB，你可以通过在终端中直接设置环境变量以连接 TiDB 集群：

```shell
export JINA_API_KEY="****"
export TIDB_DATABASE_URL="mysql+pymysql://<USERNAME>:<PASSWORD>@<HOST>:<PORT>/<DATABASE>"
# 例如：export TIDB_DATABASE_URL="mysql+pymysql://root@127.0.0.1:4000/test"
```

请替换命令中的参数为你的 TiDB 实际对应的值。如果你在本机运行 TiDB，`<HOST>` 默认为 `127.0.0.1`。`<PASSWORD>` 初始密码为空，若你是第一次启动集群，则无需带上此字段。

以下为各参数的解释：

- `<USERNAME>`：连接 TiDB 集群的用户名。
- `<PASSWORD>`：连接 TiDB 集群的密码。
- `<HOST>`：TiDB 集群的主机地址。
- `<PORT>`：TiDB 集群的端口号。
- `<DATABASE>`：要连接的数据库名称。

</div>

<div label="TiDB Cloud Serverless">

对于 TiDB Cloud Serverless 集群，请按照以下步骤配置 TiDB 连接参数：

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

4. 点击 **PyMySQL** 选项卡，复制连接字符串。

   > **Tip:**
   >
   > 如果你还没有设置密码，点击 **Generate Password** 生成一个随机密码。

5. 在终端中将 Jina AI API 密钥以及连接字符串设置为环境变量，或创建一个包含以下环境变量的 `.env` 文件。

    ```dotenv
    JINAAI_API_KEY="****"
    TIDB_DATABASE_URL="{tidb_connection_string}"
    ```

    以下为 macOS 上的连接字符串示例：

    ```dotenv
    TIDB_DATABASE_URL="mysql+pymysql://<prefix>.root:<password>@gateway01.<region>.prod.aws.tidbcloud.com:4000/test?ssl_ca=/etc/ssl/cert.pem&ssl_verify_cert=true&ssl_verify_identity=true"
    ```

</div>
</SimpleTab>

### 第 5 步：运行示例应用程序

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

### 通过 Jina AI 获取嵌入信息

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

### 连接到 TiDB 集群

通过 SQLAlchemy 连接 TiDB 集群：

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

### 定义向量表结构

创建一张 `jinaai_tidb_demo_documents` 表，其中包含一个 `content` 列用于存储文本，一个 `content_vec` 向量列用于存储向量嵌入：

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
        VectorType(dim=768)
    )
```

> **注意：**
>
> - 向量列的维度必须与嵌入模型生成的向量嵌入维度相同。
> - 在本例中，`jina-embeddings-v2-base-en` 模型生成的向量嵌入维度为 `768`。

### 使用 Jina AI 生成向量嵌入并存入 TiDB

使用 Jina AI 嵌入 API 为每条文本生成向量嵌入，并将这些向量存储在 TiDB 中：

```python
TEXTS = [
   'Jina AI offers best-in-class embeddings, reranker and prompt optimizer, enabling advanced multimodal AI.',
   'TiDB is an open-source MySQL-compatible database that supports Hybrid Transactional and Analytical Processing (HTAP) workloads.',
]
data = []

for text in TEXTS:
    # 通过 Jina AI API 生成文本的向量嵌入
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

通过 Jina AI 的嵌入 API 生成查询文本的向量嵌入，然后根据**查询文本的向量嵌入**和**向量表中各个向量嵌入**之间的余弦距离搜索最相关的 `document`：

```python
query = 'What is TiDB?'
# 通过 Jina AI API 生成查询文本的向量嵌入
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
- [向量搜索索引](/vector-search-index.md)