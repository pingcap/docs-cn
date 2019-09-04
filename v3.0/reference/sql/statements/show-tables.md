---
title: SHOW [FULL] TABLES
summary: TiDB 数据库中 SHOW [FULL] TABLES 的使用概况。
category: reference
---

# SHOW [FULL] TABLES

`SHOW [FULL] TABLES` 语句用于显示当前所选数据库中表和视图的列表。可选关键字 `FULL` 说明表的类型是 `BASE TABLE` 还是 `VIEW`。

若要在不同的数据库中显示表，可使用 `SHOW TABLES IN DatabaseName` 语句。

## 语法图

**ShowStmt:**

![ShowStmt](/media/sqlgram/ShowStmt.png)

**ShowTargetFilterable:**

![ShowTargetFilterable](/media/sqlgram/ShowTargetFilterable.png)

**ShowDatabaseNameOpt:**

![ShowDatabaseNameOpt](/media/sqlgram/ShowDatabaseNameOpt.png)

## 示例

```sql
mysql> CREATE TABLE t1 (a int);
Query OK, 0 rows affected (0.12 sec)

mysql> CREATE VIEW v1 AS SELECT 1;
Query OK, 0 rows affected (0.10 sec)

mysql> SHOW TABLES;
+----------------+
| Tables_in_test |
+----------------+
| t1             |
| v1             |
+----------------+
2 rows in set (0.00 sec)

mysql> SHOW FULL TABLES;
+----------------+------------+
| Tables_in_test | Table_type |
+----------------+------------+
| t1             | BASE TABLE |
| v1             | VIEW       |
+----------------+------------+
2 rows in set (0.00 sec)

mysql> SHOW TABLES IN mysql;
+----------------------+
| Tables_in_mysql      |
+----------------------+
| GLOBAL_VARIABLES     |
| bind_info            |
| columns_priv         |
| db                   |
| default_roles        |
| gc_delete_range      |
| gc_delete_range_done |
| help_topic           |
| role_edges           |
| stats_buckets        |
| stats_feedback       |
| stats_histograms     |
| stats_meta           |
| tables_priv          |
| tidb                 |
| user                 |
+----------------------+
16 rows in set (0.00 sec)
```

## MySQL 兼容性

`SHOW [FULL] TABLES` 语句与 MySQL 完全兼容。如有任何兼容性差异，请在 GitHub 上提交 [issue](/v3.0/report-issue.md)。

## 另请参阅

* [CREATE TABLE](/v3.0/reference/sql/statements/create-table.md)
* [DROP TABLE](/v3.0/reference/sql/statements/drop-table.md)
* [SHOW CREATE TABLE](/v3.0/reference/sql/statements/show-create-table.md)