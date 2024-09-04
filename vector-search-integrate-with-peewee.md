---
title: TiDB 向量搜索在 peewee 中的使用
summary: 了解如何在 peewee 中 TiDB 使用向量搜索，，以存储向量并执行语义搜索。
---

# TiDB 向量搜索在 peewee 中的使用

本文档将展示如何使用 [peewee](https://docs.peewee-orm.com/) 与 TiDB 向量搜索进行交互、存储向量和执行向量搜索查询。

## 准备
在开始之前，你需要确定 TiDB 集群的部署方式以及以下内容被正确安装，
- TiDB Serverless 集群
  - [Python 3.8 or higher](https://www.python.org/downloads/)
  - [Git](https://git-scm.com/downloads) 
  - TiDB Serverless集群。如果没有 TiDB Cloud 集群，请按照[创建 TiDB Serverless集群](https://dev.mysql.com/doc/refman/8.4/en/mysql.html)创建自己的 TiDB Cloud 集群。

- 本地部署的 TiDB 集群
  - [Python 3.8 or higher](https://www.python.org/downloads/)
  - [Git](https://git-scm.com/downloads) 
  - TiDB 集群。如果没有集群，请按照[使用 TiUP 部署 TiDB 集群](/production-deployment-using-tiup.md)创建自己的 TiDB 集群。

## 运行示例应用程序

你可以通过以下步骤快速了解如何在 peewee 中使用 TiDB 向量搜索。

### Step 1. 克隆仓库

将 [`tidb-vector-python`](https://github.com/pingcap/tidb-vector-python) 仓库克隆到本地计算机：

```shell
git clone https://github.com/pingcap/tidb-vector-python.git
```

### 步骤 2. 创建虚拟环境

为项目创建虚拟环境：

```bash
cd tidb-vector-python/examples/orm-peewee-quickstart
python3 -m venv .venv
source .venv/bin/activate
```

### 步骤 3. 安装所需的依赖项

安装项目所需的依赖项：

```bash
pip install -r requirements.txt
```

你也可以直接为项目安装以下依赖项：

```bash
pip install peewee pymysql python-dotenv tidb-vector
```

### 步骤 4. 配置环境变量

1. 根据 TiDB 集群的部署方式不同，选择对应的环境变量配置方式。

    <SimpleTab>

    <div label="TiDB Serverless 集群部署">

    1. 在 [**Cluster**](https://tidbcloud.com/console/clusters) 页面，单击目标群集的名称进入其概览页面。

    2. 单击右上角的**Connect**。此时将显示连接对话框。

    3. 确保连接对话框中的配置符合你的运行环境。

    - **Endpoint Type** 设置为 `Public`
    - **Branch** 设置为 `main`
    - **Connect With** 设置为 `General`
    - **Operating System** 与你的机器环境相匹配

    > **Tip:**
    >
    > 如果程序在 Windows Subsystem for Linux (WSL) 中运行，请切换到相应的 Linux 发行版。

    4. 从连接对话框中复制连接参数。

    > **Tip:**
    >
    > 如果尚未设置密码，单击**生成密码**生成一个随机密码。

    5. 在 Python 项目的根目录下创建一个 `.env` 文件，并将连接参数粘贴到相应的环境变量中。

    - `TIDB_HOST`: TiDB 集群的主机号。
    - `TIDB_PORT`: TiDB 集群的端口号。
    - `TIDB_USERNAME`: 连接 TiDB 集群的用户名。
    - `TIDB_PASSWORD`: 连接 TiDB 集群的密码。
    - `TIDB_DATABASE`: 要连接的数据库名称。
    - `TIDB_CA_PATH`: 根证书文件的路径。

    以下是 MacOS 的示例：

    ```dotenv
    TIDB_HOST=gateway01.****.prod.aws.tidbcloud.com
    TIDB_PORT=4000
    TIDB_USERNAME=********.root
    TIDB_PASSWORD=********
    TIDB_DATABASE=test
    TIDB_CA_PATH=/etc/ssl/cert.pem
    ```

    </div>

    <div label="TiDB Self-hosted 集群部署">

    在 Python 项目的根目录下创建一个 `.env` 文件，并根据启动的集群参数修改相应的环境变量中。

    - `TIDB_HOST`: TiDB 集群的主机号。
    - `TIDB_PORT`: TiDB 集群的端口号。
    - `TIDB_USERNAME`: 连接 TiDB 集群的用户名。
    - `TIDB_PASSWORD`: 连接 TiDB 集群的密码。
    - `TIDB_DATABASE`: 要连接的数据库名称。
    - `TIDB_CA_PATH`: 根证书文件的路径。

    以下是 MacOS 的示例：

    ```dotenv
    TIDB_HOST=127.0.0.1
    TIDB_PORT=4000
    TIDB_USERNAME=********.root
    TIDB_PASSWORD=********
    TIDB_DATABASE=test
    TIDB_CA_PATH=/etc/ssl/cert.pem
    ```

    </div>

    </SimpleTab>

### 步骤 5. 运行 demo

```bash
python peewee-quickstart.py
```

输出示例

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

from peewee import Model, MySQLDatabase, SQL, TextField
from tidb_vector.peewee import VectorField

dotenv.load_dotenv()

# Using `pymysql` as the driver.
connect_kwargs = {
    'ssl_verify_cert': True,
    'ssl_verify_identity': True,
}

# Using `mysqlclient` as the driver.
# connect_kwargs = {
#     'ssl_mode': 'VERIFY_IDENTITY',
#     'ssl': {
#         # Root certificate default path
#         # https://docs.pingcap.com/tidbcloud/secure-connections-to-serverless-clusters/#root-certificate-default-path
#         'ca': os.environ.get('TIDB_CA_PATH', '/path/to/ca.pem'),
#     },
# }

db = MySQLDatabase(
    database=os.environ.get('TIDB_DATABASE', 'test'),
    user=os.environ.get('TIDB_USERNAME', 'root'),
    password=os.environ.get('TIDB_PASSWORD', ''),
    host=os.environ.get('TIDB_HOST', 'localhost'),
    port=int(os.environ.get('TIDB_PORT', '4000')),
    **connect_kwargs,
)
```

#### 定义向量列

创建一个表格，其中有一列向量类型的 `embedding` ，用于存储三维向量。

```python
class Document(Model):
    class Meta:
        database = db
        table_name = 'peewee_demo_documents'

    content = TextField()
    embedding = VectorField(3)
```

### 存储带有向量的文档

```python
Document.create(content='dog', embedding=[1, 2, 1])
Document.create(content='fish', embedding=[1, 2, 4])
Document.create(content='tree', embedding=[1, 0, 0])
```

### 搜索近邻向量

我们可以选择使用余弦距离 (`CosineDistance`) 函数，查询与向量 `[1, 2, 3]` 语义最接近的前 3 个内容。

```python
distance = Document.embedding.cosine_distance([1, 2, 3]).alias('distance')
results = Document.select(Document, distance).order_by(distance).limit(3)
```

### 搜索一定距离内的向量

我们可以选择使用余弦距离 (`CosineDistance`) 函数，查询与向量 `[1, 2, 3]` 的余弦距离小于 0.2 的向量。

```python
distance_expression = Document.embedding.cosine_distance([1, 2, 3])
distance = distance_expression.alias('distance')
results = Document.select(Document, distance).where(distance_expression < 0.2).order_by(distance).limit(3)
```

## 另请参阅

- [向量数据类型](/vector-search-data-types.md)