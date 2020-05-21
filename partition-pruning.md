---
title: 分区裁剪
category: performance
---

# 分区裁剪

分区裁剪通过分析查询语句中的过滤条件，只选择可能满足条件的分区，不扫描匹配不上的分区，进而显著地减少计算的数据量。

## 分区表

分区裁剪是只有当目标表为分区表时，才可以进行的一种优化方式。[分区表](/partitioned-table.md) 是 TiDB 中常见的性能优化的手段，Range 分区可以用于解决业务中大量删除带来的性能问题，Hash 分区则可以用于大量写入场景下的数据打散。

## 分区裁剪的使用场景

### 场景一

分区裁剪需要使用分区表上面的查询条件，如果查询条件不能下推到分区表，则相应的查询语句无法使用分区裁剪。

```sql
create table t1 (x int) partition by range (x) (
    partition p0 values less than (5),
    partition p1 values less than (10));
create table t2 (x int);

explain select * from t1 left join t2 on t1.x = t2.x where t2.x > 5;
+------------------------------+----------+-----------+------------------------+----------------------------------------------+
| id                           | estRows  | task      | access object          | operator info                                |
+------------------------------+----------+-----------+------------------------+----------------------------------------------+
| HashJoin_8                   | 4166.67  | root      |                        | inner join, equal:[eq(test.t1.x, test.t2.x)] |
| ├─TableReader_15(Build)      | 3333.33  | root      |                        | data:Selection_14                            |
| │ └─Selection_14             | 3333.33  | cop[tikv] |                        | gt(test.t2.x, 5), not(isnull(test.t2.x))     |
| │   └─TableFullScan_13       | 10000.00 | cop[tikv] | table:t2               | keep order:false, stats:pseudo               |
| └─TableReader_12(Probe)      | 3333.33  | root      |                        | data:Selection_11                            |
|   └─Selection_11             | 3333.33  | cop[tikv] |                        | gt(test.t1.x, 5), not(isnull(test.t1.x))     |
|     └─TableFullScan_10       | 10000.00 | cop[tikv] | table:t1, partition:p1 | keep order:false, stats:pseudo               |
+------------------------------+----------+-----------+------------------------+----------------------------------------------+
7 rows in set (0.01 sec)
```

在这个查询中，外连接可以简化成内连接，然后由 `t1.x = t2.x` 和 `t2.x > 5` 可以推出条件 `t1.x > 5`，于是可以分区裁剪并且只使用 `p1` 分区。

```sql
explain select * from t1 left join t2 on t1.x = t2.x and t2.x > 5;
+------------------------------+----------+-----------+------------------------+---------------------------------------------------+
| id                           | estRows  | task      | access object          | operator info                                     |
+------------------------------+----------+-----------+------------------------+---------------------------------------------------+
| HashJoin_9                   | 20000.00 | root      |                        | left outer join, equal:[eq(test.t1.x, test.t2.x)] |
| ├─TableReader_18(Build)      | 3333.33  | root      |                        | data:Selection_17                                 |
| │ └─Selection_17             | 3333.33  | cop[tikv] |                        | gt(test.t2.x, 5), not(isnull(test.t2.x))          |
| │   └─TableFullScan_16       | 10000.00 | cop[tikv] | table:t2               | keep order:false, stats:pseudo                    |
| └─Union_11(Probe)            | 20000.00 | root      |                        |                                                   |
|   ├─TableReader_13           | 10000.00 | root      |                        | data:TableFullScan_12                             |
|   │ └─TableFullScan_12       | 10000.00 | cop[tikv] | table:t1, partition:p0 | keep order:false, stats:pseudo                    |
|   └─TableReader_15           | 10000.00 | root      |                        | data:TableFullScan_14                             |
|     └─TableFullScan_14       | 10000.00 | cop[tikv] | table:t1, partition:p1 | keep order:false, stats:pseudo                    |
+------------------------------+----------+-----------+------------------------+---------------------------------------------------+
9 rows in set (0.00 sec)
```

这个查询中的 `t2.x > 5` 条件不能下推到 `t1` 分区表上面，因此 `t1` 无法分区裁剪。

### 场景二

由于分区裁剪的规则优化是在查询计划的生成阶段，对于执行阶段才能获取到过滤条件的场景，无法利用分区裁剪的优化。

```sql
create table t1 (x int) partition by range (x) (
    partition p0 values less than (5),
    partition p1 values less than (10));
create table t2 (x int);
explain select * from t2 where x < (select * from t1 where t2.x < t1.x and t2.x < 2);
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

这个查询每从 `t2` 读取一行，都会去分区表 `t1` 上进行查询，理论上这时会满足 `t1.x > val` 的过滤条件，但实际上由于分区裁剪只作用于查询计划生成阶段，而不是执行阶段，因而不会做裁剪。

### 场景三

对于 `hash` 分区类型，只有等值比较的查询条件能够支持分区裁剪。

```sql
create table t (x int) partition by hash(x) partitions 4;
explain select * from t where x = 1;
+-------------------------+----------+-----------+-----------------------+--------------------------------+
| id                      | estRows  | task      | access object         | operator info                  |
+-------------------------+----------+-----------+-----------------------+--------------------------------+
| TableReader_8           | 10.00    | root      |                       | data:Selection_7               |
| └─Selection_7           | 10.00    | cop[tikv] |                       | eq(test.t.x, 1)                |
|   └─TableFullScan_6     | 10000.00 | cop[tikv] | table:t, partition:p1 | keep order:false, stats:pseudo |
+-------------------------+----------+-----------+-----------------------+--------------------------------+
3 rows in set (0.01 sec)
explain select * from t where x > 2;
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
13 rows in set (0.00 sec)
```

### 场景四

对于 `range` 分区类型，分区表达式必须是 `col` 或者 `fn(col)` 的简单形式，查询条件是 `> < = >= <=` 时才能支持分区裁剪。如果分区表达式是 `fn(col)` 形式，还要求 `fn` 必须是单调函数，才有可能分区裁剪。

理论上所有满足单调条件（严格或者非严格）的函数都是可以支持分区裁剪。实际上，目前 TiDB 已经支持的单调函数只有：

```sql
unix_timestamp
to_days
```

例如，分区表达式是 `fn(col)` 形式，`fn` 为我们支持的单调函数 `to_days`:

```sql
create table t (id datetime) partition by range (to_days(id)) (
    partition p0 values less than (to_days('2020-04-01')),
    partition p1 values less than (to_days('2020-05-01')));
explain select * from t where id > '2020-04-18';
+-------------------------+----------+-----------+-----------------------+-------------------------------------------+
| id                      | estRows  | task      | access object         | operator info                             |
+-------------------------+----------+-----------+-----------------------+-------------------------------------------+
| TableReader_8           | 3333.33  | root      |                       | data:Selection_7                          |
| └─Selection_7           | 3333.33  | cop[tikv] |                       | gt(test.t.id, 2020-04-18 00:00:00.000000) |
|   └─TableFullScan_6     | 10000.00 | cop[tikv] | table:t, partition:p1 | keep order:false, stats:pseudo            |
+-------------------------+----------+-----------+-----------------------+-------------------------------------------+
3 rows in set (0.00 sec)
```