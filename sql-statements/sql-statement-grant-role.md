---
title: GRANT <role>
summary: TiDB 数据库中 GRANT <role> 的使用概况。
---

# `GRANT <role>`

`GRANT <role>` 语句用于将之前创建的角色授予给现有用户。用户可以通过 `SET ROLE <rolename>` 语句拥有角色权限，或者通过 `SET ROLE ALL` 语句拥有被授予的所有角色。

## 语法图

```ebnf+diagram
GrantRoleStmt ::=
    'GRANT' RolenameList 'TO' UsernameList

RolenameList ::=
    Rolename ( ',' Rolename )*

UsernameList ::=
    Username ( ',' Username )*
```

## 示例

以 `root` 用户连接 TiDB：

```shell
mysql -h 127.0.0.1 -P 4000 -u root
```

创建新角色 `analyticsteam` 和新用户 `jennifer`：

```sql
CREATE ROLE analyticsteam;
Query OK, 0 rows affected (0.02 sec)

GRANT SELECT ON test.* TO analyticsteam;
Query OK, 0 rows affected (0.02 sec)

CREATE USER jennifer;
Query OK, 0 rows affected (0.01 sec)

GRANT analyticsteam TO jennifer;
Query OK, 0 rows affected (0.01 sec)
```

以 `jennifer` 用户连接 TiDB：

```shell
mysql -h 127.0.0.1 -P 4000 -u jennifer
```

需要注意的是，默认情况下，用户 `jennifer` 需要执行 `SET ROLE analyticsteam` 语句才能使用与 `analyticsteam` 角色相关联的权限：

```sql
SHOW GRANTS;
+---------------------------------------------+
| Grants for User                             |
+---------------------------------------------+
| GRANT USAGE ON *.* TO 'jennifer'@'%'        |
| GRANT 'analyticsteam'@'%' TO 'jennifer'@'%' |
+---------------------------------------------+
2 rows in set (0.00 sec)

SHOW TABLES in test;
ERROR 1044 (42000): Access denied for user 'jennifer'@'%' to database 'test'
SET ROLE analyticsteam;
Query OK, 0 rows affected (0.00 sec)

SHOW GRANTS;
+---------------------------------------------+
| Grants for User                             |
+---------------------------------------------+
| GRANT USAGE ON *.* TO 'jennifer'@'%'        |
| GRANT SELECT ON test.* TO 'jennifer'@'%'    |
| GRANT 'analyticsteam'@'%' TO 'jennifer'@'%' |
+---------------------------------------------+
3 rows in set (0.00 sec)

SHOW TABLES IN test;
+----------------+
| Tables_in_test |
+----------------+
| t1             |
+----------------+
1 row in set (0.00 sec)
```

以 `root` 用户连接 TiDB：

```shell
mysql -h 127.0.0.1 -P 4000 -u root
```

执行 `SET DEFAULT ROLE` 语句将用户 `jennifer` 与 `analyticsteam` 角色相关联：

```sql
SET DEFAULT ROLE analyticsteam TO jennifer;
Query OK, 0 rows affected (0.02 sec)
```

以 `jennifer` 用户连接 TiDB：

```shell
mysql -h 127.0.0.1 -P 4000 -u jennifer
```

此时 `jennifer` 用户无需执行 `SET ROLE` 语句就能拥有 `analyticsteam` 角色相关联的权限：

```sql
SHOW GRANTS;
+---------------------------------------------+
| Grants for User                             |
+---------------------------------------------+
| GRANT USAGE ON *.* TO 'jennifer'@'%'        |
| GRANT SELECT ON test.* TO 'jennifer'@'%'    |
| GRANT 'analyticsteam'@'%' TO 'jennifer'@'%' |
+---------------------------------------------+
3 rows in set (0.00 sec)

SHOW TABLES IN test;
+----------------+
| Tables_in_test |
+----------------+
| t1             |
+----------------+
1 row in set (0.00 sec)
```

## MySQL 兼容性

`GRANT <role>` 语句与 MySQL 8.0 的角色功能完全兼容。如发现任何兼容性差异，请尝试 [TiDB 支持资源](/support.md)。

## 另请参阅

* [`GRANT <privileges>`](/sql-statements/sql-statement-grant-privileges.md)
* [`CREATE ROLE`](/sql-statements/sql-statement-create-role.md)
* [`DROP ROLE`](/sql-statements/sql-statement-drop-role.md)
* [`REVOKE <role>`](/sql-statements/sql-statement-revoke-role.md)
* [`SET ROLE`](/sql-statements/sql-statement-set-role.md)
* [`SET DEFAULT ROLE`](/sql-statements/sql-statement-set-default-role.md)
* [基于角色的访问控制](/role-based-access-control.md)
