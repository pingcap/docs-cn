---
title: TiDB 向量搜索在 SQLAlchemy 中的使用
summary: 了解如何在 SQLAlchemy 中 TiDB 使用向量搜索，，以存储向量并执行语义搜索。
---

# TiDB 向量搜索在 SQLAlchemy 中的使用

本文档将展示如何使用 [SQLAlchemy](https://www.sqlalchemy.org/) 与 [TiDB 向量搜索](/vector-search-overview.md)进行交互、存储向量和执行向量搜索查询。


## 准备

1. 在开始之前，你需要确定 TiDB 集群的部署方式以及以下内容被正确安装，
    <SimpleTab>

    <div label="TiDB Serverless 集群部署">

    - [Python 3.8 or higher](https://www.python.org/downloads/)
    - [Git](https://git-scm.com/downloads) 
    - TiDB Serveless 群集。如果没有 TiDB Cloud 集群，请按照[创建 TiDB Serverless集群](https://docs.pingcap.com/tidbcloud/create-tidb-cluster-serverless)创建自己的 TiDB Cloud 集群。

    </div>

    <div label="TiDB Self-hosted 集群部署">

    - [Python 3.8 or higher](https://www.python.org/downloads/)
    - [Git](https://git-scm.com/downloads) 
    - TiDB 集群。如果没有，请按照[使用 TiUP 部署 TiDB 集群](/production-deployment-using-tiup.md)创建自己的 TiDB 集群。

    </div>

    </SimpleTab>

## 运行示例应用程序

你可以通过以下步骤快速了解如何在 SQLAlchemy 中使用 TiDB 向量搜索。

### 步骤 1. 克隆仓库

将 `tidb-vector-python` 仓库克隆到本地：

```shell
git clone https://github.com/pingcap/tidb-vector-python.git
```

### 步骤 2. 创建虚拟环境

为项目创建虚拟环境：

```bash
cd tidb-vector-python/examples/orm-sqlalchemy-quickstart
python3 -m venv .venv
source .venv/bin/activate
```

### 步骤 3. 安装所需的依赖项

安装示例项目所需的依赖项：

```bash
pip install -r requirements.txt
```

你也可以直接为项目安装以下依赖项：

```bash
pip install pymysql python-dotenv sqlalchemy tidb-vector
```

### 步骤 4. 配置环境变量
1. 根据 TiDB 集群的部署方式不同，选择对应的环境变量配置方式。

    <SimpleTab>

    <div label="TiDB Serverless 集群部署">

    1. 在 [**群集**](https://tidbcloud.com/console/clusters) 页面，单击目标群集的名称进入其概览页面。

    2. 单击右上角的**连接**。此时将显示连接对话框。

    3. 确保连接对话框中的配置符合你的运行环境。

    - **Endpoint Type** 设置为 `Public`
    - **Branch** 设置为 `main`
    - **Connect With** 设置为 `General`
    - **Operating System** 与你的机器环境相匹配

    > **Tip:**
    >
    > 如果程序在 Windows Subsystem for Linux (WSL) 中运行，请切换到相应的 Linux 发行版。

    4. 单击 **PyMySQL** 标签，复制连接字符串。

    > **Tip:**
    >
    > 如果尚未设置密码，单击**生成密码**生成一个随机密码。

    5. 在 Python 项目的根目录下创建一个 `.env` 文件，并将连接字符串粘贴到其中。

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
    - `CA`: 根证书文件的路径。

    以下是 MacOS 的示例：

    ```dotenv
    TIDB_DATABASE_URL="mysql+pymysql://<prefix>.root:<password>@127.0.0.1:4000/test?ssl_ca=/etc/ssl/cert.pem&ssl_verify_cert=true&ssl_verify_identity=true"
    ```

    </div>

    </SimpleTab>

### 步骤 5. 运行demo

```bash
python sqlalchemy-quickstart.py
```

输出示例:

```text
Get 3-nearest neighbor documents:
  - distance: 0.00853986601633272
    document: fish
  - distance: 0.12712843905603044
    document: dog
  - distance: 0.7327387580875756
    document: tree
Get documents within a certain distance:
  - distance: 0.00853986601633272
    document: fish
  - distance: 0.12712843905603044
    document: dog
```

## 示例代码片段

你可以参考以下示例代码片段来完成自己的程序开发。

### 创建向量表

#### 连接至 TiDB 集群

```python
import os
import dotenv

from sqlalchemy import Column, Integer, create_engine, Text
from sqlalchemy.orm import declarative_base, Session
from tidb_vector.sqlalchemy import VectorType

dotenv.load_dotenv()

tidb_connection_string = os.environ['TIDB_DATABASE_URL']
engine = create_engine(tidb_connection_string)
```

#### 定义向量列

创建一个表格，其中有一列向量类型的 `embedding` ，用于存储三维向量。

```python
Base = declarative_base()

class Document(Base):
    __tablename__ = 'sqlalchemy_demo_documents'
    id = Column(Integer, primary_key=True)
    content = Column(Text)
    embedding = Column(VectorType(3))
```

### 存储带有向量的文档

```python
with Session(engine) as session:
   session.add(Document(content="dog", embedding=[1, 2, 1]))
   session.add(Document(content="fish", embedding=[1, 2, 4]))
   session.add(Document(content="tree", embedding=[1, 0, 0]))
   session.commit()
```

### 搜索近邻向量

我们可以选择使用余弦距离 (`CosineDistance`) 函数，查询与向量 `[1, 2, 3]` 语义最接近的前 3 个内容。

```python
with Session(engine) as session:
   distance = Document.embedding.cosine_distance([1, 2, 3]).label('distance')
   results = session.query(
      Document, distance
   ).order_by(distance).limit(3).all()
```

### 搜索一定距离内的向量

我们可以选择使用余弦距离 (`CosineDistance`) 函数，查询与向量 `[1, 2, 3]` 的余弦距离小于 0.2 的向量。

```python
with Session(engine) as session:
    distance = Document.embedding.cosine_distance([1, 2, 3]).label('distance')
    results = session.query(
        Document, distance
    ).filter(distance < 0.2).order_by(distance).limit(3).all()
```

## 另请参阅

- [向量数据类型](/vector-search-data-types.md)