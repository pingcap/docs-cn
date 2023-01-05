---
title: HTAP Queries
summary: Introduce the HTAP queries in TiDB.
---

# HTAP Queries

HTAP stands for Hybrid Transactional and Analytical Processing. Traditionally, databases are often designed for transactional or analytical scenarios, so the data platform often needs to be split into Transactional Processing and Analytical Processing, and the data needs to be replicated from the transactional database to the analytical database for quick response to analytical queries. TiDB databases can perform both transactional and analytical tasks, which greatly simplifies the construction of data platforms and allows users to use fresher data for analysis.

TiDB uses TiKV, a row-based storage engine, for Online Transactional Processing (OLTP), and TiFlash, a columnar storage engine, for Online Analytical Processing (OLAP). The row-based storage engine and the columnar storage engine co-exist for HTAP. Both storage engines can replicate data automatically and keep strong consistency. The row-based storage engine optimizes OLTP performance, and the columnar storage engine optimizes OLAP performance.

The [Create a table](/develop/dev-guide-create-table.md#use-htap-capabilities) section introduces how to enable the HTAP capability of TiDB. The following describes how to use HTAP to analyze data faster.

## Data preparation

Before starting, you can import more sample data [via the `tiup demo` command](/develop/dev-guide-bookshop-schema-design.md#method-1-via-tiup-demo). For example:

```shell
tiup demo bookshop prepare --users=200000 --books=500000 --authors=100000 --ratings=1000000 --orders=1000000 --host 127.0.0.1 --port 4000 --drop-tables
```

Or you can [use the Import function of TiDB Cloud](/develop/dev-guide-bookshop-schema-design.md#method-2-via-tidb-cloud-import) to import the pre-prepared sample data.

## Window functions

When using a database, in addition to storing your data and providing application features (such as ordering and rating books), you might also need to analyze the data in the database to make further operations and decisions.

The [Query data from a single table](/develop/dev-guide-get-data-from-single-table.md) document introduces how to use aggregate queries to analyze data as a whole. In more complex scenarios, you might want to aggregate the results of multiple aggregation queries into a single query. If you want to know the historical trend of the order amount of a particular book, you can aggregate `sum` for all order data of each month, and then aggregate the `sum` results together to get the historical trend.

To facilitate such analysis, since TiDB v3.0, TiDB supports window functions. For each row of data, this function provides the ability to access data across multiple rows. Different from a regular aggregation query, the window function aggregates rows without merging results set into a single row.

Similar to aggregate functions, you also need to follow a fixed set of syntax when using the window function:

```sql
SELECT
    window_function() OVER ([partition_clause] [order_clause] [frame_clause]) AS alias
FROM
    table_name
```

### `ORDER BY` clause

With the aggregate window function `sum()`, you can analyze the historical trend of the order amount of a particular book. For example:

```sql
WITH orders_group_by_month AS (
  SELECT DATE_FORMAT(ordered_at, '%Y-%c') AS month, COUNT(*) AS orders
  FROM orders
  WHERE book_id = 3461722937
  GROUP BY 1
)
SELECT
month,
SUM(orders) OVER(ORDER BY month ASC) as acc
FROM orders_group_by_month
ORDER BY month ASC;
```

The `sum()` function accumulates the data in the order specified by the `ORDER BY` statement in the `OVER` clause. The result is as follows:

```
+---------+-------+
| month   | acc   |
+---------+-------+
| 2011-5  |     1 |
| 2011-8  |     2 |
| 2012-1  |     3 |
| 2012-2  |     4 |
| 2013-1  |     5 |
| 2013-3  |     6 |
| 2015-11 |     7 |
| 2015-4  |     8 |
| 2015-8  |     9 |
| 2017-11 |    10 |
| 2017-5  |    11 |
| 2019-5  |    13 |
| 2020-2  |    14 |
+---------+-------+
13 rows in set (0.01 sec)
```

Visualize the above data through a line chart with time as the horizontal axis and cumulative order amount as the vertical axis. You can easily know the historical ordering trend of the book through the change of the slope.

### `PARTITION BY` clause

Suppose that you want to analyze the historical ordering trend of different types of books, and visualize it in the same line chart with multiple series.

You can use the `PARTITION BY` clause to group books by types and count history orders for each type separately.

```sql
WITH orders_group_by_month AS (
    SELECT
        b.type AS book_type,
        DATE_FORMAT(ordered_at, '%Y-%c') AS month,
        COUNT(*) AS orders
    FROM orders o
    LEFT JOIN books b ON o.book_id = b.id
    WHERE b.type IS NOT NULL
    GROUP BY book_type, month
), acc AS (
    SELECT
        book_type,
        month,
        SUM(orders) OVER(PARTITION BY book_type ORDER BY book_type, month ASC) as acc
    FROM orders_group_by_month
    ORDER BY book_type, month ASC
)
SELECT * FROM acc;
```

The result is as follows:

```
+------------------------------+---------+------+
| book_type                    | month   | acc  |
+------------------------------+---------+------+
| Magazine                     | 2011-10 |    1 |
| Magazine                     | 2011-8  |    2 |
| Magazine                     | 2012-5  |    3 |
| Magazine                     | 2013-1  |    4 |
| Magazine                     | 2013-6  |    5 |
...
| Novel                        | 2011-3  |   13 |
| Novel                        | 2011-4  |   14 |
| Novel                        | 2011-6  |   15 |
| Novel                        | 2011-8  |   17 |
| Novel                        | 2012-1  |   18 |
| Novel                        | 2012-2  |   20 |
...
| Sports                       | 2021-4  |   49 |
| Sports                       | 2021-7  |   50 |
| Sports                       | 2022-4  |   51 |
+------------------------------+---------+------+
1500 rows in set (1.70 sec)
```

### Non-aggregate window functions

TiDB also provides some non-aggregated [window functions](/functions-and-operators/window-functions.md) for more analysis statements.

For example, the [Pagination Query](/develop/dev-guide-paginate-results.md) document introduces how to use the `row_number()` function to achieve efficient pagination batch processing.

## Hybrid workload

When using TiDB for real-time online analytical processing in hybrid load scenarios, you only need to provide an entry point of TiDB to your data. TiDB automatically selects different processing engines based on the specific business.

### Create TiFlash replicas

TiDB uses the row-based storage engine, TiKV, by default. To use the columnar storage engine, TiFlash, see [Enable HTAP capability](/develop/dev-guide-create-table.md#use-htap-capabilities). Before querying data through TiFlash, you need to create TiFlash replicas for `books` and `orders` tables using the following statement:

```sql
ALTER TABLE books SET TIFLASH REPLICA 1;
ALTER TABLE orders SET TIFLASH REPLICA 1;
```

You can check the progress of the TiFlash replicas using the following statement:

```sql
SELECT * FROM information_schema.tiflash_replica WHERE TABLE_SCHEMA = 'bookshop' and TABLE_NAME = 'books';
SELECT * FROM information_schema.tiflash_replica WHERE TABLE_SCHEMA = 'bookshop' and TABLE_NAME = 'orders';
```

A `PROGRESS` column of 1 indicates that the progress is 100% complete, and a `AVAILABLE` column of 1 indicates that the replica is currently available.

```
+--------------+------------+----------+---------------+-----------------+-----------+----------+
| TABLE_SCHEMA | TABLE_NAME | TABLE_ID | REPLICA_COUNT | LOCATION_LABELS | AVAILABLE | PROGRESS |
+--------------+------------+----------+---------------+-----------------+-----------+----------+
| bookshop     | books      |      143 |             1 |                 |         1 |        1 |
+--------------+------------+----------+---------------+-----------------+-----------+----------+
1 row in set (0.07 sec)
+--------------+------------+----------+---------------+-----------------+-----------+----------+
| TABLE_SCHEMA | TABLE_NAME | TABLE_ID | REPLICA_COUNT | LOCATION_LABELS | AVAILABLE | PROGRESS |
+--------------+------------+----------+---------------+-----------------+-----------+----------+
| bookshop     | orders     |      147 |             1 |                 |         1 |        1 |
+--------------+------------+----------+---------------+-----------------+-----------+----------+
1 row in set (0.07 sec)
```

After replicas are added, you can use the `EXPLAIN` statement to check the execution plan of the above window function [`PARTITION BY` clause](#partition-by-clause). If `cop[tiflash]` appears in the execution plan, it means that the TiFlash engine has started to work.

Then, execute the sample SQL statement in [`PARTITION BY` clause](#partition-by-clause) again. The result is as follows:

```
+------------------------------+---------+------+
| book_type                    | month   | acc  |
+------------------------------+---------+------+
| Magazine                     | 2011-10 |    1 |
| Magazine                     | 2011-8  |    2 |
| Magazine                     | 2012-5  |    3 |
| Magazine                     | 2013-1  |    4 |
| Magazine                     | 2013-6  |    5 |
...
| Novel                        | 2011-3  |   13 |
| Novel                        | 2011-4  |   14 |
| Novel                        | 2011-6  |   15 |
| Novel                        | 2011-8  |   17 |
| Novel                        | 2012-1  |   18 |
| Novel                        | 2012-2  |   20 |
...
| Sports                       | 2021-4  |   49 |
| Sports                       | 2021-7  |   50 |
| Sports                       | 2022-4  |   51 |
+------------------------------+---------+------+
1500 rows in set (0.79 sec)
```

By comparing the two execution results, you can find that the query speed is significantly improved with TiFlash (the improvement is more significant with a large volume of data). This is because a window function usually relies on a full table scan for some columns, and columnar TiFlash is more suitable to handle this type of analytical task than row-based TiKV. For TiKV, if you use primary keys or indexes to reduce the number of rows to be queried, the queries can be fast too and consume fewer resources compared with TiFlash.

### Specify a query engine

TiDB uses the Cost Based Optimizer (CBO) to automatically choose whether to use TiFlash replicas based on cost estimates. However, if you are sure whether your query is transactional or analytical, you can specify the query engine to be used with [Optimizer Hints](/optimizer-hints.md).

To specify which engine to be used in a query, you can use the `/*+ read_from_storage(engine_name[table_name]) */` hint as in the following statement.

> **Note:**
>
> - If a table has an alias, use the alias instead of the table name in the hint, otherwise, the hint does not work.
> - The `read_from_storage` hint does not work for [common table expression](/develop/dev-guide-use-common-table-expression.md).

```sql
WITH orders_group_by_month AS (
    SELECT
        /*+ read_from_storage(tikv[o]) */
        b.type AS book_type,
        DATE_FORMAT(ordered_at, '%Y-%c') AS month,
        COUNT(*) AS orders
    FROM orders o
    LEFT JOIN books b ON o.book_id = b.id
    WHERE b.type IS NOT NULL
    GROUP BY book_type, month
), acc AS (
    SELECT
        book_type,
        month,
        SUM(orders) OVER(PARTITION BY book_type ORDER BY book_type, month ASC) as acc
    FROM orders_group_by_month mo
    ORDER BY book_type, month ASC
)
SELECT * FROM acc;
```

You can use the `EXPLAIN` statement to check the execution plan of the above SQL statement. If `cop[tiflash]` and `cop[tikv]` appear in the task column at the same time, it means that TiFlash and TiKV are both scheduled to complete this query. Note that TiFlash and TiKV storage engines usually use different TiDB nodes, so the two query types are not affected by each other.

For more information about how TiDB chooses to use TiFlash, see [Use TiDB to read TiFlash replicas](/tiflash/use-tidb-to-read-tiflash.md)

## Read more

<CustomContent platform="tidb">

- [Quick Start with HTAP](/quick-start-with-htap.md)
- [Explore HTAP](/explore-htap.md)

</CustomContent>

<CustomContent platform="tidb-cloud">

- [TiDB Cloud HTAP Quick Start](/tidb-cloud/tidb-cloud-htap-quickstart.md)

</CustomContent>

- [Window Functions](/functions-and-operators/window-functions.md)
- [Use TiFlash](/tiflash/tiflash-overview.md#use-tiflash)
