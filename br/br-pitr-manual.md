---
title: TiDB 日志备份与 PITR 命令行手册
summary: 介绍日志备份和 PITR 命令行
aliases: ['/zh/tidb/dev/br-log-command-line/']
---

# TiDB 日志备份与 PITR 命令行手册

本文介绍 TiDB 日志备份和 PITR 命令行。

如果你想了解如何进行备份和恢复，可以参考以下教程

- [日志备份和 PITR 功能使用指南](/br/br-pitr-guide.md)
- [TiDB 集群备份和恢复实践示例](/br/br-usage.md)

## 日志备份命令行介绍

使用 `br log` 命令来打开和管理备份日志。

```shell
./br log --help

backup stream log from TiDB/TiKV cluster

Usage:
  br log [command]

Available Commands:
  metadata   get the metadata of log dir
  pause      pause a log backup task.
  resume     resume a log backup task
  start      start a log backup task
  status     get status for the log backup task
  stop       stop a log backup task
  truncate   truncate the log data until sometime
```

各个子命令的作用如下：

- `br log start`：启动一个日志备份任务
- `br log status`：查询日志备份任务状态
- `br log pause`：暂停日志备份任务
- `br log resume`：重启暂停的备份任务
- `br log stop`：停止备份任务，并删除任务元信息
- `br log truncate`：从备份存储中清理日志备份数据
- `br log metadata`：查询备份存储中备份数据的元信息

### 启动日志备份

执行 `br log start` 命令，你可以在备份集群启动一个日志备份任务。该任务在 TiDB 集群持续地运行，及时地将 KV 变更日志保存到备份存储中。

运行 `br log start --help` 可获取该子命令使用介绍：

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

以上命令行示例只展示了常用的参数，这些参数作用如下：

- `task-name`：指定日志备份任务名。该名称也用于查询备份状态、暂停、重启和恢复备份任务等操作。
- `--start-ts`：指定开始备份日志的起始时间点。如果未指定，备份程序选取当前时间作为 start-ts。
- `--pd`：指定备份集群的 PD 访问地址。BR 需要访问 PD 发起日志备份任务。
- `ca`,`cert`,`key`：指定使用 mTLS 加密方式与 TiKV 和 PD 进行通讯。
- `--storage`：指定备份存储地址。日志备份支持以 S3/GCS/Azure Blob Storage 为备份存储，以上命令以 S3 为示例。详细参考[备份存储 URL 配置](/br/backup-and-restore-storages.md#url-格式)。

使用示例：

```shell
./br log start --task-name=pitr --pd=172.16.102.95:2379 --storage='s3://backup-101/logbackup?access_key=${access key}&secret_access_key=${secret access key}"'
```

### 查询日志备份任务

执行 `br log status` 命令，你可以查询日志备份任务状态。

运行 `br log status –-help` 可获取该子命令使用介绍：

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

以上示例中， `task-name` 为常用参数，它用来指定日志备份任务名。默认值为 `*`，即显示全部任务。

使用示例：

```shell
./br log status --task-name=pitr --pd=172.16.102.95:2379
```

命令输出如下：

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

命令输出中的字段含义如下：

- `status`：任务状态，包括 NORMAL（正常）、ERROR（异常）和 PAUSE（暂停）三种状态。
- `start`：日志备份任务开始的时间，该值为备份任务启动时候指定的 start-ts。
- `storage`：备份存储。
- `speed`：日志备份任务的总 QPS（每秒备份的日志个数）。
- `checkpoint [global]`：集群中早于该 checkpoint 的数据都已经保存到备份存储，它也是备份数据可恢复的最近时间点。
- `error [store]`：存储节点上的日志备份组件运行遇到的异常。

### 暂停和重启日志备份任务

执行 `br log pause` 命令，你可以暂停正在运行中的日志备份任务。

运行 `br log pause –help` 可获取该子命令使用介绍：

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

> **注意：**
>
> - 暂停日志备份任务后，备份程序为了防止生成变更日志的 MVCC 数据被删除，暂停任务程序会自动将当前备份点 checkpoint 设置为 service safepoint，允许最多保留最近 24 小时内的 MVCC 数据。如果暂停的日志备份任务超过 24 小时未恢复，对应的数据就会被 GC，不会备份。
> - 保留过多的 MVCC 数据会影响 TiDB 集群的存储容量和性能，任务暂停后请及时恢复任务。

使用示例：

```shell
./br log pause --task-name=pitr --pd=172.16.102.95:2379
```

执行 `br log resume` 命令，你可以恢复被暂停的日志备份任务。

运行 `br log resume --help` 可获取该子命令使用介绍：

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

暂停日志备份任务超过了 24 小时后，执行 `br log resume` 会报错，提示备份数据丢失。处理方法请参考[恢复日志备份任务失败](/faq/br-faq.md#执行-br-log-resume-命令恢复处于暂停状态的任务时报-errbackupgcsafepointexceeded-错误该如何处理)。

使用示例：

```shell
./br log resume --task-name=pitr --pd=172.16.102.95:2379
```

### （永久）停止日志备份任务

执行 `br log stop` 命令，你可以永久地停止日志备份任务，该命令会清理备份集群中的任务元信息。

运行 `br log stop --help` 可获取该子命令使用介绍：

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

> **警告：**
>
> - 请谨慎使用该命令。只有在你确认不再继续使用 PiTR 的情况下，才可以停止日志备份任务。如果你只需暂停日志备份，请使用 `br log pause` 和 `br log resume` 命令。
> - 如果你选择使用 `br log stop` 停止备份任务，在使用 `br log start` 重启备份任务时，需要指定一个与之前不同的日志备份存储路径，而不同的日志备份路径会导致你无法使用 `br restore point` 进行一键恢复。

使用示例：

```shell
./br log stop --task-name=pitr --pd=172.16.102.95:2379
```

### 清理日志备份数据

执行 `br log truncate` 命令，你可以从备份存储中删除过期或不再需要的备份日志数据。

运行 `br log truncate --help` 可获取该子命令使用介绍：

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

该命令只需要访问备份存储，不需要访问备份集群。此外，常用的参数如下：

- `--dry-run`：运行命令，但是不删除文件。
- `--until`：早于该参数指定时间点的日志备份数据会被删除。建议使用快照备份的时间点作为该参数值。
- `--storage`：指定备份存储地址。日志备份支持以 S3/GCS/Azure Blob Storage 为备份存储。详细参考[备份存储 URL 配置](/br/backup-and-restore-storages.md#url-格式)。

使用示例：

```shell
./br log truncate --until='2022-07-26 21:20:00+0800' –-storage='s3://backup-101/logbackup?access_key=${access key}&secret_access_key=${secret access key}"'
```

该子命令运行后输出以下信息：

```shell
Reading Metadata... DONE; take = 277.911599ms
We are going to remove 9 files, until 2022-07-26 21:20:00.0000.
Sure? (y/N) y
Clearing data files... DONE; take = 43.504161ms, kv-count = 53, kv-size = 4573(4.573kB)
Removing metadata... DONE; take = 24.038962ms
```

### 查看备份数据元信息

执行 `br log metadata` 命令，你可以查看备份存储中保存的日志备份的元信息，例如最早和最近的可恢复时间点。

运行 `br log metadata –-help` 可获取该子命令使用介绍：

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

该命令只需要访问备份存储，不需要访问备份集群。

以上示例中，`--storage` 为常用参数，它用来指定备份存储地址。日志备份支持以 S3/GCS/Azure Blob Storage 为备份存储。详细参考[备份存储 URL 配置](/br/backup-and-restore-storages.md#url-格式)。

使用示例：

```shell
./br log metadata –-storage='s3://backup-101/logbackup?access_key=${access key}&secret_access_key=${secret access key}"'
```

该子命令运行后输出以下信息：

```shell
[2022/07/25 23:02:57.236 +08:00] [INFO] [collector.go:69] ["log metadata"] [log-min-ts=434582449885806593] [log-min-date="2022-07-14 20:08:03.268 +0800"] [log-max-ts=434834300106964993] [log-max-date="2022-07-25 23:00:15.618 +0800"]
```

## 恢复到指定时间点 PITR

执行 `br restore point` 命令，你可以在新集群上进行 PiTR ，或者只恢复日志备份数据。

运行 `br restore point --help` 可获取该命令使用介绍：

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

以上示例只展示了常用的参数，这些参数作用如下：

- `--full-backup-storage`：指定快照（全量）备份的存储地址。如果你要使用 PITR，需要指定该参数，并选择恢复时间点之前最近的快照备份；如果只恢复日志备份数据，则不需要指定该参数。快照备份支持以 S3/GCS/Azure Blob Storage 为备份存储。详细参考[备份存储 URL 配置](/br/backup-and-restore-storages.md#url-格式)。
- `--restored-ts`：指定恢复到的时间点。如果没有指定该参数，则恢复到日志备份数据最后的可恢复时间点（备份数据的 checkpoint）。
- `--start-ts`：指定日志备份恢复的起始时间点。如果你只恢复日志备份数据，不恢复快照备份，需要指定这个参数。
- `--pd`：指定恢复集群的 PD 访问地址。
- `ca`,`cert`,`key`：指定使用 mTLS 加密方式与 TiKV 和 PD 进行通讯。
- `--storage`：指定备份存储地址。日志备份支持以 S3/GCS/Azure Blob Storage 为备份存储。详细参考[备份存储 URL 配置](/br/backup-and-restore-storages.md#url-格式)。

使用示例：

```shell
./br restore point --pd=172.16.102.95:2379
--storage='s3://backup-101/logbackup?access_key=${access key}&secret_access_key=${secret access key}"'
--full-backup-storage='s3://backup-101/snapshot-202205120000?access_key=${access key}&secret_access_key=${secret access key}"'

Full Restore <--------------------------------------------------------------------------------------------------------------------------------------------------------> 100.00%
*** ***["Full Restore success summary"] ****** [total-take=3.112928252s] [restore-data-size(after-compressed)=5.056kB] [Size=5056] [BackupTS=434693927394607136] [total-kv=4] [total-kv-size=290B] [average-speed=93.16B/s]
Restore Meta Files <--------------------------------------------------------------------------------------------------------------------------------------------------> 100.00%
Restore KV Files <----------------------------------------------------------------------------------------------------------------------------------------------------> 100.00%
"restore log success summary"] [total-take=192.955533ms] [restore-from=434693681289625602] [restore-to=434693753549881345] [total-kv-count=33] [total-size=21551]
```

> **注意：**
>
> - 不支持重复恢复某段时间区间的日志，如多次重复恢复 [t1=10, t2=20) 区间的日志数据，可能会造成恢复后的数据不正确。
> - 多次恢复不同时间区间的日志时，需保证恢复日志的连续性。如先后恢复 [t1, t2)、[t2, t3) 和 [t3, t4) 三个区间的日志可以保证正确性，而在恢复 [t1, t2) 后跳过 [t2, t3) 直接恢复 [t3, t4) 的区间可能导致恢复之后的数据不正确。
