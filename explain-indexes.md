---
title: 解释使用索引的语句
summary: 了解 TiDB 中 EXPLAIN 语句返回的执行计划信息。
---

# 解释使用索引的语句

TiDB 支持几种使用索引来加速查询执行的算子：

+ [`IndexLookup`](#indexlookup)
+ [`IndexReader`](#indexreader)
+ [`Point_Get` 和 `Batch_Point_Get`](#point_get-和-batch_point_get)
+ [`IndexFullScan`](#indexfullscan)

本文档中的示例基于以下示例数据：

{{< copyable "sql" >}}

```sql
CREATE TABLE t1 (
 id INT NOT NULL PRIMARY KEY auto_increment,
 intkey INT NOT NULL,
 pad1 VARBINARY(1024),
 INDEX (intkey)
);

INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1024), RANDOM_BYTES(1024) FROM dual;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
```

## IndexLookup

TiDB 在从二级索引检索数据时使用 `IndexLookup` 算子。在这种情况下，以下查询都将在 `intkey` 索引上使用 `IndexLookup` 算子：

{{< copyable "sql" >}}

```sql
EXPLAIN SELECT * FROM t1 WHERE intkey = 123;
EXPLAIN SELECT * FROM t1 WHERE intkey < 10;
EXPLAIN SELECT * FROM t1 WHERE intkey BETWEEN 300 AND 310;
EXPLAIN SELECT * FROM t1 WHERE intkey IN (123,29,98);
EXPLAIN SELECT * FROM t1 WHERE intkey >= 99 AND intkey <= 103;
```

```sql
+-------------------------------+---------+-----------+--------------------------------+-----------------------------------+
| id                            | estRows | task      | access object                  | operator info                     |
+-------------------------------+---------+-----------+--------------------------------+-----------------------------------+
| IndexLookUp_10                | 1.00    | root      |                                |                                   |
| ├─IndexRangeScan_8(Build)     | 1.00    | cop[tikv] | table:t1, index:intkey(intkey) | range:[123,123], keep order:false |
| └─TableRowIDScan_9(Probe)     | 1.00    | cop[tikv] | table:t1                       | keep order:false                  |
+-------------------------------+---------+-----------+--------------------------------+-----------------------------------+
3 rows in set (0.00 sec)

+-------------------------------+---------+-----------+--------------------------------+-----------------------------------+
| id                            | estRows | task      | access object                  | operator info                     |
+-------------------------------+---------+-----------+--------------------------------+-----------------------------------+
| IndexLookUp_10                | 3.60    | root      |                                |                                   |
| ├─IndexRangeScan_8(Build)     | 3.60    | cop[tikv] | table:t1, index:intkey(intkey) | range:[-inf,10), keep order:false |
| └─TableRowIDScan_9(Probe)     | 3.60    | cop[tikv] | table:t1                       | keep order:false                  |
+-------------------------------+---------+-----------+--------------------------------+-----------------------------------+
3 rows in set (0.00 sec)

+-------------------------------+---------+-----------+--------------------------------+-----------------------------------+
| id                            | estRows | task      | access object                  | operator info                     |
+-------------------------------+---------+-----------+--------------------------------+-----------------------------------+
| IndexLookUp_10                | 5.67    | root      |                                |                                   |
| ├─IndexRangeScan_8(Build)     | 5.67    | cop[tikv] | table:t1, index:intkey(intkey) | range:[300,310], keep order:false |
| └─TableRowIDScan_9(Probe)     | 5.67    | cop[tikv] | table:t1                       | keep order:false                  |
+-------------------------------+---------+-----------+--------------------------------+-----------------------------------+
3 rows in set (0.00 sec)

+-------------------------------+---------+-----------+--------------------------------+-----------------------------------------------------+
| id                            | estRows | task      | access object                  | operator info                                       |
+-------------------------------+---------+-----------+--------------------------------+-----------------------------------------------------+
| IndexLookUp_10                | 4.00    | root      |                                |                                                     |
| ├─IndexRangeScan_8(Build)     | 4.00    | cop[tikv] | table:t1, index:intkey(intkey) | range:[29,29], [98,98], [123,123], keep order:false |
| └─TableRowIDScan_9(Probe)     | 4.00    | cop[tikv] | table:t1                       | keep order:false                                    |
+-------------------------------+---------+-----------+--------------------------------+-----------------------------------------------------+
3 rows in set (0.00 sec)

+-------------------------------+---------+-----------+--------------------------------+----------------------------------+
| id                            | estRows | task      | access object                  | operator info                    |
+-------------------------------+---------+-----------+--------------------------------+----------------------------------+
| IndexLookUp_10                | 6.00    | root      |                                |                                  |
| ├─IndexRangeScan_8(Build)     | 6.00    | cop[tikv] | table:t1, index:intkey(intkey) | range:[99,103], keep order:false |
| └─TableRowIDScan_9(Probe)     | 6.00    | cop[tikv] | table:t1                       | keep order:false                 |
+-------------------------------+---------+-----------+--------------------------------+----------------------------------+
3 rows in set (0.00 sec)
```

`IndexLookup` 算子有两个子节点：

* `├─IndexRangeScan_8(Build)` 算子在 `intkey` 索引上执行范围扫描，并检索内部 `RowID`（对于此表，即主键）的值。
* `└─TableRowIDScan_9(Probe)` 算子然后从表数据中检索完整的行。

因为 `IndexLookup` 任务需要两个步骤，在匹配大量行的场景中，SQL 优化器可能会根据[统计信息](/statistics.md)选择 `TableFullScan` 算子。在以下示例中，大量行匹配条件 `intkey > 100`，因此选择了 `TableFullScan`：

{{< copyable "sql" >}}

```sql
EXPLAIN SELECT * FROM t1 WHERE intkey > 100;
```

```sql
+-------------------------+---------+-----------+---------------+-------------------------+
| id                      | estRows | task      | access object | operator info           |
+-------------------------+---------+-----------+---------------+-------------------------+
| TableReader_7           | 898.50  | root      |               | data:Selection_6        |
| └─Selection_6           | 898.50  | cop[tikv] |               | gt(test.t1.intkey, 100) |
|   └─TableFullScan_5     | 1010.00 | cop[tikv] | table:t1      | keep order:false        |
+-------------------------+---------+-----------+---------------+-------------------------+
3 rows in set (0.00 sec)
```

`IndexLookup` 算子还可以用于有效地优化索引列上的 `LIMIT`：

{{< copyable "sql" >}}

```sql
EXPLAIN SELECT * FROM t1 ORDER BY intkey DESC LIMIT 10;
```

```sql
+--------------------------------+---------+-----------+--------------------------------+------------------------------------+
| id                             | estRows | task      | access object                  | operator info                      |
+--------------------------------+---------+-----------+--------------------------------+------------------------------------+
| IndexLookUp_21                 | 10.00   | root      |                                | limit embedded(offset:0, count:10) |
| ├─Limit_20(Build)              | 10.00   | cop[tikv] |                                | offset:0, count:10                 |
| │ └─IndexFullScan_18           | 10.00   | cop[tikv] | table:t1, index:intkey(intkey) | keep order:true, desc              |
| └─TableRowIDScan_19(Probe)     | 10.00   | cop[tikv] | table:t1                       | keep order:false, stats:pseudo     |
+--------------------------------+---------+-----------+--------------------------------+------------------------------------+
4 rows in set (0.00 sec)

```

在上面的示例中，从索引 `intkey` 中读取最后 10 行。然后从表数据中检索这些 `RowID` 值。

## IndexReader

TiDB 支持_覆盖索引优化_。如果所有行都可以从索引中检索，TiDB 将跳过 `IndexLookup` 中通常需要的第二个步骤。考虑以下两个示例：

{{< copyable "sql" >}}

```sql
EXPLAIN SELECT * FROM t1 WHERE intkey = 123;
EXPLAIN SELECT id FROM t1 WHERE intkey = 123;
```

```sql
+-------------------------------+---------+-----------+--------------------------------+-----------------------------------+
| id                            | estRows | task      | access object                  | operator info                     |
+-------------------------------+---------+-----------+--------------------------------+-----------------------------------+
| IndexLookUp_10                | 1.00    | root      |                                |                                   |
| ├─IndexRangeScan_8(Build)     | 1.00    | cop[tikv] | table:t1, index:intkey(intkey) | range:[123,123], keep order:false |
| └─TableRowIDScan_9(Probe)     | 1.00    | cop[tikv] | table:t1                       | keep order:false                  |
+-------------------------------+---------+-----------+--------------------------------+-----------------------------------+
3 rows in set (0.00 sec)

+--------------------------+---------+-----------+--------------------------------+-----------------------------------+
| id                       | estRows | task      | access object                  | operator info                     |
+--------------------------+---------+-----------+--------------------------------+-----------------------------------+
| Projection_4             | 1.00    | root      |                                | test.t1.id                        |
| └─IndexReader_6          | 1.00    | root      |                                | index:IndexRangeScan_5            |
|   └─IndexRangeScan_5     | 1.00    | cop[tikv] | table:t1, index:intkey(intkey) | range:[123,123], keep order:false |
+--------------------------+---------+-----------+--------------------------------+-----------------------------------+
3 rows in set (0.00 sec)
```

因为 `id` 也是内部 `RowID`，所以它存储在 `intkey` 索引中。在使用 `intkey` 索引作为 `└─IndexRangeScan_5` 的一部分后，可以直接返回 `RowID` 的值。

## Point_Get 和 Batch_Point_Get

TiDB 在直接从主键或唯一键检索数据时使用 `Point_Get` 或 `Batch_Point_Get` 算子。这些算子比 `IndexLookup` 更高效。例如：

{{< copyable "sql" >}}

```sql
EXPLAIN SELECT * FROM t1 WHERE id = 1234;
EXPLAIN SELECT * FROM t1 WHERE id IN (1234,123);

ALTER TABLE t1 ADD unique_key INT;
UPDATE t1 SET unique_key = id;
ALTER TABLE t1 ADD UNIQUE KEY (unique_key);

EXPLAIN SELECT * FROM t1 WHERE unique_key = 1234;
EXPLAIN SELECT * FROM t1 WHERE unique_key IN (1234, 123);
```

```sql
+-------------+---------+------+---------------+---------------+
| id          | estRows | task | access object | operator info |
+-------------+---------+------+---------------+---------------+
| Point_Get_1 | 1.00    | root | table:t1      | handle:1234   |
+-------------+---------+------+---------------+---------------+
1 row in set (0.00 sec)

+-------------------+---------+------+---------------+-------------------------------------------------+
| id                | estRows | task | access object | operator info                                   |
+-------------------+---------+------+---------------+-------------------------------------------------+
| Batch_Point_Get_1 | 2.00    | root | table:t1      | handle:[1234 123], keep order:false, desc:false |
+-------------------+---------+------+---------------+-------------------------------------------------+
1 row in set (0.00 sec)

Query OK, 0 rows affected (0.27 sec)

Query OK, 1010 rows affected (0.06 sec)
Rows matched: 1010  Changed: 1010  Warnings: 0

Query OK, 0 rows affected (0.37 sec)

+-------------+---------+------+----------------------------------------+---------------+
| id          | estRows | task | access object                          | operator info |
+-------------+---------+------+----------------------------------------+---------------+
| Point_Get_1 | 1.00    | root | table:t1, index:unique_key(unique_key) |               |
+-------------+---------+------+----------------------------------------+---------------+
1 row in set (0.00 sec)

+-------------------+---------+------+----------------------------------------+------------------------------+
| id                | estRows | task | access object                          | operator info                |
+-------------------+---------+------+----------------------------------------+------------------------------+
| Batch_Point_Get_1 | 2.00    | root | table:t1, index:unique_key(unique_key) | keep order:false, desc:false |
+-------------------+---------+------+----------------------------------------+------------------------------+
1 row in set (0.00 sec)
```

## IndexFullScan

因为索引是有序的，所以 `IndexFullScan` 算子可以用来优化常见查询，例如索引值的 `MIN` 或 `MAX` 值：

{{< copyable "sql" >}}

```sql
EXPLAIN SELECT MIN(intkey) FROM t1;
EXPLAIN SELECT MAX(intkey) FROM t1;
```

```sql
+------------------------------+---------+-----------+--------------------------------+-------------------------------------+
| id                           | estRows | task      | access object                  | operator info                       |
+------------------------------+---------+-----------+--------------------------------+-------------------------------------+
| StreamAgg_12                 | 1.00    | root      |                                | funcs:min(test.t1.intkey)->Column#4 |
| └─Limit_16                   | 1.00    | root      |                                | offset:0, count:1                   |
|   └─IndexReader_29           | 1.00    | root      |                                | index:Limit_28                      |
|     └─Limit_28               | 1.00    | cop[tikv] |                                | offset:0, count:1                   |
|       └─IndexFullScan_27     | 1.00    | cop[tikv] | table:t1, index:intkey(intkey) | keep order:true                     |
+------------------------------+---------+-----------+--------------------------------+-------------------------------------+
5 rows in set (0.00 sec)

+------------------------------+---------+-----------+--------------------------------+-------------------------------------+
| id                           | estRows | task      | access object                  | operator info                       |
+------------------------------+---------+-----------+--------------------------------+-------------------------------------+
| StreamAgg_12                 | 1.00    | root      |                                | funcs:max(test.t1.intkey)->Column#4 |
| └─Limit_16                   | 1.00    | root      |                                | offset:0, count:1                   |
|   └─IndexReader_29           | 1.00    | root      |                                | index:Limit_28                      |
|     └─Limit_28               | 1.00    | cop[tikv] |                                | offset:0, count:1                   |
|       └─IndexFullScan_27     | 1.00    | cop[tikv] | table:t1, index:intkey(intkey) | keep order:true, desc               |
+------------------------------+---------+-----------+--------------------------------+-------------------------------------+
5 rows in set (0.00 sec)
```

在上述语句中，在每个 TiKV Region 上执行 `IndexFullScan` 任务。尽管名称为 `FullScan`，但只需要读取第一行（`└─Limit_28`）。每个 TiKV Region 将其 `MIN` 或 `MAX` 值返回给 TiDB，然后 TiDB 执行流式聚合以过滤出单行。带有聚合函数 `MAX` 或 `MIN` 的流式聚合还确保在表为空时返回 `NULL`。

相比之下，在未索引值上执行 `MIN` 函数将导致 `TableFullScan`。查询将需要扫描 TiKV 中的所有行，但执行 `TopN` 计算以确保每个 TiKV Region 只向 TiDB 返回一行。虽然 `TopN` 防止了 TiKV 和 TiDB 之间传输过多的行，但与上面的示例相比，这个语句仍然被认为效率低得多，因为 `MIN` 能够利用索引。

{{< copyable "sql" >}}

```sql
EXPLAIN SELECT MIN(pad1) FROM t1;
```

```sql
+--------------------------------+---------+-----------+---------------+-----------------------------------+
| id                             | estRows | task      | access object | operator info                     |
+--------------------------------+---------+-----------+---------------+-----------------------------------+
| StreamAgg_13                   | 1.00    | root      |               | funcs:min(test.t1.pad1)->Column#4 |
| └─TopN_14                      | 1.00    | root      |               | test.t1.pad1, offset:0, count:1   |
|   └─TableReader_23             | 1.00    | root      |               | data:TopN_22                      |
|     └─TopN_22                  | 1.00    | cop[tikv] |               | test.t1.pad1, offset:0, count:1   |
|       └─Selection_21           | 1008.99 | cop[tikv] |               | not(isnull(test.t1.pad1))         |
|         └─TableFullScan_20     | 1010.00 | cop[tikv] | table:t1      | keep order:false                  |
+--------------------------------+---------+-----------+---------------+-----------------------------------+
6 rows in set (0.00 sec)
```

以下语句将使用 `IndexFullScan` 算子扫描索引中的每一行：

{{< copyable "sql" >}}

```sql
EXPLAIN SELECT SUM(intkey) FROM t1;
EXPLAIN SELECT AVG(intkey) FROM t1;
```

```sql
+----------------------------+---------+-----------+--------------------------------+-------------------------------------+
| id                         | estRows | task      | access object                  | operator info                       |
+----------------------------+---------+-----------+--------------------------------+-------------------------------------+
| StreamAgg_20               | 1.00    | root      |                                | funcs:sum(Column#6)->Column#4       |
| └─IndexReader_21           | 1.00    | root      |                                | index:StreamAgg_8                   |
|   └─StreamAgg_8            | 1.00    | cop[tikv] |                                | funcs:sum(test.t1.intkey)->Column#6 |
|     └─IndexFullScan_19     | 1010.00 | cop[tikv] | table:t1, index:intkey(intkey) | keep order:false                    |
+----------------------------+---------+-----------+--------------------------------+-------------------------------------+
4 rows in set (0.00 sec)

+----------------------------+---------+-----------+--------------------------------+----------------------------------------------------------------------------+
| id                         | estRows | task      | access object                  | operator info                                                              |
+----------------------------+---------+-----------+--------------------------------+----------------------------------------------------------------------------+
| StreamAgg_20               | 1.00    | root      |                                | funcs:avg(Column#7, Column#8)->Column#4                                    |
| └─IndexReader_21           | 1.00    | root      |                                | index:StreamAgg_8                                                          |
|   └─StreamAgg_8            | 1.00    | cop[tikv] |                                | funcs:count(test.t1.intkey)->Column#7, funcs:sum(test.t1.intkey)->Column#8 |
|     └─IndexFullScan_19     | 1010.00 | cop[tikv] | table:t1, index:intkey(intkey) | keep order:false                                                           |
+----------------------------+---------+-----------+--------------------------------+----------------------------------------------------------------------------+
4 rows in set (0.00 sec)
```

在上面的示例中，`IndexFullScan` 比 `TableFullScan` 更高效，因为 `(intkey + RowID)` 索引中的值宽度小于完整行的宽度。

以下语句不支持使用 `IndexFullScan` 算子，因为需要从表中获取额外的列：

{{< copyable "sql" >}}

```sql
EXPLAIN SELECT AVG(intkey), ANY_VALUE(pad1) FROM t1;
```

```sql
+------------------------------+---------+-----------+---------------+-----------------------------------------------------------------------------------------------------------------------+
| id                           | estRows | task      | access object | operator info                                                                                                         |
+------------------------------+---------+-----------+---------------+-----------------------------------------------------------------------------------------------------------------------+
| Projection_4                 | 1.00    | root      |               | Column#4, any_value(test.t1.pad1)->Column#5                                                                           |
| └─StreamAgg_16               | 1.00    | root      |               | funcs:avg(Column#10, Column#11)->Column#4, funcs:firstrow(Column#12)->test.t1.pad1                                    |
|   └─TableReader_17           | 1.00    | root      |               | data:StreamAgg_8                                                                                                      |
|     └─StreamAgg_8            | 1.00    | cop[tikv] |               | funcs:count(test.t1.intkey)->Column#10, funcs:sum(test.t1.intkey)->Column#11, funcs:firstrow(test.t1.pad1)->Column#12 |
|       └─TableFullScan_15     | 1010.00 | cop[tikv] | table:t1      | keep order:false                                                                                                      |
+------------------------------+---------+-----------+---------------+-----------------------------------------------------------------------------------------------------------------------+
5 rows in set (0.00 sec)
```
