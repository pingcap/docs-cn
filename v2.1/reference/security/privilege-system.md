---
title: Privilege Management
summary: Learn how to manage the privilege.
category: reference
---

# Privilege Management

TiDB supports MySQL 5.7's privilege management system, including the syntax and privilege types. Starting with TiDB 3.0, support for SQL Roles is also available.

This document introduces privilege-related TiDB operations, privileges required for TiDB operations and implementation of the privilege system.

## Privilege-related operations

### Grant privileges

The `GRANT` statement grants privileges to user accounts. It is recommended to first create a user, and then grant privileges. For example, use the following statement to grant the `developer` user the privilege to read the `test` database:

```sql
CREATE USER developer IDENTIFIED BY 'mypassword';
GRANT SELECT ON test.* TO 'developer';
```

Use the following statement to grant the `developer` user all privileges on all databases:

```sql
GRANT ALL PRIVILEGES ON *.* TO 'developer';
```

> **Warning：**
>
> TiDB 2.1 does not support the `NO_AUTO_CREATE_USER` SQL Mode. This means that TiDB will automatically create a new user if one does not already exist.
> This is particularly risky, since typos can lead to users created with an empty password. While this behavior is compatible with earlier releases of MySQL, it is recommended to upgrade to TiDB 3.0 to prevent this issue.

> **Note:**
>
> Granting privileges to a database or table does not check if the database or table exists.

```sql
mysql> SELECT * FROM test.xxxx;
ERROR 1146 (42S02): Table 'test.xxxx' doesn't exist

mysql> GRANT ALL PRIVILEGES ON test.xxxx TO xxxx;
Query OK, 0 rows affected (0.00 sec)

mysql> SELECT user,host FROM mysql.tables_priv WHERE user='xxxx';
+------|------+
| user | host |
+------|------+
| xxxx | %    |
+------|------+
1 row in set (0.00 sec)
```

You can use fuzzy matching to grant privileges to databases and tables.

```sql
mysql> GRANT ALL PRIVILEGES ON `te%`.* TO genius;
Query OK, 0 rows affected (0.00 sec)

mysql> SELECT user,host,db FROM mysql.db WHERE user='genius';
+--------|------|-----+
| user   | host | db  |
+--------|------|-----+
| genius | %    | te% |
+--------|------|-----+
1 row in set (0.00 sec)
```

In this example, because of the `%` in `te%`, all the databases starting with `te` are granted the privilege.

### Revoke privileges

The `REVOKE` statement enables system administrators to revoke privileges from the user accounts.

The `REVOKE` statement corresponds with the `REVOKE` statement:

```sql
REVOKE ALL PRIVILEGES ON `test`.* FROM 'genius'@'localhost';
```

> **Note:**
>
> To revoke privileges, you need the exact match. If the matching result cannot be found, an error will be displayed:

```sql
mysql> REVOKE ALL PRIVILEGES ON `te%`.* FROM 'genius'@'%';
ERROR 1141 (42000): There is no such grant defined for user 'genius' on host '%'
```

About fuzzy matching, escape, string and identifier:

```sql
mysql> GRANT ALL PRIVILEGES ON `te\%`.* TO 'genius'@'localhost';
Query OK, 0 rows affected (0.00 sec)
```

This example uses exact match to find the database named `te%`. Note that the `%` uses the `\` escape character so that `%` is not considered as a wildcard.

A string is enclosed in single quotation marks(''), while an identifier is enclosed in backticks (``). See the differences below:

```sql
mysql> GRANT ALL PRIVILEGES ON 'test'.* TO 'genius'@'localhost';
ERROR 1064 (42000): You have an error in your SQL syntax; check the
manual that corresponds to your MySQL server version for the right
syntax to use near ''test'.* to 'genius'@'localhost'' at line 1

mysql> GRANT ALL PRIVILEGES ON `test`.* TO 'genius'@'localhost';
Query OK, 0 rows affected (0.00 sec)
```

If you want to use special keywords as table names, enclose them in backticks (``). For example:

```sql
mysql> CREATE TABLE `select` (id int);
Query OK, 0 rows affected (0.27 sec)
```

### Check privileges granted to users

You can use the `SHOW GRANTS` statement to see what privileges are granted to a user. For example:

```sql
SHOW GRANTS; -- show grants for the current user
SHOW GRANTS FOR 'root'@'%'; -- show grants for a specific user
```

To be more precise, you can check the privilege information in the `Grant` table. For example, you can use the following steps to check if the `test@%` user has the `Insert` privilege on `db1.t`:

1. Check if `test@%` has global `Insert` privilege:

    ```sql
    SELECT Insert_priv FROM mysql.user WHERE user='test' AND host='%';
    ```

2. If not, check if `test@%` has database-level `Insert` privilege at `db1`:

    ```sql
    SELECT Insert_priv FROM mysql.db WHERE user='test' AND host='%';
    ```

3. If the result is still empty, check whether `test@%` has table-level `Insert` privilege at `db1.t`:

    ```sql
    SELECT table_priv FROM mysql.tables_priv WHERE user='test' AND host='%' AND db='db1';
    ```

## Privileges required for TiDB operations

You can check privileges of TiDB users in the `INFORMATION_SCHEMA.USER_PRIVILEGES` table.

| Privilege type       |  Privilege variable    | Privilege description                 |
| :------------ | :------------ | :---------------------- |
| ALL            | `AllPriv`        | All the privileges                 |
| Drop           | `DropPriv`      | Deletes a schema or table        |
| Index          | `IndexPriv`      | Creates or deletes an index          |
| Alter          | `AlterPriv`      | Executes the `ALTER` statement          |
| Super          | `SuperPriv`      | All the privileges                 |
| Grant          | `GrantPriv`      | Grants another user a privilege         |
| Create         | `CreatePriv`     | Creates a schema or table        |
| Select         | `SelectPriv`     | Reads the table data               |
| Insert         | `InsertPriv`     | Inserts data to a table             |
| Update         | `UpdatePriv`     | Updates the table data             |
| Delete         | `DeletePriv`     | Deleted the table data             |
| Trigger        | `TriggerPriv`    | /                 |
| Process        | `ProcessPriv`    | Displays the running task       |
| Execute        | `ExecutePriv`    | Executes the `EXECUTE` statement       |
| Drop Role      | `DropRolePriv`   | Executes `DROP ROLE`           |
| Show View      | `ShowViewPriv`   | Executes `SHOW CREATE VIEW`    |
| References     | `ReferencesPriv` | /                |
| Create View    | `CreateViewPriv` | Creates a View                 |
| Create User    | `CreateUserPriv` | Creates a user                |
| Create Role    | `CreateRolePriv` | Executes `CREATE ROLE`         |
| Show Databases | `ShowDBPriv`     | Shows the table status in the database |

### ALTER

- For all `ALTER` statements, users must have the `ALTER` privilege for the corresponding table.
- For statements except `ALTER...DROP` and `ALTER...RENAME TO`, users must have the `INSERT` and `CREATE` privileges for the corresponding table.
- For the `ALTER...DROP` statement, users must have the `DROP` privilege for the corresponding table.
- For the `ALTER...RENAME TO` statement, users must have the `DROP` privilege for the table before renaming, and the `CREATE` and `INSERT` privileges for the table after renaming.

> **Note:**
>
> In MySQL 5.7 documentation, users need `INSERT` and `CREATE` privileges to perform the `ALTER` operation on a table. But in reality for MySQL 5.7.25, only the `ALTER` privilege is required in this case. Currently, the `ALTER` privilege in TiDB is consistent with the actual behavior in MySQL.

### CREATE DATABASE

Requires the `CREATE` privilege for the database.

### CREATE INDEX

Requires the `INDEX` privilege for the table.

### CREATE TABLE

Requires the `CREATE` privilege for the table.

To execute the `CREATE TABLE...LIKE...` statement, the `SELECT` privilege for the table is required.

### CREATE VIEW

Requires the `CREATE VIEW` privilege.

> **Note:**
>
> If the current user is not the user that creates the View, both the `CREATE VIEW` and `SUPER` privileges are required.

### DROP DATABASE

Requires the `DROP` privilege for the table.

### DROP INDEX

Requires the `INDEX` privilege for the table.

### DROP TABLES

Requires the `DROP` privilege for the table.

### TRUNCATE TABLE

Requires the `DROP` privilege for the table.

### RENAME TABLE

Requires the `ALTER` and `DROP` privileges for the table before renaming and the `CREATE` and `INSERT` privileges for the table after renaming.

### ANALYZE TABLE

Requires the `INSERT` and `SELECT` privileges for the table.

### SHOW

`SHOW CREATE TABLE` requires any single privilege to the table.

`SHOW CREATE VIEW` requires the `SHOW VIEW` privilege.

### CREATE ROLE/USER

`CREATE ROLE` requires the `CREATE ROLE` privilege.

`CREATE USER` requires the `CREATE USER` privilege.

### DROP ROLE/USER

`DROP ROLE` requires the `DROP ROLE` privilege.

`DROP USER` requires the `CREATE USER` privilege.

### ALTER USER

Requires the `CREATE USER` privilege.

### GRANT

Requires the `GRANT` privilege with the privileges granted by `GRANT`.

### REVOKE

Requires the `SUPER` privilege.

## Implementation of the privilege system

### Grant table

The following system tables are special because all the privilege-related data is stored in them:

- mysql.user (user account, global privilege)
- mysql.db (database-level privilege)
- mysql.tables_priv (table-level privilege)
- mysql.columns_priv (column-level privilege; not currently supported)

These tables contain the effective range and privilege information of the data. For example, in the `mysql.user` table:

```sql
mysql> SELECT User,Host,Select_priv,Insert_priv FROM mysql.user LIMIT 1;
+------|------|-------------|-------------+
| User | Host | Select_priv | Insert_priv |
+------|------|-------------|-------------+
| root | %    | Y           | Y           |
+------|------|-------------|-------------+
1 row in set (0.00 sec)
```

In this record, `Host` and `User` determine that the connection request sent by the `root` user from any host (`%`) can be accepted. `Select_priv` and `Insert_priv` mean that the user has global `Select` and `Insert` privilege. The effective range in the `mysql.user` table is global.

`Host` and `User` in `mysql.db` determine which databases users can access. The effective range is the database.

> **Note:**
>
> It is recommended to only update the privilege tables via the supplied syntax such as `GRANT`, `CREATE USER` and `DROP USER`. Making direct edits to the underlying privilege tables will not automatially update the privilege cache, leading to unpredictable behavior until `FLUSH PRIVILEGES` is executed.

### Connection verification

When the client sends a connection request, TiDB server will verify the login operation. TiDB server first checks the `mysql.user` table. If a record of `User` and `Host` matches the connection request, TiDB server then verifies the `Password`.

User identity is based on two pieces of information: `Host`, the host that initiates the connection, and `User`, the user name. If the user name is not empty, the exact match of user named is a must.

`User`+`Host` may match several rows in `user` table. To deal with this scenario, the rows in the `user` table are sorted. The table rows will be checked one by one when the client connects; the first matched row will be used to verify. When sorting, Host is ranked before User.

### Request verification

When the connection is successful, the request verification process checks whether the operation has the privilege.

For database-related requests (`INSERT`, `UPDATE`), the request verification process first checks the user’s global privileges in the `mysql.user` table. If the privilege is granted, you can access directly. If not, check the `mysql.db` table.

The `user` table has global privileges regardless of the default database. For example, the `DELETE` privilege in `user` can apply to any row, table, or database.

In the `Db` table, an empty user is to match the anonymous user name. Wildcards are not allowed in the `User` column. The value for the `Host` and `Db` columns can use `%` and `_`, which can use pattern matching.

Data in the `user` and `db` tables is also sorted when loaded into memory.

The use of `%` in `tables_priv` and `columns_priv` is similar, but column value in `Db`, `Table_name` and `Column_name` cannot contain `%`. The sorting is also similar when loaded.

### Time of effect

When TiDB starts, some privilege-check tables are loaded into memory, and then the cached data is used to verify the privileges. Executing privilege management statements such as `GRANT`, `REVOKE`, `CREATE USER`, `DROP USER` will take effect immediately.

Manually editing tables such as `mysql.user` with statements such as `INSERT`, `DELETE`, `UPDATE` will not take effect immediately. This behavior is compatible with MySQL, and privilege cache can be updated with the following statement:

```sql
FLUSH PRIVILEGES;
```

### Limitations and constraints

Currently, the following privileges are not checked yet because they are less frequently used:

- FILE
- USAGE
- SHUTDOWN
- EXECUTE
- PROCESS
- INDEX
- ...

> **Note:**
>
> Column-level privileges are not implemented at this stage.
