---
title: Compatibility with MySQL
summary: Learn about the compatibility of TiDB with MySQL, and the unsupported and different features.
category: reference
aliases: ['/docs/sql/mysql-compatibility/'] 
---

# Compatibility with MySQL

TiDB supports both the MySQL wire protocol and the majority of its syntax. This means that you can use your existing MySQL connectors and clients, and your existing applications can often be migrated to TiDB without changing any application code.

Currently TiDB Server advertises itself as MySQL 5.7 and works with most MySQL database tools such as PHPMyAdmin, Navicat, MySQL Workbench, mysqldump, and mydumper/myloader.

> **Note:**
>
> This page refers to general differences between MySQL and TiDB. Please also see the dedicated pages for [Security](/dev/reference/security/compatibility.md) and [Transaction Model](/dev/reference/transactions/transaction-model.md) compatibility.

## Unsupported features

+ Stored procedures and functions
+ Views
+ Triggers
+ Events
+ User-defined functions
+ `FOREIGN KEY` constraints
+ `FULLTEXT` functions and indexes
+ `SPATIAL` functions and indexes
+ Character sets other than `utf8`
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
+ `LOCK TABLE` syntax (TiDB uses `tidb_snapshot` to [produce backups](/dev/reference/tools/mydumper.md))
+ `CHECK TABLE` syntax
+ `CHECKSUM TABLE` syntax

## Features that are different from MySQL

### Auto-increment ID

In TiDB, auto-increment columns are only guaranteed to be incremental and unique but are *not* guaranteed to be allocated sequentially. Currently, TiDB allocates IDs in batches. If data is inserted into multiple TiDB servers simultaneously, the allocated IDs will not be sequential.

> **Warning:**
>
> If you use auto-increment IDs in a cluster with multiple tidb-server instances, do not mix default values and custom values, otherwise an error will occur in the following situation:
> 
> Assume that you have a table with the auto-increment ID:
> 
> `create table t(id int unique key auto_increment, c int);`
> 
> The principle of the auto-increment ID in TiDB is that each tidb-server instance caches a section of ID values (currently 30000 IDs are cached) for allocation and fetches the next section after this section is used up.
>
> Assume that the cluster contains two tidb-server instances, namely Instance A and Instance B. Instance A caches the auto-increment ID of [1, 30000], while Instance B caches the auto-increment ID of [30001, 60000].
> 
> The operations are executed as follows:
>
> 1. The client issues the `insert into t values (1, 1)` statement to Instance B which sets the `id` to 1 and the statement is executed successfully.
> 2. The client issues the `insert into t (c) (1)` statement to Instance A. This statement does not specify the value of `id`, so Instance A allocates the value. Currently, Instances A caches the auto-increment ID of [1, 30000], so it allocates the `id` value to 1 and adds 1 to the local counter. However, at this time the data with the `id` of 1 already exists in the cluster, therefore it reports `Duplicated Error`.

### Performance schema

Performance schema tables return empty results in TiDB. TiDB uses a combination of [Prometheus and Grafana](/dev/how-to/monitor/monitor-a-cluster.md#use-prometheus-and-grafana) for performance metrics instead.

### Query Execution Plan

The output format of Query Execution Plan (`EXPLAIN`/`EXPLAIN FOR`) in TiDB is greatly different from that in MySQL. Besides, the output content and the privileges setting of `EXPLAIN FOR` are not the same as those of MySQL. See [Understand the Query Execution Plan](/dev/reference/performance/understanding-the-query-execution-plan.md) for more details.

### Built-in functions

TiDB supports most of the MySQL built-in functions, but not all. See [TiDB SQL Grammar](https://pingcap.github.io/sqlgram/#FunctionCallKeyword) for the supported functions.

### DDL

TiDB implements the asynchronous schema changes algorithm in F1. The Data Manipulation Language (DML) operations cannot be blocked during DDL the execution. Currently, the supported DDL includes:

+ Create Database
+ Drop Database
+ Create Table
+ Drop Table
+ Add Index: Does not support creating multiple indexes at the same time.
+ Drop Index
+ Add Column:
    - Does not support creating multiple columns at the same time.
    - Does not support setting a column as the primary key, or creating a unique index, or specifying auto_increment while adding it.
+ Drop Column: Does not support dropping the primary key column or index column.
+ Alter Column
+ Change/Modify Column
    - Supports changing/modifying the types among the following integer types: TinyInt, SmallInt, MediumInt, Int, BigInt.
    - Supports changing/modifying the types among the following string types: Char, Varchar, Text, TinyText, MediumText, LongText
    - Support changing/modifying the types among the following string types: Blob, TinyBlob, MediumBlob, LongBlob.
    
        > **Note:**
        >
        > The changing/modifying column operation cannot make the length of the original type become shorter and it cannot change the unsigned/charset/collate attributes of the column.

    - Supports changing the following type definitions: `default value`, `comment`, `null`, `not null` and `OnUpdate`.
    - Supports parsing the `LOCK [=] {DEFAULT|NONE|SHARED|EXCLUSIVE}` syntax, but there is no actual operation.

+ Truncate Table
+ Rename Table
+ Create Table Like

### Analyze table

+ [`ANALYZE TABLE`](/dev/reference/performance/statistics.md#manual-collection) works differently in TiDB than in MySQL, in that it is a relatively lightweight and short-lived operation in MySQL/InnoDB, while in TiDB it completely rebuilds the statistics for a table and can take much longer to complete.
    
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin
1 row in set (0.00 sec)
```

Architecturally, TiDB does support a similar storage engine abstraction to MySQL, and user tables are created in the engine specified by the [`--store`](/sql/server-command-option.md#--store) option used when you start tidb-server (typically `tikv`).

### SQL modes

TiDB supports **all of the SQL modes** from MySQL 5.7 with minor exceptions:

- The compatibility modes deprecated in MySQL 5.7 and removed in MySQL 8.0 are not supported (such as `ORACLE`, `POSTGRESQL` etc).
- The mode `ONLY_FULL_GROUP_BY` has minor [semantic differences](/dev/reference/sql/functions-and-operators/aggregate-group-by-functions.md#differences-from-mysql) to MySQL 5.7, which we plan to address in the future.
- The SQL modes `NO_DIR_IN_CREATE` and `NO_ENGINE_SUBSTITUTION` are supported for compatibility, but are not applicable to TiDB. 

### Default differences

- Default character set:
    - The default value in TiDB is `utf8` which is equivalent to `utf8mb4` in MySQL.
    - The default value in MySQL 5.7 is `latin1`, but changes to `utf8mb4` in MySQL 8.0.
- Default collation: `latin1_swedish_ci` in MySQL 5.7, while `binary` in TiDB.
- Default SQL mode:
    - The default value in TiDB is `STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION`.
    - The default value in MySQL 5.7 is `ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION`.
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
    
