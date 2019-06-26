---
title: GRANT <privileges> | TiDB SQL Statement Reference 
summary: An overview of the usage of GRANT <privileges> for the TiDB database.
category: reference
---

# GRANT <privileges>

This statement allocates privileges to a pre-existing user in TiDB. The privilege system in TiDB follows MySQL, where credentials are assigned based on a database/table pattern.

## Synopsis

**GrantStmt:**

![GrantStmt](/media/sqlgram-v3.0/GrantStmt.png)

**PrivElemList:**

![PrivElemList](/media/sqlgram-v3.0/PrivElemList.png)

**PrivElem:**

![PrivElem](/media/sqlgram-v3.0/PrivElem.png)

**PrivType:**

![PrivType](/media/sqlgram-v3.0/PrivType.png)

**ObjectType:**

![ObjectType](/media/sqlgram-v3.0/ObjectType.png)

**PrivLevel:**

![PrivLevel](/media/sqlgram-v3.0/PrivLevel.png)

**UserSpecList:**

![UserSpecList](/media/sqlgram-v3.0/UserSpecList.png)

## Examples

```sql
mysql> CREATE USER newuser IDENTIFIED BY 'mypassword';
Query OK, 1 row affected (0.02 sec)

mysql> GRANT ALL ON test.* TO 'newuser';
Query OK, 0 rows affected (0.03 sec)

mysql> SHOW GRANTS FOR 'newuser';
+-------------------------------------------------+
| Grants for newuser@%                            |
+-------------------------------------------------+
| GRANT USAGE ON *.* TO 'newuser'@'%'             |
| GRANT ALL PRIVILEGES ON test.* TO 'newuser'@'%' |
+-------------------------------------------------+
2 rows in set (0.00 sec)
```

## MySQL compatibility

* Similar to MySQL, the `USAGE` privilege denotes the ability to log into a TiDB server.
* Column level privileges are not currently supported.
* Similar to MySQL, when the `NO_AUTO_CREATE_USER` sql mode is not present, the `GRANT` statement will automatically create a new user with an empty password when a user does not exist. Removing this sql-mode (it is enabled by default) presents a security risk.

## See also

* [REVOKE <privileges>](/reference/sql/statements/revoke-privileges.md)
* [SHOW GRANTS](/reference/sql/statements/show-grants.md)
* [Privilege Management](/reference/security/privilege-system.md)

