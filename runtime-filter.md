---
title: Runtime Filter
summary: 介绍 Runtime Filter 的原理及使用方式。
---

# Runtime Filter

Runtime Filter 是 TiDB v7.3 引入的新功能，旨在提升 MPP 场景下 Hash Join 的性能。它通过动态生成 Filter 来提前过滤 Hash Join 的数据，从而减少运行时的数据扫描量以及 Hash Join 的计算量，最终提升查询性能。

## 名词解释

- Hash Join：一种实现 Join 关系代数的方式。它通过在 Join 的一侧构建 Hash Table 并在另一侧不断匹配 Hash Table 来得到 Join 的结果。
- Build Side：Hash Join 中用于构建 Hash Table 的一侧，称为 Build Side。本文默认以 Join 的右表作为 Build Side。
- Probe Side：Hash Join 中用于不断匹配 Hash Table 的一侧，称为 Probe Side。本文默认以 Join 的左表作为 Probe Side。
- Filter：也称谓词，在本文中指过滤条件。

## Runtime Filter 的原理

Hash Join 通过将右表的数据构建为 Hash Table，并将左表的数据不断匹配 Hash Table 来完成 Join。如果在匹配过程中，发现一部分 Join Key 值无法命中 Hash Table，则说明这部分数据不存在于右表，也不会出现在最终的 Join 结果中。因此，如果能够在扫描时**提前过滤掉这部分 Join Key 的数据**，将减少扫描时间和网络开销，从而大幅提升 Join 效率。

Runtime Filter 是在查询规划阶段生成的一种**动态取值谓词**。该谓词与 TiDB Selection 中的其他谓词具有相同作用，都应用于 Table Scan 操作上，用于筛选不满足谓词条件的行为。唯一的区别在于，Runtime Filter 中的参数取值来自于 Hash Join 构建过程中产生的结果。

### 示例

假设当前存在 `store_sales` 表与 `date_dim` 表的 Join 查询，它的 Join 方式为 Hash Join。`store_sales` 是一张事实表，主要存储门店销售数据，行数为 100 万。`date_dim` 是一张时间维度表，主要存储日期信息。当前想要查询 2001 年的销售数据，则 `date_dim` 表参与 Join 的数据量为 365 行。

```sql
SELECT * FROM store_sales, date_dim
WHERE ss_date_sk = d_date_sk
      AND d_year = 2001;
```

Hash Join 通常情况下的执行方式为：

```
                 +-------------------+
                 | PhysicalHashJoin  |
        +------->|                   |<------+
        |        +-------------------+       |
        |                                    |
        |                                    |
  100w  |                                    | 365
        |                                    |
        |                                    |
+-------+-------+                   +--------+-------+
| TableFullScan |                   | TableFullScan  |
|  store_sales  |                   |    date_dim    |
+---------------+                   +----------------+
```

*（上图为示意图，省略了 exchange 等节点）*

Runtime Filter 的执行方式如下：

1. 扫描 `date_dim` 的数据。
2. PhysicalHashJoin 根据 Build Side 数据计算出一个过滤条件，比如 `date_dim in (2001/01/01~2001/12/31)`。
3. 将该过滤条件发送给等待扫描 `store_sales` 的 TableFullScan。
4. `store_sales` 应用该过滤条件，并将过滤后的数据传递给 PhysicalHashJoin，从而减少 Probe Side 的扫表数据量以及匹配 Hash Table 的计算量。

```
                         2. Build RF values
            +-------->+-------------------+
            |         |PhysicalHashJoin   |<-----+
            |    +----+                   |      |
4. After RF |    |    +-------------------+      | 1. Scan T2
    5000    |    |3. Send RF                     |      365
            |    | filter data                   |
            |    |                               |
      +-----+----v------+                +-------+--------+
      |  TableFullScan  |                | TableFullScan  |
      |  store_sales    |                |    date_dim    |
      +-----------------+                +----------------+
```

* (上图中的 RF 是 Runtime Filter 的缩写) *

对比以上两个图可以看出，`store_sales` 的扫描量从 100 万减少到了 5000。通过减少 Table Full Scan 扫描的数据量，Runtime Filter 可以减少匹配 Hash Table 的次数，避免不必要的 I/O 和网络传输，从而显著提升了 Join 操作的效率。

## 使用 Runtime Filter

要使用 Runtime Filter，只需创建带 TiFlash 副本的表，并将 [`tidb_runtime_filter_mode`](/system-variables.md#tidb_runtime_filter_mode-从-v720-版本开始引入) 设置为 `LOCAL`。

本小节以 TPC-DS 的数据集为例，使用 `catalog_sales` 表和 `date_dim` 表进行 Join 操作，说明如何使用 Runtime Filter 提升查询效率。

### 第 1 步：创建表的 TiFlash 副本

给 `catalog_sales` 表和 `date_dim` 表分别增加一个 TiFlash 副本。

```sql
ALTER TABLE catalog_sales SET tiflash REPLICA 1;
ALTER TABLE date_dim SET tiflash REPLICA 1;
```

等待一段时间，并检查两个表的 TiFlash 副本已准备就绪，即副本的 `AVAILABLE` 字段和 `PROGRESS` 字段均为 `1`。

```sql
SELECT * FROM INFORMATION_SCHEMA.TIFLASH_REPLICA WHERE TABLE_NAME='catalog_sales';
+--------------+---------------+----------+---------------+-----------------+-----------+----------+
| TABLE_SCHEMA | TABLE_NAME    | TABLE_ID | REPLICA_COUNT | LOCATION_LABELS | AVAILABLE | PROGRESS |
+--------------+---------------+----------+---------------+-----------------+-----------+----------+
| tpcds50      | catalog_sales |     1055 |             1 |                 |         1 |        1 |
+--------------+---------------+----------+---------------+-----------------+-----------+----------+

mysql> SELECT * FROM INFORMATION_SCHEMA.TIFLASH_REPLICA WHERE TABLE_NAME='date_dim';
+--------------+------------+----------+---------------+-----------------+-----------+----------+
| TABLE_SCHEMA | TABLE_NAME | TABLE_ID | REPLICA_COUNT | LOCATION_LABELS | AVAILABLE | PROGRESS |
+--------------+------------+----------+---------------+-----------------+-----------+----------+
| tpcds50      | date_dim   |     1015 |             1 |                 |         1 |        1 |
+--------------+------------+----------+---------------+-----------------+-----------+----------+
```

### 第 2 步：开启 Runtime Filter

将系统变量 [`tidb_runtime_filter_mode`](/system-variables.md#tidb_runtime_filter_mode-从-v720-版本开始引入) 的值设置为 `LOCAL`，即开启 Runtime Filter。

```sql
SET tidb_runtime_filter_mode="LOCAL";
```

查看是否更改成功：

```sql
SHOW VARIABLES LIKE "tidb_runtime_filter_mode";
+--------------------------+-------+
| Variable_name            | Value |
+--------------------------+-------+
| tidb_runtime_filter_mode | LOCAL |
+--------------------------+-------+
```

系统变量的值显示为 `LOCAL`，则表示已成功开启 Runtime Filter。

### 第 3 步：执行查询

在进行查询之前，先查看一下查询计划。使用 [`EXPLAIN` 语句](/sql-statements/sql-statement-explain.md)来检查 Runtime Filter 是否已正确生效。

```sql
EXPLAIN SELECT cs_ship_date_sk FROM catalog_sales, date_dim
WHERE d_date = '2002-2-01' AND
     cs_ship_date_sk = d_date_sk;
```

当 Runtime Filter 启用时，可以看到 HashJoin 节点和 TableScan 节点上分别挂载了对应的 Runtime Filter，表示 Runtime Filter 规划成功。

```
TableFullScan: runtime filter:0[IN] -> tpcds50.catalog_sales.cs_ship_date_sk

HashJoin: runtime filter:0[IN] <- tpcds50.date_dim.d_date_sk |
```

完整的查询规划如下：

```
+----------------------------------------+-------------+--------------+---------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
| id                                     | estRows     | task         | access object       | operator info                                                                                                                                 |
+----------------------------------------+-------------+--------------+---------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
| TableReader_53                         | 37343.19    | root         |                     | MppVersion: 1, data:ExchangeSender_52                                                                                                         |
| └─ExchangeSender_52                    | 37343.19    | mpp[tiflash] |                     | ExchangeType: PassThrough                                                                                                                     |
|   └─Projection_51                      | 37343.19    | mpp[tiflash] |                     | tpcds50.catalog_sales.cs_ship_date_sk                                                                                                         |
|     └─HashJoin_48                      | 37343.19    | mpp[tiflash] |                     | inner join, equal:[eq(tpcds50.date_dim.d_date_sk, tpcds50.catalog_sales.cs_ship_date_sk)], runtime filter:0[IN] <- tpcds50.date_dim.d_date_sk |
|       ├─ExchangeReceiver_29(Build)     | 1.00        | mpp[tiflash] |                     |                                                                                                                                               |
|       │ └─ExchangeSender_28            | 1.00        | mpp[tiflash] |                     | ExchangeType: Broadcast, Compression: FAST                                                                                                    |
|       │   └─TableFullScan_26           | 1.00        | mpp[tiflash] | table:date_dim      | pushed down filter:eq(tpcds50.date_dim.d_date, 2002-02-01 00:00:00.000000), keep order:false                                                  |
|       └─Selection_31(Probe)            | 71638034.00 | mpp[tiflash] |                     | not(isnull(tpcds50.catalog_sales.cs_ship_date_sk))                                                                                            |
|         └─TableFullScan_30             | 71997669.00 | mpp[tiflash] | table:catalog_sales | pushed down filter:empty, keep order:false, runtime filter:0[IN] -> tpcds50.catalog_sales.cs_ship_date_sk                                     |
+----------------------------------------+-------------+--------------+---------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
9 rows in set (0.01 sec)
```

此时执行 SQL 查询，即可应用 Runtime Filter。

```sql
SELECT cs_ship_date_sk FROM catalog_sales, date_dim
WHERE d_date = '2002-2-01' AND
     cs_ship_date_sk = d_date_sk;
```

### 第 4 步：性能对比

以 TPC-DS 的 50 GB 数据量为例，开启 Runtime Filter 后，查询时间从 0.38 秒减少到 0.17 秒，效率提升 50%。通过 `ANALYZE` 语句可以查看 Runtime Filter 生效后各个算子的执行时间。

以下为未开启 Runtime Filter 时查询的执行信息：

```sql
EXPLAIN ANALYZE SELECT cs_ship_date_sk FROM catalog_sales, date_dim WHERE d_date = '2002-2-01' AND cs_ship_date_sk = d_date_sk;
+----------------------------------------+-------------+----------+--------------+---------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------+---------+------+
| id                                     | estRows     | actRows  | task         | access object       | execution info                                                                                                                                                                                                                                                                                                                                                                                    | operator info                                                                                | memory  | disk |
+----------------------------------------+-------------+----------+--------------+---------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------+---------+------+
| TableReader_53                         | 37343.19    | 59574    | root         |                     | time:379.7ms, loops:83, RU:0.000000, cop_task: {num: 48, max: 0s, min: 0s, avg: 0s, p95: 0s, copr_cache_hit_ratio: 0.00}                                                                                                                                                                                                                                                                          | MppVersion: 1, data:ExchangeSender_52                                                        | 12.0 KB | N/A  |
| └─ExchangeSender_52                    | 37343.19    | 59574    | mpp[tiflash] |                     | tiflash_task:{proc max:377ms, min:375.3ms, avg: 376.1ms, p80:377ms, p95:377ms, iters:1160, tasks:2, threads:16}                                                                                                                                                                                                                                                                                   | ExchangeType: PassThrough                                                                    | N/A     | N/A  |
|   └─Projection_51                      | 37343.19    | 59574    | mpp[tiflash] |                     | tiflash_task:{proc max:377ms, min:375.3ms, avg: 376.1ms, p80:377ms, p95:377ms, iters:1160, tasks:2, threads:16}                                                                                                                                                                                                                                                                                   | tpcds50.catalog_sales.cs_ship_date_sk                                                        | N/A     | N/A  |
|     └─HashJoin_48                      | 37343.19    | 59574    | mpp[tiflash] |                     | tiflash_task:{proc max:377ms, min:375.3ms, avg: 376.1ms, p80:377ms, p95:377ms, iters:1160, tasks:2, threads:16}                                                                                                                                                                                                                                                                                   | inner join, equal:[eq(tpcds50.date_dim.d_date_sk, tpcds50.catalog_sales.cs_ship_date_sk)]    | N/A     | N/A  |
|       ├─ExchangeReceiver_29(Build)     | 1.00        | 2        | mpp[tiflash] |                     | tiflash_task:{proc max:291.3ms, min:290ms, avg: 290.6ms, p80:291.3ms, p95:291.3ms, iters:2, tasks:2, threads:16}                                                                                                                                                                                                                                                                                  |                                                                                              | N/A     | N/A  |
|       │ └─ExchangeSender_28            | 1.00        | 1        | mpp[tiflash] |                     | tiflash_task:{proc max:290.9ms, min:0s, avg: 145.4ms, p80:290.9ms, p95:290.9ms, iters:1, tasks:2, threads:1}                                                                                                                                                                                                                                                                                      | ExchangeType: Broadcast, Compression: FAST                                                   | N/A     | N/A  |
|       │   └─TableFullScan_26           | 1.00        | 1        | mpp[tiflash] | table:date_dim      | tiflash_task:{proc max:3.88ms, min:0s, avg: 1.94ms, p80:3.88ms, p95:3.88ms, iters:1, tasks:2, threads:1}, tiflash_scan:{dtfile:{total_scanned_packs:2, total_skipped_packs:12, total_scanned_rows:16384, total_skipped_rows:97625, total_rs_index_load_time: 0ms, total_read_time: 0ms}, total_create_snapshot_time: 0ms, total_local_region_num: 1, total_remote_region_num: 0}                  | pushed down filter:eq(tpcds50.date_dim.d_date, 2002-02-01 00:00:00.000000), keep order:false | N/A     | N/A  |
|       └─Selection_31(Probe)            | 71638034.00 | 71638034 | mpp[tiflash] |                     | tiflash_task:{proc max:47ms, min:34.3ms, avg: 40.6ms, p80:47ms, p95:47ms, iters:1160, tasks:2, threads:16}                                                                                                                                                                                                                                                                                        | not(isnull(tpcds50.catalog_sales.cs_ship_date_sk))                                           | N/A     | N/A  |
|         └─TableFullScan_30             | 71997669.00 | 71997669 | mpp[tiflash] | table:catalog_sales | tiflash_task:{proc max:34ms, min:17.3ms, avg: 25.6ms, p80:34ms, p95:34ms, iters:1160, tasks:2, threads:16}, tiflash_scan:{dtfile:{total_scanned_packs:8893, total_skipped_packs:4007, total_scanned_rows:72056474, total_skipped_rows:32476901, total_rs_index_load_time: 8ms, total_read_time: 579ms}, total_create_snapshot_time: 0ms, total_local_region_num: 194, total_remote_region_num: 0} | pushed down filter:empty, keep order:false                                                   | N/A     | N/A  |
+----------------------------------------+-------------+----------+--------------+---------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------+---------+------+
9 rows in set (0.38 sec)
```

以下为开启 Runtime Filter 后的查询 Summary：

```sql
EXPLAIN ANALYZE SELECT cs_ship_date_sk FROM catalog_sales, date_dim
    -> WHERE d_date = '2002-2-01' AND
    ->      cs_ship_date_sk = d_date_sk;
+----------------------------------------+-------------+---------+--------------+---------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+---------+------+
| id                                     | estRows     | actRows | task         | access object       | execution info                                                                                                                                                                                                                                                                                                                                                                                       | operator info                                                                                                                                 | memory  | disk |
+----------------------------------------+-------------+---------+--------------+---------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+---------+------+
| TableReader_53                         | 37343.19    | 59574   | root         |                     | time:162.1ms, loops:82, RU:0.000000, cop_task: {num: 47, max: 0s, min: 0s, avg: 0s, p95: 0s, copr_cache_hit_ratio: 0.00}                                                                                                                                                                                                                                                                             | MppVersion: 1, data:ExchangeSender_52                                                                                                         | 12.7 KB | N/A  |
| └─ExchangeSender_52                    | 37343.19    | 59574   | mpp[tiflash] |                     | tiflash_task:{proc max:160.8ms, min:154.3ms, avg: 157.6ms, p80:160.8ms, p95:160.8ms, iters:86, tasks:2, threads:16}                                                                                                                                                                                                                                                                                  | ExchangeType: PassThrough                                                                                                                     | N/A     | N/A  |
|   └─Projection_51                      | 37343.19    | 59574   | mpp[tiflash] |                     | tiflash_task:{proc max:160.8ms, min:154.3ms, avg: 157.6ms, p80:160.8ms, p95:160.8ms, iters:86, tasks:2, threads:16}                                                                                                                                                                                                                                                                                  | tpcds50.catalog_sales.cs_ship_date_sk                                                                                                         | N/A     | N/A  |
|     └─HashJoin_48                      | 37343.19    | 59574   | mpp[tiflash] |                     | tiflash_task:{proc max:160.8ms, min:154.3ms, avg: 157.6ms, p80:160.8ms, p95:160.8ms, iters:86, tasks:2, threads:16}                                                                                                                                                                                                                                                                                  | inner join, equal:[eq(tpcds50.date_dim.d_date_sk, tpcds50.catalog_sales.cs_ship_date_sk)], runtime filter:0[IN] <- tpcds50.date_dim.d_date_sk | N/A     | N/A  |
|       ├─ExchangeReceiver_29(Build)     | 1.00        | 2       | mpp[tiflash] |                     | tiflash_task:{proc max:132.3ms, min:130.8ms, avg: 131.6ms, p80:132.3ms, p95:132.3ms, iters:2, tasks:2, threads:16}                                                                                                                                                                                                                                                                                   |                                                                                                                                               | N/A     | N/A  |
|       │ └─ExchangeSender_28            | 1.00        | 1       | mpp[tiflash] |                     | tiflash_task:{proc max:131ms, min:0s, avg: 65.5ms, p80:131ms, p95:131ms, iters:1, tasks:2, threads:1}                                                                                                                                                                                                                                                                                                | ExchangeType: Broadcast, Compression: FAST                                                                                                    | N/A     | N/A  |
|       │   └─TableFullScan_26           | 1.00        | 1       | mpp[tiflash] | table:date_dim      | tiflash_task:{proc max:3.01ms, min:0s, avg: 1.51ms, p80:3.01ms, p95:3.01ms, iters:1, tasks:2, threads:1}, tiflash_scan:{dtfile:{total_scanned_packs:2, total_skipped_packs:12, total_scanned_rows:16384, total_skipped_rows:97625, total_rs_index_load_time: 0ms, total_read_time: 0ms}, total_create_snapshot_time: 0ms, total_local_region_num: 1, total_remote_region_num: 0}                     | pushed down filter:eq(tpcds50.date_dim.d_date, 2002-02-01 00:00:00.000000), keep order:false                                                  | N/A     | N/A  |
|       └─Selection_31(Probe)            | 71638034.00 | 5308995 | mpp[tiflash] |                     | tiflash_task:{proc max:39.8ms, min:24.3ms, avg: 32.1ms, p80:39.8ms, p95:39.8ms, iters:86, tasks:2, threads:16}                                                                                                                                                                                                                                                                                       | not(isnull(tpcds50.catalog_sales.cs_ship_date_sk))                                                                                            | N/A     | N/A  |
|         └─TableFullScan_30             | 71997669.00 | 5335549 | mpp[tiflash] | table:catalog_sales | tiflash_task:{proc max:36.8ms, min:23.3ms, avg: 30.1ms, p80:36.8ms, p95:36.8ms, iters:86, tasks:2, threads:16}, tiflash_scan:{dtfile:{total_scanned_packs:660, total_skipped_packs:12451, total_scanned_rows:5335549, total_skipped_rows:100905778, total_rs_index_load_time: 2ms, total_read_time: 47ms}, total_create_snapshot_time: 0ms, total_local_region_num: 194, total_remote_region_num: 0} | pushed down filter:empty, keep order:false, runtime filter:0[IN] -> tpcds50.catalog_sales.cs_ship_date_sk                                     | N/A     | N/A  |
+----------------------------------------+-------------+---------+--------------+---------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+---------+------+
9 rows in set (0.17 sec)
```

对比两个查询的执行信息，可发现以下改进：

* IO 减少：对比 TableFullScan 算子的 `total_scanned_rows` 可知，开启 Runtime Filter 后 TableFullScan 的扫描量减少了 2/3 。
* Hash Join 性能提升：HashJoin 算子的执行耗时从 376.1ms 减少至 157.6ms。

### 最佳实践

Runtime Filter 适用于大表和小表进行 Join 的情况，比如事实表和维度表的关联查询。当维度表的命中的数据量较少时，意味着 Filter 的取值较少，事实表能更多地过滤掉不满足条件的数据。与默认情况下扫描整个事实表相比，这将显著提高查询性能。

例如，在 TPC-DS 中，泛 `Sales` 表和 `date_dim` 表的 Join 就是一个典型例子。

## 配置 Runtime Filter

在使用 Runtime Filter 时，你可以配置 Runtime Filter 的模式和谓词的类型。

### Runtime Filter Mode

Runtime Filter Mode 指的是 Runtime Filter 的模式，即 **生成 Filter 算子** 和 **接收 Filter 算子**之间的关系。共有三种模式：`OFF`、`LOCAL`、`GLOBAL`。在 v7.3.0 中仅支持 `OFF` 和 `LOCAL` 模式，通过系统变量 [`tidb_runtime_filter_mode`](/system-variables.md#tidb_runtime_filter_mode-从-v720-版本开始引入) 控制。

+ `OFF`：代表关闭 Runtime Filter。关闭后，查询行为和过去完全一致。
+ `LOCAL`：开启 LOCAL 模式的 Runtime Filter。LOCAL 模式指的是**生成 Filter 的算子**和**接收 Filter 的算子**在同一个 MPP Task 中。简单来说，Runtime Filter 可应用于 HashJoin 算子和 TableScan 算子在同一个 Task 中的情况。目前 Runtime Filter 仅支持 LOCAL 模式，要开启该模式，设置为 `LOCAL` 即可。
+ `GLOBAL`：目前不支持 GLOBAL 模式，不可设置为该模式。

### Runtime Filter Type

Runtime Filter Type 指的是 Runtime Filter 谓词的类型，即生成的 Filter 算子使用的谓词类型。目前只支持一种类型：`IN`，即生成的谓词类似于 `k1 in (xxx)`。通过系统变量 [`tidb_runtime_filter_type`](/system-variables.md#tidb_runtime_filter_type-从-v720-版本开始引入) 控制。

+ `IN`：默认为 `IN` 类型。即生成的 Runtime Filter 使用 `IN` 类型的谓词。

## 限制

+ Runtime Filter 是 MPP 架构下的优化，仅可应用于下推到 TiFlash 的查询。
+ Join 类型：Left outer、Full outer、Anti join（当左表为 Probe Side 时）均不支持生成 Runtime Filter。由于 Runtime Filter 会提前过滤参与 Join 的数据，这些类型的 Join 不会丢弃未匹配上的数据，所以无法使用该优化。
+ Equal Join expression：当等值 Join 表达式中的 Probe 列为复杂表达式，或者其类型为 JSON、Blob、Array 等复合类型时，也不会生成 Runtime Filter。主要原因是这类 Column 很少作为 Equal Join 的关联列，并且即使生成了 Filter，过滤率通常很低。

对于以上限制，如果你需要确认是否正确生成了 Runtime Filter，可以通过 [`EXPLAIN` 语句](/sql-statements/sql-statement-explain.md) 来验证。
