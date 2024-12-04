---
title: TiDB 日志备份与 PITR 命令行手册
summary: 介绍 TiDB 日志备份与 PITR 的命令行。
---

# TiDB 日志备份与 PITR 命令行手册

本文介绍 TiDB 日志备份和 PITR (Point-in-time recovery) 命令行。

如果你想了解如何进行日志备份与 PITR，可以参考以下教程：

- [TiDB 日志备份与 PITR 使用指南](/br/br-pitr-guide.md)
- [TiDB 集群备份与恢复实践示例](/br/backup-and-restore-use-cases.md)

## 日志备份命令行介绍

你可以执行 `tiup br log` 命令来开启和管理日志备份任务：

```shell
tiup br log --help

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

各个子命令的作用如下：

- `tiup br log start`：启动一个日志备份任务
- `tiup br log status`：查询日志备份任务状态
- `tiup br log pause`：暂停日志备份任务
- `tiup br log resume`：重启暂停的备份任务
- `tiup br log stop`：停止备份任务，并删除任务元信息
- `tiup br log truncate`：从备份存储中清理日志备份数据
- `tiup br log metadata`：查询备份存储中备份数据的元信息

### 启动日志备份

执行 `tiup br log start` 命令，你可以在备份集群启动一个日志备份任务。该任务在 TiDB 集群持续地运行，及时地将 KV 变更日志保存到备份存储中。

执行 `tiup br log start --help` 命令可获取该子命令使用介绍：

```shell
tiup br log start --help
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

- `--start-ts`：指定开始备份日志的起始时间点。如果未指定，备份程序选取当前时间作为 `start-ts`。
- `task-name`：指定日志备份任务名。该名称也用于查询备份状态、暂停、重启和恢复备份任务等操作。
- `ca`、`cert`、`key`：指定使用 mTLS 加密方式与 TiKV 和 PD 进行通讯。
- `--pd`：指定备份集群的 PD 访问地址。br 命令行工具需要访问 PD，发起日志备份任务。
- `--storage`：指定备份存储地址。日志备份支持以 Amazon S3、Google Cloud Storage (GCS)、Azure Blob Storage 为备份存储，以上命令以 S3 为示例。关于 URI 格式的详细信息，请参考[外部存储服务的 URI 格式](/external-storage-uri.md)。

使用示例：

```shell
tiup br log start \
  --task-name=pitr \
  --pd="${PD_IP}:2379" \
  --storage='s3://backup-101/logbackup?access-key=${access-key}&secret-access-key=${secret-access-key}'
```

### 加密日志备份数据

BR 支持在上传到备份存储之前对日志备份数据进行加密。

自 TiDB v8.4.0 起，你可以在日志备份命令中传入以下参数来加密日志备份数据，类似于[快照备份加密](/br/br-snapshot-manual.md#备份数据加密)：

- `--log.crypter.method`：加密算法，支持 `aes128-ctr`、`aes192-ctr` 和 `aes256-ctr` 三种算法，缺省值为 `plaintext`，表示不加密
- `--log.crypter.key`：加密密钥，十六进制字符串格式，`aes128-ctr` 对应 128 位（16 字节）密钥长度，`aes192-ctr` 为 24 字节，`aes256-ctr` 为 32 字节
- `--log.crypter.key-file`：密钥文件，可直接将存放密钥的文件路径作为参数传入，此时 `log.crypter.key` 不需要配置

示例如下：

```shell
tiup br log start \
    --task-name=pitr-with-encryption
    --pd ${PD_IP}:2379 \
    --storage "s3://${BACKUP_COLLECTION_ADDR}/snapshot-${DATE}?access-key=${AWS_ACCESS_KEY}&secret-access-key=${AWS_SECRET_ACCESS_KEY}" \
    --log.crypter.method aes128-ctr \
    --log.crypter.key 0123456789abcdef0123456789abcdef
```

然而，在一些对安全性要求更高的场景中，你可能不希望在命令行中直接传入固定的加密密钥。为了进一步提高安全性，你可以使用基于主密钥的加密系统来管理加密密钥。该系统会使用不同的数据密钥来加密不同的日志备份文件，并且支持主密钥轮换。你可以在日志备份命令中传入以下参数来配置基于主密钥的加密：

- `--master-key-crypter-method`：基于主密钥的加密算法，支持 `aes128-ctr`、`aes192-ctr` 和 `aes256-ctr` 三种算法，缺省值为 `plaintext`，表示不加密
- `--master-key`：主密钥配置，可以是基于本地磁盘的主密钥或基于云 KMS (Key Management Service) 的主密钥

使用本地磁盘主密钥加密：

```shell
tiup br log start \
    --task-name=pitr-with-encryption \
    --pd ${PD_IP}:2379 \
    --storage "s3://${BACKUP_COLLECTION_ADDR}/snapshot-${DATE}?access-key=${AWS_ACCESS_KEY}&secret-access-key=${AWS_SECRET_ACCESS_KEY}" \
    --master-key-crypter-method aes128-ctr \
    --master-key "local:///path/to/master.key"
```

使用 AWS KMS 加密：

```shell
tiup br log start \
    --task-name=pitr-with-encryption \
    --pd ${PD_IP}:2379 \
    --storage "s3://${BACKUP_COLLECTION_ADDR}/snapshot-${DATE}?access-key=${AWS_ACCESS_KEY}&secret-access-key=${AWS_SECRET_ACCESS_KEY}" \
    --master-key-crypter-method aes128-ctr \
    --master-key "aws-kms:///${AWS_KMS_KEY_ID}?AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY}&AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}&REGION=${AWS_REGION}"
```

使用 Google Cloud KMS 加密：

```shell
tiup br log start \
    --task-name=pitr-with-encryption \
    --pd ${PD_IP}:2379 \
    --storage "s3://${BACKUP_COLLECTION_ADDR}/snapshot-${DATE}?access-key=${AWS_ACCESS_KEY}&secret-access-key=${AWS_SECRET_ACCESS_KEY}" \
    --master-key-crypter-method aes128-ctr \
    --master-key "gcp-kms:///projects/$GCP_PROJECT_ID/locations/$GCP_LOCATION/keyRings/$GCP_KEY_RING/cryptoKeys/$GCP_KEY_NAME?AUTH=specified&CREDENTIALS=$GCP_CREDENTIALS_PATH"
```

> **注意：**
>
> - 密钥丢失，备份的数据将无法恢复到集群中。
> - 加密功能需在 br 工具和 TiDB 集群都不低于 v8.4.0 的版本上使用，且加密日志备份得到的数据无法在低于 v8.4.0 版本的集群上恢复。

### 查询日志备份任务

执行 `tiup br log status` 命令，你可以查询日志备份任务状态。

执行 `tiup br log status --help` 命令可获取该子命令使用介绍：

```shell
tiup br log status --help
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

以上示例中，`--task-name` 为常用参数，它用来指定日志备份任务名。默认值为 `*`，即显示全部任务。

使用示例：

```shell
tiup br log status --task-name=pitr --pd="${PD_IP}:2379"
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

- `status`：任务状态，包括 `NORMAL`（正常）、`ERROR`（异常）和 `PAUSE`（暂停）三种状态。
- `start`：日志备份任务开始的时间，该值为备份任务启动时候指定的 `start-ts`。
- `storage`：备份存储。
- `speed`：日志备份任务的总 QPS（每秒备份的日志个数）。
- `checkpoint [global]`：集群中早于该 `checkpoint` 的数据都已经保存到备份存储，它也是备份数据可恢复的最近时间点。
- `error [store]`：存储节点上的日志备份组件运行遇到的异常。

### 暂停和恢复日志备份任务

执行 `tiup br log pause` 命令，你可以暂停正在运行的日志备份任务。

执行 `tiup br log pause --help` 可获取该子命令使用介绍：

```shell
tiup br log pause --help
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
tiup br log pause --task-name=pitr --pd="${PD_IP}:2379"
```

执行 `tiup br log resume` 命令，你可以恢复被暂停的日志备份任务。

执行 `tiup br log resume --help` 命令可获取该子命令使用介绍：

```shell
tiup br log resume --help
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

暂停日志备份任务超过了 24 小时后，执行 `tiup br log resume` 会报错，提示备份数据丢失。处理方法请参考[恢复日志备份任务失败](/faq/backup-and-restore-faq.md#执行-br-log-resume-命令恢复处于暂停状态的任务时报-errbackupgcsafepointexceeded-错误该如何处理)。

使用示例：

```shell
tiup br log resume --task-name=pitr --pd="${PD_IP}:2379"
```

### 停止和重启日志备份任务

通过执行 `tiup br log stop` 命令，你可以停止正在进行的日志备份任务。停止的任务，可以通过 `--storage` 路径重新启动。

#### 停止日志备份任务

执行 `tiup br log stop` 命令，可以停止日志备份任务，该命令会清理备份集群中的任务元信息。

执行 `tiup br log stop --help` 命令可获取该子命令使用介绍：

```shell
tiup br log stop --help
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

> **注意：**
>
> 请谨慎使用该命令，如果你只需**暂时停止**日志备份，请使用 `tiup br log pause` 和 `tiup br log resume` 命令。

使用示例：

```shell
tiup br log stop --task-name=pitr --pd="${PD_IP}:2379"
```

#### 重新启动备份任务

当使用 `tiup br log stop` 命令停止日志备份任务后，可在另一个 `--storage` 路径下重新创建一个新的日志备份任务，也可以在原来的 `--storage` 路径下执行 `tiup br log start` 命令重新启动日志备份任务。如果是在原来的 `--storage` 路径重启任务，需要注意：

- 重启备份任务的 `--storage` 参数需要与停止任务之前的参数相同。
- 此时不需要填入 `--start-ts` 参数，程序将自动从上次的备份进度点开始备份数据。
- 如果停止任务后的时间过长，多版本的数据已经被 GC，则在重启备份任务时会报错 `BR:Backup:ErrBackupGCSafepointExceeded`，此时只能配置另外的日志路径来重新创建日志备份任务。

### 清理日志备份数据

执行 `tiup br log truncate` 命令，你可以从备份存储中删除过期或不再需要的备份日志数据。

执行 `tiup br log truncate --help` 命令可获取该子命令使用介绍：

```shell
tiup br log truncate --help
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
- `--storage`：指定备份存储地址。日志备份支持以 Amazon S3、Google Cloud Storage (GCS)、Azure Blob Storage 为备份存储。关于 URI 格式的详细信息，请参考[外部存储服务的 URI 格式](/external-storage-uri.md)。

使用示例：

```shell
tiup br log truncate --until='2022-07-26 21:20:00+0800' \
--storage='s3://backup-101/logbackup?access-key=${access-key}&secret-access-key=${secret-access-key}'
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

执行 `tiup br log metadata` 命令，你可以查看备份存储中保存的日志备份的元信息，例如最早和最近的可恢复时间点。

执行 `tiup br log metadata --help` 命令可获取该子命令使用介绍：

```shell
tiup br log metadata --help
get the metadata of log backup storage

Usage:
  br log metadata [flags]

Flags:
  -h, --help       help for metadata

Global Flags:
  -s, --storage string         specify the url where backup storage, eg, "s3://bucket/path/prefix"
```

该命令只需要访问备份存储，不需要访问备份集群。

以上示例中，`--storage` 为常用参数，它用来指定备份存储地址。日志备份支持以 Amazon S3、Google Cloud Storage (GCS)、Azure Blob Storage 为备份存储。关于 URI 格式的详细信息，请参考[外部存储服务的 URI 格式](/external-storage-uri.md)。

使用示例：

```shell
tiup br log metadata --storage='s3://backup-101/logbackup?access-key=${access-key}&secret-access-key=${secret-access-key}'
```

该子命令运行后输出以下信息：

```shell
[2022/07/25 23:02:57.236 +08:00] [INFO] [collector.go:69] ["log metadata"] [log-min-ts=434582449885806593] [log-min-date="2022-07-14 20:08:03.268 +0800"] [log-max-ts=434834300106964993] [log-max-date="2022-07-25 23:00:15.618 +0800"]
```

## 恢复到指定时间点 PITR

> **注意：**
>
> 如果 `restore point` 指定 `--full-backup-storage` 为增量备份地址，那么需要保证该备份以及之前的任意增量备份的恢复，均将参数 `--allow-pitr-from-incremental` 设置为 `true`，使增量备份兼容后续的日志备份。

执行 `tiup br restore point` 命令，你可以在新集群上进行 PITR，或者只恢复日志备份数据。

执行 `tiup br restore point --help` 命令可获取该命令使用介绍：

```shell
tiup br restore point --help
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

- `--full-backup-storage`：指定快照（全量）备份的存储地址。如果你要使用 PITR，需要指定该参数，并选择恢复时间点之前最近的快照备份；如果只恢复日志备份数据，则不需要指定该参数。需要注意的是，第一次初始化恢复集群时，必须指定快照备份，快照备份支持以 Amazon S3、Google Cloud Storage (GCS)、Azure Blob Storage 为备份存储。关于 URI 格式的详细信息，请参考[外部存储服务的 URI 格式](/external-storage-uri.md)。
- `--restored-ts`：指定恢复到的时间点。如果没有指定该参数，则恢复到日志备份数据最后的可恢复时间点（备份数据的 checkpoint）。
- `--start-ts`：指定日志备份恢复的起始时间点。如果你只恢复日志备份数据，不恢复快照备份，需要指定这个参数。
- `ca`、`cert`、`key`：指定使用 mTLS 加密方式与 TiKV 和 PD 进行通讯。
- `--pd`：指定恢复集群的 PD 访问地址。
- `--storage`：指定备份存储地址。日志备份支持以 Amazon S3、Google Cloud Storage (GCS)、Azure Blob Storage 为备份存储。关于 URI 格式的详细信息，请参考[外部存储服务的 URI 格式](/external-storage-uri.md)。

使用示例：

```shell
tiup br restore point --pd="${PD_IP}:2379"
--storage='s3://backup-101/logbackup?access-key=${access-key}&secret-access-key=${secret-access-key}'
--full-backup-storage='s3://backup-101/snapshot-202205120000?access-key=${access-key}&secret-access-key=${secret-access-key}'

Full Restore <--------------------------------------------------------------------------------------------------------------------------------------------------------> 100.00%
*** ***["Full Restore success summary"] ****** [total-take=3.112928252s] [restore-data-size(after-compressed)=5.056kB] [Size=5056] [BackupTS=434693927394607136] [total-kv=4] [total-kv-size=290B] [average-speed=93.16B/s]
Restore Meta Files <--------------------------------------------------------------------------------------------------------------------------------------------------> 100.00%
Restore KV Files <----------------------------------------------------------------------------------------------------------------------------------------------------> 100.00%
"restore log success summary"] [total-take=192.955533ms] [restore-from=434693681289625602] [restore-to=434693753549881345] [total-kv-count=33] [total-size=21551]
```

> **注意：**
>
> - 第一次恢复集群时，必须指定全量快照数据，否则可能因为 Table ID 重写规则，导致部分新创建的表数据不正确。详情可见此 GitHub issue [#54418](https://github.com/pingcap/tidb/issues/54418)。
> - 不支持重复恢复某段时间区间的日志，如多次重复恢复 `[t1=10, t2=20)` 区间的日志数据，可能会造成恢复后的数据不正确。
> - 多次恢复不同时间区间的日志时，需保证恢复日志的连续性。如先后恢复 `[t1, t2)`、`[t2, t3)` 和 `[t3, t4)` 三个区间的日志可以保证正确性，而在恢复 `[t1, t2)` 后跳过 `[t2, t3)` 直接恢复 `[t3, t4)` 的区间可能导致恢复之后的数据不正确。

### 恢复加密的日志备份数据

要恢复加密的日志备份数据，你需要在恢复命令中传入相应的解密参数。解密参数需要与加密时使用的参数一致。如果解密算法或密钥不正确，则无法恢复数据。

示例如下：

```shell
tiup br restore point --pd="${PD_IP}:2379"
--storage='s3://backup-101/logbackup?access-key=${ACCESS-KEY}&secret-access-key=${SECRET-ACCESS-KEY}'
--full-backup-storage='s3://backup-101/snapshot-202205120000?access-key=${ACCESS-KEY}&secret-access-key=${SECRET-ACCESS-KEY}'
--crypter.method aes128-ctr
--crypter.key 0123456789abcdef0123456789abcdef
--log.crypter.method aes128-ctr
--log.crypter.key 0123456789abcdef0123456789abcdef
```

如果日志备份是通过主密钥加密的，则可以使用以下命令进行解密恢复：

```shell
tiup br restore point --pd="${PD_IP}:2379"
--storage='s3://backup-101/logbackup?access-key=${ACCESS-KEY}&secret-access-key=${SECRET-ACCESS-KEY}'
--full-backup-storage='s3://backup-101/snapshot-202205120000?access-key=${ACCESS-KEY}&secret-access-key=${SECRET-ACCESS-KEY}'
--crypter.method aes128-ctr
--crypter.key 0123456789abcdef0123456789abcdef
--master-key-crypter-method aes128-ctr
--master-key "local:///path/to/master.key"
```