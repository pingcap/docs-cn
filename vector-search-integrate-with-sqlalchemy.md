---
title: 在 SQLAlchemy 中使用 TiDB 向量搜索
summary: 了解如何在 SQLAlchemy 中通过 TiDB 向量搜索功能存储向量并执行语义搜索。
---

# 在 SQLAlchemy 中使用 TiDB 向量搜索

本文档将展示如何使用 [SQLAlchemy](https://www.sqlalchemy.org/) 与 [TiDB 向量搜索](/vector-search-overview.md)进行交互，以及如何存储向量和执行向量搜索查询。

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

你可以通过以下步骤快速了解如何在 SQLAlchemy 中使用 TiDB 向量搜索。

### 第 1 步：克隆示例代码仓库

将 `tidb-vector-python` 仓库克隆到本地：

```shell
git clone https://github.com/pingcap/tidb-vector-python.git
```

### 第 2 步：创建虚拟环境

为你的项目创建虚拟环境：

```bash
cd tidb-vector-python/examples/orm-sqlalchemy-quickstart
python3 -m venv .venv
source .venv/bin/activate
```

### 第 3 步：安装所需的依赖

安装示例项目所需的依赖：

```bash
pip install -r requirements.txt
```

你也可以直接为项目安装以下依赖项：

```bash
pip install pymysql python-dotenv sqlalchemy tidb-vector
```

### 第 4 步：配置环境变量

根据 TiDB 集群的部署方式不同，选择对应的环境变量配置方式。

<SimpleTab>

<div label="TiDB 本地部署">

对于本地部署的 TiDB，请在 Python 项目的根目录下新建一个 `.env` 文件，将以下内容复制到 `.env` 文件中，并根据集群的启动参数修改环境变量值为 TiDB 实际对应的值：

```dotenv
TIDB_DATABASE_URL=mysql+pymysql://<USERNAME>:<PASSWORD>@<HOST>:<PORT>/<DATABASE>
# 例如：TIDB_DATABASE_URL="mysql+pymysql://root@127.0.0.1:4000/test"
```

如果你在本机运行 TiDB，`<HOST>` 默认为 `127.0.0.1`。`<PASSWORD>` 初始密码为空，若你是第一次启动集群，则无需带上此字段。

以下为各参数的解释：

- `<USERNAME>`：连接 TiDB 集群的用户名。
- `<PASSWORD>`：连接 TiDB 集群的密码。
- `<HOST>`：TiDB 集群的主机。
- `<PORT>`：TiDB 集群的端口。
- `<DATABASE>`：要连接的数据库名称。

</div>

<div label="TiDB Cloud Serverless">

对于 TiDB Cloud Serverless 集群，请按照以下步骤获取集群的连接字符串，然后配置环境变量：

1. 在 TiDB Cloud 的 [**Clusters**](https://tidbcloud.com/console/clusters) 页面，单击你的 TiDB Cloud Serverless 集群名，进入集群的 **Overview** 页面。

2. 点击右上角的 **Connect** 按钮，将会弹出连接对话框。

3. 确认对话框中的配置和你的运行环境一致。

    - **Connection Type** 为 `Public`。
    - **Branch** 选择 `main`。
    - **Connect With** 选择 `General`。
    - **Operating System** 为你的运行环境。

    > **Tip:**
    >
    > 如果你的程序在 Windows Subsystem for Linux (WSL) 中运行，请切换到相应的 Linux 发行版。

4. 单击 **PyMySQL** 选项卡，复制连接字符串。

    > **Tip:**
    >
    > 如果你还没有设置密码，点击 **Generate Password** 生成一个随机密码。

5. 在 Python 项目的根目录下新建一个 `.env` 文件，并将连接字符串粘贴到其中。

    以下为 macOS 的示例：

    ```dotenv
    TIDB_DATABASE_URL="mysql+pymysql://<prefix>.root:<password>@gateway01.<region>.prod.aws.tidbcloud.com:4000/test?ssl_ca=/etc/ssl/cert.pem&ssl_verify_cert=true&ssl_verify_identity=true"
    ```

</div>
</SimpleTab>

### 第 5 步：运行示例应用程序

```bash
python sqlalchemy-quickstart.py
```

输出示例：

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

你可以参考以下示例代码片段来完成自己的应用程序开发。

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

创建一个表格，其中包含一个向量数据类型的 `embedding` 列，用于存储三维向量。

```python
Base = declarative_base()

class Document(Base):
    __tablename__ = 'sqlalchemy_demo_documents'
    id = Column(Integer, primary_key=True)
    content = Column(Text)
    embedding = Column(VectorType(3))
```

### 存储包含向量的 `document`

```python
with Session(engine) as session:
   session.add(Document(content="dog", embedding=[1, 2, 1]))
   session.add(Document(content="fish", embedding=[1, 2, 4]))
   session.add(Document(content="tree", embedding=[1, 0, 0]))
   session.commit()
```

### 搜索近邻向量

可以选择使用余弦距离 (`CosineDistance`) 函数，查询与向量 `[1, 2, 3]` 语义最接近的前 3 个 `document`。

```python
with Session(engine) as session:
   distance = Document.embedding.cosine_distance([1, 2, 3]).label('distance')
   results = session.query(
      Document, distance
   ).order_by(distance).limit(3).all()
```

### 搜索一定距离内的向量

可以选择使用余弦距离 (`CosineDistance`) 函数，查询与向量 `[1, 2, 3]` 的余弦距离小于 0.2 的向量。

```python
with Session(engine) as session:
    distance = Document.embedding.cosine_distance([1, 2, 3]).label('distance')
    results = session.query(
        Document, distance
    ).filter(distance < 0.2).order_by(distance).limit(3).all()
```

## 另请参阅

- [向量数据类型](/vector-search-data-types.md)
- [向量搜索索引](/vector-search-index.md)