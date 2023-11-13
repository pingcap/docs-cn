---
title: ADMIN RESUME DDL JOBS
summary: An overview of the usage of ADMIN RESUME DDL for the TiDB database.
---

# ADMIN RESUME DDL JOBS

`ADMIN RESUME DDL` allows you to resume a paused DDL job. You can find the `job_id` by running [`ADMIN SHOW DDL JOBS`](/sql-statements/sql-statement-admin-show-ddl.md).

You can use this statement to resume a paused DDL job. After the resume is completed, the SQL statement that executes the DDL job continues to show as being executed. If you try to resume a DDL job that has already been completed, you will see the `DDL Job:90 not found` error in the `RESULT` column, which indicates that the job has been removed from the DDL waiting queue.

## Synopsis

```ebnf+diagram
AdminStmt ::=
    'ADMIN' ( 'SHOW' ( 'DDL' ( 'JOBS' Int64Num? WhereClauseOptional | 'JOB' 'QUERIES' NumList )? | TableName 'NEXT_ROW_ID' | 'SLOW' AdminShowSlow ) | 'CHECK' ( 'TABLE' TableNameList | 'INDEX' TableName Identifier ( HandleRange ( ',' HandleRange )* )? ) | 'RECOVER' 'INDEX' TableName Identifier | 'CLEANUP' ( 'INDEX' TableName Identifier | 'TABLE' 'LOCK' TableNameList ) | 'CHECKSUM' 'TABLE' TableNameList | 'CANCEL' 'DDL' 'JOBS' NumList | 'PAUSE' 'DDL' 'JOBS' NumList | 'RESUME' 'DDL' 'JOBS' NumList | 'RELOAD' ( 'EXPR_PUSHDOWN_BLACKLIST' | 'OPT_RULE_BLACKLIST' | 'BINDINGS' ) | 'PLUGINS' ( 'ENABLE' | 'DISABLE' ) PluginNameList | 'REPAIR' 'TABLE' TableName CreateTableStmt | ( 'FLUSH' | 'CAPTURE' | 'EVOLVE' ) 'BINDINGS' )

NumList ::=
    Int64Num ( ',' Int64Num )*
```

## Examples

`ADMIN RESUME DDL JOBS` resumes the currently paused DDL job and returns whether the job is resumed successfully.

```sql
ADMIN RESUME DDL JOBS job_id [, job_id] ...;
```

If the resume fails, the specific reason for the failure is displayed.

<CustomContent platform="tidb">

> **Note:**
>
> + During the cluster upgrade, the ongoing DDL jobs are paused, and the DDL jobs initiated during the upgrade are also paused. After the upgrade, all paused DDL jobs will resume. The pause and resume operations during the upgrade are taken automatically. For details, see [TiDB Smooth Upgrade](/smooth-upgrade-tidb.md).
> + This statement can resume multiple DDL jobs. You can use the [`ADMIN SHOW DDL JOBS`](/sql-statements/sql-statement-admin-show-ddl.md) statement to obtain the `job_id` of a DDL job.
> + A DDL job in other status (other than `paused`) cannot be resumed and the resume operation will fail.
> + If you try to resume a job more than once, TiDB reports an error `Error Number: 8261`.

</CustomContent>
<CustomContent platform="tidb-cloud">

> **Note:**
>
> + During the cluster upgrade, the ongoing DDL jobs are paused, and the DDL jobs initiated during the upgrade are also paused. After the upgrade, all paused DDL jobs will resume. The pause and resume operations during the upgrade are taken automatically. For details, see [TiDB Smooth Upgrade](https://docs.pingcap.com/tidb/stable/smooth-upgrade-tidb).
> + This statement can resume multiple DDL jobs. You can use the [`ADMIN SHOW DDL JOBS`](/sql-statements/sql-statement-admin-show-ddl.md) statement to obtain the `job_id` of a DDL job.
> + A DDL job in other status (other than `paused`) cannot be resumed and the resume operation will fail.
> + If you try to resume a job more than once, TiDB reports an error `Error Number: 8261`.

</CustomContent>

## MySQL compatibility

This statement is a TiDB extension to MySQL syntax.

## See also

* [`ADMIN SHOW DDL [JOBS|QUERIES]`](/sql-statements/sql-statement-admin-show-ddl.md)
* [`ADMIN CANCEL DDL`](/sql-statements/sql-statement-admin-cancel-ddl.md)
* [`ADMIN PAUSE DDL`](/sql-statements/sql-statement-admin-pause-ddl.md)
