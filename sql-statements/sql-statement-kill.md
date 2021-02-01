---
title: KILL [TIDB]
summary: TiDB 数据库中 KILL [TIDB] 的使用概况。
aliases: ['/docs-cn/dev/sql-statements/sql-statement-kill/','/docs-cn/dev/reference/sql/statements/kill/']
---

# KILL [TIDB]

`KILL TIDB` 语句用于终止 TiDB 中的连接。

## 语法图

**KillStmt:**

![KillStmt](/media/sqlgram/KillStmt.png)

**KillOrKillTiDB:**

![KillOrKillTiDB](/media/sqlgram/KillOrKillTiDB.png)

## 示例

{{< copyable "sql" >}}

```sql
SHOW PROCESSLIST;
```

```
+------+------+-----------+------+---------+------+-------+------------------+
| Id   | User | Host      | db   | Command | Time | State | Info             |
+------+------+-----------+------+---------+------+-------+------------------+
|    1 | root | 127.0.0.1 | test | Query   |    0 | 2     | SHOW PROCESSLIST |
|    2 | root | 127.0.0.1 |      | Sleep   |    4 | 2     |                  |
+------+------+-----------+------+---------+------+-------+------------------+
2 rows in set (0.00 sec)
```

{{< copyable "sql" >}}

```sql
KILL TIDB 2;
```

```
Query OK, 0 rows affected (0.00 sec)
```

## MySQL 兼容性

* 按照设计，`KILL TIDB` 语句默认与 MySQL 不兼容。负载均衡器后面通常放有多个 TiDB 服务器，这种默认不兼容有助于防止在错误的 TiDB 服务器上终止连接。
* `KILL TIDB` 语句是 TiDB 的扩展语法。如果正尝试终止的会话位于同一个 TiDB 服务器上，可在配置文件里设置 [`compatible-kill-query = true`](/tidb-configuration-file.md#compatible-kill-query)。

## Global Kill <span class="version-mark">从 v5.0.0-rc 版本开始引入</span>

从 v5.0 版本开始，TiDB 为 [Global Kill](https://github.com/pingcap/tidb/blob/master/docs/design/2020-06-01-global-kill.md) 功能提供实验性支持。该功能用于安全地终止客户端与 TiDB 服务器间的连接。启用该功能后，连接到每台 TiDB 服务器的 ID 将是全局唯一的。客户端可以向任一 TiDB 服务器发送 `KILL` 语句，服务器再将请求路由至目标 TiDB 实例。即使 TiDB 服务器位于负载均衡器之后，`KILL` 也能安全地被执行。

要启用 Global Kill 功能，需要在配置文件的 `experimental` 部分设置 [`enable-global-kill = true`](/tidb-configuration-file.md#enable-global-kill-从-v500-rc-版本开始引入)。

## Global Kill 示例

在 TiDB 实例 `127.0.0.1:10180` 上执行如下语句：

```sql
SELECT SLEEP(60);
```

在 TiDB 实例 `127.0.0.1:10080` 上执行如下查询以及 `Kill` 操作：

```sql
SELECT * FROM INFORMATION_SCHEMA.CLUSTER_PROCESSLIST;
+-----------------+---------------------+------+-----------+--------------------+---------+------+------------+------------------------------------------------------+------------------------------------------------------------------+------+----------------------------------------+
| INSTANCE        | ID                  | USER | HOST      | DB                 | COMMAND | TIME | STATE      | INFO                                                 | DIGEST                                                           | MEM  | TxnStart                               |
+-----------------+---------------------+------+-----------+--------------------+---------+------+------------+------------------------------------------------------+------------------------------------------------------------------+------+----------------------------------------+
| 127.0.0.1:10180 | 8824324082762776581 | root | 127.0.0.1 | test               | Query   |    2 | autocommit | SELECT SLEEP(60)                                     | b4dae6a771c1d84157dcc302bef38cbff77a7a8ff89ee38302ac3324485454a3 |    0 |                                        |
| 127.0.0.1:10080 |   98041252825530373 | root | 127.0.0.1 | information_schema | Query   |    0 | autocommit | SELECT * FROM INFORMATION_SCHEMA.CLUSTER_PROCESSLIST | 43113c6fe27fb20eae4a6dc8c43f176f9292fd873dd08f1041debdff6d335cb0 |    0 | 01-15 23:13:20.609(422241527558045697) |
+-----------------+---------------------+------+-----------+--------------------+---------+------+------------+------------------------------------------------------+------------------------------------------------------------------+------+----------------------------------------+
2 rows in set (0.07 sec)

KILL 8824324082762776581;
Query OK, 0 rows affected (0.00 sec)
```

## 另请参阅

* [SHOW \[FULL\] PROCESSLIST](/sql-statements/sql-statement-show-processlist.md)
* [CLUSTER_PROCESSLIST](/information-schema/information-schema-processlist.md#cluster_processlist)
