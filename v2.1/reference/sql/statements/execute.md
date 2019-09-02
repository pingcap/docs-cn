---
title: EXECUTE
summary: TiDB 数据库中 EXECUTE 的使用概况。
category: reference
---

# EXECUTE

`EXECUTE` 语句为服务器端预处理语句提供 SQL 接口。

## 语法图

**ExecuteStmt:**

![ExecuteStmt](/media/sqlgram/ExecuteStmt.png)

**Identifier:**

![Identifier](/media/sqlgram/Identifier.png)

## 示例

```sql
mysql> PREPARE mystmt FROM 'SELECT ? as num FROM DUAL';
Query OK, 0 rows affected (0.00 sec)

mysql> SET @number = 5;
Query OK, 0 rows affected (0.00 sec)

mysql> EXECUTE mystmt USING @number;
+------+
| num  |
+------+
| 5    |
+------+
1 row in set (0.00 sec)

mysql> DEALLOCATE PREPARE mystmt;
Query OK, 0 rows affected (0.00 sec)
```

## MySQL 兼容性

`EXECUTE` 语句与 MySQL 完全兼容。如有任何兼容性差异，请在 GitHub 上提交 [issue](/v2.1/report-issue.md)。

## 另请参阅

* [PREPARE](/v2.1/reference/sql/statements/prepare.md)
* [DEALLOCATE](/v2.1/reference/sql/statements/deallocate.md)