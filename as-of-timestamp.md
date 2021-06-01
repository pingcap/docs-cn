---
title: 使用 AS OF TIMESTAMP 语法读取历史数据
aliases: ['/docs-cn/dev/read-stale-data/']
---

# 使用 AS OF TIMESTAMP 语法读取历史数据

本文档介绍如何使用 Stale Read 功能中的 AS OF TIMESTAMP 语句来读取历史版本数据，包括具体的操作流程以及历史数据的保存策略。

## 功能说明

TiDB 实现了通过标准 SQL 接口读取历史数据功能，无需特殊的 client 或者 driver。当数据被更新、删除后，依然可以通过 SQL 接口将更新/删除前的数据读取出来。

另外即使在更新数据之后，表结构发生了变化，TiDB 依旧能用旧的表结构将数据读取出来。

## 语法方式

为支持读取历史版本数据，TiDB 扩展了新的语法 AS OF TIMESTAMP。目前支持以下三种方式使用该语法。

- 通过 [START TRANSACTION READ ONLY AS OF TIMESTAMP](/sql-statements/sql-statement-start-transaction.md)
- 通过 [SET TRANSACTION READ ONLY AS OF TIMESTAMP](/sql-statements/sql-statement-set-transaction.md)
- 通过 SELECT 子句中使用 AS OF TIMESTAMP

AS OF TIMESTAMP 支持接收日期时间和时间函数，日期时间的格式为：“2016-10-08 16:45:26.999”，最小时间精度范围为毫秒，但一般来说可以只写到秒，比如”2016-10-08 16:45:26”，也可以通过 `NOW(3)` 函数获得精确到毫秒的当前时间。当需要指定时间范围时，需要使用 `TIDB_BOUNDED_STALENESS()` 函数，具体用法为 `TIDB_BOUNDED_STALENESS(t1, t2)`，其中 t1 和 t2 为时间范围的两端，支持接受日期时间和时间函数，例如：

- `AS OF TIMESTAMP '2016-10-08 16:45:26'` 表示读取在 2016 年 10 月 8 日 16 点 45 分 26 秒时最新的数据。
- `AS OF TIMESTAMP NOW() - INTERVAL 10 SECOND` 表示读取 10 秒前最新的数据。
- `AS OF TIMESTAMP TIDB_BOUNDED_STALENESS('2016-10-08 16:45:26', '2016-10-08 16:45:29')` 表示读取在 2016 年 10 月 8 日 16 点 45 分 26 秒到 29 秒的时间范围内尽可能新的数据。
- `AS OF TIMESTAMP TIDB_BOUNDED_STALENESS(NOW() - INTERVAL 20 SECOND, NOW())` 表示读取 20 秒前到现在的时间范围内尽可能新的数据。

## 历史数据保留策略

参考[历史数据保留策略](/read-historical-data.md#历史数据保留策略)

## 示例

### 准备阶段

初始化阶段，创建一个表，并插入几行数据：

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

### 通过 START TRANSACTION READ ONLY AS OF TIMESTAMP 读取历史数据

通过 START TRANSACTION READ ONLY AS OF TIMESTAMP 开启一个基于历史时间的只读事务，该事务将会基于所提供的历史时间来读取历史数据。

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
> 通过 START TRANSACTION READ ONLY AS OF TIMESTAMP 开启的事务将会是一个只读事务。假如在该事务中执行写入操作，将会被该事务拒绝。

### 通过 SET TRANSACTION READ ONLY AS OF TIMESTAMP 读取历史数据

通过 START TRANSACTION READ ONLY AS OF TIMESTAMP 表示下一个事务为基于该历史时间的只读事务，该事务将会基于所提供的历史时间来读取历史数据。

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
> 通过 SET TRANSACTION READ ONLY AS OF TIMESTAMP 开启的事务将会是一个只读事务。假如在该事务中执行写入操作，将会被该事务拒绝。

### 通过 SELECT 子句中使用 AS OF TIMESTAMP 读取历史数据

通过 SELECT 子句中使用 AS OF TIMESTAMP 对当前的查询语句基于历史时间进行查询数据。

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

## 历史数据恢复策略

参考[历史数据恢复策略](/read-historical-data.md#历史数据恢复策略)
