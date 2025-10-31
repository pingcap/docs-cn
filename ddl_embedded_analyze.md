---
title: DDL Embedded Analyze
summary: 本章介绍了对于特定涉及索引创建或者更新 DDL 下的内嵌式 Analyze 的集成，主要包含了 [`ADD INDEX`](/sql-statements/sql-statement-add-index.md) 和 [`MODIFY COLUMN`](/sql-statements/sql-statement-modify-column.md) / [`CHANGE COLUMN`](/sql-statements/sql-statement-change-column.md)，该功能主要是防止新建或者重组索引之后一段时间内索引统计信息不可用导致的估算差异，从而造成的计划变更。
---

# Embedded Analyze

本文档介绍内嵌于 DDL 的 Analyze 特性，相关变量  [`tidb_stats_update_during_ddl`](/system-variables.md#tidb_stats_update_during_ddl-从-v854-版本开始引入) 可用于控制相关 DDL 在涉及索引数据新建或者重组的时候，是否做内嵌的 Analyze。该值默认为 `OFF`。

## Scenario

在一些穿插索引新增和变更的 DDL 查询场景中，很多已经稳定的查询，可能会因为一些新的索引的路径构建，并且由于没有及时收集统计信息，而导致该索引代价低估或者高估致使计划变更。详情请参考 [Issue #57948](https://github.com/pingcap/tidb/issues/57948)。

```sql

mysql> create table t(a int, b int);
mysql> insert into t values(1,1),(2,2),(3,3);
mysql> insert into t select * from t; // * N times

mysql> alter table t add index idx_a(a);
explain select * from t where a>1;

mysql> explain select * from x where a>4;
+-------------------------+-----------+-----------+---------------+--------------------------------+
| id                      | estRows   | task      | access object | operator info                  |
+-------------------------+-----------+-----------+---------------+--------------------------------+
| TableReader_8           | 131072.00 | root      |               | data:Selection_7               |
| └─Selection_7           | 131072.00 | cop[tikv] |               | gt(test.x.a, 4)                |
|   └─TableFullScan_6     | 393216.00 | cop[tikv] | table:x       | keep order:false, stats:pseudo |
+-------------------------+-----------+-----------+---------------+--------------------------------+
3 rows in set (0.002 sec)
```

SQL 计划中可以看到，由于添加索引之后其没有 stats，在路径估算的时候除非是一些简单的不用回表的启发式比较可以胜出之外，基本会选中估算确定性比较现有的路径，上述示例选择的是默认的全表扫描。但是其实从宏观视角来看，`x.a > 4` 在实际数据分布中只有 0 行，走 `idx_a` 可以更快的定位到相关的行，从而避免全表扫描。这里主要是由于在 DDL 创建索引之后，索引统计信息没有及时收集导致的计划不优，但是至少计划能够跟以往保持一致，不存在计划跳变问题。然而在上述 `issues/57948` 中，新建的索引可能会和已经存在的索引进行启发式的比较，导致原有计划所依赖的索引被裁减，最终剩下的索引路径又最后又由于没有统计信息，从而默认选择了全表扫描。在后续 v8.5 和之后的版本中，我们对索引的启发式比较和统计信息的有无做了很大的权衡和改善，但是在除此之外一些复杂场景中，在 DDL 中嵌套完成索引统计信息的分析仍然是防止计划变更最保险的选择。

## New Create Index 

当 `tidb_stats_update_during_ddl` 变量为 `ON` 时，新建索引 [`ADD INDEX`](/sql-statements/sql-statement-add-index.md) 的 DDL，可以在 Reorg 阶段结束之后，内联性发起 Analyze 命令，该命令可以在该新索引对用户可见之前，分析相关新建索引的统计信息，然后再完成 DDL。考虑到 Analyze 命令可能会带来一定的耗时，TiDB 取第一次 Reorg 的时间作为内联 Analyze 的超时机制，在相关 timeout 触发之后，`Add Index` 将不再同步等待内联 Analyze 的完成，直接继续推进对用户可见该索引，这意味着，后续该新索引的 stats 的就绪将异步等待该 Analyze 的完成。

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

mysql> explain select a from t where a > 1;
+------------------------+---------+-----------+--------------------------+----------------------------------+
| id                     | estRows | task      | access object            | operator info                    |
+------------------------+---------+-----------+--------------------------+----------------------------------+
| IndexReader_7          | 4.00    | root      |                          | index:IndexRangeScan_6           |
| └─IndexRangeScan_6     | 4.00    | cop[tikv] | table:t, index:idx(a, b) | range:(1,+inf], keep order:false |
+------------------------+---------+-----------+--------------------------+----------------------------------+
2 rows in set (0.002 sec)


mysql> show stats_histograms where table_name="t";
+---------+------------+----------------+-------------+----------+---------------------+----------------+------------+--------------+-------------+-------------+-----------------+----------------+----------------+---------------+
| Db_name | Table_name | Partition_name | Column_name | Is_index | Update_time         | Distinct_count | Null_count | Avg_col_size | Correlation | Load_status | Total_mem_usage | Hist_mem_usage | Topn_mem_usage | Cms_mem_usage |
+---------+------------+----------------+-------------+----------+---------------------+----------------+------------+--------------+-------------+-------------+-----------------+----------------+----------------+---------------+
| test    | t          |                | a           |        0 | 2025-10-30 20:17:57 |              3 |          0 |          0.5 |           1 | allLoaded   |             155 |              0 |            155 |             0 |
| test    | t          |                | idx         |        1 | 2025-10-30 20:17:57 |              3 |          0 |            0 |           0 | allLoaded   |             182 |              0 |            182 |             0 |
+---------+------------+----------------+-------------+----------+---------------------+----------------+------------+--------------+-------------+-------------+-----------------+----------------+----------------+---------------+
2 rows in set (0.013 sec)

mysql> admin show ddl jobs 1;   
+--------+---------+--------------------------+---------------+----------------------+-----------+----------+-----------+----------------------------+----------------------------+----------------------------+---------+----------------------------------------+
| JOB_ID | DB_NAME | TABLE_NAME               | JOB_TYPE      | SCHEMA_STATE         | SCHEMA_ID | TABLE_ID | ROW_COUNT | CREATE_TIME                | START_TIME                 | END_TIME                   | STATE   | COMMENTS                               |
+--------+---------+--------------------------+---------------+----------------------+-----------+----------+-----------+----------------------------+----------------------------+----------------------------+---------+----------------------------------------+
|    151 | test    | t                        | add index     | write reorganization |         2 |      148 |   6291456 | 2025-10-29 00:14:47.181000 | 2025-10-29 00:14:47.183000 | NULL                       | running | analyzing, txn-merge, max_node_count=3 |
+--------+---------+--------------------------+---------------+----------------------+-----------+----------+-----------+----------------------------+----------------------------+----------------------------+---------+----------------------------------------+
1 rows in set (0.001 sec)
```

从 `Add Index` 事例来看， 在设置完 `@@tidb_stats_update_during_ddl` 之后的 DDL 运行结束之后，我们可以从之后的 SQL 运行中看到相关 `idx` 索引的统计信息已经被加载到了内存，并且已经被用于 Range 构造。我们从 `show stats_histograms` 语句中可以得到验证，相关索引的统计信息已经被分析已经全部加在加载到了内存中。对于时间较长的索引添加或者重组过程和 Analyze 过程，我们可以在相关的 DDL Job 状态语句中看到相关索引正在被 `Analyzing` 的字段，该提示表明该 DDL Job 已经处于 stats 收集过程中了。

## Reorg Existed Index

当 `tidb_stats_update_during_ddl` 变量为 `ON` 时，Reorg 已经存在的索引 [`MODIFY COLUMN`](/sql-statements/sql-statement-modify-column.md) / [`CHANGE COLUMN`](/sql-statements/sql-statement-change-column.md) 的 DDL，可以在 Reorg 阶段结束之后，内联性发起 Analyze 命令，该命令可以在该新索引对用户可见之前，分析相关新建索引的统计信息，然后再完成 DDL。考虑到 Analyze 命令可能会带来一定的耗时，TiDB 取第一次 Reorg 的时间作为内联 Analyze 的超时机制，在相关 timeout 触发之后，`Modify Column` / `Change Column` 将不再同步等待内联 Analyze 的完成，直接继续推进对用户可见该索引，这意味着，后续该新索引的 stats 的就绪将异步等待该 Analyze 的完成。

```sql
mysql> create table s(a varchar(10), index idx(a));
Query OK, 0 rows affected (0.012 sec)

mysql> insert into s values(1),(2),(3);
Query OK, 3 rows affected (0.003 sec)
Records: 3  Duplicates: 0  Warnings: 0

mysql> set @@tidb_stats_update_during_ddl=1;
Query OK, 0 rows affected (0.001 sec)

mysql> alter table s modify column a int;
Query OK, 0 rows affected (0.056 sec)

mysql> explain select * from s where a > 1;
+------------------------+---------+-----------+-----------------------+----------------------------------+
| id                     | estRows | task      | access object         | operator info                    |
+------------------------+---------+-----------+-----------------------+----------------------------------+
| IndexReader_7          | 2.00    | root      |                       | index:IndexRangeScan_6           |
| └─IndexRangeScan_6     | 2.00    | cop[tikv] | table:s, index:idx(a) | range:(1,+inf], keep order:false |
+------------------------+---------+-----------+-----------------------+----------------------------------+
2 rows in set (0.005 sec)
  
mysql> show stats_histograms where table_name="s";
+---------+------------+----------------+-------------+----------+---------------------+----------------+------------+--------------+-------------+-------------+-----------------+----------------+----------------+---------------+
| Db_name | Table_name | Partition_name | Column_name | Is_index | Update_time         | Distinct_count | Null_count | Avg_col_size | Correlation | Load_status | Total_mem_usage | Hist_mem_usage | Topn_mem_usage | Cms_mem_usage |
+---------+------------+----------------+-------------+----------+---------------------+----------------+------------+--------------+-------------+-------------+-----------------+----------------+----------------+---------------+
| test    | s          |                | a           |        0 | 2025-10-30 20:10:18 |              3 |          0 |            2 |           1 | allLoaded   |             158 |              0 |            158 |             0 |
| test    | s          |                | a           |        0 | 2025-10-30 20:10:18 |              3 |          0 |            1 |           1 | allLoaded   |             155 |              0 |            155 |             0 |
| test    | s          |                | idx         |        1 | 2025-10-30 20:10:18 |              3 |          0 |            0 |           0 | allLoaded   |             158 |              0 |            158 |             0 |
| test    | s          |                | idx         |        1 | 2025-10-30 20:10:18 |              3 |          0 |            0 |           0 | allLoaded   |             155 |              0 |            155 |             0 |
+---------+------------+----------------+-------------+----------+---------------------+----------------+------------+--------------+-------------+-------------+-----------------+----------------+----------------+---------------+
4 rows in set (0.008 sec)

mysql> admin show ddl jobs 1; 
+--------+---------+------------------+---------------+----------------------+-----------+----------+-----------+----------------------------+----------------------------+----------------------------+---------+-----------------------------+
| JOB_ID | DB_NAME | TABLE_NAME       | JOB_TYPE      | SCHEMA_STATE         | SCHEMA_ID | TABLE_ID | ROW_COUNT | CREATE_TIME                | START_TIME                 | END_TIME                   | STATE   | COMMENTS                    |
+--------+---------+------------------+---------------+----------------------+-----------+----------+-----------+----------------------------+----------------------------+----------------------------+---------+-----------------------------+
|    153 | test    | s                | modify column | write reorganization |         2 |      148 |  12582912 | 2025-10-29 00:26:49.240000 | 2025-10-29 00:26:49.244000 | NULL                       | running | analyzing                   |
+--------+---------+------------------+---------------+----------------------+-----------+----------+-----------+----------------------------+----------------------------+----------------------------+---------+-----------------------------+
1 rows in set (0.001 sec)
```

从 `Modify Column` 有损 DDL 示例来看， 在设置完 `@@tidb_stats_update_during_ddl` 之后的相关列类型有损变更 DDL 运行结束之后，我们可以从之后的 SQL 运行中 explain 看到相关 `idx` 索引的统计信息已经被加载到了内存，并且已经被用于 Range 构造。我们从 `show stats_histograms` 语句中可以得到验证，相关索引的统计信息已经被分析已经全部加在加载到了内存中。对于时间较长的索引添加或者重组过程和 Analyze 过程，我们可以在相关的 DDL Job 状态语句中看到相关索引正在被 `Analyzing` 的字段，该提示表明该 DDL Job 已经处于 stats 收集过程中了。
