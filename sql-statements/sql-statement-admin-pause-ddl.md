---
title: ADMIN PAUSE DDL JOBS
summary: TiDB 数据库中 ADMIN PAUSE DDL JOBS 的使用概述。
---

# ADMIN PAUSE DDL JOBS

`ADMIN PAUSE DDL` 允许你暂停正在运行的 DDL 作业。可以通过运行 [`ADMIN SHOW DDL JOBS`](/sql-statements/sql-statement-admin-show-ddl.md) 找到 `job_id`。

你可以使用此语句暂停已发出但尚未完成执行的 DDL 作业。暂停后，执行 DDL 作业的 SQL 语句不会立即返回，而是看起来仍在运行。如果你尝试暂停已完成的 DDL 作业，你会在 `RESULT` 列中看到 `DDL Job:90 not found` 错误，这表示该作业已从 DDL 等待队列中移除。

## 语法图

```ebnf+diagram
AdminPauseDDLStmt ::=
    'ADMIN' 'PAUSE' 'DDL' 'JOBS' NumList 

NumList ::=
    Int64Num ( ',' Int64Num )*
```

## 示例

`ADMIN PAUSE DDL JOBS` 暂停当前正在运行的 DDL 作业，并返回作业是否成功暂停。可以通过 `ADMIN RESUME DDL JOBS` 恢复作业。

```sql
ADMIN PAUSE DDL JOBS job_id [, job_id] ...;
```

如果暂停失败，会显示具体的失败原因。

<CustomContent platform="tidb">

> **注意：**
>
> + 此语句可以暂停 DDL 作业，但除了集群升级外，其他操作和环境变化（如机器重启和集群重启）不会暂停 DDL 作业。
> + 在集群升级期间，正在进行的 DDL 作业会被暂停，升级期间发起的 DDL 作业也会被暂停。升级完成后，所有暂停的 DDL 作业将恢复。升级期间的暂停和恢复操作是自动进行的。详情请参见 [TiDB 平滑升级](/smooth-upgrade-tidb.md)。
> + 此语句可以暂停多个 DDL 作业。你可以使用 [`ADMIN SHOW DDL JOBS`](/sql-statements/sql-statement-admin-show-ddl.md) 语句获取 DDL 作业的 `job_id`。

</CustomContent>
<CustomContent platform="tidb-cloud">

> **注意：**
>
> + 此语句可以暂停 DDL 作业，但除了集群升级外，其他操作和环境变化（如机器重启和集群重启）不会暂停 DDL 作业。
> + 在集群升级期间，正在进行的 DDL 作业会被暂停，升级期间发起的 DDL 作业也会被暂停。升级完成后，所有暂停的 DDL 作业将恢复。升级期间的暂停和恢复操作是自动进行的。详情请参见 [TiDB 平滑升级](https://docs.pingcap.com/tidb/stable/smooth-upgrade-tidb)。
> + 此语句可以暂停多个 DDL 作业。你可以使用 [`ADMIN SHOW DDL JOBS`](/sql-statements/sql-statement-admin-show-ddl.md) 语句获取 DDL 作业的 `job_id`。

</CustomContent>

## MySQL 兼容性

此语句是 TiDB 对 MySQL 语法的扩展。

## 另请参见

* [`ADMIN SHOW DDL [JOBS|QUERIES]`](/sql-statements/sql-statement-admin-show-ddl.md)
* [`ADMIN CANCEL DDL`](/sql-statements/sql-statement-admin-cancel-ddl.md)
* [`ADMIN RESUME DDL`](/sql-statements/sql-statement-admin-resume-ddl.md)
