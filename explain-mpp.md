---
title: MPP 模式下的 EXPLAIN 语句
summary: 了解 TiDB 中 EXPLAIN 语句返回的 MPP 执行计划信息。
---

# MPP 模式下的 EXPLAIN 语句

TiDB 支持使用 [MPP 模式](/tiflash/use-tiflash-mpp-mode.md) 执行查询。在 MPP 模式下，TiDB 优化器会生成 MPP 执行计划。请注意，MPP 模式仅适用于在 [TiFlash](/tiflash/tiflash-overview.md) 上有副本的表。

本文档中的示例基于以下示例数据：

{{< copyable "sql" >}}

```sql
CREATE TABLE t1 (id int, value int);
INSERT INTO t1 values(1,2),(2,3),(1,3);
ALTER TABLE t1 set tiflash replica 1;
ANALYZE TABLE t1;
SET tidb_allow_mpp = 1;
```

## MPP 查询片段和 MPP 任务

在 MPP 模式下，查询在逻辑上被切分为多个查询片段。以下面的语句为例：

{{< copyable "sql" >}}

```sql
EXPLAIN SELECT COUNT(*) FROM t1 GROUP BY id;
```

这个查询在 MPP 模式下被分为两个片段。一个用于第一阶段聚合，另一个用于第二阶段聚合（也是最终聚合）。当执行这个查询时，每个查询片段会被实例化为一个或多个 MPP 任务。

## Exchange 算子

`ExchangeReceiver` 和 `ExchangeSender` 是 MPP 执行计划特有的两个 exchange 算子。`ExchangeReceiver` 算子从下游查询片段读取数据，而 `ExchangeSender` 算子将数据从下游查询片段发送到上游查询片段。在 MPP 模式下，每个 MPP 查询片段的根算子都是 `ExchangeSender`，这意味着查询片段是由 `ExchangeSender` 算子划分的。

以下是一个简单的 MPP 执行计划：

{{< copyable "sql" >}}

```sql
EXPLAIN SELECT COUNT(*) FROM t1 GROUP BY id;
```

```sql
+------------------------------------+---------+-------------------+---------------+----------------------------------------------------+
| id                                 | estRows | task              | access object | operator info                                      |
+------------------------------------+---------+-------------------+---------------+----------------------------------------------------+
| TableReader_31                     | 2.00    | root              |               | data:ExchangeSender_30                             |
| └─ExchangeSender_30                | 2.00    | batchCop[tiflash] |               | ExchangeType: PassThrough                          |
|   └─Projection_26                  | 2.00    | batchCop[tiflash] |               | Column#4                                           |
|     └─HashAgg_27                   | 2.00    | batchCop[tiflash] |               | group by:test.t1.id, funcs:sum(Column#7)->Column#4 |
|       └─ExchangeReceiver_29        | 2.00    | batchCop[tiflash] |               |                                                    |
|         └─ExchangeSender_28        | 2.00    | batchCop[tiflash] |               | ExchangeType: HashPartition, Hash Cols: test.t1.id |
|           └─HashAgg_9              | 2.00    | batchCop[tiflash] |               | group by:test.t1.id, funcs:count(1)->Column#7      |
|             └─TableFullScan_25     | 3.00    | batchCop[tiflash] | table:t1      | keep order:false                                   |
+------------------------------------+---------+-------------------+---------------+----------------------------------------------------+
```

上述执行计划包含两个查询片段：

* 第一个是 `[TableFullScan_25, HashAgg_9, ExchangeSender_28]`，主要负责第一阶段聚合。
* 第二个是 `[ExchangeReceiver_29, HashAgg_27, Projection_26, ExchangeSender_30]`，主要负责第二阶段聚合。

`ExchangeSender` 算子的 `operator info` 列显示了 exchange 类型信息。目前有三种 exchange 类型：

* HashPartition：`ExchangeSender` 算子首先根据 Hash 值对数据进行分区，然后将数据分发给上游 MPP 任务的 `ExchangeReceiver` 算子。这种 exchange 类型通常用于 Hash 聚合和 Shuffle Hash Join 算法。
* Broadcast：`ExchangeSender` 算子通过广播方式将数据分发给上游 MPP 任务。这种 exchange 类型通常用于 Broadcast Join。
* PassThrough：`ExchangeSender` 算子将数据发送给唯一的上游 MPP 任务，这与 Broadcast 类型不同。这种 exchange 类型通常用于向 TiDB 返回数据。

在示例执行计划中，算子 `ExchangeSender_28` 的 exchange 类型是 HashPartition，表示它执行 Hash 聚合算法。算子 `ExchangeSender_30` 的 exchange 类型是 PassThrough，表示它用于向 TiDB 返回数据。

MPP 也经常应用于连接操作。TiDB 中的 MPP 模式支持以下两种连接算法：

* Shuffle Hash Join：使用 HashPartition exchange 类型对连接操作的数据输入进行 shuffle。然后，上游 MPP 任务对同一分区内的数据进行连接。
* Broadcast Join：将连接操作中小表的数据广播到每个节点，然后每个节点分别进行数据连接。

以下是一个典型的 Shuffle Hash Join 执行计划：

{{< copyable "sql" >}}

```sql
SET tidb_broadcast_join_threshold_count=0;
SET tidb_broadcast_join_threshold_size=0;
EXPLAIN SELECT COUNT(*) FROM t1 a JOIN t1 b ON a.id = b.id;
```

```sql
+----------------------------------------+---------+--------------+---------------+----------------------------------------------------+
| id                                     | estRows | task         | access object | operator info                                      |
+----------------------------------------+---------+--------------+---------------+----------------------------------------------------+
| StreamAgg_14                           | 1.00    | root         |               | funcs:count(1)->Column#7                           |
| └─TableReader_48                       | 9.00    | root         |               | data:ExchangeSender_47                             |
|   └─ExchangeSender_47                  | 9.00    | cop[tiflash] |               | ExchangeType: PassThrough                          |
|     └─HashJoin_44                      | 9.00    | cop[tiflash] |               | inner join, equal:[eq(test.t1.id, test.t1.id)]     |
|       ├─ExchangeReceiver_19(Build)     | 6.00    | cop[tiflash] |               |                                                    |
|       │ └─ExchangeSender_18            | 6.00    | cop[tiflash] |               | ExchangeType: HashPartition, Hash Cols: test.t1.id |
|       │   └─Selection_17               | 6.00    | cop[tiflash] |               | not(isnull(test.t1.id))                            |
|       │     └─TableFullScan_16         | 6.00    | cop[tiflash] | table:a       | keep order:false                                   |
|       └─ExchangeReceiver_23(Probe)     | 6.00    | cop[tiflash] |               |                                                    |
|         └─ExchangeSender_22            | 6.00    | cop[tiflash] |               | ExchangeType: HashPartition, Hash Cols: test.t1.id |
|           └─Selection_21               | 6.00    | cop[tiflash] |               | not(isnull(test.t1.id))                            |
|             └─TableFullScan_20         | 6.00    | cop[tiflash] | table:b       | keep order:false                                   |
+----------------------------------------+---------+--------------+---------------+----------------------------------------------------+
12 rows in set (0.00 sec)
```

在上述执行计划中：

* 查询片段 `[TableFullScan_20, Selection_21, ExchangeSender_22]` 从表 b 读取数据并将数据 shuffle 到上游 MPP 任务。
* 查询片段 `[TableFullScan_16, Selection_17, ExchangeSender_18]` 从表 a 读取数据并将数据 shuffle 到上游 MPP 任务。
* 查询片段 `[ExchangeReceiver_19, ExchangeReceiver_23, HashJoin_44, ExchangeSender_47]` 连接所有数据并将其返回给 TiDB。

以下是一个典型的 Broadcast Join 执行计划：

{{< copyable "sql" >}}

```sql
EXPLAIN SELECT COUNT(*) FROM t1 a JOIN t1 b ON a.id = b.id;
```

```sql
+----------------------------------------+---------+--------------+---------------+------------------------------------------------+
| id                                     | estRows | task         | access object | operator info                                  |
+----------------------------------------+---------+--------------+---------------+------------------------------------------------+
| StreamAgg_15                           | 1.00    | root         |               | funcs:count(1)->Column#7                       |
| └─TableReader_47                       | 9.00    | root         |               | data:ExchangeSender_46                         |
|   └─ExchangeSender_46                  | 9.00    | cop[tiflash] |               | ExchangeType: PassThrough                      |
|     └─HashJoin_43                      | 9.00    | cop[tiflash] |               | inner join, equal:[eq(test.t1.id, test.t1.id)] |
|       ├─ExchangeReceiver_20(Build)     | 6.00    | cop[tiflash] |               |                                                |
|       │ └─ExchangeSender_19            | 6.00    | cop[tiflash] |               | ExchangeType: Broadcast                        |
|       │   └─Selection_18               | 6.00    | cop[tiflash] |               | not(isnull(test.t1.id))                        |
|       │     └─TableFullScan_17         | 6.00    | cop[tiflash] | table:a       | keep order:false                               |
|       └─Selection_22(Probe)            | 6.00    | cop[tiflash] |               | not(isnull(test.t1.id))                        |
|         └─TableFullScan_21             | 6.00    | cop[tiflash] | table:b       | keep order:false                               |
+----------------------------------------+---------+--------------+---------------+------------------------------------------------+
```

在上述执行计划中：

* 查询片段 `[TableFullScan_17, Selection_18, ExchangeSender_19]` 从小表（表 a）读取数据，并将数据广播到包含大表（表 b）数据的每个节点。
* 查询片段 `[TableFullScan_21, Selection_22, ExchangeReceiver_20, HashJoin_43, ExchangeSender_46]` 连接所有数据并将其返回给 TiDB。

## MPP 模式下的 `EXPLAIN ANALYZE` 语句

`EXPLAIN ANALYZE` 语句与 `EXPLAIN` 类似，但它还会输出一些运行时信息。

以下是一个简单的 `EXPLAIN ANALYZE` 示例输出：

{{< copyable "sql" >}}

```sql
EXPLAIN ANALYZE SELECT COUNT(*) FROM t1 GROUP BY id;
```

```sql
+------------------------------------+---------+---------+-------------------+---------------+---------------------------------------------------------------------------------------------------+----------------------------------------------------------------+--------+------+
| id                                 | estRows | actRows | task              | access object | execution info                                                                                    | operator info                                                  | memory | disk |
+------------------------------------+---------+---------+-------------------+---------------+---------------------------------------------------------------------------------------------------+----------------------------------------------------------------+--------+------+
| TableReader_31                     | 4.00    | 2       | root              |               | time:44.5ms, loops:2, cop_task: {num: 1, max: 0s, proc_keys: 0, copr_cache_hit_ratio: 0.00}       | data:ExchangeSender_30                                         | N/A    | N/A  |
| └─ExchangeSender_30                | 4.00    | 2       | batchCop[tiflash] |               | tiflash_task:{time:16.5ms, loops:1, threads:1}                                                    | ExchangeType: PassThrough, tasks: [2, 3, 4]                    | N/A    | N/A  |
|   └─Projection_26                  | 4.00    | 2       | batchCop[tiflash] |               | tiflash_task:{time:16.5ms, loops:1, threads:1}                                                    | Column#4                                                       | N/A    | N/A  |
|     └─HashAgg_27                   | 4.00    | 2       | batchCop[tiflash] |               | tiflash_task:{time:16.5ms, loops:1, threads:1}                                                    | group by:test.t1.id, funcs:sum(Column#7)->Column#4             | N/A    | N/A  |
|       └─ExchangeReceiver_29        | 4.00    | 2       | batchCop[tiflash] |               | tiflash_task:{time:14.5ms, loops:1, threads:20}                                                   |                                                                | N/A    | N/A  |
|         └─ExchangeSender_28        | 4.00    | 0       | batchCop[tiflash] |               | tiflash_task:{time:9.49ms, loops:0, threads:0}                                                    | ExchangeType: HashPartition, Hash Cols: test.t1.id, tasks: [1] | N/A    | N/A  |
|           └─HashAgg_9              | 4.00    | 0       | batchCop[tiflash] |               | tiflash_task:{time:9.49ms, loops:0, threads:0}                                                    | group by:test.t1.id, funcs:count(1)->Column#7                  | N/A    | N/A  |
|             └─TableFullScan_25     | 6.00    | 0       | batchCop[tiflash] | table:t1      | tiflash_task:{time:9.49ms, loops:0, threads:0}, tiflash_scan:{dtfile:{total_scanned_packs:1,...}} | keep order:false                                               | N/A    | N/A  |
+------------------------------------+---------+---------+-------------------+---------------+---------------------------------------------------------------------------------------------------+----------------------------------------------------------------+--------+------+
```

与 `EXPLAIN` 的输出相比，`ExchangeSender` 算子的 `operator info` 列还显示了 `tasks`，它记录了查询片段实例化成的 MPP 任务的 id。此外，每个 MPP 算子在 `execution info` 列中都有一个 `threads` 字段，它记录了 TiDB 执行此算子时的并发度。如果集群由多个节点组成，这个并发度是所有节点并发度的总和。

## MPP 版本和数据交换压缩

从 v6.6.0 开始，MPP 执行计划中新增了 `MPPVersion` 和 `Compression` 字段。

- `MppVersion`：MPP 执行计划的版本号，可以通过系统变量 [`mpp_version`](/system-variables.md#mpp_version-new-in-v660) 设置。
- `Compression`：`Exchange` 算子的数据压缩模式，可以通过系统变量 [`mpp_exchange_compression_mode`](/system-variables.md#mpp_exchange_compression_mode-new-in-v660) 设置。如果未启用数据压缩，执行计划中不会显示此字段。

请看以下示例：

```sql
mysql > EXPLAIN SELECT COUNT(*) AS count_order FROM lineitem GROUP BY l_returnflag, l_linestatus ORDER BY l_returnflag, l_linestatus;

+----------------------------------------+--------------+--------------+----------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| id                                     | estRows      | task         | access object  | operator info                                                                                                                                                                                                                                                                        |
+----------------------------------------+--------------+--------------+----------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Projection_6                           | 3.00         | root         |                | Column#18                                                                                                                                                                                                                                                                            |
| └─Sort_8                               | 3.00         | root         |                | tpch100.lineitem.l_returnflag, tpch100.lineitem.l_linestatus                                                                                                                                                                                                                         |
|   └─TableReader_36                     | 3.00         | root         |                | MppVersion: 1, data:ExchangeSender_35                                                                                                                                                                                                                                                |
|     └─ExchangeSender_35                | 3.00         | mpp[tiflash] |                | ExchangeType: PassThrough                                                                                                                                                                                                                                                            |
|       └─Projection_31                  | 3.00         | mpp[tiflash] |                | Column#18, tpch100.lineitem.l_returnflag, tpch100.lineitem.l_linestatus                                                                                                                                                                                                              |
|         └─HashAgg_32                   | 3.00         | mpp[tiflash] |                | group by:tpch100.lineitem.l_linestatus, tpch100.lineitem.l_returnflag, funcs:sum(Column#23)->Column#18, funcs:firstrow(tpch100.lineitem.l_returnflag)->tpch100.lineitem.l_returnflag, funcs:firstrow(tpch100.lineitem.l_linestatus)->tpch100.lineitem.l_linestatus, stream_count: 20 |
|           └─ExchangeReceiver_34        | 3.00         | mpp[tiflash] |                | stream_count: 20                                                                                                                                                                                                                                                                     |
|             └─ExchangeSender_33        | 3.00         | mpp[tiflash] |                | ExchangeType: HashPartition, Compression: FAST, Hash Cols: [name: tpch100.lineitem.l_returnflag, collate: utf8mb4_bin], [name: tpch100.lineitem.l_linestatus, collate: utf8mb4_bin], stream_count: 20                                                                                |
|               └─HashAgg_14             | 3.00         | mpp[tiflash] |                | group by:tpch100.lineitem.l_linestatus, tpch100.lineitem.l_returnflag, funcs:count(1)->Column#23                                                                                                                                                                                     |
|                 └─TableFullScan_30     | 600037902.00 | mpp[tiflash] | table:lineitem | keep order:false                                                                                                                                                                                                                                                                     |
+----------------------------------------+--------------+--------------+----------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
```

在上述执行计划结果中，TiDB 使用版本为 `1` 的 MPP 执行计划来构建 `TableReader`。`HashPartition` 类型的 `ExchangeSender` 算子使用 `FAST` 数据压缩模式。`PassThrough` 类型的 `ExchangeSender` 算子未启用数据压缩。
