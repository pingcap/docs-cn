---
title: Understand the Query Execution Plan
summary: Learn about the execution plan information returned by the `EXPLAIN` statement in TiDB.
category: user guide
---

# Understand the Query Execution Plan

Based on the details of your tables, the TiDB optimizer chooses the most efficient query execution plan, which consists of a series of operators. This document details the execution plan information returned by the `EXPLAIN` statement in TiDB.

## Optimize SQL statements using `EXPLAIN`

The result of the `EXPLAIN` statement provides information about how TiDB executes SQL queries:

- `EXPLAIN` works together with `SELECT`, `DELETE`, `INSERT`, `REPLACE`, and `UPDATE`.
- When you run the `EXPLAIN` statement, TiDB returns the final physical execution plan which is optimized by the SQL statement of `EXPLAIN`. In other words, `EXPLAIN` displays the complete information about how TiDB executes the SQL statement, such as in which order, how tables are joined, and what the expression tree looks like. For more information, see [`EXPLAIN` output format](#explain-output-format).
- TiDB does not support `EXPLAIN [options] FOR CONNECTION connection_id` currently. We'll do it in the future. For more information, see [#4351](https://github.com/pingcap/tidb/issues/4351).

The results of `EXPLAIN` shed light on how to index the data tables so that the execution plan can use the index to speed up the execution of SQL statements. You can also use `EXPLAIN` to check if the optimizer chooses the optimal order to join tables.

## <span id="explain-output-format">`EXPLAIN` output format</span>

Currently, the `EXPLAIN` statement returns the following four columns: id, count, task, operator info. Each operator in the execution plan is described by the four properties. In the results returned by `EXPLAIN`, each row describes an operator. See the following table for details:

| Property Name | Description |
| -----| ------------- |
| id | The id of an operator, to identify the uniqueness of an operator in the entire execution plan. As of TiDB 2.1, the id includes formatting to show a tree structure of operators. The data flows from a child to its parent, and each operator has one and only one parent. |  
| count | An estimation of the number of data items that the current operator outputs, based on the statistics and the execution logic of the operator | 
| task | the task that the current operator belongs to. The current execution plan contains two types of tasks: 1) the **root** task that runs on the TiDB server; 2) the **cop** task that runs concurrently on the TiKV server. The topological relations of the current execution plan in the task level is that a root task can be followed by many cop tasks. The root task uses the output of cop task as the input. The cop task executes the tasks that TiDB pushes to TiKV. Each cop task scatters in the TiKV cluster and is executed by multiple processes. |
| operator info | The details about each operator. The information of each operator differs from others, see [Operator Info](#operator-info).|

### Example usage

Using the [bikeshare example database](../bikeshare-example-database.md):

```sql
mysql> EXPLAIN SELECT count(*) FROM trips WHERE start_date BETWEEN '2017-07-01 00:00:00' AND '2017-07-01 23:59:59';
+--------------------------+-------------+------+------------------------------------------------------------------------------------------------------------------------+
| id                       | count       | task | operator info                                                                                                          |
+--------------------------+-------------+------+------------------------------------------------------------------------------------------------------------------------+
| StreamAgg_20             | 1.00        | root | funcs:count(col_0)                                                                                                     |
| └─TableReader_21         | 1.00        | root | data:StreamAgg_9                                                                                                       |
|   └─StreamAgg_9          | 1.00        | cop  | funcs:count(1)                                                                                                         |
|     └─Selection_19       | 8166.73     | cop  | ge(bikeshare.trips.start_date, 2017-07-01 00:00:00.000000), le(bikeshare.trips.start_date, 2017-07-01 23:59:59.000000) |
|       └─TableScan_18     | 19117643.00 | cop  | table:trips, range:[-inf,+inf], keep order:false                                                                       |
+--------------------------+-------------+------+------------------------------------------------------------------------------------------------------------------------+
5 rows in set (0.00 sec)
```

Here you can see that the coprocesor (cop) needs to scan the table `trips` to find rows that match the criteria of `start_date`. Rows that meet this criteria are determined in `Selection_19` and passed to `StreamAgg_9`, all still within the coprocessor (i.e. inside of TiKV). The `count` column shows an approximate number of rows that will be processed, which is estimated with the help of table statistics. In this query it is estimated that each of the TiKV nodes will return `1.00` row to TiDB (as `TableReader_21`), which are then aggregated as `StreamAgg_20` to return an estimated `1.00` row to the client.

The good news with this query is that most of the work is pushed down to the coprocessor. This means that minimal data transfer is required for query execution. However, the `TableScan_18` can be eliminated by adding an index to speed up queries on `start_date`:

```sql
mysql> ALTER TABLE trips ADD INDEX (start_date);
..
mysql> EXPLAIN SELECT count(*) FROM trips WHERE start_date BETWEEN '2017-07-01 00:00:00' AND '2017-07-01 23:59:59';
+------------------------+---------+------+--------------------------------------------------------------------------------------------------+
| id                     | count   | task | operator info                                                                                    |
+------------------------+---------+------+--------------------------------------------------------------------------------------------------+
| StreamAgg_25           | 1.00    | root | funcs:count(col_0)                                                                               |
| └─IndexReader_26       | 1.00    | root | index:StreamAgg_9                                                                                |
|   └─StreamAgg_9        | 1.00    | cop  | funcs:count(1)                                                                                   |
|     └─IndexScan_24     | 8166.73 | cop  | table:trips, index:start_date, range:[2017-07-01 00:00:00,2017-07-01 23:59:59], keep order:false |
+------------------------+---------+------+--------------------------------------------------------------------------------------------------+
4 rows in set (0.01 sec)
```

In the revisited `EXPLAIN` you can see the count of rows scanned has reduced via the use of an index. On a reference system, the query execution time reduced from 50.41 seconds to 0.00 seconds!

## <span id="explain-analyze-output-format">`EXPLAIN ANALYZE` output format</span>

As an extension to `EXPLAIN`, `EXPLAIN ANALYZE` will execute the query and provide additional execution statistics in the `execution info` column as follows:

* `time` shows the total wall time from entering the operator until exiting the execution. It includes all execution time of any child operator operations. If the operator is called multiple times (`loops`) from a parent operator, the time will be the cumulative time.

* `loops` is the number of times the operator was called from the parent operator.

* `rows` is the total number of rows that were returned by this operator. So for example, you can compare the accuracy of the `count` column to `rows`/`loops` in the `execution_info` column to assess how accurate the query optimizer's estimations are.

### Example usage

```sql
mysql> EXPLAIN ANALYZE SELECT count(*) FROM trips WHERE start_date BETWEEN '2017-07-01 00:00:00' AND '2017-07-01 23:59:59';
+------------------------+---------+------+--------------------------------------------------------------------------------------------------+-----------------------------------+
| id                     | count   | task | operator info                                                                                    | execution info                    |
+------------------------+---------+------+--------------------------------------------------------------------------------------------------+-----------------------------------+
| StreamAgg_25           | 1.00    | root | funcs:count(col_0)                                                                               | time:79.851424ms, loops:2, rows:1 |
| └─IndexReader_26       | 1.00    | root | index:StreamAgg_9                                                                                | time:79.835575ms, loops:2, rows:1 |
|   └─StreamAgg_9        | 1.00    | cop  | funcs:count(1)                                                                                   |                                   |
|     └─IndexScan_24     | 8161.83 | cop  | table:trips, index:start_date, range:[2017-07-01 00:00:00,2017-07-01 23:59:59], keep order:false |                                   |
+------------------------+---------+------+--------------------------------------------------------------------------------------------------+-----------------------------------+
4 rows in set (0.08 sec)
```

## Overview

### Introduction to task

Currently, there are two types of task execution: cop tasks and root tasks. A cop task refers to a computing task that is executed using the TiKV coprocessor. A root task refers to a computing task that is executed in TiDB.

One of the goals of SQL optimization is to push the calculation down to TiKV as much as possible. The TiKV coprocessor is able to assist in execution of SQL functions (both aggregate and scalar), SQL `LIMIT` operations, index scans, and table scans. All join operations, however, will be performed as root tasks.

### Table data and index data

The table data in TiDB refers to the raw data of a table, which is stored in TiKV. For each row of the table data, its key is a 64-bit integer called Handle ID. If a table has int type primary key, the value of the primary key is taken as the Handle ID of the table data, otherwise the system automatically generates the Handle ID. The value of the table data is encoded by all the data in this row. When the table data is read, return the results in the order in which the Handle ID is incremented.

Similar to the table data, the index data in TiDB is also stored in TiKV. The key of index data is ordered bytes encoded by index columns. The value is the Handle ID of each row of index data. You can use the Handle ID to read the non-index columns in this row. When the index data is read, return the results in the order in which the index columns are incremented. If the case of multiple index columns, make sure that the first column is incremented and that the i + 1 column is incremented when the i column is equal.

### Range query

In the WHERE/HAVING/ON condition, analyze the results returned by primary key or index key queries. For example, number and date types of comparison symbols, greater than, less than, equal to, greater than or equal to, less than or equal to, and character type LIKE symbols.

TiDB only supports the comparison symbols of which one side is a column and the other side is a constant or can be calculated as a constant. Query conditions like `year(birth_day) < 1992` cannot use the index. Try to use the same type to compare: additional cast operations prevent the index from being used. For example, in `user_id = 123456`, if the `user_id` is a string, you need to write `123456` as a string constant.

Using `AND` and `OR` combination on the range query conditions of the same column is equivalent to getting the intersection or union set. For multidimensional combined indexes, you can write the conditions for multiple columns. For example, in the `(a, b, c)` combined index, when `a` is an equivalent query, you can continue to calculate the query range of `b`; when `b` is also an equivalent query, you can continue to calculate the query range of `c`; otherwise, if `a` is a non-equivalent query, you can only calculate the query range of `a`.

## Operator info

### TableReader and TableScan

TableScan refers to scanning the table data at the KV side. TableReader refers to reading the table data from TiKV at the TiDB side. TableReader and TableScan are the two operators of one function. The `table` represents the table name in SQL statements. If the table is renamed, it displays the new name. The `range` represents the range of scanned data. If the WHERE/HAVING/ON condition is not specified in the query, full table scan is executed. If the range query condition is specified on the int type primary keys, range query is executed. The `keep order` indicates whether the table scan is returned in order.

### IndexReader and IndexLookUp

The index data in TiDB is read in two ways: 1) IndexReader represents reading the index columns directly from the index, which is used when only index related columns or primary keys are quoted in SQL statements; 2) IndexLookUp represents filtering part of the data from the index, returning only the Handle ID, and retrieving the table data again using Handle ID. In the second way, data is retrieved twice from TiKV. The way of reading index data is automatically selected by the optimizer.

Similar to TableScan, IndexScan is the operator to read index data in the KV side. The `table` represents the table name in SQL statements. If the table is renamed, it displays the new name. The `index` represents the index name. The `range` represents the range of scanned data. The `out of order` indicates whether the index scan is returned in order. In TiDB, the primary key composed of multiple columns or non-int columns is treated as the unique index.

### Selection

Selection represents the selection conditions in SQL statements, usually used in WHERE/HAVING/ON clause. 

### Projection

Projection corresponds to the `SELECT` list in SQL statements, used to map the input data into new output data.

### Aggregation

Aggregation corresponds to `Group By` in SQL statements, or the aggregate functions if the `Group By` statement does not exist, such as the `COUNT` or `SUM` function. TiDB supports two aggregation algorithms: Hash Aggregation and Stream Aggregation. Hash Aggregation is a hash-based aggregation algorithm. If Hash Aggregation is close to the read operator of Table or Index, the aggregation operator pre-aggregates in TiKV to improve the concurrency and reduce the network load.

### Join

TiDB supports Inner Join and Left/Right Outer Join, and automatically converts the external connection that can be simplified to Inner Join.

TiDB supports three Join algorithms: Hash Join, Sort Merge Join and Index Look up Join. The principle of Hash Join is to pre-load the memory with small tables involved in the connection and read all the data of big tables to connect. The principle of Sort Merge Join is to read the data of two tables at the same time and compare one by one using the order information of the input data. Index Look Up Join reads data of external tables and executes primary key or index key queries on internal tables.

### Apply

Apply is an operator used to describe subqueries in TiDB. The behavior of Apply is similar to Nested Loop. The Apply operator retrieves one piece of data from external tables, puts it into the associated column of the internal tables, executes and calculates the connection according to the inline Join algorithm in Apply.

Generally, the Apply operator is automatically converted to a Join operation by the query optimizer. Therefore, try to avoid using the Apply operator when you write SQL statements.
