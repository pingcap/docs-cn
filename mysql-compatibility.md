---
title: MySQL Compatibility
summary: Learn about the compatibility of TiDB with MySQL, and the unsupported and different features.
aliases: ['/docs/dev/mysql-compatibility/','/docs/dev/reference/mysql-compatibility/']
---

# MySQL Compatibility

<CustomContent platform="tidb">

TiDB is highly compatible with the MySQL protocol and the common features and syntax of MySQL 5.7 and MySQL 8.0. The ecosystem tools for MySQL (PHPMyAdmin, Navicat, MySQL Workbench, DBeaver and [more](/develop/dev-guide-third-party-support.md#gui)) and the MySQL client can be used for TiDB.

</CustomContent>

<CustomContent platform="tidb-cloud">

TiDB is highly compatible with the MySQL protocol and the common features and syntax of MySQL 5.7 and MySQL 8.0. The ecosystem tools for MySQL (PHPMyAdmin, Navicat, MySQL Workbench, DBeaver and [more](https://docs.pingcap.com/tidb/v7.2/dev-guide-third-party-support#gui)) and the MySQL client can be used for TiDB.

</CustomContent>

However, some features of MySQL are not supported in TiDB. This could be because there is now a better way to solve the problem (such as the use of JSON instead of XML functions) or a lack of current demand versus effort required (such as stored procedures and functions). Additionally, some features might be difficult to implement in a distributed system.

<CustomContent platform="tidb">

It's important to note that TiDB does not support the MySQL replication protocol. Instead, specific tools are provided to replicate data with MySQL:

- Replicate data from MySQL: [TiDB Data Migration (DM)](/dm/dm-overview.md) is a tool that supports full data migration and incremental data replication from MySQL or MariaDB into TiDB.
- Replicate data to MySQL: [TiCDC](/ticdc/ticdc-overview.md) is a tool for replicating the incremental data of TiDB by pulling TiKV change logs. TiCDC uses the [MySQL sink](/ticdc/ticdc-overview.md#replication-consistency) to replicate the incremental data of TiDB to MySQL.

</CustomContent>

<CustomContent platform="tidb">

> **Note:**
>
> This page describes general differences between MySQL and TiDB. For more information on compatibility with MySQL in the areas of security and pessimistic transaction mode, refer to the dedicated pages on [Security](/security-compatibility-with-mysql.md) and [Pessimistic Transaction Mode](/pessimistic-transaction.md#difference-with-mysql-innodb).

</CustomContent>

<CustomContent platform="tidb-cloud">

> **Note:**
>
> For information about transaction differences between MySQL and TiDB, see [Pessimistic Transaction Mode](/pessimistic-transaction.md#difference-with-mysql-innodb).

</CustomContent>

You can try out TiDB features on [TiDB Playground](https://play.tidbcloud.com/?utm_source=docs&utm_medium=mysql_compatibility).

## Unsupported features

+ Stored procedures and functions
+ Triggers
+ Events
+ User-defined functions
+ `FULLTEXT` syntax and indexes [#1793](https://github.com/pingcap/tidb/issues/1793)
+ `SPATIAL` (also known as `GIS`/`GEOMETRY`) functions, data types and indexes [#6347](https://github.com/pingcap/tidb/issues/6347)
+ Character sets other than `ascii`, `latin1`, `binary`, `utf8`, `utf8mb4`, and `gbk`.
+ SYS schema
+ Optimizer trace
+ XML Functions
+ X-Protocol [#1109](https://github.com/pingcap/tidb/issues/1109)
+ Column-level privileges [#9766](https://github.com/pingcap/tidb/issues/9766)
+ `XA` syntax (TiDB uses a two-phase commit internally, but this is not exposed via an SQL interface)
+ `CREATE TABLE tblName AS SELECT stmt` syntax [#4754](https://github.com/pingcap/tidb/issues/4754)
+ `CHECK TABLE` syntax [#4673](https://github.com/pingcap/tidb/issues/4673)
+ `CHECKSUM TABLE` syntax [#1895](https://github.com/pingcap/tidb/issues/1895)
+ `REPAIR TABLE` syntax
+ `OPTIMIZE TABLE` syntax
+ `HANDLER` statement
+ `CREATE TABLESPACE` statement
+ "Session Tracker: Add GTIDs context to the OK packet"
+ Descending Index [#2519](https://github.com/pingcap/tidb/issues/2519)
+ `SKIP LOCKED` syntax [#18207](https://github.com/pingcap/tidb/issues/18207)
+ Lateral derived tables [#40328](https://github.com/pingcap/tidb/issues/40328)

## Differences from MySQL

### Auto-increment ID

+ In TiDB, the auto-incremental column values (IDs) are globally unique and incremental within a single TiDB server. To make the IDs incremental among multiple TiDB servers, you can use the [`AUTO_INCREMENT` MySQL compatibility mode](/auto-increment.md#mysql-compatibility-mode). However, the IDs are not necessarily allocated sequentially, so it is recommended that you avoid mixing default and custom values to prevent encountering the `Duplicated Error` message.

+ You can use the `tidb_allow_remove_auto_inc` system variable to allow or forbid removing the `AUTO_INCREMENT` column attribute. To remove the column attribute, use the `ALTER TABLE MODIFY` or `ALTER TABLE CHANGE` syntax.

+ TiDB does not support adding the `AUTO_INCREMENT` column attribute, and once removed, it cannot be recovered.

+ For TiDB v6.6.0 and earlier versions, auto-increment columns in TiDB behave the same as in MySQL InnoDB, requiring them to be primary keys or index prefixes. Starting from v7.0.0, TiDB removes this restriction, allowing for more flexible table primary key definitions. [#40580](https://github.com/pingcap/tidb/issues/40580)

For more details, see [`AUTO_INCREMENT`](/auto-increment.md).

> **Note:**
>
> + If you do not specify a primary key when creating a table, TiDB uses `_tidb_rowid` to identify the row. The allocation of this value shares an allocator with the auto-increment column (if such a column exists). If you specify an auto-increment column as the primary key, TiDB uses this column to identify the row. In this situation, the following situation might occur:

```sql
mysql> CREATE TABLE t(id INT UNIQUE KEY AUTO_INCREMENT);
Query OK, 0 rows affected (0.05 sec)

mysql> INSERT INTO t VALUES();
Query OK, 1 rows affected (0.00 sec)

mysql> INSERT INTO t VALUES();
Query OK, 1 rows affected (0.00 sec)

mysql> INSERT INTO t VALUES();
Query OK, 1 rows affected (0.00 sec)

mysql> SELECT _tidb_rowid, id FROM t;
+-------------+------+
| _tidb_rowid | id   |
+-------------+------+
|           2 |    1 |
|           4 |    3 |
|           6 |    5 |
+-------------+------+
3 rows in set (0.01 sec)
```

As shown, because of the shared allocator, the `id` increments by 2 each time. This behavior changes in [MySQL compatibility mode](/auto-increment.md#mysql-compatibility-mode), where there is no shared allocator and therefore no skipping of numbers.

<CustomContent platform="tidb">

> **Note:**
>
> The `AUTO_INCREMENT` attribute might cause hotspot in production environments. See [Troubleshoot HotSpot Issues](/troubleshoot-hot-spot-issues.md) for details. It is recommended to use [`AUTO_RANDOM`](/auto-random.md) instead.

</CustomContent>

<CustomContent platform="tidb-cloud">

> **Note:**
>
> The `AUTO_INCREMENT` attribute might cause hotspot in production environments. See [Troubleshoot HotSpot Issues](https://docs.pingcap.com/tidb/stable/troubleshoot-hot-spot-issues#handle-auto-increment-primary-key-hotspot-tables-using-auto_random) for details. It is recommended to use [`AUTO_RANDOM`](/auto-random.md) instead.

</CustomContent>

### Performance schema

<CustomContent platform="tidb">

TiDB utilizes a combination of [Prometheus and Grafana](/tidb-monitoring-api.md) for storing and querying performance monitoring metrics. In TiDB, performance schema tables do not return any results.

</CustomContent>

<CustomContent platform="tidb-cloud">

To check performance metrics in TiDB Cloud, you can either check the cluster overview page on the TiDB Cloud console or use [third-party monitoring integrations](/tidb-cloud/third-party-monitoring-integrations.md). Performance schema tables return empty results in TiDB.

</CustomContent>

### Query Execution Plan

The output format, content, and privilege settings of Query Execution Plan (`EXPLAIN`/`EXPLAIN FOR`) in TiDB differ significantly from those in MySQL.

In TiDB, the MySQL system variable `optimizer_switch` is read-only and has no effect on query plans. Although optimizer hints can be used in similar syntax to MySQL, the available hints and their implementation might differ.

For more information, refer to [Understand the Query Execution Plan](/explain-overview.md).

### Built-in functions

TiDB supports most of the built-in functions in MySQL, but not all. You can use the statement `SHOW BUILTINS` to get a list of the available functions.

For more information, refer to the [TiDB SQL Grammar](https://pingcap.github.io/sqlgram/#functioncallkeyword).

### DDL operations

In TiDB, all supported DDL changes can be performed online. However, there are some major restrictions on DDL operations in TiDB compared to MySQL:

* When using a single `ALTER TABLE` statement to alter multiple schema objects (such as columns or indexes) of a table, specifying the same object in multiple changes is not supported. For example, if you execute the `ALTER TABLE t1 MODIFY COLUMN c1 INT, DROP COLUMN c1` command, the `Unsupported operate same column/index` error is output.
* It is not supported to modify multiple TiDB-specific schema objects using a single `ALTER TABLE` statement, such as `TIFLASH REPLICA`, `SHARD_ROW_ID_BITS`, and `AUTO_ID_CACHE`.
* TiDB does not support the changes of some data types using `ALTER TABLE`. For example, TiDB does not support the change from the `DECIMAL` type to the `DATE` type. If a data type change is unsupported, TiDB reports the `Unsupported modify column: type %d not match origin %d` error. Refer to [`ALTER TABLE`](/sql-statements/sql-statement-modify-column.md) for more details.
* The `ALGORITHM={INSTANT,INPLACE,COPY}` syntax functions only as an assertion in TiDB, and does not modify the `ALTER` algorithm. See [`ALTER TABLE`](/sql-statements/sql-statement-alter-table.md) for further details.
* Adding/Dropping the primary key of the `CLUSTERED` type is unsupported. For more details about the primary key of the `CLUSTERED` type, refer to [clustered index](/clustered-indexes.md).
* Different types of indexes (`HASH|BTREE|RTREE|FULLTEXT`) are not supported, and will be parsed and ignored when specified.
* TiDB supports `HASH`, `RANGE`, `LIST`, and `KEY` partitioning types. Currently, the `KEY` partition type does not support partition statements with an empty partition column list. For an unsupported partition type, TiDB returns `Warning: Unsupported partition type %s, treat as normal table`, where `%s` is the specific unsupported partition type.
* Range, Range COLUMNS, List, and List COLUMNS partitioned tables support `ADD`, `DROP`, `TRUNCATE`, and `REORGANIZE` operations. Other partition operations are ignored.
* Hash and Key partitioned tables support `ADD`, `COALESCE`, and `TRUNCATE` operations. Other partition operations are ignored.
* The following syntaxes are not supported for partitioned tables:

    - `SUBPARTITION`
    - `{CHECK|OPTIMIZE|REPAIR|IMPORT|DISCARD|REBUILD} PARTITION`

    For more details on partitioning, see [Partitioning](/partitioned-table.md).

### Analyzing tables

In TiDB, [Statistics Collection](/statistics.md#manual-collection) differs from MySQL in that it completely rebuilds the statistics for a table, making it a more resource-intensive operation that takes longer to complete. In contrast, MySQL/InnoDB performs a relatively lightweight and short-lived operation.

For more information, refer to [`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md).

### Limitations of `SELECT` syntax

TiDB does not support the following `SELECT` syntax:

- `SELECT ... INTO @variable`
- `SELECT ... GROUP BY ... WITH ROLLUP`
- `SELECT .. GROUP BY expr` does not imply `GROUP BY expr ORDER BY expr` as it does in MySQL 5.7.

For more details, see the [`SELECT`](/sql-statements/sql-statement-select.md) statement reference.

### `UPDATE` statement

See the [`UPDATE`](/sql-statements/sql-statement-update.md) statement reference.

### Views

Views in TiDB are not updatable and do not support write operations such as `UPDATE`, `INSERT`, and `DELETE`.

### Temporary tables

For more information, see [Compatibility between TiDB local temporary tables and MySQL temporary tables](/temporary-tables.md#compatibility-with-mysql-temporary-tables).

### Character sets and collations

* To learn about the character sets and collations supported by TiDB, see [Character Set and Collation Overview](/character-set-and-collation.md).

* For information on the MySQL compatibility of the GBK character set, refer to [GBK compatibility](/character-set-gbk.md#mysql-compatibility) .

* TiDB inherits the character set used in the table as the national character set.

### Storage engines

TiDB allows for tables to be created with alternative storage engines. Despite this, the metadata as described by TiDB is for the InnoDB storage engine as a way to ensure compatibility.

<CustomContent platform="tidb">

To specify a storage engine using the [`--store`](/command-line-flags-for-tidb-configuration.md#--store) option, it is necessary to start the TiDB server. This storage engine abstraction feature is similar to MySQL.

</CustomContent>

### SQL modes

TiDB supports most [SQL modes](/sql-mode.md):

- The compatibility modes, such as `Oracle` and `PostgreSQL` are parsed but ignored. Compatibility modes are deprecated in MySQL 5.7 and removed in MySQL 8.0.
- The `ONLY_FULL_GROUP_BY` mode has minor [semantic differences](/functions-and-operators/aggregate-group-by-functions.md#differences-from-mysql) from MySQL 5.7.
- The `NO_DIR_IN_CREATE` and `NO_ENGINE_SUBSTITUTION` SQL modes in MySQL are accepted for compatibility, but are not applicable to TiDB.

### Default differences

TiDB has default differences when compared with MySQL 5.7 and MySQL 8.0:

- Default character set:
    - TiDB’s default value is `utf8mb4`.
    - MySQL 5.7’s default value is `latin1`.
    - MySQL 8.0’s default value is `utf8mb4`.
- Default collation:
    - TiDB’s default collation is `utf8mb4_bin`.
    - MySQL 5.7’s default collation is `utf8mb4_general_ci`.
    - MySQL 8.0’s default collation is `utf8mb4_0900_ai_ci`.
- Default SQL mode:
    - TiDB’s default SQL mode includes these modes: `ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION`.
    - MySQL’s default SQL mode:
        - The default SQL mode in MySQL 5.7 is the same as TiDB.
        - The default SQL mode in MySQL 8.0 includes these modes: `ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION`.
- Default value of `lower_case_table_names`:
    - The default value in TiDB is `2`, and only `2` is currently supported.
    - MySQL defaults to the following values:
        - On Linux: `0`. It means that table and database names are stored on disk according to the letter case specified in the `CREATE TABLE` or `CREATE DATABASE` statement. Name comparisons are case-sensitive.
        - On Windows: `1`. It means table names are stored in lowercase on disk, and name comparisons are not case-sensitive. MySQL converts all table names to lowercase on storage and lookup. This behavior also applies to database names and table aliases.
        - On macOS: `2`. It means table and database names are stored on disk according to the letter case specified in the `CREATE TABLE` or `CREATE DATABASE` statement, but MySQL converts them to lowercase on lookup. Name comparisons are not case-sensitive.
- Default value of `explicit_defaults_for_timestamp`:
    - The default value in TiDB is `ON`, and only `ON` is currently supported.
    - MySQL defaults to the following values:
        - For MySQL 5.7: `OFF`.
        - For MySQL 8.0: `ON`.

### Date and Time

TiDB supports named timezones with the following considerations:

+ TiDB uses all the timezone rules presently installed in the system for calculation, typically the `tzdata` package. This makes it possible to use all timezone names without needing to import timezone table data. Importing timezone table data will not change the calculation rules.
+ Currently, MySQL uses the local timezone by default, then relies on the current timezone rules built into the system (for example, when daylight savings time begins) for calculation. Without [importing timezone table data](https://dev.mysql.com/doc/refman/8.0/en/time-zone-support.html#time-zone-installation), MySQL cannot specify the timezone by name.

### Type system differences

The following column types are supported by MySQL but **not** by TiDB:

- `SQL_TSI_*` (includes SQL_TSI_MONTH, SQL_TSI_WEEK, SQL_TSI_DAY, SQL_TSI_HOUR, SQL_TSI_MINUTE, and SQL_TSI_SECOND, but excludes SQL_TSI_YEAR)

### Incompatibility due to deprecated features

TiDB does not implement specific features deprecated in MySQL, including:

- Specifying precision for floating-point types. MySQL 8.0 [deprecates](https://dev.mysql.com/doc/refman/8.0/en/floating-point-types.html) this feature, and it is recommended to use the `DECIMAL` type instead.
- The `ZEROFILL` attribute. MySQL 8.0 [deprecates](https://dev.mysql.com/doc/refman/8.0/en/numeric-type-attributes.html) this feature, and it is recommended to pad numeric values in your application instead.

### `CREATE RESOURCE GROUP`, `DROP RESOURCE GROUP`, and `ALTER RESOURCE GROUP` statements

The following statements for creating, modifying, and dropping resource groups have different supported parameters than MySQL. For details, see the following documents:

- [`CREATE RESOURCE GROUP`](/sql-statements/sql-statement-create-resource-group.md)
- [`DROP RESOURCE GROUP`](/sql-statements/sql-statement-drop-resource-group.md)
- [`ALTER RESOURCE GROUP`](/sql-statements/sql-statement-alter-resource-group.md)
