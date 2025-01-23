---
title: ADMIN CANCEL DDL
summary: TiDB 数据库中 ADMIN CANCEL DDL 的使用概况。
---

# ADMIN CANCEL DDL

`ADMIN CANCEL DDL` 语句用于取消当前正在运行的 DDL 作业。可以通过 [`ADMIN SHOW DDL JOBS`](/sql-statements/sql-statement-admin-show-ddl.md) 语句获取 DDL 作业的 `job_id`。

用于取消已经提交但未执行完成的 DDL 任务。取消完成后，执行 DDL 任务的 SQL 语句会返回 `ERROR 8214 (HY000): Cancelled DDL job` 的错误。取消一个已经执行完成的 DDL 任务会在 RESULT 列看到 `DDL Job:90 not found` 的错误，表示该任务已从 DDL 等待队列中被移除。

## 语法图

```ebnf+diagram
AdminCancelDDLStmt ::=
    'ADMIN' 'CANCEL' 'DDL' 'JOBS' NumList

NumList ::=
    Int64Num ( ',' Int64Num )*
```

## 示例

可以通过 `ADMIN CANCEL DDL JOBS` 语句取消当前正在运行的 DDL 作业，并返回对应作业是否取消成功：

```sql
ADMIN CANCEL DDL JOBS job_id [, job_id] ...;
```

如果取消失败，会显示失败的具体原因。

> **注意：**
>
> + 在 v6.2.0 之前，只有该操作可以取消 DDL 作业，其他所有的操作和环境变更（例如机器重启、集群重启）都不会取消 DDL 作业。从 v6.2.0 开始，使用 [`KILL`](/sql-statements/sql-statement-kill.md) 语句终止作业的方式也可以取消正在执行中的 DDL 作业。
> + 该操作可以同时取消多个 DDL 作业，可以通过 [`ADMIN SHOW DDL JOBS`](/sql-statements/sql-statement-admin-show-ddl.md) 语句来获取 DDL 作业的 `job_id`。
> + 如果希望取消的作业已经执行完毕，取消操作将失败。

## MySQL 兼容性

`ADMIN CANCEL DDL` 语句是 TiDB 对 MySQL 语法的扩展。

## 另请参阅

* [`ADMIN SHOW DDL [JOBS|QUERIES]`](/sql-statements/sql-statement-admin-show-ddl.md)
