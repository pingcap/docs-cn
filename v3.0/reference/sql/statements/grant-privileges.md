---
title: GRANT <privileges>
summary: TiDB 数据库中 GRANT <privileges> 的使用概况。
category: reference
---

# GRANT <privileges>

`GRANT <privileges>` 语句用于为 TiDB 中已存在的用户分配权限。TiDB 中的权限系统同 MySQL 一样，都基于数据库/表模式来分配凭据。

## 语法图

**GrantStmt:**

![GrantStmt](/media/sqlgram/GrantStmt.png)

**PrivElemList:**

![PrivElemList](/media/sqlgram/PrivElemList.png)

**PrivElem:**

![PrivElem](/media/sqlgram/PrivElem.png)

**PrivType:**

![PrivType](/media/sqlgram/PrivType.png)

**ObjectType:**

![ObjectType](/media/sqlgram/ObjectType.png)

**PrivLevel:**

![PrivLevel](/media/sqlgram/PrivLevel.png)

**UserSpecList:**

![UserSpecList](/media/sqlgram/UserSpecList.png)

## 示例

```sql
mysql> CREATE USER newuser IDENTIFIED BY 'mypassword';
Query OK, 1 row affected (0.02 sec)

mysql> GRANT ALL ON test.* TO 'newuser';
Query OK, 0 rows affected (0.03 sec)

mysql> SHOW GRANTS FOR 'newuser';
+-------------------------------------------------+
| Grants for newuser@%                            |
+-------------------------------------------------+
| GRANT USAGE ON *.* TO 'newuser'@'%'             |
| GRANT ALL PRIVILEGES ON test.* TO 'newuser'@'%' |
+-------------------------------------------------+
2 rows in set (0.00 sec)
```

## MySQL 兼容性

* 与 MySQL 类似，`USAGE` 权限表示登录 TiDB 服务器的能力。
* 目前不支持列级权限。
* 与 MySQL 类似，不存在 `NO_AUTO_CREATE_USER` sql 模式时，`GRANT` 语句将在用户不存在时自动创建一个空密码的新用户。删除此 sql-mode（默认情况下已启用）会带来安全风险。

## 另请参阅

* [REVOKE <privileges>](/reference/sql/statements/revoke-privileges.md)
* [SHOW GRANTS](/reference/sql/statements/show-grants.md)
* [Privilege Management](/reference/security/privilege-system.md)