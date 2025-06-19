---
title: 将 TiDB Vector Search 与 peewee 集成
summary: 了解如何将 TiDB Vector Search 与 peewee 集成以存储嵌入向量并执行语义搜索。
---

# 将 TiDB Vector Search 与 peewee 集成

本教程将指导你如何使用 [peewee](https://docs.peewee-orm.com/) 与 [TiDB Vector Search](/tidb-cloud/vector-search-overview.md) 交互，存储嵌入向量并执行向量搜索查询。

> **注意**
>
> TiDB Vector Search 仅适用于 TiDB Self-Managed（TiDB >= v8.4）和 [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)。它不适用于 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)。

## 前提条件

完成本教程需要：

- 安装 [Python 3.8 或更高版本](https://www.python.org/downloads/)。
- 安装 [Git](https://git-scm.com/downloads)。
- 一个 TiDB Cloud Serverless 集群。如果你还没有，请参考[创建 TiDB Cloud Serverless 集群](/tidb-cloud/create-tidb-cluster-serverless.md)来创建你自己的 TiDB Cloud 集群。

## 运行示例应用

你可以按照以下步骤快速了解如何将 TiDB Vector Search 与 peewee 集成。

### 步骤 1. 克隆代码仓库

将 [`tidb-vector-python`](https://github.com/pingcap/tidb-vector-python) 代码仓库克隆到本地：

```shell
git clone https://github.com/pingcap/tidb-vector-python.git
```

### 步骤 2. 创建虚拟环境

为你的项目创建一个虚拟环境：

```bash
cd tidb-vector-python/examples/orm-peewee-quickstart
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
pip install peewee pymysql python-dotenv tidb-vector
```

### 步骤 4. 配置环境变量

1. 导航到 [**Clusters**](https://tidbcloud.com/project/clusters) 页面，然后点击目标集群的名称进入其概览页面。

2. 点击右上角的 **Connect**。将显示连接对话框。

3. 确保连接对话框中的配置与你的操作环境匹配。

   - **Connection Type** 设置为 `Public`。
   - **Branch** 设置为 `main`。
   - **Connect With** 设置为 `General`。
   - **Operating System** 与你的环境匹配。

   > **提示：**
   >
   > 如果你的程序在 Windows Subsystem for Linux (WSL) 中运行，请切换到相应的 Linux 发行版。

4. 从连接对话框中复制连接参数。

   > **提示：**
   >
   > 如果你还没有设置密码，请点击 **Generate Password** 生成一个随机密码。

5. 在 Python 项目的根目录下创建一个 `.env` 文件，并将连接参数粘贴到相应的环境变量中。

   - `TIDB_HOST`：TiDB 集群的主机地址。
   - `TIDB_PORT`：TiDB 集群的端口。
   - `TIDB_USERNAME`：连接 TiDB 集群的用户名。
   - `TIDB_PASSWORD`：连接 TiDB 集群的密码。
   - `TIDB_DATABASE`：要连接的数据库名称。
   - `TIDB_CA_PATH`：根证书文件的路径。

   以下是 macOS 的示例：

   ```dotenv
   TIDB_HOST=gateway01.****.prod.aws.tidbcloud.com
   TIDB_PORT=4000
   TIDB_USERNAME=********.root
   TIDB_PASSWORD=********
   TIDB_DATABASE=test
   TIDB_CA_PATH=/etc/ssl/cert.pem
   ```

### 步骤 5. 运行示例

```bash
python peewee-quickstart.py
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

from peewee import Model, MySQLDatabase, SQL, TextField
from tidb_vector.peewee import VectorField

dotenv.load_dotenv()

# 使用 `pymysql` 作为驱动
connect_kwargs = {
    'ssl_verify_cert': True,
    'ssl_verify_identity': True,
}

# 使用 `mysqlclient` 作为驱动
# connect_kwargs = {
#     'ssl_mode': 'VERIFY_IDENTITY',
#     'ssl': {
#         # 根证书默认路径
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

创建一个名为 `peewee_demo_documents` 的表，其中包含一个存储 3 维向量的列。

```python
class Document(Model):
    class Meta:
        database = db
        table_name = 'peewee_demo_documents'

    content = TextField()
    embedding = VectorField(3)
```

### 存储带有嵌入向量的文档

```python
Document.create(content='dog', embedding=[1, 2, 1])
Document.create(content='fish', embedding=[1, 2, 4])
Document.create(content='tree', embedding=[1, 0, 0])
```

### 搜索最近邻文档

基于余弦距离函数，搜索与查询向量 `[1, 2, 3]` 语义最接近的前 3 个文档。

```python
distance = Document.embedding.cosine_distance([1, 2, 3]).alias('distance')
results = Document.select(Document, distance).order_by(distance).limit(3)
```

### 搜索特定距离内的文档

搜索与查询向量 `[1, 2, 3]` 的余弦距离小于 0.2 的文档。

```python
distance_expression = Document.embedding.cosine_distance([1, 2, 3])
distance = distance_expression.alias('distance')
results = Document.select(Document, distance).where(distance_expression < 0.2).order_by(distance).limit(3)
```

## 另请参阅

- [向量数据类型](/tidb-cloud/vector-search-data-types.md)
- [向量搜索索引](/tidb-cloud/vector-search-index.md)
