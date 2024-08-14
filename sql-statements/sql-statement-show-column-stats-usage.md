---
title: SHOW COLUMN_STATS_USAGE
summary: TiDB 数据库中 SHOW COLUMN_STATS_USAGE 的使用概况。
---

# SHOW COLUMN_STATS_USAGE

`SHOW COLUMN_STATS_USAGE` 语句显示列统计信息的最近一次使用时间和收集时间。你还可以使用该语句来查看 `PREDICATE COLUMNS` 和已收集统计信息的列。

目前，`SHOW COLUMN_STATS_USAGE` 语句返回以下列：

| 列名 | 说明            |
| -------- | ------------- |
| `Db_name`  |  数据库名   |
| `Table_name` | 表名 |
| `Partition_name` | 分区名 |
| `Column_name` | 列名 |
| `Last_used_at` | 最近一次将列统计信息用于查询优化的时间 |
| `Last_analyzed_at` | 最近一次收集列统计信息的时间 |

## 语法图

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

该语句是 TiDB 对 MySQL 语法的扩展。

## 另请参阅

* [`ANALYZE`](/sql-statements/sql-statement-analyze-table.md)
* [常规统计信息](/statistics.md)