---
title: 将 TiDB Vector Search 与 SQLAlchemy 集成
summary: 了解如何将 TiDB Vector Search 与 SQLAlchemy 集成以存储嵌入向量并执行语义搜索。
---

# 将 TiDB Vector Search 与 SQLAlchemy 集成

本教程将指导你如何使用 [SQLAlchemy](https://www.sqlalchemy.org/) 与 [TiDB Vector Search](/tidb-cloud/vector-search-overview.md) 交互，存储嵌入向量并执行向量搜索查询。

> **注意**
>
> TiDB Vector Search 仅适用于 TiDB Self-Managed（TiDB >= v8.4）和 [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)。它不适用于 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)。

## 前提条件

完成本教程需要：

- 安装 [Python 3.8 或更高版本](https://www.python.org/downloads/)。
- 安装 [Git](https://git-scm.com/downloads)。
- 一个 TiDB Cloud Serverless 集群。如果你还没有，请按照[创建 TiDB Cloud Serverless 集群](/tidb-cloud/create-tidb-cluster-serverless.md)的说明创建自己的 TiDB Cloud 集群。

## 运行示例应用

你可以按照以下步骤快速了解如何将 TiDB Vector Search 与 SQLAlchemy 集成。

### 步骤 1. 克隆代码仓库

将 `tidb-vector-python` 代码仓库克隆到本地：

```shell
git clone https://github.com/pingcap/tidb-vector-python.git
```

### 步骤 2. 创建虚拟环境

为你的项目创建一个虚拟环境：

```bash
cd tidb-vector-python/examples/orm-sqlalchemy-quickstart
python3 -m venv .venv
source .venv/bin/activate
```

### 步骤 3. 安装所需依赖

安装示例项目所需的依赖：

```bash
pip install -r requirements.txt
```

或者，你可以为你的项目安装以下包：

```bash
pip install pymysql python-dotenv sqlalchemy tidb-vector
```

### 步骤 4. 配置环境变量

1. 导航到 [**Clusters**](https://tidbcloud.com/project/clusters) 页面，然后点击目标集群的名称进入其概览页面。

2. 点击右上角的 **Connect**。将显示连接对话框。

3. 确保连接对话框中的配置与你的环境匹配。

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

5. 在 Python 项目的根目录下创建一个 `.env` 文件，并将连接字符串粘贴到其中。

   以下是 macOS 的示例：

   ```dotenv
   TIDB_DATABASE_URL="mysql+pymysql://<prefix>.root:<password>@gateway01.<region>.prod.aws.tidbcloud.com:4000/test?ssl_ca=/etc/ssl/cert.pem&ssl_verify_cert=true&ssl_verify_identity=true"
   ```

### 步骤 5. 运行示例

```bash
python sqlalchemy-quickstart.py
```

示例输出：

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

你可以参考以下示例代码片段来开发你的应用。

### 创建向量表

#### 连接到 TiDB 集群

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

创建一个包含名为 `embedding` 的列的表，该列存储 3 维向量。

```python
Base = declarative_base()

class Document(Base):
    __tablename__ = 'sqlalchemy_demo_documents'
    id = Column(Integer, primary_key=True)
    content = Column(Text)
    embedding = Column(VectorType(3))
```

### 存储带有嵌入向量的文档

```python
with Session(engine) as session:
   session.add(Document(content="dog", embedding=[1, 2, 1]))
   session.add(Document(content="fish", embedding=[1, 2, 4]))
   session.add(Document(content="tree", embedding=[1, 0, 0]))
   session.commit()
```

### 搜索最近邻文档

搜索与查询向量 `[1, 2, 3]` 在语义上最接近的前 3 个文档，基于余弦距离函数。

```python
with Session(engine) as session:
   distance = Document.embedding.cosine_distance([1, 2, 3]).label('distance')
   results = session.query(
      Document, distance
   ).order_by(distance).limit(3).all()
```

### 搜索特定距离内的文档

搜索与查询向量 `[1, 2, 3]` 的余弦距离小于 0.2 的文档。

```python
with Session(engine) as session:
    distance = Document.embedding.cosine_distance([1, 2, 3]).label('distance')
    results = session.query(
        Document, distance
    ).filter(distance < 0.2).order_by(distance).limit(3).all()
```

## 另请参阅

- [向量数据类型](/tidb-cloud/vector-search-data-types.md)
- [向量搜索索引](/tidb-cloud/vector-search-index.md)
