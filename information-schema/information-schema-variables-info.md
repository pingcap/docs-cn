---
title: VARIABLES_INFO
summary: 了解 `VARIABLES_INFO` information_schema 表。
---

# VARIABLES_INFO

`VARIABLES_INFO` 表提供了当前 TiDB 实例或 TiDB 集群中[系统变量](/system-variables.md)的默认值、当前值和作用范围等信息。

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

`VARIABLES_INFO` 表中各字段的描述如下：

* `VARIABLE_NAME`：系统变量的名称。
* `VARIABLE_SCOPE`：系统变量的作用范围。`SESSION` 表示系统变量仅在当前会话中有效。`INSTANCE` 表示系统变量在 TiDB 实例中有效。`GLOBAL` 表示系统变量在 TiDB 集群中有效。`NONE` 表示系统变量在 TiDB 集群中为只读。
* `DEFAULT_VALUE`：系统变量的默认值。
* `CURRENT_VALUE`：系统变量的当前值。如果作用范围包含 `SESSION`，则 `CURRENT_VALUE` 为当前会话中的值。
* `MIN_VALUE`：系统变量允许的最小值。如果系统变量不是数值类型，则 `MIN_VALUE` 为 NULL。
* `MAX_VALUE`：系统变量允许的最大值。如果系统变量不是数值类型，则 `MAX_VALUE` 为 NULL。
* `POSSIBLE_VALUES`：系统变量的可能值。如果系统变量不是枚举类型，则 `POSSIBLE_VALUES` 为 NULL。
* `IS_NOOP`：系统变量是否为 `noop`（无操作）系统变量。
