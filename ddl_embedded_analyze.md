---
title: DDL Embedded Analyze 优化
summary: 本章介绍了对于特定涉及索引创建或者更新 DDL 下的内嵌式 Analyze 的优化，主要包含了 [`ADD INDEX`](/sql-statements/sql-statement-add-index.md) 和 [`MODIFY COLUMN`](/sql-statements/sql-statement-modify-column.md) / [`CHANGE COLUMN`](/sql-statements/sql-statement-change-column.md)
---

# Embedded Analyze

本文档介绍可用于 `DDL Embedded Analyze` 的优化，相关变量  [`tidb_stats_update_during_ddl`](/system-variables.md#tidb_stats_update_during_ddl) 可用于控制相关 DDL 在涉及索引数据新建或者 Reorg 时候，是否考虑做内联性 Analyze, 该值默认为 `OFF`。

## New Create Index 

当 `tidb_stats_update_during_ddl` 变量为 `ON` 时，新建索引 [`ADD INDEX`](/sql-statements/sql-statement-add-index.md) 的 DDL，可以在 Reorg 阶段结束之后，内联性发起 Analyze 命令，该命令可以在该新索引 Public 之前，分析相关新建索引的统计信息，然后再完成 DDL。考虑到 Analyze 命令可能会带来一定的耗时，TiDB 取第一次 Reorg 的时间作为内联 Analyze 的超时机制，在相关 timeout 触发之后，`Add Index` 将不再同步等待内联 Analyze 的完成，直接继续推进 Public 该索引，这意味着，后续该新索引的 stats 的就绪将异步等待该 Analyze 的完成。

```sql
mysql> create table t(a int, b int, c int);
Query OK, 0 rows affected (0.011 sec)

mysql> insert into t values(1,1,1),(2,2,2),(3,3,3);
Query OK, 3 rows affected (0.003 sec)
Records: 3  Duplicates: 0  Warnings: 0

mysql> set @@tidb_stats_update_during_ddl=1;
Query OK, 0 rows affected (0.001 sec)

mysql> alter table t add index idx(a,b);
Query OK, 0 rows affected (0.049 sec)

mysql> explain select * from t use index(idx);
+-------------------------------+---------+-----------+--------------------------+------------------+
| id                            | estRows | task      | access object            | operator info    |
+-------------------------------+---------+-----------+--------------------------+------------------+
| IndexLookUp_7                 | 3.00    | root      |                          |                  |
| ├─IndexFullScan_5(Build)      | 3.00    | cop[tikv] | table:t, index:idx(a, b) | keep order:false |
| └─TableRowIDScan_6(Probe)     | 3.00    | cop[tikv] | table:t                  | keep order:false |
+-------------------------------+---------+-----------+--------------------------+------------------+
3 rows in set (0.001 sec)

mysql> show stats_histograms where table_name="t";
+---------+------------+----------------+-------------+----------+---------------------+----------------+------------+--------------+-------------+-------------+-----------------+----------------+----------------+---------------+
| Db_name | Table_name | Partition_name | Column_name | Is_index | Update_time         | Distinct_count | Null_count | Avg_col_size | Correlation | Load_status | Total_mem_usage | Hist_mem_usage | Topn_mem_usage | Cms_mem_usage |
+---------+------------+----------------+-------------+----------+---------------------+----------------+------------+--------------+-------------+-------------+-----------------+----------------+----------------+---------------+
| test    | t          |                | a           |        0 | 2025-10-29 00:07:25 |              3 |          0 |            1 |           1 | allLoaded   |             155 |              0 |            155 |             0 |
| test    | t          |                | idx         |        1 | 2025-10-29 00:07:25 |              3 |          0 |            0 |           0 | allLoaded   |             182 |              0 |            182 |             0 |
+---------+------------+----------------+-------------+----------+---------------------+----------------+------------+--------------+-------------+-------------+-----------------+----------------+----------------+---------------+
2 rows in set (0.012 sec)

mysql> insert into t select * from t;     // run multi times.
Query OK, 3145728 rows affected (6.138 sec)
Records: 3145728  Duplicates: 0  Warnings: 0

mysql> alter table t add index idx_2(a,b,c);
Query OK, 0 rows affected (19.403 sec)

mysql> admin show ddl jobs;
+--------+---------+--------------------------+---------------+----------------------+-----------+----------+-----------+----------------------------+----------------------------+----------------------------+---------+----------------------------------------+
| JOB_ID | DB_NAME | TABLE_NAME               | JOB_TYPE      | SCHEMA_STATE         | SCHEMA_ID | TABLE_ID | ROW_COUNT | CREATE_TIME                | START_TIME                 | END_TIME                   | STATE   | COMMENTS                               |
+--------+---------+--------------------------+---------------+----------------------+-----------+----------+-----------+----------------------------+----------------------------+----------------------------+---------+----------------------------------------+
|    151 | test    | t                        | add index     | write reorganization |         2 |      148 |   6291456 | 2025-10-29 00:14:47.181000 | 2025-10-29 00:14:47.183000 | NULL                       | running | analyzing, txn-merge, max_node_count=3 |
|    150 | test    | t                        | add index     | public               |         2 |      148 |         3 | 2025-10-29 00:07:25.492000 | 2025-10-29 00:07:25.494000 | 2025-10-29 00:07:25.534000 | synced  | txn-merge, max_node_count=3            |
+--------+---------+--------------------------+---------------+----------------------+-----------+----------+-----------+----------------------------+----------------------------+----------------------------+---------+----------------------------------------+
11 rows in set (0.001 sec)
```

从 `Add Index` 事例来看， 在设置完 `@@tidb_stats_update_during_ddl` 之后的 DDL 运行结束之后，我们可以从之后的 SQL 运行中看到相关 `idx` 索引的统计信息已经被加载到了内存，并且已经被用于 Range 构造。我们从 `show stats_histograms` 语句中可以得到验证，相关索引的统计信息已经被分析已经全部加在加载到了内存中。对于时间较长的 Reorg 过程和 Analyze 过程，我们可以在相关的 DDL Job 状态语句中看到相关索引正在被 `Analyzing` 的字段，该提示表明该 DDL Job 已经处于 stats 收集过程中了。

## Reorg Existed Index

当 `tidb_stats_update_during_ddl` 变量为 `ON` 时，Reorg 已经存在的索引 [`MODIFY COLUMN`](/sql-statements/sql-statement-modify-column.md) / [`CHANGE COLUMN`](/sql-statements/sql-statement-change-column.md) 的 DDL，可以在 Reorg 阶段结束之后，内联性发起 Analyze 命令，该命令可以在该新索引 Public 之前，分析相关新建索引的统计信息，然后再完成 DDL。考虑到 Analyze 命令可能会带来一定的耗时，TiDB 取第一次 Reorg 的时间作为内联 Analyze 的超时机制，在相关 timeout 触发之后，`Modify Column` / `Change Column` 将不再同步等待内联 Analyze 的完成，直接继续推进 Public 该索引，这意味着，后续该新索引的 stats 的就绪将异步等待该 Analyze 的完成。

```sql
mysql> create table s(a int);
Query OK, 0 rows affected (0.012 sec)

mysql> insert into s values(1),(2),(3);
Query OK, 3 rows affected (0.003 sec)
Records: 3  Duplicates: 0  Warnings: 0

mysql> set @@tidb_stats_update_during_ddl=1;
Query OK, 0 rows affected (0.001 sec)

mysql> alter table s add index idx(a);
Query OK, 0 rows affected (0.049 sec)

mysql> explain select * from s use index(idx);
+-----------------------+---------+-----------+-----------------------+-----------------------+
| id                    | estRows | task      | access object         | operator info         |
+-----------------------+---------+-----------+-----------------------+-----------------------+
| IndexReader_6         | 3.00    | root      |                       | index:IndexFullScan_5 |
| └─IndexFullScan_5     | 3.00    | cop[tikv] | table:s, index:idx(a) | keep order:false      |
+-----------------------+---------+-----------+-----------------------+-----------------------+
2 rows in set (0.002 sec)

mysql> alter table s modify column a varchar(10);
Query OK, 0 rows affected (0.056 sec)

mysql> explain select * from s use index(idx);
+-----------------------+---------+-----------+-----------------------+-----------------------+
| id                    | estRows | task      | access object         | operator info         |
+-----------------------+---------+-----------+-----------------------+-----------------------+
| IndexReader_6         | 3.00    | root      |                       | index:IndexFullScan_5 |
| └─IndexFullScan_5     | 3.00    | cop[tikv] | table:s, index:idx(a) | keep order:false      |
+-----------------------+---------+-----------+-----------------------+-----------------------+
2 rows in set (0.003 sec)
  
mysql> show stats_histograms where table_name="s";
+---------+------------+----------------+-------------+----------+---------------------+----------------+------------+--------------+-------------+-------------+-----------------+----------------+----------------+---------------+
| Db_name | Table_name | Partition_name | Column_name | Is_index | Update_time         | Distinct_count | Null_count | Avg_col_size | Correlation | Load_status | Total_mem_usage | Hist_mem_usage | Topn_mem_usage | Cms_mem_usage |
+---------+------------+----------------+-------------+----------+---------------------+----------------+------------+--------------+-------------+-------------+-----------------+----------------+----------------+---------------+
| test    | s          |                | a           |        0 | 2025-10-29 00:32:43 |              3 |          0 |          0.5 |           1 | allLoaded   |             155 |              0 |            155 |             0 |
| test    | s          |                | a           |        0 | 2025-10-29 00:32:43 |              3 |          0 |            1 |           1 | allLoaded   |             158 |              0 |            158 |             0 |
| test    | s          |                | idx         |        1 | 2025-10-29 00:32:43 |              3 |          0 |            0 |           0 | allLoaded   |             155 |              0 |            155 |             0 |
| test    | s          |                | idx         |        1 | 2025-10-29 00:32:43 |              3 |          0 |            0 |           0 | allLoaded   |             158 |              0 |            158 |             0 |
+---------+------------+----------------+-------------+----------+---------------------+----------------+------------+--------------+-------------+-------------+-----------------+----------------+----------------+---------------+
4 rows in set (0.010 sec)

mysql> insert into s select * from s;     // run multi times.
Query OK, 3145728 rows affected (6.138 sec)
Records: 3145728  Duplicates: 0  Warnings: 0

mysql> alter table s modify column a varchar(5);
Query OK, 0 rows affected (19.403 sec)

mysql> admin show ddl jobs;
+--------+---------+------------------+---------------+----------------------+-----------+----------+-----------+----------------------------+----------------------------+----------------------------+---------+-----------------------------+
| JOB_ID | DB_NAME | TABLE_NAME       | JOB_TYPE      | SCHEMA_STATE         | SCHEMA_ID | TABLE_ID | ROW_COUNT | CREATE_TIME                | START_TIME                 | END_TIME                   | STATE   | COMMENTS                    |
+--------+---------+------------------+---------------+----------------------+-----------+----------+-----------+----------------------------+----------------------------+----------------------------+---------+-----------------------------+
|    153 | test    | s                | modify column | write reorganization |         2 |      148 |  12582912 | 2025-10-29 00:26:49.240000 | 2025-10-29 00:26:49.244000 | NULL                       | running | analyzing                   |
|    152 | test    | s                | modify column | public               |         2 |      148 |  18874368 | 2025-10-29 00:24:35.386000 | 2025-10-29 00:24:35.387000 | 2025-10-29 00:25:01.071000 | synced  |                             |
|    151 | test    | s                | add index     | public               |         2 |      148 |   6291456 | 2025-10-29 00:14:47.181000 | 2025-10-29 00:14:47.183000 | 2025-10-29 00:15:06.581000 | synced  | txn-merge, max_node_count=3 |
+--------+---------+------------------+---------------+----------------------+-----------+----------+-----------+----------------------------+----------------------------+----------------------------+---------+-----------------------------+
11 rows in set (0.001 sec)
```

从 `Modify Colunn` 有损 DDL 示例来看， 在设置完 `@@tidb_stats_update_during_ddl` 之后的相关列类型有损变更 DDL 运行结束之后，我们可以从之后的 SQL 运行中 explain 看到相关 `idx` 索引的统计信息已经被加载到了内存，并且已经被用于 Range 构造。我们从 `show stats_histograms` 语句中可以得到验证，相关索引的统计信息已经被分析已经全部加在加载到了内存中。对于时间较长的 Reorg 过程和 Analyze 过程，我们可以在相关的 DDL Job 状态语句中看到相关索引正在被 `Analyzing` 的字段，该提示表明该 DDL Job 已经处于 stats 收集过程中了。
