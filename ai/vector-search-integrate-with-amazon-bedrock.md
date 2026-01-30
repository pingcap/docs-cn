---
title: 集成 TiDB 向量搜索与 Amazon Bedrock
summary: 学习如何将 TiDB 向量搜索与 Amazon Bedrock 集成，构建基于检索增强生成 (RAG) 的问答机器人。
---

# 集成 TiDB 向量搜索与 Amazon Bedrock

本文档将展示如何将 TiDB 的[向量搜索](/vector-search/vector-search-overview.md)功能与 [Amazon Bedrock](https://aws.amazon.com/bedrock/) 集成，构建基于检索增强生成 (RAG) 的问答机器人。

> **注意：**
>
> - 向量搜索功能目前处于 Beta 阶段，可能会在未事先通知的情况下发生变化。如果发现 bug，请在 GitHub 上提 [issue](https://github.com/pingcap/tidb/issues) 反馈。
> - 向量搜索功能适用于 TiDB、[TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)、[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-essential) 和 [TiDB Cloud Dedicated](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-dedicated)。对于 TiDB 和 TiDB Cloud Dedicated，TiDB 版本需为 v8.4.0 或更高（推荐 v8.5.0 或更高）。

> **建议：**
>
> 你可以在 Jupyter Notebook 中查看完整的[示例代码](https://github.com/aws-samples/aws-generativeai-partner-samples/blob/main/tidb/samples/tidb-bedrock-boto3-rag.ipynb)。

## 前置需求

为了能够顺利完成本文中的操作，你需要提前：

- 安装 [Python 3.11 或更高版本](https://www.python.org/downloads/)
- 安装 [Pip](https://pypi.org/project/pip/)
- 安装 [AWS CLI](https://aws.amazon.com/cli/)

    请确保你的 AWS CLI profile 已配置为 [Amazon Bedrock](https://aws.amazon.com/bedrock/) 支持的区域。支持的区域列表可参考 [Amazon Bedrock Regions](https://docs.aws.amazon.com/zh_cn/bedrock/latest/userguide/models-regions.html)。如需切换支持区域，可运行以下命令：

    ```shell
    aws configure set region <your-region>
    ```

- 创建一个 TiDB Cloud Starter 集群

    如果你还没有 TiDB Cloud 集群，请参考[创建 TiDB Cloud Starter 集群](https://docs.pingcap.com/tidbcloud/create-tidb-cluster-serverless/)创建属于你自己的 TiDB Cloud 集群。

- 创建一个 AWS 账号，该账号具有 [Amazon Bedrock 所需权限](https://docs.aws.amazon.com/zh_cn/bedrock/latest/userguide/security_iam_id-based-policy-examples.html)并能够访问以下模型：

    - **Amazon Titan Embeddings** (`amazon.titan-embed-text-v2:0`)，用于生成文本向量
    - **Meta Llama 3** (`us.meta.llama3-2-3b-instruct-v1:0`)，用于文本生成

  如果你尚未获得访问权限，请按照[申请访问 Amazon Bedrock 基础模型](https://docs.aws.amazon.com/zh_cn/bedrock/latest/userguide/getting-started.html#getting-started-model-access)的说明操作。

## 开始使用

本节将详细介绍如何将 TiDB 向量搜索功能与 Amazon Bedrock 结合使用，以构建基于 RAG 的问答机器人。

### 第 1 步：设置环境变量

从 [TiDB Cloud 控制台](https://tidbcloud.com/)获取 TiDB 连接信息，并在你的开发环境中设置环境变量，操作如下：

1. 在 TiDB Cloud 的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面，点击你的 TiDB Cloud Starter 集群名，进入集群的 **Overview** 页面。

2. 点击右上角的 **Connect** 按钮，将会弹出连接对话框。

3. 确认对话框中的配置和你的运行环境一致。

    - **Connection Type** 为 `Public`
    - **Branch** 为 `main`
    - **Connect With** 选择 `General`
    - **Operating System** 为你的运行环境

    > **建议:**
    >
    > 如果你的程序运行在 Windows Subsystem for Linux (WSL) 中，请切换到对应的 Linux 发行版。

4. 点击 **Generate Password** 生成随机密码。

    > **Tip:**
    >
    > 如果你之前已创建过密码，可以继续使用原密码，或点击 **Reset Password** 生成新密码。

5. 在终端中运行以下命令设置环境变量。你需要将命令中的占位符替换为连接对话框中获取的对应参数。

    ```shell
    export TIDB_HOST=<your-tidb-host>
    export TIDB_PORT=4000
    export TIDB_USER=<your-tidb-user>
    export TIDB_PASSWORD=<your-tidb-password>
    export TIDB_DB_NAME=test
    ```

### 第 2 步：配置 Python 虚拟环境

1. 创建一个名为 `demo.py` 的 Python 文件：

    ```shell
    touch demo.py
    ```

2. 创建并激活虚拟环境以管理依赖：

    ```shell
    python3 -m venv env
    source env/bin/activate  # 在 Windows 上使用 env\Scripts\activate
    ```

3. 安装所需依赖：

    ```shell
    pip install SQLAlchemy==2.0.30 PyMySQL==1.1.0 tidb-vector==0.0.9 pydantic==2.7.1 boto3
    ```

### 第 3 步：导入所需库

在 `demo.py` 文件开头添加以下代码以导入所需库：

```python
import os
import json
import boto3
from sqlalchemy import Column, Integer, Text, create_engine
from sqlalchemy.orm import declarative_base, Session
from tidb_vector.sqlalchemy import VectorType
```

### 第 4 步：配置数据库连接

在 `demo.py` 中添加以下代码以配置数据库连接：

```python
# ---- Configuration Setup ----
# Set environment variables: TIDB_HOST, TIDB_PORT, TIDB_USER, TIDB_PASSWORD, TIDB_DB_NAME
TIDB_HOST = os.environ.get("TIDB_HOST")
TIDB_PORT = os.environ.get("TIDB_PORT")
TIDB_USER = os.environ.get("TIDB_USER")
TIDB_PASSWORD = os.environ.get("TIDB_PASSWORD")
TIDB_DB_NAME = os.environ.get("TIDB_DB_NAME")

# ---- Database Setup ----
def get_db_url():
    """Build the database connection URL."""
    return f"mysql+pymysql://{TIDB_USER}:{TIDB_PASSWORD}@{TIDB_HOST}:{TIDB_PORT}/{TIDB_DB_NAME}?ssl_verify_cert=True&ssl_verify_identity=True"

# Create engine
engine = create_engine(get_db_url(), pool_recycle=300)
Base = declarative_base()
```

### 第 5 步：通过 Bedrock runtime client 调用 Amazon Titan Text Embeddings V2 模型

Amazon Bedrock runtime client 提供了 `invoke_model` API，可配置以下参数：

- `modelId`：Amazon Bedrock 可用基础模型的模型 ID
- `accept`：输入请求的类型
- `contentType`：输入内容的类型
- `body`：包含 prompt 和配置的 JSON 字符串负载

在 `demo.py` 中添加以下代码，通过 `invoke_model` API 使用 Amazon Titan Text Embeddings 生成文本向量，并通过 Meta Llama 3 获取响应：

```python
# Bedrock Runtime Client Setup
bedrock_runtime = boto3.client('bedrock-runtime')

# ---- Model Invocation ----
embedding_model_name = "amazon.titan-embed-text-v2:0"
dim_of_embedding_model = 512
llm_name = "us.meta.llama3-2-3b-instruct-v1:0"


def embedding(content):
    """Invoke Amazon Bedrock to get text embeddings."""
    payload = {
        "modelId": embedding_model_name,
        "contentType": "application/json",
        "accept": "*/*",
        "body": {
            "inputText": content,
            "dimensions": dim_of_embedding_model,
            "normalize": True,
        }
    }

    body_bytes = json.dumps(payload['body']).encode('utf-8')

    response = bedrock_runtime.invoke_model(
        body=body_bytes,
        contentType=payload['contentType'],
        accept=payload['accept'],
        modelId=payload['modelId']
    )

    result_body = json.loads(response.get("body").read())
    return result_body.get("embedding")


def generate_result(query: str, info_str: str):
    """Generate answer using Meta Llama 3 model."""
    prompt = f"""
    ONLY use the content below to generate an answer:
    {info_str}

    ----
    Please carefully think about the question: {query}
    """

    payload = {
        "modelId": llm_name,
        "contentType": "application/json",
        "accept": "application/json",
        "body": {
            "prompt": prompt,
            "temperature": 0
        }
    }

    body_bytes = json.dumps(payload['body']).encode('utf-8')

    response = bedrock_runtime.invoke_model(
        body=body_bytes,
        contentType=payload['contentType'],
        accept=payload['accept'],
        modelId=payload['modelId']
    )

    result_body = json.loads(response.get("body").read())
    completion = result_body["generation"]
    return completion
```

### 第 6 步：创建向量表

在 `demo.py` 中添加以下代码，创建用于存储文本及其向量的向量表：

```python
# ---- TiDB Setup and Vector Index Creation ----
class Entity(Base):
    """Define the Entity table with a vector index."""
    __tablename__ = "entity"
    id = Column(Integer, primary_key=True)
    content = Column(Text)
    content_vec = Column(VectorType(dim=dim_of_embedding_model), comment="hnsw(distance=l2)")

# Create the table in TiDB
Base.metadata.create_all(engine)
```

### 第 7 步：将向量数据保存到 TiDB Cloud Starter

在 `demo.py` 中添加以下代码，将向量数据保存到你的 TiDB Cloud Starter 集群：

```python
# ---- Saving Vectors to TiDB ----
def save_entities_with_embedding(session, contents):
    """Save multiple entities with their embeddings to the TiDB database."""
    for content in contents:
        entity = Entity(content=content, content_vec=embedding(content))
        session.add(entity)
    session.commit()
```

### 第 8 步：运行应用

1. 在 `demo.py` 中添加以下代码，建立数据库会话，将向量保存到 TiDB，提出示例问题（如 "What is TiDB?"），并从模型生成结果：

    ```python
    if __name__ == "__main__":
        # Establish a database session
        with Session(engine) as session:
            # Example data
            contents = [
                "TiDB is a distributed SQL database compatible with MySQL.",
                "TiDB supports Hybrid Transactional and Analytical Processing (HTAP).",
                "TiDB can scale horizontally and provides high availability.",
                "Amazon Bedrock allows seamless integration with foundation models.",
                "Meta Llama 3 is a powerful model for text generation."
            ]

            # Save embeddings to TiDB
            save_entities_with_embedding(session, contents)

            # Example query
            query = "What is TiDB?"
            info_str = " ".join(contents)

            # Generate result from Meta Llama 3
            result = generate_result(query, info_str)
            print(f"Generated answer: {result}")
    ```

2. 保存所有对 `demo.py` 的更改并运行脚本：

    ```shell
    python3 demo.py
    ```

    预期输出结果：

    ```
    Generated answer:  What is the main purpose of TiDB?
         What are the key features of TiDB?
         What are the key benefits of TiDB?

        ----
        Based on the provided text, here is the answer to the question:
        What is TiDB?
        TiDB is a distributed SQL database compatible with MySQL.

    ## Step 1: Understand the question
    The question asks for the definition of TiDB.

    ## Step 2: Identify the key information
    The key information provided in the text is that TiDB is a distributed SQL database compatible with MySQL.

    ## Step 3: Provide the answer
    Based on the provided text, TiDB is a distributed SQL database compatible with MySQL.

    The final answer is: TiDB is a distributed SQL database compatible with MySQL.
    ```

## 另请参阅

- [向量数据类型](/vector-search/vector-search-data-types.md)
- [向量搜索索引](/vector-search/vector-search-index.md)
