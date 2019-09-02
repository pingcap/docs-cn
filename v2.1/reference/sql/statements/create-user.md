---
title: CREATE USER
summary: TiDB 数据库中 CREATE USER 的使用概况。
category: reference
---

# CREATE USER

`CREATE USER` 语句用于创建带有指定密码的新用户。和 MySQL 一样，在 TiDB 权限系统中，用户是用户名和用户名所连接主机的组合。因此，可创建一个用户 `'newuser2'@'192.168.1.1'`，使其只能通过 IP 地址 `192.168.1.1` 进行连接。相同的用户名从不同主机登录时可能会拥有不同的权限。

## 语法图

**CreateUserStmt:**

![CreateUserStmt](/media/sqlgram/CreateUserStmt.png)

**IfNotExists:**

![IfNotExists](/media/sqlgram/IfNotExists.png)

**UserSpecList:**

![UserSpecList](/media/sqlgram/UserSpecList.png)

**UserSpec:**

![UserSpec](/media/sqlgram/UserSpec.png)

**AuthOption:**

![AuthOption](/media/sqlgram/AuthOption.png)

**StringName:**

![StringName](/media/sqlgram/StringName.png)

## 示例

```sql
mysql> CREATE USER 'newuser' IDENTIFIED BY 'newuserpassword';
Query OK, 1 row affected (0.04 sec)

mysql> CREATE USER 'newuser2'@'192.168.1.1' IDENTIFIED BY 'newuserpassword';
Query OK, 1 row affected (0.02 sec)
```

## MySQL 兼容性

* TiDB 尚不支持若干 `CREATE` 选项。这些选项可被解析，但会被忽略。

## 另请参阅

* [Security Compatibility with MySQL](v2.1/reference/security/compatibility.md)
* [DROP USER](v2.1/reference/sql/statements/drop-user.md)
* [SHOW CREATE USER](v2.1/reference/sql/statements/show-create-user.md)
* [ALTER USER](v2.1/reference/sql/statements/alter-user.md)
* [Privilege Management](v2.1/reference/security/privilege-system.md)