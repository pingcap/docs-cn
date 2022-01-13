---
title: SHOW PLACEMENT FOR
summary: TiDB 数据库中 SHOW PLACEMENT FOR 的使用概况。
---

# SHOW PLACEMENT FOR

> **警告：**
>
> Placement Rules in SQL 是 TiDB 在 v5.3.0 中引入的实验特性，其语法在 GA 前可能会发生变化，还可能存在 bug。如果你知晓潜在的风险，可通过执行 `SET GLOBAL tidb_enable_alter_placement = 1;` 来开启该实验特性。

`SHOW PLACEMENT FOR` 用于汇总直接放置 (direct placement) 和放置策略 (placement policy) 中所有的放置选项，并为特定表、数据库或分区以规范形式呈现这些选项信息。

## 语法图

```ebnf+diagram
ShowStmt ::=
    "PLACEMENT" "FOR" ShowPlacementTarget

ShowPlacementTarget ::=
    DatabaseSym DBName
|   "TABLE" TableName
|   "TABLE" TableName "PARTITION" Identifier
```

## 示例

{{< copyable "sql" >}}

```sql
CREATE PLACEMENT POLICY p1 PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-west-1" FOLLOWERS=4;
use test;
ALTER DATABASE test PLACEMENT POLICY=p1;
CREATE TABLE t1 (a INT);
CREATE TABLE t2 (a INT) PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-west-1" FOLLOWERS=4;
SHOW PLACEMENT FOR DATABASE test;
SHOW PLACEMENT FOR TABLE t1;
SHOW CREATE TABLE t1\G
SHOW PLACEMENT FOR TABLE t2;
CREATE TABLE t3 (a INT) PARTITION BY RANGE (a) (PARTITION p1 VALUES LESS THAN (10), PARTITION p2 VALUES LESS THAN (20) FOLLOWERS=4);
SHOW PLACEMENT FOR TABLE t3 PARTITION p1;
SHOW PLACEMENT FOR TABLE t3 PARTITION p2;
```

```sql
Query OK, 0 rows affected (0.02 sec)

Query OK, 0 rows affected (0.00 sec)

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

*************************** 1. row ***************************
       Table: t1
Create Table: CREATE TABLE `t1` (
  `a` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin /*T![placement] PLACEMENT POLICY=`p1` */
1 row in set (0.00 sec)

+---------------+----------------------------------------------------------------------+------------------+
| Target        | Placement                                                            | Scheduling_State |
+---------------+----------------------------------------------------------------------+------------------+
| TABLE test.t2 | PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-west-1" FOLLOWERS=4 | INPROGRESS       |
+---------------+----------------------------------------------------------------------+------------------+
1 row in set (0.00 sec)

Query OK, 0 rows affected (0.14 sec)

+----------------------------+-----------------------------------------------------------------------+------------------+
| Target                     | Placement                                                             | Scheduling_State |
+----------------------------+-----------------------------------------------------------------------+------------------+
| TABLE test.t3 PARTITION p1 | PRIMARY_REGION="us-east-1" REGIONS="us-east-1,,us-west-1" FOLLOWERS=4 | INPROGRESS       |
+----------------------------+-----------------------------------------------------------------------+------------------+
1 row in set (0.00 sec)

+----------------------------+-------------+------------------+
| Target                     | Placement   | Scheduling_State |
+----------------------------+-------------+------------------+
| TABLE test.t3 PARTITION p2 | FOLLOWERS=4 | INPROGRESS       |
+----------------------------+-------------+------------------+
1 row in set (0.00 sec)
```

## MySQL 兼容性

该语句是 TiDB 对 MySQL 语法的扩展。

## 另请参阅

* [Placement Rules in SQL](/placement-rules-in-sql.md)
* [SHOW PLACEMENT](/sql-statements/sql-statement-show-placement.md)
* [CREATE PLACEMENT POLICY](/sql-statements/sql-statement-create-placement-policy.md)
