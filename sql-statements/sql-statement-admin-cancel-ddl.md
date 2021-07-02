---
title: ADMIN CANCEL DDL
summary: TiDB 数据库中 ADMIN CANCEL DDL 的使用概况。
---

# ADMIN CANCEL DDL

`ADMIN CANCEL DDL` 语句用于取消当前正在运行的 DDL 作业。可以通过 `ADMIN SHOW DDL JOBS` 语句获取 DDL 作业的 `job_id`。

## 语法图

```ebnf+diagram
AdminStmt ::=
    'ADMIN' ( 'SHOW' ( 'DDL' ( 'JOBS' Int64Num? WhereClauseOptional | 'JOB' 'QUERIES' NumList )? | TableName 'NEXT_ROW_ID' | 'SLOW' AdminShowSlow ) | 'CHECK' ( 'TABLE' TableNameList | 'INDEX' TableName Identifier ( HandleRange ( ',' HandleRange )* )? ) | 'RECOVER' 'INDEX' TableName Identifier | 'CLEANUP' ( 'INDEX' TableName Identifier | 'TABLE' 'LOCK' TableNameList ) | 'CHECKSUM' 'TABLE' TableNameList | 'CANCEL' 'DDL' 'JOBS' NumList | 'RELOAD' ( 'EXPR_PUSHDOWN_BLACKLIST' | 'OPT_RULE_BLACKLIST' | 'BINDINGS' ) | 'PLUGINS' ( 'ENABLE' | 'DISABLE' ) PluginNameList | 'REPAIR' 'TABLE' TableName CreateTableStmt | ( 'FLUSH' | 'CAPTURE' | 'EVOLVE' ) 'BINDINGS' )

NumList ::=
    Int64Num ( ',' Int64Num )*
```

## 示例

可以通过 `ADMIN CANCEL DDL JOBS` 语句取消当前正在运行的 DDL 作业，并返回对应作业是否取消成功：

{{< copyable "sql" >}}

```sql
ADMIN CANCEL DDL JOBS job_id [, job_id] ...;
```

如果取消失败，会显示失败的具体原因。

> **注意：**
>
> + 只有该操作可以取消 DDL 作业，其他所有的操作和环境变更（例如机器重启、集群重启）都不会取消 DDL 作业。
> + 该操作可以同时取消多个 DDL 作业，可以通过 `ADMIN SHOW DDL JOBS` 语句来获取 DDL 作业的 `job_id`。
> + 如果希望取消的作业已经执行完毕，取消操作将失败。

## MySQL 兼容性

`ADMIN CANCEL DDL` 语句是 TiDB 对 MySQL 语法的扩展。

## 另请参阅

* [`ADMIN SHOW DDL [JOBS|QUERIES]`](/sql-statements/sql-statement-admin-show-ddl.md)
