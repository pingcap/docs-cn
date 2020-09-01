---
title: SET PASSWORD
summary: TiDB 数据库中 SET PASSWORD 的使用概况。
aliases: ['/docs-cn/v2.1/sql-statements/sql-statement-set-password/','/docs-cn/v2.1/reference/sql/statements/set-password/']
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

mysql> SELECT USER, HOST, PASSWORD FROM mysql.`user`  WHERE USER = 'newuser';
+---------+------+-------------------------------------------+
| USER    | HOST | PASSWORD                                  |
+---------+------+-------------------------------------------+
| newuser | %    | *94BDCEBE19083CE2A1F959FD02F964C7AF4CFC29 |
+---------+------+-------------------------------------------+
1 row in set (0.00 sec)

mysql> SET PASSWORD FOR newuser = 'test';
Query OK, 0 rows affected (0.01 sec)

mysql> SELECT USER, HOST, PASSWORD FROM mysql.`user`  WHERE USER = 'newuser';
+---------+------+-------------------------------------------+
| USER    | HOST | PASSWORD                                  |
+---------+------+-------------------------------------------+
| newuser | %    | *94BDCEBE19083CE2A1F959FD02F964C7AF4CFC29 |
+---------+------+-------------------------------------------+
1 row in set (0.00 sec)

mysql> SET PASSWORD FOR newuser = PASSWORD('test'); -- deprecated syntax from earlier MySQL releases
Query OK, 0 rows affected (0.00 sec)

mysql> SELECT USER, HOST, PASSWORD FROM mysql.`user`  WHERE USER = 'newuser';
+---------+------+-------------------------------------------+
| USER    | HOST | PASSWORD                                  |
+---------+------+-------------------------------------------+
| newuser | %    | *94BDCEBE19083CE2A1F959FD02F964C7AF4CFC29 |
+---------+------+-------------------------------------------+
1 row in set (0.00 sec)
```

## MySQL 兼容性

`SET PASSWORD` 语句与 MySQL 完全兼容。如发现任何兼容性差异，请在 GitHub 上提交 [issue](https://github.com/pingcap/tidb/issues/new/choose)。

## 另请参阅

* [CREATE USER](/sql-statements/sql-statement-create-user.md)
* [Privilege Management](/privilege-management.md)
