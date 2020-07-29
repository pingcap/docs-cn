---
title: ANALYZE_STATUS
summary: 了解 information_schema 表 `ANALYZE_STATUS`。
---

# ANALYZE_STATUS

`ANALYZE_STATUS` 表提供正在执行的收集统计信息的任务以及有限条历史任务记录。

{{< copyable "sql" >}}

```sql
USE information_schema;
DESC analyze_status;
```

```sql
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

`STATE` 列表示特定 `ANALYZE` 任务的执行状态。其值可以是 `pending`、`running`、`finished` 或者 `failed`。

{{< copyable "sql" >}}

```sql
SELECT * FROM `ANALYZE_STATUS`;
```

```sql
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
