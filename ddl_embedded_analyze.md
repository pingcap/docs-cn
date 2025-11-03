---
title: 内嵌于 DDL 的 Analyze
summary: 本章介绍了对于特定涉及索引创建或者更新 DDL 下的内嵌式 Analyze 的集成，主要包含了 [`ADD INDEX`](/sql-statements/sql-statement-add-index.md) 和 [`MODIFY COLUMN`](/sql-statements/sql-statement-modify-column.md) / [`CHANGE COLUMN`](/sql-statements/sql-statement-change-column.md)，该功能主要是防止新建或者重组索引之后一段时间内索引统计信息不可用导致的估算差异，从而造成的计划变更。
---

# 内嵌于 DDL 的 Analyze

本文档介绍内嵌于 DDL 的 Analyze 特性。你可以使用系统变量 [`tidb_stats_update_during_ddl`](/system-variables.md#tidb_stats_update_during_ddl-从-v854-版本开始引入) 控制相关 DDL 在新建或重组索引数据时，是否使用内嵌的 Analyze。该值默认为 `OFF`。

## 使用场景

在一些穿插索引新增和变更的 DDL 查询场景中，很多已经稳定的查询，可能会因为一些新的索引的路径构建，以及没有及时收集统计信息，导致该索引代价低估或者高估致使计划变更。详情请参考 [Issue #57948](https://github.com/pingcap/tidb/issues/57948)。

```sql
CREATE TABLE t (a INT, b INT);
INSERT INTO t VALUES (1, 1), (2, 2), (3, 3);
INSERT INTO t SELECT * FROM t; -- * N times

ALTER TABLE t ADD INDEX idx_a (a);

EXPLAIN SELECT * FROM x WHERE a > 4;
```

```
+-------------------------+-----------+-----------+---------------+--------------------------------+
| id                      | estRows   | task      | access object | operator info                  |
+-------------------------+-----------+-----------+---------------+--------------------------------+
| TableReader_8           | 131072.00 | root      |               | data:Selection_7               |
| └─Selection_7           | 131072.00 | cop[tikv] |               | gt(test.x.a, 4)                |
|   └─TableFullScan_6     | 393216.00 | cop[tikv] | table:x       | keep order:false, stats:pseudo |
+-------------------------+-----------+-----------+---------------+--------------------------------+
3 rows in set (0.002 sec)
```

从 SQL 计划中可以看到，由于添加索引之后没有 stats，在路径估算的时候，除非是一些简单的不用回表的启发式比较可以胜出之外，基本会选中估算确定性比较高现有的路径，上述示例选择的是默认的全表扫描。但是从宏观视角来看，`x.a > 4` 在实际数据分布中只有 0 行，通过索引 `idx_a` 访问可以更快的定位到相关的行，从而避免全表扫描。这里主要是由于在 DDL 创建索引之后，TiDB 自身没有及时收集索引统计信息导致计划不优，但是至少计划可以和以往保持一致，不存在计划跳变问题。然而在上述 [Issue #57948](https://github.com/pingcap/tidb/issues/57948) 中，新建的索引可能会和已经存在的索引进行启发式的比较，导致原有计划所依赖的索引被裁减，最终剩下的索引路径由于没有统计信息，从而默认选择了全表扫描。

在 v8.5 及之后的版本中，TiDB 在索引的启发式比较和统计信息有无中做了很大的权衡和改善。但在一些复杂场景中，在 DDL 中嵌套完成索引统计信息的分析仍然是防止计划变更最保险的选择。

## 新建索引 `ADD INDEX` 的 DDL

当 `tidb_stats_update_during_ddl` 变量为 `ON` 时，新建索引 [`ADD INDEX`](/sql-statements/sql-statement-add-index.md) 的 DDL，可以在 Reorg 阶段结束之后，内联性发起 Analyze 命令，该命令可以在该新索引对用户可见之前，分析相关新建索引的统计信息，然后再完成执行 DDL。

考虑到 Analyze 命令可能会带来一定的耗时，TiDB 取第一次 Reorg 的时间作为内联 Analyze 的超时机制，在相关 timeout 触发之后，`ADD INDEX` 将不再同步等待内联 Analyze 的完成，直接继续推进对用户可见该索引，这意味着，需要异步等待该 Analyze 完成后，该新索引的 stats 才能就绪。

```sql
CREATE TABLE t (a INT, b INT, c INT);
Query OK, 0 rows affected (0.011 sec)

INSERT INTO t VALUES (1, 1, 1), (2, 2, 2), (3, 3, 3);
Query OK, 3 rows affected (0.003 sec)
Records: 3  Duplicates: 0  Warnings: 0

SET @@tidb_stats_update_during_ddl = 1;
Query OK, 0 rows affected (0.001 sec)

ALTER TABLE t ADD INDEX idx (a, b);
Query OK, 0 rows affected (0.049 sec)
```

```sql
EXPLAIN SELECT a FROM t WHERE a > 1;
```

```
+------------------------+---------+-----------+--------------------------+----------------------------------+
| id                     | estRows | task      | access object            | operator info                    |
+------------------------+---------+-----------+--------------------------+----------------------------------+
| IndexReader_7          | 4.00    | root      |                          | index:IndexRangeScan_6           |
| └─IndexRangeScan_6     | 4.00    | cop[tikv] | table:t, index:idx(a, b) | range:(1,+inf], keep order:false |
+------------------------+---------+-----------+--------------------------+----------------------------------+
2 rows in set (0.002 sec)

show stats_histograms where table_name="t";
+---------+------------+----------------+-------------+----------+---------------------+----------------+------------+--------------+-------------+-------------+-----------------+----------------+----------------+---------------+
| Db_name | Table_name | Partition_name | Column_name | Is_index | Update_time         | Distinct_count | Null_count | Avg_col_size | Correlation | Load_status | Total_mem_usage | Hist_mem_usage | Topn_mem_usage | Cms_mem_usage |
+---------+------------+----------------+-------------+----------+---------------------+----------------+------------+--------------+-------------+-------------+-----------------+----------------+----------------+---------------+
| test    | t          |                | a           |        0 | 2025-10-30 20:17:57 |              3 |          0 |          0.5 |           1 | allLoaded   |             155 |              0 |            155 |             0 |
| test    | t          |                | idx         |        1 | 2025-10-30 20:17:57 |              3 |          0 |            0 |           0 | allLoaded   |             182 |              0 |            182 |             0 |
+---------+------------+----------------+-------------+----------+---------------------+----------------+------------+--------------+-------------+-------------+-----------------+----------------+----------------+---------------+
2 rows in set (0.013 sec)
```

```sql
ADMIN SHOW DDL JOBS 1;
```

```
+--------+---------+--------------------------+---------------+----------------------+-----------+----------+-----------+----------------------------+----------------------------+----------------------------+---------+----------------------------------------+
| JOB_ID | DB_NAME | TABLE_NAME               | JOB_TYPE      | SCHEMA_STATE         | SCHEMA_ID | TABLE_ID | ROW_COUNT | CREATE_TIME                | START_TIME                 | END_TIME                   | STATE   | COMMENTS                               |
+--------+---------+--------------------------+---------------+----------------------+-----------+----------+-----------+----------------------------+----------------------------+----------------------------+---------+----------------------------------------+
|    151 | test    | t                        | add index     | write reorganization |         2 |      148 |   6291456 | 2025-10-29 00:14:47.181000 | 2025-10-29 00:14:47.183000 | NULL                       | running | analyzing, txn-merge, max_node_count=3 |
+--------+---------+--------------------------+---------------+----------------------+-----------+----------+-----------+----------------------------+----------------------------+----------------------------+---------+----------------------------------------+
1 rows in set (0.001 sec)
```

从 `ADD INDEX` 事例来看，当 `tidb_stats_update_during_ddl` 变量为 `ON`，在 DDL 运行结束之后，可以从之后的 SQL 运行中看到相关 `idx` 索引的统计信息已经被加载到了内存，并且已经用于 Range 构造。从 `show stats_histograms` 语句中可以得到验证，相关索引的统计信息已经被分析，全部加载到了内存中。对于时间较长的索引添加或者重组过程和 Analyze 过程，你可以在相关的 DDL Job 状态语句中看到相关索引正在被分析 (`Analyzing`)，表明该 DDL Job 已经处于 stats 收集过程中了。

## 重组已有索引的 DDL

当 `tidb_stats_update_during_ddl` 变量为 `ON` 时，重组已经存在的索引 [`MODIFY COLUMN`](/sql-statements/sql-statement-modify-column.md) / [`CHANGE COLUMN`](/sql-statements/sql-statement-change-column.md) 的 DDL，可以在重组阶段结束之后，内联性发起 Analyze 命令，该命令可以在该新索引对用户可见之前，分析相关新建索引的统计信息，然后再完成 DDL。考虑到 Analyze 命令可能会带来一定的耗时，TiDB 取第一次 Reorg 的时间作为内联 Analyze 的超时机制，在相关 timeout 触发之后，`Modify Column` / `Change Column` 将不再同步等待内联 Analyze 的完成，直接继续推进对用户可见该索引，这意味着，需要异步等待该 Analyze 完成后，该新索引的 stats 才能就绪。

```sql
CREATE TABLE s (a VARCHAR(10), INDEX idx (a));
Query OK, 0 rows affected (0.012 sec)

INSERT INTO s VALUES (1), (2), (3);
Query OK, 3 rows affected (0.003 sec)
Records: 3  Duplicates: 0  Warnings: 0

SET @@tidb_stats_update_during_ddl = 1;
Query OK, 0 rows affected (0.001 sec)

ALTER TABLE s MODIFY COLUMN a INT;
Query OK, 0 rows affected (0.056 sec)

EXPLAIN SELECT * FROM s WHERE a > 1;
```

```
+------------------------+---------+-----------+-----------------------+----------------------------------+
| id                     | estRows | task      | access object         | operator info                    |
+------------------------+---------+-----------+-----------------------+----------------------------------+
| IndexReader_7          | 2.00    | root      |                       | index:IndexRangeScan_6           |
| └─IndexRangeScan_6     | 2.00    | cop[tikv] | table:s, index:idx(a) | range:(1,+inf], keep order:false |
+------------------------+---------+-----------+-----------------------+----------------------------------+
2 rows in set (0.005 sec)
```
  
```sql
SHOW STATS_HISTOGRAMS WHERE table_name = "s";
```

```
+---------+------------+----------------+-------------+----------+---------------------+----------------+------------+--------------+-------------+-------------+-----------------+----------------+----------------+---------------+
| Db_name | Table_name | Partition_name | Column_name | Is_index | Update_time         | Distinct_count | Null_count | Avg_col_size | Correlation | Load_status | Total_mem_usage | Hist_mem_usage | Topn_mem_usage | Cms_mem_usage |
+---------+------------+----------------+-------------+----------+---------------------+----------------+------------+--------------+-------------+-------------+-----------------+----------------+----------------+---------------+
| test    | s          |                | a           |        0 | 2025-10-30 20:10:18 |              3 |          0 |            2 |           1 | allLoaded   |             158 |              0 |            158 |             0 |
| test    | s          |                | a           |        0 | 2025-10-30 20:10:18 |              3 |          0 |            1 |           1 | allLoaded   |             155 |              0 |            155 |             0 |
| test    | s          |                | idx         |        1 | 2025-10-30 20:10:18 |              3 |          0 |            0 |           0 | allLoaded   |             158 |              0 |            158 |             0 |
| test    | s          |                | idx         |        1 | 2025-10-30 20:10:18 |              3 |          0 |            0 |           0 | allLoaded   |             155 |              0 |            155 |             0 |
+---------+------------+----------------+-------------+----------+---------------------+----------------+------------+--------------+-------------+-------------+-----------------+----------------+----------------+---------------+
4 rows in set (0.008 sec)
```

```sql
ADMIN SHOW DDL JOBS 1;
```

```
+--------+---------+------------------+---------------+----------------------+-----------+----------+-----------+----------------------------+----------------------------+----------------------------+---------+-----------------------------+
| JOB_ID | DB_NAME | TABLE_NAME       | JOB_TYPE      | SCHEMA_STATE         | SCHEMA_ID | TABLE_ID | ROW_COUNT | CREATE_TIME                | START_TIME                 | END_TIME                   | STATE   | COMMENTS                    |
+--------+---------+------------------+---------------+----------------------+-----------+----------+-----------+----------------------------+----------------------------+----------------------------+---------+-----------------------------+
|    153 | test    | s                | modify column | write reorganization |         2 |      148 |  12582912 | 2025-10-29 00:26:49.240000 | 2025-10-29 00:26:49.244000 | NULL                       | running | analyzing                   |
+--------+---------+------------------+---------------+----------------------+-----------+----------+-----------+----------------------------+----------------------------+----------------------------+---------+-----------------------------+
1 rows in set (0.001 sec)
```

从 `Modify Column` 有损 DDL 示例来看， 当 `tidb_stats_update_during_ddl` 变量为 `ON` 时，相关列类型有损变更 DDL 运行结束之后，你可以从之后的 SQL 运行中 Explain 看到相关 `idx` 索引的统计信息已经被加载到了内存，并且已经被用于 Range 构造。从 `show stats_histograms` 语句中可以得到验证，相关索引的统计信息已经被分析，全部加载到了内存中。

对于时间较长的索引添加或者重组过程和 Analyze 过程，可以在相关的 DDL Job 状态语句中看到相关索引正在被分析 (`Analyzing`)，表明该 DDL Job 已经处于 stats 收集过程中了。
