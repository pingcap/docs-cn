---
title: SHOW STATS_HISTOGRAMS
summary: TiDB 数据库中 SHOW STATS_HISTOGRAMS 语句的简单说明。
---

# SHOW STATS_HISTOGRAMS

你可以使用 `SHOW STATS_HISTOGRAMS` 语句查看通过 [`ANALYZE` 语句](/sql-statements/sql-statement-analyze-table.md)收集的直方图信息，该内容是数据库[常规统计信息](/statistics.md)的一部分。

目前，`SHOW STATS_HISTOGRAMS` 语句返回以下列：

| 列名 | 说明            |
| -------- | ------------- |
| `Db_name`  |  数据库名    |
| `Table_name` | 表名 |
| `Partition_name` | 分区名 |
| `Column_name` | 取决于 `Is_index` 值：`Is_index` 为 `0` 时显示列名，为 `1` 时显示索引名 |
| `Is_index` | 是否是索引列 |
| `Update_time` | 更新时间 |
| `Distinct_count` | 不同值数量 |
| `Null_count` | `NULL` 的数量 |
| `Avg_col_size` | 列平均长度 |
| `Correlation` | 该列与整型主键的皮尔逊系数，表示两列之间的关联程度 |
| `Load_status` | 加载状态，例如 `allEvicted` 和 `allLoaded` |
| `Total_mem_usage` | 总内存占用 |
| `Hist_mem_usage` | 历史内存占用 |
| `Topn_mem_usage` | `TopN` 内存占用 |
| `Cms_mem_usage` | CMS 内存占用 |

## 语法图

```ebnf+diagram
ShowStatsHistogramsStmt ::=
    "SHOW" "STATS_HISTOGRAMS" ShowLikeOrWhere?

ShowLikeOrWhere ::=
    "LIKE" SimpleExpr
|   "WHERE" Expression
```

## 示例

```sql
SHOW STATS_HISTOGRAMS;
```

```sql
+---------+------------+----------------+-------------+----------+---------------------+----------------+------------+--------------+-------------+
| Db_name | Table_name | Partition_name | Column_name | Is_index | Update_time         | Distinct_count | Null_count | Avg_col_size | Correlation |
+---------+------------+----------------+-------------+----------+---------------------+----------------+------------+--------------+-------------+
| test    | t          |                | a           |        0 | 2020-05-25 19:20:00 |              7 |          0 |            1 |           1 |
| test    | t2         |                | a           |        0 | 2020-05-25 19:20:01 |              6 |          0 |            8 |           0 |
| test    | t2         |                | b           |        0 | 2020-05-25 19:20:01 |              6 |          0 |         1.67 |           1 |
+---------+------------+----------------+-------------+----------+---------------------+----------------+------------+--------------+-------------+
3 rows in set (0.00 sec)
```

```sql
SHOW STATS_HISTOGRAMS WHERE table_name = 't2';
```

```sql
+---------+------------+----------------+-------------+----------+---------------------+----------------+------------+--------------+-------------+
| Db_name | Table_name | Partition_name | Column_name | Is_index | Update_time         | Distinct_count | Null_count | Avg_col_size | Correlation |
+---------+------------+----------------+-------------+----------+---------------------+----------------+------------+--------------+-------------+
| test    | t2         |                | b           |        0 | 2020-05-25 19:20:01 |              6 |          0 |         1.67 |           1 |
| test    | t2         |                | a           |        0 | 2020-05-25 19:20:01 |              6 |          0 |            8 |           0 |
+---------+------------+----------------+-------------+----------+---------------------+----------------+------------+--------------+-------------+
2 rows in set (0.00 sec)
```

## MySQL 兼容性

该语句是 TiDB 对 MySQL 语法的扩展。

## 另请参阅

* [`ANALYZE`](/sql-statements/sql-statement-analyze-table.md)
* [常规统计信息](/statistics.md)
