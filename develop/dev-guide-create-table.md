---
title: Create a Table
summary: Learn the definitions, rules, and guidelines in table creation.
---

# Create a Table

This document introduces how to create tables using the SQL statement and the related best practices. An example of the TiDB-based [Bookshop](/develop/dev-guide-bookshop-schema-design.md) application) is provided to illustrate the best practices.

## Before you start

Before reading this document, make sure that the following tasks are completed:

- [Build a TiDB Cluster in TiDB Cloud (Serverless Tier)](/develop/dev-guide-build-cluster-in-cloud.md).
- Read [Schema Design Overview](/develop/dev-guide-schema-design-overview.md).
- [Create a Database](/develop/dev-guide-create-database.md).

## What is a table

A [table](/develop/dev-guide-schema-design-overview.md#table) is a logical object in TiDB cluster that is subordinate to the [database](/develop/dev-guide-schema-design-overview.md#database). It is used to store the data sent from SQL statements. Tables save data records in the form of rows and columns. A table has at least one column. If you have defined `n` columns, each row of data has exactly the same fields as the `n` columns.

## Name a table

The first step for creating a table is to give your table a name. Do not use meaningless names that will cause great distress to yourself or your colleagues in the future. It is recommended that you follow your company or organization's table naming convention.

The `CREATE TABLE` statement usually takes the following form:

```sql
CREATE TABLE {table_name} ( {elements} );
```

**Parameter description**

- `{table_name}`: The name of the table to be created.
- `{elements}`: A comma-separated list of table elements, such as column definitions and primary key definitions.

Suppose you need to create a table to store the user information in the `bookshop` database.

Note that you cannot execute the following SQL statement yet because not a single column has been added.

```sql
CREATE TABLE `bookshop`.`users` (
);
```

## Define columns

A **column** is subordinate to a table. Each table has at least one column. Columns provide a structure to a table by dividing the values in each row into small cells of a single data type.

Column definitions typically take the following form.

```
{column_name} {data_type} {column_qualification}
```

**Parameter description**

- `{column_name}`: The column name.
- `{data_type}`: The column [data type](/data-type-overview.md).
- `{column_qualification}`: Column qualifications, such as **column-level constraints** or [generated column (experimental feature)](/generated-columns.md) clauses.

You can add some columns to the `users` table, such as the unique identifier `id`, `balance` and `nickname`.

```sql
CREATE TABLE `bookshop`.`users` (
  `id` bigint,
  `nickname` varchar(100),
  `balance` decimal(15,2)
);
```

In the above statement, a field is defined with the name `id` and the type [bigint](/data-type-numeric.md#bigint-type). This is used to represent a unique user identifier. This means that all user identifiers should be of the `bigint` type.

Then, a field named `nickname` is defined, which is the [varchar](/data-type-string.md#varchar-type) type, with a length limit of 100 characters. This means that the `nicknames` of the users use the `varchar` type and are not longer than 100 characters.

Finally, a field named `balance` is added, which is the [decimal](/data-type-numeric.md#decimal-type) type, with a **precision** of `15` and a **scale** of `2`. **Precision** represents the total number of digits in the field, and **scale** represents the number of decimal places. For example, `decimal(5,2)` means a precision of `5` and a scale of `2`, with the range from `-999.99` to `999.99`. `decimal(6,1)` means a precision of `6` and a scale of `1`, with the range from `-99999.9` to `99999.9`. **decimal** is a [fixed-point types](/data-type-numeric.md#fixed-point-types), which can be used to store numbers accurately. In scenarios where accurate numbers are needed (for example, user property-related), make sure that you use the **decimal** type.

TiDB supports many other column data types, including the [integer types](/data-type-numeric.md#integer-types), [floating-point types](/data-type-numeric.md#floating-point-types), [fixed-point types](/data-type-numeric.md#fixed-point-types), [date and time types](/data-type-date-and-time.md), and the [enum type](/data-type-string.md#enum-type). You can refer to the supported column [data types](/data-type-overview.md) and use the **data types** that match the data you want to save in the database.

To make it a bit more complex, you can define a `books` table which will be the core of the `bookshop` data. The `books` table contains fields for the book's ids, titles, types (for example, magazine, novel, life, arts), stock, prices, and publication dates.

```sql
CREATE TABLE `bookshop`.`books` (
  `id` bigint NOT NULL,
  `title` varchar(100),
  `type` enum('Magazine', 'Novel', 'Life', 'Arts', 'Comics', 'Education & Reference', 'Humanities & Social Sciences', 'Science & Technology', 'Kids', 'Sports'),
  `published_at` datetime,
  `stock` int,
  `price` decimal(15,2)
);
```

This table contains more data types than the `users` table.

- [int](/data-type-numeric.md#integer-types): It is recommended to use the type of right size to avoid using too much disk or even affecting performance (too large a type range) or data overflow (too small a data type range).
- [datetime](/data-type-date-and-time.md): The **datetime** type can be used to store time values.
- [enum](/data-type-string.md#enum-type): The enum type can be used to store a limited selection of values.

## Select primary key

A [primary key](/constraints.md#primary-key) is a column or a set of columns in a table whose values uniquely identify a row in the table.

> **Note:**
>
> The default definition of **primary key** in TiDB is different from that in [InnoDB](https://mariadb.com/kb/en/innodb/)(the common storage engine of MySQL). 
>
> - In **InnoDB**: A **primary key** is unique, not null, and **index clustered**.
>
> - In TiDB: A **primary key** is unique and is not null. But the primary key is not guaranteed to be a **clustered index**. Instead, another set of keywords `CLUSTERED` / `NONCLUSTERED` additionally controls whether the **primary key** is a **clustered index**. If the keyword is not specified, it is controlled by the system variable `@@global.tidb_enable_clustered_index`, as described in [clustered indexes](https://docs.pingcap.com/zh/tidb/stable/clustered-indexes).

The **primary key** is defined in the `CREATE TABLE` statement. The [primary key constraint](/constraints.md#primary-key) requires that all constrained columns contain only non-NULL values.

A table can be created without a **primary key** or with a non-integer **primary key**. In this case, TiDB creates a `_tidb_rowid` as an **implicit primary key**. The implicit primary key `_tidb_rowid`, because of its monotonically increasing nature, might cause write hotspots in write-intensive scenarios. Therefore, if your application is write-intensive, consider sharding data using the [`SHARD_ROW_ID_BITS`](/shard-row-id-bits.md) and [`PRE_SPLIT_REGIONS`](/sql-statements/sql-statement-split-region.md#pre_split_regions) parameters. However, this might lead to read amplification, so you need to make your own trade-off.

When the **primary key** of a table is an [integer type](/data-type-numeric.md#integer-types) and `AUTO_INCREMENT` is used, hotspots cannot be avoided by using `SHARD_ROW_ID_BITS`. If you need to avoid hotspots and do not need a continuous and incremental primary key, you can use [`AUTO_RANDOM`](/auto-random.md) instead of `AUTO_INCREMENT` to eliminate row ID continuity.

<CustomContent platform="tidb">

For more information on how to handle hotspot issues, refer to [Troubleshoot Hotspot Issues](/troubleshoot-hot-spot-issues.md).

</CustomContent>

Following the [guidelines for selecting primary key](#guidelines-to-follow-when-selecting-primary-key), the following example shows how an `AUTO_RANDOM` primary key is defined in the `users` table.

```sql
CREATE TABLE `bookshop`.`users` (
  `id` bigint AUTO_RANDOM,
  `balance` decimal(15,2),
  `nickname` varchar(100),
  PRIMARY KEY (`id`)
);
```

## Clustered or not

TiDB supports the [clustered index](/clustered-indexes.md) feature since v5.0. This feature controls how data is stored in tables containing primary keys. It provides TiDB the ability to organize tables in a way that can improve the performance of certain queries.

The term clustered in this context refers to the organization of how data is stored and not a group of database servers working together. Some database management systems refer to clustered indexes as index-organized tables (IOT).

Currently, tables **_containing primary_** keys in TiDB are divided into the following two categories:

- `NONCLUSTERED`: The primary key of the table is non-clustered index. In tables with non-clustered indexes, the keys for row data consist of internal `_tidb_rowid` implicitly assigned by TiDB. Because primary keys are essentially unique indexes, tables with non-clustered indexes need at least two key-value pairs to store a row, which are:
    - `_tidb_rowid` (key) - row data (value)
    - Primary key data (key) - `_tidb_rowid` (value)
- `CLUSTERED`: The primary key of the table is clustered index. In tables with clustered indexes, the keys for row data consist of primary key data given by the user. Therefore, tables with clustered indexes need only one key-value pair to store a row, which is:
    - Primary key data (key) - row data (value)

As described in [select primary key](#select-primary-key), **clustered indexes** are controlled in TiDB using the keywords `CLUSTERED` and `NONCLUSTERED`.

> **Note:**
>
> TiDB supports clustering only by a table's `PRIMARY KEY`. With clustered indexes enabled, the terms _the_ `PRIMARY KEY` and _the clustered index_ might be used interchangeably. `PRIMARY KEY` refers to the constraint (a logical property), and clustered index describes the physical implementation of how the data is stored.

Following the [guidelines for selecting clustered index](#guidelines-to-follow-when-selecting-clustered-index), the following example creates a table with an association between `books` and `users`, which represents the `ratings` of a `book` by `users`. The example creates the table and constructs a composite primary key using `book_id` and `user_id`, and creates a **clustered index** on that **primary key**.

```sql
CREATE TABLE `bookshop`.`ratings` (
  `book_id` bigint,
  `user_id` bigint,
  `score` tinyint,
  `rated_at` datetime,
  PRIMARY KEY (`book_id`,`user_id`) CLUSTERED
);
```

## Add column constraints

In addition to [primary key constraints](#select-primary-key), TiDB also supports other **column constraints** such as [NOT NULL](/constraints.md#not-null) constraint, [UNIQUE KEY](/constraints.md#unique-key) constraint, and `DEFAULT`. For complete constraints, refer to the [TiDB constraints](/constraints.md) document.

### Set default value

To set a default value on a column, use the `DEFAULT` constraint. The default value allows you to insert data without specifying a value for each column.

You can use `DEFAULT` together with [supported SQL functions](/functions-and-operators/functions-and-operators-overview.md) to move the calculation of defaults out of the application layer, thus saving resources of the application layer. The resources consumed by the calculation do not disappear and are moved to the TiDB cluster. Commonly, you can insert data with the default time. The following exemplifies setting the default value in the `ratings` table:

```sql
CREATE TABLE `bookshop`.`ratings` (
  `book_id` bigint,
  `user_id` bigint,
  `score` tinyint,
  `rated_at` datetime DEFAULT NOW(),
  PRIMARY KEY (`book_id`,`user_id`) CLUSTERED
);
```

In addition, if the current time is also filled in by default when the data is being updated, the following statements can be used (but only the [current time related statements](https://pingcap.github.io/sqlgram/#NowSymOptionFraction) can be filled in after `ON UPDATE`, and [more options](https://pingcap.github.io/sqlgram/#DefaultValueExpr) are supported after `DEFAULT`):

```sql
CREATE TABLE `bookshop`.`ratings` (
  `book_id` bigint,
  `user_id` bigint,
  `score` tinyint,
  `rated_at` datetime DEFAULT NOW() ON UPDATE NOW(),
  PRIMARY KEY (`book_id`,`user_id`) CLUSTERED
);
```

### Prevent duplicate values

If you need to prevent duplicate values in a column, you can use the `UNIQUE` constraint.

For example, to make sure that users' nicknames are unique, you can rewrite the table creation SQL statement for the `users` table like this:

```sql
CREATE TABLE `bookshop`.`users` (
  `id` bigint AUTO_RANDOM,
  `balance` decimal(15,2),
  `nickname` varchar(100) UNIQUE,
  PRIMARY KEY (`id`)
);
```

If you try to insert the same `nickname` in the `users` table, an error is returned.

### Prevent null values

If you need to prevent null values in a column, you can use the `NOT NULL` constraint.

Take user nicknames as an example. To ensure that a nickname is not only unique but is also not null, you can rewrite the SQL statement for creating the `users` table as follows:

```sql
CREATE TABLE `bookshop`.`users` (
  `id` bigint AUTO_RANDOM,
  `balance` decimal(15,2),
  `nickname` varchar(100) UNIQUE NOT NULL,
  PRIMARY KEY (`id`)
);
```

## Use HTAP capabilities

<CustomContent platform="tidb">

> **Note:**
>
> The steps provided in this guide is **_ONLY_** for quick start in the test environment. For production environments, refer to [explore HTAP](/explore-htap.md).

</CustomContent>

<CustomContent platform="tidb-cloud">

> **Note:**
>
> The steps provided in this guide is **_ONLY_** for quick start. For more instructions, refer to [Use an HTAP Cluster with TiFlash](/tiflash/tiflash-overview.md).

</CustomContent>

Suppose that you want to perform OLAP analysis on the `ratings` table using the `bookshop` application, for example, to query **whether the rating of a book has a significant correlation with the time of the rating**, which is to analyze whether the user's rating of the book is objective or not. Then you need to query the `score` and `rated_at` fields of the entire `ratings` table. This operation is resource-intensive for an OLTP-only database. Or you can use some ETL or other data synchronization tools to export the data from the OLTP database to a dedicated OLAP database for analysis.

In this scenario, TiDB, an **HTAP (Hybrid Transactional and Analytical Processing)** database that supports both OLTP and OLAP scenarios, is an ideal one-stop database solution.

### Replicate column-based data

<CustomContent platform="tidb">

Currently, TiDB supports two data analysis engines, **TiFlash** and **TiSpark**. For the large data scenarios (100 T), **TiFlash MPP** is recommended as the primary solution for HTAP, and **TiSpark** as a complementary solution.

To learn more about TiDB HTAP capabilities, refer to the following documents: [Quick Start Guide for TiDB HTAP](/quick-start-with-htap.md) and [Explore HTAP](/explore-htap.md).

</CustomContent>

<CustomContent platform="tidb-cloud">

To learn more about TiDB HTAP capabilities, see [TiDB Cloud HTAP Quick Start](/tidb-cloud/tidb-cloud-htap-quickstart.md) and [Use an HTAP Cluster with TiFlash](/tiflash/tiflash-overview.md).

</CustomContent>

In this example, [TiFlash](https://docs.pingcap.com/tidb/stable/tiflash-overview) has been chosen as the data analysis engine for the `bookshop` database.

TiFlash does not automatically replicate data after deployment. Therefore, you need to manually specify the tables to be replicated:

```sql
ALTER TABLE {table_name} SET TIFLASH REPLICA {count};
```

**Parameter description**

- `{table_name}`: The table name.
- `{count}`: The number of replicated replicas. If it is 0, replicated replicas are deleted.

**TiFlash** will then replicate the table. When a query is performed, TiDB automatically selects TiKV (row-based) or TiFlash (column-based) for the query based on cost optimization. Alternatively, you can manually specify whether the query uses a **TiFlash** replica. To learn how to specify it, refer to [Use TiDB to read TiFlash replicas](/tiflash/use-tidb-to-read-tiflash.md).

### An example of using HTAP capabilities

The `ratings` table opens `1` replica of TiFlash:

```sql
ALTER TABLE `bookshop`.`ratings` SET TIFLASH REPLICA 1;
```

> **Note:**
>
> If your cluster does not contain **TiFlash** nodes, this SQL statement will report an error: `1105 - the tiflash replica count: 1 should be less than the total tiflash server count: 0`. You can use [Build a TiDB Cluster in TiDB Cloud (Serverless Tier)](/develop/dev-guide-build-cluster-in-cloud.md#step-1-create-a-serverless-tier-cluster) to create a Serverless Tier cluster that includes **TiFlash**.

Then you can go on to perform the following query:

```sql
SELECT HOUR(`rated_at`), AVG(`score`) FROM `bookshop`.`ratings` GROUP BY HOUR(`rated_at`);
```

You can also execute the [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md) statement to see whether this statement is using the **TiFlash**:

```sql
EXPLAIN ANALYZE SELECT HOUR(`rated_at`), AVG(`score`) FROM `bookshop`.`ratings` GROUP BY HOUR(`rated_at`);
```

Running results:

```sql
+-----------------------------+-----------+---------+--------------+---------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------+----------+------+
| id                          | estRows   | actRows | task         | access object | execution info                                                                                                                                                                                                                                                                                                                                                       | operator info                                                                                                                                  | memory   | disk |
+-----------------------------+-----------+---------+--------------+---------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------+----------+------+
| Projection_4                | 299821.99 | 24      | root         |               | time:60.8ms, loops:6, Concurrency:5                                                                                                                                                                                                                                                                                                                                  | hour(cast(bookshop.ratings.rated_at, time))->Column#6, Column#5                                                                                | 17.7 KB  | N/A  |
| └─HashAgg_5                 | 299821.99 | 24      | root         |               | time:60.7ms, loops:6, partial_worker:{wall_time:60.660079ms, concurrency:5, task_num:293, tot_wait:262.536669ms, tot_exec:40.171833ms, tot_time:302.827753ms, max:60.636886ms, p95:60.636886ms}, final_worker:{wall_time:60.701437ms, concurrency:5, task_num:25, tot_wait:303.114278ms, tot_exec:176.564µs, tot_time:303.297475ms, max:60.69326ms, p95:60.69326ms}  | group by:Column#10, funcs:avg(Column#8)->Column#5, funcs:firstrow(Column#9)->bookshop.ratings.rated_at                                         | 714.0 KB | N/A  |
|   └─Projection_15           | 300000.00 | 300000  | root         |               | time:58.5ms, loops:294, Concurrency:5                                                                                                                                                                                                                                                                                                                                | cast(bookshop.ratings.score, decimal(8,4) BINARY)->Column#8, bookshop.ratings.rated_at, hour(cast(bookshop.ratings.rated_at, time))->Column#10 | 366.2 KB | N/A  |
|     └─TableReader_10        | 300000.00 | 300000  | root         |               | time:43.5ms, loops:294, cop_task: {num: 1, max: 43.1ms, proc_keys: 0, rpc_num: 1, rpc_time: 43ms, copr_cache_hit_ratio: 0.00}                                                                                                                                                                                                                                        | data:TableFullScan_9                                                                                                                           | 4.58 MB  | N/A  |
|       └─TableFullScan_9     | 300000.00 | 300000  | cop[tiflash] | table:ratings | tiflash_task:{time:5.98ms, loops:8, threads:1}, tiflash_scan:{dtfile:{total_scanned_packs:45, total_skipped_packs:1, total_scanned_rows:368640, total_skipped_rows:8192, total_rs_index_load_time: 1ms, total_read_time: 1ms},total_create_snapshot_time:1ms}                                                                                                        | keep order:false                                                                                                                               | N/A      | N/A  |
+-----------------------------+-----------+---------+--------------+---------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------+----------+------+
```

When the field `cop[tiflash]` appears, it means that the task is sent to **TiFlash** for processing.

## Execute the `CREATE TABLE` statement

After creating all the tables as above rules, our [database initialization](/develop/dev-guide-bookshop-schema-design.md#database-initialization-script-dbinitsql) script should look like this. If you need to see the table information in detail, please refer to [Description of the Tables](/develop/dev-guide-bookshop-schema-design.md#description-of-the-tables).

To name the database initialization script `init.sql` and save it, you can execute the following statement to initialize the database.

```shell
mysql
    -u root \
    -h {host} \
    -P {port} \
    -p {password} \
    < init.sql
```

To view all tables under the `bookshop` database, use the [`SHOW TABLES`](/sql-statements/sql-statement-show-tables.md#show-full-tables) statement.

```sql
SHOW TABLES IN `bookshop`;
```

Running results:

```
+--------------------+
| Tables_in_bookshop |
+--------------------+
| authors            |
| book_authors       |
| books              |
| orders             |
| ratings            |
| users              |
+--------------------+
```

## Guidelines to follow when creating a table

This section provides guidelines you need to follow when creating a table.

### Guidelines to follow when naming a table

- Use a **fully-qualified** table name (for example, `CREATE TABLE {database_name}. {table_name}`). If you do not specify the database name, TiDB uses the current database in your **SQL session**. If you do not use `USE {databasename};` to specify the database in your SQL session, TiDB returns an error.
- Use meaningful table names. For example, if you need to create a user table, you can use names: `user`, `t_user`,`users`, or follow your company or organization's naming convention. If your company or organization does not have a naming convention, you can refer to the [table naming convention](/develop/dev-guide-object-naming-guidelines.md#table-naming-convention). Do not use such table names as: `t1`, `table1`.
- Multiple words are separated by an underscore, and it is recommended that the name is no more than 32 characters.
- Create a separate `DATABASE` for tables of different business modules and add comments accordingly.

### Guidelines to follow when defining columns

- Check the [data types](/data-type-overview.md) supported by columns and organize your data according to the data type restrictions. Select the appropriate type for the data you plan to store in the column.
- Check the [guidelines to follow](#guidelines-to-follow-when-selecting-primary-key) for selecting primary keys and decide whether to use primary key columns.
- Check the [guidelines to follow](#guidelines-to-follow-when-selecting-clustered-index) for selecting clustered indexes and decide whether to specify **clustered indexes**.
- Check [adding column constraints](#add-column-constraints) and decide whether to add constraints to the columns.
- Use meaningful column names. It is recommended that you follow your company or organization's table naming convention. If your company or organization does not have a corresponding naming convention, refer to the [column naming convention](/develop/dev-guide-object-naming-guidelines.md#column-naming-convention).

### Guidelines to follow when selecting primary key

- Define a **primary key** or **unique index** within the table.
- Try to select meaningful **columns** as **primary keys**.
- For performance reasons, try to avoid storing extra-wide tables. It is not recommended that the number of table fields is over `60` and that the total data size of a single row is over `64K`. It is recommended to split fields with too much data length to another table.
- It is not recommended to use complex data types.
- For the fields to be joined, ensure that the data types are consistent and avoid implicit conversion.
- Avoid defining **primary keys** on a single monotonic data column. If you use a single monotonic data column (for example, a column with the `AUTO_INCREMENT` attribute) to define the **primary key**, it might impact the write performance. If possible, use `AUTO_RANDOM` instead of `AUTO_INCREMENT`, which discards the continuous and incremental attribute of the primary key.
- If you really need to create an index on a single monotonic data column at write-intensive scenarios, instead of defining this monotonic data column as the **primary key**, you can use `AUTO_RANDOM` to create the **primary key** for that table, or use [`SHARD_ROW_ID_BITS`](/shard-row-id-bits.md) and [`PRE_SPLIT_REGIONS`](/sql-statements/sql-statement-split-region.md#pre_split_regions) to shard `_tidb_rowid`.

### Guidelines to follow when selecting clustered index

- Follow [guidelines for selecting primary key](#guidelines-to-follow-when-selecting-primary-key) to build **clustered indexes**.
- Compared to tables with non-clustered indexes, tables with clustered indexes offer greater performance and throughput advantages in the following scenarios:
    - When data is inserted, the clustered index reduces one write of the index data from the network.
    - When a query with an equivalent condition only involves the primary key, the clustered index reduces one read of index data from the network.
    - When a query with a range condition only involves the primary key, the clustered index reduces multiple reads of index data from the network.
    - When a query with an equivalent or range condition only involves the primary key prefix, the clustered index reduces multiple reads of index data from the network.
- On the other hand, tables with clustered indexes might have the following issues:
    - There might be write hotspot issues when you insert a large number of primary keys with close values. Follow the [guidelines to follow when selecting primary key](#guidelines-to-follow-when-selecting-primary-key).
    - The table data takes up more storage space if the data type of the primary key is larger than 64 bits, especially when there are multiple secondary indexes.

- To control the [default behavior of whether to use clustered indexes](/clustered-indexes.md#create-a-table-with-clustered-indexes), you can explicitly specify whether to use clustered indexes instead of using the system variable `@@global.tidb_enable_clustered_index` and the configuration `alter-primary-key`.

### Guidelines to follow when executing the `CREATE TABLE` statement

- It is not recommended to use a client-side Driver or ORM to perform database schema changes. It is recommended to use a [MySQL client](https://dev.mysql.com/doc/refman/8.0/en/mysql.html) or use a GUI client to perform database schema changes. In this document, the **MySQL client** is used to pass in SQL files to perform database schema changes in most scenarios.
- Follow the SQL development [specification for creating and deleting tables](/develop/dev-guide-sql-development-specification.md#create-and-delete-tables). It is recommended to wrap the build and delete statements inside the business application to add judgment logic.

## One more step

Note that all the tables that have been created in this document do not contain secondary indexes. For a guide to add secondary indexes, refer to [Creating Secondary Indexes](/develop/dev-guide-create-secondary-indexes.md).
