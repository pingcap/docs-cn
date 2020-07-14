---
title: SHOW [BACKUPS|RESTORES] | TiDB SQL Statement Reference
summary: An overview of the usage of SHOW [BACKUPS|RESTORES] for the TiDB database.
aliases: ['/docs/dev/sql-statements/sql-statement-show-backups/']
---

# SHOW [BACKUPS|RESTORES]

This statement shows a list of all queued and running [`BACKUP`](/sql-statements/sql-statement-backup.md) and [`RESTORE`](/sql-statements/sql-statement-restore.md) tasks.

Use `SHOW BACKUPS` to query `BACKUP` tasks and use `SHOW RESTORES` to query `RESTORE` tasks. Both statements require `SUPER` privilege to run.

## Synopsis

**ShowBRIEStmt:**

![ShowBRIEStmt](/media/sqlgram/ShowBRIEStmt.png)

**ShowLikeOrWhereOpt:**

![ShowLikeOrWhereOpt](/media/sqlgram/ShowLikeOrWhereOpt.png)

## Examples

In one connection, execute the following statement:

{{< copyable "sql" >}}

```sql
BACKUP DATABASE `test` TO 's3://example-bucket/backup-01/?region=us-west-1';
```

Before the backup completes, run `SHOW BACKUPS` in a new connection:

{{< copyable "sql" >}}

```sql
SHOW BACKUPS;
```

```sql
+--------------------------------+---------+----------+---------------------+---------------------+-------------+------------+
| Destination                    | State   | Progress | Queue_Time          | Execution_Time      | Finish_Time | Connection |
+--------------------------------+---------+----------+---------------------+---------------------+-------------+------------+
| s3://example-bucket/backup-01/ | Backup  | 98.38    | 2020-04-12 23:09:03 | 2020-04-12 23:09:25 |        NULL |          4 |
+--------------------------------+---------+----------+---------------------+---------------------+-------------+------------+
1 row in set (0.00 sec)
```

The first row of the result above is described as follows:

| Column | Description |
| :-------- | :--------- |
| `Destination` | The destination URL (with all parameters stripped to avoid leaking secret keys) |
| `State` | State of the task |
| `Progress` | Estimated progress in the current state as a percentage |
| `Queue_Time` | When the task was queued |
| `Execution_Time` | When the task was started; the value is `0000-00-00 00:00:00` for queueing tasks |
| `Finish_Time` | (not used for now) |
| `Connection` | Connection ID running this task |

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
