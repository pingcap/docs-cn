---
title: TiDB 向量搜索与 peewee 相结合
summary: 了解如何将 TiDB 向量搜索与 peewee 集成，以存储嵌入信息并执行语义搜索。
---

# TiDB 向量搜索与 peewee 结合

本教程将展示如何使用 [peewee](https://docs.peewee-orm.com/)与TiDB向量搜索交互、存储嵌入和执行向量搜索查询。

## 准备

要实现本部分的内容，需要确保安装以下内容：

- [Python 3.8 or higher](https://www.python.org/downloads/) installed.
- [Git](https://git-scm.com/downloads) installed.
- TiDB serverless集群。如果没有，请按照[使用 TiDB Serverless 构建 TiDB 集群](/develop/dev-guide-build-cluster-in-cloud.md)创建自己的 TiDB 集群。

## 运行示例应用程序

通过以下步骤，您可以快速了解如何将 TiDB 向量搜索与 peewee 结合。

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

您可以为现有项目安装以下软件包：

```bash
pip install peewee pymysql python-dotenv tidb-vector
```

### 步骤 4. 配置环境变量

1. 导航至 [** 群集**](https://tidbcloud.com/console/clusters) 页面，然后单击目标群集的名称进入其概览页面。

2. 单击右上角的**连接**。此时将显示连接对话框。

3. 确保连接对话框中的配置符合您的运行环境。

    - **Endpoint Type** 设置为 `Public`.
    - **Branch** 设置为 `main`.
    - **Connect With** 设置为 `General`.
    - **Operating System** 与环境相匹配.

    > **Tip:**
    >
    > 如果程序在 Windows Subsystem for Linux (WSL) 中运行，请切换到相应的 Linux 发行版。

4. 从连接对话框中复制连接参数。

    > **Tip:**
    >
    > 如果尚未设置密码，请单击**生成密码**生成一个随机密码。

5. In the root directory of your Python project, create a `.env` file and paste the connection parameters to the corresponding environment variables.

    - `TIDB_HOST`: TiDB 集群的主机。
    - `TIDB_PORT`: TiDB 集群的端口。
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

### 步骤 5. 运行demo

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

您可以参考以下示例代码片段来开发您的应用程序。

### 创建矢量表

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

创建一个表格，其中有一列名为 “peewee_demo_documents”，用于存储一个三维向量。

```python
class Document(Model):
    class Meta:
        database = db
        table_name = 'peewee_demo_documents'

    content = TextField()
    embedding = VectorField(3)
```

#### 用索引定义优化的矢量列

定义三维矢量列，并使用[向量搜索索引](/vector-search-index.md) （HNSW 索引）对其进行优化。

```python
class DocumentWithIndex(Model):
    class Meta:
        database = db
        table_name = 'peewee_demo_documents_with_index'

    content = TextField()
    embedding = VectorField(3, constraints=[SQL("COMMENT 'hnsw(distance=cosine)'")])
```

TiDB 将使用该索引来加速基于余弦距离函数的矢量搜索查询。

### 存储向量

```python
Document.create(content='dog', embedding=[1, 2, 1])
Document.create(content='fish', embedding=[1, 2, 4])
Document.create(content='tree', embedding=[1, 0, 0])
```

### 搜索近邻向量

根据余弦距离函数，搜索与查询向量“[1, 2, 3]”语义最接近的前 3 个向量。

```python
distance = Document.embedding.cosine_distance([1, 2, 3]).alias('distance')
results = Document.select(Document, distance).order_by(distance).limit(3)
```

### 搜索一定距离内的向量

搜索与查询向量`“`[1, 2, 3]`的余弦距离小于 0.2 的文档。

```python
distance_expression = Document.embedding.cosine_distance([1, 2, 3])
distance = distance_expression.alias('distance')
results = Document.select(Document, distance).where(distance_expression < 0.2).order_by(distance).limit(3)
```

## See also

- [向量数据类型](/vector-search-data-types.md)
- [向量搜索索引](/vector-search-index.md)