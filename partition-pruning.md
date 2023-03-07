---
title: Partition Pruning
summary: Learn about the usage scenarios of TiDB partition pruning.
---

# Partition Pruning

Partition pruning is a performance optimization that applies to partitioned tables. It analyzes the filter conditions in query statements, and eliminates (_prunes_) partitions from consideration when they do not contain any data that will be required. By eliminating the non-required partitions, TiDB is able to reduce the amount of data that needs to be accessed and potentially significantly improving query execution times.

The following is an example:

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

## Usage scenarios of partition pruning

The usage scenarios of partition pruning are different for the two types of partitioned tables: Range partitioned tables and Hash partitioned tables.

### Use partition pruning in Hash partitioned tables

This section describes the applicable and inapplicable usage scenarios of partition pruning in Hash partitioned tables.

#### Applicable scenario in Hash partitioned tables

Partition pruning applies only to the query condition of equality comparison in Hash partitioned tables.

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

In the SQL statement above, it can be known from the condition `x = 1` that all results fall in one partition. The value `1` can be confirmed to be in the `p1` partition after passing through the Hash partition. Therefore, only the `p1` partition needs to be scanned, and there is no need to access the `p2`, `p3`, and `p4` partitions that will not have matching results. From the execution plan, only one `TableFullScan` operator appears and the `p1` partition is specified in `access object`, so it can be confirmed that `partition pruning` takes effect.

#### Inapplicable scenarios in Hash partitioned tables

This section describes two inapplicable usage scenarios of partition pruning in Hash partitioned tables.

##### Scenario one

If you cannot confirm the condition that the query result falls in only one partition (such as `in`, `between`, `>`, `<`, `>=`, `<=`), you cannot use the partition pruning optimization. For example:

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

In this case, partition pruning is inapplicable because the corresponding Hash partition cannot be confirmed by the `x > 2` condition.

##### Scenario two

Because the rule optimization of partition pruning is performed during the generation phase of the query plan, partition pruning is not suitable for scenarios where the filter conditions can be obtained only during the execution phase. For example:

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

Each time this query reads a row from `t2`, it will query on the `t1` partitioned table. Theoretically, the filter condition of `t1.x = val` is met at this time, but in fact, partition pruning takes effect only in the generation phase of the query plan, not the execution phase.

### Use partition pruning in Range partitioned tables

This section describes the applicable and inapplicable usage scenarios of partition pruning in Range partitioned tables.

#### Applicable scenarios in Range partitioned tables

This section describes three applicable usage scenarios of partition pruning in Range partitioned tables.

##### Scenario one

Partition pruning applies to the query condition of equality comparison in Range partitioned tables. For example:

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

Partition pruning also applies to the equality comparison that uses the `in` query condition. For example:

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

In the SQL statement above, it can be known from the `x in(1,13)` condition that all results fall in a few partitions. After analysis, it is found that all records of `x = 1` are in the `p0` partition, and all records of `x = 13` are in the `p2` partition, so only `p0` and `p2` partitions need to be accessed.

##### Scenario two

Partition pruning applies to the query condition of interval comparison, such as `between`, `>`, `<`, `=`, `>=`, `<=`. For example:

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

##### Scenario three

Partition pruning applies to the scenario where the partition expression is in the simple form of `fn(col)`, the query condition is one of `>`, `<`, `=`, `>=`, and `<=`, and the `fn` function is monotonous.

If the `fn` function is monotonous, for any `x` and `y`, if `x > y`, then `fn(x) > fn(y)`. Then this `fn` function can be called strictly monotonous. For any `x` and `y`, if `x > y`, then `fn(x) >= fn(y)`. In this case, `fn` could also be called "monotonous". Theoretically, all monotonous functions, strictly or not, are supported by partition pruning. Currently, TiDB only supports the following monotonous functions:

* [`UNIX_TIMESTAMP()`](/functions-and-operators/date-and-time-functions.md)
* [`TO_DAYS()`](/functions-and-operators/date-and-time-functions.md)

For example, partition pruning takes effect when the partition expression is in the form of `fn(col)`, where the `fn` is monotonous function `to_days`:

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

#### Inapplicable scenario in Range partitioned tables

Because the rule optimization of partition pruning is performed during the generation phase of the query plan, partition pruning is not suitable for scenarios where the filter conditions can be obtained only during the execution phase. For example:

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

Each time this query reads a row from `t2`, it will query on the `t1` partitioned table. Theoretically, the `t1.x> val` filter condition is met at this time, but in fact, partition pruning takes effect only in the generation phase of the query plan, not the execution phase.
