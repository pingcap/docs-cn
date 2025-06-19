---
title: ANALYZE_STATUS
summary: 了解 `ANALYZE_STATUS` information_schema 表。
---

# ANALYZE_STATUS

`ANALYZE_STATUS` 表提供了正在运行的统计信息收集任务和有限数量的历史任务的信息。

从 TiDB v6.1.0 开始，`ANALYZE_STATUS` 表支持显示集群级别的任务。即使在 TiDB 重启后，你仍然可以通过此表查看重启前的任务记录。在 TiDB v6.1.0 之前，`ANALYZE_STATUS` 表只能显示实例级别的任务，且任务记录会在 TiDB 重启后被清除。

从 TiDB v6.1.0 开始，你可以通过系统表 `mysql.analyze_jobs` 查看最近 7 天的历史任务。

```sql
USE information_schema;
DESC analyze_status;
```

```sql
+----------------------+---------------------+------+------+---------+-------+
| Field                | Type                | Null | Key  | Default | Extra |
+----------------------+---------------------+------+------+---------+-------+
| TABLE_SCHEMA         | varchar(64)         | YES  |      | NULL    |       |
| TABLE_NAME           | varchar(64)         | YES  |      | NULL    |       |
| PARTITION_NAME       | varchar(64)         | YES  |      | NULL    |       |
| JOB_INFO             | longtext            | YES  |      | NULL    |       |
| PROCESSED_ROWS       | bigint(64) unsigned | YES  |      | NULL    |       |
| START_TIME           | datetime            | YES  |      | NULL    |       |
| END_TIME             | datetime            | YES  |      | NULL    |       |
| STATE                | varchar(64)         | YES  |      | NULL    |       |
| FAIL_REASON          | longtext            | YES  |      | NULL    |       |
| INSTANCE             | varchar(512)        | YES  |      | NULL    |       |
| PROCESS_ID           | bigint(64) unsigned | YES  |      | NULL    |       |
| REMAINING_SECONDS    | bigint(64) unsigned | YES  |      | NULL    |       |
| PROGRESS             | varchar(20)         | YES  |      | NULL    |       |
| ESTIMATED_TOTAL_ROWS | bigint(64) unsigned | YES  |      | NULL    |       |
+----------------------+---------------------+------+------+---------+-------+
14 rows in set (0.00 sec)
```

{{< copyable "sql" >}}

```sql
SELECT * FROM information_schema.analyze_status;
```

```sql
+--------------+------------+----------------+--------------------------------------------------------------------+----------------+---------------------+---------------------+----------+-------------+----------------+------------+----------------------+----------+-----------------------+
| TABLE_SCHEMA | TABLE_NAME | PARTITION_NAME | JOB_INFO                                                           | PROCESSED_ROWS | START_TIME          | END_TIME            | STATE    | FAIL_REASON | INSTANCE       | PROCESS_ID | REMAINING_SECONDS    | PROGRESS | ESTIMATED_TOTAL_ROWS  |
+--------------+------------+----------------+--------------------------------------------------------------------+----------------+---------------------+---------------------+----------+-------------+----------------+------------+----------------------+----------+-----------------------+
| test         | t          | p1             | analyze table all columns with 256 buckets, 500 topn, 1 samplerate |              0 | 2022-05-27 11:30:12 | 2022-05-27 11:30:12 | finished |        NULL | 127.0.0.1:4000 | NULL       | NULL                 | NULL     |                  NULL |
| test         | t          | p0             | analyze table all columns with 256 buckets, 500 topn, 1 samplerate |              0 | 2022-05-27 11:30:12 | 2022-05-27 11:30:12 | finished |        NULL | 127.0.0.1:4000 | NULL       | NULL                 | NULL     |                  NULL |
| test         | t          | p1             | analyze index idx                                                  |              0 | 2022-05-27 11:29:46 | 2022-05-27 11:29:46 | finished |        NULL | 127.0.0.1:4000 | NULL       | NULL                 | NULL     |                  NULL |
| test         | t          | p0             | analyze index idx                                                  |              0 | 2022-05-27 11:29:46 | 2022-05-27 11:29:46 | finished |        NULL | 127.0.0.1:4000 | NULL       | NULL                 | NULL     |                  NULL |
| test         | t          | p1             | analyze columns                                                    |              0 | 2022-05-27 11:29:46 | 2022-05-27 11:29:46 | finished |        NULL | 127.0.0.1:4000 | NULL       | NULL                 | NULL     |                  NULL |
| test         | t          | p0             | analyze columns                                                    |              0 | 2022-05-27 11:29:46 | 2022-05-27 11:29:46 | finished |        NULL | 127.0.0.1:4000 | NULL       | NULL                 | NULL     |                  NULL |
| test         | t          | p1             | analyze table all columns with 256 buckets, 500 topn, 1 samplerate |        1000000 | 2022-05-27 11:30:12 | 2022-05-27 11:40:12 | running  |        NULL | 127.0.0.1:4000 | 690208308  | 600s                 | 0.25     | 4000000               |
+--------------+------------+----------------+--------------------------------------------------------------------+----------------+---------------------+---------------------+----------+-------------+----------------+------------+----------------------+----------+-----------------------+
6 rows in set (0.00 sec)
```

`ANALYZE_STATUS` 表中的字段说明如下：

* `TABLE_SCHEMA`：表所属的数据库名称。
* `TABLE_NAME`：表名。
* `PARTITION_NAME`：分区表的分区名称。
* `JOB_INFO`：`ANALYZE` 任务的信息。如果分析的是索引，该信息会包含索引名称。当 `tidb_analyze_version = 2` 时，该信息会包含采样率等配置项。
* `PROCESSED_ROWS`：已处理的行数。
* `START_TIME`：`ANALYZE` 任务的开始时间。
* `END_TIME`：`ANALYZE` 任务的结束时间。
* `STATE`：`ANALYZE` 任务的执行状态。其值可以是 `pending`、`running`、`finished` 或 `failed`。
* `FAIL_REASON`：任务失败的原因。如果执行成功，该值为 `NULL`。
* `INSTANCE`：执行任务的 TiDB 实例。
* `PROCESS_ID`：执行任务的进程 ID。
* `REMAINING_SECONDS`：任务完成的预计剩余时间（以秒为单位）。
* `PROGRESS`：任务的进度。
* `ESTIMATED_TOTAL_ROWS`：任务需要分析的总行数。

## 另请参阅

- [`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md)
- [`SHOW ANALYZE STATUS`](/sql-statements/sql-statement-show-analyze-status.md)
