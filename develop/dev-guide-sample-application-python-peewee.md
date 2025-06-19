---
title: 使用 peewee 连接 TiDB
summary: 了解如何使用 peewee 连接 TiDB。本教程提供使用 peewee 操作 TiDB 的 Python 示例代码片段。
---

# 使用 peewee 连接 TiDB

TiDB 是一个兼容 MySQL 的数据库，而 [peewee](https://docs.peewee-orm.com/) 是一个流行的 Python 对象关系映射器（ORM）。

在本教程中，您可以学习如何使用 TiDB 和 peewee 完成以下任务：

- 设置环境。
- 使用 peewee 连接到 TiDB 集群。
- 构建并运行应用程序。您也可以查看基本 CRUD 操作的示例代码片段。

> **注意：**
>
> 本教程适用于 TiDB Cloud Serverless、TiDB Cloud Dedicated 和 TiDB Self-Managed 集群。

## 前提条件

要完成本教程，您需要：

- [Python 3.8 或更高版本](https://www.python.org/downloads/)。
- [Git](https://git-scm.com/downloads)。
- 一个 TiDB 集群。

<CustomContent platform="tidb">

**如果您还没有 TiDB 集群，可以按照以下方式创建：**

- （推荐）按照[创建 TiDB Cloud Serverless 集群](/develop/dev-guide-build-cluster-in-cloud.md)创建您自己的 TiDB Cloud 集群。
- 按照[部署本地测试 TiDB 集群](/quick-start-with-tidb.md#deploy-a-local-test-cluster)或[部署生产 TiDB 集群](/production-deployment-using-tiup.md)创建本地集群。

</CustomContent>
<CustomContent platform="tidb-cloud">

**如果您还没有 TiDB 集群，可以按照以下方式创建：**

- （推荐）按照[创建 TiDB Cloud Serverless 集群](/develop/dev-guide-build-cluster-in-cloud.md)创建您自己的 TiDB Cloud 集群。
- 按照[部署本地测试 TiDB 集群](https://docs.pingcap.com/tidb/stable/quick-start-with-tidb#deploy-a-local-test-cluster)或[部署生产 TiDB 集群](https://docs.pingcap.com/tidb/stable/production-deployment-using-tiup)创建本地集群。

</CustomContent>

## 运行示例应用程序连接到 TiDB

本节演示如何运行示例应用程序代码并连接到 TiDB。

### 步骤 1：克隆示例应用程序仓库

在终端窗口中运行以下命令来克隆示例代码仓库：

```shell
git clone https://github.com/tidb-samples/tidb-python-peewee-quickstart.git
cd tidb-python-peewee-quickstart
```

### 步骤 2：安装依赖

运行以下命令安装示例应用程序所需的包（包括 peewee 和 PyMySQL）：

```shell
pip install -r requirements.txt
```

#### 为什么使用 PyMySQL？

peewee 是一个可以与多个数据库一起工作的 ORM 库。它提供了数据库的高级抽象，帮助开发人员以更面向对象的方式编写 SQL 语句。但是，peewee 不包含数据库驱动程序。要连接到数据库，您需要安装数据库驱动程序。本示例应用程序使用 PyMySQL 作为数据库驱动程序，它是一个纯 Python MySQL 客户端库，与 TiDB 兼容，并且可以在所有平台上安装。更多信息，请参考 [peewee 官方文档](https://docs.peewee-orm.com/en/latest/peewee/database.html?highlight=mysql#using-mysql)。

### 步骤 3：配置连接信息

根据您选择的 TiDB 部署选项连接到您的 TiDB 集群。

<SimpleTab>
<div label="TiDB Cloud Serverless">

1. 导航到[**集群**](https://tidbcloud.com/project/clusters)页面，然后点击目标集群的名称进入其概览页面。

2. 点击右上角的**连接**。将显示连接对话框。

3. 确保连接对话框中的配置与您的操作环境匹配。

    - **连接类型**设置为 `Public`
    - **分支**设置为 `main`
    - **连接工具**设置为 `General`
    - **操作系统**与您的环境匹配。

    > **提示：**
    >
    > 如果您的程序在 Windows Subsystem for Linux (WSL) 中运行，请切换到相应的 Linux 发行版。

4. 点击**生成密码**创建随机密码。

    > **提示：**
    > 
    > 如果您之前已经创建了密码，您可以使用原始密码或点击**重置密码**生成新密码。

5. 运行以下命令复制 `.env.example` 并将其重命名为 `.env`：

    ```shell
    cp .env.example .env
    ```

6. 将相应的连接字符串复制并粘贴到 `.env` 文件中。示例结果如下：

    ```dotenv
    TIDB_HOST='{host}'  # 例如 gateway01.ap-northeast-1.prod.aws.tidbcloud.com
    TIDB_PORT='4000'
    TIDB_USER='{user}'  # 例如 xxxxxx.root
    TIDB_PASSWORD='{password}'
    TIDB_DB_NAME='test'
    CA_PATH='{ssl_ca}'  # 例如 /etc/ssl/certs/ca-certificates.crt (Debian / Ubuntu / Arch)
    ```

    请确保将占位符 `{}` 替换为从连接对话框获得的连接参数。

7. 保存 `.env` 文件。

</div>
<div label="TiDB Cloud Dedicated">

1. 导航到[**集群**](https://tidbcloud.com/project/clusters)页面，然后点击目标集群的名称进入其概览页面。

2. 点击右上角的**连接**。将显示连接对话框。

3. 在连接对话框中，从**连接类型**下拉列表中选择**公共**，然后点击 **CA 证书**下载 CA 证书。

    如果您尚未配置 IP 访问列表，请在首次连接之前点击**配置 IP 访问列表**或按照[配置 IP 访问列表](https://docs.pingcap.com/tidbcloud/configure-ip-access-list)中的步骤进行配置。

    除了**公共**连接类型外，TiDB Cloud Dedicated 还支持**私有端点**和 **VPC 对等连接**类型。更多信息，请参见[连接到您的 TiDB Cloud Dedicated 集群](https://docs.pingcap.com/tidbcloud/connect-to-tidb-cluster)。

4. 运行以下命令复制 `.env.example` 并将其重命名为 `.env`：

    ```shell
    cp .env.example .env
    ```

5. 将相应的连接字符串复制并粘贴到 `.env` 文件中。示例结果如下：

    ```dotenv
    TIDB_HOST='{host}'  # 例如 tidb.xxxx.clusters.tidb-cloud.com
    TIDB_PORT='4000'
    TIDB_USER='{user}'  # 例如 root
    TIDB_PASSWORD='{password}'
    TIDB_DB_NAME='test'
    CA_PATH='{your-downloaded-ca-path}'
    ```

    请确保将占位符 `{}` 替换为从连接对话框获得的连接参数，并将 `CA_PATH` 配置为之前下载的证书路径。

6. 保存 `.env` 文件。

</div>
<div label="TiDB Self-Managed">

1. 运行以下命令复制 `.env.example` 并将其重命名为 `.env`：

    ```shell
    cp .env.example .env
    ```

2. 将相应的连接字符串复制并粘贴到 `.env` 文件中。示例结果如下：

    ```dotenv
    TIDB_HOST='{tidb_server_host}'
    TIDB_PORT='4000'
    TIDB_USER='root'
    TIDB_PASSWORD='{password}'
    TIDB_DB_NAME='test'
    ```

    请确保将占位符 `{}` 替换为连接参数，并删除 `CA_PATH` 行。如果您在本地运行 TiDB，默认主机地址为 `127.0.0.1`，密码为空。

3. 保存 `.env` 文件。

</div>
</SimpleTab>

### 步骤 4：运行代码并检查结果

1. 执行以下命令运行示例代码：

    ```shell
    python peewee_example.py
    ```

2. 查看 [Expected-Output.txt](https://github.com/tidb-samples/tidb-python-peewee-quickstart/blob/main/Expected-Output.txt) 以检查输出是否匹配。

## 示例代码片段

您可以参考以下示例代码片段来完成自己的应用程序开发。

有关完整的示例代码和如何运行它，请查看 [tidb-samples/tidb-python-peewee-quickstart](https://github.com/tidb-samples/tidb-python-peewee-quickstart) 仓库。

### 连接到 TiDB

```python
from peewee import MySQLDatabase

def get_db_engine():
    config = Config()
    connect_params = {}
    if ${ca_path}:
        connect_params = {
            "ssl_verify_cert": True,
            "ssl_verify_identity": True,
            "ssl_ca": ${ca_path},
        }
    return MySQLDatabase(
        ${tidb_db_name},
        host=${tidb_host},
        port=${tidb_port},
        user=${tidb_user},
        password=${tidb_password},
        **connect_params,
    )
```

使用此函数时，您需要将 `${tidb_host}`、`${tidb_port}`、`${tidb_user}`、`${tidb_password}`、`${tidb_db_name}` 和 `${ca_path}` 替换为您的 TiDB 集群的实际值。

### 定义表

```python
from peewee import Model, CharField, IntegerField

db = get_db_engine()

class BaseModel(Model):
    class Meta:
        database = db

class Player(BaseModel):
    name = CharField(max_length=32, unique=True)
    coins = IntegerField(default=0)
    goods = IntegerField(default=0)

    class Meta:
        table_name = "players"
```

更多信息，请参见 [peewee 文档：模型和字段](https://docs.peewee-orm.com/en/latest/peewee/models.html)。

### 插入数据

```python
# 插入单条记录
Player.create(name="test", coins=100, goods=100)

# 插入多条记录
Player.insert_many(
    [
        {"name": "test1", "coins": 100, "goods": 100},
        {"name": "test2", "coins": 100, "goods": 100},
    ]
).execute()
```

更多信息，请参见[插入数据](/develop/dev-guide-insert-data.md)。

### 查询数据

```python
# 查询所有记录
players = Player.select()

# 查询单条记录
player = Player.get(Player.name == "test")

# 查询多条记录
players = Player.select().where(Player.coins == 100)
```

更多信息，请参见[查询数据](/develop/dev-guide-get-data-from-single-table.md)。

### 更新数据

```python
# 更新单条记录
player = Player.get(Player.name == "test")
player.coins = 200
player.save()

# 更新多条记录
Player.update(coins=200).where(Player.coins == 100).execute()
```

更多信息，请参见[更新数据](/develop/dev-guide-update-data.md)。

### 删除数据

```python
# 删除单条记录
player = Player.get(Player.name == "test")
player.delete_instance()

# 删除多条记录
Player.delete().where(Player.coins == 100).execute()
```

更多信息，请参见[删除数据](/develop/dev-guide-delete-data.md)。

## 下一步

- 从 [peewee 文档](https://docs.peewee-orm.com/)了解更多 peewee 的用法。
- 通过[开发者指南](/develop/dev-guide-overview.md)中的章节学习 TiDB 应用程序开发的最佳实践，如[插入数据](/develop/dev-guide-insert-data.md)、[更新数据](/develop/dev-guide-update-data.md)、[删除数据](/develop/dev-guide-delete-data.md)、[单表读取](/develop/dev-guide-get-data-from-single-table.md)、[事务](/develop/dev-guide-transaction-overview.md)和 [SQL 性能优化](/develop/dev-guide-optimize-sql-overview.md)。
- 学习专业的 [TiDB 开发者课程](https://www.pingcap.com/education/)，通过考试后获得 [TiDB 认证](https://www.pingcap.com/education/certification/)。

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上询问社区，或[提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上询问社区，或[提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>
