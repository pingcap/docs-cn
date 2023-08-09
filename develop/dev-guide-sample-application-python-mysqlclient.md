---
title: TiDB 和 mysqlclient 的简单示例
summary: 介绍如何使用 TiDB 和 mysqlclient 构造一个 CRUD 应用程序并给出重点代码片段。
---

<!-- markdownlint-disable MD024 -->
<!-- markdownlint-disable MD029 -->

# TiDB 和 mysqlclient 的简单示例

[mysqlclient](https://pypi.org/project/mysqlclient/) 为当前比较流行的开源 Python Driver 之一。

本文介绍如何使用 TiDB 和 mysqlclient 构造一个简单的 CRUD 应用程序。

虽然 Python 的 Driver 相较其他语言，使用简单。但其不可屏蔽底层实现，需要手动管控事务。所以如果没有大量必须使用 SQL 的场景，仍然推荐使用 ORM 编写程序，以降低程序耦合度。

## 前提条件

- Python 3.10 或更高版本
- mysqlclient 2.1.1 或更高版本
- TiDB 集群

    - 推荐使用 TiDB Serverless 集群。详情请参考[创建 TiDB Serverless 集群](/develop/dev-guide-build-cluster-in-cloud.md#第-1-步创建-tidb-serverless-集群)。
    - 可选使用[本地测试 TiDB 集群](/quick-start-with-tidb.md#部署本地测试集群)或[正式 TiDB 集群](/production-deployment-using-tiup.md)。

## 重点代码片段

本示例将运行在你的 TiDB 集群上，如果你还没有 TiDB 集群：


### 连接到 TiDB

下面函数示例使用 mysqlclient 连接到 TiDB：

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

在使用该函数时，你需要将 `${tidb_host}`、`${tidb_port}`、`${tidb_user}`、`${tidb_password}`、`${tidb_db_name}` 等变量替换为你的 TiDB 集群的实际值。

### 插入数据

下面示例为使用 mysqlclient 向 `player` 表插入数据：

```python
with get_mysqlclient_connection(autocommit=True) as conn:
    with conn.cursor() as cur:
        player = ("test", 1, 1)
        cursor.execute("INSERT INTO player (id, coins, goods) VALUES (%s, %s, %s)", player)
```

更多信息参考[插入数据](/develop/dev-guide-insert-data.md)。

### 查询数据

下面示例为使用 mysqlclient 从 `player` 表查询数据：

```python
with get_mysqlclient_connection(autocommit=True) as conn:
    with conn.cursor() as cur:
        cur.execute("SELECT count(*) FROM player")
        print(cur.fetchone()[0])
```

更多信息参考[查询数据](/develop/dev-guide-get-data-from-single-table.md)。

### 更新数据

下面示例为使用 mysqlclient 更新 `player` 表的数据：

```python
with get_mysqlclient_connection(autocommit=True) as conn:
    with conn.cursor() as cur:
        sell_id, amount, price="2", 10, 500
        cursor.execute("UPDATE player SET goods = goods + %s, coins = coins + %s WHERE id = %s", (-amount, price, sell_id))
```

更多信息参考[更新数据](/develop/dev-guide-update-data.md)。

### 删除数据

下面示例为使用 mysqlclient 删除 `player` 表的数据：

```python
with get_mysqlclient_connection(autocommit=True) as conn:
    with conn.cursor() as cur:
        player_id = "test"
        cursor.execute("DELETE FROM player WHERE id = %s", (player_id,))
```

更多信息参考[删除数据](/develop/dev-guide-delete-data.md)。

## 注意事项

- 完整代码及运行方式见 [tidb-example-python](https://github.com/pingcap-inc/tidb-example-python/blob/main/README-zh.md) GitHub 仓库。
- 由于 Driver 封装程度较低，程序内存在大量的 SQL 语句。需要注意，mysqlclient 的查询对象为元组 (tuple) 形式，与使用 ORM 的数据对象形式不同。
- 关于 mysqlclient 的更多使用方法，你可以参考 [mysqlclient 官方文档](https://mysqlclient.readthedocs.io/)。
- 你可以继续阅读开发者文档，以获取更多关于 TiDB 的应用开发知识。例如：[插入数据](/develop/dev-guide-insert-data.md)，[更新数据](/develop/dev-guide-update-data.md)，[删除数据](/develop/dev-guide-delete-data.md)，[单表读取](/develop/dev-guide-get-data-from-single-table.md)，[事务](/develop/dev-guide-transaction-overview.md)，[SQL 性能优化](/develop/dev-guide-optimize-sql-overview.md)等。
- 你还可以通过视频学习 [TiDB 开发者课程](https://cn.pingcap.com/courses-catalog/back-end-developer/?utm_source=docs-cn-dev-guide)并获得[认证](https://learn.pingcap.com/learner/certification-center)。