---
title: 使用 SQLAlchemy 连接到 TiDB
summary: 了解如何使用 SQLAlchemy 连接到 TiDB。本文提供了使用 SQLAlchemy 与 TiDB 交互的 Python 示例代码片段。
---

# 使用 SQLAlchemy 连接到 TiDB

TiDB 是一个兼容 MySQL 的数据库。[SQLAlchemy](https://www.sqlalchemy.org/) 为当前流行的开源 Python ORM (Object Relational Mapper) 之一。

本文档将展示如何使用 TiDB 和 SQLAlchemy 来完成以下任务：

- 配置你的环境。
- 使用 SQLAlchemy 连接到 TiDB 集群。
- 构建并运行你的应用程序。你也可以参考[示例代码片段](#示例代码片段)，完成基本的 CRUD 操作。

> **注意**
>
> 本文档适用于 TiDB Serverless、TiDB Dedicated 和本地部署的 TiDB。

## 前置需求

- 推荐 [Python 3.8](https://www.python.org/downloads/) 及以上版本。
- [Git](https://git-scm.com/downloads)。
- TiDB 集群。如果你还没有 TiDB 集群，可以按照以下方式创建：
    - （推荐方式）参考[创建 TiDB Serverless 集群](/develop/dev-guide-build-cluster-in-cloud.md#第-1-步创建-tidb-serverless-集群)，创建你自己的 TiDB Cloud 集群。
    - 参考[部署本地测试 TiDB 集群](/quick-start-with-tidb.md#部署本地测试集群)或[部署正式 TiDB 集群](/production-deployment-using-tiup.md)，创建本地集群。

## 运行代码并连接到 TiDB

本小节演示如何运行示例应用程序的代码，并连接到 TiDB。

### 第 1 步：克隆示例代码仓库到本地

运行以下命令，将示例代码仓库克隆到本地：

```bash
git clone https://github.com/tidb-samples/tidb-python-sqlalchemy-quickstart.git
cd tidb-python-sqlalchemy-quickstart
```

### 第 2 步：安装依赖

运行以下命令，安装示例代码所需要的依赖（包括 SQLAlchemy 和 PyMySQL）：

```bash
pip install -r requirements.txt
```

#### 为什么安装 PyMySQL？

SQLAlchemy 是一个支持多种数据库的 ORM 库。它是对数据库的高层抽象，可以帮助开发者以更面向对象的方式编写 SQL 语句。但 SQLAlchemy 并不提供数据库驱动，因此需要单独安装用于连接 TiDB 的驱动。本示例项目使用 PyMySQL 作为数据库驱动。PyMySQL 是一个与 TiDB 兼容的纯 Python 实现的 MySQL 客户端库，并可以在所有平台上安装。

你也可以使用其他数据库驱动，例如 [mysqlclient](https://github.com/PyMySQL/mysqlclient) 以及 [mysql-connector-python](https://dev.mysql.com/doc/connector-python/en/)。但是它们不是纯 Python 库，需要安装对应的 C/C++ 编译器和 MySQL 客户端库进行编译。更多信息，参考 [SQLAlchemy 官方文档](https://docs.sqlalchemy.org/en/20/core/engines.html#mysql)。

### 第 3 步：配置连接信息

根据不同的 TiDB 部署方式，使用不同的方法连接到 TiDB 集群。

<SimpleTab>

<div label="TiDB Serverless">

> **注意：**
>
> TiDB Serverless 集群目前存在一个限制：如果 5 分钟内没有活跃连接，集群将会自动关闭，这会导致所有连接中断。因此，当使用 SQLAlchemy 连接到 TiDB Serverless 集群时，从连接池中获取的连接可能会遇到 `OperationalError` 报错，例如 `Lost connection to MySQL server during query` 或 `MySQL Connection not available`。为了避免该错误，可将 `pool_recycle` 参数设置为 `300`。更多信息，请参阅 SQLAlchemy 文档 [Dealing with Disconnects](https://docs.sqlalchemy.org/en/20/core/pooling.html#dealing-with-disconnects)。

1. 在 TiDB Cloud 的 [**Clusters**](https://tidbcloud.com/console/clusters) 页面中，选择你的 TiDB Serverless 集群，进入集群的 **Overview** 页面。

2. 点击右上角的 **Connect** 按钮，将会弹出连接对话框。

3. 确认对话框中的配置和你的运行环境一致。

    - **Connection Type** 为 `Public`。
    - **Branch** 选择 `main`。
    - **Connect With** 选择 `General`。
    - **Operating System** 为你的运行环境。

    > **Tip:**
    >
    > 如果你在 Windows Subsystem for Linux (WSL) 中运行，请切换为对应的 Linux 发行版。

4. 如果你还没有设置密码，点击 **Generate Password** 生成一个随机密码。

    > **Tip:**
    >
    > 如果你之前已经生成过密码，可以直接使用原密码，或点击 **Reset Password** 重新生成密码。

5. 运行以下命令，将 `.env.example` 复制并重命名为 `.env`：

    ```bash
    cp .env.example .env
    ```

6. 复制并粘贴对应连接字符串至 `.env` 中。示例结果如下：

    ```dotenv
    TIDB_HOST='{host}'  # e.g. gateway01.ap-northeast-1.prod.aws.tidbcloud.com
    TIDB_PORT='4000'
    TIDB_USER='{user}'  # e.g. xxxxxx.root
    TIDB_PASSWORD='{password}'
    TIDB_DB_NAME='test'
    CA_PATH='{ssl_ca}'  # e.g. /etc/ssl/certs/ca-certificates.crt (Debian / Ubuntu / Arch)
    ```

    注意替换 `{}` 中的占位符为连接对话框中获得的值。

7. 保存 `.env` 文件。

</div>

<div label="TiDB Dedicated">

1. 在 TiDB Cloud 的 [**Clusters**](https://tidbcloud.com/console/clusters) 页面中，选择你的 TiDB Dedicated 集群，进入集群的 **Overview** 页面。

2. 点击右上角的 **Connect** 按钮，将会出现连接对话框。

3. 在连接对话框中，从 **Connection Type** 下拉列表中选择 **Public**，并点击 **CA cert** 下载 CA 文件。

    如果你尚未配置 IP 访问列表，请在首次连接前点击 **Configure IP Access List** 或按照[配置 IP 访问列表（英文）](https://docs.pingcap.com/tidbcloud/configure-ip-access-list)中的步骤进行配置。

    除 **Public** 连接类型外，TiDB Dedicated 还支持 **Private Endpoint** 和 **VPC Peering** 连接类型。详情请参阅[连接 TiDB Dedicated 集群（英文）](https://docs.pingcap.com/tidbcloud/connect-to-tidb-cluster)。

4. 运行以下命令，将 `.env.example` 复制并重命名为 `.env`：

    ```bash
    cp .env.example .env
    ```

5. 复制并粘贴对应的连接字符串至 `.env` 中。示例结果如下：

    ```dotenv
    TIDB_HOST='{host}'  # e.g. tidb.xxxx.clusters.tidb-cloud.com
    TIDB_PORT='4000'
    TIDB_USER='{user}'  # e.g. root
    TIDB_PASSWORD='{password}'
    TIDB_DB_NAME='test'
    CA_PATH='{your-downloaded-ca-path}'
    ```

    注意替换 `{}` 中的占位符为连接对话框中获得的值，并配置前面步骤中下载好的证书路径。

6. 保存 `.env` 文件。

</div>

<div label="本地部署 TiDB">

1. 运行以下命令，将 `.env.example` 复制并重命名为 `.env`：

    ```bash
    cp .env.example .env
    ```

2. 复制并粘贴对应 TiDB 的连接字符串至 `.env` 中。示例结果如下：

    ```dotenv
    TIDB_HOST='{host}'
    TIDB_PORT='4000'
    TIDB_USER='root'
    TIDB_PASSWORD='{password}'
    TIDB_DB_NAME='test'
    ```

    注意替换 `{}` 中的占位符为你的 TiDB 对应的值，并删除 `CA_PATH` 这行。如果你在本机运行 TiDB，默认 Host 地址为 `127.0.0.1`，密码为空。

3. 保存 `.env` 文件。

</div>

</SimpleTab>

### 第 4 步：运行代码并查看结果

1. 运行下述命令，执行示例代码：

    ```bash
    python sqlalchemy_example.py
    ```

2. 查看 [`Expected-Output.txt`](https://github.com/tidb-samples/tidb-python-sqlalchemy-quickstart/blob/main/Expected-Output.txt)，并与你的程序输出进行比较。结果近似即为连接成功。

## 示例代码片段

你可参考以下关键代码片段，完成自己的应用开发。

完整代码及其运行方式，见代码仓库 [tidb-samples/tidb-python-sqlalchemy-quickstart](https://github.com/tidb-samples/tidb-python-sqlalchemy-quickstart)。

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

在使用该函数时，你需要将 `${tidb_host}`、`${tidb_port}`、`${tidb_user}`、`${tidb_password}`、`${tidb_db_name}` 以及 `${ca_path}` 替换为你的 TiDB 集群的实际值。

### 声明数据对象

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

更多信息参考 [SQLAlchemy 声明式映射表](https://docs.sqlalchemy.org/en/20/orm/declarative_mapping.html)。

### 插入数据

```python
with Session() as session:
    player = Player(name="test", coins=100, goods=100)
    session.add(player)
    session.commit()
```

更多信息参考[插入数据](/develop/dev-guide-insert-data.md)以及 [SQLAlchemy Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html)。

### 查询数据

```python
with Session() as session:
    player = session.query(Player).filter_by(name == "test").one()
    print(player)
```

更多信息参考[查询数据](/develop/dev-guide-get-data-from-single-table.md)以及 [SQLAlchemy Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html)。

### 更新数据

```python
with Session() as session:
    player = session.query(Player).filter_by(name == "test").one()
    player.coins = 200
    session.commit()
```

更多信息参考[更新数据](/develop/dev-guide-update-data.md)以及 [SQLAlchemy Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html)。

### 删除数据

```python
with Session() as session:
    player = session.query(Player).filter_by(name == "test").one()
    session.delete(player)
    session.commit()
```

更多信息参考[删除数据](/develop/dev-guide-delete-data.md)以及 [SQLAlchemy Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html)。

## 下一步

- 关于 SQLAlchemy 的更多使用方法，可以参考 [SQLAlchemy 官方文档](https://www.sqlalchemy.org/)。
- 你可以继续阅读开发者文档，以获取更多关于 TiDB 应用开发的最佳实践。例如：[插入数据](/develop/dev-guide-insert-data.md)、[更新数据](/develop/dev-guide-update-data.md)、[删除数据](/develop/dev-guide-delete-data.md)、[单表读取](/develop/dev-guide-get-data-from-single-table.md)、[事务](/develop/dev-guide-transaction-overview.md)、[SQL 性能优化](/develop/dev-guide-optimize-sql-overview.md)等。
- 如果你更倾向于参与课程进行学习，我们也提供专业的 [TiDB 开发者课程](https://cn.pingcap.com/courses-catalog/category/back-end-developer/?utm_source=docs-cn-dev-guide)支持，并在考试后提供相应的[资格认证](https://learn.pingcap.com/learner/certification-center)。

## 需要帮助?

如果在开发的过程中遇到问题，可以在 [AskTUG](https://asktug.com/?utm_source=docs-cn-dev-guide) 上进行提问，寻求帮助。
