---
title: SHOW TABLE DISTRIBUTION
summary: 介绍 TiDB 数据库中 SHOW TABLE DISTRIBUTION 的使用概况。
---

# SHOW TABLE DISTRIBUTION

`SHOW TABLE DISTRIBUTION` 语句用于显示指定表的 Region 分布情况。

## 语法图

```ebnf+diagram
ShowTableDistributionStmt ::=
    "SHOW" "TABLE" "DISTRIBUTION" TableName

TableName ::=
    (SchemaName ".")? Identifier
```

## 示例

显示当前表 `t1` 的 Region 分布情况：

```sql
SHOW TABLE DISTRIBUTION t1;
```

```
+--------+----------+-------+----------------+--------+----------------+-----------+---------------------+---------------------+---------------------+
| Job_ID | Database | Table | Partition_List | Engine | Rule           | Status    | Create_Time         | Start_Time          | Finish_Time         |
+--------+----------+-------+----------------+--------+----------------+-----------+---------------------+---------------------+---------------------+
|    100 | test     | t1    | NULL           | tikv   | leader-scatter | finished  | 2025-04-24 16:09:55 | 2025-04-24 16:09:55 | 2025-04-24 17:09:59 |
|    101 | test     | t2    | NULL           | tikv   | learner-scatter| cancelled | 2025-05-08 15:33:29 | 2025-05-08 15:33:29 | 2025-05-08 15:33:37 |
|    102 | test     | t5    | p1,p2          | tikv   | peer-scatter   | cancelled | 2025-05-21 15:32:44 | 2025-05-21 15:32:47 | 2025-05-21 15:32:47 |
+--------+----------+-------+----------------+--------+----------------+-----------+---------------------+---------------------+---------------------+
```

## MySQL 兼容性

该语句是 TiDB 对 MySQL 语法的扩展。

## 另请参阅

- [`DISTRIBUTE TABLE`](/sql-statements/sql-statement-distribute-table.md)
- [`SHOW DISTRIBUTION JOBS`](/sql-statements/sql-statement-show-distribution-jobs.md)