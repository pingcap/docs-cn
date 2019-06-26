---
title: DROP USER | TiDB SQL Statement Reference 
summary: An overview of the usage of DROP USER for the TiDB database.
category: reference
---

# DROP USER

This statement removes a user from the TiDB system database. The optional keyword `IF EXISTS` can be used to silence an error if the user does not exist.

## Synopsis

**DropUserStmt:**

![DropUserStmt](/media/sqlgram-dev/DropUserStmt.png)

**Username:**

![Username](/media/sqlgram-dev/Username.png)


## Examples

```sql
mysql> DROP USER idontexist;
ERROR 1396 (HY000): Operation DROP USER failed for idontexist@%

mysql> DROP USER IF EXISTS idontexist;
Query OK, 0 rows affected (0.01 sec)

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

mysql> REVOKE ALL ON test.* FROM 'newuser';
Query OK, 0 rows affected (0.03 sec)

mysql> SHOW GRANTS FOR 'newuser';
+-------------------------------------+
| Grants for newuser@%                |
+-------------------------------------+
| GRANT USAGE ON *.* TO 'newuser'@'%' |
+-------------------------------------+
1 row in set (0.00 sec)

mysql> DROP USER newuser;
Query OK, 0 rows affected (0.14 sec)

mysql> SHOW GRANTS FOR newuser;
ERROR 1141 (42000): There is no such grant defined for user 'newuser' on host '%'
```

## MySQL compatibility

* Dropping a user that does not exist with `IF EXISTS` will not create a warning in TiDB. [Issue #10196](https://github.com/pingcap/tidb/issues/10196).

## See also

* [CREATE USER](/reference/sql/statements/create-user.md)
* [ALTER USER](/reference/sql/statements/alter-user.md)
* [SHOW CREATE USER](/reference/sql/statements/show-create-user.md)
* [Privilege Management](/reference/security/privilege-system.md)

