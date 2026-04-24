---
title: 集成 TiDB 向量搜索与 peewee
summary: 学习如何将 TiDB 向量搜索与 peewee 集成，以存储嵌入向量并执行语义搜索。
aliases: ['/zh/tidb/stable/vector-search-integrate-with-peewee/','/zh/tidb/dev/vector-search-integrate-with-peewee/','/zh/tidbcloud/vector-search-integrate-with-peewee/']
---

# 集成 TiDB 向量搜索与 peewee

本教程将指导你如何使用 [peewee](https://docs.peewee-orm.com/) 与 [TiDB 向量搜索](/ai/concepts/vector-search-overview.md) 进行交互，存储嵌入向量，并执行向量搜索查询。

> **注意：**
>
> - 向量搜索功能目前为 beta 版本，可能会在未提前通知的情况下发生变更。如果你发现了 bug，可以在 GitHub 上提交 [issue](https://github.com/pingcap/tidb/issues)。
> - 向量搜索功能适用于 [TiDB 自托管](/overview.md)、[TiDB Cloud Starter](https://docs.pingcap.com/zh/tidbcloud/select-cluster-tier/#starter)、[TiDB Cloud Essential](https://docs.pingcap.com/zh/tidbcloud/select-cluster-tier/#essential) 和 [TiDB Cloud Dedicated](https://docs.pingcap.com/zh/tidbcloud/select-cluster-tier/#tidb-cloud-dedicated)。对于 TiDB 自托管和 TiDB Cloud Dedicated，TiDB 版本需为 v8.4.0 或更高（推荐 v8.5.0 或更高）。

## 前置条件

完成本教程，你需要：

- 已安装 [Python 3.8 或更高版本](https://www.python.org/downloads/)。
- 已安装 [Git](https://git-scm.com/downloads)。
- 一个 TiDB 集群。

**如果你还没有 TiDB 集群，可以按如下方式创建：**

- （推荐）参考 [创建 TiDB Cloud Starter 集群](/develop/dev-guide-build-cluster-in-cloud.md) 创建属于你自己的 TiDB Cloud 集群。
- 参考 [部署本地测试 TiDB 集群](/quick-start-with-tidb.md#deploy-a-local-test-cluster) 或 [部署生产环境 TiDB 集群](/production-deployment-using-tiup.md) 创建本地集群。

## 运行示例应用

你可以按照以下步骤快速学习如何将 TiDB 向量搜索与 peewee 集成。

### 第 1 步：克隆仓库

将 [`tidb-vector-python`](https://github.com/pingcap/tidb-vector-python) 仓库克隆到本地：

```shell
git clone https://github.com/pingcap/tidb-vector-python.git
```

### 第 2 步：创建虚拟环境

为你的项目创建虚拟环境：

```bash
cd tidb-vector-python/examples/orm-peewee-quickstart
python3 -m venv .venv
source .venv/bin/activate
```

### 第 3 步：安装所需依赖

为示例项目安装所需依赖：

```bash
pip install -r requirements.txt
```

或者，你也可以为你的项目单独安装以下包：

```bash
pip install peewee pymysql python-dotenv tidb-vector
```

### 第 4 步：配置环境变量

根据你选择的 TiDB 部署方式配置环境变量。

<SimpleTab>
<div label="TiDB Cloud Starter or Essential">

对于 TiDB Cloud Starter 集群，按如下步骤获取集群连接字符串并配置环境变量：

1. 进入 [**Clusters**](https://tidbcloud.com/console/clusters) 页面，点击目标集群名称进入其概览页面。

2. 点击右上角的 **Connect**，弹出连接对话框。

3. 确保连接对话框中的配置与你的运行环境一致。

    - **Connection Type** 设置为 `Public`。
    - **Branch** 设置为 `main`。
    - **Connect With** 设置为 `General`。
    - **Operating System** 与你的环境一致。

    > **提示：**
    >
    > 如果你的程序运行在 Windows Subsystem for Linux (WSL) 中，请切换到对应的 Linux 发行版。

4. 从连接对话框中复制连接参数。

    > **提示：**
    >
    > 如果你还未设置密码，请点击 **Generate Password** 生成随机密码。

5. 在 Python 项目的根目录下创建 `.env` 文件，并将连接参数粘贴到对应的环境变量中。

    - `TIDB_HOST`：TiDB 集群的主机。
    - `TIDB_PORT`：TiDB 集群的端口。
    - `TIDB_USERNAME`：连接 TiDB 集群的用户名。
    - `TIDB_PASSWORD`：连接 TiDB 集群的密码。
    - `TIDB_DATABASE`：要连接的数据库名称。
    - `TIDB_CA_PATH`：根证书文件的路径。

    以下为 macOS 示例：

    ```dotenv
    TIDB_HOST=gateway01.****.prod.aws.tidbcloud.com
    TIDB_PORT=4000
    TIDB_USERNAME=********.root
    TIDB_PASSWORD=********
    TIDB_DATABASE=test
    TIDB_CA_PATH=/etc/ssl/cert.pem
    ```

</div>
<div label="TiDB 自托管" value="tidb">

对于自托管的 TiDB 集群，在 Python 项目的根目录下创建 `.env` 文件。将以下内容复制到 `.env` 文件中，并根据你的 TiDB 集群连接参数修改环境变量的值：

```dotenv
TIDB_HOST=127.0.0.1
TIDB_PORT=4000
TIDB_USERNAME=root
TIDB_PASSWORD=
TIDB_DATABASE=test
```

如果你在本地运行 TiDB，`TIDB_HOST` 默认为 `127.0.0.1`。初始 `TIDB_PASSWORD` 为空，因此如果是首次启动集群，可以省略该字段。

各参数说明如下：

- `TIDB_HOST`：TiDB 集群的主机。
- `TIDB_PORT`：TiDB 集群的端口。
- `TIDB_USERNAME`：连接 TiDB 集群的用户名。
- `TIDB_PASSWORD`：连接 TiDB 集群的密码。
- `TIDB_DATABASE`：你要连接的数据库名称。

</div>

</SimpleTab>

### 第 5 步：运行示例

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

你可以参考以下示例代码片段开发你的应用。

### 创建向量表

#### 连接 TiDB 集群

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

创建一个包含名为 `peewee_demo_documents` 的表，并存储 3 维向量。

```python
class Document(Model):
    class Meta:
        database = db
        table_name = 'peewee_demo_documents'

    content = TextField()
    embedding = VectorField(3)
```

### 存储带嵌入向量的文档

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

### 搜索距离在指定范围内的文档

搜索与查询向量 `[1, 2, 3]` 的余弦距离小于 0.2 的文档。

```python
distance_expression = Document.embedding.cosine_distance([1, 2, 3])
distance = distance_expression.alias('distance')
results = Document.select(Document, distance).where(distance_expression < 0.2).order_by(distance).limit(3)
```

## 另请参阅

- [向量数据类型](/ai/reference/vector-search-data-types.md)
- [向量搜索索引](/ai/reference/vector-search-index.md)
