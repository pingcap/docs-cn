---
title: CREATE USER | TiDB SQL Statement Reference
summary: An overview of the usage of CREATE USER for the TiDB database.
aliases: ['/docs/dev/sql-statements/sql-statement-create-user/','/docs/dev/reference/sql/statements/create-user/']
---

# CREATE USER

This statement creates a new user, specified with a password. In the MySQL privilege system, a user is the combination of a username and the host from which they are connecting from. Thus, it is possible to create a user `'newuser2'@'192.168.1.1'` who is only able to connect from the IP address `192.168.1.1`. It is also possible to have two users have the same user-portion, and different permissions as they login from different hosts.

## Synopsis

```ebnf+diagram
CreateUserStmt ::=
    'CREATE' 'USER' IfNotExists UserSpecList RequireClauseOpt ConnectionOptions PasswordOrLockOptions

IfNotExists ::=
    ('IF' 'NOT' 'EXISTS')?

UserSpecList ::=
    UserSpec ( ',' UserSpec )*

UserSpec ::=
    Username AuthOption

AuthOption ::=
    ( 'IDENTIFIED' ( 'BY' ( AuthString | 'PASSWORD' HashString ) | 'WITH' StringName ( 'BY' AuthString | 'AS' HashString )? ) )?

StringName ::=
    stringLit
|   Identifier
```

## Examples

Create a user with the `newuserpassword` password.

```sql
mysql> CREATE USER 'newuser' IDENTIFIED BY 'newuserpassword';
Query OK, 1 row affected (0.04 sec)
```

Create a user who can only log in to `192.168.1.1`.

```sql
mysql> CREATE USER 'newuser2'@'192.168.1.1' IDENTIFIED BY 'newuserpassword';
Query OK, 1 row affected (0.02 sec)
```

Create a user who is enforced to log in using TLS connection.

```sql
CREATE USER 'newuser3'@'%' REQUIRE SSL IDENTIFIED BY 'newuserpassword';
Query OK, 1 row affected (0.02 sec)
```

Create a user who is required to use X.509 certificate at login.

```sql
CREATE USER 'newuser4'@'%' REQUIRE ISSUER '/C=US/ST=California/L=San Francisco/O=PingCAP' IDENTIFIED BY 'newuserpassword';
Query OK, 1 row affected (0.02 sec)
```

## MySQL compatibility

The following `CREATE USER` options are not yet supported by TiDB, and will be parsed but ignored:

* TiDB does not support `WITH MAX_QUERIES_PER_HOUR`, `WITH MAX_UPDATES_PER_HOUR`, and `WITH MAX_USER_CONNECTIONS` options.
* TiDB does not support the `DEFAULT ROLE` option.
* TiDB does not support `PASSWORD EXPIRE`, `PASSWORD HISTORY` or other options related to password.
* TiDB does not support the `ACCOUNT LOCK` and `ACCOUNT UNLOCK` options.

## See also

* [Security Compatibility with MySQL](/security-compatibility-with-mysql.md)
* [DROP USER](/sql-statements/sql-statement-drop-user.md)
* [SHOW CREATE USER](/sql-statements/sql-statement-show-create-user.md)
* [ALTER USER](/sql-statements/sql-statement-alter-user.md)
* [Privilege Management](/privilege-management.md)
