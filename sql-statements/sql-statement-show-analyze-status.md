---
title: SHOW ANALYZE STATUS
summary: TiDB 数据库中 SHOW ANALYZE STATUS 的使用概况。
aliases: ['/docs-cn/dev/sql-statements/sql-statement-show-analyze-status/']
---

# SHOW ANALYZE STATUS

`SHOW ANALYZE STATUS` 语句提供 TiDB 正在执行的统计信息收集任务以及有限条历史任务记录。

在 TiDB v6.1 之前，`SHOW ANALYZE STATUS` 显示实例级别的任务，且 TiDB 重启后任务记录会被清空。从 TiDB v6.1 起，`SHOW ANALYZE STATUS` 显示集群级别的任务，且 TiDB 重启后仍能看到重启之前的任务记录。

从 TiDB v6.1 起，可以通过系统表 `mysql.analyze_jobs` 查看更早的（7 天内的） 历史记录。

## 语法图

```ebnf+diagram
ShowAnalyzeStatusStmt ::= 'SHOW' 'ANALYZE' 'STATUS' ShowLikeOrWhereOpt

ShowLikeOrWhereOpt ::= 'LIKE' SimpleExpr | 'WHERE' Expression
```

## 示例

```sql
mysql> create table t(x int, index idx(x)) partition by hash(x) partitions 4;
Query OK, 0 rows affected (0.69 sec)

mysql> set @@tidb_analyze_version = 1;
Query OK, 0 rows affected (0.00 sec)

mysql> analyze table t;
Query OK, 0 rows affected (0.20 sec)

mysql> show analyze status;
+--------------+------------+----------------+-------------------+----------------+---------------------+---------------------+----------+-------------+----------------+------------+
| Table_schema | Table_name | Partition_name | Job_info          | Processed_rows | Start_time          | End_time            | State    | Fail_reason | Instance       | Process_ID |
+--------------+------------+----------------+-------------------+----------------+---------------------+---------------------+----------+-------------+----------------+------------+
| test         | t          | p3             | analyze index idx |              0 | 2022-05-16 19:42:34 | 2022-05-16 19:42:34 | finished | NULL        | 127.0.0.1:4000 |       NULL |
| test         | t          | p2             | analyze index idx |              0 | 2022-05-16 19:42:34 | 2022-05-16 19:42:34 | finished | NULL        | 127.0.0.1:4000 |       NULL |
| test         | t          | p1             | analyze index idx |              0 | 2022-05-16 19:42:34 | 2022-05-16 19:42:34 | finished | NULL        | 127.0.0.1:4000 |       NULL |
| test         | t          | p0             | analyze index idx |              0 | 2022-05-16 19:42:34 | 2022-05-16 19:42:34 | finished | NULL        | 127.0.0.1:4000 |       NULL |
| test         | t          | p3             | analyze columns   |              0 | 2022-05-16 19:42:34 | 2022-05-16 19:42:34 | finished | NULL        | 127.0.0.1:4000 |       NULL |
| test         | t          | p2             | analyze columns   |              0 | 2022-05-16 19:42:34 | 2022-05-16 19:42:34 | finished | NULL        | 127.0.0.1:4000 |       NULL |
| test         | t          | p1             | analyze columns   |              0 | 2022-05-16 19:42:34 | 2022-05-16 19:42:34 | finished | NULL        | 127.0.0.1:4000 |       NULL |
| test         | t          | p0             | analyze columns   |              0 | 2022-05-16 19:42:34 | 2022-05-16 19:42:34 | finished | NULL        | 127.0.0.1:4000 |       NULL |
+--------------+------------+----------------+-------------------+----------------+---------------------+---------------------+----------+-------------+----------------+------------+
8 rows in set (0.00 sec)

mysql> set @@tidb_analyze_version = 2;
Query OK, 0 rows affected (0.00 sec)

mysql> analyze table t;
Query OK, 0 rows affected, 4 warnings (0.15 sec)

mysql> show analyze status;
+--------------+------------+----------------+--------------------------------------------------------------------+----------------+---------------------+---------------------+----------+-------------+----------------+------------+
| Table_schema | Table_name | Partition_name | Job_info                                                           | Processed_rows | Start_time          | End_time            | State    | Fail_reason | Instance       | Process_ID |
+--------------+------------+----------------+--------------------------------------------------------------------+----------------+---------------------+---------------------+----------+-------------+----------------+------------+
| test         | t          | p3             | analyze table all columns with 256 buckets, 500 topn, 1 samplerate |              0 | 2022-05-16 19:43:10 | 2022-05-16 19:43:10 | finished | NULL        | 127.0.0.1:4000 |       NULL |
| test         | t          | p2             | analyze table all columns with 256 buckets, 500 topn, 1 samplerate |              0 | 2022-05-16 19:43:10 | 2022-05-16 19:43:10 | finished | NULL        | 127.0.0.1:4000 |       NULL |
| test         | t          | p1             | analyze table all columns with 256 buckets, 500 topn, 1 samplerate |              0 | 2022-05-16 19:43:10 | 2022-05-16 19:43:10 | finished | NULL        | 127.0.0.1:4000 |       NULL |
| test         | t          | p0             | analyze table all columns with 256 buckets, 500 topn, 1 samplerate |              0 | 2022-05-16 19:43:10 | 2022-05-16 19:43:10 | finished | NULL        | 127.0.0.1:4000 |       NULL |
| test         | t          | p3             | analyze index idx                                                  |              0 | 2022-05-16 19:42:34 | 2022-05-16 19:42:34 | finished | NULL        | 127.0.0.1:4000 |       NULL |
| test         | t          | p2             | analyze index idx                                                  |              0 | 2022-05-16 19:42:34 | 2022-05-16 19:42:34 | finished | NULL        | 127.0.0.1:4000 |       NULL |
| test         | t          | p1             | analyze index idx                                                  |              0 | 2022-05-16 19:42:34 | 2022-05-16 19:42:34 | finished | NULL        | 127.0.0.1:4000 |       NULL |
| test         | t          | p0             | analyze index idx                                                  |              0 | 2022-05-16 19:42:34 | 2022-05-16 19:42:34 | finished | NULL        | 127.0.0.1:4000 |       NULL |
| test         | t          | p3             | analyze columns                                                    |              0 | 2022-05-16 19:42:34 | 2022-05-16 19:42:34 | finished | NULL        | 127.0.0.1:4000 |       NULL |
| test         | t          | p2             | analyze columns                                                    |              0 | 2022-05-16 19:42:34 | 2022-05-16 19:42:34 | finished | NULL        | 127.0.0.1:4000 |       NULL |
| test         | t          | p1             | analyze columns                                                    |              0 | 2022-05-16 19:42:34 | 2022-05-16 19:42:34 | finished | NULL        | 127.0.0.1:4000 |       NULL |
| test         | t          | p0             | analyze columns                                                    |              0 | 2022-05-16 19:42:34 | 2022-05-16 19:42:34 | finished | NULL        | 127.0.0.1:4000 |       NULL |
+--------------+------------+----------------+--------------------------------------------------------------------+----------------+---------------------+---------------------+----------+-------------+----------------+------------+
12 rows in set (0.00 sec)
```

## MySQL 兼容性

该语句是 TiDB 对 MySQL 语法的扩展。

## 另请参阅

* [ANALYZE_STATUS 表](/information-schema/information-schema-analyze-status.md)