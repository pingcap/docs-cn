---
title: SET ROLE
summary: TiDB 数据库中 SET ROLE 的使用概况。
---

# SET ROLE

`SET ROLE` 用于在当前用户会话中启用角色。使用 `SET ROLE` 启用角色后，用户可以使用这些角色的权限。

## 语法图

```ebnf+diagram
SetRoleStmt ::=
    "SET" "ROLE" ( "DEFAULT" | "ALL" ( "EXCEPT" Rolename ("," Rolename)* )? | "NONE" | Rolename ("," Rolename)* )?
```

## 示例

创建一个用户 `'u1'@'%'`，创建三个角色 `'r1'@'%'`、`'r2'@'%'` 和 `'r3'@'%'` 并将这些角色授予给 `'u1'@'%'`。将 `'u1'@'%'` 的默认启用角色设置为 `'r1'@'%'`。

```sql
CREATE USER 'u1'@'%';
CREATE ROLE 'r1', 'r2', 'r3';
GRANT 'r1', 'r2', 'r3' TO 'u1'@'%';
SET DEFAULT ROLE 'r1' TO 'u1'@'%';
```

使用 `'u1'@'%'` 登录，执行 `SET ROLE` 将启用角色设置为 `ALL`。

```sql
SET ROLE ALL;
SELECT CURRENT_ROLE();
```

```
+----------------------------+
| CURRENT_ROLE()             |
+----------------------------+
| `r1`@`%`,`r2`@`%`,`r3`@`%` |
+----------------------------+
1 row in set (0.000 sec)
```

执行 `SET ROLE` 将启用角色设置为 `'r2'` 和 `'r3'`。

```sql
SET ROLE 'r2', 'r3';
SELECT CURRENT_ROLE();
```

```
+-------------------+
| CURRENT_ROLE()    |
+-------------------+
| `r2`@`%`,`r3`@`%` |
+-------------------+
1 row in set (0.000 sec)
```

执行 `SET ROLE` 将启用角色设置为 `DEFAULT`。

```sql
SET ROLE DEFAULT;
SELECT CURRENT_ROLE();
```

```
+----------------+
| CURRENT_ROLE() |
+----------------+
| `r1`@`%`       |
+----------------+
1 row in set (0.000 sec)
```

执行 `SET ROLE` 将启用角色设置为 `NONE`。

```sql
SET ROLE NONE;
SELECT CURRENT_ROLE();
```

```
+----------------+
| CURRENT_ROLE() |
+----------------+
|                |
+----------------+
1 row in set (0.000 sec)
```

## MySQL 兼容性

`SET ROLE` 语句与 MySQL 8.0 的角色功能完全兼容。如发现任何兼容性差异，请尝试 [TiDB 支持资源](/support.md)。

## 另请参阅

* [`CREATE ROLE`](/sql-statements/sql-statement-create-role.md)
* [`DROP ROLE`](/sql-statements/sql-statement-drop-role.md)
* [`GRANT <role>`](/sql-statements/sql-statement-grant-role.md)
* [`REVOKE <role>`](/sql-statements/sql-statement-revoke-role.md)
* [`SET DEFAULT ROLE`](/sql-statements/sql-statement-set-default-role.md)
* [基于角色的访问控制](/role-based-access-control.md)
