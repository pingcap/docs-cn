---
title: SHOW TABLE STATUS | TiDB SQL Statement Reference
summary: An overview of the usage of SHOW TABLE STATUS for the TiDB database.
category: reference
---

# SHOW TABLE STATUS

This statement shows various statistics about tables in TiDB. If the statistics appear out of date, it is recommended to run [`ANALYZE TABLE`](/dev/reference/sql/statements/analyze-table.md).

## Synopsis

**ShowStmt:**

![ShowStmt](/media/sqlgram-dev/ShowStmt.png)

**ShowTargetFilterable:**

![ShowTargetFilterable](/media/sqlgram-dev/ShowTargetFilterable.png)

**ShowDatabaseNameOpt:**

![ShowDatabaseNameOpt](/media/sqlgram-dev/ShowDatabaseNameOpt.png)

## Examples

```sql
mysql> CREATE TABLE t1 (id INT NOT NULL PRIMARY KEY auto_increment, c1 INT NOT NULL);
Query OK, 0 rows affected (0.11 sec)

mysql> INSERT INTO t1 (c1) VALUES (1),(2),(3),(4),(5);
Query OK, 5 rows affected (0.02 sec)
Records: 5  Duplicates: 0  Warnings: 0

mysql> SHOW TABLE STATUS LIKE 't1'\G
*************************** 1. row ***************************
           Name: t1
         Engine: InnoDB
        Version: 10
     Row_format: Compact
           Rows: 0
 Avg_row_length: 0
    Data_length: 0
Max_data_length: 0
   Index_length: 0
      Data_free: 0
 Auto_increment: 30001
    Create_time: 2019-04-19 08:32:06
    Update_time: NULL
     Check_time: NULL
      Collation: utf8mb4_bin
       Checksum:
 Create_options:
        Comment:
1 row in set (0.00 sec)

mysql> analyze table t1;
Query OK, 0 rows affected (0.12 sec)

mysql> SHOW TABLE STATUS LIKE 't1'\G
*************************** 1. row ***************************
           Name: t1
         Engine: InnoDB
        Version: 10
     Row_format: Compact
           Rows: 5
 Avg_row_length: 16
    Data_length: 80
Max_data_length: 0
   Index_length: 0
      Data_free: 0
 Auto_increment: 30001
    Create_time: 2019-04-19 08:32:06
    Update_time: NULL
     Check_time: NULL
      Collation: utf8mb4_bin
       Checksum:
 Create_options:
        Comment:
1 row in set (0.00 sec)
```

## MySQL compatibility

This statement is understood to be fully compatible with MySQL. Any compatibility differences should be [reported via an issue](/dev/report-issue.md) on GitHub.

## See also

* [SHOW TABLES](/dev/reference/sql/statements/show-tables.md)
* [CREATE TABLE](/dev/reference/sql/statements/create-table.md)
* [DROP TABLE](/dev/reference/sql/statements/drop-table.md)
* [SHOW CREATE TABLE](/dev/reference/sql/statements/show-create-table.md)
