---
title: Filter Certain Row Changes Using SQL Expressions
---

# Filter Certain Row Changes Using SQL Expressions

## Overview

In the process of data migration, DM provides the [Binlog Event Filter](/dm/dm-key-features.md#binlog-event-filter) feature to filter certain types of binlog events. For example, for archiving or auditing purposes, `DELETE` event might be filtered when data is migrated to the downstream. However, Binlog Event Filter cannot judge with a greater granularity whether the `DELETE` event of a certain row should be filtered.

To solve the above issue, DM supports filtering certain row changes using SQL expressions. The binlog in the `ROW` format supported by DM has the values of all columns in binlog events. You can configure SQL expressions according to these values. If the SQL expressions evaluate a row change as `TRUE`, DM will not migrate the row change downstream.

> **Note:**
>
> This feature only takes effect in the phase of incremental replication, not in the phase of full migration.

## Configuration example

Similar to [Binlog Event Filter](/dm/dm-key-features.md#binlog-event-filter), you also need to configure the expression-filter feature in the configuration file of the data migration task, as shown below. For complete configuration and its descriptions, refer to [DM Advanced Task Configuration File](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced)：

```yml
name: test
task-mode: all

target-database:
  host: "127.0.0.1"
  port: 4000
  user: "root"
  password: ""

mysql-instances:
  - source-id: "mysql-replica-01"
    expression-filters: ["even_c"]

expression-filter:
  even_c:
    schema: "expr_filter"
    table: "tbl"
    insert-value-expr: "c % 2 = 0"
```

The above example configures `even_c` rule, and allows the data source whose ID is `mysql-replica-01` to refer this rule. The meaning of `even_c` is:

For the `tbl` table in the `expr_filter` shema, when the value of the inserted `c` is even (`c % 2 = 0`), the inserted statement will not be migrated downstream.

The usage result of this rule is shown below.

Insert the following data in the upstream data source:

```sql
INSERT INTO tbl(id, c) VALUES (1, 1), (2, 2), (3, 3), (4, 4);
```

Then query the `tbl` table downstream and you can find that only rows with an odd value of `c` are migrated downstream:

```sql
MySQL [test]> select * from tbl;
+------+------+
| id   | c    |
+------+------+
|    1 |    1 |
|    3 |    3 |
+------+------+
2 rows in set (0.001 sec)
```

## Configuration parameters and rule descriptions

- `schema`: The name of the upstream database to be matched. Wildcard match or regular match is not supported.
- `table`: The name of the upstream table to be matched. Wildcard match or regular match is not supported.
- `insert-value-expr`: Specifies an expression which takes effect on the value of binlog event (WRITE_ROWS_EVENT) of INSERT type. Do not use it with `update-old-value-expr`, `update-new-value-expr`, or `delete-value-expr` in the same configuration item.
- `update-old-value-expr`：Specifies an expression which takes effect on the old value of binlog event (UPDATE_ROWS_EVENT) of UPDATE type. Do not use it with `insert-value-expr` or `delete-value-expr` in the same configuration item.
- `update-new-value-expr`: Specifies an expression which takes effect on the new value of binlog event (UPDATE_ROWS_EVENT) of UPDATE type. Do not use it with `insert-value-expr` or `delete-value-expr` in the same configuration item.
- `delete-value-expr`：Specifies an expression which takes effect on the value of binlog event (DELETE_ROWS_EVENT) of DELETE type. Do not use it with`insert-value-expr`, `update-old-value-expr`, or `update-new-value-expr` in the same configuration item.

> **Note:**
>
> You can configure `update-old-value-expr` and `update-new-value-expr` at the same time.
>
> - When you configure `update-old-value-expr` and `update-new-value-expr` at the same time, the row changes where updated old value meets the rule of `update-old-value-expr` **and** the updated new value meets the rule of `update-new-value-expr` will be filtered out.
> - When you only configure one parameter, the statement you configure will decide whether to filter **the whole row changes**, which means the delete event of an old value and the insert event of a new value will be filtered out as a whole.

SQL expressions can involve one or more columns. You can also use the SQL functions TiDB supports, such as `c % 2 = 0`, `a*a + b*b = c*c`, and `ts > NOW()`.

The timezone of TIMESTAMP is UTC by default. You can use `c_timestamp = '2021-01-01 12:34:56.5678+08:00'` to specify the timezone explicitly.

You can define multiple filter rules under the configuration item `expression-filter`. By refering the rules you need in the configuration item of `expression-filters` in the upstream data source, the rules can take effect. When multiple rules take effect, matching **any** of the rules causes a row change to be filtered.

> **Note:**
>
> Setting too many expression filters for a table increases the computing overhead of DM， which might impede data migration.