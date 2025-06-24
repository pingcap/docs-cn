---
title: SHOW STATS_BUCKETS
summary: TiDB 数据库中 SHOW STATS_BUCKETS 的使用概述。
---

# SHOW STATS_BUCKETS

`SHOW STATS_BUCKETS` 语句显示[统计信息](/statistics.md)中的桶信息。

目前，`SHOW STATS_BUCKETS` 语句返回以下列：

| 列名 | 描述 |
| :-------- | :------------- |
| `Db_name` | 数据库名称 |
| `Table_name` | 表名 |
| `Partition_name` | 分区名称 |
| `Column_name` | 当 `is_index` 为 `0` 时表示列名，当 `is_index` 为 `1` 时表示索引名 |
| `Is_index` | 是否为索引列 |
| `Bucket_id` | 桶的 ID |
| `Count` | 落在该桶及之前所有桶中的值的数量 |
| `Repeats` | 最大值的出现次数 |
| `Lower_bound` | 最小值 |
| `Upper_bound` | 最大值 |
| `Ndv` | 桶中不同值的数量。由于该字段的值不准确，已被弃用且始终显示为 `0`。 |

## 语法

```ebnf+diagram
ShowStatsBucketsStmt ::=
    "SHOW" "STATS_BUCKETS" ShowLikeOrWhere?

ShowLikeOrWhere ::=
    "LIKE" SimpleExpr
|   "WHERE" Expression
```

## 示例

```sql
SHOW STATS_BUCKETS WHERE Table_name='t';
```

```
+---------+------------+----------------+-------------+----------+-----------+-------+---------+--------------------------+--------------------------+------+
| Db_name | Table_name | Partition_name | Column_name | Is_index | Bucket_id | Count | Repeats | Lower_Bound              | Upper_Bound              | Ndv  |
+---------+------------+----------------+-------------+----------+-----------+-------+---------+--------------------------+--------------------------+------+
| test    | t          |                | a           |        0 |         0 |     1 |       1 | 2023-12-27 00:00:00      | 2023-12-27 00:00:00      |    0 |
| test    | t          |                | a           |        0 |         1 |     2 |       1 | 2023-12-28 00:00:00      | 2023-12-28 00:00:00      |    0 |
| test    | t          |                | ia          |        1 |         0 |     1 |       1 | (NULL, 2)                | (NULL, 2)                |    0 |
| test    | t          |                | ia          |        1 |         1 |     2 |       1 | (NULL, 4)                | (NULL, 4)                |    0 |
| test    | t          |                | ia          |        1 |         2 |     3 |       1 | (2023-12-27 00:00:00, 1) | (2023-12-27 00:00:00, 1) |    0 |
| test    | t          |                | ia          |        1 |         3 |     4 |       1 | (2023-12-28 00:00:00, 3) | (2023-12-28 00:00:00, 3) |    0 |
+---------+------------+----------------+-------------+----------+-----------+-------+---------+--------------------------+--------------------------+------+
6 rows in set (0.00 sec)
```

## MySQL 兼容性

此语句是 TiDB 对 MySQL 语法的扩展。

## 另请参阅

* [`ANALYZE`](/sql-statements/sql-statement-analyze-table.md)
* [统计信息简介](/statistics.md)
