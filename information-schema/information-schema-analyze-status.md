---
title: ANALYZE_STATUS
summary: Learn the `ANALYZE_STATUS` information_schema table.
---

# ANALYZE_STATUS

The `ANALYZE_STATUS` table provides information about the running tasks that collect statistics and a limited number of history tasks.

Starting from TiDB v6.1.0, the `ANALYZE_STATUS` table supports showing cluster-level tasks. Even after a TiDB restart, you can still view task records before the restart using this table. Before TiDB v6.1.0, the `ANALYZE_STATUS` table can only show instance-level tasks, and task records are cleared after a TiDB restart.

Starting from TiDB v6.1.0, you can view the history tasks within the last 7 days through the system table `mysql.analyze_jobs`.

{{< copyable "sql" >}}

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

Fields in the `ANALYZE_STATUS` table are described as follows:

* `TABLE_SCHEMA`: The name of the database to which the table belongs.
* `TABLE_NAME`: The name of the table.
* `PARTITION_NAME`: The name of the partitioned table.
* `JOB_INFO`: The information of the `ANALYZE` task. If an index is analyzed, this information will include the index name. When `tidb_analyze_version = 2`, this information will include configuration items such as sample rate.
* `PROCESSED_ROWS`: The number of rows that have been processed.
* `START_TIME`: The start time of the `ANALYZE` task.
* `END_TIME`: The end time of the `ANALYZE` task.
* `STATE`: The execution status of the `ANALYZE` task. Its value can be `pending`, `running`,`finished` or `failed`.
* `FAIL_REASON`: The reason why the task fails. If the execution is successful, the value is `NULL`.
* `INSTANCE`: The TiDB instance that executes the task.
* `PROCESS_ID`: The process ID that executes the task.
* `REMAINING_SECONDS`: The estimated time (in seconds) remaining for the task to complete.
* `PROGRESS`: The progress of the task.
* `ESTIMATED_TOTAL_ROWS`: The total rows that need to be analyzed by the task.
