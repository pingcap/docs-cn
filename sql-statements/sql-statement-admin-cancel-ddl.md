---
title: ADMIN CANCEL DDL | TiDB SQL 语句参考
summary: TiDB 数据库中 ADMIN CANCEL DDL 的使用概览。
category: reference
---

# ADMIN CANCEL DDL

`ADMIN CANCEL DDL` 语句允许您取消正在运行的 DDL 作业。可以通过运行 [`ADMIN SHOW DDL JOBS`](/sql-statements/sql-statement-admin-show-ddl.md) 找到 `job_id`。

`ADMIN CANCEL DDL` 语句还允许您取消已提交但尚未完成执行的 DDL 作业。取消后，执行 DDL 作业的 SQL 语句将返回 `ERROR 8214 (HY000): Cancelled DDL job` 错误。如果您取消一个已经完成的 DDL 作业，您将在 `RESULT` 列中看到 `DDL Job:90 not found` 错误，这表示该作业已从 DDL 等待队列中移除。

## 语法

```ebnf+diagram
AdminCancelDDLStmt ::=
    'ADMIN' 'CANCEL' 'DDL' 'JOBS' NumList 

NumList ::=
    Int64Num ( ',' Int64Num )*
```

## 示例

要取消当前正在运行的 DDL 作业并返回相应作业是否成功取消，使用 `ADMIN CANCEL DDL JOBS`：

```sql
ADMIN CANCEL DDL JOBS job_id [, job_id] ...;
```

如果操作未能取消作业，将显示具体原因。

> **注意：**
>
> - 在 v6.2.0 之前，只有此操作可以取消 DDL 作业，所有其他操作和环境变化（如机器重启和集群重启）都不能取消这些作业。从 v6.2.0 开始，[`KILL`](/sql-statements/sql-statement-kill.md) 语句也可以通过终止正在进行的 DDL 作业来取消它们。
> - 此操作可以同时取消多个 DDL 作业。您可以使用 [`ADMIN SHOW DDL JOBS`](/sql-statements/sql-statement-admin-show-ddl.md) 语句获取 DDL 作业的 ID。
> - 如果您要取消的作业已经完成，取消操作将失败。

## MySQL 兼容性

此语句是 TiDB 对 MySQL 语法的扩展。

## 另请参见

* [`ADMIN SHOW DDL [JOBS|JOB QUERIES]`](/sql-statements/sql-statement-admin-show-ddl.md)
