---
title: BACKUP | TiDB SQL Statement Reference
summary: An overview of the usage of BACKUP for the TiDB database.
aliases: ['/docs/dev/sql-statements/sql-statement-backup/']
---

# BACKUP

This statement is used to perform a distributed backup of the TiDB cluster.

The `BACKUP` statement uses the same engine as the [BR tool](/br/backup-and-restore-overview.md) does, except that the backup process is driven by TiDB itself rather than a separate BR tool. All benefits and warnings of BR also apply in this statement.

Executing `BACKUP` requires either the `BACKUP_ADMIN` or `SUPER` privilege. Additionally, both the TiDB node executing the backup and all TiKV nodes in the cluster must have read or write permission to the destination. Local storage (storage paths starting with `local://`) is not permitted when [Security Enhanced Mode](/system-variables.md#tidb_enable_enhanced_security) is enabled.

The `BACKUP` statement is blocked until the entire backup task is finished, failed, or canceled. A long-lasting connection should be prepared for executing `BACKUP`. The task can be canceled using the [`KILL TIDB QUERY`](/sql-statements/sql-statement-kill.md) statement.

Only one `BACKUP` and [`RESTORE`](/sql-statements/sql-statement-restore.md) task can be executed at a time. If a `BACKUP` or `RESTORE` statement is already being executed on the same TiDB server, the new `BACKUP` execution will wait until all previous tasks are finished.

`BACKUP` can only be used with "tikv" storage engine. Using `BACKUP` with the "unistore" engine will fail.

## Synopsis

```ebnf+diagram
BackupStmt ::=
    "BACKUP" BRIETables "TO" stringLit BackupOption*

BRIETables ::=
    "DATABASE" ( '*' | DBName (',' DBName)* )
|   "TABLE" TableNameList

BackupOption ::=
    "RATE_LIMIT" '='? LengthNum "MB" '/' "SECOND"
|   "CONCURRENCY" '='? LengthNum
|   "CHECKSUM" '='? Boolean
|   "SEND_CREDENTIALS_TO_TIKV" '='? Boolean
|   "LAST_BACKUP" '='? BackupTSO
|   "SNAPSHOT" '='? ( BackupTSO | LengthNum TimestampUnit "AGO" )

Boolean ::=
    NUM | "TRUE" | "FALSE"

BackupTSO ::=
    LengthNum | stringLit
```

## Examples

### Back up databases

{{< copyable "sql" >}}

```sql
BACKUP DATABASE `test` TO 'local:///mnt/backup/2020/04/';
```

```sql
+------------------------------+-----------+-----------------+---------------------+---------------------+
| Destination                  | Size      | BackupTS        | Queue Time          | Execution Time      |
+------------------------------+-----------+-----------------+---------------------+---------------------+
| local:///mnt/backup/2020/04/ | 248665063 | 416099531454472 | 2020-04-12 23:09:48 | 2020-04-12 23:09:48 |
+------------------------------+-----------+-----------------+---------------------+---------------------+
1 row in set (58.453 sec)
```

In the example above, the `test` database is backed up into the local filesystem. The data is saved as SST files in the `/mnt/backup/2020/04/` directories distributed among all TiDB and TiKV nodes.

The first row of the result above is described as follows:

| Column | Description |
| :-------- | :--------- |
| `Destination` | The destination URL |
| `Size` |  The total size of the backup archive, in bytes |
| `BackupTS` | The TSO of the snapshot when the backup is created (useful for [incremental backup](#incremental-backup)) |
| `Queue Time` | The timestamp (in current time zone) when the `BACKUP` task is queued. |
| `Execution Time` | The timestamp (in current time zone) when the `BACKUP` task starts to run. |

### Back up tables

{{< copyable "sql" >}}

```sql
BACKUP TABLE `test`.`sbtest01` TO 'local:///mnt/backup/sbtest01/';
```

{{< copyable "sql" >}}

```sql
BACKUP TABLE sbtest02, sbtest03, sbtest04 TO 'local:///mnt/backup/sbtest/';
```

### Back up the entire cluster

{{< copyable "sql" >}}

```sql
BACKUP DATABASE * TO 'local:///mnt/backup/full/';
```

Note that the system tables (`mysql.*`, `INFORMATION_SCHEMA.*`, `PERFORMANCE_SCHEMA.*`, …) will not be included into the backup.

### External storages

BR supports backing up data to S3 or GCS:

{{< copyable "sql" >}}

```sql
BACKUP DATABASE `test` TO 's3://example-bucket-2020/backup-05/?access-key={YOUR_ACCESS_KEY}&secret-access-key={YOUR_SECRET_KEY}';
```

The URL syntax is further explained in [external storage URL](/br/backup-and-restore-storages.md#url-format).

When running on cloud environment where credentials should not be distributed, set the `SEND_CREDENTIALS_TO_TIKV` option to `FALSE`:

{{< copyable "sql" >}}

```sql
BACKUP DATABASE `test` TO 's3://example-bucket-2020/backup-05/'
    SEND_CREDENTIALS_TO_TIKV = FALSE;
```

### Performance fine-tuning

Use `RATE_LIMIT` to limit the average upload speed per TiKV node to reduce network bandwidth.

By default, every TiKV node would run 4 backup threads. This value can be adjusted with the `CONCURRENCY` option.

Before backup is completed, `BACKUP` would perform a checksum against the data on the cluster to verify correctness. This step can be disabled with the `CHECKSUM` option if you are confident that this is unnecessary.

{{< copyable "sql" >}}

```sql
BACKUP DATABASE `test` TO 's3://example-bucket-2020/backup-06/'
    RATE_LIMIT = 120 MB/SECOND
    CONCURRENCY = 8
    CHECKSUM = FALSE;
```

### Snapshot

Specify a timestamp, TSO or relative time to backup historical data.

{{< copyable "sql" >}}

```sql
-- relative time
BACKUP DATABASE `test` TO 'local:///mnt/backup/hist01'
    SNAPSHOT = 36 HOUR AGO;

-- timestamp (in current time zone)
BACKUP DATABASE `test` TO 'local:///mnt/backup/hist02'
    SNAPSHOT = '2020-04-01 12:00:00';

-- timestamp oracle
BACKUP DATABASE `test` TO 'local:///mnt/backup/hist03'
    SNAPSHOT = 415685305958400;
```

The supported units for relative time are:

* MICROSECOND
* SECOND
* MINUTE
* HOUR
* DAY
* WEEK

Note that, following SQL standard, the units are always singular.

### Incremental backup

Supply the `LAST_BACKUP` option to only backup the changes between the last backup to the current snapshot.

{{< copyable "sql" >}}

```sql
-- timestamp (in current time zone)
BACKUP DATABASE `test` TO 'local:///mnt/backup/hist02'
    LAST_BACKUP = '2020-04-01 12:00:00';

-- timestamp oracle
BACKUP DATABASE `test` TO 'local:///mnt/backup/hist03'
    LAST_BACKUP = 415685305958400;
```

## MySQL compatibility

This statement is a TiDB extension to MySQL syntax.

## See also

* [RESTORE](/sql-statements/sql-statement-restore.md)
* [SHOW BACKUPS](/sql-statements/sql-statement-show-backups.md)
