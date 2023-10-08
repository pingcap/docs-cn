---
title: SHOW [BACKUPS|RESTORES] | TiDB SQL Statement Reference
summary: An overview of the usage of SHOW [BACKUPS|RESTORES] for the TiDB database.
aliases: ['/docs/dev/sql-statements/sql-statement-show-backups/']
---

# SHOW [BACKUPS|RESTORES]

These statements show a list of all queued, running and recently finished [`BACKUP`](/sql-statements/sql-statement-backup.md) and [`RESTORE`](/sql-statements/sql-statement-restore.md) tasks that were executed on a TiDB instance.

Both statements require `SUPER` privilege to run.

Use `SHOW BACKUPS` to query `BACKUP` tasks and use `SHOW RESTORES` to query `RESTORE` tasks.

> **Note:**
>
> This feature is not available on [TiDB Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless) clusters.

Backups and restores that were started with the `br` commandline tool are not shown.

## Synopsis

```ebnf+diagram
ShowBRIEStmt ::=
    "SHOW" ("BACKUPS" | "RESTORES") ShowLikeOrWhere?

ShowLikeOrWhere ::=
    "LIKE" SimpleExpr
|   "WHERE" Expression
```

## Examples

In one connection, execute the following statement:

{{< copyable "sql" >}}

```sql
BACKUP DATABASE `test` TO 's3://example-bucket/backup-01';
```

Before the backup completes, run `SHOW BACKUPS` in a new connection:

{{< copyable "sql" >}}

```sql
SHOW BACKUPS;
```

```sql
+--------------------------------+---------+----------+---------------------+---------------------+-------------+------------+---------+
| Destination                    | State   | Progress | Queue_time          | Execution_time      | Finish_time | Connection | Message |
+--------------------------------+---------+----------+---------------------+---------------------+-------------+------------+---------+
| s3://example-bucket/backup-01/ | Backup  | 98.38    | 2020-04-12 23:09:03 | 2020-04-12 23:09:25 |        NULL |          4 | NULL    |
+--------------------------------+---------+----------+---------------------+---------------------+-------------+------------+---------+
1 row in set (0.00 sec)
```

The first row of the result above is described as follows:

| Column | Description |
| :-------- | :--------- |
| `Destination` | The destination URL (with all parameters stripped to avoid leaking secret keys) |
| `State` | State of the task |
| `Progress` | Estimated progress in the current state as a percentage |
| `Queue_time` | When the task was queued |
| `Execution_time` | When the task was started; the value is `0000-00-00 00:00:00` for queueing tasks |
| `Finish_time` | The timestamp when the task finished; the value is `0000-00-00 00:00:00` for queueing and running tasks |
| `Connection` | Connection ID running this task |
| `Message` | Message with details |

The possible states are:

| State | Description |
| :-----|:------------|
| Backup | Making a backup |
| Wait | Waiting for execution |
| Checksum | Running a checksum operation |

The connection ID can be used to cancel a backup/restore task via the [`KILL TIDB QUERY`](/sql-statements/sql-statement-kill.md) statement.

{{< copyable "sql" >}}

```sql
KILL TIDB QUERY 4;
```

```sql
Query OK, 0 rows affected (0.00 sec)
```

### Filtering

Use the `LIKE` clause to filter out tasks by matching the destination URL against a wildcard expression.

{{< copyable "sql" >}}

```sql
SHOW BACKUPS LIKE 's3://%';
```

Use the `WHERE` clause to filter by columns.

{{< copyable "sql" >}}

```sql
SHOW BACKUPS WHERE `Progress` < 25.0;
```

## MySQL compatibility

This statement is a TiDB extension to MySQL syntax.

## See also

* [BACKUP](/sql-statements/sql-statement-backup.md)
* [RESTORE](/sql-statements/sql-statement-restore.md)
