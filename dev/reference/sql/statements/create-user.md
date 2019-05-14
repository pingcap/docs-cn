---
title: CREATE USER | TiDB SQL Statement Reference 
summary: An overview of the usage of CREATE USER for the TiDB database.
category: reference
---

# CREATE USER

This statement creates a new user, specified with a password. In the MySQL privilege system, a user is the combination of a username and the host from which they are connecting from. Thus, it is possible to create a user `'newuser2'@'192.168.1.1'` who is only able to connect from the IP address `192.168.1.1`. It is also possible to have two users have the same user-portion, and different permissions as they login from different hosts.

## Synopsis

**CreateUserStmt:**

![CreateUserStmt](/media/sqlgram/CreateUserStmt.png)

**IfNotExists:**

![IfNotExists](/media/sqlgram/IfNotExists.png)

**UserSpecList:**

![UserSpecList](/media/sqlgram/UserSpecList.png)

**UserSpec:**

![UserSpec](/media/sqlgram/UserSpec.png)

**AuthOption:**

![AuthOption](/media/sqlgram/AuthOption.png)

**StringName:**

![StringName](/media/sqlgram/StringName.png)

## Examples

```sql
mysql> CREATE USER 'newuser' IDENTIFIED BY 'newuserpassword';
Query OK, 1 row affected (0.04 sec)

mysql> CREATE USER 'newuser2'@'192.168.1.1' IDENTIFIED BY 'newuserpassword';
Query OK, 1 row affected (0.02 sec)
```

## MySQL compatibility

* Several of the `CREATE` options are not yet supported by TiDB, and will be parsed but ignored.

## See also

* [Security Compatibility with MySQL](/dev/reference/security/compatibility.md)
* [DROP USER](/dev/reference/sql/statements/drop-user.md)
* [SHOW CREATE USER](/dev/reference/sql/statements/show-create-user.md)
* [ALTER USER](/dev/reference/sql/statements/alter-user.md)
* [Privilege Management](/dev/reference/security/privilege-system.md)

