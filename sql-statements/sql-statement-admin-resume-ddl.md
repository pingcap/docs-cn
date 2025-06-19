---
title: ADMIN RESUME DDL JOBS
summary: TiDB 数据库中 ADMIN RESUME DDL 的使用概览。
---

# ADMIN RESUME DDL JOBS

`ADMIN RESUME DDL` 允许你恢复已暂停的 DDL 任务。你可以通过运行 [`ADMIN SHOW DDL JOBS`](/sql-statements/sql-statement-admin-show-ddl.md) 找到 `job_id`。

你可以使用此语句恢复已暂停的 DDL 任务。恢复完成后，执行 DDL 任务的 SQL 语句继续显示为正在执行。如果你尝试恢复已完成的 DDL 任务，你将在 `RESULT` 列中看到 `DDL Job:90 not found` 错误，这表示该任务已从 DDL 等待队列中移除。

## 语法

```ebnf+diagram
AdminResumeDDLStmt ::=
    'ADMIN' 'RESUME' 'DDL' 'JOBS' NumList 

NumList ::=
    Int64Num ( ',' Int64Num )*
```

## 示例

`ADMIN RESUME DDL JOBS` 恢复当前暂停的 DDL 任务，并返回任务是否恢复成功。

```sql
ADMIN RESUME DDL JOBS job_id [, job_id] ...;
```

如果恢复失败，将显示具体的失败原因。

<CustomContent platform="tidb">

> **注意：**
>
> + 在集群升级期间，正在进行的 DDL 任务会被暂停，升级期间发起的 DDL 任务也会被暂停。升级完成后，所有暂停的 DDL 任务将恢复。升级期间的暂停和恢复操作是自动进行的。详情请参阅 [TiDB 平滑升级](/smooth-upgrade-tidb.md)。
> + 此语句可以恢复多个 DDL 任务。你可以使用 [`ADMIN SHOW DDL JOBS`](/sql-statements/sql-statement-admin-show-ddl.md) 语句获取 DDL 任务的 `job_id`。
> + 处于其他状态（非 `paused`）的 DDL 任务无法恢复，恢复操作将失败。
> + 如果你多次尝试恢复同一个任务，TiDB 会报错 `Error Number: 8261`。

</CustomContent>
<CustomContent platform="tidb-cloud">

> **注意：**
>
> + 在集群升级期间，正在进行的 DDL 任务会被暂停，升级期间发起的 DDL 任务也会被暂停。升级完成后，所有暂停的 DDL 任务将恢复。升级期间的暂停和恢复操作是自动进行的。详情请参阅 [TiDB 平滑升级](https://docs.pingcap.com/tidb/stable/smooth-upgrade-tidb)。
> + 此语句可以恢复多个 DDL 任务。你可以使用 [`ADMIN SHOW DDL JOBS`](/sql-statements/sql-statement-admin-show-ddl.md) 语句获取 DDL 任务的 `job_id`。
> + 处于其他状态（非 `paused`）的 DDL 任务无法恢复，恢复操作将失败。
> + 如果你多次尝试恢复同一个任务，TiDB 会报错 `Error Number: 8261`。

</CustomContent>

## MySQL 兼容性

该语句是 TiDB 对 MySQL 语法的扩展。

## 另请参阅

* [`ADMIN SHOW DDL [JOBS|QUERIES]`](/sql-statements/sql-statement-admin-show-ddl.md)
* [`ADMIN CANCEL DDL`](/sql-statements/sql-statement-admin-cancel-ddl.md)
* [`ADMIN PAUSE DDL`](/sql-statements/sql-statement-admin-pause-ddl.md)
