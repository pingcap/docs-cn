---
title: SESSION_VARIABLES
summary: Learn the `SESSION_VARIABLES` INFORMATION_SCHEMA table.
---

# SESSION_VARIABLES

The `SESSION_VARIABLES` table provides information about session variables. The table data is similar to the result of the `SHOW SESSION VARIABLES` statement.

```sql
USE INFORMATION_SCHEMA;
DESC SESSION_VARIABLES;
```

The output is as follows:

```sql
+----------------+---------------+------+------+---------+-------+
| Field          | Type          | Null | Key  | Default | Extra |
+----------------+---------------+------+------+---------+-------+
| VARIABLE_NAME  | varchar(64)   | YES  |      | NULL    |       |
| VARIABLE_VALUE | varchar(1024) | YES  |      | NULL    |       |
+----------------+---------------+------+------+---------+-------+
2 rows in set (0.00 sec)
```

Query the first 10 rows of the `SESSION_VARIABLES` table:

```sql
SELECT * FROM SESSION_VARIABLES ORDER BY variable_name LIMIT 10;
```

The output is as follows:

```sql
+-----------------------------------+------------------+
| VARIABLE_NAME                     | VARIABLE_VALUE   |
+-----------------------------------+------------------+
| allow_auto_random_explicit_insert | OFF              |
| auto_increment_increment          | 1                |
| auto_increment_offset             | 1                |
| autocommit                        | ON               |
| automatic_sp_privileges           | 1                |
| avoid_temporal_upgrade            | OFF              |
| back_log                          | 80               |
| basedir                           | /usr/local/mysql |
| big_tables                        | OFF              |
| bind_address                      | *                |
+-----------------------------------+------------------+
10 rows in set (0.00 sec)
```

The description of columns in the `SESSION_VARIABLES` table is as follows:

* `VARIABLE_NAME`: The name of the session-level variable in the database.
* `VARIABLE_VALUE`: The value of the session-level variable in the database.
