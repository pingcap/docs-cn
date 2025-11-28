---
title: 使用 mysqlclient 连接到 TiDB
summary: 本文描述了 TiDB 和 mysqlclient 的连接步骤，并给出了简单示例代码片段。
---

<!-- markdownlint-disable MD024 -->
<!-- markdownlint-disable MD029 -->

# 如何用 mysqlclient 连接到 TiDB

TiDB 是一个兼容 MySQL 的数据库。[mysqlclient](https://pypi.org/project/mysqlclient/) 为当前流行的开源 Python Driver 之一。

本文档将展示如何使用 TiDB 和 mysqlclient 来构造一个简单的 CRUD 应用程序。

## 前置需求

- 推荐 [Python **3.10**](https://www.python.org/downloads/) 及以上版本。
- mysqlclient **2.1.1** 版本。在运行本教程的过程中会进行安装和配置，如果遇到安装问题，请参考 [mysqlclient 官方文档](https://github.com/PyMySQL/mysqlclient#install)。
- [Git](https://git-scm.com/downloads)。
- TiDB 集群。如果你还没有 TiDB 集群，可以按照以下方式创建：
    - （推荐方式）参考[创建 TiDB Serverless 集群](/develop/dev-guide-build-cluster-in-cloud.md#第-1-步创建-tidb-serverless-集群)，创建你自己的 TiDB Cloud 集群。
    - 参考[部署本地测试 TiDB 集群](/quick-start-with-tidb.md#部署本地测试集群)或[部署正式 TiDB 集群](/production-deployment-using-tiup.md)，创建本地集群。

## 运行代码并连接到 TiDB

本小节演示如何运行示例应用程序的代码，并连接到 TiDB。

### 第 1 步：克隆示例代码仓库到本地

```bash
git clone https://github.com/pingcap-inc/tidb-example-python.git
```

### 第 2 步：安装依赖 (包括 mysqlclient)

```bash
cd tidb-example-python;
pip install -r requirement.txt
```

### 第 3 步：配置连接信息

根据不同的 TiDB 部署方式，使用不同的方法连接到 TiDB 集群。

<SimpleTab>

<div label="TiDB Serverless">

1. 在 TiDB Cloud Web Console 中，选择你的 TiDB Serverless 集群，进入 **Overview** 页面，点击右上角的 **Connect** 按钮。

2. 确认窗口中的配置和你的运行环境一致。

    - Endpoint 为 **Public**
    - Connect With 选择 **General**
    - Operating System 为你的运行环境。

    <Tip>如果你在 Windows Subsystem for Linux (WSL) 中运行，请切换为对应的 Linux 发行版。</Tip>

3. 点击 **Generate Password** 生成密码。
   
   <Tip>如果你之前已经生成过密码，可以直接使用原密码，或点击 **Reset Password** 重新生成密码。</Tip>

4. 运行以下命令，将 `.env.example` 复制并重命名为 `.env`：

    ```bash
    cp .env.example .env
    ```

5. 复制并粘贴对应连接字符串至 `.env` 中。示例结果如下。

    ```python
    TIDB_HOST='{gateway-region}.aws.tidbcloud.com'
    TIDB_PORT='4000'
    TIDB_USER='{prefix}.root'
    TIDB_PASSWORD='{password}'
    TIDB_DB_NAME='test'
    CA_PATH=''
    ```

    注意替换 `{}` 中的占位符为 **Connect** 窗口中获得的值。
    
    TiDB Serverless 要求使用 secure connection，由于 mysqlclient 的 `ssl_mode` 默认为 `PREFERRED`，所以不需要你手动指定 `CA_PATH`，设置为空即可。但如果你有特殊原因需要手动指定 `CA_PATH`，可以参考 [TiDB Cloud 文档](https://docs.pingcap.com/tidbcloud/secure-connections-to-serverless-clusters#root-certificate-default-path)获取不同操作系统下证书的路径。

6. 保存文件。

</div>

<div label="TiDB Dedicated">

1. 在 TiDB Cloud Web Console 中，选择你的 TiDB Dedicated 集群，进入 **Overview** 页面，点击右上角的 **Connect** 按钮。点击 **Allow Access from Anywhere** 并点击 **Download CA cert** 下载证书。

    <Tip>

    更多配置细节，可参考 [TiDB Dedicated 标准连接教程](https://docs.pingcap.com/tidbcloud/connect-via-standard-connection)。

    </Tip>

2. 运行以下命令，将 `.env.example` 复制并重命名为 `.env`：

    ```bash
    cp .env.example .env
    ```

3. 复制并粘贴对应的连接字符串至 `.env` 中。示例结果如下：

    ```python
    TIDB_HOST='{host}.clusters.tidb-cloud.com'
    TIDB_PORT='4000'
    TIDB_USER='{username}'
    TIDB_PASSWORD='{password}'
    TIDB_DB_NAME='test'
    CA_PATH='{your-downloaded-ca-path}'
    ```

    注意替换 `{}` 中的占位符为 **Connect** 窗口中获得的值，并配置前面步骤中下载好的证书路径。

4. 保存文件。

</div>

<div label="自建 TiDB">

1. 运行以下命令，将 `.env.example` 复制并重命名为 `.env`：

    ```bash
    cp .env.example .env
    ```

2. 复制并粘贴对应 TiDB 的连接字符串至 `.env` 中。示例结果如下。

    ```python
    TIDB_HOST='{tidb_server_host}'
    TIDB_PORT='4000'
    TIDB_USER='root'
    TIDB_PASSWORD='{password}'
    TIDB_DB_NAME='test'
    ```

    注意替换 `{}` 中的占位符为你的 TiDB 对应的值，并删除 `CA_PATH` 这行。如果你在本机运行 TiDB，默认 Host 地址为 `127.0.0.1`，密码为空。

3. 保存文件。

</div>

</SimpleTab>

### 第 4 步：运行代码并查看结果

1. 运行下述命令，执行示例代码：

    ```python
    python3 mysqlclient_example.py
    ```

2. 查看[示例输出](https://github.com/pingcap-inc/tidb-example-python/blob/main/Expected-Output.md#mysqlclient)，并与你的程序输出进行比较。结果近似即为连接成功。

## 重点代码片段

你可参考以下关键代码片段，完成自己的应用开发。

### 连接到 TiDB

```python
def get_mysqlclient_connection(autocommit:bool=True) -> MySQLdb.Connection:
    db_conf = {
        "host": ${tidb_host},
        "port": ${tidb_port},
        "user": ${tidb_user},
        "password": ${tidb_password},
        "database": ${tidb_db_name},
        "autocommit": autocommit
    }

    if ${ca_path}:
        db_conf["ssl_mode"] = "VERIFY_IDENTITY"
        db_conf["ssl"] = {"ca": ${ca_path}}

    return MySQLdb.connect(**db_conf)
```

在使用该函数时，你需要将 `${tidb_host}`、`${tidb_port}`、`${tidb_user}`、`${tidb_password}`、`${tidb_db_name}` 等替换为你的 TiDB 集群的实际值。

### 插入数据

```python
with get_mysqlclient_connection(autocommit=True) as conn:
    with conn.cursor() as cur:
        player = ("1", 1, 1)
        cursor.execute("INSERT INTO player (id, coins, goods) VALUES (%s, %s, %s)", player)
```

更多信息参考[插入数据](/develop/dev-guide-insert-data.md)。

### 查询数据

```python
with get_mysqlclient_connection(autocommit=True) as conn:
    with conn.cursor() as cur:
        cur.execute("SELECT count(*) FROM player")
        print(cur.fetchone()[0])
```

更多信息参考[查询数据](/develop/dev-guide-get-data-from-single-table.md)。

### 更新数据

```python
with get_mysqlclient_connection(autocommit=True) as conn:
    with conn.cursor() as cur:
        player_id, amount, price="1", 10, 500
        cursor.execute("UPDATE player SET goods = goods + %s, coins = coins + %s WHERE id = %s", (-amount, price, player_id))
```

更多信息参考[更新数据](/develop/dev-guide-update-data.md)。

### 删除数据

```python
with get_mysqlclient_connection(autocommit=True) as conn:
    with conn.cursor() as cur:
        player_id = "1"
        cursor.execute("DELETE FROM player WHERE id = %s", (player_id,))
```

更多信息参考[删除数据](/develop/dev-guide-delete-data.md)。

## 注意事项

- 完整代码及其运行方式，见 [tidb-example-python](https://github.com/pingcap-inc/tidb-example-python/blob/main/README-zh.md) GitHub 仓库。
- Driver 封装程度较低，因此在程序内会见到大量的 SQL 语句。与 ORM 不同，因为没有数据对象的存在，`mysqlclient` 的查询对象以元组 (tuple) 进行表示。虽然 Python 的 Driver 相较其他语言的使用更方便，但因其不可屏蔽底层实现，需手动管控事务的特性，如果没有大量必须使用 SQL 的场景，仍然推荐使用 ORM 进行程序编写。这可以降低程序的耦合性。
- 关于 mysqlclient 的更多使用方法，可以参考 [mysqlclient 官方文档](https://mysqlclient.readthedocs.io/)。

## 下一步

- 你可以继续阅读开发者文档，以获取更多关于 TiDB 的开发者知识。例如：[插入数据](/develop/dev-guide-insert-data.md)，[更新数据](/develop/dev-guide-update-data.md)，[删除数据](/develop/dev-guide-delete-data.md)，[单表读取](/develop/dev-guide-get-data-from-single-table.md)，[事务](/develop/dev-guide-transaction-overview.md)，[SQL 性能优化](/develop/dev-guide-optimize-sql-overview.md)等。
- 如果你更倾向于参与课程进行学习，我们也提供专业的 [TiDB 开发者课程](https://cn.pingcap.com/courses-catalog/back-end-developer/?utm_source=docs-cn-dev-guide)支持，并在考试后提供相应的[资格认证](https://learn.pingcap.cn/learner/certification-center)。
