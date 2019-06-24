---
title: Compatibility with MySQL
summary: Learn about the compatibility of TiDB with MySQL, and the unsupported and different features.
category: user guide
---

# Compatibility with MySQL

TiDB supports the majority of the MySQL 5.7 syntax, including cross-row transactions, JOIN, subquery, and so on. You can connect to TiDB directly using your own MySQL client. If your existing business is developed based on MySQL, you can replace MySQL with TiDB to power your application without changing a single line of code in most cases.

TiDB is compatible with most of the MySQL database management & administration tools such as `PHPMyAdmin`, `Navicat`, `MySQL Workbench`, and so on. It also supports the database backup tools, such as `mysqldump` and `mydumper/myloader`.

However, in TiDB, the following MySQL features are not supported for the time being or are different:

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

## Features that are different from MySQL

### Auto-increment ID

The auto-increment ID feature in TiDB is only guaranteed to be automatically incremental and unique but is not guaranteed to be allocated sequentially. Currently, TiDB is allocating IDs in batches. If data is inserted into multiple TiDB servers simultaneously, the allocated IDs are not sequential.

> **Warning:**
>
> If you use the auto-increment ID in a cluster with multiple tidb-server instances, do not mix the default value and the custom value, otherwise an error occurs in the following situation:
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

Performance schema tables return empty results in TiDB. TiDB uses a combination of [Prometheus and Grafana](https://pingcap.com/docs/op-guide/monitor/#use-prometheus-and-grafana) for performance metrics instead.

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

### Transaction model

TiDB implements an optimistic transaction model. Unlike MySQL, which uses row-level locking to avoid write conflict, in TiDB, the write conflict is checked only in the `commit` process during the execution of the statements like `Update`, `Insert`, `Delete`, and so on.

Similarly, functions such as `GET_LOCK()` and `RELEASE_LOCK()` and statements such as `SELECT .. FOR UPDATE` do not work in the same way as in MySQL.

> **Note:**
>
> On the business side, remember to check the returned results of `commit` because even there is no error in the execution, there might be errors in the `commit` process.

### Large transactions

Due to the distributed, 2-phase commit requirement of TiDB, large transactions that modify data can be particularly problematic. TiDB intentionally sets some limits on transaction sizes to reduce this impact:

* Each Key-Value entry is no more than 6MB
* The total number of Key-Value entries is no more than 300,000
* The total size of Key-Value entries is no more than 100MB

### Small transactions

Since each transaction in TiDB requires two round trips to the PD leader, small transactions may have higher latencies in TiDB than MySQL. As a hypothetical example, the following query could be improved by moving from `auto_commit` to using an explicit transaction:

```sql
# original version with auto_commit
UPDATE my_table SET a='new_value' WHERE id = 1; 
UPDATE my_table SET a='newer_value' WHERE id = 2;
UPDATE my_table SET a='newest_value' WHERE id = 3;

# improved version
START TRANSACTION;
UPDATE my_table SET a='new_value' WHERE id = 1; 
UPDATE my_table SET a='newer_value' WHERE id = 2;
UPDATE my_table SET a='newest_value' WHERE id = 3;
COMMIT;
```

### Single-threaded workloads

Due to its distributed nature, workloads that are single-threaded may perform worse in TiDB when compared to a single-instance deployment of MySQL. This difference is similar to the case of small transactions being potentially slower in TiDB.

### Load data

+ Syntax:

    ```
    LOAD DATA LOCAL INFILE 'file_name' INTO TABLE table_name
        {FIELDS | COLUMNS} TERMINATED BY 'string' ENCLOSED BY 'char' ESCAPED BY 'char'
        LINES STARTING BY 'string' TERMINATED BY 'string'
        IGNORE n LINES
        (col_name ...);
    ```
    
    Currently, the supported `ESCAPED BY` characters are: `/\/\`.

+ Transaction

    When TiDB is in the execution of loading data, by default, a record with 20,000 rows of data is seen as a transaction for persistent storage. If a load data operation inserts more than 20,000 rows, it will be divided into multiple transactions to commit. If an error occurs in one transaction, this transaction in process will not be committed. However, transactions before that are committed successfully. In this case, a part of the load data operation is successfully inserted, and the rest of the data insertion fails. But MySQL treats a load data operation as a transaction, one error leads to the failure of the entire load data operation.
    
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

Architecturally, TiDB does support a similar storage engine abstraction to MySQL, and user tables are created in the engine specified by the [`--store`](server-command-option.md#--store) option used when you start tidb-server (typically `tikv`).

### SQL Modes

TiDB supports **all of the SQL modes** from MySQL 5.7 with minor exceptions:

1. The `ALLOW_INVALID_DATES` mode is not yet supported. See [TiDB #8263](https://github.com/pingcap/tidb/issues/8263).
2. The compatibility modes deprecated in MySQL 5.7 and removed in MySQL 8.0 are not supported (such as `ORACLE`, `POSTGRESQL` etc).
3. The mode `ONLY_FULL_GROUP_BY` has minor [semantic differences](../sql/aggregate-group-by-functions.md#differences-from-mysql) to MySQL 5.7, which we plan to address in the future.
4. The SQL modes `NO_DIR_IN_CREATE` and `NO_ENGINE_SUBSTITUTION` are supported for compatibility, but are not applicable to TiDB. 

### EXPLAIN

The output of the query execution plan returned from the `EXPLAIN` command differs from MySQL. For more information, see [Understand the Query Execution Plan](../sql/understanding-the-query-execution-plan.md).

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
