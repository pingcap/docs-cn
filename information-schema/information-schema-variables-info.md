---
title: VARIABLES_INFO
summary: 了解 information_schema 表 `VARIABLES_INFO`。
---

# VARIABLES_INFO

`VARIABLES_INFO` 可用于查看当前 TiDB 集群或实例的[系统变量](/system-variables.md)默认值、当前值以及作用域等信息。

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

`VARIABLES_INFO` 表中列的含义如下：

* `VARIABLE_NAME`：系统变量名称。
* `VARIABLE_SCOPE`：系统变量的作用域。`SESSION` 表示当前 session 可见；`INSTANCE` 表示当前 TiDB 实例可见；`GLOBAL` 表示集群内可见；`NONE` 表示全局只读。
* `DEFAULT_VALUE`：系统变量的默认值。
* `CURRENT_VALUE`：系统变量的当前值。如果应用范围中包含 `SESSION`，则显示当前 session 的值。
* `MIN_VALUE`：数值类型的系统变量允许的最小值。如果变量值为非数值类型，则为 NULL。
* `MAX_VALUE`：数值类型的系统变量允许的最大值。如果变量值为非数值类型，则为 NULL。
* `POSSIBLE_VALUES`：系统变量所有可能的值。如果变量值不可枚举，则为 NULL。
* `IS_NOOP`：是否为 `noop` 的系统变量。
