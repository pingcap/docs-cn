---
title: VARIABLES_INFO
summary: Learn the `VARIABLES_INFO` information_schema table.
---

# VARIABLES_INFO

The `VARIABLES_INFO` table provides information about the default value, current value, and scope of system variables in the current TiDB instance or TiDB cluster.

```sql
USE information_schema;
DESC variables_info;
```

```sql
+-----------------+---------------------+------+------+---------+-------+
| Field           | Type                | Null | Key  | Default | Extra |
+-----------------+---------------------+------+------+---------+-------+
| VARIABLE_NAME   | varchar(64)         | NO   |      | NULL    |       |
| VARIABLE_SCOPE  | varchar(64)         | NO   |      | NULL    |       |
| DEFAULT_VALUE   | varchar(64)         | NO   |      | NULL    |       |
| CURRENT_VALUE   | varchar(64)         | NO   |      | NULL    |       |
| MIN_VALUE       | bigint(64)          | YES  |      | NULL    |       |
| MAX_VALUE       | bigint(64) unsigned | YES  |      | NULL    |       |
| POSSIBLE_VALUES | varchar(256)        | YES  |      | NULL    |       |
| IS_NOOP         | varchar(64)         | NO   |      | NULL    |       |
+-----------------+---------------------+------+------+---------+-------+
8 rows in set (0.00 sec)
```

```sql
SELECT * FROM variables_info ORDER BY variable_name LIMIT 3;
```

```sql
+-----------------------------------+----------------+---------------+---------------+-----------+-----------+-----------------+---------+
| VARIABLE_NAME                     | VARIABLE_SCOPE | DEFAULT_VALUE | CURRENT_VALUE | MIN_VALUE | MAX_VALUE | POSSIBLE_VALUES | IS_NOOP |
+-----------------------------------+----------------+---------------+---------------+-----------+-----------+-----------------+---------+
| allow_auto_random_explicit_insert | SESSION,GLOBAL | OFF           | OFF           |      NULL |      NULL | NULL            | NO      |
| auto_increment_increment          | SESSION,GLOBAL | 1             | 1             |         1 |     65535 | NULL            | NO      |
| auto_increment_offset             | SESSION,GLOBAL | 1             | 1             |         1 |     65535 | NULL            | NO      |
+-----------------------------------+----------------+---------------+---------------+-----------+-----------+-----------------+---------+
3 rows in set (0.01 sec)
```

Fields in the `VARIABLES_INFO` table are described as follows:

* `VARIABLE_NAME`: the name of the system variable.
* `VARIABLE_SCOPE`: the scope of the system variable. `SESSION` means that the system variable is only valid in the current session. `INSTANCE` means that the system variable is valid in the TiDB instance. `GLOBAL` means that the system variable is valid in the TiDB cluster.
* `DEFAULT_VALUE`: the default value of the system variable.
* `CURRENT_VALUE`: the current value of the system variable. If the scope includes `SESSION`, `CURRENT_VALUE` is the value in the current session.
* `MIN_VALUE`: the minimum value allowed for the system variable. If the system variable is not numeric, `MIN_VALUE` is NULL.
* `MAX_VALUE`: the maximum value allowed for the system variable. If the system variable is not numeric, `MAX_VALUE` is NULL.
* `POSSIBLE_VALUES`: the possible values of the system variable. If the system variable is not an enum type, `POSSIBLE_VALUES` is NULL.
* `IS_NOOP`: whether the system variable is a `noop` system variable.
