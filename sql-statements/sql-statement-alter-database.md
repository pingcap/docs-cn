---
title: ALTER DATABASE | TiDB SQL Statement Reference
summary: An overview of the usage of ALTER DATABASE for the TiDB database.
aliases: ['/docs/dev/sql-statements/sql-statement-alter-database/','/docs/dev/reference/sql/statements/alter-database/']
---

# ALTER DATABASE

`ALTER DATABASE` is used to specify or modify the default character set and collation of the current database. `ALTER SCHEMA` has the same effect as `ALTER DATABASE`.

## Synopsis

```ebnf+diagram
AlterDatabaseStmt ::=
    'ALTER' 'DATABASE' DBName? DatabaseOptionList

DatabaseOption ::=
    DefaultKwdOpt ( CharsetKw '='? CharsetName | 'COLLATE' '='? CollationName | 'ENCRYPTION' '='? EncryptionOpt )
```

## Examples

Modify the test database schema to use the utf8mb4 character set:

{{< copyable "sql" >}}

```sql
ALTER DATABASE test DEFAULT CHARACTER SET = utf8mb4;
```

```sql
Query OK, 0 rows affected (0.00 sec)
```

Currently, TiDB only supports some character sets and collations. See [Character Set and Collation Support](/character-set-and-collation.md) for details.

## MySQL compatibility

The `ALTER DATABASE` statement in TiDB is fully compatible with MySQL. If you find any compatibility differences, [report a bug](https://docs.pingcap.com/tidb/stable/support).

## See also

* [CREATE DATABASE](/sql-statements/sql-statement-create-database.md)
* [SHOW DATABASES](/sql-statements/sql-statement-show-databases.md)
