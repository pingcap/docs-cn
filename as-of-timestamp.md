---
title: 使用 AS OF TIMESTAMP 语法读取历史数据
summary: 了解如何使用 AS OF TIMESTAMP 语法读取历史数据。
---

# 使用 AS OF TIMESTAMP 语法读取历史数据

本文档介绍如何通过 `AS OF TIMESTAMP` 语句使用 [Stale Read](/stale-read.md) 功能来读取 TiDB 历史版本数据，包括具体的操作示例以及历史数据的保存策略。

TiDB 支持通过标准 SQL 接口，即通过 `AS OF TIMESTAMP` SQL 语法的形式读取历史数据，无需特殊的服务器或者驱动器。当数据被更新或删除后，你可以通过 SQL 接口将更新或删除前的数据读取出来。

> **注意：**
>
> 读取历史数据时，即使当前数据的表结构相较于历史数据的表结构已经发生改变，历史数据也会以当时的历史表结构来返回。

## 语法方式

你可以通过以下三种方式使用 `AS OF TIMESTAMP` 语法：

- [`SELECT ... FROM ... AS OF TIMESTAMP`](/sql-statements/sql-statement-select.md)
- [`START TRANSACTION READ ONLY AS OF TIMESTAMP`](/sql-statements/sql-statement-start-transaction.md)
- [`SET TRANSACTION READ ONLY AS OF TIMESTAMP`](/sql-statements/sql-statement-set-transaction.md)

如果你想要指定一个精确的时间点，可在 `AS OF TIMESTAMP` 中使用日期时间和时间函数，日期时间的格式为："2016-10-08 16:45:26.999"，最小时间精度范围为毫秒，通常可只写到秒，例如 "2016-10-08 16:45:26"。你也可以通过 `NOW(3)` 函数获得精确到毫秒的当前时间。如果想读取几秒前的数据，可以使用表达式如：`NOW() - INTERVAL 10 SECOND`（推荐）

如果你想要指定一个时间范围，需要使用 `TIDB_BOUNDED_STALENESS()` 函数。使用该函数，TiDB 会在指定的时间范围内选择一个合适的时间戳，该时间戳能保证所访问的副本上不存在开始于这个时间戳之前且还没有提交的相关事务，即能保证所访问的可用副本上执行读取操作而且不会被阻塞。用法为 `TIDB_BOUNDED_STALENESS(t1, t2)`，其中 `t1` 和 `t2` 为时间范围的两端，支持使用日期时间和时间函数。

示例如下：

- `AS OF TIMESTAMP '2016-10-08 16:45:26'` 表示读取在 2016 年 10 月 8 日 16 点 45 分 26 秒时最新的数据。
- `AS OF TIMESTAMP NOW() - INTERVAL 10 SECOND` 表示读取 10 秒前最新的数据。
- `AS OF TIMESTAMP TIDB_BOUNDED_STALENESS('2016-10-08 16:45:26', '2016-10-08 16:45:29')` 表示读取在 2016 年 10 月 8 日 16 点 45 分 26 秒到 29 秒的时间范围内尽可能新的数据。
- `AS OF TIMESTAMP TIDB_BOUNDED_STALENESS(NOW() - INTERVAL 20 SECOND, NOW())` 表示读取 20 秒前到现在的时间范围内尽可能新的数据。

注意： 除了指定时间戳，`AS OF TIMESTAMP` 语法最常用使用的方式是读几秒前的数据。如果采用这种方式，取值范围推荐为读 5 秒以上的历史数据。

## 示例

本节通过多个示例介绍 `AS OF TIMESTAMP` 语法的不同使用方法。在本节中，先介绍如何准备用于恢复的数据，再分别展示如何通过 `SELECT`、`START TRANSACTION READ ONLY AS OF TIMESTAMP`、`SET TRANSACTION READ ONLY AS OF TIMESTAMP` 以及 `SELECT` 子句使用 `AS OF TIMESTAMP`。

### 准备数据

在准备数据阶段，创建一张表，并插入若干行数据：

```sql
create table t (c int);
```

```
Query OK, 0 rows affected (0.01 sec)
```

```sql
insert into t values (1), (2), (3);
```

```
Query OK, 3 rows affected (0.00 sec)
```

查看表中的数据：

```sql
select * from t;
```

```
+------+
| c    |
+------+
|    1 |
|    2 |
|    3 |
+------+
3 rows in set (0.00 sec)
```

查看当前时间：

```sql
select now();
```

```
+---------------------+
| now()               |
+---------------------+
| 2021-05-26 16:45:26 |
+---------------------+
1 row in set (0.00 sec)
```

更新某一行数据：

```sql
update t set c=22 where c=2;
```

```
Query OK, 1 row affected (0.00 sec)
```

确认数据已经被更新：

```sql
select * from t;
```

```
+------+
| c    |
+------+
|    1 |
|   22 |
|    3 |
+------+
3 rows in set (0.00 sec)
```

### 通过 `SELECT` 读取历史数据

通过 [`SELECT ... FROM ... AS OF TIMESTAMP`](/sql-statements/sql-statement-select.md) 语句读取一个基于历史时间的数据。

```sql
select * from t as of timestamp '2021-05-26 16:45:26';
```

```
+------+
| c    |
+------+
|    1 |
|    2 |
|    3 |
+------+
3 rows in set (0.00 sec)
```

> **注意：**
>
> 通过 `SELECT` 语句读取多个表时要保证 TIMESTAMP EXPRESSION 是一致的。 比如： `select * from t as of timestamp NOW() - INTERVAL 2 SECOND, c as of timestamp NOW() - INTERVAL 2 SECOND;`。此外，在 `SELECT` 语句中，你必须要指定相关数据表的 as of 信息，若不指定，`SELECT` 语句会默认读最新的数据。

### 通过 `START TRANSACTION READ ONLY AS OF TIMESTAMP` 读取历史数据

通过 [`START TRANSACTION READ ONLY AS OF TIMESTAMP`](/sql-statements/sql-statement-start-transaction.md) 语句，你可以开启一个基于历史时间的只读事务，该事务基于所提供的历史时间来读取历史数据。

```sql
start transaction read only as of timestamp '2021-05-26 16:45:26';
```

```
Query OK, 0 rows affected (0.00 sec)
```

```sql
select * from t;
```

```
+------+
| c    |
+------+
|    1 |
|    2 |
|    3 |
+------+
3 rows in set (0.00 sec)
```

```sql
commit;
```

```
Query OK, 0 rows affected (0.00 sec)
```

当事务结束后，即可读取最新数据。

```sql
select * from t;
```

```
+------+
| c    |
+------+
|    1 |
|   22 |
|    3 |
+------+
3 rows in set (0.00 sec)
```

> **注意：**
>
> 通过 `START TRANSACTION READ ONLY AS OF TIMESTAMP` 开启的事务为只读事务。假如在该事务中执行写入操作，操作将会被该事务拒绝。

### 通过 `SET TRANSACTION READ ONLY AS OF TIMESTAMP` 读取历史数据

通过 [`SET TRANSACTION READ ONLY AS OF TIMESTAMP`](/sql-statements/sql-statement-set-transaction.md) 语句，你可以将下一个事务设置为基于指定历史时间的只读事务。该事务将会基于所提供的历史时间来读取历史数据。

```sql
set transaction read only as of timestamp '2021-05-26 16:45:26';
```

```
Query OK, 0 rows affected (0.00 sec)
```

```sql
begin;
```

```
Query OK, 0 rows affected (0.00 sec)
```

```sql
select * from t;
```

```
+------+
| c    |
+------+
|    1 |
|    2 |
|    3 |
+------+
3 rows in set (0.00 sec)
```

```sql
commit;
```

```
Query OK, 0 rows affected (0.00 sec)
```

当事务结束后，即可读取最新数据。

```sql
select * from t;
```

```
+------+
| c    |
+------+
|    1 |
|   22 |
|    3 |
+------+
3 rows in set (0.00 sec)
```

> **注意：**
>
> 通过 `SET TRANSACTION READ ONLY AS OF TIMESTAMP` 开启的事务为只读事务。假如在该事务中执行写入操作，操作将会被该事务拒绝。
