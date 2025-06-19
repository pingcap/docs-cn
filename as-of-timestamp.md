---
title: 使用 `AS OF TIMESTAMP` 子句读取历史数据
summary: 了解如何使用 `AS OF TIMESTAMP` 语句子句读取历史数据。
---

# 使用 `AS OF TIMESTAMP` 子句读取历史数据

本文档介绍如何使用 `AS OF TIMESTAMP` 子句执行[历史读取](/stale-read.md)功能来读取 TiDB 中的历史数据，包括具体的使用示例和保存历史数据的策略。

TiDB 支持通过标准 SQL 接口读取历史数据，即 `AS OF TIMESTAMP` SQL 子句，无需特殊的客户端或驱动程序。在数据更新或删除后，您可以使用此 SQL 接口读取更新或删除之前的历史数据。

> **注意：**
>
> 在读取历史数据时，即使当前表结构已经发生变化，TiDB 也会返回旧表结构的数据。

## 语法

您可以通过以下三种方式使用 `AS OF TIMESTAMP` 子句：

- [`SELECT ... FROM ... AS OF TIMESTAMP`](/sql-statements/sql-statement-select.md)
- [`START TRANSACTION READ ONLY AS OF TIMESTAMP`](/sql-statements/sql-statement-start-transaction.md)
- [`SET TRANSACTION READ ONLY AS OF TIMESTAMP`](/sql-statements/sql-statement-set-transaction.md)

如果要指定精确的时间点，可以在 `AS OF TIMESTAMP` 子句中设置日期时间值或使用时间函数。日期时间的格式类似于 "2016-10-08 16:45:26.999"，最小时间单位为毫秒，但大多数情况下，秒级的时间单位足以指定日期时间，例如 "2016-10-08 16:45:26"。您也可以使用 `NOW(3)` 函数获取精确到毫秒的当前时间。如果要读取几秒前的数据，**建议**使用 `NOW() - INTERVAL 10 SECOND` 这样的表达式。

如果要指定时间范围，可以在子句中使用 [`TIDB_BOUNDED_STALENESS()`](/functions-and-operators/tidb-functions.md#tidb_bounded_staleness) 函数。使用此函数时，TiDB 会在指定的时间范围内选择一个合适的时间戳。"合适"意味着在访问的副本上没有在此时间戳之前开始且尚未提交的事务，即 TiDB 可以在访问的副本上执行读取操作，且读取操作不会被阻塞。您需要使用 `TIDB_BOUNDED_STALENESS(t1, t2)` 来调用此函数。`t1` 和 `t2` 是时间范围的两端，可以使用日期时间值或时间函数指定。

以下是 `AS OF TIMESTAMP` 子句的一些示例：

- `AS OF TIMESTAMP '2016-10-08 16:45:26'`：告诉 TiDB 读取 2016 年 10 月 8 日 16:45:26 存储的最新数据。
- `AS OF TIMESTAMP NOW() - INTERVAL 10 SECOND`：告诉 TiDB 读取 10 秒前存储的最新数据。
- `AS OF TIMESTAMP TIDB_BOUNDED_STALENESS('2016-10-08 16:45:26', '2016-10-08 16:45:29')`：告诉 TiDB 读取 2016 年 10 月 8 日 16:45:26 到 16:45:29 时间范围内尽可能新的数据。
- `AS OF TIMESTAMP TIDB_BOUNDED_STALENESS(NOW() - INTERVAL 20 SECOND, NOW())`：告诉 TiDB 读取 20 秒前到现在时间范围内尽可能新的数据。

> **注意：**
>
> 除了指定时间戳外，`AS OF TIMESTAMP` 子句最常见的用法是读取几秒前的数据。如果采用这种方法，建议读取 5 秒以前的历史数据。
>
> 使用历史读取时，需要为 TiDB 和 PD 节点部署 NTP 服务。这可以避免 TiDB 使用的指定时间戳超前于最新的 TSO 分配进度（例如超前几秒的时间戳），或晚于 GC 安全点时间戳的情况。当指定的时间戳超出服务范围时，TiDB 会返回错误。
>
> 为了减少延迟并提高历史读取数据的时效性，您可以修改 TiKV 的 `advance-ts-interval` 配置项。详情请参见[减少历史读取延迟](/stale-read.md#reduce-stale-read-latency)。

## 使用示例

本节通过几个示例介绍使用 `AS OF TIMESTAMP` 子句的不同方式。首先介绍如何准备用于恢复的数据，然后分别展示如何在 `SELECT`、`START TRANSACTION READ ONLY AS OF TIMESTAMP` 和 `SET TRANSACTION READ ONLY AS OF TIMESTAMP` 中使用 `AS OF TIMESTAMP`。

### 准备数据样本

要准备用于恢复的数据，首先创建一个表并插入几行数据：

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

更新一行数据：

```sql
update t set c=22 where c=2;
```

```
Query OK, 1 row affected (0.00 sec)
```

确认该行数据已更新：

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

### 使用 `SELECT` 语句读取历史数据

您可以使用 [`SELECT ... FROM ... AS OF TIMESTAMP`](/sql-statements/sql-statement-select.md) 语句读取过去某个时间点的数据。

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
> 在使用一个 `SELECT` 语句读取多个表时，需要确保 TIMESTAMP EXPRESSION 的格式一致。例如 `select * from t as of timestamp NOW() - INTERVAL 2 SECOND, c as of timestamp NOW() - INTERVAL 2 SECOND;`。此外，必须为 `SELECT` 语句中的相关表指定 `AS OF` 信息，否则 `SELECT` 语句默认读取最新数据。

### 使用 `START TRANSACTION READ ONLY AS OF TIMESTAMP` 语句读取历史数据

您可以使用 [`START TRANSACTION READ ONLY AS OF TIMESTAMP`](/sql-statements/sql-statement-start-transaction.md) 语句基于过去的某个时间点启动只读事务。该事务读取给定时间的历史数据。

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

事务提交后，您可以读取最新数据。

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
> 如果使用 `START TRANSACTION READ ONLY AS OF TIMESTAMP` 语句启动事务，则该事务为只读事务。在此事务中，写入操作将被拒绝。

### 使用 `SET TRANSACTION READ ONLY AS OF TIMESTAMP` 语句读取历史数据

您可以使用 [`SET TRANSACTION READ ONLY AS OF TIMESTAMP`](/sql-statements/sql-statement-set-transaction.md) 语句将下一个事务设置为基于过去某个时间点的只读事务。该事务读取给定时间的历史数据。

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

事务提交后，您可以读取最新数据。

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
> 如果使用 `SET TRANSACTION READ ONLY AS OF TIMESTAMP` 语句启动事务，则该事务为只读事务。在此事务中，写入操作将被拒绝。
