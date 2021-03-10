---
title: 基于角色的访问控制
aliases: ['/docs-cn/dev/role-based-access-control/','/docs-cn/dev/reference/security/role-based-access-control/']
---

# 基于角色的访问控制

TiDB 的基于角色的访问控制 (RBAC) 系统的实现类似于 MySQL 8.0 的 RBAC 系统。TiDB 兼容大部分 MySQL RBAC 系统的语法。

本文档主要介绍 TiDB 基于角色的访问控制相关操作及实现。

## 角色访问控制相关操作

角色是一系列权限的集合。用户可以创建角色、删除角色、将权限赋予角色；也可以将角色授予给其他用户，被授予的用户在启用角色后，可以得到角色所包含的权限。

### 创建角色

创建角色 app_developer，app_read 和 app_write：

{{< copyable "sql" >}}

```sql
CREATE ROLE 'app_developer', 'app_read', 'app_write';
```

角色名的格式和规范可以参考 [TiDB 用户账户管理](/user-account-management.md)。

角色会被保存在 `mysql.user` 表中，角色名称的主机名部分（如果省略）默认为 `'%'`。如果表中有同名角色或用户，角色会创建失败并报错。创建角色的用户需要拥有 `CREATE ROLE` 或 `CREATE USER` 权限。

### 授予角色权限

为角色授予权限和为用户授予权限操作相同，可参考 [TiDB 权限管理](/privilege-management.md)。

为 `app_read` 角色授予数据库 `app_db` 的读权限：

{{< copyable "sql" >}}

```sql
GRANT SELECT ON app_db.* TO 'app_read'@'%';
```

为 `app_write` 角色授予数据库 `app_db` 的写权限：

{{< copyable "sql" >}}

```sql
GRANT INSERT, UPDATE, DELETE ON app_db.* TO 'app_write'@'%';
```

为 `app_developer` 角色授予 `app_db` 数据库的全部权限：

{{< copyable "sql" >}}

```sql
GRANT ALL ON app_db.* TO 'app_developer';
```

### 将角色授予给用户

假设有一个用户拥有开发者角色，可以对 `app_db` 的所有操作权限；另外有两个用户拥有 `app_db` 的只读权限；还有一个用户拥有 `app_db` 的读写权限。

首先用 `CREATE USER` 来创建用户。

{{< copyable "sql" >}}

```sql
CREATE USER 'dev1'@'localhost' IDENTIFIED BY 'dev1pass';
CREATE USER 'read_user1'@'localhost' IDENTIFIED BY 'read_user1pass';
CREATE USER 'read_user2'@'localhost' IDENTIFIED BY 'read_user2pass';
CREATE USER 'rw_user1'@'localhost' IDENTIFIED BY 'rw_user1pass';
```

然后使用 `GRANT` 授予用户对应的角色。

{{< copyable "sql" >}}

```sql
GRANT 'app_developer' TO 'dev1'@'localhost';
GRANT 'app_read' TO 'read_user1'@'localhost', 'read_user2'@'localhost';
GRANT 'app_read', 'app_write' TO 'rw_user1'@'localhost';
```

用户执行将角色授予给其他用户或者收回角色的命令，需要用户拥有 `SUPER` 权限。将角色授予给用户时并不会启用该角色，启用角色需要额外的操作。

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

### 查看角色拥有的权限

可以通过 `SHOW GRANTS` 语句查看用户被授予了哪些角色。当用户查看其他用户权限相关信息时，需要对 `mysql` 数据库拥有 `SELECT` 权限。

{{< copyable "sql" >}}

```sql
SHOW GRANTS FOR 'dev1'@'localhost';
```

```
+-------------------------------------------------+
| Grants for dev1@localhost                       |
+-------------------------------------------------+
| GRANT USAGE ON *.* TO `dev1`@`localhost`        |
| GRANT `app_developer`@`%` TO `dev1`@`localhost` |
+-------------------------------------------------+
```

可以通过使用 `SHOW GRANTS` 的 `USING` 选项来查看角色对应的权限。

{{< copyable "sql" >}}

```sql
SHOW GRANTS FOR 'dev1'@'localhost' USING 'app_developer';
```

```
+----------------------------------------------------------+
| Grants for dev1@localhost                                |
+----------------------------------------------------------+
| GRANT USAGE ON *.* TO `dev1`@`localhost`                 |
| GRANT ALL PRIVILEGES ON `app_db`.* TO `dev1`@`localhost` |
| GRANT `app_developer`@`%` TO `dev1`@`localhost`          |
+----------------------------------------------------------+
```

{{< copyable "sql" >}}

```sql
SHOW GRANTS FOR 'rw_user1'@'localhost' USING 'app_read', 'app_write';
```

```
+------------------------------------------------------------------------------+
| Grants for rw_user1@localhost                                                |
+------------------------------------------------------------------------------+
| GRANT USAGE ON *.* TO `rw_user1`@`localhost`                                 |
| GRANT SELECT, INSERT, UPDATE, DELETE ON `app_db`.* TO `rw_user1`@`localhost` |
| GRANT `app_read`@`%`,`app_write`@`%` TO `rw_user1`@`localhost`               |
+------------------------------------------------------------------------------+
```

{{< copyable "sql" >}}

```sql
SHOW GRANTS FOR 'read_user1'@'localhost' USING 'app_read';
```

```
+--------------------------------------------------------+
| Grants for read_user1@localhost                        |
+--------------------------------------------------------+
| GRANT USAGE ON *.* TO `read_user1`@`localhost`         |
| GRANT SELECT ON `app_db`.* TO `read_user1`@`localhost` |
| GRANT `app_read`@`%` TO `read_user1`@`localhost`       |
+--------------------------------------------------------+
```

可以使用 `SHOW GRANTS` 或 `SHOW GRANTS FOR CURRENT_USER()` 查看当前用户的权限。这两个语句有细微的差异，`SHOW GRANTS` 会显示当前用户的启用角色的权限，而 `SHOW GRANTS FOR CURRENT_USER()` 则不会显示启用角色的权限。

### 设置默认启用角色

角色在授予给用户之后，并不会生效；只有在用户启用了某些角色之后，才可以使用角色拥有的权限。

可以对用户设置默认启用的角色；用户在登陆时，默认启用的角色会被自动启用。

{{< copyable "sql" >}}

```sql
SET DEFAULT ROLE
    {NONE | ALL | role [, role ] ...}
    TO user [, user ]
```

比如将 `app_read` 和 `app_wirte` 设置为 `rw_user1@localhost` 的默认启用角色：

{{< copyable "sql" >}}

```sql
SET DEFAULT ROLE app_read, app_write TO 'rw_user1'@'localhost';
```

将 `dev1@localhost` 的所有角色，设为其默认启用角色：

{{< copyable "sql" >}}

```sql
SET DEFAULT ROLE ALL TO 'dev1'@'localhost';
```

关闭 `dev1@localhost` 的所有默认启用角色：

{{< copyable "sql" >}}

```sql
SET DEFAULT ROLE NONE TO 'dev1'@'localhost';
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

例如，登陆 `rw_user1` 后，为当前用户启用角色 `app_read` 和 `app_write` ，仅在当前 session 有效：

{{< copyable "sql" >}}

```sql
SET ROLE 'app_read', 'app_write';
```

启用当前用户的默认角色：

{{< copyable "sql" >}}

```sql
SET ROLE DEFAULT
```

启用授予给当前用户的所有角色：

{{< copyable "sql" >}}

```sql
SET ROLE ALL
```

不启用任何角色：

{{< copyable "sql" >}}

```sql
SET ROLE NONE
```

启用除 `app_read` 外的角色：

{{< copyable "sql" >}}

```sql
SET ROLE ALL EXCEPT 'app_read'
```

> **注意：**
>
> 使用 `SET ROLE` 启用的角色只有在当前 session 才会有效。

### 查看当前启用角色

当前用户可以通过 `CURRENT_ROLE()` 函数查看当前用户启用了哪些角色。

例如，先对 `rw_user1'@'localhost` 设置默认角色：

{{< copyable "sql" >}}

```sql
SET DEFAULT ROLE ALL TO 'rw_user1'@'localhost';
```

用 `rw_user1@localhost` 登陆后：

{{< copyable "sql" >}}

```sql
SELECT CURRENT_ROLE();
```

```
+--------------------------------+
| CURRENT_ROLE()                 |
+--------------------------------+
| `app_read`@`%`,`app_write`@`%` |
+--------------------------------+
```

{{< copyable "sql" >}}

```sql
SET ROLE 'app_read'; SELECT CURRENT_ROLE();
```

```
+----------------+
| CURRENT_ROLE() |
+----------------+
| `app_read`@`%` |
+----------------+
```

### 收回角色

解除角色 `app_read` 与用户 `read_user1@localhost`、`read_user2@localhost` 的授权关系。

{{< copyable "sql" >}}

```sql
REVOKE 'app_read' FROM 'read_user1'@'localhost', 'read_user2'@'localhost';
```

解除角色 `app_read`、`app_write` 与用户 `rw_user1@localhost` 的授权关系。

{{< copyable "sql" >}}

```sql
REVOKE 'app_read', 'app_write' FROM 'rw_user1'@'localhost';
```

解除角色授权具有原子性，如果在撤销授权操作中失败会回滚。

### 收回权限

`REVOKE` 语句与 `GRANT` 对应，可以使用 `REVOKE` 来撤销 `app_write` 的权限。

{{< copyable "sql" >}}

```sql
REVOKE INSERT, UPDATE, DELETE ON app_db.* FROM 'app_write';
```

具体可参考 [TiDB 权限管理](/privilege-management.md)。

### 删除角色

删除角色 `app_read` 和 `app_write`：

{{< copyable "sql" >}}

```sql
DROP ROLE 'app_read', 'app_write';
```

这个操作会清除角色在 `mysql.user` 表里面的记录项，并且清除在授权表里面的相关记录，解除和其相关的授权关系。执行删除角色的用户需要拥有 `DROP ROLE` 或 `DROP USER` 权限。

### 授权表

在原有的四张[系统权限表](/privilege-management.md#授权表)的基础上，角色访问控制引入了两张新的系统表：

- `mysql.role_edges`：记录角色与用户的授权关系
- `mysql.default_roles`：记录每个用户默认启用的角色

以下是 `mysql.role_edges` 所包含的数据。

{{< copyable "sql" >}}

```sql
select * from mysql.role_edges;
```

```
+-----------+-----------+---------+---------+-------------------+
| FROM_HOST | FROM_USER | TO_HOST | TO_USER | WITH_ADMIN_OPTION |
+-----------+-----------+---------+---------+-------------------+
| %         | r_1       | %       | u_1     | N                 |
+-----------+-----------+---------+---------+-------------------+
1 row in set (0.00 sec)
```

其中 `FROM_HOST` 和 `FROM_USER` 分别表示角色的主机名和用户名，`TO_HOST` 和 `TO_USER` 分别表示被授予角色的用户的主机名和用户名。

`mysql.default_roles` 中包含了每个用户默认启用了哪些角色。

{{< copyable "sql" >}}

```sql
select * from mysql.default_roles;
```

```
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

由于基于角色的访问控制模块和用户管理以及权限管理结合十分紧密，因此需要参考一些操作的细节：

- [TiDB 权限管理](/privilege-management.md)
- [TiDB 用户账户管理](/user-account-management.md)
