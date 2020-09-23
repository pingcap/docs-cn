---
title: ADMIN CANCEL DDL | TiDB SQL Statement Reference
summary: An overview of the usage of ADMIN CANCEL DDL for the TiDB database.
category: reference
---

# ADMIN CANCEL DDL

The `ADMIN CANCEL DDL` statement allows you to cancel a running DDL job. The `job_id` can be found by running `ADMIN SHOW DDL JOBS`.

## Synopsis

**AdminStmt:**

![AdminStmt](/media/sqlgram/AdminStmt.png)

**NumList:**

![NumList](/media/sqlgram/NumList.png)

## Examples

To cancel the currently running DDL jobs and return whether the corresponding jobs are successfully cancelled, use `ADMIN CANCEL DDL JOBS`:

{{< copyable "sql" >}}

```sql
ADMIN CANCEL DDL JOBS job_id [, job_id] ...;
```

If the operation fails to cancel the jobs, specific reasons are displayed.

> **Note:**
>
> - Only this operation can cancel DDL jobs. All other operations and environment changes (such as machine restart and cluster restart) cannot cancel these jobs.
> - This operation can cancel multiple DDL jobs at the same time. You can get the ID of DDL jobs using the `ADMIN SHOW DDL JOBS` statement.
> - If the jobs you want to cancel are finished, the cancellation operation fails.

## MySQL compatibility

This statement is a TiDB extension to MySQL syntax.

## See also

* [`ADMIN SHOW DDL [JOBS,QUERIES]`](/sql-statements/sql-statement-admin-show-ddl.md)