---
title: Create a Database
summary: Learn steps, rules, and examples to create a database.
---

# Create a Database

This document describes how to create a database using SQL and various programming languages and lists the rules of database creation. In this document, the [Bookshop](/develop/dev-guide-bookshop-schema-design.md) application is taken as an example to walk you through the steps of database creation.

## Before you start

Before creating a database, do the following:

- [Build a TiDB Serverless Cluster](/develop/dev-guide-build-cluster-in-cloud.md).
- Read [Schema Design Overview](/develop/dev-guide-schema-design-overview.md).

## What is database

[Database](/develop/dev-guide-schema-design-overview.md) objects in TiDB contain **tables**, **views**, **sequences**, and other objects.

## Create databases

To create a database, you can use the `CREATE DATABASE` statement.

For example, to create a database named `bookshop` if it does not exist, use the following statement:

```sql
CREATE DATABASE IF NOT EXISTS `bookshop`;
```

For more information and examples of the `CREATE DATABASE` statement, see the [`CREATE DATABASE`](/sql-statements/sql-statement-create-database.md) document.

To execute the library build statement as the `root` user, run the following command:

```shell
mysql
    -u root \
    -h {host} \
    -P {port} \
    -p {password} \
    -e "CREATE DATABASE IF NOT EXISTS bookshop;"
```

## View databases

To view the databases in a cluster, use the [`SHOW DATABASES`](/sql-statements/sql-statement-show-databases.md) statement.

For example:

```shell
mysql
    -u root \
    -h {host} \
    -P {port} \
    -p {password} \
    -e "SHOW DATABASES;"
```

The following is an example output:

```
+--------------------+
| Database           |
+--------------------+
| INFORMATION_SCHEMA |
| PERFORMANCE_SCHEMA |
| bookshop           |
| mysql              |
| test               |
+--------------------+
```

## Rules in database creation

- Follow the [Database Naming Conventions](/develop/dev-guide-object-naming-guidelines.md) and name your database meaningfully.
- TiDB comes with a default database named `test`. However, it is not recommended that you use it in a production environment if you do not have to. You can create your own database using the `CREATE DATABASE` statement and change the current database using the [`USE {databasename};`](/sql-statements/sql-statement-use.md) statement in a SQL session.
- Use the `root` user to create objects such as database, roles, and users. Grant only the necessary privileges to roles and users.
- As a best practice, it is recommended that you use a **MySQL command-line client** or a **MySQL GUI client** instead of a driver or ORM to execute database schema changes.

## Next step

After creating a database, you can add **tables** to it. For more information, see [Create a Table](/develop/dev-guide-create-table.md).
