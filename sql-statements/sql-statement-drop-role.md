---
title: DROP ROLE
summary: TiDB 数据库中 DROP ROLE 的使用概况。
---

# DROP ROLE

使用 `DROP ROLE` 语句可删除已用 `CREATE ROLE` 语句创建的角色。

## 语法图

```ebnf+diagram
DropRoleStmt ::=
    'DROP' 'ROLE' ( 'IF' 'EXISTS' )? RolenameList

RolenameList ::=
    Rolename ( ',' Rolename )*
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

需要注意的是，默认情况下，用户 `jennifer` 需要执行 `SET ROLE analyticsteam` 语句才能使用与角色相关联的权限：

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

以 `root` 用户连接 TiDB：

```shell
mysql -h 127.0.0.1 -P 4000 -u root
```

删除角色 `analyticsteam`：

```sql
DROP ROLE analyticsteam;
Query OK, 0 rows affected (0.02 sec)
```

`jennifer` 用户不再具有与 `analyticsteam` 关联的默认角色，或不能再将 `analyticsteam` 设为启用角色：

以 `jennifer` 用户连接 TiDB：

```shell
mysql -h 127.0.0.1 -P 4000 -u jennifer
```

查看 `jennifer` 用户的权限：

```sql
SHOW GRANTS;
+--------------------------------------+
| Grants for User                      |
+--------------------------------------+
| GRANT USAGE ON *.* TO 'jennifer'@'%' |
+--------------------------------------+
1 row in set (0.00 sec)

SET ROLE analyticsteam;
ERROR 3530 (HY000): `analyticsteam`@`%` is is not granted to jennifer@%
```

## MySQL 兼容性

`DROP ROLE` 语句与 MySQL 8.0 的角色功能完全兼容。如发现任何兼容性差异，请尝试 [TiDB 支持资源](/support.md)。

## 另请参阅

* [`CREATE ROLE`](/sql-statements/sql-statement-create-role.md)
* [`GRANT <role>`](/sql-statements/sql-statement-grant-role.md)
* [`REVOKE <role>`](/sql-statements/sql-statement-revoke-role.md)
* [`SET ROLE`](/sql-statements/sql-statement-set-role.md)
* [`SET DEFAULT ROLE`](/sql-statements/sql-statement-set-default-role.md)
* [基于角色的访问控制](/role-based-access-control.md)
