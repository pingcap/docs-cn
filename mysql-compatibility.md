---
title: Compatibility with MySQL
summary: Learn about the compatibility of TiDB with MySQL, and the unsupported and different features.
aliases: ['/docs/dev/mysql-compatibility/','/docs/dev/reference/mysql-compatibility/']
---

# Compatibility with MySQL

TiDB is fully compatible with the MySQL 5.7 protocol and the common features and syntax of MySQL 5.7. The ecosystem tools for MySQL 5.7 (PHPMyAdmin, Navicat, MySQL Workbench, mysqldump, and Mydumper/myloader) and the MySQL client can be used for TiDB.

However, some features of MySQL are not supported. This could be because there is now a better way to solve the problem (such as XML functions superceded by JSON), or a lack of current demand versus effort required (such as stored procedures and functions). Some features might also be difficult to implement as a distributed system.

> **Note:**
>
> This page refers to general differences between MySQL and TiDB. Refer to the dedicated pages for [Security](/security-compatibility-with-mysql.md) and [Pessimistic Transaction Model](/pessimistic-transaction.md#difference-with-mysql-innodb) compatibility.

## Unsupported features

+ Stored procedures and functions
+ Triggers
+ Events
+ User-defined functions
+ `FOREIGN KEY` constraints [#18209](https://github.com/pingcap/tidb/issues/18209)
+ `FULLTEXT`/`SPATIAL` functions and indexes [#1793](https://github.com/pingcap/tidb/issues/1793)
+ Character sets other than `utf8`, `utf8mb4`, `ascii`, `latin1` and `binary`
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
+ `GET_LOCK` and `RELEASE_LOCK` functions [#14994](https://github.com/pingcap/tidb/issues/14994)

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

TiDB uses a combination of [Prometheus and Grafana](/tidb-monitoring-api.md) to store and query the performance monitoring metrics. Performance schema tables return empty results in TiDB.

### Query Execution Plan

The output format, output content, and the privilege setting of Query Execution Plan (`EXPLAIN`/`EXPLAIN FOR`) in TiDB is greatly different from those in MySQL. See [Understand the Query Execution Plan](/query-execution-plan.md) for more details.

### Built-in functions

TiDB supports most of the MySQL built-in functions, but not all. The statement `SHOW BUILTINS` provides a list of functions that are available.

See also: [TiDB SQL Grammar](https://pingcap.github.io/sqlgram/#functioncallkeyword).

### DDL

In TiDB, all supported DDL changes are performed online. The MySQL DDL assertions `ALGORITHM=INSTANT` and `ALGORITHM=INPLACE` can also be used to assert which algorithm will be used to modify the table (which might differ from MySQL).

The following major restrictions apply to DDL versus MySQL:

* Multiple operations cannot be completed in a single `ALTER TABLE` statement. For example, it is not possible to add multiple columns or indexes in a single statement. Otherwise, the `Unsupported multi schema change` error might be output.
* Different types of indexes (`HASH|BTREE|RTREE|FULLTEXT`) are not supported, and will be parsed and ignored when specified.
* Adding/Dropping the primary key is unsupported unless [`alter-primary-key`](/tidb-configuration-file.md#alter-primary-key) is enabled.
* Change/Modify data type does not currently support "lossy changes", such as changing from BIGINT to INT.
* Change/Modify decimal columns does not support changing the prevision.
* Change/Modify integer columns does not permit changing the `UNSIGNED` attribute.
* Table Partitioning supports Hash, Range, and `Add`/`Drop`/`Truncate`/`Coalesce`. The other partition operations are ignored. The `Warning: Unsupported partition type, treat as normal table` error might be output. The following Table Partition syntaxes are not supported:
    - `PARTITION BY LIST`
    - `PARTITION BY KEY`
    - `SUBPARTITION`
    - `{CHECK|EXCHANGE|TRUNCATE|OPTIMIZE|REPAIR|IMPORT|DISCARD|REBUILD|REORGANIZE} PARTITION`

### Analyze table

[Statistics Collection](/statistics.md#manual-collection) works differently in TiDB than in MySQL, in that it is a relatively lightweight and short-lived operation in MySQL/InnoDB, while in TiDB it completely rebuilds the statistics for a table and can take much longer to complete.

These differences are documented futher in [`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md).

### Views

Views in TiDB are not updatable. They do not support write operations such as `UPDATE`, `INSERT`, and `DELETE`.

### Storage engines

For compatibility reasons, TiDB supports the syntax to create tables with alternative storage engines. In implementation, TiDB describes the metadata as the InnoDB storage engine.

TiDB supports storage engine abstraction similar to MySQL, but you need to specify the storage engine using the [`--store`](/command-line-flags-for-tidb-configuration.md#--store) option when you start the TiDB server.

### SQL modes

TiDB supports most [SQL modes](/sql-mode.md):

- The compatibility modes, such as `ORACLE` and `POSTGRESQL` are parsed but ignored. Compatibility modes are deprecated in MySQL 5.7 and removed in MySQL 8.0.
- The `ONLY_FULL_GROUP_BY` mode has minor [semantic differences](/functions-and-operators/aggregate-group-by-functions.md#differences-from-mysql) from MySQL 5.7.
- The `NO_DIR_IN_CREATE` and `NO_ENGINE_SUBSTITUTION` SQL modes in MySQL are accepted for compatibility, but are not applicable to TiDB.

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

#### Zero month and zero day

By default, the `NO_ZERO_DATE` and `NO_ZERO_IN_DATE` modes are enabled in TiDB, which is the same in MySQL, but TiDB and MySQL handle the two SQL modes differently in the following aspects:

- The two SQL modes above are enabled in TiDB in the non-strict mode where no warning is prompted for inserting values of zero month/zero day/zero date. In MySQL, such `INSERT` operations prompt warning.
- In the strict mode, when `NO_ZERO_DATE` is enabled, you can still insert values of zero date; when `NO_ZERO_IN_DATE` is enabled, you cannot insert date of zero month/zero day. In the strict mode of MySQL, you can insert neither of them.

### Type system differences

The following column types are supported by MySQL, but **NOT** by TiDB:

+ FLOAT4/FLOAT8
+ FIXED (alias for DECIMAL)
+ SERIAL (alias for BIGINT UNSIGNED NOT NULL AUTO_INCREMENT UNIQUE)
+ `SQL_TSI_*` (including SQL_TSI_YEAR, SQL_TSI_MONTH, SQL_TSI_WEEK, SQL_TSI_DAY, SQL_TSI_HOUR, SQL_TSI_MINUTE and SQL_TSI_SECOND)
