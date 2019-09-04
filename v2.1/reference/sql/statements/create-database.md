---
title: CREATE DATABASE | TiDB SQL Statement Reference
summary: An overview of the usage of CREATE DATABASE for the TiDB database.
category: reference
---

# CREATE DATABASE

This statement creates a new database in TiDB. The MySQL terminology for 'database' most closely maps to a schema in the SQL standard.

## Synopsis

**CreateDatabaseStmt:**

![CreateDatabaseStmt](/media/sqlgram-v2.1/CreateDatabaseStmt.png)

**DatabaseSym:**

![DatabaseSym](/media/sqlgram-v2.1/DatabaseSym.png)

**IfNotExists:**

![IfNotExists](/media/sqlgram-v2.1/IfNotExists.png)

**DBName:**

![DBName](/media/sqlgram-v2.1/DBName.png)

**DatabaseOptionListOpt:**

![DatabaseOptionListOpt](/media/sqlgram-v2.1/DatabaseOptionListOpt.png)

## Syntax

The `CREATE DATABASE` statement is used to create a database, and to specify the default properties of the database, such as the default character set and validation rules. `CREATE SCHEMA` is a synonym for `CREATE DATABASE`.

```sql
CREATE {DATABASE | SCHEMA} [IF NOT EXISTS] db_name
    [create_specification] ...

create_specification:
    [DEFAULT] CHARACTER SET [=] charset_name
  | [DEFAULT] COLLATE [=] collation_name
```

If you create an existing database and does not specify `IF NOT EXISTS`, an error is displayed.

The `create_specification` option is used to specify the specific `CHARACTER SET` and `COLLATE` in the database. Currently, the option is only supported in syntax.

## Examples

```sql
mysql> CREATE DATABASE mynewdatabase;
Query OK, 0 rows affected (0.09 sec)

mysql> USE mynewdatabase;
Database changed
mysql> CREATE TABLE t1 (a int);
Query OK, 0 rows affected (0.11 sec)

mysql> SHOW TABLES;
+-------------------------+
| Tables_in_mynewdatabase |
+-------------------------+
| t1                      |
+-------------------------+
1 row in set (0.00 sec)
```

## MySQL compatibility

This statement is understood to be fully compatible with MySQL. Any compatibility differences should be [reported via an issue](/v2.1/report-issue.md) on GitHub.

## See also

* [USE](/v2.1/reference/sql/statements/use.md)
* [ALTER DATABASE](/v2.1/reference/sql/statements/alter-database.md)
* [DROP DATABASE](/v2.1/reference/sql/statements/drop-database.md)
* [SHOW DATABASES](/v2.1/reference/sql/statements/show-databases.md)
