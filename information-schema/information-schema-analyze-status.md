---
title: ANALYZE_STATUS
summary: 了解 information_schema 表 `ANALYZE_STATUS`。
---

# ANALYZE_STATUS

`ANALYZE_STATUS` 表提供正在执行的收集统计信息的任务以及有限条历史任务记录。

从 TiDB v6.1.0 起，`ANALYZE_STATUS` 表显示集群级别的任务，且 TiDB 重启后仍能看到重启之前的任务记录。在 TiDB v6.1.0 之前，`ANALYZE_STATUS` 仅显示实例级别的任务，且 TiDB 重启后任务记录会被清空。

从 TiDB v6.1.0 起，可以通过系统表 `mysql.analyze_jobs` 查看过去 7 天内的历史任务记录。

{{< copyable "sql" >}}

```sql
USE information_schema;
DESC analyze_status;
```

```sql
+----------------------+---------------------+------+-----+---------+-------+
| Field                | Type                | Null | Key | Default | Extra |
+----------------------+---------------------+------+-----+---------+-------+
| TABLE_SCHEMA         | varchar(64)         | YES  |     | <null>  |       |
| TABLE_NAME           | varchar(64)         | YES  |     | <null>  |       |
| PARTITION_NAME       | varchar(64)         | YES  |     | <null>  |       |
| JOB_INFO             | longtext            | YES  |     | <null>  |       |
| PROCESSED_ROWS       | bigint(64) unsigned | YES  |     | <null>  |       |
| START_TIME           | datetime            | YES  |     | <null>  |       |
| END_TIME             | datetime            | YES  |     | <null>  |       |
| STATE                | varchar(64)         | YES  |     | <null>  |       |
| FAIL_REASON          | longtext            | YES  |     | <null>  |       |
| INSTANCE             | varchar(512)        | YES  |     | <null>  |       |
| PROCESS_ID           | bigint(64) unsigned | YES  |     | <null>  |       |
| Remaining_seconds    | bigint(64) unsigned | YES  |     | <null>  |       |
| Progress             | varchar(20)         | YES  |     | <null>  |       |
| Estimated_total_rows | bigint(64) unsigned | YES  |     | <null>  |       |
+----------------------+---------------------+------+-----+---------+-------+
11 rows in set (0.00 sec)
```

{{< copyable "sql" >}}

```sql
SELECT * FROM information_schema.analyze_status;
```

```sql
+--------------+------------+----------------+--------------------------------------------------------------------+----------------+---------------------+---------------------+----------+-------------+----------------+------------+----------------------+----------+-----------------------+-------------------------+--------------------------+
| TABLE_SCHEMA | TABLE_NAME | PARTITION_NAME | JOB_INFO | PROCESSED_ROWS | START_TIME | END_TIME | STATE | FAIL_REASON | INSTANCE | PROCESS_ID | Remaining_seconds | Progress | Estimated_total_rows |
+--------------+------------+----------------+--------------------------------------------------------------------+----------------+---------------------+---------------------+----------+-------------+----------------+------------+----------------------+----------+-----------------------+-------------------------+--------------------------+
| test | t | p1 | analyze table all columns with 256 buckets, 500 topn, 1 samplerate | 0 | 2022-05-27 11:30:12 | 2022-05-27 11:30:12 | finished | NULL | 127.0.0.1:4000 | NULL | NULL | NULL | NULL |
| test | t | p0 | analyze table all columns with 256 buckets, 500 topn, 1 samplerate | 0 | 2022-05-27 11:30:12 | 2022-05-27 11:30:12 | finished | NULL | 127.0.0.1:4000 | NULL | NULL | NULL | NULL |
| test | t | p1 | analyze index idx | 0 | 2022-05-27 11:29:46 | 2022-05-27 11:29:46 | finished | NULL | 127.0.0.1:4000 | NULL | NULL | NULL | NULL |
| test | t | p0 | analyze index idx | 0 | 2022-05-27 11:29:46 | 2022-05-27 11:29:46 | finished | NULL | 127.0.0.1:4000 | NULL | NULL | NULL | NULL |
| test | t | p1 | analyze columns | 0 | 2022-05-27 11:29:46 | 2022-05-27 11:29:46 | finished | NULL | 127.0.0.1:4000 | NULL | NULL | NULL | NULL |
| test | t | p0 | analyze columns | 0 | 2022-05-27 11:29:46 | 2022-05-27 11:29:46 | finished | NULL | 127.0.0.1:4000 | NULL | NULL | NULL | NULL |
+--------------+------------+----------------+--------------------------------------------------------------------+----------------+---------------------+---------------------+----------+-------------+----------------+------------+----------------------+----------+-----------------------+-------------------------+--------------------------+
6 rows in set (0.00 sec)
```

`ANALYZE_STATUS` 表中列的含义如下：

* `TABLE_SCHEMA`：表所属的数据库的名称。
* `TABLE_NAME`：表的名称。
* `PARTITION_NAME`：分区表的名称。
* `JOB_INFO`：`ANALYZE` 任务的信息。如果分析索引，该信息会包含索引名。当 `tidb_analyze_version =2` 时，该信息会包含采样率等配置项。
* `PROCESSED_ROWS`：已经处理的行数。
* `START_TIME`：`ANALYZE` 任务的开始时间。
* `END_TIME`：`ANALYZE` 任务的结束时间。
* `STATE`：`ANALYZE` 任务的执行状态。其值可以是 `pending`、`running`、`finished` 或者 `failed`。
* `FAIL_REASON`：任务失败的原因。如果执行成功则为 `NULL`。
* `INSTANCE`：执行任务的 TiDB 实例。
* `PROCESS_ID`：执行任务的 process ID。
* `Remaining_seconds`：表示作业预计还需要多少秒才能完成。
* `Progress`：表示作业的进度。
* `Estimated_total_rows`：表示需要分析的总行数。