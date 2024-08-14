---
title: SHOW STATS_TOPN
summary: TiDB 数据库中 SHOW STATS_TOPN 的使用概况。
---

# SHOW STATS_TOPN

`SHOW STATS_TOPN` 语句显示[常规统计信息](/statistics.md)中的 Top-N 信息。

目前，`SHOW STATS_TOPN` 语句返回以下列：

| 列名 | 说明 |
| ---- | ----|
| `Db_name` | 数据库名 |
| `Table_name` | 表名 |
| `Partition_name` | 分区名 |
| `Column_name` | 取决于 `Is_index` 值：`Is_index` 为 `0` 时显示列名，为 `1` 时显示索引名 |
| `Is_index` | 是否是索引列 |
| `Value` | 该列的值 |
| `Count` | 值出现的次数 |

## 语法图

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

该语句是 TiDB 对 MySQL 语法的扩展。

## 另请参阅

* [`ANALYZE`](/sql-statements/sql-statement-analyze-table.md)
* [常规统计信息](/statistics.md)