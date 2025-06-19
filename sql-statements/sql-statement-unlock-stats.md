---
title: UNLOCK STATS
summary: TiDB 数据库中 UNLOCK STATS 的使用概述。
---

# UNLOCK STATS

`UNLOCK STATS` 用于解锁表或多个表的统计信息。

## 语法概要

```ebnf+diagram
UnlockStatsStmt ::=
    'UNLOCK' 'STATS' (TableNameList | TableName 'PARTITION' PartitionNameList)

TableNameList ::=
    TableName (',' TableName)*

TableName ::=
    Identifier ( '.' Identifier )?

PartitionNameList ::=
    Identifier ( ',' Identifier )*
```

## 示例

参考 [LOCK STATS](/sql-statements/sql-statement-lock-stats.md) 中的示例创建表 `t` 并锁定其统计信息。

解锁表 `t` 的统计信息后，可以成功执行 `ANALYZE`。

```sql
mysql> UNLOCK STATS t;
Query OK, 0 rows affected (0.01 sec)

mysql> ANALYZE TABLE t;
Query OK, 0 rows affected, 1 warning (0.03 sec)

mysql> SHOW WARNINGS;
+-------+------+-----------------------------------------------------------------------------------------------------------------------------------------+
| Level | Code | Message                                                                                                                                 |
+-------+------+-----------------------------------------------------------------------------------------------------------------------------------------+
| Note  | 1105 | Analyze use auto adjusted sample rate 1.000000 for table test.t, reason to use this rate is "use min(1, 110000/8) as the sample-rate=1" |
+-------+------+-----------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

参考 [LOCK STATS](/sql-statements/sql-statement-lock-stats.md) 中的示例创建表 `t` 并锁定其分区 `p1` 的统计信息。

解锁分区 `p1` 的统计信息后，可以成功执行 `ANALYZE`。

```sql
mysql> UNLOCK STATS t PARTITION p1;
Query OK, 0 rows affected (0.00 sec)

mysql> ANALYZE TABLE t PARTITION p1;
Query OK, 0 rows affected, 1 warning (0.01 sec)

mysql> SHOW WARNINGS;
+-------+------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Level | Code | Message                                                                                                                                                              |
+-------+------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Note  | 1105 | Analyze use auto adjusted sample rate 1.000000 for table test.t's partition p1, reason to use this rate is "TiDB assumes that the table is empty, use sample-rate=1" |
+-------+------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

## MySQL 兼容性

此语句是 TiDB 对 MySQL 语法的扩展。

## 另请参阅

* [统计信息](/statistics.md#lock-statistics)
* [LOCK STATS](/sql-statements/sql-statement-lock-stats.md)
* [SHOW STATS_LOCKED](/sql-statements/sql-statement-show-stats-locked.md)
