---
title: CREATE USER
summary: TiDB 数据库中 CREATE USER 的使用概况。
category: reference
aliases: ['/docs-cn/dev/reference/sql/statements/create-user/']
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

创建一个密码为 `newuserpassword` 的用户。

{{< copyable "sql" >}}

```sql
CREATE USER 'newuser' IDENTIFIED BY 'newuserpassword';
```

```
Query OK, 1 row affected (0.04 sec)
```

创建一个只能在 `192.168.1.1` 登陆的用户，密码为 `newuserpassword`。

{{< copyable "sql" >}}

```sql
CREATE USER 'newuser2'@'192.168.1.1' IDENTIFIED BY 'newuserpassword';
```

```
Query OK, 1 row affected (0.02 sec)
```

创建一个要求在登录时使用 TLS 连接的用户。

{{< copyable "sql" >}}

```sql
CREATE USER 'newuser3'@'%' REQUIRE SSL IDENTIFIED BY 'newuserpassword';
```

```
Query OK, 1 row affected (0.02 sec)
```

创建一个要求在登录时提供指定客户端证书的用户。

{{< copyable "sql" >}}

```sql
CREATE USER 'newuser4'@'%' REQUIRE ISSUER '/C=US/ST=California/L=San Francisco/O=PingCAP' IDENTIFIED BY 'newuserpassword';
```

```
Query OK, 1 row affected (0.02 sec)
```

## MySQL 兼容性

* TiDB 不支持 `WITH MAX_QUERIES_PER_HOUR`、`WITH MAX_UPDATES_PER_HOUR`、`WITH MAX_USER_CONNECTIONS` 等 `CREATE` 选项。
* TiDB 不支持 `DEFAULT ROLE` 选项。
* TiDB 不支持 `PASSWORD EXPIRE`、`PASSWORD HISTORY` 等有关密码限制的 `CREATE` 选项。
* TiDB 不支持 `ACCOUNT LOCK` 和 `ACCOUNT UNLOCK` 选项。
* 对于 TiDB 尚不支持的 `CREATE` 选项。这些选项可被解析，但会被忽略。

## 另请参阅

* [Security Compatibility with MySQL](/security-compatibility-with-mysql.md)
* [DROP USER](/sql-statements/sql-statement-drop-user.md)
* [SHOW CREATE USER](/sql-statements/sql-statement-show-create-user.md)
* [ALTER USER](/sql-statements/sql-statement-alter-user.md)
* [Privilege Management](/privilege-management.md)
