---
title: 分区裁剪
summary: 了解 TiDB 分区裁剪的使用场景。
---

# 分区裁剪

分区裁剪是一种应用于分区表的性能优化。它分析查询语句中的过滤条件，并消除（_裁剪_）不包含任何所需数据的分区。通过消除不需要的分区，TiDB 能够减少需要访问的数据量，从而可能显著提高查询执行时间。

以下是一个示例：

{{< copyable "sql" >}}

```sql
CREATE TABLE t1 (
 id INT NOT NULL PRIMARY KEY,
 pad VARCHAR(100)
)
PARTITION BY RANGE COLUMNS(id) (
 PARTITION p0 VALUES LESS THAN (100),
 PARTITION p1 VALUES LESS THAN (200),
 PARTITION p2 VALUES LESS THAN (MAXVALUE)
);

INSERT INTO t1 VALUES (1, 'test1'),(101, 'test2'), (201, 'test3');
EXPLAIN SELECT * FROM t1 WHERE id BETWEEN 80 AND 120;
```

```sql
+----------------------------+---------+-----------+------------------------+------------------------------------------------+
| id                         | estRows | task      | access object          | operator info                                  |
+----------------------------+---------+-----------+------------------------+------------------------------------------------+
| PartitionUnion_8           | 80.00   | root      |                        |                                                |
| ├─TableReader_10           | 40.00   | root      |                        | data:TableRangeScan_9                          |
| │ └─TableRangeScan_9       | 40.00   | cop[tikv] | table:t1, partition:p0 | range:[80,120], keep order:false, stats:pseudo |
| └─TableReader_12           | 40.00   | root      |                        | data:TableRangeScan_11                         |
|   └─TableRangeScan_11      | 40.00   | cop[tikv] | table:t1, partition:p1 | range:[80,120], keep order:false, stats:pseudo |
+----------------------------+---------+-----------+------------------------+------------------------------------------------+
5 rows in set (0.00 sec)
```

## 分区裁剪的使用场景

分区裁剪的使用场景因分区表的类型不同而不同：范围分区表和哈希分区表。

### 在哈希分区表中使用分区裁剪

本节描述分区裁剪在哈希分区表中的适用和不适用场景。

#### 哈希分区表中的适用场景

分区裁剪仅适用于哈希分区表中的等值比较查询条件。

{{< copyable "sql" >}}

```sql
create table t (x int) partition by hash(x) partitions 4;
explain select * from t where x = 1;
```

```sql
+-------------------------+----------+-----------+-----------------------+--------------------------------+
| id                      | estRows  | task      | access object         | operator info                  |
+-------------------------+----------+-----------+-----------------------+--------------------------------+
| TableReader_8           | 10.00    | root      |                       | data:Selection_7               |
| └─Selection_7           | 10.00    | cop[tikv] |                       | eq(test.t.x, 1)                |
|   └─TableFullScan_6     | 10000.00 | cop[tikv] | table:t, partition:p1 | keep order:false, stats:pseudo |
+-------------------------+----------+-----------+-----------------------+--------------------------------+
```

在上面的 SQL 语句中，可以从条件 `x = 1` 知道所有结果都落在一个分区中。值 `1` 经过哈希分区后可以确定在 `p1` 分区中。因此，只需要扫描 `p1` 分区，不需要访问不会有匹配结果的 `p2`、`p3` 和 `p4` 分区。从执行计划中可以看到，只出现了一个 `TableFullScan` 算子，并且在 `access object` 中指定了 `p1` 分区，因此可以确认 `partition pruning` 生效。

#### 哈希分区表中的不适用场景

本节描述分区裁剪在哈希分区表中的两个不适用场景。

##### 场景一

如果无法确定查询结果只落在一个分区中的条件（如 `in`、`between`、`>`、`<`、`>=`、`<=`），则无法使用分区裁剪优化。例如：

{{< copyable "sql" >}}

```sql
create table t (x int) partition by hash(x) partitions 4;
explain select * from t where x > 2;
```

```sql
+------------------------------+----------+-----------+-----------------------+--------------------------------+
| id                           | estRows  | task      | access object         | operator info                  |
+------------------------------+----------+-----------+-----------------------+--------------------------------+
| Union_10                     | 13333.33 | root      |                       |                                |
| ├─TableReader_13             | 3333.33  | root      |                       | data:Selection_12              |
| │ └─Selection_12             | 3333.33  | cop[tikv] |                       | gt(test.t.x, 2)                |
| │   └─TableFullScan_11       | 10000.00 | cop[tikv] | table:t, partition:p0 | keep order:false, stats:pseudo |
| ├─TableReader_16             | 3333.33  | root      |                       | data:Selection_15              |
| │ └─Selection_15             | 3333.33  | cop[tikv] |                       | gt(test.t.x, 2)                |
| │   └─TableFullScan_14       | 10000.00 | cop[tikv] | table:t, partition:p1 | keep order:false, stats:pseudo |
| ├─TableReader_19             | 3333.33  | root      |                       | data:Selection_18              |
| │ └─Selection_18             | 3333.33  | cop[tikv] |                       | gt(test.t.x, 2)                |
| │   └─TableFullScan_17       | 10000.00 | cop[tikv] | table:t, partition:p2 | keep order:false, stats:pseudo |
| └─TableReader_22             | 3333.33  | root      |                       | data:Selection_21              |
|   └─Selection_21             | 3333.33  | cop[tikv] |                       | gt(test.t.x, 2)                |
|     └─TableFullScan_20       | 10000.00 | cop[tikv] | table:t, partition:p3 | keep order:false, stats:pseudo |
+------------------------------+----------+-----------+-----------------------+--------------------------------+
```

在这种情况下，分区裁剪不适用，因为无法通过 `x > 2` 条件确定对应的哈希分区。

##### 场景二

因为分区裁剪的规则优化是在查询计划生成阶段进行的，所以分区裁剪不适用于只能在执行阶段获得过滤条件的场景。例如：

{{< copyable "sql" >}}

```sql
create table t (x int) partition by hash(x) partitions 4;
explain select * from t2 where x = (select * from t1 where t2.x = t1.x and t2.x < 2);
```

```sql
+--------------------------------------+----------+-----------+------------------------+----------------------------------------------+
| id                                   | estRows  | task      | access object          | operator info                                |
+--------------------------------------+----------+-----------+------------------------+----------------------------------------------+
| Projection_13                        | 9990.00  | root      |                        | test.t2.x                                    |
| └─Apply_15                           | 9990.00  | root      |                        | inner join, equal:[eq(test.t2.x, test.t1.x)] |
|   ├─TableReader_18(Build)            | 9990.00  | root      |                        | data:Selection_17                            |
|   │ └─Selection_17                   | 9990.00  | cop[tikv] |                        | not(isnull(test.t2.x))                       |
|   │   └─TableFullScan_16             | 10000.00 | cop[tikv] | table:t2               | keep order:false, stats:pseudo               |
|   └─Selection_19(Probe)              | 0.80     | root      |                        | not(isnull(test.t1.x))                       |
|     └─MaxOneRow_20                   | 1.00     | root      |                        |                                              |
|       └─Union_21                     | 2.00     | root      |                        |                                              |
|         ├─TableReader_24             | 2.00     | root      |                        | data:Selection_23                            |
|         │ └─Selection_23             | 2.00     | cop[tikv] |                        | eq(test.t2.x, test.t1.x), lt(test.t2.x, 2)   |
|         │   └─TableFullScan_22       | 2500.00  | cop[tikv] | table:t1, partition:p0 | keep order:false, stats:pseudo               |
|         └─TableReader_27             | 2.00     | root      |                        | data:Selection_26                            |
|           └─Selection_26             | 2.00     | cop[tikv] |                        | eq(test.t2.x, test.t1.x), lt(test.t2.x, 2)   |
|             └─TableFullScan_25       | 2500.00  | cop[tikv] | table:t1, partition:p1 | keep order:false, stats:pseudo               |
+--------------------------------------+----------+-----------+------------------------+----------------------------------------------+
```

这个查询每次从 `t2` 读取一行时，都会在分区表 `t1` 上进行查询。理论上，此时满足 `t1.x = val` 的过滤条件，但实际上分区裁剪只在查询计划生成阶段生效，而不是在执行阶段。

### 在范围分区表中使用分区裁剪

本节描述分区裁剪在范围分区表中的适用和不适用场景。

#### 范围分区表中的适用场景

本节描述分区裁剪在范围分区表中的三个适用场景。

##### 场景一

分区裁剪适用于范围分区表中的等值比较查询条件。例如：

{{< copyable "sql" >}}

```sql
create table t (x int) partition by range (x) (
    partition p0 values less than (5),
    partition p1 values less than (10),
    partition p2 values less than (15)
    );
explain select * from t where x = 3;
```

```sql
+-------------------------+----------+-----------+-----------------------+--------------------------------+
| id                      | estRows  | task      | access object         | operator info                  |
+-------------------------+----------+-----------+-----------------------+--------------------------------+
| TableReader_8           | 10.00    | root      |                       | data:Selection_7               |
| └─Selection_7           | 10.00    | cop[tikv] |                       | eq(test.t.x, 3)                |
|   └─TableFullScan_6     | 10000.00 | cop[tikv] | table:t, partition:p0 | keep order:false, stats:pseudo |
+-------------------------+----------+-----------+-----------------------+--------------------------------+
```

分区裁剪也适用于使用 `in` 查询条件的等值比较。例如：

{{< copyable "sql" >}}

```sql
create table t (x int) partition by range (x) (
    partition p0 values less than (5),
    partition p1 values less than (10),
    partition p2 values less than (15)
    );
explain select * from t where x in(1,13);
```

```sql
+-----------------------------+----------+-----------+-----------------------+--------------------------------+
| id                          | estRows  | task      | access object         | operator info                  |
+-----------------------------+----------+-----------+-----------------------+--------------------------------+
| Union_8                     | 40.00    | root      |                       |                                |
| ├─TableReader_11            | 20.00    | root      |                       | data:Selection_10              |
| │ └─Selection_10            | 20.00    | cop[tikv] |                       | in(test.t.x, 1, 13)            |
| │   └─TableFullScan_9       | 10000.00 | cop[tikv] | table:t, partition:p0 | keep order:false, stats:pseudo |
| └─TableReader_14            | 20.00    | root      |                       | data:Selection_13              |
|   └─Selection_13            | 20.00    | cop[tikv] |                       | in(test.t.x, 1, 13)            |
|     └─TableFullScan_12      | 10000.00 | cop[tikv] | table:t, partition:p2 | keep order:false, stats:pseudo |
+-----------------------------+----------+-----------+-----------------------+--------------------------------+
```

在上面的 SQL 语句中，可以从 `x in(1,13)` 条件知道所有结果都落在几个分区中。经过分析，发现 `x = 1` 的所有记录都在 `p0` 分区中，`x = 13` 的所有记录都在 `p2` 分区中，所以只需要访问 `p0` 和 `p2` 分区。

##### 场景二

分区裁剪适用于区间比较的查询条件，如 `between`、`>`、`<`、`=`、`>=`、`<=`。例如：

{{< copyable "sql" >}}

```sql
create table t (x int) partition by range (x) (
    partition p0 values less than (5),
    partition p1 values less than (10),
    partition p2 values less than (15)
    );
explain select * from t where x between 7 and 14;
```

```sql
+-----------------------------+----------+-----------+-----------------------+-----------------------------------+
| id                          | estRows  | task      | access object         | operator info                     |
+-----------------------------+----------+-----------+-----------------------+-----------------------------------+
| Union_8                     | 500.00   | root      |                       |                                   |
| ├─TableReader_11            | 250.00   | root      |                       | data:Selection_10                 |
| │ └─Selection_10            | 250.00   | cop[tikv] |                       | ge(test.t.x, 7), le(test.t.x, 14) |
| │   └─TableFullScan_9       | 10000.00 | cop[tikv] | table:t, partition:p1 | keep order:false, stats:pseudo    |
| └─TableReader_14            | 250.00   | root      |                       | data:Selection_13                 |
|   └─Selection_13            | 250.00   | cop[tikv] |                       | ge(test.t.x, 7), le(test.t.x, 14) |
|     └─TableFullScan_12      | 10000.00 | cop[tikv] | table:t, partition:p2 | keep order:false, stats:pseudo    |
+-----------------------------+----------+-----------+-----------------------+-----------------------------------+
```

##### 场景三

分区裁剪适用于分区表达式为简单形式 `fn(col)` 的场景，其中查询条件是 `>`、`<`、`=`、`>=` 和 `<=` 之一，且 `fn` 函数是单调的。

如果 `fn` 函数是单调的，对于任何 `x` 和 `y`，如果 `x > y`，则 `fn(x) > fn(y)`。这种 `fn` 函数可以称为严格单调的。对于任何 `x` 和 `y`，如果 `x > y`，则 `fn(x) >= fn(y)`。在这种情况下，`fn` 也可以称为"单调的"。理论上，分区裁剪支持所有单调函数，无论是严格单调还是非严格单调。目前，TiDB 仅支持以下单调函数：

* [`UNIX_TIMESTAMP()`](/functions-and-operators/date-and-time-functions.md)
* [`TO_DAYS()`](/functions-and-operators/date-and-time-functions.md)

例如，当分区表达式为 `fn(col)` 形式，其中 `fn` 是单调函数 `to_days` 时，分区裁剪生效：

{{< copyable "sql" >}}

```sql
create table t (id datetime) partition by range (to_days(id)) (
    partition p0 values less than (to_days('2020-04-01')),
    partition p1 values less than (to_days('2020-05-01')));
explain select * from t where id > '2020-04-18';
```

```sql
+-------------------------+----------+-----------+-----------------------+-------------------------------------------+
| id                      | estRows  | task      | access object         | operator info                             |
+-------------------------+----------+-----------+-----------------------+-------------------------------------------+
| TableReader_8           | 3333.33  | root      |                       | data:Selection_7                          |
| └─Selection_7           | 3333.33  | cop[tikv] |                       | gt(test.t.id, 2020-04-18 00:00:00.000000) |
|   └─TableFullScan_6     | 10000.00 | cop[tikv] | table:t, partition:p1 | keep order:false, stats:pseudo            |
+-------------------------+----------+-----------+-----------------------+-------------------------------------------+
```

#### 范围分区表中的不适用场景

因为分区裁剪的规则优化是在查询计划生成阶段进行的，所以分区裁剪不适用于只能在执行阶段获得过滤条件的场景。例如：

{{< copyable "sql" >}}

```sql
create table t1 (x int) partition by range (x) (
    partition p0 values less than (5),
    partition p1 values less than (10));
create table t2 (x int);
explain select * from t2 where x < (select * from t1 where t2.x < t1.x and t2.x < 2);
```

```sql
+--------------------------------------+----------+-----------+------------------------+-----------------------------------------------------------+
| id                                   | estRows  | task      | access object          | operator info                                             |
+--------------------------------------+----------+-----------+------------------------+-----------------------------------------------------------+
| Projection_13                        | 9990.00  | root      |                        | test.t2.x                                                 |
| └─Apply_15                           | 9990.00  | root      |                        | CARTESIAN inner join, other cond:lt(test.t2.x, test.t1.x) |
|   ├─TableReader_18(Build)            | 9990.00  | root      |                        | data:Selection_17                                         |
|   │ └─Selection_17                   | 9990.00  | cop[tikv] |                        | not(isnull(test.t2.x))                                    |
|   │   └─TableFullScan_16             | 10000.00 | cop[tikv] | table:t2               | keep order:false, stats:pseudo                            |
|   └─Selection_19(Probe)              | 0.80     | root      |                        | not(isnull(test.t1.x))                                    |
|     └─MaxOneRow_20                   | 1.00     | root      |                        |                                                           |
|       └─Union_21                     | 2.00     | root      |                        |                                                           |
|         ├─TableReader_24             | 2.00     | root      |                        | data:Selection_23                                         |
|         │ └─Selection_23             | 2.00     | cop[tikv] |                        | lt(test.t2.x, 2), lt(test.t2.x, test.t1.x)                |
|         │   └─TableFullScan_22       | 2.50     | cop[tikv] | table:t1, partition:p0 | keep order:false, stats:pseudo                            |
|         └─TableReader_27             | 2.00     | root      |                        | data:Selection_26                                         |
|           └─Selection_26             | 2.00     | cop[tikv] |                        | lt(test.t2.x, 2), lt(test.t2.x, test.t1.x)                |
|             └─TableFullScan_25       | 2.50     | cop[tikv] | table:t1, partition:p1 | keep order:false, stats:pseudo                            |
+--------------------------------------+----------+-----------+------------------------+-----------------------------------------------------------+
14 rows in set (0.00 sec)
```

这个查询每次从 `t2` 读取一行时，都会在分区表 `t1` 上进行查询。理论上，此时满足 `t1.x > val` 的过滤条件，但实际上分区裁剪只在查询计划生成阶段生效，而不是在执行阶段。
