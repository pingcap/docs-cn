---
title: SHOW STATS_HISTOGRAMS
summary: TiDB 数据库中 SHOW HISTOGRAMS 语句的简单说明。
aliases: ['/docs-cn/dev/sql-statements/sql-statement-show-histograms/']
---

# SHOW STATS_HISTOGRAMS

你可以使用 `SHOW STATS_HISTOGRAMS` 语句查看统计信息中直方图的相关信息。

## 语法图

**ShowStmt**

![ShowStmt](/media/sqlgram/ShowStmt.png)

**ShowTargetFiltertable**

![ShowTargetFilterable](/media/sqlgram/ShowTargetFilterable.png)

**ShowLikeOrWhereOpt**

![ShowLikeOrWhereOpt](/media/sqlgram/ShowLikeOrWhereOpt.png)

## 示例

{{< copyable "sql" >}}

```sql
show stats_histograms;
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

{{< copyable "sql" >}}

```sql
show stats_histograms where table_name = 't2';
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

 `SHOW STATS_HISTOGRAMS`只会显示加载到内存中的统计信息，对于列的统计信息，当有查询条件涉及到该列时，tidb 才会将该列的统计信息加载到内存中。当展示结果中没有想要查看的列信息，可以使用where中带有待查看列的查询语句先执行一遍。例如，上述t2表中想要展示c列信息，可以先执行如下语句之后，在执行 `SHOW STATS_HISTOGRAMS`

```sql
select count(1) from t2 where c>'';
```

## MySQL 兼容性

该语句是 TiDB 对 MySQL 语法的扩展。

## 另请参阅

* [ANALYZE](/sql-statements/sql-statement-analyze-table.md)
* [统计信息介绍](/statistics.md)
