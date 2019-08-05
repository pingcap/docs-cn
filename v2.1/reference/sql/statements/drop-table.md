---
title: DROP TABLE | TiDB SQL Statement Reference
summary: An overview of the usage of DROP TABLE for the TiDB database.
category: reference
---

# DROP TABLE

This statement drops a table from the currently selected database. An error is returned if the table does not exist, unless the `IF EXISTS` modifier is used.

By design `DROP TABLE` will also drop views, as they share the same namespace as tables.

## Synopsis

**DropTableStmt:**

![DropTableStmt](/media/sqlgram-v2.1/DropTableStmt.png)

**TableOrTables:**

![TableOrTables](/media/sqlgram-v2.1/TableOrTables.png)

**TableNameList:**

![TableNameList](/media/sqlgram-v2.1/TableNameList.png)

## Examples

```sql
mysql> CREATE TABLE t1 (a INT);
Query OK, 0 rows affected (0.11 sec)

mysql> DROP TABLE t1;
Query OK, 0 rows affected (0.22 sec)

mysql> DROP TABLE table_not_exists;
ERROR 1051 (42S02): Unknown table 'test.table_not_exists'
mysql> DROP TABLE IF EXISTS table_not_exists;
Query OK, 0 rows affected (0.01 sec)

mysql> CREATE VIEW v1 AS SELECT 1;
Query OK, 0 rows affected (0.10 sec)

mysql> DROP TABLE v1;
Query OK, 0 rows affected (0.23 sec)
```

## MySQL compatibility

* Dropping a table with `IF EXISTS` does not return a warning when attempting to drop a table that does not exist. [Issue #7867](https://github.com/pingcap/tidb/issues/7867)

## See also

* [DROP VIEW](/reference/sql/statements/drop-view.md)
* [CREATE TABLE](/reference/sql/statements/create-table.md)
* [SHOW CREATE TABLE](/reference/sql/statements/show-create-table.md)
* [SHOW TABLES](/reference/sql/statements/show-tables.md)
