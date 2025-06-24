---
title: SHOW ANALYZE STATUS
summary: TiDB 数据库中 SHOW ANALYZE STATUS 的使用概述。
---

# SHOW ANALYZE STATUS

`SHOW ANALYZE STATUS` 语句显示 TiDB 正在执行的统计信息收集任务和有限数量的历史任务记录。

从 TiDB v6.1.0 开始，`SHOW ANALYZE STATUS` 语句支持显示集群级别的任务。即使在 TiDB 重启后，你仍然可以使用此语句查看重启前的任务记录。在 TiDB v6.1.0 之前，`SHOW ANALYZE STATUS` 语句只能显示实例级别的任务，且任务记录会在 TiDB 重启后被清除。

从 TiDB v6.1.0 开始，你可以通过系统表 `mysql.analyze_jobs` 查看最近 7 天的历史任务。

从 TiDB v7.3.0 开始，你可以通过系统表 `mysql.analyze_jobs` 或 `SHOW ANALYZE STATUS` 查看当前 `ANALYZE` 任务的进度。

目前，`SHOW ANALYZE STATUS` 语句返回以下列：

| 列名            | 描述 |
| :--------------- | :------------- |
| `Table_schema`   | 数据库名 |
| `Table_name`     | 表名 |
| `Partition_name` | 分区名 |
| `Job_info`       | 任务信息。如果分析了索引，此信息将包括索引名。当 `tidb_analyze_version =2` 时，此信息将包括采样率等配置项。 |
| `Processed_rows` | 已分析的行数 |
| `Start_time`     | 任务开始时间 |
| `State`          | 任务状态，包括 `pending`、`running`、`finished` 和 `failed` |
| `Fail_reason`    | 任务失败的原因。如果执行成功，该值为 `NULL`。 |
| `Instance`       | 执行任务的 TiDB 实例 |
| `Process_id`     | 执行任务的进程 ID |

## 语法概要

```ebnf+diagram
ShowAnalyzeStatusStmt ::= 'SHOW' 'ANALYZE' 'STATUS' ShowLikeOrWhereOpt

ShowLikeOrWhereOpt ::= 'LIKE' SimpleExpr | 'WHERE' Expression
```

## 示例

```sql
mysql> create table t(x int, index idx(x)) partition by hash(x) partitions 2;
Query OK, 0 rows affected (0.69 sec)

mysql> set @@tidb_analyze_version = 1;
Query OK, 0 rows affected (0.00 sec)

mysql> analyze table t;
Query OK, 0 rows affected (0.20 sec)

mysql> show analyze status;
+--------------+------------+----------------+-------------------+----------------+---------------------+---------------------+----------+-------------+----------------+------------+------------------+----------+---------------------+
| Table_schema | Table_name | Partition_name | Job_info          | Processed_rows | Start_time          | End_time            | State    | Fail_reason | Instance       | Process_ID | Remaining_seconds| Progress | Estimated_total_rows|
+--------------+------------+----------------+-------------------+----------------+---------------------+---------------------+----------+-------------+----------------+------------+------------------+----------+---------------------+
| test         | t          | p1             | analyze index idx |              0 | 2022-05-27 11:29:46 | 2022-05-27 11:29:46 | finished | NULL        | 127.0.0.1:4000 | NULL       | NULL             | NULL     | NULL                |
| test         | t          | p0             | analyze index idx |              0 | 2022-05-27 11:29:46 | 2022-05-27 11:29:46 | finished | NULL        | 127.0.0.1:4000 | NULL       | NULL             | NULL     | NULL                |
| test         | t          | p1             | analyze columns   |              0 | 2022-05-27 11:29:46 | 2022-05-27 11:29:46 | finished | NULL        | 127.0.0.1:4000 | NULL       | NULL             | NULL     | NULL                |
| test         | t          | p0             | analyze columns   |              0 | 2022-05-27 11:29:46 | 2022-05-27 11:29:46 | finished | NULL        | 127.0.0.1:4000 | NULL       | NULL             | NULL     | NULL                |
| test         | t1         | p0             | analyze columns   |       28523259 | 2022-05-27 11:29:46 | 2022-05-27 11:29:46 | running  | NULL        | 127.0.0.1:4000 | 690208308  | 0s               | 0.9843   | 28978290            |
+--------------+------------+----------------+-------------------+----------------+---------------------+---------------------+----------+-------------+----------------+------------+------------------+----------+---------------------+
4 rows in set (0.01 sec)

mysql> set @@tidb_analyze_version = 2;
Query OK, 0 rows affected (0.00 sec)

mysql> analyze table t;
Query OK, 0 rows affected, 2 warnings (0.03 sec)

mysql> show analyze status;
+--------------+------------+----------------+--------------------------------------------------------------------+----------------+---------------------+---------------------+----------+-------------+----------------+------------+--------------------+----------+----------------------+
| Table_schema | Table_name | Partition_name | Job_info                                                           | Processed_rows | Start_time          | End_time            | State    | Fail_reason | Instance       | Process_ID | Remaining_seconds  | Progress | Estimated_total_rows |
+--------------+------------+----------------+--------------------------------------------------------------------+----------------+---------------------+---------------------+----------+-------------+----------------+------------+--------------------+----------+----------------------+
| test         | t          | p1             | analyze table all columns with 256 buckets, 500 topn, 1 samplerate |              0 | 2022-05-27 11:30:12 | 2022-05-27 11:30:12 | finished | NULL        | 127.0.0.1:4000 | NULL       | NULL               | NULL     | NULL                 |
| test         | t          | p0             | analyze table all columns with 256 buckets, 500 topn, 1 samplerate |              0 | 2022-05-27 11:30:12 | 2022-05-27 11:30:12 | finished | NULL        | 127.0.0.1:4000 | NULL       | NULL               | NULL     | NULL                 |
| test         | t          | p1             | analyze index idx                                                  |              0 | 2022-05-27 11:29:46 | 2022-05-27 11:29:46 | finished | NULL        | 127.0.0.1:4000 | NULL       | NULL               | NULL     | NULL                 |
| test         | t          | p0             | analyze index idx                                                  |              0 | 2022-05-27 11:29:46 | 2022-05-27 11:29:46 | finished | NULL        | 127.0.0.1:4000 | NULL       | NULL               | NULL     | NULL                 |
| test         | t          | p1             | analyze columns                                                    |              0 | 2022-05-27 11:29:46 | 2022-05-27 11:29:46 | finished | NULL        | 127.0.0.1:4000 | NULL       | NULL               | NULL     | NULL                 |
| test         | t          | p0             | analyze columns                                                    |              0 | 2022-05-27 11:29:46 | 2022-05-27 11:29:46 | finished | NULL        | 127.0.0.1:4000 | NULL       | NULL               | NULL     | NULL                 |
+--------------+------------+----------------+--------------------------------------------------------------------+----------------+---------------------+---------------------+----------+-------------+----------------+------------+--------------------+----------+----------------------+
6 rows in set (0.00 sec)
```

## MySQL 兼容性

此语句是 TiDB 对 MySQL 语法的扩展。

## 另请参阅

* [ANALYZE_STATUS 表](/information-schema/information-schema-analyze-status.md)
