---
title: Explore SQL with TiDB
summary: Learn about the basic SQL statements for the TiDB database.
aliases: ['/docs/dev/basic-sql-operations/','/docs/dev/how-to/get-started/explore-sql/']
---

# Explore SQL with TiDB

TiDB is compatible with MySQL, you can use MySQL statements directly in most of the cases. For unsupported features, see [Compatibility with MySQL](/mysql-compatibility.md#unsupported-features).

To experiment with SQL and test out TiDB compatibility with MySQL queries, you can [run TiDB directly in your web browser without installing it](https://tour.tidb.io/). You can also first deploy a TiDB cluster and then run SQL statements in it.

This page walks you through the basic TiDB SQL statements such as DDL, DML and CRUD operations. For a complete list of TiDB statements, see [TiDB SQL Syntax Diagram](https://pingcap.github.io/sqlgram/).

## Category

SQL is divided into the following 4 types according to their functions:

- DDL (Data Definition Language): It is used to define database objects, including databases, tables, views, and indexes.

- DML (Data Manipulation Language): It is used to manipulate application related records.

- DQL (Data Query Language): It is used to query the records after conditional filtering.

- DCL (Data Control Language): It is used to define access privileges and security levels.

Common DDL features are creating, modifying, and deleting objects (such as tables and indexes). The corresponding commands are `CREATE`, `ALTER`, and `DROP`.

## Show, create and drop a database

A database in TiDB can be considered as a collection of objects such as tables and indexes.

To show the list of databases, use the `SHOW DATABASES` statement:

{{< copyable "sql" >}}

```sql
SHOW DATABASES;
```

To use the database named `mysql`, use the following statement:

{{< copyable "sql" >}}

```sql
USE mysql;
```

To show all the tables in a database, use the `SHOW TABLES` statement:

{{< copyable "sql" >}}

```sql
SHOW TABLES FROM mysql;
```

To create a database, use the `CREATE DATABASE` statement:

{{< copyable "sql" >}}

```sql
CREATE DATABASE db_name [options];
```

To create a database named `samp_db`, use the following statement:

{{< copyable "sql" >}}

```sql
CREATE DATABASE IF NOT EXISTS samp_db;
```

Add `IF NOT EXISTS` to prevent an error if the database exists.

To delete a database, use the `DROP DATABASE` statement:

{{< copyable "sql" >}}

```sql
DROP DATABASE samp_db;
```

## Create, show, and drop a table

To create a table, use the `CREATE TABLE` statement:

{{< copyable "sql" >}}

```sql
CREATE TABLE table_name column_name data_type constraint;
```

For example, to create a table named `person` which includes fields such as number, name, and birthday, use the following statement:

{{< copyable "sql" >}}

```sql
CREATE TABLE person (
    id INT(11),
    name VARCHAR(255),
    birthday DATE
    );
```

To view the statement that creates the table (DDL), use the `SHOW CREATE` statement:

{{< copyable "sql" >}}

```sql
SHOW CREATE table person;
```

To delete a table, use the `DROP TABLE` statement:

{{< copyable "sql" >}}

```sql
DROP TABLE person;
```

## Create, show, and drop an index

Indexes are used to speed up queries on indexed columns. To create an index for the column whose value is not unique, use the `CREATE INDEX` statement:

{{< copyable "sql" >}}

```sql
CREATE INDEX person_id ON person (id);
```

Or use the `ALTER TABLE` statement:

{{< copyable "sql" >}}

```sql
ALTER TABLE person ADD INDEX person_id (id);
```

To create a unique index for the column whose value is unique, use the `CREATE UNIQUE INDEX` statement:

{{< copyable "sql" >}}

```sql
CREATE UNIQUE INDEX person_unique_id ON person (id);
```

Or use the `ALTER TABLE` statement:

{{< copyable "sql" >}}

```sql
ALTER TABLE person ADD UNIQUE person_unique_id (id);
```

To show all the indexes in a table, use the `SHOW INDEX` statement:

{{< copyable "sql" >}}

```sql
SHOW INDEX FROM person;
```

To delete an index, use the `DROP INDEX` or `ALTER TABLE` statement. `DROP INDEX` can be nested in `ALTER TABLE`:

{{< copyable "sql" >}}

```sql
DROP INDEX person_id ON person;
```

{{< copyable "sql" >}}

```sql
ALTER TABLE person DROP INDEX person_unique_id;
```

> **Note:**
> 
> DDL operations are not transactions. You don't need to run a `COMMIT` statement when executing DDL operations.

## Insert, update, and delete data

Common DML features are adding, modifying, and deleting table records. The corresponding commands are `INSERT`, `UPDATE`, and `DELETE`.

To insert data into a table, use the `INSERT` statement:

{{< copyable "sql" >}}

```sql
INSERT INTO person VALUES(1,'tom','20170912');
```

To insert a record containing data of some fields into a table, use the `INSERT` statement:

{{< copyable "sql" >}}

```sql
INSERT INTO person(id,name) VALUES('2','bob');
```

To update some fields of a record in a table, use the `UPDATE` statement:

{{< copyable "sql" >}}

```sql
UPDATE person SET birthday='20180808' WHERE id=2;
```

To delete the data in a table, use the `DELETE` statement:

{{< copyable "sql" >}}

```sql
DELETE FROM person WHERE id=2;
```

> **Note:**
> 
> The `UPDATE` and `DELETE` statements without the `WHERE` clause as a filter operate on the entire table.

## Query data

DQL is used to retrieve the desired data rows from a table or multiple tables.

To view the data in a table, use the `SELECT` statement:

{{< copyable "sql" >}}

```sql
SELECT * FROM person;
```

To query a specific column, add the column name after the `SELECT` keyword:

{{< copyable "sql" >}}

```sql
SELECT name FROM person;
+------+
| name |
+------+
| tom  |
+------+
```

Use the `WHERE` clause to filter all records that match the conditions and then return the result:

{{< copyable "sql" >}}

```sql
SELECT * FROM person where id<5;
```

## Create, authorize, and delete a user

DCL are usually used to create or delete users, and manage user privileges.

To create a user, use the `CREATE USER` statement. The following example creates a user named `tiuser` with the password `123456`:

{{< copyable "sql" >}}

```sql
CREATE USER 'tiuser'@'localhost' IDENTIFIED BY '123456';
```

To grant `tiuser` the privilege to retrieve the tables in the `samp_db` database:

{{< copyable "sql" >}}

```sql
GRANT SELECT ON samp_db.* TO 'tiuser'@'localhost';
```

To check the privileges of `tiuser`:

{{< copyable "sql" >}}

```sql
SHOW GRANTS for tiuser@localhost;
```

To delete `tiuser`:

{{< copyable "sql" >}}

```sql
DROP USER 'tiuser'@'localhost';
```
