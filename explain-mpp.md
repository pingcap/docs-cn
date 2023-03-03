---
title: Explain Statements in the MPP Mode
summary: Learn about the execution plan information returned by the EXPLAIN statement in TiDB.
---

# Explain Statements in the MPP Mode

TiDB supports using the [MPP mode](/tiflash/use-tiflash-mpp-mode.md) to execute queries. In the MPP mode, the TiDB optimizer generates execution plans for MPP. Note that the MPP mode is only available for tables that have replicas on [TiFlash](/tiflash/tiflash-overview.md).

The examples in this document are based on the following sample data:

{{< copyable "sql" >}}

```sql
CREATE TABLE t1 (id int, value int);
INSERT INTO t1 values(1,2),(2,3),(1,3);
ALTER TABLE t1 set tiflash replica 1;
ANALYZE TABLE t1;
SET tidb_allow_mpp = 1;
```

## MPP query fragments and MPP tasks

In the MPP mode, a query is logically sliced into multiple query fragments. Take the following statement as an example:

{{< copyable "sql" >}}

```sql
EXPLAIN SELECT COUNT(*) FROM t1 GROUP BY id;
```

This query is divided into two fragments in the MPP mode. One for the first-stage aggregation and the other for the second-stage aggregation, also the final aggregation. When this query is executed, each query fragment is instantiated into one or more MPP tasks.

## Exchange operators

`ExchangeReceiver` and `ExchangeSender`are two exchange operators specific for MPP execution plans. The `ExchangeReceiver` operator reads data from downstream query fragments and the `ExchangeSender` operator sends data from downstream query fragments to upstream query fragments. In the MPP mode, the root operator of each MPP query fragment is `ExchangeSender`, meaning that query fragments are delimited by the `ExchangeSender` operator.

The following is a simple MPP execution plan:

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

The above execution plan contains two query fragments:

* The first is `[TableFullScan_25, HashAgg_9, ExchangeSender_28]`, which is mainly responsible for the first-stage aggregation.
* The second is `[ExchangeReceiver_29, HashAgg_27, Projection_26, ExchangeSender_30]`, which is mainly responsible for the second-stage aggregation.

The `operator info` column of the `ExchangeSender` operator shows the exchange type information. Currently, there are three exchange types. See the following:

* HashPartition: The `ExchangeSender` operator firstly partitions data according to the Hash values and then distributes data to the `ExchangeReceiver` operator of upstream MPP tasks. This exchange type is often used for Hash Aggregation and Shuffle Hash Join algorithms.
* Broadcast: The `ExchangeSender` operator distributes data to upstream MPP tasks through broadcast. This exchange type is often used for Broadcast Join.
* PassThrough: The `ExchangeSender` operator sends data to the only upstream MPP task, which is different from the Broadcast type. This exchange type is often used when returning data to TiDB.

In the example execution plan, the exchange type of the operator `ExchangeSender_28` is HashPartition, meaning that it performs the Hash Aggregation algorithm. The exchange type of the operator `ExchangeSender_30` is PassThrough, meaning that it is used to return data to TiDB.

MPP is also often applied to join operations. The MPP mode in TiDB supports the following two join algorithms:

* Shuffle Hash Join: Shuffle the data input from the join operation using the HashPartition exchange type. Then, upstream MPP tasks join data within the same partition.
* Broadcast Join: Broadcast data of the small table in the join operation to each node, after which each node joins the data separately.

The following is a typical execution plan for Shuffle Hash Join:

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

In the above execution plan:

* The query fragment `[TableFullScan_20, Selection_21, ExchangeSender_22]` reads data from table b and shuffles data to upstream MPP tasks.
* The query fragment `[TableFullScan_16, Selection_17, ExchangeSender_18]` reads data from table a and shuffles data to upstream MPP tasks.
* The query fragment `[ExchangeReceiver_19, ExchangeReceiver_23, HashJoin_44, ExchangeSender_47]` joins all data and returns it to TiDB.

A typical execution plan for Broadcast Join is as follows:

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

In the above execution plan:

* The query fragment `[TableFullScan_17, Selection_18, ExchangeSender_19]` reads data from the small table (table a) and broadcasts the data to each node that contains data from the large table (table b).
* The query fragment `[TableFullScan_21, Selection_22, ExchangeReceiver_20, HashJoin_43, ExchangeSender_46]` joins all data and returns it to TiDB.

## `EXPLAIN ANALYZE` statements in the MPP mode

The `EXPLAIN ANALYZE` statement is similar to `EXPLAIN`, but it also outputs some runtime information.

The following is the output of a simple `EXPLAIN ANALYZE` example:

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

Compared to the output of `EXPLAIN`, the `operator info` column of the operator `ExchangeSender` also shows `tasks`, which records the id of the MPP task that the query fragment instantiates into. In addition, each MPP operator has a `threads` field in the `execution info` column, which records the concurrency of operations when TiDB executes this operator. If the cluster consists of multiple nodes, this concurrency is the result of adding up the concurrency of all nodes.

## MPP version and exchange data compression

Starting from v6.6.0, the new fields `MPPVersion` and `Compression` are added to the MPP execution plan.

- `MppVersion`: The version number of the MPP execution plan, which can be set through the system variable [`mpp_version`](/system-variables.md#mpp_version-new-in-v660).
- `Compression`: The data compression mode of the `Exchange` operator, which can be set through the system variable [`mpp_exchange_compression_mode`](/system-variables.md#mpp_exchange_compression_mode-new-in-v660). If data compression is not enabled, this field is not displayed in the execution plan.

See the following example:

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

In the preceding execution plan result, TiDB uses an MPP execution plan of version `1` to build `TableReader`. The `ExchangeSender` operator of the `HashPartition` type uses the `FAST` data compression mode. Data compression is not enabled for the `ExchangeSender` operator of the `PassThrough` type.
