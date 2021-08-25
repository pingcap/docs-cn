---
title: SHOW STATS_META
summary: TiDB 数据库中 SHOW STATS_META 语句的简单说明。
---

# SHOW STATS_META

你可以通过 `SHOW STATS_META` 来查看表的总行数以及修改的行数等信息，可以通过 ShowLikeOrWhere 来筛选需要的信息。

目前 `SHOW STATS_META` 会输出 6 列，具体如下：

| 语法元素 | 说明            |
| -------- | ------------- |
| db_name  |  数据库名    |
| table_name | 表名 |
| partition_name| 分区名 |
| update_time | 更新时间 |
| modify_count | 修改的行数 |
| row_count | 总行数 |

> **注意：**
>
> 在 TiDB 根据 DML 语句自动更新总行数以及修改的行数时，`update_time` 也会被更新，因此并不能认为 `update_time` 是最近一次发生 Analyze 的时间。

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
show stats_meta;
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

{{< copyable "sql" >}}

```sql
show stats_meta where table_name = 't2';
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
* [统计信息介绍](/statistics.md)
