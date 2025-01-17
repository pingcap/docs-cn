---
title: 信息函数
summary: TiDB 支持 MySQL 8.0 中提供的大部分信息函数。
---

# 信息函数

TiDB 支持使用 MySQL 8.0 中提供的大部分[信息函数](https://dev.mysql.com/doc/refman/8.0/en/information-functions.html)。

## TiDB 支持的 MySQL 信息函数

| 函数名 | 功能描述                                 |
| ------ | ---------------------------------------- |
| [`BENCHMARK()`](#benchmark) | 循环执行一个表达式 |
| [`CONNECTION_ID()`](#connection_id) | 返回当前连接的连接 ID（线程 ID）  |
| [`CURRENT_ROLE()`](#current_role) | 返回当前连接的角色 |
| [`CURRENT_USER()`, `CURRENT_USER`](#current_user) | 返回当前用户的用户名和主机名 |
| [`DATABASE()`](#database) | 返回默认（当前）的数据库  |
| [`FOUND_ROWS()`](#found_rows) | 该函数对于一个包含 `LIMIT` 的 `SELECT` 查询语句，返回在不包含 `LIMIT` 的情况下的记录数 |
| [`LAST_INSERT_ID()`](#last_insert_id) | 返回上一条 `INSERT` 语句中自增列的值  |
| [`ROW_COUNT()`](#row_count) | 影响的行数 |
| [`SCHEMA()`](#schema) | 与 `DATABASE()` 同义  |
| [`SESSION_USER()`](#session_user) | 与 `USER()` 同义   |
| [`SYSTEM_USER()`](#system_user) | 与 `USER()` 同义   |
| [`USER()`](#user) | 返回客户端提供的用户名和主机名    |
| [`VERSION()`](#version) | 返回当前 MySQL 服务器的版本信息   |

### BENCHMARK()

`BENCHMARK()` 函数可以按照指定的次数重复执行给定的表达式。

语法：

```sql
BENCHMARK(count, expression)
```

- `count`：要执行表达式的次数。
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

`CONNECTION_ID()` 函数返回连接的 ID。根据 TiDB 的 [`enable-32bits-connection-id`](/tidb-configuration-file.md#enable-32bits-connection-id-从-v730-版本开始引入) 配置项的值不同，该函数将返回一个 32 位或 64 位的连接 ID。

如果启用了 [`enable-global-kill`](/tidb-configuration-file.md#enable-global-kill-从-v610-版本开始引入)，连接的 ID 可用于在同一集群的多个 TiDB 实例中终止查询。

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

`CURRENT_ROLE()` 函数返回当前会话的当前[角色](/role-based-access-control.md)。

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

`CURRENT_USER()` 函数返回当前会话中使用的账户。

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

`DATABASE()` 函数返回当前会话正在使用的数据库名。

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

`FOUND_ROWS()` 函数返回上一条执行的 `SELECT` 语句的结果集中的行数。

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
> `SQL_CALC_FOUND_ROWS` 查询修饰符用于计算在没有 `LIMIT` 子句的情况下结果集中的总行数，只有在启用了 [`tidb_enable_noop_functions`](/system-variables.md#tidb_enable_noop_functions-从-v40-版本开始引入) 时才能使用。从 MySQL 8.0.17 开始，该查询修饰符已废弃。建议使用 `COUNT(*)` 代替。

### LAST_INSERT_ID()

`LAST_INSERT_ID()` 函数返回包含 [`AUTO_INCREMENT`](/auto-increment.md) 或 [`AUTO_RANDOM`](/auto-random.md) 列的表中最后插入行的 ID。

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
> - 在 TiDB 中，[`AUTO_ID_CACHE`](/auto-increment.md#auto_id_cache) 可能会导致该函数的返回结果与 MySQL 不同。这是因为 TiDB 在每个节点上都会各自缓存 ID，这可能导致分配的 ID 出现无序或间隔。如果你的应用程序依赖于严格的 ID 顺序，可以启用 [MySQL 兼容模式](/auto-increment.md#mysql-兼容模式)。
>
> - 在以上示例中，ID 是以 2 递增的，而 MySQL 在相同场景中生成的 ID 是以 1 递增的。关于兼容性的更多信息，请参见[自增 ID](/mysql-compatibility.md#自增-id)。

`LAST_INSERT_ID(expr)` 函数可以接受一个表达式作为参数，并将该值存储以供下一次调用 `LAST_INSERT_ID()` 时使用。你可以使用该函数生成序列，与 MySQL 保持兼容。注意 TiDB 也支持标准的[序列函数](/functions-and-operators/sequence-functions.md)。

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

`SCHEMA()` 函数与 [`DATABASE()`](#database) 同义。

### SESSION_USER()

`SESSION_USER()` 函数与 [`USER()`](#user) 同义。

### SYSTEM_USER()

`SYSTEM_USER()` 函数与 [`USER()`](#user) 同义。

### USER()

`USER()` 函数返回当前连接的用户。该函数的输出可能与 `CURRENT_USER()` 的输出略有不同，因为 `USER()` 显示的是实际 IP 地址，而不是通配符。

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

`VERSION()` 函数以与 MySQL 兼容的格式返回 TiDB 版本。如需获取更详细的版本信息，可以使用 [`TIDB_VERSION()`](/functions-and-operators/tidb-functions.md#tidb_version) 函数。

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

以上示例来自 TiDB v7.5.1，它会将自身标识为 MySQL 8.0.11。

如需更改该函数返回的版本，可以修改 [`server-version`](/tidb-configuration-file.md#server-version) 配置项。

## TiDB 特有的信息函数

下列函数为 TiDB 中特有的信息函数，MySQL 中无对应的函数。

| 函数名 | 功能描述                                 |
| ------ | ---------------------------------------- |
| [`CURRENT_RESOURCE_GROUP()`](/functions-and-operators/tidb-functions.md#current_resource_group) | 返回当前连接的资源组名 |

## TiDB 不支持的信息函数

* `CHARSET()`
* `COERCIBILITY()`
* `COLLATION()`
* `ICU_VERSION()`
* `ROLES_GRAPHML()`
