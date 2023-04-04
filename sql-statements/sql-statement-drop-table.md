---
title: DROP TABLE | TiDB SQL Statement Reference
summary: An overview of the usage of DROP TABLE for the TiDB database.
aliases: ['/docs/dev/sql-statements/sql-statement-drop-table/','/docs/dev/reference/sql/statements/drop-table/']
---

# DROP TABLE

This statement drops a table from the currently selected database. An error is returned if the table does not exist, unless the `IF EXISTS` modifier is used.

## Synopsis

```ebnf+diagram
DropTableStmt ::=
    'DROP' OptTemporary TableOrTables IfExists TableNameList RestrictOrCascadeOpt

OptTemporary ::=
    ( 'TEMPORARY' | ('GLOBAL' 'TEMPORARY') )?

TableOrTables ::=
    'TABLE'
|   'TABLES'

TableNameList ::=
    TableName ( ',' TableName )*
```

## Drop temporary tables

You can use the following syntax to drop ordinary tables and temporary tables:

- Use `DROP TEMPORARY TABLE` to drop local temporary tables.
- Use `DROP GLOBAL TEMPORARY TABLE` to drop global temporary tables.
- Use `DROP TABLE` to drop ordinary tables or temporary tables.

## Examples

```sql
mysql> CREATE TABLE t1 (a INT);
Query OK, 0 rows affected (0.11 sec)

mysql> DROP TABLE t1;
Query OK, 0 rows affected (0.22 sec)

mysql> DROP TABLE table_not_exists;
ERROR 1051 (42S02): Unknown table 'test.table_not_exists'

mysql> DROP TABLE IF EXISTS table_not_exists;
Query OK, 0 rows affected, 1 warning (0.01 sec)

mysql> SHOW WARNINGS;
+-------+------+---------------------------------------+
| Level | Code | Message                               |
+-------+------+---------------------------------------+
| Note  | 1051 | Unknown table 'test.table_not_exists' |
+-------+------+---------------------------------------+
1 row in set (0.01 sec)

mysql> CREATE VIEW v1 AS SELECT 1;
Query OK, 0 rows affected (0.10 sec)

mysql> DROP TABLE v1;
Query OK, 0 rows affected (0.23 sec)
```

## MySQL compatibility

Currently, `RESTRICT` and `CASCADE` are only supported syntactically.

## See also

* [CREATE TABLE](/sql-statements/sql-statement-create-table.md)
* [SHOW CREATE TABLE](/sql-statements/sql-statement-show-create-table.md)
* [SHOW TABLES](/sql-statements/sql-statement-show-tables.md)
