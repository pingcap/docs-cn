---
title: TiDB 向量搜索与 SQLAlchemy 结合
summary: 了解如何将 TiDB 向量搜索与 SQLAlchemy 结合，以存储embedding并执行语义搜索。
---

# TiDB 向量搜索与 SQLAlchemy 结合

本教程将展示如何使用 [SQLAlchemy](https://www.sqlalchemy.org/)与 [TiDB 向量搜索](/tidb-cloud/vector-search-overview.md)交互、存储嵌入和执行向量搜索查询。


## Prerequisites

要实现本部分的内容，需要确保安装以下内容：

- [Python 3.8 or higher](https://www.python.org/downloads/) installed.
- [Git](https://git-scm.com/downloads) installed.
- TiDB serverless集群。如果没有，请按照[使用 TiDB Serverless 构建 TiDB 集群](/develop/dev-guide-build-cluster-in-cloud.md)创建自己的 TiDB 集群。

## 运行示例应用程序

您可以通过以下步骤快速了解如何将 TiDB 向量搜索与 SQLAlchemy 结合。

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

您可以为现有项目安装以下软件包：

```bash
pip install pymysql python-dotenv sqlalchemy tidb-vector
```

### 步骤 4. 配置环境变量

1. 导航至 [** 群集**](https://tidbcloud.com/console/clusters) 页面，然后单击目标群集的名称进入其概览页面。

2. 单击右上角的**连接**。此时将显示连接对话框。

3. 确保连接对话框中的配置符合您的运行环境。

    - **Endpoint Type** 设置为 `Public`.
    - **Branch** 设置为 `main`.
    - **Connect With** 设置为 `SQLAlchemy`.
    - **Operating System** 与环境相匹配.

    > **Tip:**
    >
    > 如果程序在 Windows Subsystem for Linux (WSL) 中运行，请切换到相应的 Linux 发行版。

4. 单击 **PyMySQL** 标签，复制连接字符串。

    > **Tip:**
    >
    > 如果尚未设置密码，请单击**生成密码**生成一个随机密码。

5. 在 Python 项目的根目录下创建一个 `.env` 文件，并将连接字符串粘贴到其中。

    以下是 MacOS 的示例：

    ```dotenv
    TIDB_DATABASE_URL="mysql+pymysql://<prefix>.root:<password>@gateway01.<region>.prod.aws.tidbcloud.com:4000/test?ssl_ca=/etc/ssl/cert.pem&ssl_verify_cert=true&ssl_verify_identity=true"
    ```

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

您可以参考以下示例代码片段来开发您的应用程序。

### 创建矢量表

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

创建一个表格，其中有一列名为 `embedding`，用于存储三维向量。

```python
Base = declarative_base()

class Document(Base):
    __tablename__ = 'sqlalchemy_demo_documents'
    id = Column(Integer, primary_key=True)
    content = Column(Text)
    embedding = Column(VectorType(3))
```

#### 用索引定义优化的矢量列

定义三维矢量列，并使用[矢量搜索索引](/vector-search-index.md) （HNSW 索引）对其进行优化。

```python
class DocumentWithIndex(Base):
    __tablename__ = 'sqlalchemy_demo_documents_with_index'
    id = Column(Integer, primary_key=True)
    content = Column(Text)
    embedding = Column(VectorType(3), comment="hnsw(distance=cosine)")
```

TiDB 将使用该索引来加速基于余弦距离函数的矢量搜索查询。

### 存储带有向量的文档

```python
with Session(engine) as session:
   session.add(Document(content="dog", embedding=[1, 2, 1]))
   session.add(Document(content="fish", embedding=[1, 2, 4]))
   session.add(Document(content="tree", embedding=[1, 0, 0]))
   session.commit()
```

### 搜索近邻向量

根据余弦距离函数，搜索与查询向量`[1, 2, 3]`”`语义最接近的前 3 篇向量。

```python
with Session(engine) as session:
   distance = Document.embedding.cosine_distance([1, 2, 3]).label('distance')
   results = session.query(
      Document, distance
   ).order_by(distance).limit(3).all()
```

### 搜索一定距离内的向量

搜索与查询向量`[1, 2, 3]`的余弦距离小于 0.2 的文档。

```python
with Session(engine) as session:
    distance = Document.embedding.cosine_distance([1, 2, 3]).label('distance')
    results = session.query(
        Document, distance
    ).filter(distance < 0.2).order_by(distance).limit(3).all()
```

## See also

- [向量数据类型](/vector-search-data-types.md)
- [向量搜索索引](/vector-search-index.md)