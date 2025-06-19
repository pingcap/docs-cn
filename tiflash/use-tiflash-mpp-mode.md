---
title: 使用 TiFlash MPP 模式
summary: 了解 TiFlash 的 MPP 模式及其使用方法。
---

# 使用 TiFlash MPP 模式

<CustomContent platform="tidb">

本文档介绍 TiFlash 的[大规模并行处理 (MPP)](/glossary.md#mpp) 模式及其使用方法。

</CustomContent>

<CustomContent platform="tidb-cloud">

本文档介绍 TiFlash 的[大规模并行处理 (MPP)](/tidb-cloud/tidb-cloud-glossary.md#mpp) 模式及其使用方法。

</CustomContent>

TiFlash 支持使用 MPP 模式执行查询，该模式在计算过程中引入了跨节点数据交换（数据 shuffle 过程）。TiDB 会根据优化器的成本估算自动决定是否选择 MPP 模式。你可以通过修改 [`tidb_allow_mpp`](/system-variables.md#tidb_allow_mpp-new-in-v50) 和 [`tidb_enforce_mpp`](/system-variables.md#tidb_enforce_mpp-new-in-v51) 的值来改变选择策略。

下图展示了 MPP 模式的工作原理。

![mpp-mode](/media/tiflash/tiflash-mpp.png)

## 控制是否选择 MPP 模式

`tidb_allow_mpp` 变量控制 TiDB 是否可以选择 MPP 模式来执行查询。`tidb_enforce_mpp` 变量控制是否忽略优化器的成本估算并强制使用 TiFlash 的 MPP 模式来执行查询。

这两个变量的所有取值对应的结果如下：

|                        | tidb_allow_mpp=off | tidb_allow_mpp=on（默认）              |
| ---------------------- | -------------------- | -------------------------------- |
| tidb_enforce_mpp=off（默认） | 不使用 MPP 模式 | 优化器根据成本估算选择是否使用 MPP 模式（默认）|
| tidb_enforce_mpp=on  | 不使用 MPP 模式   | TiDB 忽略成本估算，选择使用 MPP 模式      |

例如，如果你不想使用 MPP 模式，可以执行以下语句：

{{< copyable "sql" >}}

```sql
set @@session.tidb_allow_mpp=0;
```

如果你希望 TiDB 的基于成本的优化器自动决定是否使用 MPP 模式（默认），可以执行以下语句：

{{< copyable "sql" >}}

```sql
set @@session.tidb_allow_mpp=1;
set @@session.tidb_enforce_mpp=0;
```

如果你希望 TiDB 忽略优化器的成本估算并强制选择 MPP 模式，可以执行以下语句：

{{< copyable "sql" >}}

```sql
set @@session.tidb_allow_mpp=1;
set @@session.tidb_enforce_mpp=1;
```

<CustomContent platform="tidb">

`tidb_enforce_mpp` 会话变量的初始值等于该 tidb-server 实例的 [`enforce-mpp`](/tidb-configuration-file.md#enforce-mpp) 配置值（默认为 `false`）。如果 TiDB 集群中的多个 tidb-server 实例仅执行分析查询，并且你希望确保在这些实例上使用 MPP 模式，可以将它们的 [`enforce-mpp`](/tidb-configuration-file.md#enforce-mpp) 配置值更改为 `true`。

</CustomContent>

> **注意：**
>
> 当 `tidb_enforce_mpp=1` 生效时，TiDB 优化器将忽略成本估算来选择 MPP 模式。但是，如果其他因素阻止了 MPP 模式，TiDB 将不会选择 MPP 模式。这些因素包括缺少 TiFlash 副本、TiFlash 副本复制未完成，以及语句包含 MPP 模式不支持的运算符或函数。
>
> 如果 TiDB 优化器由于成本估算以外的原因无法选择 MPP 模式，当你使用 `EXPLAIN` 语句查看执行计划时，会返回一个警告来解释原因。例如：
>
> ```sql
> set @@session.tidb_enforce_mpp=1;
> create table t(a int);
> explain select count(*) from t;
> show warnings;
> ```
>
> ```
> +---------+------+-----------------------------------------------------------------------------+
> | Level   | Code | Message                                                                     |
> +---------+------+-----------------------------------------------------------------------------+
> | Warning | 1105 | MPP mode may be blocked because there aren't tiflash replicas of table `t`. |
> +---------+------+-----------------------------------------------------------------------------+
> ```

## MPP 模式支持的算法

MPP 模式支持以下物理算法：Broadcast Hash Join、Shuffled Hash Join、Shuffled Hash Aggregation、Union All、TopN 和 Limit。优化器会自动决定在查询中使用哪种算法。要查看具体的查询执行计划，可以执行 `EXPLAIN` 语句。如果 `EXPLAIN` 语句的结果显示 ExchangeSender 和 ExchangeReceiver 算子，则表示 MPP 模式已生效。

以下语句以 TPC-H 测试集中的表结构为例：

```sql
explain select count(*) from customer c join nation n on c.c_nationkey=n.n_nationkey;
+------------------------------------------+------------+--------------+---------------+----------------------------------------------------------------------------+
| id                                       | estRows    | task         | access object | operator info                                                              |
+------------------------------------------+------------+--------------+---------------+----------------------------------------------------------------------------+
| HashAgg_23                               | 1.00       | root         |               | funcs:count(Column#16)->Column#15                                          |
| └─TableReader_25                         | 1.00       | root         |               | data:ExchangeSender_24                                                     |
|   └─ExchangeSender_24                    | 1.00       | mpp[tiflash] |               | ExchangeType: PassThrough                                                  |
|     └─HashAgg_12                         | 1.00       | mpp[tiflash] |               | funcs:count(1)->Column#16                                                  |
|       └─HashJoin_17                      | 3000000.00 | mpp[tiflash] |               | inner join, equal:[eq(tpch.nation.n_nationkey, tpch.customer.c_nationkey)] |
|         ├─ExchangeReceiver_21(Build)     | 25.00      | mpp[tiflash] |               |                                                                            |
|         │ └─ExchangeSender_20            | 25.00      | mpp[tiflash] |               | ExchangeType: Broadcast                                                    |
|         │   └─TableFullScan_18           | 25.00      | mpp[tiflash] | table:n       | keep order:false                                                           |
|         └─TableFullScan_22(Probe)        | 3000000.00 | mpp[tiflash] | table:c       | keep order:false                                                           |
+------------------------------------------+------------+--------------+---------------+----------------------------------------------------------------------------+
9 rows in set (0.00 sec)
```

在示例执行计划中，包含了 `ExchangeReceiver` 和 `ExchangeSender` 算子。执行计划表明，在读取 `nation` 表后，`ExchangeSender` 算子将该表广播到每个节点，对 `nation` 表和 `customer` 表执行 `HashJoin` 和 `HashAgg` 操作，然后将结果返回给 TiDB。

TiFlash 提供以下 3 个全局/会话变量来控制是否使用 Broadcast Hash Join：

- [`tidb_broadcast_join_threshold_size`](/system-variables.md#tidb_broadcast_join_threshold_size-new-in-v50)：值的单位为字节。如果表大小（以字节为单位）小于该变量的值，则使用 Broadcast Hash Join 算法。否则，使用 Shuffled Hash Join 算法。
- [`tidb_broadcast_join_threshold_count`](/system-variables.md#tidb_broadcast_join_threshold_count-new-in-v50)：值的单位为行数。如果连接操作的对象属于子查询，优化器无法估计子查询结果集的大小，因此由结果集中的行数来决定。如果子查询的估计行数小于该变量的值，则使用 Broadcast Hash Join 算法。否则，使用 Shuffled Hash Join 算法。
- [`tidb_prefer_broadcast_join_by_exchange_data_size`](/system-variables.md#tidb_prefer_broadcast_join_by_exchange_data_size-new-in-v710)：控制是否使用网络传输开销最小的算法。如果启用此变量，TiDB 会分别估算使用 `Broadcast Hash Join` 和 `Shuffled Hash Join` 时在网络中交换的数据大小，然后选择大小较小的那个。启用此变量后，[`tidb_broadcast_join_threshold_count`](/system-variables.md#tidb_broadcast_join_threshold_count-new-in-v50) 和 [`tidb_broadcast_join_threshold_size`](/system-variables.md#tidb_broadcast_join_threshold_size-new-in-v50) 将不会生效。

## 在 MPP 模式下访问分区表

要在 MPP 模式下访问分区表，你需要先启用[动态裁剪模式](https://docs.pingcap.com/tidb/stable/partitioned-table#dynamic-pruning-mode)。

示例：

```sql
mysql> DROP TABLE if exists test.employees;
Query OK, 0 rows affected, 1 warning (0.00 sec)

mysql> CREATE TABLE test.employees
(id int(11) NOT NULL,
 fname varchar(30) DEFAULT NULL,
 lname varchar(30) DEFAULT NULL,
 hired date NOT NULL DEFAULT '1970-01-01',
 separated date DEFAULT '9999-12-31',
 job_code int DEFAULT NULL,
 store_id int NOT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
PARTITION BY RANGE (store_id)
(PARTITION p0 VALUES LESS THAN (6),
 PARTITION p1 VALUES LESS THAN (11),
 PARTITION p2 VALUES LESS THAN (16),
 PARTITION p3 VALUES LESS THAN (MAXVALUE));
Query OK, 0 rows affected (0.10 sec)

mysql> ALTER table test.employees SET tiflash replica 1;
Query OK, 0 rows affected (0.09 sec)

mysql> SET tidb_partition_prune_mode=static;
Query OK, 0 rows affected (0.00 sec)

mysql> explain SELECT count(*) FROM test.employees;
+----------------------------------+----------+-------------------+-------------------------------+-----------------------------------+
| id                               | estRows  | task              | access object                 | operator info                     |
+----------------------------------+----------+-------------------+-------------------------------+-----------------------------------+
| HashAgg_18                       | 1.00     | root              |                               | funcs:count(Column#10)->Column#9  |
| └─PartitionUnion_20              | 4.00     | root              |                               |                                   |
|   ├─StreamAgg_35                 | 1.00     | root              |                               | funcs:count(Column#12)->Column#10 |
|   │ └─TableReader_36             | 1.00     | root              |                               | data:StreamAgg_26                 |
|   │   └─StreamAgg_26             | 1.00     | batchCop[tiflash] |                               | funcs:count(1)->Column#12         |
|   │     └─TableFullScan_34       | 10000.00 | batchCop[tiflash] | table:employees, partition:p0 | keep order:false, stats:pseudo    |
|   ├─StreamAgg_52                 | 1.00     | root              |                               | funcs:count(Column#14)->Column#10 |
|   │ └─TableReader_53             | 1.00     | root              |                               | data:StreamAgg_43                 |
|   │   └─StreamAgg_43             | 1.00     | batchCop[tiflash] |                               | funcs:count(1)->Column#14         |
|   │     └─TableFullScan_51       | 10000.00 | batchCop[tiflash] | table:employees, partition:p1 | keep order:false, stats:pseudo    |
|   ├─StreamAgg_69                 | 1.00     | root              |                               | funcs:count(Column#16)->Column#10 |
|   │ └─TableReader_70             | 1.00     | root              |                               | data:StreamAgg_60                 |
|   │   └─StreamAgg_60             | 1.00     | batchCop[tiflash] |                               | funcs:count(1)->Column#16         |
|   │     └─TableFullScan_68       | 10000.00 | batchCop[tiflash] | table:employees, partition:p2 | keep order:false, stats:pseudo    |
|   └─StreamAgg_86                 | 1.00     | root              |                               | funcs:count(Column#18)->Column#10 |
|     └─TableReader_87             | 1.00     | root              |                               | data:StreamAgg_77                 |
|       └─StreamAgg_77             | 1.00     | batchCop[tiflash] |                               | funcs:count(1)->Column#18         |
|         └─TableFullScan_85       | 10000.00 | batchCop[tiflash] | table:employees, partition:p3 | keep order:false, stats:pseudo    |
+----------------------------------+----------+-------------------+-------------------------------+-----------------------------------+
18 rows in set (0,00 sec)

mysql> SET tidb_partition_prune_mode=dynamic;
Query OK, 0 rows affected (0.00 sec)

mysql> explain SELECT count(*) FROM test.employees;
+------------------------------+----------+--------------+-----------------+---------------------------------------------------------+
| id                           | estRows  | task         | access object   | operator info                                           |
+------------------------------+----------+--------------+-----------------+---------------------------------------------------------+
| HashAgg_17                   | 1.00     | root         |                 | funcs:count(Column#11)->Column#9                        |
| └─TableReader_19             | 1.00     | root         | partition:all   | data:ExchangeSender_18                                  |
|   └─ExchangeSender_18        | 1.00     | mpp[tiflash] |                 | ExchangeType: PassThrough                               |
|     └─HashAgg_8              | 1.00     | mpp[tiflash] |                 | funcs:count(1)->Column#11                               |
|       └─TableFullScan_16     | 10000.00 | mpp[tiflash] | table:employees | keep order:false, stats:pseudo, PartitionTableScan:true |
+------------------------------+----------+--------------+-----------------+---------------------------------------------------------+
5 rows in set (0,00 sec)
```
