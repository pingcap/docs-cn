---
title: Filter DML Events Using SQL Expressions
summary: Learn how to filter DML events using SQL expressions.
---

# Filter DML Events Using SQL Expressions

This document introduces how to filter binlog events using SQL expressions when you use DM to perform continuous incremental data replication. For the detailed replication instruction, refer to the following documents:

- [Migrate MySQL of Small Datasets to TiDB](/migrate-small-mysql-to-tidb.md)
- [Migrate MySQL of Large Datasets to TiDB](/migrate-large-mysql-to-tidb.md)
- [Migrate and Merge MySQL Shards of Small Datasets to TiDB](/migrate-small-mysql-shards-to-tidb.md)
- [Migrate and Merge MySQL Shards of Large Datasets to TiDB](/migrate-large-mysql-shards-to-tidb.md)

When performing incremental data replication, you can use the [Binlog Event Filter](/filter-binlog-event.md) to filter certain types of binlog events. For example, you can choose not to replicate `DELETE` events to the downstream for the purposes like archiving and auditing. However, the Binlog Event Filter cannot determine whether to filter the `DELETE` event of a row that requires finer granularity.

To address the issue, since v2.0.5, DM supports using `binlog value filter` in incremental data replication to filter data. Among the DM-supported and `ROW`-formatted binlog, the binlog events carry values of all columns, and you can configure SQL expressions based on these values. If the expression calculates a row change as `TRUE`, DM does not replicate this row change to the downstream.

Similar to [Binlog Event Filter](/filter-binlog-event.md), you need to configure `binlog value filter` in the task configuration file. For details, see the following configuration example. For the advanced task configuration and the description, refer to [DM advanced task configuration file](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced).

```yaml
name: test
task-mode: all

mysql-instances:
  - source-id: "mysql-replica-01"
    expression-filters: ["even_c"]

expression-filter:
  even_c:
    schema: "expr_filter"
    table: "tbl"
    insert-value-expr: "c % 2 = 0"
```

In the above configuration example, the `even_c` rule is configured and referenced by the data source `mysql-replica-01`. According to this rule, for the `tb1` table in the `expr_filter` schema, when an even number is inserted into the `c` column (`c % 2 = 0`), this `insert` statement is not replicated to the downstream. The following example shows the effect of this rule.

Incrementally insert the following data in the upstream data source:

```sql
INSERT INTO tbl(id, c) VALUES (1, 1), (2, 2), (3, 3), (4, 4);
```

Then query the `tb1` table on downstream. You can see that only the rows with odd numbers on `c` are replicated.

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

## Configuration parameters and description

- `schema`: The name of the upstream schema to match. Wildcard matching or regular matching is not supported.
- `table`: The name of the upstream table to match. Wildcard matching or regular matching is not supported.
- `insert-value-expr`: Configures an expression that takes effect on values carried by the `INSERT` type binlog events (WRITE_ROWS_EVENT). You cannot use this expression together with `update-old-value-expr`, `update-new-value-expr` or `delete-value-expr` in the same configuration item.
- `update-old-value-expr`: Configures an expression that takes effect on the old values carried by the `UPDATE` type binlog events (UPDATE_ROWS_EVENT). You cannot use this expression together with `insert-value-expr` or `delete-value-expr` in the same configuration item.
- `update-new-value-expr`: Configures an expression that takes effect on the new values carried by the `UPDATE` type binlog events (UPDATE_ROWS_EVENT). You cannot use this expression together with `insert-value-expr` or `delete-value-expr` in the same configuration item.
- `delete-value-expr`: Configures an expression that takes effect on values carried by the `DELETE` type binlog events (DELETE_ROWS_EVENT). You cannot use this expression together with `insert-value-expr`, `update-old-value-expr` or `update-new-value-expr`.

> **Note:**
>
> - You can configure `update-old-value-expr` and `update-new-value-expr` together.
> - When `update-old-value-expr` and `update-new-value-expr` are configured together, the rows whose "update + old values" meet `update-old-value-expr` **and** whose "update + new values" meet `update-new-value-expr` are filtered.
> - When one of `update-old-value-expr` and `update-new-value-expr` is configured, the configured expression determines whether to filter the **entire row change**, which means that the deletion of old values and the insertion of new values are filtered as a whole.

You can use the SQL expression on one column or on multiple columns. You can also use the SQL functions supported by TiDB, such as `c % 2 = 0`, `a*a + b*b = c*c`, and `ts > NOW()`.

The `TIMESTAMP` default time zone is the time zone specified in the task configuration file. The default value is the time zone of the downstream. You can explicitly specify the time zone in a way like `c_timestamp = '2021-01-01 12:34:56.5678+08:00'`.

You can configure multiple filtering rules under the `expression-filter` configuration item. The upstream data source references the required rule in `expression-filters` to make it effective. When multiple rules are used, if **any** one of the rules are matched, the entire row change is filtered.

> **Note:**
>
> Configuring too many expression filtering rules increases the calculation overhead of DM and slows down the data replication.
