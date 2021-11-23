---
title: Temporary Tables
summary: Learn the temporary tables feature in TiDB, and learn how to use temporary tables to store intermediate data of an application, which helps reduce table management overhead and improve performance.
---

# Temporary Tables

The temporary tables feature is introduced in TiDB v5.3.0. This feature solves the issue of temporarily storing the intermediate results of an application, which frees you from frequently creating and dropping tables. You can store the intermediate calculation data in temporary tables. When the intermediate data is no longer needed, TiDB automatically cleans up and recycles the temporary tables. This avoids user applications being too complicated, reduces table management overhead, and improves performance.

This document introduces the user scenarios and the types of temporary tables, provides usage examples and instruction on how to limit the memory usage of temporary tables, and explains compatibility restrictions with other TiDB features.

## User scenarios

You can use TiDB temporary tables in the following scenarios:

- Cache the intermediate temporary data of an application. After the calculation is completed, the data is dumped to the ordinary table, and the temporary table is automatically released.
- Perform multiple DML operations on the same data in a short period of time. For example, in an e-commerce shopping cart application, add, modify, and delete products, complete the payment, and remove the shopping cart information.
- Quickly import intermediate temporary data in batches to improve the performance of importing temporary data.
- Update data in batches. Import data into temporary tables in the database in batches, and export the data to files after finishing modify the data.

## Types of temporary tables

Temporary tables in TiDB are divided into two types: local temporary tables and global temporary tables.

- For a local temporary table, the table definition and data in the table are visible only to the current session. This type is suitable for temporarily storing intermediate data in the session.
- For a global temporary table, the table definition is visible to the entire TiDB cluster, and the data in the table is visible only to the current transaction. This type is suitable for temporarily storing intermediate data in the transaction.

## Local temporary tables

The semantics of the local temporary table in TiDB is consistent with that of the MySQL temporary table. The characteristics are as follows:

- The table definition of a local temporary table is not persistent. A local temporary table is visible only to the session in which the table is created, and other sessions cannot access the table.
- You can create local temporary tables with the same name in different sessions, and each session reads only from and writes only to the local temporary table created in the session.
- The data of a local temporary table is visible to all transactions in the session.
- After a session ends, the local temporary table created in the session is automatically dropped.
- A local temporary table can have the same name as an ordinary table. In this case, in the DDL and DML statements, the ordinary table is hidden until the local temporary table is dropped.

To create a local temporary table, you can use the `CREATE TEMPORARY TABLE` statement. To drop a local temporary table, you can use the `DROP TABLE` or `DROP TEMPORARY TABLE` statement.

Different from MySQL, the local temporary tables in TiDB are all external tables, and no internal temporary tables will be created automatically when SQL statements are executed.

### Usage examples of local temporary tables

> **Note:**
>
> - Before you use the temporary table in TiDB, pay attention to the [compatibility restrictions with other TiDB features](#compatibility-restrictions-with-other-tidb-features) and the [compatibility with MySQL temporary tables](#compatibility-with-mysql-temporary-tables).
> - If you have created local temporary tables on a cluster earlier than TiDB v5.3.0, these tables are actually ordinary tables, and treated as ordinary tables after the cluster is upgraded to TiDB v5.3.0 or a later version.

Assume that there is an ordinary table `users`:

{{< copyable "sql" >}}

```sql
CREATE TABLE users (
    id BIGINT,
    name VARCHAR(100),
    PRIMARY KEY(id)
);
```

In session A, creating a local temporary table `users` does not conflict with the ordinary table `users`. When session A accesses the `users` table, it accesses the local temporary table `users`.

{{< copyable "sql" >}}

```sql
CREATE TEMPORARY TABLE users (
    id BIGINT,
    name VARCHAR(100),
    city VARCHAR(50),
    PRIMARY KEY(id)
);
```

```
Query OK, 0 rows affected (0.01 sec)
```

If you insert data into `users`, data is inserted to the local temporary table `users` in session A.

{{< copyable "sql" >}}

```sql
INSERT INTO users(id, name, city) VALUES(1001, 'Davis', 'LosAngeles');
```

```
Query OK, 1 row affected (0.00 sec)
```

{{< copyable "sql" >}}

```sql
SELECT * FROM users;
```

```
+------+-------+------------+
| id   | name  | city       |
+------+-------+------------+
| 1001 | Davis | LosAngeles |
+------+-------+------------+
1 row in set (0.00 sec)
```

In session B, creating a local temporary table `users` does not conflict with the ordinary table `users` or the local temporary table `users` in session A. When session B accesses the `users` table, it accesses the local temporary table `users` in session B.

{{< copyable "sql" >}}

```sql
CREATE TEMPORARY TABLE users (
    id BIGINT,
    name VARCHAR(100),
    city VARCHAR(50),
    PRIMARY KEY(id)
);
```

```
Query OK, 0 rows affected (0.01 sec)
```

If you insert data into `users`, data is inserted to the local temporary table `users` in session B.

{{< copyable "sql" >}}

```sql
INSERT INTO users(id, name, city) VALUES(1001, 'James', 'NewYork');
```

```
Query OK, 1 row affected (0.00 sec)
```

{{< copyable "sql" >}}

```sql
SELECT * FROM users;
```

```
+------+-------+---------+
| id   | name  | city    |
+------+-------+---------+
| 1001 | James | NewYork |
+------+-------+---------+
1 row in set (0.00 sec)
```

### Compatibility with MySQL temporary tables

The following features and limitations of TiDB local temporary tables are the same with those of MySQL temporary tables:

- When you create or drop local temporary tables, the current transaction is not automatically committed.
- After dropping the schema where a local temporary table is located, the temporary table is not dropped and is still readable and writable.
- Creating a local temporary table requires the `CREATE TEMPORARY TABLES` permission. All subsequent operations on the table do not require any permission.
- Local temporary tables do not support foreign keys and partitioned tables.
- Does not support creating views based on local temporary tables.
- `SHOW [FULL] TABLES` does not show local temporary tables.

Local temporary tables in TiDB are incompatible with MySQL temporary tables in the following aspects:

- TiDB local temporary tables do not support `ALTER TABLE`.
- TiDB local temporary tables ignore the `ENGINE` table option, and always store temporary table data in TiDB memory with a [memory limit](#limit-the-memory-usage-of-temporary-tables).
- When `MEMORY` is declared as the storage engine, TiDB local temporary tables are not restricted by the `MEMORY` storage engine.
- When `INNODB` or `MYISAM` is declared as the storage engine, TiDB local temporary tables ignore the system variables specific to the InnoDB temporary tables.
- MySQL does not permit referencing to the same temporary table multiple times in the same SQL statement. TiDB local temporary tables do not have this restriction.
- The system table `information_schema.INNODB_TEMP_TABLE_INFO` that shows temporary tables in MySQL does not exist in TiDB. Currently, TiDB does not have a system table that shows local temporary tables.
- TiDB does not have internal temporary tables. The MySQL system variables for internal temporary tables do not take effect for TiDB.

## Global temporary tables

The global temporary table is an extension of TiDB. The characteristics are as follows:

- The table definition of a global temporary table is persistent and visible to all sessions.
- The data of a global temporary table is visible only in the current transaction. When the transaction ends, the data is automatically cleared.
- A global temporary table cannot have the same name as an ordinary table.

To create a global temporary table, you can use the `CREATE GLOBAL TEMPORARY TABLE` statement ended with `ON COMMIT DELETE ROWS`. To drop a global temporary table, you can use the `DROP TABLE` or `DROP GLOBAL TEMPORARY TABLE` statement.

### Usage examples of global temporary tables

> **Note:**
>
> - Before you use the temporary table in TiDB, pay attention to the [compatibility restrictions with other TiDB features](#compatibility-restrictions-with-other-tidb-features).
> - If you have created global temporary tables on a TiDB cluster of v5.3.0 or later, when the cluster is downgraded to a version earlier than v5.3.0, these tables are handled as ordinary tables. In this case, a data error occurs.

Create a global temporary table `users` in session A:

{{< copyable "sql" >}}

```sql
CREATE GLOBAL TEMPORARY TABLE users (
    id BIGINT,
    name VARCHAR(100),
    city VARCHAR(50),
    PRIMARY KEY(id)
) ON COMMIT DELETE ROWS;
```

```
Query OK, 0 rows affected (0.01 sec)
```

The data written to `users` is visible to the current transaction:

{{< copyable "sql" >}}

```sql
BEGIN;
```

```
Query OK, 0 rows affected (0.00 sec)
```

{{< copyable "sql" >}}

```sql
INSERT INTO users(id, name, city) VALUES(1001, 'Davis', 'LosAngeles');
```

```
Query OK, 1 row affected (0.00 sec)
```

{{< copyable "sql" >}}

```sql
SELECT * FROM users;
```

```
+------+-------+------------+
| id   | name  | city       |
+------+-------+------------+
| 1001 | Davis | LosAngeles |
+------+-------+------------+
1 row in set (0.00 sec)
```

After the transaction ends, the data is automatically cleared:

{{< copyable "sql" >}}

```sql
COMMIT;
```

```
Query OK, 0 rows affected (0.00 sec)
```

{{< copyable "sql" >}}

```sql
SELECT * FROM users;
```

```
Empty set (0.00 sec)
```

After `users` is created in session A, session B can also read from and write to the `users` table:

{{< copyable "sql" >}}

```sql
SELECT * FROM users;
```

```
Empty set (0.00 sec)
```

> **Note:**
>
> If the transaction is automatically committed, after the SQL statement is executed, the inserted data is automatically cleared and unavailable to subsequent SQL executions. Therefore, you should use non-autocommit transactions to read from and write to global temporary tables.

## Limit the memory usage of temporary tables

No matter which storage engine is declared as `ENGINE` when you define a table, the data of local temporary tables and global temporary tables is only stored in the memory of TiDB instances. This data is not persisted.

To avoid memory overflow, you can limit the size of each temporary table using the [`tidb_tmp_table_max_size`](/system-variables.md#tidb_tmp_table_max_size-new-in-v530) system variable. Once a temporary table is larger than the `tidb_tmp_table_max_size` threshold value, TiDB reports an error. The default value of `tidb_tmp_table_max_size` is `64MB`.

For example, set the maximum size of a temporary table to `256MB`:

{{< copyable "sql" >}}

```sql
SET GLOBAL tidb_tmp_table_max_size=268435456;
```

## Compatibility restrictions with other TiDB features

Local temporary tables and global temporary tables in TiDB are **NOT** compatible with the following TiDB features:

- `AUTO_RANDOM` columns
- `SHARD_ROW_ID_BITS` and `PRE_SPLIT_REGIONS` table options
- Partitioned tables
- `SPLIT REGION` statements
- `ADMIN CHECK TABLE` and `ADMIN CHECKSUM TABLE` statements
- `FLASHBACK TABLE` and `RECOVER TABLE` statements
- Executing `CREATE TABLE LIKE` statements based on a temporary table
- Stale Read
- Foreign keys
- SQL bindings
- TiFlash replicas
- Creating views on a temporary table
- Placement Rules
- Execution plans involving a temporary table are not cached by `prepare plan cache`.

Local temporary tables in TiDB do **NOT** support the following feature:

- Reading historical data using the `tidb_snapshot` system variable.

## TiDB ecosystem tool support

Local temporary tables are not exported, backed up or replicated by TiDB ecosystem tools, because these tables are visible only to the current session.

Global temporary tables are exported, backed up, and replicated by TiDB ecosystem tools, because the table definition is globally visible. Note that the data on the tables are not exported.

> **Note:**
>
> - Replicating temporary tables using TiCDC requires TiCDC v5.3.0 or later. Otherwise, the table definition of the downstream table is wrong.
> - Backing up temporary tables using BR requires BR v5.3.0 or later. Otherwise, the table definitions of the backed temporary tables are wrong.
> - The cluster to export, the cluster after data restore, and the downstream cluster of a replication should support global temporary tables. Otherwise, an error is reported.

## See also

* [CREATE TABLE](/sql-statements/sql-statement-create-table.md)
* [CREATE TABLE LIKE](/sql-statements/sql-statement-create-table-like.md)
* [DROP TABLE](/sql-statements/sql-statement-drop-table.md)
