---
title: 使用 MySQL Connector/Python 连接到 TiDB
summary: 了解如何使用 MySQL Connector/Python 连接到 TiDB。本文提供了使用 MySQL Connector/Python 与 TiDB 交互的 Python 示例代码片段。
---

# 使用 MySQL Connector/Python 连接到 TiDB

TiDB 是一个兼容 MySQL 的数据库。[MySQL Connector/Python](https://dev.mysql.com/doc/connector-python/en/) 是由 MySQL 开发的 Python Driver。

本文档将展示如何使用 TiDB 和 MySQL Connector/Python 来完成以下任务：

- 配置你的环境。
- 使用 MySQL Connector/Python 连接到 TiDB 集群。
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
git clone https://github.com/tidb-samples/tidb-python-mysqlconnector-quickstart.git
cd tidb-python-mysqlconnector-quickstart
```

### 第 2 步：安装依赖

运行以下命令，安装示例代码所需要的依赖（包括 mysql-connector-python）：

```bash
pip install -r requirements.txt
```

### 第 3 步：配置连接信息

根据不同的 TiDB 部署方式，使用不同的方法连接到 TiDB 集群。

<SimpleTab>

<div label="TiDB Serverless">

1. 在 TiDB Cloud 的 [**Clusters**](https://tidbcloud.com/console/clusters) 页面中，选择你的 TiDB Serverless 集群，进入集群的 **Overview** 页面。

2. 点击右上角的 **Connect** 按钮，将会弹出连接对话框。

3. 确认对话框中的配置和你的运行环境一致。

    - **Endpoint Type** 为 `Public`。
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
    TIDB_HOST='{host}'  # e.g. xxxxxx.aws.tidbcloud.com
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

3. 在对话框中点击 **Allow Access from Anywhere**，然后点击 **Download CA cert** 下载 TiDB Cloud 提供的 CA 证书。

    更多配置细节，可参考 [TiDB Dedicated 标准连接教程（英文）](https://docs.pingcap.com/tidbcloud/connect-via-standard-connection)。

4. 运行以下命令，将 `.env.example` 复制并重命名为 `.env`：

    ```bash
    cp .env.example .env
    ```

5. 复制并粘贴对应的连接字符串至 `.env` 中。示例结果如下：

    ```dotenv
    TIDB_HOST='{host}'  # e.g. xxxxxx.aws.tidbcloud.com
    TIDB_PORT='4000'
    TIDB_USER='{user}'  # e.g. xxxxxx.root
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
    python mysql_connector_example.py
    ```

2. 查看 [`Expected-Output.txt`](https://github.com/tidb-samples/tidb-python-mysqlconnector-quickstart/blob/main/Expected-Output.txt)，并与你的程序输出进行比较。结果近似即为连接成功。

## 示例代码片段

你可参考以下关键代码片段，完成自己的应用开发。

完整代码及其运行方式，见代码仓库 [tidb-samples/tidb-python-mysqlconnector-quickstart](https://github.com/tidb-samples/tidb-python-mysqlconnector-quickstart)。

### 连接到 TiDB

```python
def get_connection(autocommit: bool = True) -> MySQLConnection:
    db_conf = {
        "host": '${tidb_host}',
        "port": '${tidb_port}',
        "user": '${tidb_user}',
        "password": '${tidb_password}',
        "database": '${tidb_db_name}',
        "autocommit": autocommit,
        "use_pure": True,
    }

    if '${ca_path}':
        db_conf["ssl_verify_cert"] = True
        db_conf["ssl_verify_identity"] = True
        db_conf["ssl_ca"] = '${ca_path}'
    return mysql.connector.connect(**db_conf)
```

在使用该函数时，你需要将 `${tidb_host}`、`${tidb_port}`、`${tidb_user}`、`${tidb_password}`、`${tidb_db_name}` 以及 `${ca_path}` 替换为你的 TiDB 集群的实际值。

### 插入数据

```python
with get_connection(autocommit=True) as conn:
    with conn.cursor() as cur:
        player = ("test", 1, 1)
        cursor.execute("INSERT INTO players (id, coins, goods) VALUES (%s, %s, %s)", player)
```

更多信息参考[插入数据](/develop/dev-guide-insert-data.md)。

### 查询数据

```python
with get_connection(autocommit=True) as conn:
    with conn.cursor() as cur:
        cur.execute("SELECT count(*) FROM players")
        print(cur.fetchone()[0])
```

更多信息参考[查询数据](/develop/dev-guide-get-data-from-single-table.md)。

### 更新数据

```python
with get_connection(autocommit=True) as conn:
    with conn.cursor() as cur:
        player_id, amount, price="test", 10, 500
        cur.execute(
            "UPDATE players SET goods = goods + %s, coins = coins + %s WHERE id = %s",
            (-amount, price, player_id),
        )
```

更多信息参考[更新数据](/develop/dev-guide-update-data.md)。

### 删除数据

```python
with get_connection(autocommit=True) as conn:
    with conn.cursor() as cur:
        player_id = "test"
        cur.execute("DELETE FROM players WHERE id = %s", (player_id,))
```

更多信息参考[删除数据](/develop/dev-guide-delete-data.md)。

## 注意事项

### 使用驱动程序还是 ORM 框架？

Python 驱动程序提供对数据库的底层访问，但要求开发者：

- 手动建立和释放数据库连接
- 手动管理数据库事务
- 手动将数据行（在 `mysql-connector-python` 中表示为元组 (Tuple) 或者字典 (Dictionary)）映射为数据对象

建议仅在需要编写复杂的 SQL 语句时使用驱动程序。其他情况下，建议使用 [ORM](https://zh.wikipedia.org/wiki/对象关系映射) 框架进行开发，例如 [SQLAlchemy](/develop/dev-guide-sample-application-python-sqlalchemy.md)、[Peewee](/develop/dev-guide-sample-application-python-peewee.md) 和 [Django](/develop/dev-guide-sample-application-python-django.md)。ORM 可以帮助你：

- 减少管理连接和事务的[模板代码](https://en.wikipedia.org/wiki/Boilerplate_code)
- 使用数据对象代替大量 SQL 语句来操作数据

## 下一步

- 关于 mysql-connector-python 的更多使用方法，可以参考 [MySQL Connector/Python 官方文档](https://dev.mysql.com/doc/connector-python/en/)。
- 你可以继续阅读开发者文档，以获取更多关于 TiDB 应用开发的最佳实践。例如：[插入数据](/develop/dev-guide-insert-data.md)、[更新数据](/develop/dev-guide-update-data.md)、[删除数据](/develop/dev-guide-delete-data.md)、[单表读取](/develop/dev-guide-get-data-from-single-table.md)、[事务](/develop/dev-guide-transaction-overview.md)、[SQL 性能优化](/develop/dev-guide-optimize-sql-overview.md)等。
- 如果你更倾向于参与课程进行学习，我们也提供专业的 [TiDB 开发者课程](https://cn.pingcap.com/courses-catalog/category/back-end-developer/?utm_source=docs-cn-dev-guide)支持，并在考试后提供相应的[资格认证](https://learn.pingcap.com/learner/certification-center)。

## 需要帮助?

如果在开发的过程中遇到问题，可以在 [AskTUG](https://asktug.com/?utm_source=docs-cn-dev-guide) 上进行提问，寻求帮助。