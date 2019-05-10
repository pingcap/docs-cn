---
title: TiDB User Account Management
summary: Learn how to manage a TiDB user account.
category: user guide
---

# TiDB User Account Management

This document describes how to manage a TiDB user account.

## User names and passwords

TiDB stores the user accounts in the table of the `mysql.user` system database. Each account is identified by a user name and the client host. Each account may have a password.

You can connect to the TiDB server using the MySQL client, and use the specified account and password to login:

```sql
shell> mysql --port 4000 --user xxx --password
```

Or use the abbreviation of command line parameters:
   
```sql
shell> mysql -P 4000 -u xxx -p
```

## Add user accounts

You can create TiDB accounts in two ways:

- By using the standard account-management SQL statements intended for creating accounts and establishing their privileges, such as `CREATE USER` and `GRANT`. 
- By manipulating the grant tables directly with statements such as `INSERT`, `UPDATE`, or `DELETE`. 

It is recommended to use the account-management statements, because manipulating the grant tables directly can lead to incomplete updates. You can also create accounts by using third party GUI tools.

The following example uses the `CREATE USER` and `GRANT` statements to set up four accounts: 

```sql
mysql> CREATE USER 'finley'@'localhost' IDENTIFIED BY 'some_pass';
mysql> GRANT ALL PRIVILEGES ON *.* TO 'finley'@'localhost' WITH GRANT OPTION;
mysql> CREATE USER 'finley'@'%' IDENTIFIED BY 'some_pass';
mysql> GRANT ALL PRIVILEGES ON *.* TO 'finley'@'%' WITH GRANT OPTION;
mysql> CREATE USER 'admin'@'localhost' IDENTIFIED BY 'admin_pass';
mysql> GRANT RELOAD,PROCESS ON *.* TO 'admin'@'localhost';
mysql> CREATE USER 'dummy'@'localhost';
```

To see the privileges for an account, use `SHOW GRANTS`:

```sql
mysql> SHOW GRANTS FOR 'admin'@'localhost';
+-----------------------------------------------------+
| Grants for admin@localhost                          |
+-----------------------------------------------------+
| GRANT RELOAD, PROCESS ON *.* TO 'admin'@'localhost' |
+-----------------------------------------------------+
```

## Remove user accounts

To remove a user account, use the `DROP USER` statement:

```sql
mysql> DROP USER 'test'@'localhost';
```

## Reserved user accounts

TiDB creates the `'root'@'%'` default account during the database initialization. 

## Set account resource limits

Currently, TiDB does not support setting account resource limits.

## Assign account passwords

TiDB stores passwords in the `mysql.user` system database. Operations that assign or update passwords are permitted only to users with the `CREATE USER` privilege, or, alternatively, privileges for the `mysql` database (`INSERT` privilege to create new accounts, `UPDATE` privilege to update existing accounts).  

- To assign a password when you create a new account, use `CREATE USER` and include an `IDENTIFIED BY` clause: 

    ```sql
    CREATE USER 'test'@'localhost' IDENTIFIED BY 'mypass';
    ```

- To assign or change a password for an existing account, use `SET PASSWORD FOR` or `ALTER USER`:

    ```sql
    SET PASSWORD FOR 'root'@'%' = 'xxx';
    ```

    Or:

    ```sql
    ALTER USER 'test'@'localhost' IDENTIFIED BY 'mypass';
    ```

## Forget the `root` password

1. Modify the configuration file by adding `skip-grant-table` in the `security` part:

    ```
    [security]
    skip-grant-table = true
    ```

2. Restart TiDB using the modified configuration (the `root` privilege is required):

    ```bash
    sudo ./tidb-server -skip-grant-table=true -store=tikv -path=...
    ```

    By using the `skip-grant-table` configuration parameter, TiDB skips the privilege system.

3. Use `root` to log in and then modify the password:

    ```bash
    mysql -h 127.0.0.1 -P 4000 -u root
    ```

## `FLUSH PRIVILEGES` 

If you modified the grant tables directly, run the following command to apply changes immediately:

```sql
FLUSH PRIVILEGES;
```

For details, see [Privilege Management](../sql/privilege.md).
