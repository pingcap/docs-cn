---
title: RENAME TABLE
summary: TiDB 数据库中 RENAME TABLE 的使用概况。
category: reference
---

# RENAME TABLE

`RENAME TABLE` 语句用于对已有表进行重命名。

## 语法图

**RenameTableStmt:**

![RenameTableStmt](/media/sqlgram/RenameTableStmt.png)

**TableToTable:**

![TableToTable](/media/sqlgram/TableToTable.png)

## 示例

```sql
mysql> CREATE TABLE t1 (a int);
Query OK, 0 rows affected (0.12 sec)

mysql> SHOW TABLES;
+----------------+
| Tables_in_test |
+----------------+
| t1             |
+----------------+
1 row in set (0.00 sec)

mysql> RENAME TABLE t1 TO t2;
Query OK, 0 rows affected (0.08 sec)

mysql> SHOW TABLES;
+----------------+
| Tables_in_test |
+----------------+
| t2             |
+----------------+
1 row in set (0.00 sec)
```

## MySQL 兼容性

`RENAME TABLE` 语句与 MySQL 完全兼容。如有任何兼容性差异，请在 GitHub 上提交 [issue](/v3.0/report-issue.md)。

## 另请参阅

* [CREATE TABLE](/v3.0/reference/sql/statements/create-table.md)
* [SHOW TABLES](/v3.0/reference/sql/statements/show-tables.md)
* [ALTER TABLE](/v3.0/reference/sql/statements/alter-table.md)