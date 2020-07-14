---
title: SET [GLOBAL|SESSION] <variable> | TiDB SQL Statement Reference
summary: An overview of the usage of SET [GLOBAL|SESSION] <variable> for the TiDB database.
aliases: ['/docs/dev/sql-statements/sql-statement-set-variable/','/docs/dev/reference/sql/statements/set-variable/']
---

# `SET [GLOBAL|SESSION] <variable>`

The statement `SET [GLOBAL|SESSION]` modifies one of TiDB's built in variables, of either `SESSION` or `GLOBAL` scope. 

> **Note:**
>
> Similar to MySQL, changes to `GLOBAL` variables do not apply to either existing connections, or the local connection. Only new sessions reflect the changes to the value.

## Synopsis

**SetStmt:**

![SetStmt](/media/sqlgram/SetStmt.png)

**VariableAssignment:**

![VariableAssignment](/media/sqlgram/VariableAssignment.png)

## Examples

Get the value of `sql_mode`.

```sql
mysql> SHOW GLOBAL VARIABLES LIKE 'sql_mode';
+---------------+-------------------------------------------------------------------------------------------------------------------------------------------+
| Variable_name | Value                                                                                                                                     |
+---------------+-------------------------------------------------------------------------------------------------------------------------------------------+
| sql_mode      | ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION |
+---------------+-------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)

mysql> SHOW SESSION VARIABLES LIKE 'sql_mode';
+---------------+-------------------------------------------------------------------------------------------------------------------------------------------+
| Variable_name | Value                                                                                                                                     |
+---------------+-------------------------------------------------------------------------------------------------------------------------------------------+
| sql_mode      | ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION |
+---------------+-------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

Update the value of `sql_mode` globally.
If you check the value of `SQL_mode` after the update, you can see that the value of `SESSION` level has not been updated:

```sql
mysql> SET GLOBAL sql_mode = 'STRICT_TRANS_TABLES,NO_AUTO_CREATE_USER';
Query OK, 0 rows affected (0.03 sec)

mysql> SHOW GLOBAL VARIABLES LIKE 'sql_mode';
+---------------+-----------------------------------------+
| Variable_name | Value                                   |
+---------------+-----------------------------------------+
| sql_mode      | STRICT_TRANS_TABLES,NO_AUTO_CREATE_USER |
+---------------+-----------------------------------------+
1 row in set (0.00 sec)

mysql> SHOW SESSION VARIABLES LIKE 'sql_mode';
+---------------+-------------------------------------------------------------------------------------------------------------------------------------------+
| Variable_name | Value                                                                                                                                     |
+---------------+-------------------------------------------------------------------------------------------------------------------------------------------+
| sql_mode      | ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION |
+---------------+-------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

Using `SET SESSION` takes effect immediately:

```sql
mysql> SET SESSION sql_mode = 'STRICT_TRANS_TABLES,NO_AUTO_CREATE_USER';
Query OK, 0 rows affected (0.01 sec)

mysql> SHOW SESSION VARIABLES LIKE 'sql_mode';
+---------------+-----------------------------------------+
| Variable_name | Value                                   |
+---------------+-----------------------------------------+
| sql_mode      | STRICT_TRANS_TABLES,NO_AUTO_CREATE_USER |
+---------------+-----------------------------------------+
1 row in set (0.00 sec)
```

## MySQL compatibility

This statement is understood to be fully compatible with MySQL. Any compatibility differences should be [reported via an issue](/report-issue.md) on GitHub.

## See also

* [SHOW \[GLOBAL|SESSION\] VARIABLES](/sql-statements/sql-statement-show-variables.md)
