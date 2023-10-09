---
title: SHOW STATS_LOCKED
summary: An overview of the usage of SHOW STATS_LOCKED for the TiDB database.
---

# SHOW STATS_LOCKED

`SHOW STATS_LOCKED` shows the tables whose statistics are locked.

> **Warning:**
>
> Locking statistics is an experimental feature for the current version. It is not recommended to use it in the production environment.

## Synopsis

```ebnf+diagram
ShowStatsLockedStmt ::= 'SHOW' 'STATS_LOCKED' ShowLikeOrWhereOpt

ShowLikeOrWhereOpt ::= 'LIKE' SimpleExpr | 'WHERE' Expression
```

## Examples

Create table `t`, and insert data into it. When the statistics of table `t` are not locked, the `ANALYZE` statement can be successfully executed.

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

Lock the statistics of table `t` and execute `SHOW STATS_LOCKED`. The output shows that the statistics of table `t` have been locked.

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
```

## MySQL compatibility

This statement is a TiDB extension to MySQL syntax.

## See also

* [Statistics](/statistics.md#lock-statistics)
* [LOCK STATS](/sql-statements/sql-statement-lock-stats.md)
* [UNLOCK STATS](/sql-statements/sql-statement-unlock-stats.md)
