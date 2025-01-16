---
title: ADMIN PAUSE DDL JOBS
summary: TiDB 数据库中 ADMIN PAUSE DDL JOBS 的使用概况。
---

# ADMIN PAUSE DDL JOBS

`ADMIN PAUSE DDL` 语句用于暂停当前正在运行的 DDL 作业。可以通过 [`ADMIN SHOW DDL JOBS`](/sql-statements/sql-statement-admin-show-ddl.md) 语句获取 DDL 作业的 `job_id`。

该语句可用于暂停已经发起但未执行完成的 DDL 任务。成功暂停后，执行 DDL 任务的 SQL 语句不会立即返回，表现为正在执行。如果尝试暂停一个已经完成的 DDL 任务，会在 `RESULT` 列看到 `DDL Job:90 not found` 的错误，表示该任务已从 DDL 等待队列中被移除。

> **注意：**
>
> + 该操作可以暂停 DDL 作业，但除版本升级外，其他操作和环境变更（例如机器重启、集群重启）不会暂停 DDL 作业。
> + 版本升级时，正在运行的 DDL 作业将被暂停，同时在升级过程中发起的 DDL 作业也将被暂停。升级结束后，所有已暂停的 DDL 作业将恢复执行。升级过程中的操作为自动进行，详情查阅 [TiDB 平滑升级](/smooth-upgrade-tidb.md)。
> + 该操作可以同时暂停多个 DDL 作业，可以通过 [`ADMIN SHOW DDL JOBS`](/sql-statements/sql-statement-admin-show-ddl.md) 语句来获取 DDL 作业的 `job_id`。

## 语法图

```ebnf+diagram
AdminPauseDDLStmt ::=
    'ADMIN' 'PAUSE' 'DDL' 'JOBS' NumList

NumList ::=
    Int64Num ( ',' Int64Num )*
```

## 示例

可以通过 `ADMIN PAUSE DDL JOBS` 语句暂停当前正在运行的 DDL 作业，并返回对应作业是否暂停成功，直到被 `ADMIN RESUME DDL JOBS` 恢复：

```sql
ADMIN PAUSE DDL JOBS job_id [, job_id] ...;
```

如果暂停失败，会显示失败的具体原因。

## MySQL 兼容性

`ADMIN PAUSE DDL JOBS` 语句是 TiDB 对 MySQL 语法的扩展。

## 另请参阅

* [`ADMIN SHOW DDL [JOBS|QUERIES]`](/sql-statements/sql-statement-admin-show-ddl.md)
* [`ADMIN CANCEL DDL`](/sql-statements/sql-statement-admin-cancel-ddl.md)
* [`ADMIN RESUME DDL`](/sql-statements/sql-statement-admin-resume-ddl.md)
