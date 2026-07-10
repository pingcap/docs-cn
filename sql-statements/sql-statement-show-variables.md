---
title: SHOW [GLOBAL|SESSION] VARIABLES
summary: TiDB 数据库中 SHOW [GLOBAL|SESSION] VARIABLES 的使用概况。
aliases: ['/docs-cn/dev/sql-statements/sql-statement-show-variables/','/docs-cn/dev/reference/sql/statements/show-variables/']
---

# SHOW [GLOBAL|SESSION] VARIABLES

`SHOW [GLOBAL|SESSION] VARIABLES` 语句用于显示 `GLOBAL` 或 `SESSION` 范围的变量列表。如果未指定范围，则应用默认范围 `SESSION`。

## 语法图

```ebnf+diagram
ShowVariablesStmt ::=
    "SHOW" ("GLOBAL" | "SESSION")? VARIABLES ShowLikeOrWhere?

ShowLikeOrWhere ::=
    "LIKE" SimpleExpr
|   "WHERE" Expression
```

## 示例

以下示例展示了如何使用 `SHOW [GLOBAL|SESSION] VARIABLES` 语句显示名称或值与特定模式匹配的变量。关于这些变量的详细说明，参见[系统变量和语法](/system-variables.md)。

{{< copyable "sql" >}}

```sql
SHOW GLOBAL VARIABLES LIKE 'tidb_stmt_summary%';
```

```sql
+-------------------------------------+---------------------+
| Variable_name                       | Value               |
+-------------------------------------+---------------------+
| tidb_stmt_summary_enable_persistent | OFF                 |
| tidb_stmt_summary_file_max_backups  | 0                   |
| tidb_stmt_summary_file_max_days     | 3                   |
| tidb_stmt_summary_file_max_size     | 64                  |
| tidb_stmt_summary_filename          | tidb-statements.log |
| tidb_stmt_summary_history_size      | 24                  |
| tidb_stmt_summary_internal_query    | OFF                 |
| tidb_stmt_summary_max_sql_length    | 4096                |
| tidb_stmt_summary_max_stmt_count    | 3000                |
| tidb_stmt_summary_refresh_interval  | 1800                |
+-------------------------------------+---------------------+
10 rows in set (0.001 sec)
```

{{< copyable "sql" >}}

```sql
SHOW GLOBAL VARIABLES LIKE 'time_zone%';
```

```sql
+---------------+--------+
| Variable_name | Value  |
+---------------+--------+
| time_zone     | SYSTEM |
+---------------+--------+
1 row in set (0.00 sec)
```

```sql
SHOW VARIABLES WHERE Variable_name="tidb_window_concurrency";
```

```sql
+-------------------------+-------+
| Variable_name           | Value |
+-------------------------+-------+
| tidb_window_concurrency | -1    |
+-------------------------+-------+
1 row in set (0.00 sec)
```

```sql
SHOW VARIABLES WHERE Value=300;
```

```sql
+--------------------------------+-------+
| Variable_name                  | Value |
+--------------------------------+-------+
| ddl_slow_threshold             | 300   |
| delayed_insert_timeout         | 300   |
| innodb_purge_batch_size        | 300   |
| key_cache_age_threshold        | 300   |
| slave_checkpoint_period        | 300   |
| tidb_slow_log_threshold        | 300   |
| tidb_wait_split_region_timeout | 300   |
+--------------------------------+-------+
7 rows in set (0.00 sec)
```

## MySQL 兼容性

`SHOW [GLOBAL|SESSION] VARIABLES` 语句与 MySQL 完全兼容。如发现任何兼容性差异，请尝试 [TiDB 支持资源](/support.md)。

## 另请参阅

* [`SET [GLOBAL|SESSION]`](/sql-statements/sql-statement-set-variable.md)
