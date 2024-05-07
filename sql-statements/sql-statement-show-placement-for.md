---
title: SHOW PLACEMENT FOR
summary: TiDB 数据库中 SHOW PLACEMENT FOR 的使用概况。
---

# SHOW PLACEMENT FOR

`SHOW PLACEMENT FOR` 用于汇总所有放置策略 (placement policy)，并用统一的形式呈现特定表、数据库或分区的信息。

本语句返回结果中的 `Scheduling_State` 列标识了 Placement Driver (PD) 在当前对象上的调度进度，有以下可能的结果：

* `PENDING`: PD 没有进行调度。可能的原因之一是放置规则虽然语法上正确，但集群拓扑并不满足。比如指定 `FOLLOWERS=4` 但只有 3 个可用作 follower 的 TiKV 实例。
* `INPROGRESS`: PD 正在进行调度。
* `SCHEDULED`: PD 调度完成。

## 语法图

```ebnf+diagram
ShowStmt ::=
    "SHOW" "PLACEMENT" "FOR" ShowPlacementTarget

ShowPlacementTarget ::=
    DatabaseSym DBName
|   "TABLE" TableName
|   "TABLE" TableName "PARTITION" Identifier
```

## 示例

```sql
CREATE PLACEMENT POLICY p1 PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-west-1" FOLLOWERS=4;
use test;
ALTER DATABASE test PLACEMENT POLICY=p1;
CREATE TABLE t1 (a INT);
SHOW PLACEMENT FOR DATABASE test;
SHOW PLACEMENT FOR TABLE t1;
SHOW CREATE TABLE t1\G
CREATE TABLE t3 (a INT) PARTITION BY RANGE (a) (PARTITION p1 VALUES LESS THAN (10), PARTITION p2 VALUES LESS THAN (20));
SHOW PLACEMENT FOR TABLE t3 PARTITION p1\G
```

```sql
Query OK, 0 rows affected (0.02 sec)

Query OK, 0 rows affected (0.00 sec)

Query OK, 0 rows affected (0.01 sec)

+---------------+----------------------------------------------------------------------+------------------+
| Target        | Placement                                                            | Scheduling_State |
+---------------+----------------------------------------------------------------------+------------------+
| DATABASE test | PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-west-1" FOLLOWERS=4 | INPROGRESS       |
+---------------+----------------------------------------------------------------------+------------------+
1 row in set (0.00 sec)

+---------------+-------------+------------------+
| Target        | Placement   | Scheduling_State |
+---------------+-------------+------------------+
| TABLE test.t1 | FOLLOWERS=4 | INPROGRESS       |
+---------------+-------------+------------------+
1 row in set (0.00 sec)

***************************[ 1. row ]***************************
Table        | t1
Create Table | CREATE TABLE `t1` (
  `a` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin /*T![placement] PLACEMENT POLICY=`p1` */
1 row in set (0.00 sec)

***************************[ 1. row ]***************************
Target           | TABLE test.t3 PARTITION p1
Placement        | PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-west-1" FOLLOWERS=4
Scheduling_State | PENDING
1 row in set (0.00 sec)
```

## MySQL 兼容性

该语句是 TiDB 对 MySQL 语法的扩展。

## 另请参阅

* [Placement Rules in SQL](/placement-rules-in-sql.md)
* [SHOW PLACEMENT](/sql-statements/sql-statement-show-placement.md)
* [CREATE PLACEMENT POLICY](/sql-statements/sql-statement-create-placement-policy.md)
