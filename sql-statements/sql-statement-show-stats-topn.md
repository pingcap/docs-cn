---
title: SHOW STATS_TOPN
summary: TiDB 数据库中 SHOW STATS_TOPN 的使用概览。
---

# SHOW STATS_TOPN

`SHOW STATS_TOPN` 语句显示[统计信息](/statistics.md)中的 Top-N 信息。

目前，`SHOW STATS_TOPN` 语句返回以下列：

| 列名 | 描述 |
| ---- | ----|
| `Db_name` | 数据库名称 |
| `Table_name` | 表名 |
| `Partition_name` | 分区名称 |
| `Column_name` | 列名（当 `is_index` 为 `0` 时）或索引名（当 `is_index` 为 `1` 时） |
| `Is_index` | 是否为索引列 |
| `Value` | 该列的值 |
| `Count` | 该值出现的次数 |

## 语法

```ebnf+diagram
ShowStatsTopnStmt ::=
    "SHOW" "STATS_TOPN" ShowLikeOrWhere?

ShowLikeOrWhere ::=
    "LIKE" SimpleExpr
|   "WHERE" Expression
```

## 示例

```sql
SHOW STATS_TOPN WHERE Table_name='t';
```

```
+---------+------------+----------------+-------------+----------+--------------------------+-------+
| Db_name | Table_name | Partition_name | Column_name | Is_index | Value                    | Count |
+---------+------------+----------------+-------------+----------+--------------------------+-------+
| test    | t          |                | a           |        0 | 2023-12-27 00:00:00      |     1 |
| test    | t          |                | a           |        0 | 2023-12-28 00:00:00      |     1 |
| test    | t          |                | ia          |        1 | (NULL, 2)                |     1 |
| test    | t          |                | ia          |        1 | (NULL, 4)                |     1 |
| test    | t          |                | ia          |        1 | (2023-12-27 00:00:00, 1) |     1 |
| test    | t          |                | ia          |        1 | (2023-12-28 00:00:00, 3) |     1 |
+---------+------------+----------------+-------------+----------+--------------------------+-------+
6 rows in set (0.00 sec)
```

## MySQL 兼容性

此语句是 TiDB 对 MySQL 语法的扩展。

## 另请参阅

* [`ANALYZE`](/sql-statements/sql-statement-analyze-table.md)
* [统计信息简介](/statistics.md)
