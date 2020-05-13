---
title: SHOW CREATE TABLE
summary: TiDB 数据库中 SHOW CREATE TABLE 的使用概况。
category: reference
---

# SHOW CREATE TABLE

`SHOW CREATE TABLE` 语句用于显示用 SQL 重新创建已有表的确切语句。

## 语法图

**ShowStmt:**

![ShowStmt](/media/sqlgram/ShowStmt.png)

**TableName:**

![TableName](/media/sqlgram/TableName.png)

## 示例

{{< copyable "sql" >}}

```sql
CREATE TABLE t1 (a INT);
```

```
Query OK, 0 rows affected (0.12 sec)
```

{{< copyable "sql" >}}

```sql
SHOW CREATE TABLE t1;
```

```
+-------+------------------------------------------------------------------------------------------------------------+
| Table | Create Table                                                                                               |
+-------+------------------------------------------------------------------------------------------------------------+
| t1    | CREATE TABLE `t1` (
  `a` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin |
+-------+------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

## MySQL 兼容性

`SHOW CREATE TABLE` 语句与 MySQL 完全兼容。如有任何兼容性差异，请在 GitHub 上提交 [issue](/report-issue.md)。

## 另请参阅

* [CREATE TABLE](/reference/sql/statements/create-table.md)
* [DROP TABLE](/reference/sql/statements/drop-table.md)
* [SHOW TABLES](/reference/sql/statements/show-tables.md)
* [SHOW COLUMNS FROM](/reference/sql/statements/show-columns-from.md)
