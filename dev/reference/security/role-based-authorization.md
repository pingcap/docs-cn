---
title: 基于角色的访问控制
category: user guide
---

# 基于角色的访问控制

TiDB 的角色访问控制系统参考 MySQL 的角色访问控制系统进行实现。TiDB 兼容大部分 MySQL 角色访问控制的语法。

本文档主要介绍 TiDB 角色访问控制相关操作及实现。

## 角色访问控制相关操作

角色是一系列权限的集合。用户可以创建角色、删除角色、将权限赋予给角色；也可以将角色授予给其他用户，被授予的用户在启用角色后，可以得到角色所包含的权限。

### 创建角色

创建角色 r_1 和 r_2：

```sql
CREATE ROLE `r_1`@`%`, `r_2`@`%`;
```

角色名的格式和规范可以参考 [TiDB 用户账户管理](/dev/reference/security/user-account-management.md)。

角色会被保存在 `mysql.user` 表中，如果表中有同名角色或用户，角色会创建失败并报错。
创建角色的用户需要拥有 `CREATE ROLE` 或 `CREATE USER` 权限。

### 删除角色

删除角色 r_1 和 r_2：

```sql
DROP ROLE `r_1`@`%`, `r_2`@`%`;
```

这个操作会清除角色在 `mysql.user` 表里面的记录项，并且清除在授权表里面的相关记录，解除和其相关的授权关系。
执行删除角色的用户需要拥有 `DROP ROLE` 或 `DROP USER` 权限。

### 授予角色权限

为角色授予权限和为用户授予权限操作相同，可参考 [TiDB 权限管理](/dev/reference/security/privilege-system.md)。

为 `xxx` 角色授予数据库 `test` 的读权限：

```sql
GRANT SELECT ON test.* TO 'xxx'@'%';
```

为 `xxx` 角色授予所有数据库的全部权限：

```sql
GRANT ALL PRIVILEGES ON *.* TO 'xxx'@'%';
```

### 收回权限

`REVOKE` 语句与 `GRANT` 对应：

```sql
REVOKE ALL PRIVILEGES ON `test`.* FROM 'xxx'@'%';
```

具体可参考 [TiDB 权限管理](/dev/reference/security/privilege-system.md)。

### 将角色授予给用户

将角色 role1 和 role2 同时授予给用户 `user1@localhost` 和 `user2@localhost`。 

```sql
GRANT 'role1', 'role2' TO 'user1'@'localhost', 'user2'@'localhost';
```

用户执行将角色授予给其他用户或者收回角色的命令，需要用户拥有 `SUPER` 权限。
将角色授予给用户时并不会启用该角色，启用角色需要额外的操作。

以下操作可能会形成一个“关系环”：

```sql
CREATE USER 'u1', 'u2';
CREATE ROLE 'r1', 'r2';

GRANT 'u1' TO 'u1';
GRANT 'r1' TO 'r1';

GRANT 'r2' TO 'u2';
GRANT 'u2' TO 'r2';
```

TiDB 允许这种多层授权关系存在，可以使用多层授权关系实现权限继承。

### 收回角色

解除角色 role1、role2 与用户 `user1@localhost`、`user2@localhost` 的授权关系。 

```sql
REVOKE 'role1', 'role2' FROM 'user1'@'localhost', 'user2'@'localhost';
```

解除角色授权具有原子性，如果在撤销授权操作中失败会回滚。

### 设置默认启用角色

角色在授予给用户之后，并不会生效；只有在用户启用了某些角色之后，才可以使用角色拥有的权限。

可以对用户设置默认启用的角色；用户在登陆时，默认启用的角色会被自动启用。

```sql
SET DEFAULT ROLE
    {NONE | ALL | role [, role ] ...}
    TO user [, user ]
```

比如将 administrator 和 developer 设置为 `test@localhost` 的默认启用角色：

```sql
SET DEFAULT ROLE administrator, developer TO 'test'@'localhost';
```

将 `test@localhost` 的所有角色，设为其默认启用角色。

```sql
SET DEFAULT ROLE ALL TO 'test'@'localhost';
```

关闭 `test@localhost` 的所有默认启用角色。

```sql
SET DEFAULT ROLE NONE TO 'test'@'localhost';
```

需要注意的是，设置为默认启用角色的角色必须已经授予给那个用户。

### 在当前 session 启用角色

除了使用 `SET DEFAULT ROLE` 启用角色外，TiDB 还提供让用户在当前 session 启用某些角色的功能。

```sql
SET ROLE {
    DEFAULT
  | NONE
  | ALL
  | ALL EXCEPT role [, role ] ...
  | role [, role ] ...
}
```

例如，为当前用户启用角色 role1 和 role2 ，仅在当前 session 有效。

```sql
SET ROLE 'role1', 'role2';
```

除此之外，还有其他的用法。

```sql
SET ROLE DEFAULT --启用当前用户的默认角色。
SET ROLE ALL --启用授予给当前用户的所有角色。
SET ROLE NONE --不启用任何角色。
SET ROLE ALL EXCEPT 'role1', 'role2' --启用除 role1 和 role2 外的角色。
```

要注意，使用 `SET ROLE` 启用的角色只有在当前 session 才会有效。

### 查看当前启用角色

当前用户可以通过 `CURRENT_ROLE()` 函数查看当前用户启用了哪些角色。

例如，先对 `u1'@'localhost` 授予角色。

```sql
GRANT 'r1', 'r2' TO 'u1'@'localhost';
SET DEFAULT ROLE ALL TO 'u1'@'localhost';
```

在 u1 登陆后：

```sql
mysql> SELECT CURRENT_ROLE();
+-------------------+
| CURRENT_ROLE()    |
+-------------------+
| `r1`@`%`,`r2`@`%` |
+-------------------+
mysql> SET ROLE 'r1'; SELECT CURRENT_ROLE();
+----------------+
| CURRENT_ROLE() |
+----------------+
| `r1`@`%`       |
+----------------+
```

### 查看角色拥有的权限

可以通过 `SHOW GRANTS` 语句查看用户被授予了哪些角色。
当用户查看其他用户权限相关信息时，需要对 `mysql` 数据库拥有 `SELECT` 权限。

```sql
mysql> SHOW GRANTS FOR 'u1'@'localhost';
+---------------------------------------------+
| Grants for u1@localhost                     |
+---------------------------------------------+
| GRANT USAGE ON *.* TO `u1`@`localhost`      |
| GRANT `r1`@`%`,`r2`@`%` TO `u1`@`localhost` |
+---------------------------------------------+
```

可以通过使用 `SHOW GRANTS` 的 `USING` 选项来查看角色对应的权限。

```sql
mysql> SHOW GRANTS FOR 'u1'@'localhost' USING 'r1';
+---------------------------------------------+
| Grants for u1@localhost                     |
+---------------------------------------------+
| GRANT USAGE ON *.* TO `u1`@`localhost`      |
| GRANT Select ON `db1`.* TO `u1`@`localhost` |
| GRANT `r1`@`%`,`r2`@`%` TO `u1`@`localhost` |
+---------------------------------------------+
mysql> SHOW GRANTS FOR 'u1'@'localhost' USING 'r2';
+-------------------------------------------------------------+
| Grants for u1@localhost                                     |
+-------------------------------------------------------------+
| GRANT USAGE ON *.* TO `u1`@`localhost`                      |
| GRANT Insert, Update, Delete ON `db1`.* TO `u1`@`localhost` |
| GRANT `r1`@`%`,`r2`@`%` TO `u1`@`localhost`                 |
+-------------------------------------------------------------+
mysql> SHOW GRANTS FOR 'u1'@'localhost' USING 'r1', 'r2';
+---------------------------------------------------------------------+
| Grants for u1@localhost                                             |
+---------------------------------------------------------------------+
| GRANT USAGE ON *.* TO `u1`@`localhost`                              |
| GRANT Select, Insert, Update, Delete ON `db1`.* TO `u1`@`localhost` |
| GRANT `r1`@`%`,`r2`@`%` TO `u1`@`localhost`                         |
+---------------------------------------------------------------------+
```

### 授权表

在原有的四张系统表的基础上，角色访问控制引入了三张新的系统表：

- `mysql.role_edges`：记录角色与用户的授权关系
- `mysql.default_role`：记录每个用户默认启用的角色

以下是 `mysql.role_edges` 所包含的数据。

```sql
mysql> select * from mysql.role_edges;
+-----------+-----------+---------+---------+-------------------+
| FROM_HOST | FROM_USER | TO_HOST | TO_USER | WITH_ADMIN_OPTION |
+-----------+-----------+---------+---------+-------------------+
| %         | r_1       | %       | u_1     | N                 |
+-----------+-----------+---------+---------+-------------------+
1 row in set (0.00 sec)
```

其中 `FROM_HOST` 和 `FROM_USER` 分别表示角色的主机名和用户名，`TO_HOST` 和 `TO_USER` 分别表示被授予角色的用户的主机名和用户名。

`mysql.default_roles` 中包含了每个用户默认启用了哪些角色。

```sql
mysql> select * from mysql.default_roles;
+------+------+-------------------+-------------------+
| HOST | USER | DEFAULT_ROLE_HOST | DEFAULT_ROLE_USER |
+------+------+-------------------+-------------------+
| %    | u_1  | %                 | r_1               |
| %    | u_1  | %                 | r_2               |
+------+------+-------------------+-------------------+
2 rows in set (0.00 sec)
```

`HOST` 和 `USER` 分别表示用户的主机名和用户名，`DEFAULT_ROLE_HOST` 和 `DEFAULT_ROLE_USER` 分别表示默认启用的角色的主机名和用户名。

### 其他

由于角色访问控制模块和用户管理以及权限管理结合十分紧密，因此需要参考一些操作的细节：

- [TiDB 权限管理](/dev/reference/security/privilege-system.md)
- [TiDB 用户账户管理](/dev/reference/security/user-account-management.md)