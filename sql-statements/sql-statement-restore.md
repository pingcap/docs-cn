---
title: RESTORE | TiDB SQL Statement Reference
summary: An overview of the usage of RESTORE for the TiDB database.
aliases: ['/docs/dev/sql-statements/sql-statement-restore/']
---

# RESTORE

This statement performs a distributed restore from a backup archive previously produced by a [`BACKUP` statement](/sql-statements/sql-statement-backup.md).

The `RESTORE` statement uses the same engine as the [BR tool](/br/backup-and-restore-overview.md), except that the restore process is driven by TiDB itself rather than a separate BR tool. All benefits and caveats of BR also apply here. In particular, **`RESTORE` is currently not ACID-compliant**. Before running `RESTORE`, ensure that the following requirements are met:

* The cluster is "offline", and the current TiDB session is the only active SQL connection to access all tables being restored.
* When a full restore is being performed, the tables being restored should not already exist, because existing data might be overridden and causes inconsistency between the data and indices.
* When an incremental restore is being performed, the tables should be at the exact same state as the `LAST_BACKUP` timestamp when the backup is created.

Running `RESTORE` requires either the `RESTORE_ADMIN` or `SUPER` privilege. Additionally, both the TiDB node executing the restore and all TiKV nodes in the cluster must have read permission from the destination.

The `RESTORE` statement is blocking, and will finish only after the entire restore task is finished, failed, or canceled. A long-lasting connection should be prepared for running `RESTORE`. The task can be canceled using the [`KILL TIDB QUERY`](/sql-statements/sql-statement-kill.md) statement.

Only one `BACKUP` and `RESTORE` task can be executed at a time. If a `BACKUP` or `RESTORE` task is already running on the same TiDB server, the new `RESTORE` execution will wait until all previous tasks are done.

`RESTORE` can only be used with "tikv" storage engine. Using `RESTORE` with the "unistore" engine will fail.

## Synopsis

```ebnf+diagram
RestoreStmt ::=
    "RESTORE" BRIETables "FROM" stringLit RestoreOption*

BRIETables ::=
    "DATABASE" ( '*' | DBName (',' DBName)* )
|   "TABLE" TableNameList

RestoreOption ::=
    "RATE_LIMIT" '='? LengthNum "MB" '/' "SECOND"
|   "CONCURRENCY" '='? LengthNum
|   "CHECKSUM" '='? Boolean
|   "SEND_CREDENTIALS_TO_TIKV" '='? Boolean

Boolean ::=
    NUM | "TRUE" | "FALSE"
```

## Examples

### Restore from backup archive

{{< copyable "sql" >}}

```sql
RESTORE DATABASE * FROM 'local:///mnt/backup/2020/04/';
```

```sql
+------------------------------+-----------+----------+---------------------+---------------------+
| Destination                  | Size      | BackupTS | Queue Time          | Execution Time      |
+------------------------------+-----------+----------+---------------------+---------------------+
| local:///mnt/backup/2020/04/ | 248665063 | 0        | 2020-04-21 17:16:55 | 2020-04-21 17:16:55 |
+------------------------------+-----------+----------+---------------------+---------------------+
1 row in set (28.961 sec)
```

In the example above, all data is restored from a backup archive at the local filesystem. The data is read as SST files from the `/mnt/backup/2020/04/` directories distributed among all TiDB and TiKV nodes.

The first row of the result above is described as follows:

| Column | Description |
| :-------- | :--------- |
| `Destination` | The destination URL to read from |
| `Size` |  The total size of the backup archive, in bytes |
| `BackupTS` | (not used) |
| `Queue Time` | The timestamp (in current time zone) when the `RESTORE` task was queued. |
| `Execution Time` | The timestamp (in current time zone) when the `RESTORE` task starts to run. |

### Partial restore

You can specify which databases or tables to restore. If some databases or tables are missing from the backup archive, they will be ignored, and thus `RESTORE` would complete without doing anything.

{{< copyable "sql" >}}

```sql
RESTORE DATABASE `test` FROM 'local:///mnt/backup/2020/04/';
```

{{< copyable "sql" >}}

```sql
RESTORE TABLE `test`.`sbtest01`, `test`.`sbtest02` FROM 'local:///mnt/backup/2020/04/';
```

### External storages

BR supports restoring data from S3 or GCS:

{{< copyable "sql" >}}

```sql
RESTORE DATABASE * FROM 's3://example-bucket-2020/backup-05/';
```

The URL syntax is further explained in [external storage URI](/br/backup-and-restore-storages.md#uri-format).

When running on cloud environment where credentials should not be distributed, set the `SEND_CREDENTIALS_TO_TIKV` option to `FALSE`:

{{< copyable "sql" >}}

```sql
RESTORE DATABASE * FROM 's3://example-bucket-2020/backup-05/'
    SEND_CREDENTIALS_TO_TIKV = FALSE;
```

### Performance fine-tuning

Use `RATE_LIMIT` to limit the average download speed per TiKV node to reduce network bandwidth.

By default, TiDB node would run 128 restore threads. This value can be adjusted with the `CONCURRENCY` option.

Before restore is completed, `RESTORE` would perform a checksum against the data from the archive to verify correctness. This step can be disabled with the `CHECKSUM` option if you are confident that this is unnecessary.

{{< copyable "sql" >}}

```sql
RESTORE DATABASE * FROM 's3://example-bucket-2020/backup-06/'
    RATE_LIMIT = 120 MB/SECOND
    CONCURRENCY = 64
    CHECKSUM = FALSE;
```

### Incremental restore

There is no special syntax to perform incremental restore. TiDB will recognize whether the backup archive is full or incremental and take appropriate action. You only need to apply each incremental restore in correct order.

For instance, if a backup task is created as follows:

{{< copyable "sql" >}}

```sql
BACKUP DATABASE `test` TO 's3://example-bucket/full-backup'  SNAPSHOT = 413612900352000;
BACKUP DATABASE `test` TO 's3://example-bucket/inc-backup-1' SNAPSHOT = 414971854848000 LAST_BACKUP = 413612900352000;
BACKUP DATABASE `test` TO 's3://example-bucket/inc-backup-2' SNAPSHOT = 416353458585600 LAST_BACKUP = 414971854848000;
```

then the same order should be applied in the restore:

{{< copyable "sql" >}}

```sql
RESTORE DATABASE * FROM 's3://example-bucket/full-backup';
RESTORE DATABASE * FROM 's3://example-bucket/inc-backup-1';
RESTORE DATABASE * FROM 's3://example-bucket/inc-backup-2';
```

## MySQL compatibility

This statement is a TiDB extension to MySQL syntax.

## See also

* [BACKUP](/sql-statements/sql-statement-backup.md)
* [SHOW RESTORES](/sql-statements/sql-statement-show-backups.md)
