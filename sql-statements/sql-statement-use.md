---
title: USE | TiDB SQL Statement Reference
summary: An overview of the usage of USE for the TiDB database.
aliases: ['/docs/dev/sql-statements/sql-statement-use/','/docs/dev/reference/sql/statements/use/']
---

# USE

The `USE` statement selects a current database for the user session.

## Synopsis

**UseStmt:**

![UseStmt](/media/sqlgram/UseStmt.png)

**DBName:**

![DBName](/media/sqlgram/DBName.png)

## Examples

```sql
mysql> USE mysql;
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Database changed
mysql> SHOW TABLES;
+-------------------------+
| Tables_in_mysql         |
+-------------------------+
| GLOBAL_VARIABLES        |
| bind_info               |
| columns_priv            |
| db                      |
| default_roles           |
| expr_pushdown_blacklist |
| gc_delete_range         |
| gc_delete_range_done    |
| global_priv             |
| help_topic              |
| opt_rule_blacklist      |
| role_edges              |
| stats_buckets           |
| stats_feedback          |
| stats_histograms        |
| stats_meta              |
| stats_top_n             |
| tables_priv             |
| tidb                    |
| user                    |
+-------------------------+
20 rows in set (0.01 sec)

mysql> CREATE DATABASE newtest;
Query OK, 0 rows affected (0.10 sec)

mysql> USE newtest;
Database changed
mysql> SHOW TABLES;
Empty set (0.00 sec)

mysql> CREATE TABLE t1 (a int);
Query OK, 0 rows affected (0.10 sec)

mysql> SHOW TABLES;
+-------------------+
| Tables_in_newtest |
+-------------------+
| t1                |
+-------------------+
1 row in set (0.00 sec)
```

## MySQL compatibility

In TiDB 2.0 versions, you can use `USE` statements to access any database. In TiDB 3.0 or later versions, TiDB checks whether you have the privilege to access the database when you use `USE` statements.

Currently, `USE` statements are understood to be fully compatible with MySQL. Any compatibility differences should be [reported via an issue](/report-issue.md) on GitHub.

## See also

* [CREATE DATABASE](/sql-statements/sql-statement-create-database.md)
* [SHOW TABLES](/sql-statements/sql-statement-show-tables.md)
