---
title: ADD TIDB\_STATS
summary: TiDB 数据库中 ADD TIDB\_STATS 的使用概况。
---

# ADD TIDB\_STATS

`ALTER TABLE.. ADD TIDB_STATS` 语句用于为指定表的指定列组合创建扩展统计信息。

## 语法图

**AddTiDBStatsStmt:**

![AddTiDBStatsStmt](/media/sqlgram/ExtendedStatistics.png)

**StatsType:**

![StatsType](/media/sqlgram/StatsType.png)

完整的 `ALTER TABLE` 语法图参见 [ALTER TABLE](/sql-statements/sql-statement-alter-table.md)。

## 示例

{{< copyable "sql" >}}

```sql
ALTER TABLE t ADD TIDB_STATS s1 correlation(a,b);
```

```sql
Query OK, 0 rows affected (0.01 sec)
```

{{< copyable "sql" >}}

```sql
SELECT * FROM mysql.stats_extended;
```

```sql
+------+------+----------+------------+-------+--------------------+--------+
| name | type | table_id | column_ids | stats | version            | status |
+------+------+----------+------------+-------+--------------------+--------+
| s1   |    2 |       94 | [1,2]      | NULL  | 420241592536793088 | 0      |
+------+------+----------+------------+-------+--------------------+--------+
1 row in set (0.00 sec)
```

## MySQL 兼容性

该语句是 TiDB 对 MySQL `ALTER TABLE` 语法的扩展。

## 另请参阅

* [ALTER TABLE](/sql-statements/sql-statement-alter-table.md)
* [扩展统计信息简介](/extended-statistics.md)
