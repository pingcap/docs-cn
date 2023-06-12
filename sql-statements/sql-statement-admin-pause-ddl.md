---
title: ADMIN PAUSE DDL
summary: TiDB 数据库中 ADMIN PAUSE DDL 的使用概况。
---

# ADMIN PAUSE DDL

`ADMIN PAUSE DDL` 语句用于暂停当前正在运行的 DDL 作业。可以通过 [`ADMIN SHOW DDL JOBS`](/sql-statements/sql-statement-admin-show-ddl.md) 语句获取 DDL 作业的 `job_id`。

用于暂停已经提交但未执行完成的 DDL 任务。成功暂停后，执行 DDL 任务的 SQL 语句不会立即返回，表现为正在执行。暂停一个已经执行完成的 DDL 任务会在 RESULT 列看到 `DDL Job:90 not found` 的错误，表示该任务已从 DDL 等待队列中被移除。

## 语法图

```ebnf+diagram
AdminStmt ::=
    'ADMIN' ( 'SHOW' ( 'DDL' ( 'JOBS' Int64Num? WhereClauseOptional | 'JOB' 'QUERIES' NumList )? | TableName 'NEXT_ROW_ID' | 'SLOW' AdminShowSlow ) | 'CHECK' ( 'TABLE' TableNameList | 'INDEX' TableName Identifier ( HandleRange ( ',' HandleRange )* )? ) | 'RECOVER' 'INDEX' TableName Identifier | 'CLEANUP' ( 'INDEX' TableName Identifier | 'TABLE' 'LOCK' TableNameList ) | 'CHECKSUM' 'TABLE' TableNameList | 'CANCEL' 'DDL' 'JOBS' NumList | 'PAUSE' 'DDL' 'JOBS' NumList | 'RESUME' 'DDL' 'JOBS' NumList | 'RELOAD' ( 'EXPR_PUSHDOWN_BLACKLIST' | 'OPT_RULE_BLACKLIST' | 'BINDINGS' ) | 'PLUGINS' ( 'ENABLE' | 'DISABLE' ) PluginNameList | 'REPAIR' 'TABLE' TableName CreateTableStmt | ( 'FLUSH' | 'CAPTURE' | 'EVOLVE' ) 'BINDINGS' )

NumList ::=
    Int64Num ( ',' Int64Num )*
```

## 示例

可以通过 `ADMIN PAUSE DDL JOBS` 语句暂停当前正在运行的 DDL 作业，并返回对应作业是否暂停成功，直到被 `ADMIN RESUME DDL JOBS` 恢复：

{{< copyable "sql" >}}

```sql
ADMIN PAUSE DDL JOBS job_id [, job_id] ...;
```

如果暂停失败，会显示失败的具体原因。

> **注意：**
>
> + 该操作可以暂停 DDL 作业，除版本升级外，其他操作和环境变更（例如机器重启、集群重启）不会暂停 DDL 作业。
> + 版本升级操作发生时，会将正在运行的 DDL 作业暂停；并将升级过程中发起的 DDL 作业也暂停。升级结束后，将所有暂停的 DDL 作业恢复运行。
> + 该操作可以同时暂停多个 DDL 作业，可以通过 [`ADMIN SHOW DDL JOBS`](/sql-statements/sql-statement-admin-show-ddl.md) 语句来获取 DDL 作业的 `job_id`。
> + 如果希望暂停的作业已经执行完毕或接近执行完毕，暂停操作将失败。

## MySQL 兼容性

`ADMIN PAUSE DDL JOBS` 语句是 TiDB 对 MySQL 语法的扩展。

## 另请参阅

* [`ADMIN SHOW DDL [JOBS|QUERIES]`](/sql-statements/sql-statement-admin-show-ddl.md)
* [`ADMIN CANCEL DDL`](/sql-statements/sql-statement-admin-cancel-ddl.md)
* [`ADMIN RESUME DDL`](/sql-statements/sql-statement-admin-resume-ddl.md)
