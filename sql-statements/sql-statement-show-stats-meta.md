---
title: SHOW STATS_META
summary: TiDB 数据库中 SHOW STATS_META 语句的简单说明。
aliases: ['/docs-cn/dev/sql-statements/sql-statement-show-stats-meta/']
---

# SHOW STATS_META

你可以通过 `SHOW STATS_META` 来查看表的总行数以及修改的行数等信息，可以通过 ShowLikeOrWhere 来筛选需要的信息。

目前 `SHOW STATS_META` 会输出以下列：

| 列名 | 说明            |
| -------- | ------------- |
| Db_name  |  数据库名    |
| Table_name | 表名 |
| Partition_name| 分区名 |
| Update_time | 更新时间 |
| Modify_count | 修改的行数 |
| Row_count | 总行数 |
| Last_analyze_time | 表上次被分析的时间 |

> **注意：**
>
> 在 TiDB 根据 DML 语句自动更新总行数以及修改的行数时，`update_time` 也会被更新，因此并不能认为 `update_time` 是最近一次发生 Analyze 的时间。

## 语法图

```ebnf+diagram
ShowStatsMetaStmt ::=
    "SHOW" "STATS_META" ShowLikeOrWhere?

ShowLikeOrWhere ::=
    "LIKE" SimpleExpr
|   "WHERE" Expression
```

## 示例

```sql
SHOW STATS_META;
```

```sql
+---------+------------+----------------+---------------------+--------------+-----------+---------------------+
| Db_name | Table_name | Partition_name | Update_time         | Modify_count | Row_count | Last_analyze_time   |
+---------+------------+----------------+---------------------+--------------+-----------+---------------------+
| test    | t0         |                | 2025-07-27 16:58:00 |            0 |         0 | 2025-07-27 16:58:00 |
| test    | t1         |                | 2025-07-27 16:58:04 |            0 |         0 | 2025-07-27 16:58:04 |
| test    | t2         |                | 2025-07-27 16:58:11 |            0 |         0 | 2025-07-27 16:58:11 |
| test    | s          |                | 2025-07-27 19:46:43 |            0 |         0 | 2025-07-27 19:46:43 |
| test    | t          |                | 2025-07-27 12:04:21 |            0 |         0 | 2025-07-27 12:04:21 |
+---------+------------+----------------+---------------------+--------------+-----------+---------------------+
5 rows in set (0.00 sec)
```

```sql
SHOW STATS_META WHERE table_name = 't2';
```

```sql
+---------+------------+----------------+---------------------+--------------+-----------+---------------------+
| Db_name | Table_name | Partition_name | Update_time         | Modify_count | Row_count | Last_analyze_time   |
+---------+------------+----------------+---------------------+--------------+-----------+---------------------+
| test    | t2         |                | 2025-07-27 16:58:11 |            0 |         0 | 2025-07-27 16:58:11 |
+---------+------------+----------------+---------------------+--------------+-----------+---------------------+
1 row in set (0.00 sec)
```

## MySQL 兼容性

该语句是 TiDB 对 MySQL 语法的扩展。

## 另请参阅

* [`ANALYZE`](/sql-statements/sql-statement-analyze-table.md)
* [常规统计信息](/statistics.md)
