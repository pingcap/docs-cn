---
title: SESSION_VARIABLES
summary: 了解 information_schema 表 `SESSION_VARIABLES`。
---

# SESSION_VARIABLES

`SESSION_VARIABLES` 表提供了关于 session 变量的信息。表中的数据跟 `SHOW SESSION VARIABLES` 语句执行结果类似。

{{< copyable "sql" >}}

```sql
USE information_schema;
DESC session_variables;
```

```sql
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

```sql
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

`SESSION_VARIABLES` 表各列字段含义如下：

* `VARIABLE_NAME`：数据库中 session 级变量的名称。
* `VARIABLE_VALUE`：数据库中对应该 session 变量名的具体值。
