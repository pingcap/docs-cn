---
title: SET ROLE | TiDB SQL Statement Reference
summary: An overview of the usage of SET ROLE for the TiDB database.
aliases: ['/docs/dev/sql-statements/sql-statement-set-role/']
---

# SET ROLE

The `SET ROLE` statement is used to enable roles in the current session. After enabling roles, users can use the privileges of the role(s).

## Synopsis

**SetRoleStmt:**

![SetRoleStmt](/media/sqlgram/SetRoleStmt.png)

**SetRoleOpt:**

![SetRoleOpt](/media/sqlgram/SetRoleOpt.png)

**SetDefaultRoleOpt:**

![SetDefaultRoleOpt](/media/sqlgram/SetDefaultRoleOpt.png)

## Examples

Create a user `'u1'@'%'` and three roles: `'r1'@'%'`, `'r2'@'%'` and `'r3'@'%'`. Grant these roles to `'u1'@'%'` and set `'r1'@'%'` as the default role of `'u1'@'%'`.

{{< copyable "sql" >}}

```sql
CREATE USER 'u1'@'%';
CREATE ROLE 'r1', 'r2', 'r3';
GRANT 'r1', 'r2', 'r3' TO 'u1'@'%';
SET DEFAULT ROLE 'r1' TO 'u1'@'%';
```

Log in as `'u1'@'%'` and execute the following `SET ROLE` statement to enable all roles.

{{< copyable "sql" >}}

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

Execute the following `SET ROLE` statement to enable `'r2'` and `'r3'`.

{{< copyable "sql" >}}

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

Execute the following `SET ROLE` statement to enable the default role(s).

{{< copyable "sql" >}}

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

Execute the following `SET ROLE` statement to cancel all enabled role(s).

{{< copyable "sql" >}}

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

## MySQL compatibility

The `SET ROLE` statement in TiDB is fully compatible with the roles feature in MySQL 8.0. If you find any compatibility differences, [report a bug](https://docs.pingcap.com/tidb/stable/support).

## See also

* [CREATE ROLE](/sql-statements/sql-statement-create-role.md)
* [DROP ROLE](/sql-statements/sql-statement-drop-role.md)
* [`GRANT <role>`](/sql-statements/sql-statement-grant-role.md)
* [`REVOKE <role>`](/sql-statements/sql-statement-revoke-role.md)
* [SET DEFAULT ROLE](/sql-statements/sql-statement-set-default-role.md)

<CustomContent platform="tidb">

* [Role-Based Access Control](/role-based-access-control.md)

</CustomContent>
