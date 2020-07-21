---
title: ANALYZE_STATUS
summary: Learn the `ANALYZE_STATUS` information_schema table.
---

# ANALYZE_STATUS

The `ANALYZE_STATUS` table provides information about the running tasks that collect statistics and a limited number of history tasks.

{{< copyable "sql" >}}

```sql
USE information_schema;
DESC analyze_status;
```

```
+----------------+---------------------+------+------+---------+-------+
| Field          | Type                | Null | Key  | Default | Extra |
+----------------+---------------------+------+------+---------+-------+
| TABLE_SCHEMA   | varchar(64)         | YES  |      | NULL    |       |
| TABLE_NAME     | varchar(64)         | YES  |      | NULL    |       |
| PARTITION_NAME | varchar(64)         | YES  |      | NULL    |       |
| JOB_INFO       | varchar(64)         | YES  |      | NULL    |       |
| PROCESSED_ROWS | bigint(20) unsigned | YES  |      | NULL    |       |
| START_TIME     | datetime            | YES  |      | NULL    |       |
| STATE          | varchar(64)         | YES  |      | NULL    |       |
+----------------+---------------------+------+------+---------+-------+
7 rows in set (0.00 sec)
```

The `STATE` column shows the execution status of a specific `ANALYZE` task. Its value can be `pending`, `running`,`finished` or `failed`.

{{< copyable "sql" >}}

```sql
SELECT * FROM `ANALYZE_STATUS`;
```

```
+--------------+------------+----------------+-------------------+----------------+---------------------+----------+
| TABLE_SCHEMA | TABLE_NAME | PARTITION_NAME | JOB_INFO          | PROCESSED_ROWS | START_TIME          | STATE    |
+--------------+------------+----------------+-------------------+----------------+---------------------+----------+
| test         | t          |                | analyze index idx | 2              | 2019-06-21 19:51:14 | finished |
| test         | t          |                | analyze columns   | 2              | 2019-06-21 19:51:14 | finished |
| test         | t1         | p0             | analyze columns   | 0              | 2019-06-21 19:51:15 | finished |
| test         | t1         | p3             | analyze columns   | 0              | 2019-06-21 19:51:15 | finished |
| test         | t1         | p1             | analyze columns   | 0              | 2019-06-21 19:51:15 | finished |
| test         | t1         | p2             | analyze columns   | 1              | 2019-06-21 19:51:15 | finished |
+--------------+------------+----------------+-------------------+----------------+---------------------+----------+
6 rows in set
```