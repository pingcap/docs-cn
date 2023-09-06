---
title: SET DEFAULT ROLE | TiDB SQL Statement Reference
summary: An overview of the usage of SET DEFAULT ROLE for the TiDB database.
---

# `SET DEFAULT ROLE`

This statement sets a specific role to be applied to a user by default. Thus, they will automatically have the permissions associated with a role without having to execute `SET ROLE <rolename>` or `SET ROLE ALL`.

## Synopsis

**SetDefaultRoleStmt:**

![SetDefaultRoleStmt](/media/sqlgram/SetDefaultRoleStmt.png)

**SetDefaultRoleOpt:**

![SetDefaultRoleOpt](/media/sqlgram/SetDefaultRoleOpt.png)

**RolenameList:**

![RolenameList](/media/sqlgram/RolenameList.png)

**UsernameList:**

![UsernameList](/media/sqlgram/UsernameList.png)

## Examples

Connect to TiDB as the `root` user:

```shell
mysql -h 127.0.0.1 -P 4000 -u root
```

Create a new role `analyticsteam` and a new user `jennifer`:

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

Connect to TiDB as the `jennifer` user:

```shell
mysql -h 127.0.0.1 -P 4000 -u jennifer
```

Note that by default `jennifer` needs to execute `SET ROLE analyticsteam` in order to be able to use the privileges associated with the `analyticsteam` role:

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
| GRANT Select ON test.* TO 'jennifer'@'%'    |
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

Connect to TiDB as the `root` user:

```shell
mysql -h 127.0.0.1 -P 4000 -u root
```

The statement `SET DEFAULT ROLE` can be used to associate the role `analyticsteam` to `jennifer`:

```sql
SET DEFAULT ROLE analyticsteam TO jennifer;
Query OK, 0 rows affected (0.02 sec)
```

Connect to TiDB as the `jennifer` user:

```shell
mysql -h 127.0.0.1 -P 4000 -u jennifer
```

After this, the user `jennifer` has the privileges associated with the role `analyticsteam` and `jennifer` does not have to execute the statement `SET ROLE`:

```sql
SHOW GRANTS;
+---------------------------------------------+
| Grants for User                             |
+---------------------------------------------+
| GRANT USAGE ON *.* TO 'jennifer'@'%'        |
| GRANT Select ON test.* TO 'jennifer'@'%'    |
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

`SET DEFAULT ROLE` will not automatically `GRANT` the associated role to the user. Attempting to `SET DEFAULT ROLE` for a role that `jennifer` does not have granted results in the following error:

```sql
SET DEFAULT ROLE analyticsteam TO jennifer;
ERROR 3530 (HY000): `analyticsteam`@`%` is is not granted to jennifer@%
```

## MySQL compatibility

The `SET DEFAULT ROLE` statement in TiDB is fully compatible with the roles feature in MySQL 8.0. If you find any compatibility differences, [report a bug](https://docs.pingcap.com/tidb/stable/support).

## See also

* [`CREATE ROLE`](/sql-statements/sql-statement-create-role.md)
* [`DROP ROLE`](/sql-statements/sql-statement-drop-role.md)
* [`GRANT <role>`](/sql-statements/sql-statement-grant-role.md)
* [`REVOKE <role>`](/sql-statements/sql-statement-revoke-role.md)
* [`SET ROLE`](/sql-statements/sql-statement-set-role.md)

<CustomContent platform="tidb">

* [Role-Based Access Control](/role-based-access-control.md)

</CustomContent>
