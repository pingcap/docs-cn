---
title: TiDB Log Backup and PITR Command Manual
summary: Learn about the commands of TiDB log backup and point-in-time recovery.
aliases: ['/tidb/dev/br-log-command-line/']
---

# TiDB Log Backup and PITR Command Manual

This document describes the commands used in TiDB log backup and point-in-time recovery (PITR).

For more information about log backup and PITR, refer to:

- [Log Backup and PITR Guide](/br/br-pitr-guide.md)
- [Back up and Restore Use Cases](/br/backup-and-restore-use-cases.md)

## Perform log backup

You can start and manage log backup using the `br log` command.

```shell
./br log --help

backup stream log from TiDB/TiKV cluster

Usage:
  br log [command]

Available Commands:
  metadata   get the metadata of log dir
  pause      pause a log backup task
  resume     resume a log backup task
  start      start a log backup task
  status     get status for the log backup task
  stop       stop a log backup task
  truncate   truncate the log data until sometime
```

Each subcommand is described as follows:

- `br log start`: start a log backup task.
- `br log status`: query the status of the log backup task.
- `br log pause`: pause a log backup task.
- `br log resume`: resume a paused log backup task.
- `br log stop`: stop a log backup task and delete the task metadata.
- `br log truncate`: clean up the log backup data from the backup storage.
- `br log metadata`: query the metadata of the log backup data.

### Start a backup task

You can run the `br log start` command to start a log backup task. This task runs in the background of your TiDB cluster and automatically backs up the change log of KV storage to the backup storage.

Run `br log start --help` to see the help information:

```shell
./br log start --help
start a log backup task

Usage:
  br log start [flags]

Flags:
  -h, --help               help for start
  --start-ts string        usually equals last full backupTS, used for backup log. Default value is current ts. support TSO or datetime, e.g. '400036290571534337' or '2018-05-11 01:42:23+0800'.
  --task-name string       The task name for the backup log task.

Global Flags:
 --ca string                  CA certificate path for TLS connection
 --cert string                Certificate path for TLS connection
 --key string                 Private key path for TLS connection
 -u, --pd strings             PD address (default [127.0.0.1:2379])
 -s, --storage string         specify the url where backup storage, eg, "s3://bucket/path/prefix"

```

The example output only shows the common parameters. These parameters are described as follows:

- `--start-ts`: specifies the start timestamp for the log backup. If this parameter is not specified, the backup program uses the current time as `start-ts`.
- `task-name`: specifies the task name for the log backup. This name is also used to query, pause, and resume the backup task.
- `--ca`, `--cert`, `--key`: specifies the mTLS encryption method to communicate with TiKV and PD.
- `--pd`: specifies the PD address for the backup cluster. BR needs to access PD to start the log backup task.
- `--storage`: specifies the backup storage address. Currently, BR supports Amazon S3, Google Cloud Storage (GCS), or Azure Blob Storage as the storage for log backup. The preceding command uses Amazon S3 as an example. For details, see [URI format of backup storages](/br/backup-and-restore-storages.md#uri-format).

Usage example:

```shell
./br log start --task-name=pitr --pd="${PD_IP}:2379" \
--storage='s3://backup-101/logbackup?access-key=${access-key}&secret-access-key=${secret-access-key}"'
```

### Query the backup status

You can run the `br log status` command to query the backup status.

Run `br log status --help` to see the help information:

```shell
./br log status --help
get status for the log backup task

Usage:
  br log status [flags]

Flags:
  -h, --help           help for status
  --json               Print JSON as the output.
  --task-name string   The task name for backup stream log. If default, get status of all of tasks (default "*")

Global Flags:
 --ca string                  CA certificate path for TLS connection
 --cert string                Certificate path for TLS connection
 --key string                 Private key path for TLS connection
 -u, --pd strings             PD address (default [127.0.0.1:2379])

```

In the example output, `task-name` is used to specify the name of the backup task. The default value is `*`, which means querying the status of all tasks.

Usage example:

```shell
./br log status --task-name=pitr --pd="${PD_IP}:2379"
```

Expected output:

```shell
● Total 1 Tasks.
> #1 <
              name: pitr
            status: ● NORMAL
             start: 2022-07-14 20:08:03.268 +0800
               end: 2090-11-18 22:07:45.624 +0800
           storage: s3://backup-101/logbackup
       speed(est.): 0.82 ops/s
checkpoint[global]: 2022-07-25 22:52:15.518 +0800; gap=2m52s
```

The output fields are described as follows:

- `status`: the status of the backup task, which can be `NORMAL`, `ERROR`, or `PAUSE`.
- `start`: the start time of the backup task. It is the `start-ts` value specified when the backup task is started.
- `storage`: the backup storage address.
- `speed`: the total QPS of the backup task. QPS means the number of logs backed per second.
- `checkpoint [global]`: all data before this checkpoint is backed up to the backup storage. This is the latest timestamp available for restoring the backup data.
- `error [store]`: the error the log backup program encounters on the storage node.

### Pause and resume a backup task

You can run the `br log pause` command to pause a running backup task.

Run `br log pause --help` to see the help information:

```shell
./br log pause --help
pause a log backup task

Usage:
  br log pause [flags]

Flags:
  --gc-ttl int         the TTL (in seconds) that PD holds for BR's GC safepoint (default 86400)
  -h, --help           help for status
  --task-name string   The task name for backup stream log.

Global Flags:
 --ca string                  CA certificate path for TLS connection
 --cert string                Certificate path for TLS connection
 --key string                 Private key path for TLS connection
 -u, --pd strings             PD address (default [127.0.0.1:2379])
```

> **Note:**
>
> - After the log backup task is paused, to prevent the MVCC data that generates the change log from being deleted, the backup program automatically sets the current backup checkpoint as the service safepoint, which retains MVCC data within the latest 24 hours. If the backup task is paused for more than 24 hours, the corresponding data is garbage collected and is not backed up.
> - Retaining too much MVCC data has a negative impact on the storage capacity and performance of the TiDB cluster. Therefore, it is recommended to resume the backup task in time.

Usage example:

```shell
./br log pause --task-name=pitr --pd="${PD_IP}:2379"
```

You can run the `br log resume` command to resume a paused backup task.

Run `br log resume --help` to see the help information:

```shell
./br log resume --help
resume a log backup task

Usage:
  br log resume [flags]

Flags:
  -h, --help           help for status
  --task-name string   The task name for backup stream log.

Global Flags:
 --ca string                  CA certificate path for TLS connection
 --cert string                Certificate path for TLS connection
 --key string                 Private key path for TLS connection
 -u, --pd strings             PD address (default [127.0.0.1:2379])
```

After the backup task is paused for more than 24 hours, running `br log resume` reports an error, and BR prompts that backup data is lost. To handle this error, refer to [Backup & Restore FAQs](/faq/backup-and-restore-faq.md#what-should-i-do-if-the-error-message-errbackupgcsafepointexceeded-is-returned-when-using-the-br-log-resume-command-to-resume-a-suspended-task).

Usage example:

```shell
./br log resume --task-name=pitr --pd="${PD_IP}:2379"
```

### Stop and restart a backup task

You can stop a log backup task by running the `br log stop` command and restart a backup task that is stopped by using the original `--storage` directory.

#### Stop a backup task

You can run the `br log stop` command to stop a log backup task. This command cleans up the task metadata in the backup cluster.

Run `br log stop --help` to see the help information:

```shell
./br log stop --help
stop a log backup task

Usage:
  br log stop [flags]

Flags:
  -h, --help           help for status
  --task-name string   The task name for the backup log task.

Global Flags:
 --ca string                  CA certificate path for TLS connection
 --cert string                Certificate path for TLS connection
 --key string                 Private key path for TLS connection
 -u, --pd strings             PD address (default [127.0.0.1:2379])
```

> **Note:**
>
> Use this command with caution. If you need to pause a log backup task, use `br log pause` and `br log resume` instead.

Usage example:

```shell
./br log stop --task-name=pitr --pd="${PD_IP}:2379"
```

#### Restart a backup task

After running the `br log stop` command to stop a log backup task, you can create a new log backup task in another `--storage` directory or restart the log backup task in the original `--storage` directory by running the `br log start` command. If you restart the task in the original `--storage` directory, pay attention to the following points:

- Parameters of the `--storage` directory for restarting a task must be the same as the task that is stopped.
- The `--start-ts` does not need to be specified. BR automatically starts the backup from the last backup checkpoint.
- If the task is stopped for a long time and multiple versions of the data have been garbage collected, the error `BR:Backup:ErrBackupGCSafepointExceeded` is reported when you attempt to restart the task. In this case, you have to create a new log backup task in another `--storage` directory.

### Clean up backup data

You can run the `br log truncate` command to clean up the outdated or no longer needed log backup data.

Run `br log truncate --help` to see the help information:

```shell
./br log truncate --help
truncate the incremental log until sometime.

Usage:
  br log truncate [flags]

Flags:
  --dry-run        Run the command but don't really delete the files.
  -h, --help       help for truncate
  --until string   Remove all backup data until this TS.(support TSO or datetime, e.g. '400036290571534337' or '2018-05-11 01:42:23+0800'.)
  -y, --yes        Skip all prompts and always execute the command.


Global Flags:
  -s, --storage string         specify the url where backup storage, eg, "s3://bucket/path/prefix"
```

This command only accesses the backup storage and does not access the TiDB cluster. Some parameters are described as follows:

- `--dry-run`: run the command but do not really delete the files.
- `--until`: delete all log backup data before the specified timestamp.
- `--storage`: the backup storage address. Currently, BR supports Amazon S3, GCS, or Azure Blob Storage as the storage for log backup. For details, see [URI format of backup storages](/br/backup-and-restore-storages.md#uri-format).

Usage example:

```shell
./br log truncate --until='2022-07-26 21:20:00+0800' \
–-storage='s3://backup-101/logbackup?access-key=${access-key}&secret-access-key=${secret-access-key}"'
```

Expected output:

```shell
Reading Metadata... DONE; take = 277.911599ms
We are going to remove 9 files, until 2022-07-26 21:20:00.0000.
Sure? (y/N) y
Clearing data files... DONE; take = 43.504161ms, kv-count = 53, kv-size = 4573(4.573kB)
Removing metadata... DONE; take = 24.038962ms
```

### View the backup metadata

You can run the `br log metadata` command to view the backup metadata in the storage system, such as the earliest and latest timestamp that can be restored.

Run `br log metadata --help` to see the help information:

```shell
./br log metadata --help
get the metadata of log backup storage

Usage:
  br log metadata [flags]

Flags:
  -h, --help       help for metadata

Global Flags:
  -s, --storage string         specify the url where backup storage, eg, "s3://bucket/path/prefix"
```

This command only accesses the backup storage and does not access the TiDB cluster.

The `--storage` parameter is used to specify the backup storage address. Currently, BR supports Amazon S3, GCS, or Azure Blob Storage as the storage for log backup. For details, see [URI format of backup storages](/br/backup-and-restore-storages.md#uri-format).

Usage example:

```shell
./br log metadata –-storage='s3://backup-101/logbackup?access-key=${access-key}&secret-access-key=${secret-access-key}"'
```

Expected output:

```shell
[2022/07/25 23:02:57.236 +08:00] [INFO] [collector.go:69] ["log metadata"] [log-min-ts=434582449885806593] [log-min-date="2022-07-14 20:08:03.268 +0800"] [log-max-ts=434834300106964993] [log-max-date="2022-07-25 23:00:15.618 +0800"]
```

## Restore to a specified point in time (PITR)

You can run the `br restore point` command to perform a PITR on a new cluster or just restore the log backup data.

Run `br restore point --help` to see the help information:

```shell
./br restore point --help
restore data from log until specify commit timestamp

Usage:
  br restore point [flags]

Flags:
  --full-backup-storage string specify the backup full storage. fill it if want restore full backup before restore log.
  -h, --help                   help for point
  --restored-ts string         the point of restore, used for log restore. support TSO or datetime, e.g. '400036290571534337' or '2018-05-11 01:42:23+0800'
  --start-ts string            the start timestamp which log restore from. support TSO or datetime, e.g. '400036290571534337' or '2018-05-11 01:42:23+0800'


Global Flags:
 --ca string                  CA certificate path for TLS connection
 --cert string                Certificate path for TLS connection
 --key string                 Private key path for TLS connection
 -u, --pd strings             PD address (default [127.0.0.1:2379])
 -s, --storage string         specify the url where backup storage, eg, "s3://bucket/path/prefix"
```

The example output only shows the common parameters. These parameters are described as follows:

- `--full-backup-storage`: the storage address for the snapshot (full) backup. To use PITR, specify this parameter and choose the latest snapshot backup before the restore timestamp. To restore only log backup data, you can omit this parameter. Currently, BR supports Amazon S3, GCS, or Azure Blob Storage as the storage for log backup. For details, see [URI format of backup storages](/br/backup-and-restore-storages.md#uri-format).
- `--restored-ts`: the timestamp that you want to restore data to. If this parameter is not specified, BR restores data to the latest timestamp available in the log backup, that is, the checkpoint of the backup data.
- `--start-ts`: the start timestamp that you want to restore log backup data from. If you only need to restore log backup data, you must specify this parameter.
- `--pd`: the PD address of the restore cluster.
- `--ca`, `--cert`, `--key`: specify the mTLS encryption method to communicate with TiKV and PD.
- `--storage`: the storage address for the log backup. Currently, BR supports Amazon S3, GCS, or Azure Blob Storage as the storage for log backup. For details, see [URI format of backup storages](/br/backup-and-restore-storages.md#uri-format).

Usage example:

```shell
./br restore point --pd="${PD_IP}:2379"
--storage='s3://backup-101/logbackup?access-key=${access-key}&secret-access-key=${secret-access-key}"'
--full-backup-storage='s3://backup-101/snapshot-202205120000?access-key=${access-key}&secret-access-key=${secret-access-key}"'

Full Restore <--------------------------------------------------------------------------------------------------------------------------------------------------------> 100.00%
*** ***["Full Restore success summary"] ****** [total-take=3.112928252s] [restore-data-size(after-compressed)=5.056kB] [Size=5056] [BackupTS=434693927394607136] [total-kv=4] [total-kv-size=290B] [average-speed=93.16B/s]
Restore Meta Files <--------------------------------------------------------------------------------------------------------------------------------------------------> 100.00%
Restore KV Files <----------------------------------------------------------------------------------------------------------------------------------------------------> 100.00%
"restore log success summary"] [total-take=192.955533ms] [restore-from=434693681289625602] [restore-to=434693753549881345] [total-kv-count=33] [total-size=21551]
```

> **Note:**
>
> - You cannot restore the log backup data of a certain time period repeatedly. If you restore the log backup data of a range `[t1=10, t2=20)` repeatedly, the restored data might be inconsistent.
> - When you restore log data of different time periods in multiple batches, ensure that the log data is restored in consecutive order. If you restore the log backup data of `[t1, t2)`, `[t2, t3)`, and `[t3, t4)` in consecutive order, the restored data is consistent. However, if you restore `[t1, t2)` and then skip `[t2, t3)` to restore `[t3, t4)`, the restored data might be inconsistent.
