---
title: 将 TiDB 向量搜索与 Amazon Bedrock 集成
summary: 了解如何将 TiDB 向量搜索与 Amazon Bedrock 集成以构建检索增强生成（RAG）问答机器人。
---

# 将 TiDB 向量搜索与 Amazon Bedrock 集成

本教程演示如何将 TiDB 的[向量搜索](/tidb-cloud/vector-search-overview.md)功能与 [Amazon Bedrock](https://aws.amazon.com/bedrock/) 集成，以构建检索增强生成（RAG）问答机器人。

> **注意**
>
> TiDB 向量搜索仅适用于 TiDB Self-Managed（TiDB >= v8.4）和 [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)。它不适用于 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)。

> **提示**
>
> 你可以在 Notebook 格式中查看完整的[示例代码](https://github.com/aws-samples/aws-generativeai-partner-samples/blob/main/tidb/samples/tidb-bedrock-boto3-rag.ipynb)。

## 前提条件

要完成本教程，你需要：

- 安装 [Python 3.11 或更高版本](https://www.python.org/downloads/)
- 安装 [Pip](https://pypi.org/project/pip/)
- 安装 [AWS CLI](https://aws.amazon.com/cli/)

    确保你的 AWS CLI 配置文件配置为本教程支持的 [Amazon Bedrock](https://aws.amazon.com/bedrock/) 区域。你可以在 [Amazon Bedrock 区域](https://docs.aws.amazon.com/bedrock/latest/userguide/models-regions.html)找到支持的区域列表。要切换到支持的区域，请运行以下命令：

    ```shell
    aws configure set region <your-region>
    ```

- 一个 TiDB Cloud Serverless 集群

    如果你没有集群，请按照[创建 TiDB Cloud Serverless 集群](/tidb-cloud/create-tidb-cluster-serverless.md)的说明创建自己的 TiDB Cloud 集群。

- 具有 [Amazon Bedrock 所需权限](https://docs.aws.amazon.com/bedrock/latest/userguide/security_iam_id-based-policy-examples.html)并可访问以下模型的 AWS 账户：

    - **Amazon Titan Embeddings**（`amazon.titan-embed-text-v2:0`），用于生成文本嵌入
    - **Meta Llama 3**（`us.meta.llama3-2-3b-instruct-v1:0`），用于文本生成

  如果你没有访问权限，请按照[请求访问 Amazon Bedrock 基础模型](https://docs.aws.amazon.com/bedrock/latest/userguide/getting-started.html#getting-started-model-access)中的说明操作。

## 开始使用

本节提供将 TiDB 向量搜索与 Amazon Bedrock 集成以构建基于 RAG 的问答机器人的分步说明。

### 步骤 1. 设置环境变量

从 [TiDB Cloud 控制台](https://tidbcloud.com/)获取 TiDB 连接信息，并在开发环境中设置环境变量，如下所示：

1. 导航到[**集群**](https://tidbcloud.com/project/clusters)页面，然后点击目标集群的名称进入其概览页面。

2. 点击右上角的**连接**。此时会显示连接对话框。

3. 确保连接对话框中的配置与你的操作环境匹配。

    - **连接类型**设置为 `Public`
    - **分支**设置为 `main`
    - **连接方式**设置为 `General`
    - **操作系统**与你的环境匹配。

    > **提示：**
    >
    > 如果你的程序在 Windows Subsystem for Linux (WSL) 中运行，请切换到相应的 Linux 发行版。

4. 点击**生成密码**创建随机密码。

    > **提示：**
    >
    > 如果你之前已经创建了密码，可以使用原始密码或点击**重置密码**生成新密码。

5. 在终端中运行以下命令来设置环境变量。你需要将命令中的占位符替换为从连接对话框获得的相应连接参数。

    ```shell
    export TIDB_HOST=<your-tidb-host>
    export TIDB_PORT=4000
    export TIDB_USER=<your-tidb-user>
    export TIDB_PASSWORD=<your-tidb-password>
    export TIDB_DB_NAME=test
    ```

### 步骤 2. 设置 Python 虚拟环境

1. 创建一个名为 `demo.py` 的 Python 文件：

    ```shell
    touch demo.py
    ```

2. 创建并激活虚拟环境以管理依赖项：

    ```shell
    python3 -m venv env
    source env/bin/activate  # 在 Windows 上，使用 env\Scripts\activate
    ```

3. 安装所需的依赖项：

    ```shell
    pip install SQLAlchemy==2.0.30 PyMySQL==1.1.0 tidb-vector==0.0.9 pydantic==2.7.1 boto3
    ```

### 步骤 3. 导入所需库

在 `demo.py` 的开头添加以下代码以导入所需的库：

```python
import os
import json
import boto3
from sqlalchemy import Column, Integer, Text, create_engine
from sqlalchemy.orm import declarative_base, Session
from tidb_vector.sqlalchemy import VectorType
```

### 步骤 4. 配置数据库连接

在 `demo.py` 中，添加以下代码以配置数据库连接：

```python
# ---- 配置设置 ----
# 设置环境变量：TIDB_HOST, TIDB_PORT, TIDB_USER, TIDB_PASSWORD, TIDB_DB_NAME
TIDB_HOST = os.environ.get("TIDB_HOST")
TIDB_PORT = os.environ.get("TIDB_PORT")
TIDB_USER = os.environ.get("TIDB_USER")
TIDB_PASSWORD = os.environ.get("TIDB_PASSWORD")
TIDB_DB_NAME = os.environ.get("TIDB_DB_NAME")

# ---- 数据库设置 ----
def get_db_url():
    """构建数据库连接 URL。"""
    return f"mysql+pymysql://{TIDB_USER}:{TIDB_PASSWORD}@{TIDB_HOST}:{TIDB_PORT}/{TIDB_DB_NAME}?ssl_verify_cert=True&ssl_verify_identity=True"

# 创建引擎
engine = create_engine(get_db_url(), pool_recycle=300)
Base = declarative_base()
```

### 步骤 5. 使用 Bedrock 运行时客户端调用 Amazon Titan Text Embeddings V2 模型

Amazon Bedrock 运行时客户端提供了一个 `invoke_model` API，它接受以下参数：

- `modelId`：Amazon Bedrock 中可用的基础模型的模型 ID。
- `accept`：输入请求的类型。
- `contentType`：输入的内容类型。
- `body`：由提示和配置组成的 JSON 字符串负载。

在 `demo.py` 中，添加以下代码以调用 `invoke_model` API，使用 Amazon Titan Text Embeddings 生成文本嵌入并从 Meta Llama 3 获取响应：

```python
# Bedrock 运行时客户端设置
bedrock_runtime = boto3.client('bedrock-runtime')

# ---- 模型调用 ----
embedding_model_name = "amazon.titan-embed-text-v2:0"
dim_of_embedding_model = 512
llm_name = "us.meta.llama3-2-3b-instruct-v1:0"


def embedding(content):
    """调用 Amazon Bedrock 获取文本嵌入。"""
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
    """使用 Meta Llama 3 模型生成答案。"""
    prompt = f"""
    仅使用以下内容生成答案：
    {info_str}

    ----
    请仔细思考这个问题：{query}
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

### 步骤 6. 创建向量表

在 `demo.py` 中，添加以下代码以创建一个用于存储文本和向量嵌入的向量表：

```python
# ---- TiDB 设置和向量索引创建 ----
class Entity(Base):
    """定义带有向量索引的 Entity 表。"""
    __tablename__ = "entity"
    id = Column(Integer, primary_key=True)
    content = Column(Text)
    content_vec = Column(VectorType(dim=dim_of_embedding_model), comment="hnsw(distance=l2)")

# 在 TiDB 中创建表
Base.metadata.create_all(engine)
```

### 步骤 7. 将向量数据保存到 TiDB Cloud Serverless

在 `demo.py` 中，添加以下代码以将向量数据保存到你的 TiDB Cloud Serverless 集群：

```python
# ---- 将向量保存到 TiDB ----
def save_entities_with_embedding(session, contents):
    """将多个实体及其嵌入保存到 TiDB Serverless 数据库。"""
    for content in contents:
        entity = Entity(content=content, content_vec=embedding(content))
        session.add(entity)
    session.commit()
```

### 步骤 8. 运行应用程序

1. 在 `demo.py` 中，添加以下代码以建立数据库会话，将嵌入保存到 TiDB，提出示例问题（如"什么是 TiDB？"），并从模型生成结果：

    ```python
    if __name__ == "__main__":
        # 建立数据库会话
        with Session(engine) as session:
            # 示例数据
            contents = [
                "TiDB 是一个与 MySQL 兼容的分布式 SQL 数据库。",
                "TiDB 支持混合事务和分析处理（HTAP）。",
                "TiDB 可以水平扩展并提供高可用性。",
                "Amazon Bedrock 允许与基础模型无缝集成。",
                "Meta Llama 3 是一个强大的文本生成模型。"
            ]

            # 将嵌入保存到 TiDB
            save_entities_with_embedding(session, contents)

            # 示例查询
            query = "什么是 TiDB？"
            info_str = " ".join(contents)

            # 从 Meta Llama 3 生成结果
            result = generate_result(query, info_str)
            print(f"生成的答案：{result}")
    ```

2. 保存对 `demo.py` 的所有更改并运行脚本：

    ```shell
    python3 demo.py
    ```

    预期输出类似于以下内容：

    ```
    生成的答案： 什么是 TiDB 的主要目的？
         TiDB 的主要特性是什么？
         TiDB 的主要优势是什么？

        ----
        根据提供的文本，以下是对问题的回答：
        什么是 TiDB？
        TiDB 是一个与 MySQL 兼容的分布式 SQL 数据库。

    ## 步骤 1：理解问题
    问题询问 TiDB 的定义。

    ## 步骤 2：识别关键信息
    文本中提供的关键信息是 TiDB 是一个与 MySQL 兼容的分布式 SQL 数据库。

    ## 步骤 3：提供答案
    根据提供的文本，TiDB 是一个与 MySQL 兼容的分布式 SQL 数据库。

    最终答案是：TiDB 是一个与 MySQL 兼容的分布式 SQL 数据库。
    ```

## 另请参阅

- [向量数据类型](/tidb-cloud/vector-search-data-types.md)
- [向量搜索索引](/tidb-cloud/vector-search-index.md)
