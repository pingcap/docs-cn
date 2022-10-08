---
title: 使用 MPP 模式
summary: 了解如何使用 MPP 模式。
---

# 使用 MPP 模式

本文档介绍 TiFlash 的 MPP 模式及其使用方法。

TiFlash 支持 MPP 模式的查询执行，即在计算中引入跨节点的数据交换（data shuffle 过程）。TiDB 默认由优化器自动选择是否使用 MPP 模式，你可以通过修改变量 [`tidb_allow_mpp`](/system-variables.md#tidb_allow_mpp-从-v50-版本开始引入) 和 [`tidb_enforce_mpp`](/system-variables.md#tidb_enforce_mpp-从-v51-版本开始引入) 的值来更改选择策略。

## 控制是否选择 MPP 模式

变量 `tidb_allow_mpp` 控制 TiDB 能否选择 MPP 模式执行查询。变量 `tidb_enforce_mpp` 控制是否忽略优化器代价估算，强制使用 TiFlash 的 MPP 模式执行查询。

这两个变量所有取值对应的结果如下：

|                        | tidb_allow_mpp=off | tidb_allow_mpp=on（默认）              |
| ---------------------- | -------------------- | -------------------------------- |
| tidb_enforce_mpp=off（默认） | 不使用 MPP 模式。  | 优化器根据代价估算选择。（默认） |
| tidb_enforce_mpp=on  | 不使用 MPP 模式。  | TiDB 无视代价估算，选择 MPP 模式。      |

例如，如果你不想使用 MPP 模式，可以通过以下语句来设置：

{{< copyable "sql" >}}

```sql
set @@session.tidb_allow_mpp=0;
```

如果想要通过优化器代价估算来智能选择是否使用 MPP（默认情况），可以通过如下语句来设置：

{{< copyable "sql" >}}

```sql
set @@session.tidb_allow_mpp=1;
set @@session.tidb_enforce_mpp=0;
```

如果想要 TiDB 忽略优化器的代价估算，强制使用 MPP，可以通过如下语句来设置：

{{< copyable "sql" >}}

```sql
set @@session.tidb_allow_mpp=1;
set @@session.tidb_enforce_mpp=1;
```

Session 变量 `tidb_enforce_mpp` 的初始值等于这台 tidb-server 实例的 [`enforce-mpp`](/tidb-configuration-file.md#enforce-mpp) 配置项值（默认为 `false`）。在一个 TiDB 集群中，如果有若干台 tidb-server 实例只执行分析型查询，要确保它们能够选中 MPP 模式，你可以将它们的 [`enforce-mpp`](/tidb-configuration-file.md#enforce-mpp) 配置值修改为 `true`.

> **注意：**
>
> `tidb_enforce_mpp=1` 在生效时，TiDB 优化器会忽略代价估算选择 MPP 模式。但如果存在其它不支持 MPP 的因素，例如没有 TiFlash 副本、TiFlash 副本同步未完成、语句中含有 MPP 模式不支持的算子或函数等，那么 TiDB 仍然不会选择 MPP 模式。
>
> 如果由于代价估算之外的原因导致 TiDB 优化器无法选择 MPP，在你使用 `EXPLAIN` 语句查看执行计划时，会返回警告说明原因，例如：
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

## MPP 模式的算法支持

MPP 模式目前支持的物理算法有：Broadcast Hash Join、Shuffled Hash Join、 Shuffled Hash Aggregation、Union All、 TopN 和 Limit。算法的选择由优化器自动判断。通过 `EXPLAIN` 语句可以查看具体的查询执行计划。如果 `EXPLAIN` 语句的结果中出现 ExchangeSender 和 ExchangeReceiver 算子，表明 MPP 已生效。

以 TPC-H 测试集中的表结构为例：

```sql
mysql> explain select count(*) from customer c join nation n on c.c_nationkey=n.n_nationkey;
+------------------------------------------+------------+-------------------+---------------+----------------------------------------------------------------------------+
| id                                       | estRows    | task              | access object | operator info                                                              |
+------------------------------------------+------------+-------------------+---------------+----------------------------------------------------------------------------+
| HashAgg_23                               | 1.00       | root              |               | funcs:count(Column#16)->Column#15                                          |
| └─TableReader_25                         | 1.00       | root              |               | data:ExchangeSender_24                                                     |
|   └─ExchangeSender_24                    | 1.00       | batchCop[tiflash] |               | ExchangeType: PassThrough                                                  |
|     └─HashAgg_12                         | 1.00       | batchCop[tiflash] |               | funcs:count(1)->Column#16                                                  |
|       └─HashJoin_17                      | 3000000.00 | batchCop[tiflash] |               | inner join, equal:[eq(tpch.nation.n_nationkey, tpch.customer.c_nationkey)] |
|         ├─ExchangeReceiver_21(Build)     | 25.00      | batchCop[tiflash] |               |                                                                            |
|         │ └─ExchangeSender_20            | 25.00      | batchCop[tiflash] |               | ExchangeType: Broadcast                                                    |
|         │   └─TableFullScan_18           | 25.00      | batchCop[tiflash] | table:n       | keep order:false                                                           |
|         └─TableFullScan_22(Probe)        | 3000000.00 | batchCop[tiflash] | table:c       | keep order:false                                                           |
+------------------------------------------+------------+-------------------+---------------+----------------------------------------------------------------------------+
9 rows in set (0.00 sec)
```

在执行计划中，出现了 `ExchangeReceiver` 和 `ExchangeSender` 算子。该执行计划表示 `nation` 表读取完毕后，经过 `ExchangeSender` 算子广播到各个节点中，与 `customer` 表先后进行 `HashJoin` 和 `HashAgg` 操作，再将结果返回至 TiDB 中。

TiFlash 提供了两个全局/会话变量决定是否选择 Broadcast Hash Join，分别为：

- [`tidb_broadcast_join_threshold_size`](/system-variables.md#tidb_broadcast_join_threshold_count-从-v50-版本开始引入)，单位为 bytes。如果表大小（字节数）小于该值，则选择 Broadcast Hash Join 算法。否则选择 Shuffled Hash Join 算法。
- [`tidb_broadcast_join_threshold_count`](/system-variables.md#tidb_broadcast_join_threshold_count-从-v50-版本开始引入)，单位为行数。如果 join 的对象为子查询，优化器无法估计子查询结果集大小，在这种情况下通过结果集行数判断。如果子查询的行数估计值小于该变量，则选择 Broadcast Hash Join 算法。否则选择 Shuffled Hash Join 算法。

## MPP 模式访问分区表

如果希望使用 MPP 模式访问分区表，需要先开启[动态裁剪模式](/partitioned-table.md#动态裁剪模式)。

示例如下：

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
