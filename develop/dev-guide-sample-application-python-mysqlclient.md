---
title: TiDB 和 mysqlclient 的简单 CRUD 应用程序
summary: 给出一个 TiDB 和 mysqlclient 的简单 CRUD 应用程序示例。
---

<!-- markdownlint-disable MD024 -->
<!-- markdownlint-disable MD029 -->

# TiDB 和 mysqlclient 的简单 CRUD 应用程序

[mysqlclient](https://pypi.org/project/mysqlclient/) 为当前比较流行的开源 Python Driver 之一。

本文档将展示如何使用 TiDB 和 mysqlclient 来构造一个简单的 CRUD 应用程序。此处将以 mysqlclient **2.1.1** 版本进行说明。虽然 Python 的 Driver 相较其他语言，使用也极其方便。但因其不可屏蔽底层实现，需手动管控事务的特性，如果没有大量必须使用 SQL 的场景，仍然推荐使用 ORM 进行程序编写。这可以降低程序的耦合性。

## 前提要求

- 已安装 [Python](https://www.python.org/)，推荐版本 3.10 及以上。
- 启动你的 TiDB 集群，如果你还没有 TiDB 集群：

    - 推荐参考[创建 TiDB Serverless 集群](/develop/dev-guide-build-cluster-in-cloud.md#第-1-步创建-tidb-serverless-集群)文档创建你自己的 TiDB Cloud 集群。
    - 备选参考[部署本地测试 TiDB 集群](/quick-start-with-tidb.md#部署本地测试集群)或[部署正式 TiDB 集群](/production-deployment-using-tiup.md)文档创建本地集群。

- 已获取代码并安装依赖

    ```bash
    git clone https://github.com/pingcap-inc/tidb-example-python.git
    cd tidb-example-python
    pip install requirement.txt
    ```

- 已正确配置代码目录下的 `.env` 配置文件，你可以用 `cp .env.example .env` 复制初始配置文件后进行更改。如果你不知道这些信息如何获取，请参考 [Obtain the connection parameters](https://docs.pingcap.com/tidbcloud/connect-via-standard-connection-serverless#obtain-the-connection-parameters) 及 [Where is the CA root path on my system?](https://docs.pingcap.com/tidbcloud/secure-connections-to-serverless-tier-clusters#where-is-the-ca-root-path-on-my-system) 文档：

    ```properties
    # TiDB 集群地址
    TIDB_HOST='xxxxxxxx.aws.tidbcloud.com'
    # TiDB 集群端口
    TIDB_PORT='4000'
    # TiDB 集群用户名
    TIDB_USER='xxxxxxxxxxx.root'
    # TiDB 集群密码
    TIDB_PASSWORD='xxxxxxx'
    # 希望本示例使用的数据库名称
    TIDB_DB_NAME='test'
    # 使用的 TiDB 集群是否是 Serverless
    IS_SERVERLESS='true'
    # 运行示例的实例上，CA 证书存在的位置，在 IS_SERVERLESS='true' 时必需
    CA_PATH='/etc/ssl/cert.pem'
    ```

## 运行

运行命令及结果如下：

```bash
% python3 mysqlclient_example.py
id:test, coins:1, goods:1
number of players: 1920
id:0008cd1b-9f88-47cd-865c-2f276add1618, coins:10000, goods:10000
id:0021e5ea-03ce-49d7-a9ad-fb837523b57a, coins:10000, goods:10000
id:00470444-e776-42b0-b248-f4a65bae80df, coins:10000, goods:10000
buy player 1 coins not enough
id:1, coins:100, goods:0
id:2, coins:114514, goods:20
```

## 重点代码片段

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

    if ${is_serverless}:
        db_conf["ssl_mode"] = "VERIFY_IDENTITY"
        db_conf["ssl"] = {"ca": ${ca_path}}

    return MySQLdb.connect(**db_conf)
```

### 增加

```python
with get_mysqlclient_connection(autocommit=True) as conn:
    with conn.cursor() as cur:
        player = ("test", 1, 1)
        cursor.execute("INSERT INTO player (id, coins, goods) VALUES (%s, %s, %s)", player)
```

### 删除

```python
with get_mysqlclient_connection(autocommit=True) as conn:
    with conn.cursor() as cur:
        player_id = 1
        cursor.execute("DELETE FROM player WHERE id = %s", (player_id,))
```

### 更新

```python
with get_mysqlclient_connection(autocommit=True) as conn:
    with conn.cursor() as cur:
        sell_id, amount, price="2", 10, 500
        cursor.execute("UPDATE player set goods = goods + %s, coins = coins + %s WHERE id = %s", (-amount, price, sell_id))
```

### 查询

```python
with get_mysqlclient_connection(autocommit=True) as conn:
    with conn.cursor() as cur:
        cur.execute("SELECT count(*) FROM player")
        print(cur.fetchone()[0])
```

## 其他值得注意的事

- Driver 有着更低的封装程度，因此我们可以在程序内见到大量的 SQL。与 ORM 不同，因为没有数据对象的存在，`mysqlclient` 的查询对象将以元组 (tuple) 进行表示。
- 关于 mysqlclient 的更多使用方法，你可以参考 [mysqlclient 官方文档](https://mysqlclient.readthedocs.io/)。
- 你可以继续阅读开发者文档，以获取更多关于 TiDB 的开发者知识。例如：[插入数据](/develop/dev-guide-insert-data.md)，[更新数据](/develop/dev-guide-update-data.md)，[删除数据](/develop/dev-guide-delete-data.md)，[单表读取](/develop/dev-guide-get-data-from-single-table.md)，[事务](/develop/dev-guide-transaction-overview.md)，[SQL 性能优化](/develop/dev-guide-optimize-sql-overview.md)等。
- 如果你更倾向于参与课程进行学习，我们也提供专业的 [TiDB 开发者课程](https://cn.pingcap.com/courses-catalog/back-end-developer/?utm_source=docs-cn-dev-guide)支持，并在考试后提供相应的[资格认证](https://learn.pingcap.com/learner/certification-center)。