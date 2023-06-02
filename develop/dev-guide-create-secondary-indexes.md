---
title: Create a Secondary Index
summary: Learn steps, rules, and examples to create a secondary index.
---

# Create a Secondary Index

This document describes how to create a secondary index using SQL and various programming languages and lists the rules of index creation. In this document, the [Bookshop](/develop/dev-guide-bookshop-schema-design.md) application is taken as an example to walk you through the steps of secondary index creation.

## Before you start

Before creating a secondary index, do the following:

- [Build a TiDB Serverless Cluster](/develop/dev-guide-build-cluster-in-cloud.md).
- Read [Schema Design Overview](/develop/dev-guide-schema-design-overview.md).
- [Create a Database](/develop/dev-guide-create-database.md).
- [Create a Table](/develop/dev-guide-create-table.md).

## What is secondary index

A secondary index is a logical object in a TiDB cluster. You can simply regard it as a sorting type of data that TiDB uses to improve the query performance. In TiDB, creating a secondary index is an online operation, which does not block any data read and write operations on a table. For each index, TiDB creates references for each row in a table and sorts the references by selected columns instead of by data directly.

<CustomContent platform="tidb">

For more information about secondary indexes, see [Secondary Indexes](/best-practices/tidb-best-practices.md#secondary-index).

</CustomContent>

<CustomContent platform="tidb-cloud">

For more information about secondary indexes, see [Secondary Indexes](https://docs.pingcap.com/tidb/stable/tidb-best-practices#secondary-index).

</CustomContent>

In TiDB, you can either [add a secondary index to an existing table](#add-a-secondary-index-to-an-existing-table) or [create a secondary index when creating a new table](#create-a-secondary-index-when-creating-a-new-table).

## Add a secondary index to an existing table

To add a secondary index to an existing table, you can use the [CREATE INDEX](/sql-statements/sql-statement-create-index.md) statement as follows:

```sql
CREATE INDEX {index_name} ON {table_name} ({column_names});
```

Parameter description:

- `{index_name}`: the name of a secondary index.
- `{table_name}`: the table name.
- `{column_names}`: the names of the columns to be indexed, separated by semi-colon commas.

## Create a secondary index when creating a new table

To create a secondary index at the same time as table creation, you can add a clause containing the `KEY` keyword to the end of the [CREATE TABLE](/sql-statements/sql-statement-create-table.md) statement:

```sql
KEY `{index_name}` (`{column_names}`)
```

Parameter description:

- `{index_name}`: the name of a secondary index.
- `{column_names}`: the names of the columns to be indexed, separated by semi-colon commas.

## Rules in secondary index creation

See [Best Practices for Indexing](/develop/dev-guide-index-best-practice.md).

## Example

Suppose you want the `bookshop` application to support **searching for all books published in a given year**.

The fields in the `books` table are as follows:

| Field name   | Type          | Field description                                                          |
|--------------|---------------|------------------------------------------------------------------|
| id           | bigint(20)    | Unique ID of the book                                            |
| title        | varchar(100)  | Book title                                                       |
| type         | enum          | Types of books (for example, magazines, animations, and teaching aids) |
| stock        | bigint(20)    | Stock                                                            |
| price        | decimal(15,2) | Price                                                            |
| published_at | datetime      | Date of publishing                                                  |

The `books` table is created using the following SQL statement:

```sql
CREATE TABLE `bookshop`.`books` (
  `id` bigint(20) AUTO_RANDOM NOT NULL,
  `title` varchar(100) NOT NULL,
  `type` enum('Magazine', 'Novel', 'Life', 'Arts', 'Comics', 'Education & Reference', 'Humanities & Social Sciences', 'Science & Technology', 'Kids', 'Sports') NOT NULL,
  `published_at` datetime NOT NULL,
  `stock` int(11) DEFAULT '0',
  `price` decimal(15,2) DEFAULT '0.0',
  PRIMARY KEY (`id`) CLUSTERED
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
```

To support the searching by year feature, you need to write a SQL statement to **search for all books published in a given year**. Taking 2022 as an example, write a SQL statement as follows:

```sql
SELECT * FROM `bookshop`.`books` WHERE `published_at` >= '2022-01-01 00:00:00' AND `published_at` < '2023-01-01 00:00:00';
```

To check the execution plan of the SQL statement, you can use the [`EXPLAIN`](/sql-statements/sql-statement-explain.md) statement.

```sql
EXPLAIN SELECT * FROM `bookshop`.`books` WHERE `published_at` >= '2022-01-01 00:00:00' AND `published_at` < '2023-01-01 00:00:00';
```

The following is an example output of the execution plan:

```
+-------------------------+----------+-----------+---------------+--------------------------------------------------------------------------------------------------------------------------+
| id                      | estRows  | task      | access object | operator info                                                                                                            |
+-------------------------+----------+-----------+---------------+--------------------------------------------------------------------------------------------------------------------------+
| TableReader_7           | 346.32   | root      |               | data:Selection_6                                                                                                         |
| └─Selection_6           | 346.32   | cop[tikv] |               | ge(bookshop.books.published_at, 2022-01-01 00:00:00.000000), lt(bookshop.books.published_at, 2023-01-01 00:00:00.000000) |
|   └─TableFullScan_5     | 20000.00 | cop[tikv] | table:books   | keep order:false                                                                                                         |
+-------------------------+----------+-----------+---------------+--------------------------------------------------------------------------------------------------------------------------+
3 rows in set (0.61 sec)
```

In the example output, **TableFullScan** is displayed in the `id` column, which means that TiDB is ready to do a full table scan on the `books` table in this query. In the case of a large amount of data, however, a full table scan might be quite slow and cause a fatal impact.

To avoid such impact, you can add an index for the `published_at` column to the `books` table as follows:

```sql
CREATE INDEX `idx_book_published_at` ON `bookshop`.`books` (`bookshop`.`books`.`published_at`);
```

After adding the index, execute the `EXPLAIN` statement again to check the execution plan.

The following is an example output.

```
+-------------------------------+---------+-----------+--------------------------------------------------------+-------------------------------------------------------------------+
| id                            | estRows | task      | access object                                          | operator info                                                     |
+-------------------------------+---------+-----------+--------------------------------------------------------+-------------------------------------------------------------------+
| IndexLookUp_10                | 146.01  | root      |                                                        |                                                                   |
| ├─IndexRangeScan_8(Build)     | 146.01  | cop[tikv] | table:books, index:idx_book_published_at(published_at) | range:[2022-01-01 00:00:00,2023-01-01 00:00:00), keep order:false |
| └─TableRowIDScan_9(Probe)     | 146.01  | cop[tikv] | table:books                                            | keep order:false                                                  |
+-------------------------------+---------+-----------+--------------------------------------------------------+-------------------------------------------------------------------+
3 rows in set (0.18 sec)
```

In the output, **IndexRangeScan** is displayed instead of **TableFullScan**, which means that TiDB is ready to use indexes to do this query.

The words such as **TableFullScan** and **IndexRangeScan** in the execution plan are [operators](/explain-overview.md#operator-overview) in TiDB. For more information about execution plans and operators, see [TiDB Query Execution Plan Overview](/explain-overview.md).

<CustomContent platform="tidb">

The execution plan does not return the same operator every time. This is because TiDB uses a **Cost-Based Optimization (CBO)** approach, in which an execution plan depends on both rules and data distribution. For more information about TiDB SQL performance, see [SQL Tuning Overview](/sql-tuning-overview.md).

</CustomContent>

<CustomContent platform="tidb-cloud">

The execution plan does not return the same operator every time. This is because TiDB uses a **Cost-Based Optimization (CBO)** approach, in which an execution plan depends on both rules and data distribution. For more information about TiDB SQL performance, see [SQL Tuning Overview](/tidb-cloud/tidb-cloud-sql-tuning-overview.md).

</CustomContent>

> **Note:**
>
> TiDB also supports explicit use of indexes when querying, and you can use [Optimizer Hints](/optimizer-hints.md) or [SQL Plan Management (SPM)](/sql-plan-management.md) to artificially control the use of indexes. But if you do not know well about indexes, optimizer hints, or SPM, **DO NOT** use this feature to avoid any unexpected results.

To query the indexes on a table, you can use the [SHOW INDEXES](/sql-statements/sql-statement-show-indexes.md) statement:

```sql
SHOW INDEXES FROM `bookshop`.`books`;
```

The following is an example output:

```
+-------+------------+-----------------------+--------------+--------------+-----------+-------------+----------+--------+------+------------+---------+---------------+---------+------------+-----------+
| Table | Non_unique | Key_name              | Seq_in_index | Column_name  | Collation | Cardinality | Sub_part | Packed | Null | Index_type | Comment | Index_comment | Visible | Expression | Clustered |
+-------+------------+-----------------------+--------------+--------------+-----------+-------------+----------+--------+------+------------+---------+---------------+---------+------------+-----------+
| books |          0 | PRIMARY               |            1 | id           | A         |           0 |     NULL | NULL   |      | BTREE      |         |               | YES     | NULL       | YES       |
| books |          1 | idx_book_published_at |            1 | published_at | A         |           0 |     NULL | NULL   |      | BTREE      |         |               | YES     | NULL       | NO        |
+-------+------------+-----------------------+--------------+--------------+-----------+-------------+----------+--------+------+------------+---------+---------------+---------+------------+-----------+
2 rows in set (1.63 sec)
```

## Next step

After creating a database and adding tables and secondary indexes to it, you can start adding the data [write](/develop/dev-guide-insert-data.md) and [read](/develop/dev-guide-get-data-from-single-table.md) features to your application.
