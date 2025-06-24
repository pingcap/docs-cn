---
title: 使用 SQLAlchemy 连接 TiDB
summary: 学习如何使用 SQLAlchemy 连接 TiDB。本教程提供使用 SQLAlchemy 操作 TiDB 的 Python 示例代码片段。
---

# 使用 SQLAlchemy 连接 TiDB

TiDB 是一个兼容 MySQL 的数据库，而 [SQLAlchemy](https://www.sqlalchemy.org/) 是一个流行的 Python SQL 工具包和对象关系映射器（ORM）。

在本教程中，你可以学习如何使用 TiDB 和 SQLAlchemy 完成以下任务：

- 设置你的环境。
- 使用 SQLAlchemy 连接到你的 TiDB 集群。
- 构建并运行你的应用程序。你也可以找到基本 CRUD 操作的示例代码片段。

> **注意：**
>
> 本教程适用于 TiDB Cloud Serverless、TiDB Cloud Dedicated 和 TiDB Self-Managed 集群。

## 前提条件

要完成本教程，你需要：

- [Python 3.8 或更高版本](https://www.python.org/downloads/)。
- [Git](https://git-scm.com/downloads)。
- 一个 TiDB 集群。

<CustomContent platform="tidb">

**如果你还没有 TiDB 集群，可以按照以下方式创建：**

- （推荐）按照[创建 TiDB Cloud Serverless 集群](/develop/dev-guide-build-cluster-in-cloud.md)创建你自己的 TiDB Cloud 集群。
- 按照[部署本地测试 TiDB 集群](/quick-start-with-tidb.md#deploy-a-local-test-cluster)或[部署生产 TiDB 集群](/production-deployment-using-tiup.md)来创建本地集群。

</CustomContent>
<CustomContent platform="tidb-cloud">

**如果你还没有 TiDB 集群，可以按照以下方式创建：**

- （推荐）按照[创建 TiDB Cloud Serverless 集群](/develop/dev-guide-build-cluster-in-cloud.md)创建你自己的 TiDB Cloud 集群。
- 按照[部署本地测试 TiDB 集群](https://docs.pingcap.com/tidb/stable/quick-start-with-tidb#deploy-a-local-test-cluster)或[部署生产 TiDB 集群](https://docs.pingcap.com/tidb/stable/production-deployment-using-tiup)来创建本地集群。

</CustomContent>

## 运行示例程序连接 TiDB

本节演示如何运行示例应用程序代码并连接到 TiDB。

### 第 1 步：克隆示例程序仓库

在终端窗口中运行以下命令来克隆示例代码仓库：

```shell
git clone https://github.com/tidb-samples/tidb-python-sqlalchemy-quickstart.git
cd tidb-python-sqlalchemy-quickstart
```

### 第 2 步：安装依赖

运行以下命令来安装示例程序所需的包（包括 SQLAlchemy 和 PyMySQL）：

```shell
pip install -r requirements.txt
```

#### 为什么使用 PyMySQL？

SQLAlchemy 是一个可以与多个数据库一起工作的 ORM 库。它提供了数据库的高级抽象，帮助开发人员以更面向对象的方式编写 SQL 语句。但是，SQLAlchemy 不包含数据库驱动程序。要连接到数据库，你需要安装一个数据库驱动程序。本示例应用程序使用 PyMySQL 作为数据库驱动程序，它是一个纯 Python MySQL 客户端库，与 TiDB 兼容，并且可以在所有平台上安装。

你也可以使用其他数据库驱动程序，如 [mysqlclient](https://github.com/PyMySQL/mysqlclient) 和 [mysql-connector-python](https://dev.mysql.com/doc/connector-python/en/)。但它们不是纯 Python 库，需要相应的 C/C++ 编译器和 MySQL 客户端来编译。更多信息，请参考 [SQLAlchemy 官方文档](https://docs.sqlalchemy.org/en/20/core/engines.html#mysql)。

### 第 3 步：配置连接信息

根据你选择的 TiDB 部署选项连接到你的 TiDB 集群。

<SimpleTab>
<div label="TiDB Cloud Serverless">

> **注意：**
>
> 目前，TiDB Cloud Serverless 集群有一个限制：如果 5 分钟内没有活动连接，它们将关闭，这会关闭所有连接。因此，在将 SQLAlchemy 与 TiDB Cloud Serverless 集群一起使用时，池化连接可能会遇到 `OperationalError`，如 `Lost connection to MySQL server during query` 或 `MySQL Connection not available`。要避免此错误，你可以将 `pool_recycle` 参数设置为 `300`。更多信息，请参阅 SQLAlchemy 文档中的[处理断开连接](https://docs.sqlalchemy.org/en/20/core/pooling.html#dealing-with-disconnects)。

1. 导航到[**集群**](https://tidbcloud.com/project/clusters)页面，然后点击目标集群的名称进入其概览页面。

2. 点击右上角的**连接**。此时会显示一个连接对话框。

3. 确保连接对话框中的配置与你的操作环境匹配。

    - **连接类型**设置为 `Public`
    - **分支**设置为 `main`
    - **连接方式**设置为 `General`
    - **操作系统**与你的环境匹配。

    > **提示：**
    >
    > 如果你的程序在 Windows Subsystem for Linux (WSL) 中运行，请切换到相应的 Linux 发行版。

4. 点击**生成密码**来创建随机密码。

    > **提示：**
    > 
    > 如果你之前已经创建了密码，你可以使用原始密码，也可以点击**重置密码**生成新密码。

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

2. 点击右上角的**连接**。此时会显示一个连接对话框。

3. 在连接对话框中，从**连接类型**下拉列表中选择 **Public**，然后点击 **CA cert** 下载 CA 证书。

    如果你还没有配置 IP 访问列表，请点击**配置 IP 访问列表**或按照[配置 IP 访问列表](https://docs.pingcap.com/tidbcloud/configure-ip-access-list)中的步骤在首次连接之前进行配置。

    除了 **Public** 连接类型外，TiDB Cloud Dedicated 还支持 **Private Endpoint** 和 **VPC Peering** 连接类型。更多信息，请参阅[连接到你的 TiDB Cloud Dedicated 集群](https://docs.pingcap.com/tidbcloud/connect-to-tidb-cluster)。

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

    请确保将占位符 `{}` 替换为从连接对话框获得的连接参数，并将 `CA_PATH` 配置为上一步下载的证书路径。

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

    请确保将占位符 `{}` 替换为连接参数，并删除 `CA_PATH` 行。如果你在本地运行 TiDB，默认主机地址是 `127.0.0.1`，密码为空。

3. 保存 `.env` 文件。

</div>
</SimpleTab>

### 第 4 步：运行代码并检查结果

1. 执行以下命令运行示例代码：

    ```shell
    python sqlalchemy_example.py
    ```

2. 查看 [Expected-Output.txt](https://github.com/tidb-samples/tidb-python-sqlalchemy-quickstart/blob/main/Expected-Output.txt) 以确认输出是否匹配。

## 示例代码片段

你可以参考以下示例代码片段来完成自己的应用程序开发。

要查看完整的示例代码及其运行方法，请查看 [tidb-samples/tidb-python-sqlalchemy-quickstart](https://github.com/tidb-samples/tidb-python-sqlalchemy-quickstart) 仓库。

### 连接到 TiDB

```python
from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker

def get_db_engine():
    connect_args = {}
    if ${ca_path}:
        connect_args = {
            "ssl_verify_cert": True,
            "ssl_verify_identity": True,
            "ssl_ca": ${ca_path},
        }
    return create_engine(
        URL.create(
            drivername="mysql+pymysql",
            username=${tidb_user},
            password=${tidb_password},
            host=${tidb_host},
            port=${tidb_port},
            database=${tidb_db_name},
        ),
        connect_args=connect_args,
    )

engine = get_db_engine()
Session = sessionmaker(bind=engine)
```

使用此函数时，你需要将 `${tidb_host}`、`${tidb_port}`、`${tidb_user}`、`${tidb_password}`、`${tidb_db_name}` 和 `${ca_path}` 替换为你的 TiDB 集群的实际值。

### 定义表

```python
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Player(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(32), unique=True)
    coins = Column(Integer)
    goods = Column(Integer)

    __tablename__ = "players"
```

更多信息，请参考 [SQLAlchemy 文档：使用声明式映射类](https://docs.sqlalchemy.org/en/20/orm/declarative_mapping.html)。

### 插入数据

```python
with Session() as session:
    player = Player(name="test", coins=100, goods=100)
    session.add(player)
    session.commit()
```

更多信息，请参考[插入数据](/develop/dev-guide-insert-data.md)。

### 查询数据

```python
with Session() as session:
    player = session.query(Player).filter_by(name == "test").one()
    print(player)
```

更多信息，请参考[查询数据](/develop/dev-guide-get-data-from-single-table.md)。

### 更新数据

```python
with Session() as session:
    player = session.query(Player).filter_by(name == "test").one()
    player.coins = 200
    session.commit()
```

更多信息，请参考[更新数据](/develop/dev-guide-update-data.md)。

### 删除数据

```python
with Session() as session:
    player = session.query(Player).filter_by(name == "test").one()
    session.delete(player)
    session.commit()
```

更多信息，请参考[删除数据](/develop/dev-guide-delete-data.md)。

## 下一步

- 从 [SQLAlchemy 的文档](https://www.sqlalchemy.org/)了解更多 SQLAlchemy 的用法。
- 通过[开发者指南](/develop/dev-guide-overview.md)中的章节学习 TiDB 应用程序开发的最佳实践，例如[插入数据](/develop/dev-guide-insert-data.md)、[更新数据](/develop/dev-guide-update-data.md)、[删除数据](/develop/dev-guide-delete-data.md)、[单表读取](/develop/dev-guide-get-data-from-single-table.md)、[事务](/develop/dev-guide-transaction-overview.md)和 [SQL 性能优化](/develop/dev-guide-optimize-sql-overview.md)。
- 通过专业的 [TiDB 开发者课程](https://www.pingcap.com/education/)学习，并在通过考试后获得 [TiDB 认证](https://www.pingcap.com/education/certification/)。

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上询问社区，或[提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上询问社区，或[提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>
