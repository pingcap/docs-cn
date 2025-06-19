---
title: DROP ROLE | TiDB SQL 语句参考
summary: TiDB 数据库中 DROP ROLE 的使用概述。
---

# DROP ROLE

此语句用于删除之前通过 `CREATE ROLE` 创建的角色。

## 语法

```ebnf+diagram
DropRoleStmt ::=
    'DROP' 'ROLE' ( 'IF' 'EXISTS' )? RolenameList

RolenameList ::=
    Rolename ( ',' Rolename )*
```

## 示例

以 `root` 用户身份连接到 TiDB：

```shell
mysql -h 127.0.0.1 -P 4000 -u root
```

创建一个新角色 `analyticsteam` 和一个新用户 `jennifer`：

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

以 `jennifer` 用户身份连接到 TiDB：

```shell
mysql -h 127.0.0.1 -P 4000 -u jennifer
```

注意，默认情况下，`jennifer` 需要执行 `SET ROLE analyticsteam` 才能使用与 `analyticsteam` 角色相关的权限：

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

以 `root` 用户身份连接到 TiDB：

```shell
mysql -h 127.0.0.1 -P 4000 -u root
```

可以使用 `SET DEFAULT ROLE` 语句将角色 `analyticsteam` 关联到 `jennifer`：

```sql
SET DEFAULT ROLE analyticsteam TO jennifer;
Query OK, 0 rows affected (0.02 sec)
```

以 `jennifer` 用户身份连接到 TiDB：

```shell
mysql -h 127.0.0.1 -P 4000 -u jennifer
```

此后，用户 `jennifer` 拥有与角色 `analyticsteam` 相关的权限，且 `jennifer` 不需要执行 `SET ROLE` 语句：

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

以 `root` 用户身份连接到 TiDB：

```shell
mysql -h 127.0.0.1 -P 4000 -u root
```

删除 `analyticsteam` 角色：

```sql
DROP ROLE analyticsteam;
Query OK, 0 rows affected (0.02 sec)
```

`jennifer` 不再具有默认角色 `analyticsteam`，也无法将角色设置为 `analyticsteam`。

以 `jennifer` 用户身份连接到 TiDB：

```shell
mysql -h 127.0.0.1 -P 4000 -u jennifer
```

显示 `jennifer` 的权限：

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

TiDB 中的 `DROP ROLE` 语句与 MySQL 8.0 的角色功能完全兼容。如果发现任何兼容性差异，请[报告问题](https://docs.pingcap.com/tidb/stable/support)。

## 另请参阅

* [`CREATE ROLE`](/sql-statements/sql-statement-create-role.md)
* [`GRANT <role>`](/sql-statements/sql-statement-grant-role.md)
* [`REVOKE <role>`](/sql-statements/sql-statement-revoke-role.md)
* [`SET ROLE`](/sql-statements/sql-statement-set-role.md)
* [`SET DEFAULT ROLE`](/sql-statements/sql-statement-set-default-role.md)

<CustomContent platform="tidb">

* [基于角色的访问控制](/role-based-access-control.md)

</CustomContent>
