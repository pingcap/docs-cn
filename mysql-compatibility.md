---
title: Compatibility with MySQL
summary: Learn about the compatibility of TiDB with MySQL, and the unsupported and different features.
category: reference
aliases: ['/docs/dev/mysql-compatibility/','/docs/dev/reference/mysql-compatibility/']
---

# Compatibility with MySQL

TiDB is fully compatible with the MySQL 5.7 protocol and the common features and syntax of MySQL 5.7. The ecosystem tools for MySQL 5.7 (PHPMyAdmin, Navicat, MySQL Workbench, mysqldump, and Mydumper/myloader) and the MySQL client can be used for TiDB.

However, some features of MySQL have not been implemented in the distributed database TiDB yet, or are only syntactically supported, because these features are difficult to implement or have low ROI (Return On Investment).

> **Note:**
>
> This page refers to general differences between MySQL and TiDB. Refer to the dedicated pages for [Security](/security-compatibility-with-mysql.md) and [Pessimistic Transaction Model](/pessimistic-transaction.md#difference-with-mysql-innodb) compatibility.

## Unsupported features

+ Stored procedures and functions
+ Triggers
+ Events
+ User-defined functions
+ `FOREIGN KEY` constraints
+ `FULLTEXT`/`SPATIAL` functions and indexes
+ Character sets other than `utf8`, `utf8mb4`, `ascii`, `latin1` and `binary`
+ Add/drop primary key
+ SYS schema
+ Optimizer trace
+ XML Functions
+ X-Protocol
+ Savepoints
+ Column-level privileges
+ `XA` syntax (TiDB uses a two-phase commit internally, but this is not exposed via an SQL interface)
+ `CREATE TABLE tblName AS SELECT stmt` syntax
+ `CREATE TEMPORARY TABLE` syntax
+ `CHECK TABLE` syntax
+ `CHECKSUM TABLE` syntax
+ `SELECT INTO FILE` syntax
+ `GET_LOCK` and `RELEASE_LOCK` functions

## Features that are different from MySQL

### Auto-increment ID

+ In TiDB, auto-increment columns are only guaranteed to be incremental and unique but are *not* guaranteed to be allocated sequentially. It is recommended that you do not mix default values and custom values. Otherwise, you might encounter the `Duplicated Error` error message.

+ The implementation principle of the auto-increment ID in TiDB is that each tidb-server instance caches a section of ID values (currently 30,000 IDs are cached) for allocation. The number of cached IDs is determined by `AUTO_ID_CACHE`. Note that both the auto-increment columns and `_tidb_rowid` consume the cached IDs. If the `INSERT` statement requires that the number of consecutive IDs is greater than the `AUTO_ID_CACHE` value, the system automatically adjusts this value so that this statement can be executed.

+ You can use the `tidb_allow_remove_auto_inc` system variable to enable or disable the `AUTO_INCREMENT` column attribute. The syntax of removing the column attribute is `alter table modify` or `alter table change`.

> **Note:**
>
> + To use the `tidb_allow_remove_auto_inc` system variable, your TiDB version must be >= v2.1.18 or >= v3.0.4.
> + The `AUTO_ID_CACHE` table attribute requires that your TiDB version >= v3.0.14 or >= v3.1.2 or >= v4.0.0-rc.2.
> + If you have not specified the primary key when creating a table, TiDB uses `_tidb_rowid` to identify the row. The allocation of this value shares an allocator with the auto-increment column (if such a column exists). If you specify an auto-increment column as the primary key, TiDB uses this column to identify the row. In this situation, the following situation might happen:

```sql
mysql> create table t(id int unique key AUTO_INCREMENT);
Query OK, 0 rows affected (0.05 sec)

mysql> insert into t values(),(),();
Query OK, 3 rows affected (0.00 sec)
Records: 3  Duplicates: 0  Warnings: 0

mysql> select _tidb_rowid, id from t;
+-------------+------+
| _tidb_rowid | id   |
+-------------+------+
|           4 |    1 |
|           5 |    2 |
|           6 |    3 |
+-------------+------+
3 rows in set (0.01 sec)
```

### Performance schema

TiDB uses a combination of [Prometheus and Grafana](/tidb-monitoring-api.md) to store and query the performance monitoring metrics. Some performance schema tables return empty results in TiDB.

### Query Execution Plan

The output format, output content, and the privilege setting of Query Execution Plan (`EXPLAIN`/`EXPLAIN FOR`) in TiDB is greatly different from those in MySQL. See [Understand the Query Execution Plan](/query-execution-plan.md) for more details.

### Built-in functions

TiDB supports most of the MySQL built-in functions, but not all. See [TiDB SQL Grammar](https://pingcap.github.io/sqlgram/#functioncallkeyword) for the supported functions.

### DDL

+ Add Index:
    - Does not support creating multiple indexes using a single SQL statement.
    - Supports creating index of different types (HASH/BTREE/RTREE) only in syntax, not implemented yet.
    - Supports the `VISIBLE`/`INVISIBLE` index and ignores other options.
+ Add Column:
    - Does not support setting the `PRIMARY KEY` and `UNIQUE KEY`. Does not support setting the  `AUTO_INCREMENT` attribute. Otherwise, the `unsupported add column '%s' constraint PRIMARY/UNIQUE/AUTO_INCREMENT KEY` error might be output.
+ Drop Column
    - Does not support dropping the `PRIMARY KEY` column or index column. Otherwise, the `Unsupported drop integer primary key/column a with index covered` error might be output.
+ Drop Primary Key
    - Only supports dropping the primary key of the tables with `alter-primary-key` enabled when the tables are created. Otherwise, the `Unsupported drop primary key when alter-primary-key is false` error might be output.
+ Order By
    - Ignores all options related to column ordering.
+ Change/Modify Column:
    - Does not support lossy changes, such as from `BIGINT` to `INTEGER` or from `VARCHAR(255)` to `VARCHAR(10)`. Otherwise, the `length %d is less than origin %d` error might be output.
    - Does not support modifying the precision of `DECIMAL` data types. Otherwise, the `can't change decimal column precision` error might be output.
    - Does not support changing the `UNSIGNED` attribute. Otherwise, the `can't change unsigned integer to signed or vice versa` error might be output.
    - Only supports changing the `CHARACTER SET` attribute from `utf8` to `utf8mb4`.
+ `LOCK [=] {DEFAULT|NONE|SHARED|EXCLUSIVE}`
    - The syntax is supported, but not implemented in TiDB yet. All DDL changes that are supported do not lock the table.
+ `ALGORITHM [=] {DEFAULT|INSTANT|INPLACE|COPY}`
    - TiDB supports the `ALGORITHM=INSTANT` and `ALGORITHM=INPLACE` syntax, but they work differently from MySQL because some operations that are `INPLACE` in MySQL are `INSTANT` in TiDB.
    - The syntax of `ALGORITHM=COPY` is supported, but not implemented in TiDB yet. It returns a warning.
+ Multiple operations cannot be completed in a single `ALTER TABLE` statement. For example, it is not possible to add multiple columns or indexes in a single statement. Otherwise, the `Unsupported multi schema change` error might be output.

+ The `AUTO_INCREMENT`, `CHARACTER SET`, `COLLATE`, and `COMMENT` Table Options are supported in syntax. The following Table Options are not supported in syntax:
    - `WITH/WITHOUT VALIDATION`
    - `SECONDARY_LOAD/SECONDARY_UNLOAD`
    - `CHECK/DROP CHECK`
    - `STATS_AUTO_RECALC/STATS_SAMPLE_PAGES`
    - `SECONDARY_ENGINE`
    - `ENCRYPTION`

+ The Table Partition supports Hash, Range, and `Add`/`Drop`/`Truncate`/`Coalesce`. The other partition operations are ignored. The `Warning: Unsupported partition type, treat as normal table` error might be output. The following Table Partition syntaxes are not supported:
    - `PARTITION BY LIST`
    - `PARTITION BY KEY`
    - `SUBPARTITION`
    - `{CHECK|EXCHANGE|TRUNCATE|OPTIMIZE|REPAIR|IMPORT|DISCARD|REBUILD|REORGANIZE} PARTITION`

### Analyze table

[`ANALYZE TABLE`](/statistics.md#manual-collection) works differently in TiDB than in MySQL, in that it is a relatively lightweight and short-lived operation in MySQL/InnoDB, while in TiDB it completely rebuilds the statistics for a table and can take much longer to complete.

### Views

For the views feature, TiDB does not support write operations like `UPDATE`, `INSERT`, and `DELETE`.

### Storage engines

For compatibility reasons, TiDB supports the syntax to create tables with alternative storage engines. In implementation, TiDB describes the metadata as the InnoDB storage engine.

TiDB supports storage engine abstraction similar to MySQL, but you need to specify the storage engine using the [`--store`](/command-line-flags-for-tidb-configuration.md#--store) option when you start the TiDB server.

### SQL modes

- Does not support the compatibility mode, such as `ORACLE` and `POSTGRESQL`. The compatibility mode is deprecated in MySQL 5.7 and removed in MySQL 8.0.
- The `ONLY_FULL_GROUP_BY` mode has minor [semantic differences](/functions-and-operators/aggregate-group-by-functions.md#differences-from-mysql) from MySQL 5.7.
- The `NO_DIR_IN_CREATE` and `NO_ENGINE_SUBSTITUTION` SQL modes in MySQL are supported for compatibility, but are not applicable to TiDB.

### Default differences

- Default character set:
    - The default value in TiDB is `utf8mb4`.
    - The default value in MySQL 5.7 is `latin1`.
    - The default value in MySQL 8.0 is `utf8mb4`.
- Default collation:
    - The default collation of `utf8mb4` in TiDB is `utf8mb4_bin`.
    - The default collation of `utf8mb4` in MySQL 5.7 is `utf8mb4_general_ci`.
    - The default collation of `utf8mb4` in MySQL 8.0 is `utf8mb4_0900_ai_ci`.
- Default value of `foreign_key_checks`:
    - The default value in TiDB is `OFF` and currently TiDB only supports `OFF`.
    - The default value in MySQL 5.7 is `ON`.
- Default SQL mode:
    - The default SQL mode in TiDB includes these modes: `ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION`.
    - The default SQL mode in MySQL:
        - The default SQL mode in MySQL 5.7 is the same as TiDB.
        - The default SQL mode in MySQL 8.0 includes these modes: `ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION`.
- Default value of `lower_case_table_names`:
    - The default value in TiDB is `2` and currently TiDB only supports `2`.
    - The default value in MySQL:
        - On Linux: `0`
        - On Windows: `1`
        - On macOS: `2`
- Default value of `explicit_defaults_for_timestamp`:
    - The default value in TiDB is `ON` and currently TiDB only supports `ON`.
    - The default value in MySQL:
        - For MySQL 5.7: `OFF`.
        - For MySQL 8.0: `ON`.

### Date and Time

#### Named timezone

+ TiDB uses all time zone rules currently installed in the system for calculation (usually the `tzdata` package). You can use all time zone names without importing the time zone table data. You cannot modify the calculation rules by importing the time zone table data.
+ MySQL uses the local time zone by default and relies on the current time zone rules built into the system (such as when to start daylight saving time) for calculation; and the time zone cannot be specified by the time zone name without [importing the time zone table data](https://dev.mysql.com/doc/refman/5.7/en/time-zone-support.html#time-zone-installation).

> **Note:**
>
> TiKV calculates time-related expressions that can be pushed down to it. This calculation uses the built-in time zone rule and does not depend on the time zone rule installed in the system. If the time zone rule installed in the system does not match the version of the built-in time zone rule in TiKV, the time data that can be inserted might result in a statement error in a few cases.
>
> For example, if the tzdata 2018a timezone rule is installed in the system, the time `1988-04-17 02:00:00` can be inserted into TiDB of the 3.0 RC.1 version when the timezone is set to Asia/Shanghai or the timezone is set to the local timezone and the local timezone is Asia/Shanghai. But reading this record might result in a statement error because this time does not exist in the Asia/Shanghai timezone according to the tzdata 2018i timezone rule used by TiKV 3.0 RC.1. Daylight saving time is one hour late.
>
> The named timezone rules in TiKV of two versions are as follows:
>
> - 3.0.0 RC.1 and later: [tzdata 2018i](https://github.com/eggert/tz/tree/2018i)
> - 2.1.0 RC.1 and later: [tzdata 2018e](https://github.com/eggert/tz/tree/2018e)

#### Zero month and zero day

It is not recommended to unset the `NO_ZERO_DATE` and `NO_ZERO_IN_DATE` SQL modes, which are enabled by default in TiDB as in MySQL. Although TiDB supports operating with these modes disabled, the TiKV coprocessor might be affected. Executing certain statements that push down date and time processing functions to TiKV might result in a statement error.

### Type system differences

The following column types are supported by MySQL, but **NOT** by TiDB:

+ FLOAT4/FLOAT8
+ FIXED (alias for DECIMAL)
+ SERIAL (alias for BIGINT UNSIGNED NOT NULL AUTO_INCREMENT UNIQUE)
+ `SQL_TSI_*` (including SQL_TSI_YEAR, SQL_TSI_MONTH, SQL_TSI_WEEK, SQL_TSI_DAY, SQL_TSI_HOUR, SQL_TSI_MINUTE and SQL_TSI_SECOND)
