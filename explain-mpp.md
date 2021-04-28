---
title: 用 EXPLAIN 查看 MPP 模式查询的执行计划
summary: 了解 TiDB 中 EXPLAIN 语句返回的执行计划信息。
---

# 用 EXPLAIN 查看 MPP 模式查询的执行计划

TiDB 支持使用 [MPP 模式](/tiflash/use-tiflash.md#使用-mpp-模式)来执行查询。在 MPP 执行模式下，SQL 优化器会生成 MPP 的执行计划。注意 MPP 模式仅对有 [TiFlash](/tiflash/tiflash-overview.md) 副本的表生效。

本文档使用的示例数据如下:

{{< copyable "sql" >}}

```sql
CREATE TABLE t1 (id int, value int);
INSERT INTO t1 values(1,2),(2,3),(1,3);
ALTER TABLE t1 set tiflash replica 1;
ANALYZE TABLE t1;
SET tidb_allow_mpp = 1;
```

## MPP 查询片段和 MPP 任务

在 MPP 模式下，一个查询在逻辑上会被切分为多个 MPP 查询片段 (query fragment)。示例如下：

{{< copyable "sql" >}}

```sql
EXPLAIN SELECT COUNT(*) FROM t1 GROUP BY id;
```

这个查询在 MPP 模式下会包含两个查询片段，一个为一阶段聚合，一个为二阶段聚合（最终聚合）。在查询执行的时候每个查询片段都会被实例化为一个或者多个 MPP 任务。

## Exchange 算子

MPP 查询的执行计划中有两个 MPP 特有的 Exchange 算子，分别为 ExchangeReceiver 和 ExchangeSender。ExchangeReceiver 表示从下游查询片段读取数据，ExchangeSender 表示下游查询片段向上游查询片段发送数据。在 MPP 执行模式下，每个 MPP 查询片段的根算子均为 ExchangeSender 算子，即每个查询片段以 ExchangeSender 为界进行划分。一个简单的 MPP 计划如下：

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

以上执行计划中有两个查询片段：

* `[TableFullScan_25, HashAgg_9, ExchangeSender_28]` 为第一个查询片段，其主要完成一阶段聚合的计算。
* `[ExchangeReceiver_29, HashAgg_27, Projection_26, ExchangeSender_30]` 为第二个查询片段，其主要完成二阶段聚合的计算。

ExchangeSender 算子的 `operator info` 列输出了 ExchangeType 信息。目前有以下三种 ExchangeType：

* HashPartition：ExchangeSender 把数据按 Hash 值进行分区之后分发给上游的 MPP 任务的 ExchangeReceiver 算子，通常在 Hash Aggregation 以及 Shuffle Hash Join 算法中使用。
* Broadcast：ExchangeSender 通过广播的方式把数据分发给上游的 MPP 任务，通常在 Broadcast Join 中使用。
* PassThrough：ExchangeSender 把数据分发给上游的 MPP Task，与 Broadcast 的区别是此时上游有且仅有一个 MPP 任务，通常用于向 TiDB 返回数据。

上述例子中 ExchangeSender 的 ExchangeType 为 HashPartition 以及 PassThrough，分别对应于 Hash Aggregation 运算以及向 TiDB 返回数据。

另外一个典型的 MPP 应用为 join 运算。TiDB MPP 支持两种类型的 join，分别为：

* Shuffle Hash Join：join 的 input 通过 HashPartition 的方式 shuffle 数据，上游的 MPP 任务进行分区内的 join。 
* Broadcast Join：join 中的小表以 Broadcast 的方式把数据广播到各个节点，各个节点各自进行 join。

典型的 Shuffle Hash Join 执行计划如下：

{{< copyable "sql" >}}

```sql
SET tidb_opt_broadcast_join=0; SET tidb_broadcast_join_threshold_count=0; SET tidb_broadcast_join_threshold_size=0; EXPLAIN SELECT COUNT(*) FROM t1 a JOIN t1 b ON a.id = b.id;
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

以上执行计划中，

* `[TableFullScan_20, Selection_21, ExchangeSender_22]` 完成表 b 的数据读取并通过 HashPartition 的方式把数据 shuffle 给上游 MPP 任务。
* `[TableFullScan_16, Selection_17, ExchangeSender_18]` 完成表 a 的数据读取并通过 HashPartition 的方式把数据 shuffle 给上游 MPP 任务。
* `[ExchangeReceiver_19, ExchangeReceiver_23, HashJoin_44, ExchangeSender_47]` 完成 join 并把数据返回给 TiDB。

典型的 Broadcast Join 执行计划如下：

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

以上执行计划中，

* `[TableFullScan_17, Selection_18, ExchangeSender_19]` 从小表读数据并广播给大表（表 a）数据所在的各个节点。
* `[TableFullScan_21, Selection_22, ExchangeReceiver_20, HashJoin_43, ExchangeSender_46]` 完成 join 并将数据返回给 TiDB。

## 对 MPP 模式的查询使用 `EXPLAIN ANALYZE`

`EXPLAIN ANALYZE` 语句与 `EXPLAIN` 类似，但还会输出一些运行时的信息。一个简单的 `EXPLAIN ANALYZE` 输出信息如下：

{{< copyable "sql" >}}

```sql
EXPLAIN ANALYZE SELECT COUNT(*) FROM t1 GROUP BY id;
```

```sql
+------------------------------------+---------+---------+-------------------+---------------+---------------------------------------------------------------------------------------------+----------------------------------------------------------------+--------+------+
| id                                 | estRows | actRows | task              | access object | execution info                                                                              | operator info                                                  | memory | disk |
+------------------------------------+---------+---------+-------------------+---------------+---------------------------------------------------------------------------------------------+----------------------------------------------------------------+--------+------+
| TableReader_31                     | 4.00    | 2       | root              |               | time:44.5ms, loops:2, cop_task: {num: 1, max: 0s, proc_keys: 0, copr_cache_hit_ratio: 0.00} | data:ExchangeSender_30                                         | N/A    | N/A  |
| └─ExchangeSender_30                | 4.00    | 2       | batchCop[tiflash] |               | tiflash_task:{time:16.5ms, loops:1, threads:1}                                              | ExchangeType: PassThrough, tasks: [2, 3, 4]                    | N/A    | N/A  |
|   └─Projection_26                  | 4.00    | 2       | batchCop[tiflash] |               | tiflash_task:{time:16.5ms, loops:1, threads:1}                                              | Column#4                                                       | N/A    | N/A  |
|     └─HashAgg_27                   | 4.00    | 2       | batchCop[tiflash] |               | tiflash_task:{time:16.5ms, loops:1, threads:1}                                              | group by:test.t1.id, funcs:sum(Column#7)->Column#4             | N/A    | N/A  |
|       └─ExchangeReceiver_29        | 4.00    | 2       | batchCop[tiflash] |               | tiflash_task:{time:14.5ms, loops:1, threads:20}                                             |                                                                | N/A    | N/A  |
|         └─ExchangeSender_28        | 4.00    | 0       | batchCop[tiflash] |               | tiflash_task:{time:9.49ms, loops:0, threads:0}                                              | ExchangeType: HashPartition, Hash Cols: test.t1.id, tasks: [1] | N/A    | N/A  |
|           └─HashAgg_9              | 4.00    | 0       | batchCop[tiflash] |               | tiflash_task:{time:9.49ms, loops:0, threads:0}                                              | group by:test.t1.id, funcs:count(1)->Column#7                  | N/A    | N/A  |
|             └─TableFullScan_25     | 6.00    | 0       | batchCop[tiflash] | table:t1      | tiflash_task:{time:9.49ms, loops:0, threads:0}                                              | keep order:false                                               | N/A    | N/A  |
+------------------------------------+---------+---------+-------------------+---------------+---------------------------------------------------------------------------------------------+----------------------------------------------------------------+--------+------+
```

与 `EXPLAIN` 相比，ExchangeSender 的 `operator info` 中多了 `task id` 的输出，其记录了该查询片段实例化成的 MPP 任务的任务 ID。此外 MPP 算子中都会有 `threads` 这一列，这列记录了 MPP 在执行该算子时使用的并发数（如果集群由多个节点组成，该并发数是所有节点并发数相加的结果）。

## 其他类型查询的执行计划

+ [索引查询的执行计划](/explain-indexes.md)
+ [Join 查询的执行计划](/explain-joins.md)
+ [子查询的执行计划](/explain-subqueries.md)
+ [聚合查询的执行计划](/explain-aggregation.md)
+ [视图查询的执行计划](/explain-views.md)
+ [分区查询的执行计划](/explain-partitions.md)
+ [开启 IndexMerge 查询的执行计划](/explain-index-merge.md)
