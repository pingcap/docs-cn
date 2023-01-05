---
title: SQL Performance Tuning
summary: Introduces TiDB's SQL performance tuning scheme and analysis approach.
---

# SQL Performance Tuning

This document introduces some common reasons for slow SQL statements and techniques for tuning SQL performance.

## Before you begin

You can use [`tiup demo` import](/develop/dev-guide-bookshop-schema-design.md#method-1-via-tiup-demo) to prepare data:

```shell
tiup demo bookshop prepare --host 127.0.0.1 --port 4000 --books 1000000
```

Or [using the Import feature of TiDB Cloud](/develop/dev-guide-bookshop-schema-design.md#method-2-via-tidb-cloud-import) to import the pre-prepared sample data.

## Issue: Full table scan

The most common reason for slow SQL queries is that the `SELECT` statements perform full table scan or use incorrect indexes.

When TiDB retrieves a small number of rows from a large table based on a column that is not the primary key or in the secondary index, the performance is usually poor:

```sql
SELECT * FROM books WHERE title = 'Marian Yost';
```

```sql
+------------+-------------+-----------------------+---------------------+-------+--------+
| id         | title       | type                  | published_at        | stock | price  |
+------------+-------------+-----------------------+---------------------+-------+--------+
| 65670536   | Marian Yost | Arts                  | 1950-04-09 06:28:58 | 542   | 435.01 |
| 1164070689 | Marian Yost | Education & Reference | 1916-05-27 12:15:35 | 216   | 328.18 |
| 1414277591 | Marian Yost | Arts                  | 1932-06-15 09:18:14 | 303   | 496.52 |
| 2305318593 | Marian Yost | Arts                  | 2000-08-15 19:40:58 | 398   | 402.90 |
| 2638226326 | Marian Yost | Sports                | 1952-04-02 12:40:37 | 191   | 174.64 |
+------------+-------------+-----------------------+---------------------+-------+--------+
5 rows in set
Time: 0.582s
```

To understand why this query is slow, you can use `EXPLAIN` to see the execution plan:

```sql
EXPLAIN SELECT * FROM books WHERE title = 'Marian Yost';
```

```sql
+---------------------+------------+-----------+---------------+-----------------------------------------+
| id                  | estRows    | task      | access object | operator info                           |
+---------------------+------------+-----------+---------------+-----------------------------------------+
| TableReader_7       | 1.27       | root      |               | data:Selection_6                        |
| └─Selection_6       | 1.27       | cop[tikv] |               | eq(bookshop.books.title, "Marian Yost") |
|   └─TableFullScan_5 | 1000000.00 | cop[tikv] | table:books   | keep order:false                        |
+---------------------+------------+-----------+---------------+-----------------------------------------+
```

As can be seen from `TableFullScan_5` in the execution plan, TiDB performs a full table scan on the `books` table and checks whether `title` satisfies the condition for each row. The `estRows` value of `TableFullScan_5` is `1000000.00`, which means the optimizer estimates that this full table scan takes `1000000.00` rows of data.

For more information about the usage of `EXPLAIN`, see [`EXPLAIN` Walkthrough](/explain-walkthrough.md).

### Solution: Use secondary index

To speed up this query above, add a secondary index on the `books.title` column:

```sql
CREATE INDEX title_idx ON books (title);
```

The query execution is much faster:

```sql
SELECT * FROM books WHERE title = 'Marian Yost';
```

```sql
+------------+-------------+-----------------------+---------------------+-------+--------+
| id         | title       | type                  | published_at        | stock | price  |
+------------+-------------+-----------------------+---------------------+-------+--------+
| 1164070689 | Marian Yost | Education & Reference | 1916-05-27 12:15:35 | 216   | 328.18 |
| 1414277591 | Marian Yost | Arts                  | 1932-06-15 09:18:14 | 303   | 496.52 |
| 2305318593 | Marian Yost | Arts                  | 2000-08-15 19:40:58 | 398   | 402.90 |
| 2638226326 | Marian Yost | Sports                | 1952-04-02 12:40:37 | 191   | 174.64 |
| 65670536   | Marian Yost | Arts                  | 1950-04-09 06:28:58 | 542   | 435.01 |
+------------+-------------+-----------------------+---------------------+-------+--------+
5 rows in set
Time: 0.007s
```

To understand why the performance is improved, use `EXPLAIN` to see the new execution plan:

```sql
EXPLAIN SELECT * FROM books WHERE title = 'Marian Yost';
```

```sql
+---------------------------+---------+-----------+-------------------------------------+-------------------------------------------------------+
| id                        | estRows | task      | access object                       | operator info                                         |
+---------------------------+---------+-----------+-------------------------------------+-------------------------------------------------------+
| IndexLookUp_10            | 1.27    | root      |                                     |                                                       |
| ├─IndexRangeScan_8(Build) | 1.27    | cop[tikv] | table:books, index:title_idx(title) | range:["Marian Yost","Marian Yost"], keep order:false |
| └─TableRowIDScan_9(Probe) | 1.27    | cop[tikv] | table:books                         | keep order:false                                      |
+---------------------------+---------+-----------+-------------------------------------+-------------------------------------------------------+
```

As can be seen from `IndexLookup_10` in the execution plan, TiDB queries the data by the `title_idx` index. Its `estRows` value is `1.27`, which means that the optimizer estimates that only `1.27` rows are scanned. The estimated rows scanned are much fewer than the `1000000.00` rows of data in the full table scan.

The `IndexLookup_10` execution plan is to first use the `IndexRangeScan_8` operator to read the index data that meets the condition through the `title_idx` index, and then use the `TableLookup_9` operator to query the corresponding rows according to the Row ID stored in the index data.

For more information on the TiDB execution plan, see [TiDB Query Execution Plan Overview](/explain-overview.md).

### Solution: Use covering index

If the index is a covering index, which contains all the columns queried by the SQL statements, scanning the index data is sufficient for the query.

For example, in the following query, you only need to query the corresponding `price` based on `title`:

```sql
SELECT title, price FROM books WHERE title = 'Marian Yost';
```

```sql
+-------------+--------+
| title       | price  |
+-------------+--------+
| Marian Yost | 435.01 |
| Marian Yost | 328.18 |
| Marian Yost | 496.52 |
| Marian Yost | 402.90 |
| Marian Yost | 174.64 |
+-------------+--------+
5 rows in set
Time: 0.007s
```

Because the `title_idx` index only contains data in the `title` column, TiDB still needs to first scan the index data and then query the `price` column from the table.

```sql
EXPLAIN SELECT title, price FROM books WHERE title = 'Marian Yost';
```

```sql
+---------------------------+---------+-----------+-------------------------------------+-------------------------------------------------------+
| id                        | estRows | task      | access object                       | operator info                                         |
+---------------------------+---------+-----------+-------------------------------------+-------------------------------------------------------+
| IndexLookUp_10            | 1.27    | root      |                                     |                                                       |
| ├─IndexRangeScan_8(Build) | 1.27    | cop[tikv] | table:books, index:title_idx(title) | range:["Marian Yost","Marian Yost"], keep order:false |
| └─TableRowIDScan_9(Probe) | 1.27    | cop[tikv] | table:books                         | keep order:false                                      |
+---------------------------+---------+-----------+-------------------------------------+-------------------------------------------------------+
```

To optimize the performance, drop the `title_idx` index and create a new covering index `title_price_idx`:

```sql
ALTER TABLE books DROP INDEX title_idx;
```

```sql
CREATE INDEX title_price_idx ON books (title, price);
```

Because the `price` data is stored in the `title_price_idx` index, the following query only needs to scan the index data:

```sql
EXPLAIN SELECT title, price FROM books WHERE title = 'Marian Yost';
```

```sql
--------------------+---------+-----------+--------------------------------------------------+-------------------------------------------------------+
| id                 | estRows | task      | access object                                    | operator info                                         |
+--------------------+---------+-----------+--------------------------------------------------+-------------------------------------------------------+
| IndexReader_6      | 1.27    | root      |                                                  | index:IndexRangeScan_5                                |
| └─IndexRangeScan_5 | 1.27    | cop[tikv] | table:books, index:title_price_idx(title, price) | range:["Marian Yost","Marian Yost"], keep order:false |
+--------------------+---------+-----------+--------------------------------------------------+-------------------------------------------------------+
```

Now this query runs faster:

```sql
SELECT title, price FROM books WHERE title = 'Marian Yost';
```

```sql
+-------------+--------+
| title       | price  |
+-------------+--------+
| Marian Yost | 174.64 |
| Marian Yost | 328.18 |
| Marian Yost | 402.90 |
| Marian Yost | 435.01 |
| Marian Yost | 496.52 |
+-------------+--------+
5 rows in set
Time: 0.004s
```

Since the `books` table will be used in later examples, drop the `title_price_idx` index:

```sql
ALTER TABLE books DROP INDEX title_price_idx;
```

### Solution: Use primary index

If a query uses the primary key to filter data, the query runs fast. For example, the primary key of the `books` table is the `id` column, so you can use the `id` column to query data:

```sql
SELECT * FROM books WHERE id = 896;
```

```sql
+-----+----------------+----------------------+---------------------+-------+--------+
| id  | title          | type                 | published_at        | stock | price  |
+-----+----------------+----------------------+---------------------+-------+--------+
| 896 | Kathryne Doyle | Science & Technology | 1969-03-18 01:34:15 | 468   | 281.32 |
+-----+----------------+----------------------+---------------------+-------+--------+
1 row in set
Time: 0.004s
```

Use `EXPLAIN` to see the execution plan:

```sql
EXPLAIN SELECT * FROM books WHERE id = 896;
```

```sql
+-------------+---------+------+---------------+---------------+
| id          | estRows | task | access object | operator info |
+-------------+---------+------+---------------+---------------+
| Point_Get_1 | 1.00    | root | table:books   | handle:896    |
+-------------+---------+------+---------------+---------------+
```

`Point_Get` is a very fast execute plan.

## Use the right join type

See [JOIN Execution Plan](/explain-joins.md).

### See also

* [EXPLAIN Walkthrough](/explain-walkthrough.md)
* [Explain Statements That Use Indexes](/explain-indexes.md)
