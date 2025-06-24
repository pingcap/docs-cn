---
title: 信息函数
summary: 了解信息函数。
---

# 信息函数

TiDB 支持大多数 MySQL 8.0 中可用的[信息函数](https://dev.mysql.com/doc/refman/8.0/en/information-functions.html)。

## TiDB 支持的 MySQL 函数

| 名称 | 描述 |
|:-----|:------------|
| [`BENCHMARK()`](#benchmark) | 在循环中执行表达式 |
| [`CONNECTION_ID()`](#connection_id) | 返回连接 ID（线程 ID） |
| [`CURRENT_ROLE()`](#current_role) | 返回连接当前使用的角色 |
| [`CURRENT_USER()`, `CURRENT_USER`](#current_user) | 返回已认证的用户名和主机名 |
| [`DATABASE()`](#database) | 返回默认（当前）数据库名称 |
| [`FOUND_ROWS()`](#found_rows) | 对于带有 `LIMIT` 子句的 `SELECT`，返回如果没有 `LIMIT` 子句时将返回的行数 |
| [`LAST_INSERT_ID()`](#last_insert_id) | 返回最后一次 `INSERT` 的 `AUTOINCREMENT` 列的值 |
| [`ROW_COUNT()`](#row_count) | 受影响的行数 |
| [`SCHEMA()`](#schema) | `DATABASE()` 的同义词 |
| [`SESSION_USER()`](#session_user) | `USER()` 的同义词 |
| [`SYSTEM_USER()`](#system_user) | `USER()` 的同义词 |
| [`USER()`](#user) | 返回客户端提供的用户名和主机名 |
| [`VERSION()`](#version) | 返回表示 MySQL 服务器版本的字符串 |

### BENCHMARK()

`BENCHMARK()` 函数将给定表达式执行指定次数。

语法：

```sql
BENCHMARK(count, expression)
```

- `count`：表达式要执行的次数。
- `expression`：要重复执行的表达式。

示例：

```sql
SELECT BENCHMARK(5, SLEEP(2));
```

```
+------------------------+
| BENCHMARK(5, SLEEP(2)) |
+------------------------+
|                      0 |
+------------------------+
1 row in set (10.00 sec)
```

### CONNECTION_ID()

<CustomContent platform="tidb">

`CONNECTION_ID()` 函数返回连接的 ID。根据 TiDB 的 [`enable-32bits-connection-id`](/tidb-configuration-file.md#enable-32bits-connection-id-new-in-v730) 配置项的值，此函数返回 32 位或 64 位连接 ID。

如果启用了 [`enable-global-kill`](/tidb-configuration-file.md#enable-global-kill-new-in-v610)，则可以使用连接 ID 在同一集群的多个 TiDB 实例之间终止查询。

</CustomContent>

<CustomContent platform="tidb-cloud">

`CONNECTION_ID()` 函数返回连接的 ID。根据 TiDB 的 [`enable-32bits-connection-id`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#enable-32bits-connection-id-new-in-v730) 配置项的值，此函数返回 32 位或 64 位连接 ID。

如果启用了 [`enable-global-kill`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#enable-global-kill-new-in-v610)，则可以使用连接 ID 在同一集群的多个 TiDB 实例之间终止查询。

</CustomContent>

```sql
SELECT CONNECTION_ID();
```

```
+-----------------+
| CONNECTION_ID() |
+-----------------+
|       322961414 |
+-----------------+
1 row in set (0.00 sec)
```

### CURRENT_ROLE()

<CustomContent platform="tidb">

`CURRENT_ROLE()` 函数返回当前会话的当前[角色](/role-based-access-control.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

`CURRENT_ROLE()` 函数返回当前会话的当前[角色](https://docs.pingcap.com/tidb/stable/role-based-access-control)。

</CustomContent>

```sql
SELECT CURRENT_ROLE();
```

```
+----------------+
| CURRENT_ROLE() |
+----------------+
| NONE           |
+----------------+
1 row in set (0.00 sec)
```

### CURRENT_USER()

`CURRENT_USER()` 函数返回当前会话使用的账户。

```sql
SELECT CURRENT_USER();
```

```
+----------------+
| CURRENT_USER() |
+----------------+
| root@%         |
+----------------+
1 row in set (0.00 sec)
```

### DATABASE()

`DATABASE()` 函数返回当前会话正在使用的数据库架构。

```sql
SELECT DATABASE();
```

```
+------------+
| DATABASE() |
+------------+
| test       |
+------------+
1 row in set (0.00 sec)
```

### FOUND_ROWS()

`FOUND_ROWS()` 函数返回最后执行的 `SELECT` 语句结果集中的行数。

```sql
SELECT 1 UNION ALL SELECT 2;
```

```
+------+
| 1    |
+------+
|    2 |
|    1 |
+------+
2 rows in set (0.01 sec)
```

```sql
SELECT FOUND_ROWS();
```

```
+--------------+
| FOUND_ROWS() |
+--------------+
|            2 |
+--------------+
1 row in set (0.00 sec)
```

> **注意：**
>
> `SQL_CALC_FOUND_ROWS` 查询修饰符（用于计算结果集中的总行数而不考虑 `LIMIT` 子句）仅在启用 [`tidb_enable_noop_functions`](/system-variables.md#tidb_enable_noop_functions-new-in-v40) 时才被接受。从 MySQL 8.0.17 开始，此查询修饰符已被弃用。建议使用 `COUNT(*)` 代替。

### LAST_INSERT_ID()

`LAST_INSERT_ID()` 函数返回最后插入到包含 [`AUTO_INCREMENT`](/auto-increment.md) 或 [`AUTO_RANDOM`](/auto-random.md) 列的表中的行的 ID。

```sql
CREATE TABLE t1(id SERIAL);
Query OK, 0 rows affected (0.17 sec)

INSERT INTO t1() VALUES();
Query OK, 1 row affected (0.03 sec)

INSERT INTO t1() VALUES();
Query OK, 1 row affected (0.00 sec)

SELECT LAST_INSERT_ID();
+------------------+
| LAST_INSERT_ID() |
+------------------+
|                3 |
+------------------+
1 row in set (0.00 sec)

TABLE t1;
+----+
| id |
+----+
|  1 |
|  3 |
+----+
2 rows in set (0.00 sec)
```

> **注意**
>
> - 在 TiDB 中，[`AUTO_ID_CACHE`](/auto-increment.md#auto_id_cache) 可能导致结果与 MySQL 返回的结果不同。这种差异是因为 TiDB 在每个节点上缓存 ID，可能导致 ID 不按顺序或有间隔。如果您的应用程序需要严格的 ID 顺序，可以启用 [MySQL 兼容模式](/auto-increment.md#mysql-compatibility-mode)。
>
> - 在上面的示例中，ID 增加了 2，而 MySQL 在相同情况下会生成增加 1 的 ID。有关更多兼容性信息，请参见[自增 ID](/mysql-compatibility.md#auto-increment-id)。

### ROW_COUNT()

`ROW_COUNT()` 函数返回受影响的行数。

```sql
CREATE TABLE t1(id BIGINT UNSIGNED PRIMARY KEY AUTO_RANDOM);
Query OK, 0 rows affected, 1 warning (0.16 sec)

INSERT INTO t1() VALUES (),(),();
Query OK, 3 rows affected (0.02 sec)
Records: 3  Duplicates: 0  Warnings: 0

SELECT ROW_COUNT();
+-------------+
| ROW_COUNT() |
+-------------+
|           3 |
+-------------+
1 row in set (0.00 sec)
```

### SCHEMA()

`SCHEMA()` 函数是 [`DATABASE()`](#database) 的同义词。

### SESSION_USER()

`SESSION_USER()` 函数是 [`USER()`](#user) 的同义词。

### SYSTEM_USER()

`SYSTEM_USER()` 函数是 [`USER()`](#user) 的同义词。

### USER()

`USER()` 函数返回当前连接的用户。这可能与 `CURRENT_USER()` 的输出略有不同，因为 `USER()` 显示实际的 IP 地址而不是通配符。

```sql
SELECT USER(), CURRENT_USER();
```

```
+----------------+----------------+
| USER()         | CURRENT_USER() |
+----------------+----------------+
| root@127.0.0.1 | root@%         |
+----------------+----------------+
1 row in set (0.00 sec)
```

### VERSION()

`VERSION()` 函数返回与 MySQL 兼容格式的 TiDB 版本。要获取更详细的结果，可以使用 [`TIDB_VERSION()`](/functions-and-operators/tidb-functions.md#tidb_version) 函数。

```sql
SELECT VERSION();
+--------------------+
| VERSION()          |
+--------------------+
| 8.0.11-TiDB-v7.5.1 |
+--------------------+
1 row in set (0.00 sec)
```

```sql
SELECT TIDB_VERSION()\G
*************************** 1. row ***************************
TIDB_VERSION(): Release Version: v7.5.1
Edition: Community
Git Commit Hash: 7d16cc79e81bbf573124df3fd9351c26963f3e70
Git Branch: heads/refs/tags/v7.5.1
UTC Build Time: 2024-02-27 14:28:32
GoVersion: go1.21.6
Race Enabled: false
Check Table Before Drop: false
Store: tikv
1 row in set (0.00 sec)
```

上述示例来自 TiDB v7.5.1，它将自己标识为 MySQL 8.0.11。

<CustomContent platform="tidb">

如果要更改返回的版本，可以修改 [`server-version`](/tidb-configuration-file.md#server-version) 配置项。

</CustomContent>

## TiDB 特有函数

以下函数仅由 TiDB 支持，在 MySQL 中没有等效函数。

| 名称 | 描述 |
|:-----|:------------|
| [`CURRENT_RESOURCE_GROUP()`](/functions-and-operators/tidb-functions.md#current_resource_group) | 返回当前会话绑定的资源组名称 |

## 不支持的函数

* `CHARSET()`
* `COERCIBILITY()`
* `COLLATION()`
* `ICU_VERSION()`
* `ROLES_GRAPHML()`
