---
title: SET PASSWORD
summary: TiDB 数据库中 SET PASSWORD 的使用概况。
category: reference
---

# SET PASSWORD

`SET PASSWORD` 语句用于更改 TiDB 系统数据库中的用户密码。

## 语法图

**SetStmt:**

![SetStmt](/media/sqlgram/SetStmt.png)

## 示例

```sql
mysql> SET PASSWORD='test'; -- change my password
Query OK, 0 rows affected (0.01 sec)

mysql> CREATE USER 'newuser' IDENTIFIED BY 'test';
Query OK, 1 row affected (0.00 sec)

mysql> SHOW CREATE USER newuser;
+----------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| CREATE USER for newuser@%                                                                                                                                            |
+----------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| CREATE USER 'newuser'@'%' IDENTIFIED WITH 'mysql_native_password' AS '*94BDCEBE19083CE2A1F959FD02F964C7AF4CFC29' REQUIRE NONE PASSWORD EXPIRE DEFAULT ACCOUNT UNLOCK |
+----------------------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)

mysql> SET PASSWORD FOR newuser = 'test';
Query OK, 0 rows affected (0.01 sec)

mysql> SHOW CREATE USER newuser;
+----------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| CREATE USER for newuser@%                                                                                                                                            |
+----------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| CREATE USER 'newuser'@'%' IDENTIFIED WITH 'mysql_native_password' AS '*94BDCEBE19083CE2A1F959FD02F964C7AF4CFC29' REQUIRE NONE PASSWORD EXPIRE DEFAULT ACCOUNT UNLOCK |
+----------------------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)

mysql> SET PASSWORD FOR newuser = PASSWORD('test'); -- deprecated syntax from earlier MySQL releases
Query OK, 0 rows affected (0.00 sec)

mysql> SHOW CREATE USER newuser;
+----------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| CREATE USER for newuser@%                                                                                                                                            |
+----------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| CREATE USER 'newuser'@'%' IDENTIFIED WITH 'mysql_native_password' AS '*94BDCEBE19083CE2A1F959FD02F964C7AF4CFC29' REQUIRE NONE PASSWORD EXPIRE DEFAULT ACCOUNT UNLOCK |
+----------------------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

## MySQL 兼容性

`SET PASSWORD` 语句与 MySQL 完全兼容。如有任何兼容性差异，请在 GitHub 上提交 [issue](/dev/report-issue.md)。

## 另请参阅

* [CREATE USER](/dev/reference/sql/statements/create-user.md)
* [Privilege Management](/dev/reference/security/privilege-system.md)