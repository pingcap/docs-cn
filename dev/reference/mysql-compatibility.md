---
title: Compatibility with MySQL
summary: Learn about the compatibility of TiDB with MySQL, and the unsupported and different features.
category: reference
---

# Compatibility with MySQL

TiDB supports both the MySQL wire protocol and the majority of its syntax. This means that you can use your existing MySQL connectors and clients, and your existing applications can often be migrated to TiDB without changing any application code.

Currently TiDB Server advertises itself as MySQL 5.7 and works with most MySQL database tools such as PHPMyAdmin, Navicat, MySQL Workbench, mysqldump, and mydumper/myloader.

However, TiDB does not support some of MySQL features or behaves differently from MySQL because these features cannot be easily implemented in a distributed system. For some MySQL syntax, TiDB can parse but does not process it. For example, `Engine` in the `CREATE TABLE` statement can be parsed but is ignored.

> **Note:**
>
> This page refers to general differences between MySQL and TiDB. Please also see the dedicated pages for [Security](/dev/reference/security/compatibility.md) and [Transaction Model](/dev/reference/transactions/transaction-model.md) compatibility.

## Unsupported features

+ Stored procedures and functions
+ Triggers
+ Events
+ User-defined functions
+ `FOREIGN KEY` constraints
+ `FULLTEXT` functions and indexes
+ `SPATIAL` functions and indexes
+ Character sets other than `utf8`, `utf8mb4`, `ascii`, `latin1` and `binary`
+ Collations other than `BINARY`
+ Add primary key
+ Drop primary key
+ SYS schema
+ Optimizer trace
+ XML Functions
+ X-Protocol
+ Savepoints
+ Column-level privileges
+ `CREATE TABLE tblName AS SELECT stmt` syntax
+ `CREATE TEMPORARY TABLE` syntax
+ `XA` syntax (TiDB uses a two-phase commit internally, but this is not exposed via an SQL interface)
+ `CHECK TABLE` syntax
+ `CHECKSUM TABLE` syntax
+ `GET_LOCK` and `RELEASE_LOCK` functions

## Features that are different from MySQL

### Auto-increment ID

In TiDB, auto-increment columns are only guaranteed to be incremental and unique but are *not* guaranteed to be allocated sequentially. Currently, TiDB allocates IDs in batches. If data is inserted into multiple TiDB servers simultaneously, the allocated IDs will not be sequential.

> **Note:**
>
> If you use auto-increment IDs in a cluster with multiple tidb-server instances, do not mix default values and custom values. Otherwise, an error might occur in the following situation.

Assume that you have a table with the auto-increment ID:

```sql
create table t(id int unique key auto_increment, c int);
```

The principle of the auto-increment ID in TiDB is that each tidb-server instance caches a section of ID values (currently 30000 IDs are cached) for allocation and fetches the next section after this section is used up.

Assume that the cluster contains two tidb-server instances, namely Instance A and Instance B. Instance A caches the auto-increment ID of [1, 30000], while Instance B caches the auto-increment ID of [30001, 60000].

The operations are executed as follows:

1. The client issues the `insert into t values (1, 1)` statement to Instance B which sets the `id` to 1 and the statement is executed successfully.
2. The client issues the `insert into t (c) (1)` statement to Instance A. This statement does not specify the value of `id`, so Instance A allocates the value. Currently, Instances A caches the auto-increment ID of [1, 30000], so it allocates the `id` value to 1 and adds 1 to the local counter. However, at this time the data with the `id` of 1 already exists in the cluster, therefore it reports `Duplicated Error`.

Also, starting from TiDB 2.1.18 and 3.0.4, TiDB supports using the system variable `tidb_allow_remove_auto_inc` to control whether the `auto_increment` property of a column is allowed to be removed by executing  `ALTER TABLE MODIFY` or `ALTER TABLE CHANGE` statements. It is not allowed by default.

### Performance schema

Performance schema tables return empty results in TiDB. TiDB uses a combination of [Prometheus and Grafana](/dev/how-to/monitor/monitor-a-cluster.md) for performance metrics instead.

### Query Execution Plan

The output format of Query Execution Plan (`EXPLAIN`/`EXPLAIN FOR`) in TiDB is greatly different from that in MySQL. Besides, the output content and the privileges setting of `EXPLAIN FOR` are not the same as those of MySQL. See [Understand the Query Execution Plan](/dev/reference/performance/understanding-the-query-execution-plan.md) for more details.

### Built-in functions

TiDB supports most of the MySQL built-in functions, but not all. See [TiDB SQL Grammar](https://pingcap.github.io/sqlgram/#functioncallkeyword) for the supported functions.

### DDL

In TiDB DDL does not block reads or writes to tables while in operation. However, some restrictions currently apply to DDL changes:

+ Add Index:
    - Does not support creating multiple indexes at the same time.
    - Adding an index on a generated column via `ALTER TABLE` is not supported.
+ Add Column:
    - Does not support creating multiple columns at the same time.
    - Does not support setting a column as the `PRIMARY KEY`, or creating a unique index, or specifying `auto_increment` while adding it.
+ Drop Column: Does not support dropping the `PRIMARY KEY` column or index column.
+ Change/Modify Column:
    - Does not support lossy changes, such as from `BIGINT` to `INTEGER` or `VARCHAR(255)` to `VARCHAR(10)`.
    - Does not support modifying the precision of `DECIMAL` data types.
    - Does not support changing the `UNSIGNED` attribute.
    - Only supports changing the `CHARACTER SET` attribute from `utf8` to `utf8mb4`.
+ `LOCK [=] {DEFAULT|NONE|SHARED|EXCLUSIVE}`: the syntax is supported, but is not applicable to TiDB. All DDL changes that are supported do not lock the table.
+ `ALGORITHM [=] {DEFAULT|INSTANT|INPLACE|COPY}`: the syntax for `ALGORITHM=INSTANT` and `ALGORITHM=INPLACE` is fully supported, but it works differently from MySQL because some operations that are `INPLACE` in MySQL are `INSTANT` in TiDB. The syntax `ALGORITHM=COPY` is not applicable to TIDB and returns a warning.

For more information, see [Online Schema Changes](/dev/key-features.md#online-schema-changes).

### Analyze table

[`ANALYZE TABLE`](/dev/reference/performance/statistics.md#manual-collection) works differently in TiDB than in MySQL, in that it is a relatively lightweight and short-lived operation in MySQL/InnoDB, while in TiDB it completely rebuilds the statistics for a table and can take much longer to complete.

### Views

Views in TiDB are currently non-insertable and non-updatable.

### Storage engines

For compatibility reasons, TiDB supports the syntax to create tables with alternative storage engines. Metadata commands describe tables as being of engine InnoDB:

```sql
mysql> CREATE TABLE t1 (a INT) ENGINE=MyISAM;
Query OK, 0 rows affected (0.14 sec)

mysql> SHOW CREATE TABLE t1\G
*************************** 1. row ***************************
       Table: t1
Create Table: CREATE TABLE `t1` (
  `a` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
1 row in set (0.00 sec)
```

Architecturally, TiDB does support a similar storage engine abstraction to MySQL, and user tables are created in the engine specified by the [`--store`](/dev/reference/configuration/tidb-server/configuration.md#--store) option used when you start tidb-server (typically `tikv`).

### SQL modes

TiDB supports **all of the SQL modes** from MySQL 5.7 with minor exceptions:

- The compatibility modes deprecated in MySQL 5.7 and removed in MySQL 8.0 are not supported (such as `ORACLE`, `POSTGRESQL` etc).
- The mode `ONLY_FULL_GROUP_BY` has minor [semantic differences](/dev/reference/sql/functions-and-operators/aggregate-group-by-functions.md#differences-from-mysql) to MySQL 5.7, which we plan to address in the future.
- The SQL modes `NO_DIR_IN_CREATE` and `NO_ENGINE_SUBSTITUTION` are supported for compatibility, but are not applicable to TiDB.

### Version-specific comments

TiDB executes all MySQL version-specific comments, regardless of the version they apply to. For example, the comment `/*!90000 */` would instruct a MySQL server less than 9.0 to not execute code. In TiDB this code will always be executed:

```sql
mysql 8.0.16> SELECT /*!90000 "I should not run", */ "I should run" FROM dual;
+--------------+
| I should run |
+--------------+
| I should run |
+--------------+
1 row in set (0.00 sec)

tidb> SELECT /*!90000 "I should not run", */ "I should run" FROM dual;
+------------------+--------------+
| I should not run | I should run |
+------------------+--------------+
| I should not run | I should run |
+------------------+--------------+
1 row in set (0.00 sec)
```

### Lock tables

Support for `LOCK TABLE` syntax is currently experimental, and must be explicitly enabled ([TiDB #10343](https://github.com/pingcap/tidb/pull/10343)).

It is recommended to use the historical reads feature of `tidb_snapshot` to produce consistent reads, instead of `FLUSH TABLES WITH READ LOCK`. Support for `tidb_snapshot` is available in [Mydumper](/dev/reference/tools/mydumper.md)).

### Default differences

- Default character set:
    - The default value in TiDB is `utf8mb4`.
    - The default value in MySQL 5.7 is `latin1`, but changes to `utf8mb4` in MySQL 8.0.
- Default collation:
    - The default collation of `utf8mb4` in TiDB is `utf8mb4_bin`.
    - The default collation of `utf8mb4` in MySQL 5.7 is `utf8mb4_general_ci`, but changes to `utf8mb4_0900_ai_ci` in MySQL 8.0.
    - You can use the [`SHOW CHARACTER SET`](/dev/reference/sql/statements/show-character-set.md) statement to check the default collations of all character sets.
- Default value of `foreign_key_checks`:
    - The default value in TiDB is `OFF` and currently TiDB only supports `OFF`.
    - The default value in MySQL 5.7 is `ON`.
- Default value of `lower_case_table_names`:
    - The default value in TiDB is 2 and currently TiDB only supports 2.
    - The default value in MySQL:
        - On Linux: 0
        - On Windows: 1
        - On macOS: 2
- Default value of `explicit_defaults_for_timestamp`:
    - The default value in TiDB is `ON` and currently TiDB only supports `ON`.
    - The default value in MySQL:
        - For MySQL 5.7: `OFF`
        - For MySQL 8.0: `ON`

### Date and Time

#### Named timezone

TiDB supports named timezones such as `America/Los_Angeles` without having to load the [time zone information tables](https://dev.mysql.com/doc/refman/8.0/en/time-zone-support.html#time-zone-installation) as in MySQL.

Because they are built-in, named time zones in TiDB might behave slightly differently to MySQL, and cannot be modified. For example, in TiDB the names are case-sensitive [#8087](https://github.com/pingcap/tidb/issues/8087).

> **Note:**
>
> TiKV calculates time-related expressions that can be pushed down to it. This calculation uses the built-in time zone rule and does not depend on the time zone rule installed in the system. If the time zone rule installed in the system does not match the version of the built-in time zone rule in TiKV, the time data that can be inserted might result in a statement error in a few cases.
>
> For example, if the tzdata 2018a time zone rule is installed in the system, the time `1988-04-17 02:00:00` can be inserted into TiDB of the 3.0.0-rc.1 version when the time zone is set to Asia/Shanghai or the time zone is set to the local time zone and the local time zone is Asia/Shanghai. But reading this record might result in a statement error because this time does not exist in the Asia/Shanghai time zone according to the tzdata 2018i time zone rule used by TiKV 3.0.0-rc.1. Daylight saving time is one hour late.
>
> The named timezone rules in TiKV of two versions are as follows:
>
> - 3.0.0 RC.1 and later: [tzdata 2018i](https://github.com/eggert/tz/tree/2018i)
> - 2.1.0 RC.1 and later: [tzdata 2018e](https://github.com/eggert/tz/tree/2018e)

#### Zero month and zero day

It is not recommended to unset the `NO_ZERO_DATE` and `NO_ZERO_IN_DATE` SQL modes, which are enabled by default in TiDB as in MySQL. While TiDB supports operating with these modes disabled, the TiKV coprocessor does not. Executing certain statements that push down date and time processing functions to TiKV might result in a statement error.
