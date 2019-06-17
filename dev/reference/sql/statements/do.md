---
title: DO | TiDB SQL Statement Reference
summary: TiDB 数据库中 DO 的使用概况。
category: reference
---

# DO

`DO` 语句用于执行表达式，而不返回结果。在 MySQL 中，`DO` 的一个常见用例是执行存储的程序，而无需处理结果。但是 TiDB 不提供存储例程，因此该功能的使用较为受限。

## 语法图

**DoStmt:**

![DoStmt](/media/sqlgram/DoStmt.png)

**ExpressionList:**

![ExpressionList](/media/sqlgram/ExpressionList.png)

**Expression:**

![Expression](/media/sqlgram/Expression.png)

## 示例

```sql
mysql> SELECT SLEEP(5);
+----------+
| SLEEP(5) |
+----------+
|        0 |
+----------+
1 row in set (5.00 sec)

mysql> DO SLEEP(5);
Query OK, 0 rows affected (5.00 sec)

mysql> DO SLEEP(1), SLEEP(1.5);
Query OK, 0 rows affected (2.50 sec)
```

## MySQL 兼容性

`DO` 语句与 MySQL 完全兼容。如有任何兼容性差异，请在 GitHub 上 提交 [issue](/report-issue.md)。

## 另请参阅

* [SELECT](/dev/reference/sql/statements/select.md)
