---
title: Explain Statements That Use Subqueries
summary: Learn about the execution plan information returned by the EXPLAIN statement in TiDB.
---

# Explain Statements That Use Subqueries

TiDB performs [several optimizations](/subquery-optimization.md) to improve the performance of subqueries. This document describes some of these optimizations for common subqueries and how to interpret the output of `EXPLAIN`.

The examples in this document are based on the following sample data:

```sql
CREATE TABLE t1 (id BIGINT NOT NULL PRIMARY KEY auto_increment, pad1 BLOB, pad2 BLOB, pad3 BLOB, int_col INT NOT NULL DEFAULT 0);
CREATE TABLE t2 (id BIGINT NOT NULL PRIMARY KEY auto_increment, t1_id BIGINT NOT NULL, pad1 BLOB, pad2 BLOB, pad3 BLOB, INDEX(t1_id));
CREATE TABLE t3 (
 id INT NOT NULL PRIMARY KEY auto_increment,
 t1_id INT NOT NULL,
 UNIQUE (t1_id)
);

INSERT INTO t1 SELECT NULL, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024), 0 FROM dual;
INSERT INTO t1 SELECT NULL, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024), 0 FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024), 0 FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024), 0 FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024), 0 FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024), 0 FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024), 0 FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024), 0 FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024), 0 FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024), 0 FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024), 0 FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t2 SELECT NULL, a.id, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t2 SELECT NULL, a.id, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t2 SELECT NULL, a.id, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t2 SELECT NULL, a.id, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t2 SELECT NULL, a.id, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t2 SELECT NULL, a.id, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t2 SELECT NULL, a.id, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t2 SELECT NULL, a.id, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t2 SELECT NULL, a.id, RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
UPDATE t1 SET int_col = 1 WHERE pad1 = (SELECT pad1 FROM t1 ORDER BY RAND() LIMIT 1);
INSERT INTO t3 SELECT NULL, id FROM t1 WHERE id < 1000;

SELECT SLEEP(1);
ANALYZE TABLE t1, t2, t3;
```

## Inner join (non-unique subquery)

In the following example, the `IN` subquery searches for a list of IDs from the table `t2`. For semantic correctness, TiDB needs to guarantee that the column `t1_id` is unique. Using `EXPLAIN`, you can see the execution plan used to remove duplicates and perform an `INNER JOIN` operation:

```sql
EXPLAIN SELECT * FROM t1 WHERE id IN (SELECT t1_id FROM t2);
```

```sql
+----------------------------------+----------+-----------+------------------------------+---------------------------------------------------------------------------------------------------------------------------+
| id                               | estRows  | task      | access object                | operator info                                                                                                             |
+----------------------------------+----------+-----------+------------------------------+---------------------------------------------------------------------------------------------------------------------------+
| IndexJoin_14                     | 5.00     | root      |                              | inner join, inner:IndexLookUp_13, outer key:test.t2.t1_id, inner key:test.t1.id, equal cond:eq(test.t2.t1_id, test.t1.id) |
| ├─StreamAgg_49(Build)            | 5.00     | root      |                              | group by:test.t2.t1_id, funcs:firstrow(test.t2.t1_id)->test.t2.t1_id                                                      |
| │ └─IndexReader_50               | 5.00     | root      |                              | index:StreamAgg_39                                                                                                        |
| │   └─StreamAgg_39               | 5.00     | cop[tikv] |                              | group by:test.t2.t1_id,                                                                                                   |
| │     └─IndexFullScan_31         | 50000.00 | cop[tikv] | table:t2, index:t1_id(t1_id) | keep order:true                                                                                                           |
| └─IndexLookUp_13(Probe)          | 1.00     | root      |                              |                                                                                                                           |
|   ├─IndexRangeScan_11(Build)     | 1.00     | cop[tikv] | table:t1, index:PRIMARY(id)  | range: decided by [eq(test.t1.id, test.t2.t1_id)], keep order:false                                                       |
|   └─TableRowIDScan_12(Probe)     | 1.00     | cop[tikv] | table:t1                     | keep order:false                                                                                                          |
+----------------------------------+----------+-----------+------------------------------+---------------------------------------------------------------------------------------------------------------------------+
8 rows in set (0.00 sec)
```

From the query results above, you can see that TiDB uses the index join operation `| IndexJoin_14` to join and transform the subquery. In the execution plan, the execution process is as follows:

1. The index scanning operator `└─IndexFullScan_31` at the TiKV side reads the values of the `t2.t1_id` column.
2. Some tasks of the `└─StreamAgg_39` operator deduplicate the values of `t1_id` in TiKV.
3. Some tasks of the `├─StreamAgg_49(Build)` operator deduplicate the values of `t1_id` in TiDB. The deduplication is performed by the aggregate function `firstrow(test.t2.t1_id)`.
4. The operation results are joined with the primary key of the `t1` table. The join condition is `eq(test.t1.id, test.t2.t1_id)`.

## Inner join (unique subquery)

In the previous example, aggregation is required to ensure that the values of `t1_id` are unique before joining against the table `t1`. But in the following example, `t3.t1_id` is already guaranteed unique because of a `UNIQUE` constraint:

```sql
EXPLAIN SELECT * FROM t1 WHERE id IN (SELECT t1_id FROM t3);
```

```sql
+----------------------------------+---------+-----------+-----------------------------+---------------------------------------------------------------------------------------------------------------------------+
| id                               | estRows | task      | access object               | operator info                                                                                                             |
+----------------------------------+---------+-----------+-----------------------------+---------------------------------------------------------------------------------------------------------------------------+
| IndexJoin_17                     | 1978.13 | root      |                             | inner join, inner:IndexLookUp_16, outer key:test.t3.t1_id, inner key:test.t1.id, equal cond:eq(test.t3.t1_id, test.t1.id) |
| ├─TableReader_44(Build)          | 1978.00 | root      |                             | data:TableFullScan_43                                                                                                     |
| │ └─TableFullScan_43             | 1978.00 | cop[tikv] | table:t3                    | keep order:false                                                                                                          |
| └─IndexLookUp_16(Probe)          | 1.00    | root      |                             |                                                                                                                           |
|   ├─IndexRangeScan_14(Build)     | 1.00    | cop[tikv] | table:t1, index:PRIMARY(id) | range: decided by [eq(test.t1.id, test.t3.t1_id)], keep order:false                                                       |
|   └─TableRowIDScan_15(Probe)     | 1.00    | cop[tikv] | table:t1                    | keep order:false                                                                                                          |
+----------------------------------+---------+-----------+-----------------------------+---------------------------------------------------------------------------------------------------------------------------+
6 rows in set (0.01 sec)
```

Semantically because `t3.t1_id` is guaranteed unique, it can be executed directly as an `INNER JOIN`.

## Semi join (correlated subquery)

In the previous two examples, TiDB is able to perform an `INNER JOIN` operation after the data inside the subquery is made unique (via `HashAgg`) or guaranteed unique. Both joins are performed using an Index Join.

In this example, TiDB chooses a different execution plan:

```sql
EXPLAIN SELECT * FROM t1 WHERE id IN (SELECT t1_id FROM t2 WHERE t1_id != t1.int_col);
```

```sql
+-----------------------------+-----------+-----------+------------------------------+--------------------------------------------------------------------------------------------------------+
| id                          | estRows   | task      | access object                | operator info                                                                                          |
+-----------------------------+-----------+-----------+------------------------------+--------------------------------------------------------------------------------------------------------+
| MergeJoin_9                 | 45446.40  | root      |                              | semi join, left key:test.t1.id, right key:test.t2.t1_id, other cond:ne(test.t2.t1_id, test.t1.int_col) |
| ├─IndexReader_24(Build)     | 180000.00 | root      |                              | index:IndexFullScan_23                                                                                 |
| │ └─IndexFullScan_23        | 180000.00 | cop[tikv] | table:t2, index:t1_id(t1_id) | keep order:true                                                                                        |
| └─TableReader_22(Probe)     | 56808.00  | root      |                              | data:Selection_21                                                                                      |
|   └─Selection_21            | 56808.00  | cop[tikv] |                              | ne(test.t1.id, test.t1.int_col)                                                                        |
|     └─TableFullScan_20      | 71010.00  | cop[tikv] | table:t1                     | keep order:true                                                                                        |
+-----------------------------+-----------+-----------+------------------------------+--------------------------------------------------------------------------------------------------------+
6 rows in set (0.00 sec)
```

From the result above, you can see that TiDB uses a `Semi Join` algorithm. Semi-join differs from inner join: semi-join only permits the first value on the right key (`t2.t1_id`), which means that the duplicates are eliminated as a part of the join operator task. The join algorithm is also Merge Join, which is like an efficient zipper-merge as the operator reads data from both the left and the right side in sorted order.

The original statement is considered a _correlated subquery_, because the subquery refers to a column (`t1.int_col`) that exists outside of the subquery. However, the output of `EXPLAIN` shows the execution plan after the [subquery decorrelation optimization](/correlated-subquery-optimization.md) has been applied. The condition `t1_id != t1.int_col` is rewritten to `t1.id != t1.int_col`. TiDB can perform this in `└─Selection_21` as it is reading data from the table `t1`, so this decorrelation and rewriting make the execution a lot more efficient.

## Anti semi join (`NOT IN` subquery)

In the following example, the query semantically returns all rows from the table `t3` _unless_ `t3.t1_id` is in the subquery:

```sql
EXPLAIN SELECT * FROM t3 WHERE t1_id NOT IN (SELECT id FROM t1 WHERE int_col < 100);
```

```sql
+-----------------------------+---------+-----------+---------------+-------------------------------------------------------------------------------------+
| id                          | estRows | task      | access object | operator info                                                                       |
+-----------------------------+---------+-----------+---------------+-------------------------------------------------------------------------------------+
| IndexMergeJoin_20           | 1598.40 | root      |               | anti semi join, inner:TableReader_15, outer key:test.t3.t1_id, inner key:test.t1.id |
| ├─TableReader_28(Build)     | 1998.00 | root      |               | data:TableFullScan_27                                                               |
| │ └─TableFullScan_27        | 1998.00 | cop[tikv] | table:t3      | keep order:false                                                                    |
| └─TableReader_15(Probe)     | 1.00    | root      |               | data:Selection_14                                                                   |
|   └─Selection_14            | 1.00    | cop[tikv] |               | lt(test.t1.int_col, 100)                                                            |
|     └─TableRangeScan_13     | 1.00    | cop[tikv] | table:t1      | range: decided by [test.t3.t1_id], keep order:true                                  |
+-----------------------------+---------+-----------+---------------+-------------------------------------------------------------------------------------+
6 rows in set (0.00 sec)
```

This query starts by reading the table `t3` and then probes the table `t1` based on the `PRIMARY KEY`. The join type is an _anti semi join_; anti because this example is for the non-existence of the value (`NOT IN`) and semi-join because only the first row needs to match before the join is rejected.
