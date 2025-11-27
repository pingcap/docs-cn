---
title: 内嵌于 DDL 的 Analyze
summary: 本文介绍内嵌于新建或重组索引的 DDL 中的 Analyze 特性，用于确保新索引的统计信息及时更新。
---

# 内嵌于 DDL 的 Analyze <span class="version-mark">从 v8.5.4 开始引入</span>

本文介绍内嵌于以下两类 DDL 的 Analyze 特性：

- 新建索引的 DDL：[`ADD INDEX`](/sql-statements/sql-statement-add-index.md)
- 重组已有索引的 DDL：[`MODIFY COLUMN`](/sql-statements/sql-statement-modify-column.md) 和 [`CHANGE COLUMN`](/sql-statements/sql-statement-change-column.md)

开启该特性后，TiDB 会在新索引对用户可见前自动执行一次 Analyze（统计信息收集），以避免新建或重组索引后因统计信息暂不可用而导致优化器估算不准，从而引起执行计划变更的问题。

## 使用场景

在一些交替执行索引新增或修改的 DDL 操作场景中，已有的稳定查询可能因为新索引缺乏统计信息而出现代价估算偏差，导致优化器生成次优计划。详情可参考 [Issue #57948](https://github.com/pingcap/tidb/issues/57948)。

例如：

```sql
CREATE TABLE t (a INT, b INT);
INSERT INTO t VALUES (1, 1), (2, 2), (3, 3);
INSERT INTO t SELECT * FROM t; -- * N times

ALTER TABLE t ADD INDEX idx_a (a);

EXPLAIN SELECT * FROM t WHERE a > 4;
```

```
+-------------------------+-----------+-----------+---------------+--------------------------------+
| id                      | estRows   | task      | access object | operator info                  |
+-------------------------+-----------+-----------+---------------+--------------------------------+
| TableReader_8           | 131072.00 | root      |               | data:Selection_7               |
| └─Selection_7           | 131072.00 | cop[tikv] |               | gt(test.t.a, 4)                |
|   └─TableFullScan_6     | 393216.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo |
+-------------------------+-----------+-----------+---------------+--------------------------------+
3 rows in set (0.002 sec)
```

从以上执行计划可以看到，由于新建索引尚未生成统计信息，TiDB 在路径估算时只能依赖启发式规则。除非索引访问路径无需回表且代价显著更低，否则优化器倾向于选择估算更稳定的现有路径，因此上述示例中使用了全表扫描。然而，从数据分布角度来看，`t.a > 4` 实际返回 0 行，如果能使用新建索引 `idx_a`，查询可以快速定位到相关行，从而避免全表扫描。在该示例中，由于 DDL 创建索引后 TiDB 未能及时收集索引统计信息，生成的执行计划不是最优的，但优化器会继续沿用原有计划，因此查询性能不会出现突变或退化。然而，根据 [Issue #57948](https://github.com/pingcap/tidb/issues/57948)，在某些情况下，启发式规则可能会导致新旧索引进行不合理的比较，从而裁剪原查询计划依赖的索引，最终 fallback 到全表扫描。

从 v8.5.0 起，TiDB 对索引的启发式比较和统计信息缺失时的行为进行了优化。但在部分复杂场景中，在 DDL 执行过程中内嵌 Analyze 仍是防止执行计划变更的最佳方案。你可以通过系统变量 [`tidb_stats_update_during_ddl`](/system-variables.md#tidb_stats_update_during_ddl-从-v854-版本开始引入) 控制在索引创建或重组阶段是否执行内嵌 Analyze。该变量默认值为 `OFF`。

## 新建索引 `ADD INDEX` 的 DDL

当 `tidb_stats_update_during_ddl` 设置为 `ON` 时，执行 [`ADD INDEX`](/sql-statements/sql-statement-add-index.md) 操作将在 Reorg 阶段结束后自动执行内嵌的 Analyze 命令。此 Analyze 命令会在新索引对用户可见前，分析相关新建索引的统计信息，然后再继续执行 `ADD INDEX` 的剩余阶段。

考虑到 Analyze 可能会有一定的耗时，TiDB 会以首次 Reorg 的执行时间为参考设置超时阈值。若 Analyze 超时，`ADD INDEX` 将不再同步等待 Analyze 完成，而是继续执行后续流程，使索引提前对用户可见。这意味着，该新索引的统计信息会在 Analyze 异步完成后更新。

示例：

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
```

```sql
SHOW STATS_HISTOGRAMS WHERE table_name = "t";
```

```
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

从 `ADD INDEX` 示例来看，当 `tidb_stats_update_during_ddl` 设置为 `ON` 时，在 `ADD INDEX` DDL 执行结束后，可以看到其之后运行的 `EXPLAIN` 查询中，相关索引 `idx` 的统计信息已经被自动收集并加载到内存中（可通过 `SHOW STATS_HISTOGRAMS` 语句的输出结果得到验证）。因此，优化器可以立即在范围扫描（Range Scan）中使用这些统计信息。如果索引的创建或重组以及 Analyze 过程耗时较长，可以通过 `ADMIN SHOW DDL JOBS` 查看 DDL Job 的状态。当输出结果中的 `COMMENTS` 列包含 `analyzing` 时，表示该 DDL Job 正在执行统计信息收集。

## 重组已有索引的 DDL

当 `tidb_stats_update_during_ddl` 设置为 `ON` 时，执行 [`MODIFY COLUMN`](/sql-statements/sql-statement-modify-column.md) 或 [`CHANGE COLUMN`](/sql-statements/sql-statement-change-column.md) 操作重组索引时，TiDB 也会在 Reorg 阶段结束后执行内嵌的 Analyze 命令。其机制与 `ADD INDEX` 相同：

- 在索引可见前开始进行统计信息收集。
- 若 Analyze 超时，[`MODIFY COLUMN`](/sql-statements/sql-statement-modify-column.md) 和 [`CHANGE COLUMN`](/sql-statements/sql-statement-change-column.md) 将不会同步等待 Analyze 完成，而是继续执行后续流程，使索引提前对用户可见。这意味着，该新索引的统计信息会在 Analyze 异步完成后更新。

示例：

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

从 `MODIFY COLUMN` 示例来看，当 `tidb_stats_update_during_ddl` 设置为 `ON` 时，在 `MODIFY COLUMN` DDL 执行结束后，可以看到其之后运行的 `EXPLAIN` 查询中，相关索引 `idx` 的统计信息已经被自动收集并加载到内存中（可通过 `SHOW STATS_HISTOGRAMS` 语句的输出结果得到验证），因此优化器能够立即在范围扫描（Range Scan）中使用这些统计信息。如果索引的创建或重组以及 Analyze 过程耗时较长，可以通过 `ADMIN SHOW DDL JOBS` 查看 DDL Job 的状态。当输出结果中的 `COMMENTS` 列包含 `analyzing` 时，表示该 DDL Job 正在执行统计信息收集。
