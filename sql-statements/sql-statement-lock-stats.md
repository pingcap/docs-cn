---
title: LOCK STATS
summary: TiDB 数据库中 LOCK STATS 的使用概述。
---

# LOCK STATS

`LOCK STATS` 用于锁定表或分区的统计信息。当统计信息被锁定时，TiDB 不会自动更新表或分区的统计信息。有关具体行为的详细信息，请参见[锁定统计信息的行为](/statistics.md#behaviors-of-locking-statistics)。

## 语法图

```ebnf+diagram
LockStatsStmt ::=
    'LOCK' 'STATS' (TableNameList) | (TableName 'PARTITION' PartitionNameList)

TableNameList ::=
    TableName (',' TableName)*

TableName ::=
    Identifier ( '.' Identifier )?

PartitionNameList ::=
    Identifier ( ',' Identifier )*
```

## 示例

创建表 `t` 并向其中插入数据。当表 `t` 的统计信息未被锁定时，`ANALYZE` 语句可以成功执行。

```sql
mysql> CREATE TABLE t(a INT, b INT);
Query OK, 0 rows affected (0.03 sec)

mysql> INSERT INTO t VALUES (1,2), (3,4), (5,6), (7,8);
Query OK, 4 rows affected (0.00 sec)
Records: 4  Duplicates: 0  Warnings: 0

mysql> ANALYZE TABLE t;
Query OK, 0 rows affected, 1 warning (0.02 sec)

mysql> SHOW WARNINGS;
+-------+------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Level | Code | Message                                                                                                                                                                                                               |
+-------+------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Note  | 1105 | Analyze use auto adjusted sample rate 1.000000 for table test.t, reason to use this rate is "Row count in stats_meta is much smaller compared with the row count got by PD, use min(1, 15000/4) as the sample-rate=1" |
+-------+------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

锁定表 `t` 的统计信息并执行 `ANALYZE`。从 `SHOW STATS_LOCKED` 的输出可以看到表 `t` 的统计信息已被锁定。警告信息显示 `ANALYZE` 语句已跳过表 `t`。

```sql
mysql> LOCK STATS t;
Query OK, 0 rows affected (0.00 sec)

mysql> SHOW STATS_LOCKED;
+---------+------------+----------------+--------+
| Db_name | Table_name | Partition_name | Status |
+---------+------------+----------------+--------+
| test    | t          |                | locked |
+---------+------------+----------------+--------+
1 row in set (0.01 sec)

mysql> ANALYZE TABLE t;
Query OK, 0 rows affected, 2 warnings (0.00 sec)

mysql> SHOW WARNINGS;
+---------+------+-----------------------------------------------------------------------------------------------------------------------------------------+
| Level   | Code | Message                                                                                                                                 |
+---------+------+-----------------------------------------------------------------------------------------------------------------------------------------+
| Note    | 1105 | Analyze use auto adjusted sample rate 1.000000 for table test.t, reason to use this rate is "use min(1, 110000/8) as the sample-rate=1" |
| Warning | 1105 | skip analyze locked table: test.t                                                                                                       |
+---------+------+-----------------------------------------------------------------------------------------------------------------------------------------+
2 rows in set (0.00 sec)
```

此外，你还可以使用 `LOCK STATS` 锁定分区的统计信息。例如：

创建分区表 `t` 并向其中插入数据。当分区 `p1` 的统计信息未被锁定时，`ANALYZE` 语句可以成功执行。

```sql
mysql> CREATE TABLE t(a INT, b INT) PARTITION BY RANGE (a) (PARTITION p0 VALUES LESS THAN (10), PARTITION p1 VALUES LESS THAN (20), PARTITION p2 VALUES LESS THAN (30));
Query OK, 0 rows affected (0.03 sec)

mysql> INSERT INTO t VALUES (1,2), (3,4), (5,6), (7,8);
Query OK, 4 rows affected (0.00 sec)
Records: 4  Duplicates: 0  Warnings: 0

mysql> ANALYZE TABLE t;
Query OK, 0 rows affected, 6 warning (0.02 sec)

mysql> SHOW WARNINGS;
+---------+------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Level   | Code | Message                                                                                                                                                                                                                              |
+---------+------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Warning | 1105 | disable dynamic pruning due to t has no global stats                                                                                                                                                                                 |
| Note    | 1105 | Analyze use auto adjusted sample rate 1.000000 for table test.t's partition p0, reason to use this rate is "Row count in stats_meta is much smaller compared with the row count got by PD, use min(1, 15000/4) as the sample-rate=1" |
| Warning | 1105 | disable dynamic pruning due to t has no global stats                                                                                                                                                                                 |
| Note    | 1105 | Analyze use auto adjusted sample rate 1.000000 for table test.t's partition p1, reason to use this rate is "TiDB assumes that the table is empty, use sample-rate=1"                                                                 |
| Warning | 1105 | disable dynamic pruning due to t has no global stats                                                                                                                                                                                 |
| Note    | 1105 | Analyze use auto adjusted sample rate 1.000000 for table test.t's partition p2, reason to use this rate is "TiDB assumes that the table is empty, use sample-rate=1"                                                                 |
+---------+------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
6 rows in set (0.01 sec)
```

锁定分区 `p1` 的统计信息并执行 `ANALYZE`。警告信息显示 `ANALYZE` 语句已跳过分区 `p1`。

```sql
mysql> LOCK STATS t PARTITION p1;
Query OK, 0 rows affected (0.00 sec)

mysql> SHOW STATS_LOCKED;
+---------+------------+----------------+--------+
| Db_name | Table_name | Partition_name | Status |
+---------+------------+----------------+--------+
| test    | t          | p1             | locked |
+---------+------------+----------------+--------+
1 row in set (0.00 sec)

mysql> ANALYZE TABLE t PARTITION p1;
Query OK, 0 rows affected, 2 warnings (0.01 sec)

mysql> SHOW WARNINGS;
+---------+------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Level   | Code | Message                                                                                                                                                              |
+---------+------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Note    | 1105 | Analyze use auto adjusted sample rate 1.000000 for table test.t's partition p1, reason to use this rate is "TiDB assumes that the table is empty, use sample-rate=1" |
| Warning | 1105 | skip analyze locked table: test.t partition (p1)                                                                                                                     |
+---------+------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------+
2 rows in set (0.00 sec)
```

有关解锁统计信息的信息，请参见 [UNLOCK STATS](/sql-statements/sql-statement-unlock-stats.md)。

## MySQL 兼容性

该语句是 TiDB 对 MySQL 语法的扩展。

## 另请参阅

* [统计信息](/statistics.md#lock-statistics)
* [UNLOCK STATS](/sql-statements/sql-statement-unlock-stats.md)
* [SHOW STATS_LOCKED](/sql-statements/sql-statement-show-stats-locked.md)
