---
title: SESSION_VARIABLES
summary: Learn the `SESSION_VARIABLES` information_schema table.
---

# SESSION_VARIABLES

The `SESSION_VARIABLES` table provides information about session variables. The table data is similar to the result of the `SHOW SESSION VARIABLES` statement.

{{< copyable "sql" >}}

```sql
USE information_schema;
DESC session_variables;
```

```
+----------------+---------------+------+------+---------+-------+
| Field          | Type          | Null | Key  | Default | Extra |
+----------------+---------------+------+------+---------+-------+
| VARIABLE_NAME  | varchar(64)   | YES  |      | NULL    |       |
| VARIABLE_VALUE | varchar(1024) | YES  |      | NULL    |       |
+----------------+---------------+------+------+---------+-------+
2 rows in set (0.00 sec)
```

{{< copyable "sql" >}}

```sql
SELECT * FROM session_variables ORDER BY variable_name LIMIT 10;
```

```
+-----------------------------------+------------------+
| VARIABLE_NAME                     | VARIABLE_VALUE   |
+-----------------------------------+------------------+
| allow_auto_random_explicit_insert | off              |
| auto_increment_increment          | 1                |
| auto_increment_offset             | 1                |
| autocommit                        | 1                |
| automatic_sp_privileges           | 1                |
| avoid_temporal_upgrade            | 0                |
| back_log                          | 80               |
| basedir                           | /usr/local/mysql |
| big_tables                        | 0                |
| bind_address                      | *                |
+-----------------------------------+------------------+
10 rows in set (0.00 sec)
```

The description of columns in the `SESSION_VARIABLES` table is as follows:

* `VARIABLE_NAME`: The name of the session-level variable in the database.
* `VARIABLE_VALUE`: The value of the session-level
variable in the database.
