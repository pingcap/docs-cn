---
title: CREATE TABLE | TiDB SQL Statement Reference 
summary: An overview of the usage of CREATE TABLE for the TiDB database.
category: reference
aliases: ['/docs/sql/ddl/']
---

# CREATE TABLE 

This statement creates a new table in the currently selected database. See also `CREATE TABLE AS`, which is documented separately.

## Synopsis

**CreateTableStmt:**

![CreateTableStmt](/media/sqlgram/CreateTableStmt.png)

**IfNotExists:**

![IfNotExists](/media/sqlgram/IfNotExists.png)

**TableName:**

![TableName](/media/sqlgram/TableName.png)

**TableElementListOpt:**

![TableElementListOpt](/media/sqlgram/TableElementListOpt.png)

**TableElement:**

![TableElement](/media/sqlgram/TableElement.png)

**PartitionOpt:**

![PartitionOpt](/media/sqlgram/PartitionOpt.png)

**ColumnDef:**

![ColumnDef](/media/sqlgram/ColumnDef.png)

**ColumnName:**

![ColumnName](/media/sqlgram/ColumnName.png)

**Type:**

![Type](/media/sqlgram/Type.png)

**ColumnOptionListOpt:**

![ColumnOptionListOpt](/media/sqlgram/ColumnOptionListOpt.png)

**TableOptionListOpt:**

![TableOptionListOpt](/media/sqlgram/TableOptionListOpt.png)

## Examples

```sql
mysql> CREATE TABLE t1 (a int);
Query OK, 0 rows affected (0.11 sec)

mysql> CREATE TABLE t2 LIKE t1;
Query OK, 0 rows affected (0.10 sec)

mysql> DESC t1;
+-------+---------+------+------+---------+-------+
| Field | Type    | Null | Key  | Default | Extra |
+-------+---------+------+------+---------+-------+
| a     | int(11) | YES  |      | NULL    |       |
+-------+---------+------+------+---------+-------+
1 row in set (0.00 sec)

mysql> INSERT INTO t1 VALUES (1);
Query OK, 1 row affected (0.02 sec)

mysql> SELECT * FROM t1;
+------+
| a    |
+------+
|    1 |
+------+
1 row in set (0.00 sec)
```

## MySQL compatibility

* TiDB does not support the syntax `CREATE TEMPORARY TABLE`.
* All of the data types except spatial types are supported.
* `FULLTEXT`, `HASH` and `SPATIAL` indexes are not supported.
* The `KEY_BLOCK_SIZE` and `ENGINE` attributes are parsed but ignored.
* The `index_col_name` attribute supports the length option with a maximum length limit of 3072 bytes. The length limit does not change depending on the storage engine, and character set used when building the table.
* The `index_col_name` attribute supports the index sorting options of `ASC` and `DESC`
* The `COMMENT` attribute supports a maximum of 1024 characters and does not support the `WITH PARSER` option.
* TiDB supports at most 512 columns in a single table. The corresponding number limit in InnoDB is 1017, and the hard limit in MySQL is 4096.

## See also

* [DROP TABLE](/dev/reference/sql/statements/drop-table.md)
* [CREATE TABLE LIKE](/dev/reference/sql/statements/create-table-like.md)
* [SHOW CREATE TABLE](/dev/reference/sql/statements/show-create-table.md)
