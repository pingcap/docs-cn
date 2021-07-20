---
title: SHOW ANALYZE STATUS
summary: An overview of the usage of SHOW ANALYZE STATUS for the TiDB database.
aliases: ['/docs/dev/sql-statements/sql-statement-show-analyze-status/']
---

# SHOW ANALYZE STATUS

The `SHOW ANALYZE STATUS` statement shows the statistics collection tasks being executed by TiDB and a limited number of historical task records.

## Synopsis

**ShowStmt:**

![ShowStmt](/media/sqlgram/ShowStmt.png)

**ShowTargetFilterable:**

![ShowTargetFilterable](/media/sqlgram/ShowTargetFilterable.png)

## Examples

{{< copyable "sql" >}}

```sql
create table t(x int, index idx(x)) partition by hash(x) partition 4;
analyze table t;
show analyze status;
```

```sql
+--------------+------------+----------------+-------------------+----------------+---------------------+----------+
| Table_schema | Table_name | Partition_name | Job_info          | Processed_rows | Start_time          | State    |
+--------------+------------+----------------+-------------------+----------------+---------------------+----------+
| test         | t          | p1             | analyze columns   |              0 | 2020-05-25 17:23:55 | finished |
| test         | t          | p0             | analyze columns   |              0 | 2020-05-25 17:23:55 | finished |
| test         | t          | p0             | analyze index idx |              0 | 2020-05-25 17:23:55 | finished |
| test         | t          | p1             | analyze index idx |              0 | 2020-05-25 17:23:55 | finished |
| test         | t          | p2             | analyze index idx |              0 | 2020-05-25 17:23:55 | finished |
| test         | t          | p3             | analyze index idx |              0 | 2020-05-25 17:23:55 | finished |
| test         | t          | p3             | analyze columns   |              0 | 2020-05-25 17:23:55 | finished |
| test         | t          | p2             | analyze columns   |              0 | 2020-05-25 17:23:55 | finished |
+--------------+------------+----------------+-------------------+----------------+---------------------+----------+
8 rows in set (0.00 sec)
```

## MySQL compatibility

This statement is a TiDB extension to MySQL syntax.

## See also

* [ANALYZE_STATUS table](/information-schema/information-schema-analyze-status.md)