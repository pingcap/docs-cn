# Compatibility with MySQL

TiDB supports the majority of the MySQL grammar, including cross-row transactions, JOIN, subquery, and so on. You can connect to TiDB directly using your own MySQL client. If your existing business is developed based on MySQL, you can replace MySQL with TiDB to power your application without changing a single line of code in most cases.

TiDB is compatible with most of the MySQL database management & administration tools such as `PHPMyAdmin`, `Navicat`, `MySQL Workbench`, and so on. It also supports the database backup tools, such as `mysqldump` and `mydumper/myloader`.

However, in TiDB, the following MySQL features are not supported for the time being or are different:

## Unsupported features

* Stored Procedures

* View

* Trigger

* The user-defined functions

* The `FOREIGN KEY` constraints

* The `FULLTEXT` indexes

* The `Spatial` indexes

* The Non-UTF-8 Characters

* The JSON Data Type

## Features that are different from MySQL

### Auto-Increment ID

The auto-increment ID feature in TiDB is only guaranteed to be automatically incremental and unique but is not guaranteed to be allocated sequentially. Currently, TiDB is allocating IDs in batches. If data is inserted into multiple TiDB servers simultaneously, the allocated IDs are not sequential.

### Built-in Functions

TiDB supports most of the MySQL built-in functions, but not all. See [TiDB SQL Grammar](https://pingcap.github.io/sqlgram/#FunctionCallKeyword) for the supported functions.

### DDL

TiDB implements the asynchronous schema changes algorithm in F1. The Data Manipulation Language (DML) operations cannot be blocked during DDL the execution. Currently, the supported DDL includes:

* Create Database

* Drop Database

* Create Table

* Drop Database

* Add Index

* Drop Index

* Add Column

* Drop Column

* Truncate Table

* Rename Table

### Transaction

TiDB implements an optimistic transaction model. Unlike MySQL, which uses row-level locking to avoid write conflict, in TiDB, the write conflict is checked only in the `commit` process during the execution of the statements like `Update`, `Insert`, `Delete`, and so on. 

**Note:** On the business side, remember to check the returned results of `commit` because even there is no error in the execution, there might be errors in the `commit` process.

