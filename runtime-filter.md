---
title: 运行时过滤器
summary: 了解运行时过滤器的工作原理及其使用方法。
---

# 运行时过滤器

运行时过滤器（Runtime Filter）是 TiDB v7.3 中引入的新特性，旨在提高 MPP 场景下哈希连接的性能。通过动态生成过滤器来预先过滤哈希连接的数据，TiDB 可以减少运行时的数据扫描量和哈希连接的计算量，最终提升查询性能。

## 概念

- 哈希连接（Hash join）：实现连接关系代数的一种方式。通过在一侧建立哈希表，另一侧持续匹配哈希表来获得连接结果。
- 构建侧（Build side）：哈希连接中用于构建哈希表的一侧。在本文档中，默认哈希连接的右表称为构建侧。
- 探测侧（Probe side）：哈希连接中用于持续匹配哈希表的一侧。在本文档中，默认哈希连接的左表称为探测侧。
- 过滤器（Filter）：也称为谓词（predicate），在本文档中指过滤条件。

## 运行时过滤器的工作原理

哈希连接通过基于右表构建哈希表并使用左表持续探测哈希表来执行连接操作。如果在探测过程中某些连接键值无法命中哈希表，这意味着该数据在右表中不存在，也不会出现在最终的连接结果中。因此，如果 TiDB 能够在扫描过程中**预先过滤掉连接键数据**，就会减少扫描时间和网络开销，从而大大提高连接效率。

运行时过滤器是在查询规划阶段生成的**动态谓词**。这个谓词与 TiDB Selection 算子中的其他谓词具有相同的功能。这些谓词都应用于 Table Scan 操作以过滤掉不符合谓词的行。唯一的区别是运行时过滤器中的参数值来自哈希连接构建过程中生成的结果。

### 示例

假设在 `store_sales` 表和 `date_dim` 表之间有一个连接查询，连接方式是哈希连接。`store_sales` 是一个事实表，主要存储商店的销售数据，行数为 100 万。`date_dim` 是一个时间维度表，主要存储日期信息。你想查询 2001 年的销售数据，因此 `date_dim` 表中有 365 行参与连接操作。

```sql
SELECT * FROM store_sales, date_dim
WHERE ss_date_sk = d_date_sk
    AND d_year = 2001;
```

哈希连接的执行计划通常如下：

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

*（上图省略了 exchange 节点和其他节点。）*

运行时过滤器的执行过程如下：

1. 扫描 `date_dim` 表的数据。
2. `PhysicalHashJoin` 根据构建侧的数据计算出一个过滤条件，如 `date_dim in (2001/01/01~2001/12/31)`。
3. 将过滤条件发送给正在等待扫描 `store_sales` 的 `TableFullScan` 算子。
4. 过滤条件应用于 `store_sales`，过滤后的数据传递给 `PhysicalHashJoin`，从而减少探测侧扫描的数据量和匹配哈希表的计算量。

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

*（RF 是 Runtime Filter 的缩写）*

从上面两个图中可以看到，`store_sales` 扫描的数据量从 100 万减少到了 5000。通过减少 `TableFullScan` 扫描的数据量，运行时过滤器可以减少匹配哈希表的次数，避免不必要的 I/O 和网络传输，从而显著提高连接操作的效率。
## 使用运行时过滤器

要使用运行时过滤器，你需要创建带有 TiFlash 副本的表，并将 [`tidb_runtime_filter_mode`](/system-variables.md#tidb_runtime_filter_mode-new-in-v720) 设置为 `LOCAL`。

以 TPC-DS 数据集为例，本节使用 `catalog_sales` 表和 `date_dim` 表进行连接操作，说明运行时过滤器如何提高查询效率。

### 步骤 1. 为要连接的表创建 TiFlash 副本

为 `catalog_sales` 表和 `date_dim` 表各添加一个 TiFlash 副本。

```sql
ALTER TABLE catalog_sales SET tiflash REPLICA 1;
ALTER TABLE date_dim SET tiflash REPLICA 1;
```

等待两个表的 TiFlash 副本就绪，即副本的 `AVAILABLE` 和 `PROGRESS` 字段都为 `1`。

```sql
SELECT * FROM INFORMATION_SCHEMA.TIFLASH_REPLICA WHERE TABLE_NAME='catalog_sales';
+--------------+---------------+----------+---------------+-----------------+-----------+----------+
| TABLE_SCHEMA | TABLE_NAME    | TABLE_ID | REPLICA_COUNT | LOCATION_LABELS | AVAILABLE | PROGRESS |
+--------------+---------------+----------+---------------+-----------------+-----------+----------+
| tpcds50      | catalog_sales |     1055 |             1 |                 |         1 |        1 |
+--------------+---------------+----------+---------------+-----------------+-----------+----------+

SELECT * FROM INFORMATION_SCHEMA.TIFLASH_REPLICA WHERE TABLE_NAME='date_dim';
+--------------+------------+----------+---------------+-----------------+-----------+----------+
| TABLE_SCHEMA | TABLE_NAME | TABLE_ID | REPLICA_COUNT | LOCATION_LABELS | AVAILABLE | PROGRESS |
+--------------+------------+----------+---------------+-----------------+-----------+----------+
| tpcds50      | date_dim   |     1015 |             1 |                 |         1 |        1 |
+--------------+------------+----------+---------------+-----------------+-----------+----------+
```

### 步骤 2. 启用运行时过滤器

要启用运行时过滤器，需要将系统变量 [`tidb_runtime_filter_mode`](/system-variables.md#tidb_runtime_filter_mode-new-in-v720) 的值设置为 `LOCAL`。

```sql
SET tidb_runtime_filter_mode="LOCAL";
```

检查更改是否成功：

```sql
SHOW VARIABLES LIKE "tidb_runtime_filter_mode";
+--------------------------+-------+
| Variable_name            | Value |
+--------------------------+-------+
| tidb_runtime_filter_mode | LOCAL |
+--------------------------+-------+
```

如果系统变量的值为 `LOCAL`，则运行时过滤器已启用。
### 步骤 3. 执行查询

在执行查询之前，使用 [`EXPLAIN` 语句](/sql-statements/sql-statement-explain.md)显示执行计划并检查运行时过滤器是否已生效。

```sql
EXPLAIN SELECT cs_ship_date_sk FROM catalog_sales, date_dim
WHERE d_date = '2002-2-01' AND
     cs_ship_date_sk = d_date_sk;
```

当运行时过滤器生效时，相应的运行时过滤器会挂载在 `HashJoin` 节点和 `TableScan` 节点上，表示运行时过滤器已成功应用。

```
TableFullScan: runtime filter:0[IN] -> tpcds50.catalog_sales.cs_ship_date_sk
HashJoin: runtime filter:0[IN] <- tpcds50.date_dim.d_date_sk |
```

完整的查询执行计划如下：

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

现在，执行 SQL 查询，运行时过滤器将被应用。

```sql
SELECT cs_ship_date_sk FROM catalog_sales, date_dim
WHERE d_date = '2002-2-01' AND
     cs_ship_date_sk = d_date_sk;
```
### 步骤 4. 性能对比

本示例使用 50 GB 的 TPC-DS 数据。启用运行时过滤器后，查询时间从 0.38 秒减少到 0.17 秒，效率提升了 50%。你可以使用 `ANALYZE` 语句查看运行时过滤器生效后各个算子的执行时间。

以下是未启用运行时过滤器时查询的执行信息：

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

以下是启用运行时过滤器时查询的执行信息：

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

通过比较两个查询的执行信息，你可以发现以下改进：

* IO 减少：通过比较 TableFullScan 算子的 `total_scanned_rows`，可以看到启用运行时过滤器后 `TableFullScan` 的扫描量减少了 2/3。
* 哈希连接性能提升：`HashJoin` 算子的执行时长从 376.1 ms 减少到 157.6 ms。

### 最佳实践

运行时过滤器适用于大表和小表连接的场景，例如事实表和维度表的连接查询。当维度表的命中数据量较小时，意味着过滤器的值较少，因此可以更有效地过滤掉事实表中不满足条件的数据。与默认扫描整个事实表的场景相比，这显著提高了查询性能。

TPC-DS 中 `Sales` 表和 `date_dim` 表的连接操作就是一个典型的例子。
## 配置运行时过滤器

在使用运行时过滤器时，你可以配置运行时过滤器的模式和谓词类型。

### 运行时过滤器模式

运行时过滤器的模式是**过滤器发送算子**和**过滤器接收算子**之间的关系。有三种模式：`OFF`、`LOCAL` 和 `GLOBAL`。在 v7.3.0 中，仅支持 `OFF` 和 `LOCAL` 模式。运行时过滤器模式由系统变量 [`tidb_runtime_filter_mode`](/system-variables.md#tidb_runtime_filter_mode-new-in-v720) 控制。

- `OFF`：运行时过滤器被禁用。禁用后，查询行为与之前版本相同。
- `LOCAL`：运行时过滤器以本地模式启用。在本地模式下，**过滤器发送算子**和**过滤器接收算子**在同一个 MPP 任务中。换句话说，运行时过滤器可以应用于 HashJoin 算子和 TableScan 算子在同一任务中的场景。目前，运行时过滤器仅支持本地模式。要启用此模式，请将其设置为 `LOCAL`。
- `GLOBAL`：目前不支持全局模式。你不能将运行时过滤器设置为此模式。

### 运行时过滤器类型

运行时过滤器的类型是生成的过滤器算子使用的谓词类型。目前仅支持一种类型：`IN`，这意味着生成的谓词类似于 `k1 in (xxx)`。运行时过滤器类型由系统变量 [`tidb_runtime_filter_type`](/system-variables.md#tidb_runtime_filter_type-new-in-v720) 控制。

- `IN`：默认类型。表示生成的运行时过滤器使用 `IN` 类型谓词。

## 限制

- 运行时过滤器是 MPP 架构中的优化，只能应用于下推到 TiFlash 的查询。
- 连接类型：Left outer、Full outer 和 Anti join（当左表是探测侧时）不支持运行时过滤器。因为运行时过滤器会预先过滤参与连接的数据，而上述连接类型不会丢弃不匹配的数据，所以不能使用运行时过滤器。
- 等值连接表达式：当等值连接表达式中的探测列是复杂表达式时，或者当探测列类型是 JSON、Blob、Array 或其他复杂数据类型时，不会生成运行时过滤器。主要原因是上述类型的列很少用作连接列。即使生成了过滤器，过滤率通常也很低。

对于上述限制，如果你需要确认运行时过滤器是否正确生成，可以使用 [`EXPLAIN` 语句](/sql-statements/sql-statement-explain.md)验证执行计划。
