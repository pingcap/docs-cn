---
title: SHOW STATS_META
summary: TiDB 数据库中 SHOW STATS_META 的使用概述。
---

# SHOW STATS_META

你可以使用 `SHOW STATS_META` 来查看表中有多少行以及该表中有多少行被更改。使用此语句时，你可以通过 `ShowLikeOrWhere` 子句过滤所需信息。

目前，`SHOW STATS_META` 语句输出 6 列：

| 列名 | 描述 |
| -------- | ------------- |
| db_name  | 数据库名称 |
| table_name | 表名 |
| partition_name | 分区名称 |
| update_time | 最后更新时间 |
| modify_count | 修改的行数 |
| row_count | 总行数 |

> **注意：**
>
> `update_time` 是在 TiDB 根据 DML 语句更新 `modify_count` 和 `row_count` 字段时更新的。因此 `update_time` 不是 `ANALYZE` 语句的最后执行时间。

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
+---------+------------+----------------+---------------------+--------------+-----------+
| Db_name | Table_name | Partition_name | Update_time         | Modify_count | Row_count |
+---------+------------+----------------+---------------------+--------------+-----------+
| test    | t0         |                | 2020-05-15 16:58:00 |            0 |         0 |
| test    | t1         |                | 2020-05-15 16:58:04 |            0 |         0 |
| test    | t2         |                | 2020-05-15 16:58:11 |            0 |         0 |
| test    | s          |                | 2020-05-22 19:46:43 |            0 |         0 |
| test    | t          |                | 2020-05-25 12:04:21 |            0 |         0 |
+---------+------------+----------------+---------------------+--------------+-----------+
5 rows in set (0.00 sec)
```

```sql
SHOW STATS_META WHERE table_name = 't2';
```

```sql
+---------+------------+----------------+---------------------+--------------+-----------+
| Db_name | Table_name | Partition_name | Update_time         | Modify_count | Row_count |
+---------+------------+----------------+---------------------+--------------+-----------+
| test    | t2         |                | 2020-05-15 16:58:11 |            0 |         0 |
+---------+------------+----------------+---------------------+--------------+-----------+
1 row in set (0.00 sec)
```

## MySQL 兼容性

该语句是 TiDB 对 MySQL 语法的扩展。

## 另请参阅

* [ANALYZE](/sql-statements/sql-statement-analyze-table.md)
* [统计信息简介](/statistics.md)
