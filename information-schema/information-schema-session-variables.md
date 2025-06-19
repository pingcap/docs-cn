---
title: SESSION_VARIABLES
summary: 了解 `SESSION_VARIABLES` INFORMATION_SCHEMA 表。
---

# SESSION_VARIABLES

`SESSION_VARIABLES` 表提供了会话变量的相关信息。该表的数据类似于 [`SHOW SESSION VARIABLES`](/sql-statements/sql-statement-show-variables.md) 语句的结果。

```sql
USE INFORMATION_SCHEMA;
DESC SESSION_VARIABLES;
```

输出结果如下：

```sql
+----------------+---------------+------+------+---------+-------+
| Field          | Type          | Null | Key  | Default | Extra |
+----------------+---------------+------+------+---------+-------+
| VARIABLE_NAME  | varchar(64)   | YES  |      | NULL    |       |
| VARIABLE_VALUE | varchar(1024) | YES  |      | NULL    |       |
+----------------+---------------+------+------+---------+-------+
2 rows in set (0.00 sec)
```

查询 `SESSION_VARIABLES` 表的前 10 行：

```sql
SELECT * FROM SESSION_VARIABLES ORDER BY variable_name LIMIT 10;
```

输出结果如下：

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

`SESSION_VARIABLES` 表中各列的描述如下：

* `VARIABLE_NAME`：数据库中会话级变量的名称。
* `VARIABLE_VALUE`：数据库中会话级变量的值。
