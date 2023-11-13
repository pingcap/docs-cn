---
title: ADMIN PAUSE DDL JOBS
summary: An overview of the usage of ADMIN PAUSE DDL JOBS for the TiDB database.
---

# ADMIN PAUSE DDL JOBS

`ADMIN PAUSE DDL` allows you to pause a running DDL job. The `job_id` can be found by running [`ADMIN SHOW DDL JOBS`](/sql-statements/sql-statement-admin-show-ddl.md).

You can use this statement to pause a DDL job that is issued but not yet completed executing. After the pause, the SQL statement that executes the DDL job does not return immediately, but looks like it is still running. If you try to pause a DDL job that has already been completed, you will see the `DDL Job:90 not found` error in the `RESULT` column, which indicates that the job has been removed from the DDL waiting queue.

## Synopsis

```ebnf+diagram
AdminStmt ::=
    'ADMIN' ( 'SHOW' ( 'DDL' ( 'JOBS' Int64Num? WhereClauseOptional | 'JOB' 'QUERIES' NumList )? | TableName 'NEXT_ROW_ID' | 'SLOW' AdminShowSlow ) | 'CHECK' ( 'TABLE' TableNameList | 'INDEX' TableName Identifier ( HandleRange ( ',' HandleRange )* )? ) | 'RECOVER' 'INDEX' TableName Identifier | 'CLEANUP' ( 'INDEX' TableName Identifier | 'TABLE' 'LOCK' TableNameList ) | 'CHECKSUM' 'TABLE' TableNameList | 'CANCEL' 'DDL' 'JOBS' NumList | 'PAUSE' 'DDL' 'JOBS' NumList | 'RESUME' 'DDL' 'JOBS' NumList | 'RELOAD' ( 'EXPR_PUSHDOWN_BLACKLIST' | 'OPT_RULE_BLACKLIST' | 'BINDINGS' ) | 'PLUGINS' ( 'ENABLE' | 'DISABLE' ) PluginNameList | 'REPAIR' 'TABLE' TableName CreateTableStmt | ( 'FLUSH' | 'CAPTURE' | 'EVOLVE' ) 'BINDINGS' )

NumList ::=
    Int64Num ( ',' Int64Num )*
```

## Examples

`ADMIN PAUSE DDL JOBS` pauses the currently running DDL job and returns whether the job is paused successfully. The job can be resumed by `ADMIN RESUME DDL JOBS`.

```sql
ADMIN PAUSE DDL JOBS job_id [, job_id] ...;
```

If the pause fails, the specific reason for the failure is displayed.

<CustomContent platform="tidb">

> **Note:**
>
> + This statement can pause a DDL job, but other operations and environment changes (such as machine restarts and cluster restarts) do not pause DDL jobs except for cluster upgrades.
> + During the cluster upgrade, the ongoing DDL jobs are paused, and the DDL jobs initiated during the upgrade are also paused. After the upgrade, all paused DDL jobs will resume. The pause and resume operations during the upgrade are taken automatically. For details, see [TiDB Smooth Upgrade](/smooth-upgrade-tidb.md).
> + This statement can pause multiple DDL jobs. You can use the [`ADMIN SHOW DDL JOBS`](/sql-statements/sql-statement-admin-show-ddl.md) statement to obtain the `job_id` of a DDL job.

</CustomContent>
<CustomContent platform="tidb-cloud">

> **Note:**
>
> + This statement can pause a DDL job, but other operations and environment changes (such as machine restarts and cluster restarts) do not pause DDL jobs except for cluster upgrades.
> + During the cluster upgrade, the ongoing DDL jobs are paused, and the DDL jobs initiated during the upgrade are also paused. After the upgrade, all paused DDL jobs will resume. The pause and resume operations during the upgrade are taken automatically. For details, see [TiDB Smooth Upgrade](https://docs.pingcap.com/tidb/stable/smooth-upgrade-tidb).
> + This statement can pause multiple DDL jobs. You can use the [`ADMIN SHOW DDL JOBS`](/sql-statements/sql-statement-admin-show-ddl.md) statement to obtain the `job_id` of a DDL job.

</CustomContent>

## MySQL compatibility

This statement is a TiDB extension to MySQL syntax.

## See also

* [`ADMIN SHOW DDL [JOBS|QUERIES]`](/sql-statements/sql-statement-admin-show-ddl.md)
* [`ADMIN CANCEL DDL`](/sql-statements/sql-statement-admin-cancel-ddl.md)
* [`ADMIN RESUME DDL`](/sql-statements/sql-statement-admin-resume-ddl.md)
