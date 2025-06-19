---
title: SHOW COLUMN_STATS_USAGE
summary: TiDB 数据库中 SHOW COLUMN_STATS_USAGE 的使用概览。
---

# SHOW COLUMN_STATS_USAGE

`SHOW COLUMN_STATS_USAGE` 语句显示列统计信息的最后使用时间和收集时间。你还可以使用它来定位 `PREDICATE COLUMNS` 和已收集统计信息的列。

目前，`SHOW COLUMN_STATS_USAGE` 语句返回以下列：

| 列名 | 描述            |
| -------- | ------------- |
| `Db_name`  | 数据库名称    |
| `Table_name` | 表名 |
| `Partition_name` | 分区名称 |
| `Column_name` | 列名 |
| `Last_used_at` | 列统计信息在查询优化中最后一次使用的时间 |
| `Last_analyzed_at` | 列统计信息最后一次收集的时间 |

## 语法

```ebnf+diagram
ShowColumnStatsUsageStmt ::=
    "SHOW" "COLUMN_STATS_USAGE" ShowLikeOrWhere?

ShowLikeOrWhere ::=
    "LIKE" SimpleExpr
|   "WHERE" Expression
```

## 示例

```sql
SHOW COLUMN_STATS_USAGE;
```

```
+---------+------------+----------------+-------------+--------------+---------------------+
| Db_name | Table_name | Partition_name | Column_name | Last_used_at | Last_analyzed_at    |
+---------+------------+----------------+-------------+--------------+---------------------+
| test    | t1         |                | id          | NULL         | 2024-05-10 11:04:23 |
| test    | t1         |                | b           | NULL         | 2024-05-10 11:04:23 |
| test    | t1         |                | pad         | NULL         | 2024-05-10 11:04:23 |
| test    | t          |                | a           | NULL         | 2024-05-10 11:37:06 |
| test    | t          |                | b           | NULL         | 2024-05-10 11:37:06 |
+---------+------------+----------------+-------------+--------------+---------------------+
5 rows in set (0.00 sec)
```

## MySQL 兼容性

此语句是 TiDB 对 MySQL 语法的扩展。

## 另请参阅

* [`ANALYZE`](/sql-statements/sql-statement-analyze-table.md)
* [统计信息简介](/statistics.md)
