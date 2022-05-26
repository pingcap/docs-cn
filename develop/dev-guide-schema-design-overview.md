---
title: TiDB Database Schema Design Overview
summary: Learn the basics on TiDB database schema design.
---

# TiDB Database Schema Design Overview

This document provides the basics of TiDB database schema design, including the objects in TiDB, access control, database schema changes, and object limitations.

In the subsequent documents, [Bookshop](/develop/dev-guide-bookshop-schema-design.md) will be taken as an example to show you how to design a database and perform data read and write operations in a database.

## Objects in TiDB

To distinguish some general terms, here is a brief agreement on the terms used in TiDB:

- To avoid confusion with the generic term [database](https://en.wikipedia.org/wiki/Database), **database** in this document refers to a logical object, **TiDB** refers to TiDB itself, and **cluster** refers to a deployed instance of TiDB.

- TiDB uses MySQL-compatible syntax, in which **schema** means the generic term [schema](https://en.wiktionary.org/wiki/schema) instead of a logical object in a database. For more information, see [MySQL documentation](https://dev.mysql.com/doc-/refman/8.0/en/create-database.html). Make sure that you note this difference if you are migrating from databases that have schemas as logical objects (for example, [PostgreSQL](https://www.postgresql.org/docs/current/ddl-schemas.html), [Oracle](https://docs.oracle.com/en/database/oracle/oracle-database/21/tdddg/creating-managing-schema-objects.html), and [Microsoft SQL Server](https://docs.microsoft.com/en-us/sql/relational-databases/security/authentication-access/create-a-database-schema?view=sql-server-ver15)).

### Database

A database in TiDB is a collection of objects such as tables and indexes.

TiDB comes with a default database named `test`. However, it is recommended that you create your own database instead of using the `test` database.

### Table

A table is a collection of related data in a [database](#database).

Each table consists of **rows** and **columns**. Each value in a row belongs to a specific **column**. Each column allows only a single data type. To further qualify columns, you can add some [constraints](/constraints.md). To accelerate calculations, you can add [generated columns (experimental feature)](/generated-columns.md).

### Index

An index is a copy of selected columns in a table. You can create an index using one or more columns of a [table](#table). With indexes, TiDB can quickly locate data without having to search every row in a table every time, which greatly improves your query performance.

There are two common types of indexes:

- **Primary Key**: indexes on the primary key column.
- **Secondary Index**: indexes on non-primary key columns.

> **Note:**
>
> In TiDB, the default definition of **Primary Key** is different from that in [InnoDB](https://mariadb.com/kb/en/innodb/) (a common storage engine of MySQL).
>
> - In InnoDB, the definition of **Primary Key** is unique, not null, and a **clustered index**.
> - In TiDB, the definition of **Primary Key** is unique and not null. But the primary key is not guaranteed to be a **clustered index**. To specify whether the primary key is a clustered index, you can add non-reserved keywords `CLUSTERED` or `NONCLUSTERED` after `PRIMARY KEY` in a `CREATE TABLE` statement. If a statement does not explicitly specify these keywords, the default behavior is controlled by the system variable `@@global.tidb_enable_clustered_index`. For more information, see [Clustered Indexes](/clustered-indexes.md).

#### Specialized indexes

To improve query performance of various user scenarios, TiDB provides you with some specialized types of indexes. For details of each type, see the following links:

- [Expression indexes](/sql-statements/sql-statement-create-index.md#expression-index) (Experimental)
- [Columnar storage (TiFlash)](/tiflash/tiflash-overview.md)
- [RocksDB engine](/storage-engine/rocksdb-overview.md)
- [Titan plugin](/storage-engine/titan-overview.md)
- [Invisible indexes](/sql-statements/sql-statement-add-index.md)
- [Composite `PRIMARY KEY`](/constraints.md#primary-key)
- [Unique indexes](/constraints.md#unique-key)
- [Clustered indexes on integer `PRIMARY KEY`](/constraints.md)
- [Clustered indexes on composite or non-integer key](/constraints.md)

### Other supported logical objects

TiDB supports the following logical objects at the same level as **table**:

- [View](/views.md): a view acts as a virtual table, whose schema is defined by the `SELECT` statement that creates the view.
- [Sequence](/sql-statements/sql-statement-create-sequence.md): a sequence generates and stores sequential data.
- [Temporary table](/temporary-tables.md): a table whose data is not persistent.

## Access Control

TiDB supports both user-based and role-based access control. To allow users to view, modify, or delete data objects and data schemas, you can either grant [privileges](/privilege-management.md) to [users](/user-account-management.md) directly or grant [privileges](/privilege-management.md) to users through [roles](/role-based-access-control.md).

## Database schema changes

As a best practice, it is recommended that you use a [MySQL client](https://dev.mysql.com/doc/refman/8.0/en/mysql.html) or a GUI client instead of a driver or ORM to execute database schema changes.

## Object limitations

This section lists the object limitations on identifier length, a single table, and string types. For more information, see [TiDB Limitations](/tidb-limitations.md).

### Limitations on identifier length

| Identifier type | Maximum length (number of characters allowed) |
|:---------|:--------------|
| Database | 64 |
| Table    | 64 |
| Column   | 64 |
| Index    | 64 |
| View     | 64 |
| Sequence | 64 |

### Limitations on a single table

| Type       | Upper limit (default value)  |
|:----------|:----------|
| Columns   | Defaults to 1017 and can be adjusted up to 4096     |
| Indexes   |  Defaults to 64 and can be adjusted up to 512        |
| Partitions | 8192     |
| Single Line Size | 6 MB by default. You can adjust the size limit via the [**txn-entry-size-limit**](/tidb-configuration-file.md#txn-entry-size-limit-new-in-v50) configuration item. |
| Single Column in a Line Size | 6 MB       |

### Limitations on string types

| Type       | Upper limit   |
|:----------|:----------|
| CHAR       | 256 characters      |
| BINARY     | 256 characters      |
| VARBINARY  | 65535 characters    |
| VARCHAR    | 16383 characters    |
| TEXT       | 6 MB                |
| BLOB       | 6 MB                |

### Number of rows

TiDB supports an **unlimited** number of rows by adding nodes to the cluster. For the relevant principles, see [TiDB Best Practices](/best-practices/tidb-best-practices.md).
