---
title: Role-Based Access Control
summary: This document introduces TiDB RBAC operations and implementation.
category: reference
---

# Role-Based Access Control

The implementation of TiDB's role-based access control (RBAC) system is similar to that of MySQL 8.0. TiDB is compatible with most RBAC syntax of MySQL.

This document introduces TiDB RBAC-related operations and implementation.

> **Warning:**
>
> The feature of RBAC is still in the testing phase. Do not use it in the production environment.

## RBAC operations

A role is a collection of a series of privileges. You can do the following operations:

- Create a role.
- Delete a role.
- Grant a privilege to a role.
- Grant a role to another user. That user can obtain the privileges involved in the role, after enabling the role.

### Create a role

For example, you can use the following statement to create roles `r_1` and `r_2`:

{{< copyable "sql" >}}

```sql
CREATE ROLE `r_1`@`%`, `r_2`@`%`;
```

For the role naming format and rule, see [TiDB User Account Management](/reference/security/user-account-management.md).

Roles are stored in the `mysql.user` table. The name of the role you are trying to create must be unique; otherwise, an error is reported.

To create a role, you need the `CREATE ROLE` or `CREATE USER` privilege.

### Delete a role

For example, you can use the following statement to delete roles `r_1` and `r_2`:

{{< copyable "sql" >}}

```sql
DROP ROLE `r_1`@`%`, `r_2`@`%`;
```

This operation deletes role records in the `mysql.user` table, removes related records in the authorization table, and terminates role-related authorization relationship.

To delete a role, you need the `DROP ROLE` or `DROP USER` privilege.

### Grant a privilege to a role

The operation of granting a privilege to a role is the same with that of granting a privilege to a user. For details, see [TiDB Privilege Management](/reference/security/privilege-system.md).

For example, you can use the following statement to grant the `analyst` role the privilege to read the `test` database:

{{< copyable "sql" >}}

```sql
GRANT SELECT ON test.* TO 'analyst'@'%';
```

You can use the following statement to grant the `analyst` role all privileges on all databases:

{{< copyable "sql" >}}

```sql
GRANT ALL PRIVILEGES ON *.* TO 'analyst'@'%';
```

### Revoke a privilege

For example, you can use the following statement to revoke all privileges on the `test` database granted to the `analyst` role:

{{< copyable "sql" >}}

```sql
REVOKE ALL PRIVILEGES ON `test`.* FROM 'analyst'@'%';
```

For details, see [TiDB Privilege Management](/reference/security/privilege-system.md).

### Grant a role to a user

For example, you can use the following statement to grant both roles `role1` and `role2` to users `user1@localhost` and `user2@localhost`:

{{< copyable "sql" >}}

```sql
GRANT 'role1', 'role2' TO 'user1'@'localhost', 'user2'@'localhost';
```

To grant a role to another user or revoke a role, you need the `SUPER` privilege.

Granting a role to a user does not mean enabling the role immediately. Enabling a role is another operation.

The following operations might form a "relation loop:"

```sql
CREATE USER 'u1', 'u2';
CREATE ROLE 'r1', 'r2';

GRANT 'u1' TO 'u1';
GRANT 'r1' TO 'r1';

GRANT 'r2' TO 'u2';
GRANT 'u2' TO 'r2';
```

TiDB supports this multi-level authorization relationship. You can use it to implement privilege inheritance.

### Revoke a role

Revoke roles `role1` and `role2` from users `user1@localhost` and `user2@localhost`.

{{< copyable "sql" >}}

```sql
REVOKE 'role1', 'role2' FROM 'user1'@'localhost', 'user2'@'localhost';
```

The operation of revoking a role from a user is atomic. If you fail to revoke a role, this operation rolls back.

### Set the default role

After a role is granted to a user, it does not take effect immediately. Only after the user enables this role, he can use the privilege the role owns.

You can set default roles for a user. When the user logs in, the default roles are automatically enabled.

{{< copyable "sql" >}}

```sql
SET DEFAULT ROLE
    {NONE | ALL | role [, role ] ...}
    TO user [, user ]
```

For example, you can use the following statement to set default roles of `test@localhost` to `administrator` and `developer`:

{{< copyable "sql" >}}

```sql
SET DEFAULT ROLE administrator, developer TO 'test'@'localhost';
```

You can use the following statement to set default roles of `test@localhost` to all roles:

{{< copyable "sql" >}}

```sql
SET DEFAULT ROLE ALL TO 'test'@'localhost';
```

You can use the following statement to disable all default roles of `test@localhost`:

{{< copyable "sql" >}}

```sql
SET DEFAULT ROLE NONE TO 'test'@'localhost';
```

> **Note:**
>
> You need to grant the role to the user before you set the default role to this role.

### Enable a role in the current session

You can enable some role(s) in the current session.

```sql
SET ROLE {
    DEFAULT
  | NONE
  | ALL
  | ALL EXCEPT role [, role ] ...
  | role [, role ] ...
}
```

For example, you can use the following statement to enable roles `role1` and `role2` that are valid only in the current session:

{{< copyable "sql" >}}

```sql
SET ROLE 'role1', 'role2';
```

You can use the following statement to enable the default role of the current user:

{{< copyable "sql" >}}

```sql
SET ROLE DEFAULT
```

You can use the following statement to enable all roles granted to the current user:

{{< copyable "sql" >}}

```sql
SET ROLE ALL
```

You can use the following statement to disable all roles:

{{< copyable "sql" >}}

```sql
SET ROLE NONE
```

You can use the following statement to enable roles except `role1` and `role2`:

{{< copyable "sql" >}}

```sql
SET ROLE ALL EXCEPT 'role1', 'role2' --
```

> **Note:**
>
> If you use `SET ROLE` to enable a role, this role is valid only in the current session.

### Check the current enabled role

The current user can use the `CURRENT_ROLE()` function to check which role has been enabled by the current user.

For example:

1. You can grant roles to `u1'@'localhost`:

    {{< copyable "sql" >}}

    ```sql
    GRANT 'r1', 'r2' TO 'u1'@'localhost';
    ```

    {{< copyable "sql" >}}

    ```sql
    SET DEFAULT ROLE ALL TO 'u1'@'localhost';
    ```

2. After `u1` logs in, you can execute the following statement:

    {{< copyable "sql" >}}

    ```sql
    SELECT CURRENT_ROLE();
    ```

    ```
    +-------------------+
    | CURRENT_ROLE()    |
    +-------------------+
    | `r1`@`%`,`r2`@`%` |
    +-------------------+
    ```

    {{< copyable "sql" >}}

    ```sql
    SET ROLE 'r1'; SELECT CURRENT_ROLE();
    ```

    ```
    +----------------+
    | CURRENT_ROLE() |
    +----------------+
    | `r1`@`%`       |
    +----------------+
    ```

### Check a role's privileges

You can use the `SHOW GRANTS` statement to check which role has been granted to the user.

To check privilege-related information of another user, you need the `SELECT` privilege on the `mysql` database.

{{< copyable "sql" >}}

```sql
SHOW GRANTS FOR 'u1'@'localhost';
```

```
+---------------------------------------------+
| Grants for u1@localhost                     |
+---------------------------------------------+
| GRANT USAGE ON *.* TO `u1`@`localhost`      |
| GRANT `r1`@`%`,`r2`@`%` TO `u1`@`localhost` |
+---------------------------------------------+
```

You can use the `USING` option of `SHOW GRANTS` to check a role's privileges:

{{< copyable "sql" >}}

```sql
SHOW GRANTS FOR 'u1'@'localhost' USING 'r1';
```

```
+---------------------------------------------+
| Grants for u1@localhost                     |
+---------------------------------------------+
| GRANT USAGE ON *.* TO `u1`@`localhost`      |
| GRANT Select ON `db1`.* TO `u1`@`localhost` |
| GRANT `r1`@`%`,`r2`@`%` TO `u1`@`localhost` |
+---------------------------------------------+
```

{{< copyable "sql" >}}

```sql
SHOW GRANTS FOR 'u1'@'localhost' USING 'r2';
```

```
+-------------------------------------------------------------+
| Grants for u1@localhost                                     |
+-------------------------------------------------------------+
| GRANT USAGE ON *.* TO `u1`@`localhost`                      |
| GRANT Insert, Update, Delete ON `db1`.* TO `u1`@`localhost` |
| GRANT `r1`@`%`,`r2`@`%` TO `u1`@`localhost`                 |
+-------------------------------------------------------------+
```

{{< copyable "sql" >}}

```sql
SHOW GRANTS FOR 'u1'@'localhost' USING 'r1', 'r2';
```

```
+---------------------------------------------------------------------+
| Grants for u1@localhost                                             |
+---------------------------------------------------------------------+
| GRANT USAGE ON *.* TO `u1`@`localhost`                              |
| GRANT Select, Insert, Update, Delete ON `db1`.* TO `u1`@`localhost` |
| GRANT `r1`@`%`,`r2`@`%` TO `u1`@`localhost`                         |
+---------------------------------------------------------------------+
```

You can use `SHOW GRANTS` or `SHOW GRANTS FOR CURRENT_USER()` to check the current user's privileges. There is a difference between these two statements:

- `SHOW GRANTS` shows the privilege of the enabled role for the current user.
- `SHOW GRANTS FOR CURRENT_USER()` does not show the enabled role's privilege.

### Authorization table

In addition to four system [privilege tables](/reference/security/privilege-system.md#privilege-table), the RBAC system introduces two new system privilege tables:

- `mysql.role_edges`: records the authorization relationship of the role and user.
- `mysql.default_roles`: records default roles of each user.

#### `mysql.role_edges`

`mysql.role_edges` contains the following data:

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

- `FROM_HOST` and `FROM_USER` indicate the role's host name and user name respectively.
- `TO_HOST` and `TO_USER` indicate the host name and user name of the user to which a role is granted.

#### `mysql.default_roles`

`mysql.default_roles` shows which roles have been enabled by default for each user.

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

- `HOST` and `USER` indicate the user's host name and user name respectively.
- `DEFAULT_ROLE_HOST` and `DEFAULT_ROLE_USER` indicate the host name and user name of the default role respectively.

### References

Because RBAC, user management, and privilege management are closely related, you can refer to operation details in the following resources:

- [TiDB Privilege Management](/reference/security/privilege-system.md)
- [TiDB User Account Management](/reference/security/user-account-management.md)
