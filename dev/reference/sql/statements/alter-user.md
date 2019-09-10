---
title: ALTER USER
summary: TiDB 数据库中 ALTER USER 的使用概况。
category: reference
---

# ALTER USER

`ALTER USER` 语句用于更改 TiDB 权限系统内的已有用户。和 MySQL 一样，在 TiDB 权限系统中，用户是用户名和用户名所连接主机的组合。因此，可创建一个用户 `'newuser2'@'192.168.1.1'`，使其只能通过 IP 地址 `192.168.1.1` 进行连接。相同的用户名从不同主机登录时可能会拥有不同的权限。

## 语法图

**AlterUserStmt:**

![AlterUserStmt](/media/sqlgram/AlterUserStmt.png)

**UserSpecList:**

![UserSpecList](/media/sqlgram/UserSpecList.png)

**UserSpec:**

![UserSpec](/media/sqlgram/UserSpec.png)

## 示例

```sql
mysql> CREATE USER 'newuser' IDENTIFIED BY 'newuserpassword';
Query OK, 1 row affected (0.01 sec)

mysql> SHOW CREATE USER 'newuser';
+----------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| CREATE USER for newuser@%                                                                                                                                            |
+----------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| CREATE USER 'newuser'@'%' IDENTIFIED WITH 'mysql_native_password' AS '*5806E04BBEE79E1899964C6A04D68BCA69B1A879' REQUIRE NONE PASSWORD EXPIRE DEFAULT ACCOUNT UNLOCK |
+----------------------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)

mysql> ALTER USER 'newuser' IDENTIFIED BY 'newnewpassword';
Query OK, 0 rows affected (0.02 sec)

mysql> SHOW CREATE USER 'newuser';
+----------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| CREATE USER for newuser@%                                                                                                                                            |
+----------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| CREATE USER 'newuser'@'%' IDENTIFIED WITH 'mysql_native_password' AS '*FB8A1EA1353E8775CA836233E367FBDFCB37BE73' REQUIRE NONE PASSWORD EXPIRE DEFAULT ACCOUNT UNLOCK |
+----------------------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

## MySQL 兼容性

* 在 MySQL 中，`ALTER` 语句用于更改属性，例如使密码失效。但 TiDB 尚不支持此功能。

## 另请参阅

* [Security Compatibility with MySQL](/dev/reference/security/compatibility.md)
* [CREATE USER](/dev/reference/sql/statements/create-user.md)
* [DROP USER](/dev/reference/sql/statements/drop-user.md)
* [SHOW CREATE USER](/dev/reference/sql/statements/show-create-user.md)
