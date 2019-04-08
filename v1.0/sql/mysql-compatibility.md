---
title: Compatibility with MySQL
category: user guide
---

# Compatibility with MySQL

TiDB supports the majority of the MySQL grammar, including cross-row transactions, JOIN, subquery, and so on. You can connect to TiDB directly using your own MySQL client. If your existing business is developed based on MySQL, you can replace MySQL with TiDB to power your application without changing a single line of code in most cases.

TiDB is compatible with most of the MySQL database management & administration tools such as `PHPMyAdmin`, `Navicat`, `MySQL Workbench`, and so on. It also supports the database backup tools, such as `mysqldump` and `mydumper/myloader`.

However, in TiDB, the following MySQL features are not supported for the time being or are different:

## Unsupported features

+ Stored Procedures
+ View
+ Trigger
+ The user-defined functions
+ The `FOREIGN KEY` constraints
+ The `FULLTEXT` indexes
+ The `Spatial` indexes
+ The Non-UTF-8 characters
+ The JSON data type
+ Add primary key
+ Drop primary key

## Features that are different from MySQL

### Auto-increment ID

The auto-increment ID feature in TiDB is only guaranteed to be automatically incremental and unique but is not guaranteed to be allocated sequentially. Currently, TiDB is allocating IDs in batches. If data is inserted into multiple TiDB servers simultaneously, the allocated IDs are not sequential.

> **Warning**:
> 
> If you use the auto-increment ID in a cluster with multiple TiDB servers, do not mix the default value and the custom value, because it reports an error in the following situation:
> 
> In a cluster of two TiDB servers, namely TiDB A and TiDB B, TiDB A caches [1,5000] auto-increment ID, while TiDB B caches [5001,10000] auto-increment ID. Use the following statement to create a table with auto-increment ID:
> 
> ```
> create table t(id int unique key auto_increment, c int);
> ```
>
> The statement is executed as follows:
>
> 1. The client inserts a statement to TiDB B which sets the `id` to be 1 and the statement is executed successfully.
> 2. The client inserts a record to TiDB A which sets the `id` set to the default value 1. In this case, it returns `Duplicated Error`.

### Built-in functions

TiDB supports most of the MySQL built-in functions, but not all. See [TiDB SQL Grammar](https://pingcap.github.io/sqlgram/#FunctionCallKeyword) for the supported functions.

### DDL

TiDB implements the asynchronous schema changes algorithm in F1. The Data Manipulation Language (DML) operations cannot be blocked during DDL the execution. Currently, the supported DDL includes:

+ Create Database
+ Drop Database
+ Create Table
+ Drop Table
+ Add Index: Does not support creating multiple indexs at the same time.
+ Drop Index
+ Add Column:
    - Does not support creating multiple columns at the same time.
    - Does not support setting a column as the primary key, or creating a unique index, or specifying auto_increment while adding it.
+ Drop Column: Does not support dropping the primary key column or index column.
+ Alter Column
+ Change/Modify Column
    - Supports changing/modifying the types among the following integer types: TinyInt，SmallInt，MediumInt，Int，BigInt.
    - Supports changing/modifying the types among the following string types: Char，Varchar，Text，TinyText，MediumText，LongText
    - Support changing/modifying the types among the following string types: Blob，TinyBlob，MediumBlob，LongBlob.

**Note:** The change/modifying column operation cannot make the length of the original type become shorter and it cannot change the unsigned/charset/collate attributes of the column.

    - Supports changing the following type definitions: default value，comment，null，not null and OnUpdate, but does not support changing from null to not null.
    - Supports parsing the `LOCK [=] {DEFAULT|NONE|SHARED|EXCLUSIVE}` syntax, but there is no actual operation.

+ Truncate Table
+ Rename Table
+ Create Table Like


### Transaction

TiDB implements an optimistic transaction model. Unlike MySQL, which uses row-level locking to avoid write conflict, in TiDB, the write conflict is checked only in the `commit` process during the execution of the statements like `Update`, `Insert`, `Delete`, and so on.

**Note:** On the business side, remember to check the returned results of `commit` because even there is no error in the execution, there might be errors in the `commit` process.


### Load data

+ Syntax:

    ```
    LOAD DATA LOCAL INFILE 'file_name' INTO TABLE table_name
        {FIELDS | COLUMNS} TERMINATED BY 'string' ENCLOSED BY 'char' ESCAPED BY 'char'
        LINES STARTING BY 'string' TERMINATED BY 'string'
        (col_name ...);
    ```
Currently, the supported `ESCAPED BY` characters are: `/\/\`.
+ Transaction

    When TiDB is in the execution of loading data, by default, a record with 20,000 rows of data is seen as a transaction for persistent storage. If a load data operation inserts more than 20,000 rows, it will be divided into multiple transactions to commit. If an error occurs in one transaction, this transaction in process will not be committed. However, transactions before that are committed successfully. In this case, a part of the load data operation is successfully inserted, and the rest of the data insertion fails. But MySQL treats a load data operation as a transaction, one error leads to the failure of the entire load data operation.
