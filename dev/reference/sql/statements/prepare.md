---
title: PREPARE
summary: TiDB 数据库中 PREPARE 的使用概况。
category: reference
aliases: ['/docs-cn/sql/prepare/']
---

# PREPARE

`PREPARE` 语句为服务器端预处理语句提供 SQL 接口。

## 语法图

**PreparedStmt:**

![PreparedStmt](/media/sqlgram/PreparedStmt.png)

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

`PREPARE` 语句与 MySQL 完全兼容。如有任何兼容性差异，请在 GitHub 上 提交 [issue](/report-issue.md)。

## 另请参阅

* [EXECUTE](/dev/reference/sql/statements/execute.md)
* [DEALLOCATE](/dev/reference/sql/statements/deallocate.md)
