---
title: Privilege Management
category: user guide
---

# Privilege Management

## Privilege management overview

TiDB's privilege management system is implemented according to the privilege management system in MySQL. It supports most of the syntaxes and privilege types in MySQL. If you find any inconsistency with MySQL, feel free to [open an issue](https://github.com/pingcap/docs-cn/issues/new).

## Examples

### User account operation

TiDB user account names consist of a user name and a host name. The account name syntax is `'user_name'@'host_name'`.

- The `user_name` is case sensitive.
- The `host_name` can be a host name or an IP address. The `%` and `_` wildcard characters are permitted in host name or IP address values. For example, a host value of `'%'` matches any host name and `'192.168.1.%'` matches every host on a subnet.

#### Create user

The `CREATE USER` statement creates new MySQL accounts.

```sql
create user 'test'@'127.0.0.1' identified by 'xxx';
```

If the host name is not specified, you can log in from any IP address. If the password is not specified, it is empty by default:

```sql
create user 'test';
```

Equals:

```sql
create user 'test'@'%' identified by '';
```

**Required Privilege:** To use `CREATE USER`, you must have the global `CREATE USER` privilege.

#### Change the password

You can use the `SET PASSWORD` syntax to assign or modify a password to a user account.

```sql
set password for 'root'@'%' = 'xxx';
```

**Required Privilege:** Operations that assign or modify passwords are permitted only to users with the `CREATE USER` privilege.

#### Drop user

The `DROP USER` statement removes one or more MySQL accounts and their privileges. It removes the user record entries in the `mysql.user` table and the privilege rows for the account from all grant tables.

```sql
drop user 'test'@'%';
```
**Required Privilege:** To use `DROP USER`, you must have the global `CREATE USER` privilege.

#### Reset the root password

If you forget the root password, you can skip the privilege system and use the root privilege to reset the password.

To reset the root password,

1. Start TiDB with a special startup option (root privilege required)：

    ```bash
    sudo ./tidb-server -skip-grant-table=true
    ```

2. Use the root account to log in and reset the password:

    ```base
    mysql -h 127.0.0.1 -P 4000 -u root
    ```

### Privilege-related operations

#### Grant privileges

The `GRANT` statement grants privileges to the user accounts.

For example, use the following statement to grant the `xxx` user the privilege to read the `test` database.

```sql
grant Select on test.* to 'xxx'@'%';
```

Use the following statement to grant the `xxx` user all privileges on all databases:

```
grant all privileges on *.* to 'xxx'@'%';
```

If the granted user does not exist, TiDB will automatically create a user.

```
mysql> select * from mysql.user where user='xxxx';
Empty set (0.00 sec)

mysql> grant all privileges on test.* to 'xxxx'@'%' identified by 'yyyyy';
Query OK, 0 rows affected (0.00 sec)

mysql> select user,host from mysql.user where user='xxxx';
+------|------+
| user | host |
+------|------+
| xxxx | %    |
+------|------+
1 row in set (0.00 sec)
```

In this example, `xxxx@%` is the user that is automatically created.

> **Note:** Granting privileges to a database or table does not check if the database or table exists.

```
mysql> select * from test.xxxx;
ERROR 1146 (42S02): Table 'test.xxxx' doesn't exist

mysql> grant all privileges on test.xxxx to xxxx;
Query OK, 0 rows affected (0.00 sec)

mysql> select user,host from mysql.tables_priv where user='xxxx';
+------|------+
| user | host |
+------|------+
| xxxx | %    |
+------|------+
1 row in set (0.00 sec)
```

You can use fuzzy matching to grant privileges to databases and tables.

```
mysql> grant all privileges on `te%`.* to genius;
Query OK, 0 rows affected (0.00 sec)

mysql> select user,host,db from mysql.db where user='genius';
+--------|------|-----+
| user   | host | db  |
+--------|------|-----+
| genius | %    | te% |
+--------|------|-----+
1 row in set (0.00 sec)
```

In this example, because of the `%` in `te%`, all the databases starting with `te` are granted the privilege.

#### Revoke privileges

The `REVOKE` statement enables system administrators to revoke privileges from the user accounts.

The `REVOKE` statement corresponds with the `REVOKE` statement:

```sql
revoke all privileges on `test`.* from 'genius'@'localhost';
```

> **Note:** To revoke privileges, you need the exact match. If the matching result cannot be found, an error will be displayed:

    ```
    mysql> revoke all privileges on `te%`.* from 'genius'@'%';
    ERROR 1141 (42000): There is no such grant defined for user 'genius' on host '%'
    ```

About fuzzy matching, escape, string and identifier:

```sql
mysql> grant all privileges on `te\%`.* to 'genius'@'localhost';
Query OK, 0 rows affected (0.00 sec)
```

This example uses exact match to find the database named `te%`. Note that the `%` uses the `\` escape character so that `%` is not considered as a wildcard.

A string is enclosed in single quotation marks(''), while an identifier is enclosed in backticks (``). See the differences below:

```sql
mysql> grant all privileges on 'test'.* to 'genius'@'localhost';
ERROR 1064 (42000): You have an error in your SQL syntax; check the
manual that corresponds to your MySQL server version for the right
syntax to use near ''test'.* to 'genius'@'localhost'' at line 1

mysql> grant all privileges on `test`.* to 'genius'@'localhost';
Query OK, 0 rows affected (0.00 sec)
```

If you want to use special keywords as table names, enclose them in backticks (``). For example:

```sql
mysql> create table `select` (id int);
Query OK, 0 rows affected (0.27 sec)
```

#### Check privileges granted to user

You can use the `show grant` statement to see what privileges are granted to a user.

```sql
show grants for 'root'@'%';
```

To be more precise, you can check the privilege information in the `Grant` table. For example, you can use the following steps to check if the `test@%` user has the `Insert` privilege on `db1.t`:

1. Check if `test@%` has global `Insert` privilege:

    ```sql
    select Insert from mysql.user where user='test' and host='%';
    ```

2. If not, check if `test@%` has database-level `Insert` privilege at `db1`:

    ```sql
    select Insert from mysql.db where user='test' and host='%';
    ```

3. If the result is still empty, check whether `test@%` has table-level `Insert` privilege at `db1.t`:

    ```sql
    select tables_priv from mysql.tables_priv where user='test' and host='%' and db='db1';
    ```

### Implementation of the privilege system

#### Grant table

The following system tables are special because all the privilege-related data is stored in them:

- mysql.user (user account, global privilege)
- mysql.db (database-level privilege)
- mysql.tables_priv (table-level privilege)
- mysql.columns_priv (column-level privilege)

These tables contain the effective range and privilege information of the data. For example, in the `mysql.user` table:

```sql
mysql> select User,Host,Select_priv,Insert_priv from mysql.user limit 1;
+------|------|-------------|-------------+
| User | Host | Select_priv | Insert_priv |
+------|------|-------------|-------------+
| root | %    | Y           | Y           |
+------|------|-------------|-------------+
1 row in set (0.00 sec)
```

In this record, `Host` and `User` determine that the connection request sent by the `root` user from any host (`%`) can be accepted. `Select_priv` and `Insert_priv` mean that the user has global `Select` and `Insert` privilege. The effective range in the `mysql.user` table is global.

`Host` and `User` in `mysql.db` determine which databases users can access. The effective range is the database.

In theory, all privilege-related operations can be done directly by the CRUD operations on the grant table.

On the implementation level, only a layer of syntactic sugar is added. For example, you can use the following command to remove a user:

```
delete from mysql.user where user='test';
```

However, it’s not recommended to manually modify the grant table.

#### Connection verification

When the client sends a connection request, TiDB server will verify the login operation. TiDB server first checks the `mysql.user` table. If a record of `User` and `Host` matches the connection request, TiDB server then verifies the `Password`.

User identity is based on two pieces of information: `Host`, the host that initiates the connection, and `User`, the user name. If the user name is not empty, the exact match of user named is a must.

`User`+`Host` may match several rows in `user` table. To deal with this scenario, the rows in the `user` table are sorted. The table rows will be checked one by one when the client connects; the first matched row will be used to verify. When sorting, Host is ranked before User.

#### Request verification

When the connection is successful, the request verification process checks whether the operation has the privilege.

For database-related requests (INSERT, UPDATE), the request verification process first checks the user’s global privileges in the `mysql.user` table. If the privilege is granted, you can access directly. If not, check the `mysql.db` table.

The `user` table has global privileges regardless of the default database. For example, the `DELETE` privilege in `user` can apply to any row, table, or database.

In the `Db` table, an empty user is to match the anonymous user name. Wildcards are not allowed in the `User` column. The value for the `Host` and `Db` columns can use `%` and `_`, which can use pattern matching.

Data in the `user` and `db` tables is also sorted when loaded into memory.

The use of `%` in `tables_priv` and `columns_priv` is similar, but column value in `Db`, `Table_name` and `Column_name` cannot contain `%`. The sorting is also similar when loaded.

#### Time of effect

When TiDB starts, some privilege-check tables are loaded into memory, and then the cached data is used to verify the privileges. The system will periodically synchronize the `grant` table from database to cache. Time of effect is determined by the synchronization cycle. Currently, the value is 5 minutes.

If an immediate effect is needed when you modify the `grant` table, you can run the following command:

```sql
flush privileges
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

**Note:** The column-level privilege is not implemented at this stage.

## `Create User` statement

```sql
CREATE USER [IF NOT EXISTS]
    user [auth_spec] [, user [auth_spec]] ...
auth_spec: {
    IDENTIFIED BY 'auth_string'
  | IDENTIFIED BY PASSWORD 'hash_string'
}
```

For more information about the user account, see [TiDB user account management](user-account-management.md).

- IDENTIFIED BY `auth_string`

  When you set the login password, `auth_string` is encrypted by TiDB and stored in the `mysql.user` table.

- IDENTIFIED BY PASSWORD `hash_string`

  When you set the login password, `hash_string` is encrypted by TiDB and stored in the `mysql.user` table. Currently, this is not the same as MySQL.
