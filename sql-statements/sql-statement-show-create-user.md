---
title: SHOW CREATE USER | TiDB SQL Statement Reference
summary: An overview of the usage of SHOW CREATE USER for the TiDB database.
aliases: ['/docs/dev/sql-statements/sql-statement-show-create-user/','/docs/dev/reference/sql/statements/show-create-user/']
---

# SHOW CREATE USER

This statement shows how to re-create a user using the `CREATE USER` syntax.

## Synopsis

**ShowCreateUserStmt:**

![ShowCreateUserStmt](/media/sqlgram/ShowCreateUserStmt.png)

**Username:**

![Username](/media/sqlgram/Username.png)

## Examples

```sql
mysql> SHOW CREATE USER 'root';
+--------------------------------------------------------------------------------------------------------------------------+
| CREATE USER for root@%                                                                                                   |
+--------------------------------------------------------------------------------------------------------------------------+
| CREATE USER 'root'@'%' IDENTIFIED WITH 'mysql_native_password' AS '' REQUIRE NONE PASSWORD EXPIRE DEFAULT ACCOUNT UNLOCK |
+--------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)

mysql> SHOW GRANTS FOR 'root';
+-------------------------------------------+
| Grants for root@%                         |
+-------------------------------------------+
| GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' |
+-------------------------------------------+
1 row in set (0.00 sec)
```

## MySQL compatibility

* The output of `SHOW CREATE USER` is designed to match MySQL, but several of the `CREATE` options are not yet supported by TiDB.  Not yet supported options will be parsed but ignored. See [security compatibility] for more details.

## See also

* [CREATE USER](/sql-statements/sql-statement-create-user.md)
* [SHOW GRANTS](/sql-statements/sql-statement-show-grants.md)
* [DROP USER](/sql-statements/sql-statement-drop-user.md)
