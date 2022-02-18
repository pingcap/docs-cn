---
title: 备份 TiDB 集群的数据
summary: 了解如何使用 BR 命令行进行数据备份。
---

# 备份 TiDB 集群数据

下面介绍各种 TiDB 集群备份功能的使用方式，

## 备份 TiDB 集群快照

TiDB 集群快照数据是只包含某个物理时间点上集群的最新的、满足事务一致性的数据。 使用 `br backup full` 可以备份 TiDB 最新的或者指定时间点的快照数据。该命令的使用帮助可以通过 `br backup full --help` 来获取。

用例：将集群属于 '2022-01-30 07:42:23' 的快照数据备份到 s3 的名为 `backup-data` bucket 下的 `2022-01-30/` 前缀目录中。

{{< copyable "shell-regular" >}}

```shell
br backup full \
    --pd "${PDIP}:2379" \
    --backupts '2022-01-30 07:42:23' \
    --storage "s3://backup-data/2022-01-30/" \
    --ratelimit 128 \
    --log-file backupfull.log
```

以上命令中：

- `--ratelimit` 选项限制了**每个 TiKV** 执行备份任务的速度上限（单位 MiB/s）。`--log-file` 选项指定把 BR 的 log 写到 `backupfull.log` 文件中；
- `--backupts` 选项指定了快照对应的物理时间点。如果该快照的数据被 GC 了，那么 `br backup` 命令会报错退出；如果用户没有指定该参数，那么 BR 会选取备份开始的时间点所对应的快照。

备份期间有进度条在终端中显示。当进度条前进到 100% 时，说明备份已完成。进度条效果如下：

```shell
br backup full \
    --pd "${PDIP}:2379" \
    --storage "s3://backup-data/2022-01-30/" \
    --ratelimit 128 \
    --log-file backupfull.log
Full Backup <---------/................................................> 17.12%.
```

在完成备份后，BR 为了确保数据安全性，会将备份数据的 checksum 同集群 [admin checksum table](/sql-statements/sql-statement-admin-checksum-table.md) 的结果比较，来保证正确性。

## 备份 TiDB 集群增量数据

TiDB 集群增量数据包含某个时间段的起始和结束两个快照的差异变化的数据。 增量数据相对比快照数据而言数据量更小，适合配合快照备份一起使用，来减少备份的数据量。

如果想要备份增量数据，只需要使用 `br backup` 进行备份的时候指定**上一次的备份时间戳** `--lastbackupts` 即可。你可以使用 `validate` 指令获取上一次备份的时间戳，示例如下：

{{< copyable "shell-regular" >}}

```shell
LAST_BACKUP_TS=`br validate decode --field="end-version" -s s3://backup-data/2022-01-30/ | tail -n1`
```

注意增量备份有以下限制：

- 增量备份数据需要与前一次快照备份数据保存在不同的路径下；
- GC safepoint 必须在 `lastbackupts` 之前。TiDB 默认的 GC Lifetime 为 10 min，即默认 TiDB 只支持备份 10 min 内的增量数据。如果你希望备份更长时间的增量数据，则需要[调整 TiDB 集群的 GC Lifetime 设置](/system-variables.md#tidb_gc_life_time-从-v50-版本开始引入)。

{{< copyable "shell-regular" >}}

```shell
br backup full\
    --pd ${PDIP}:2379 \
    --ratelimit 128 \
    --storage "s3://backup-data/2022-01-30/incr" \ 
    --lastbackupts ${LAST_BACKUP_TS}
```

以上命令会备份 `(LAST_BACKUP_TS, current PD timestamp]` 之间的增量数据，以及这段时间内的 DDL。在恢复的时候，BR 会先把所有 DDL 恢复，而后才会恢复数据。

## 备份 TiDB 集群的指定库表的数据

BR 支持只备份集群快照和增量数据中指定库/表的局部数据。该功能在快照备份和增量数据备份的基础上，过滤掉不需要的数据，帮助用户备份实现只备份关键业务的数据。

### 备份单个数据库的数据

要备份集群中指定单个数据库的数据，可使用 `br backup db` 命令。同样可通过 `br backup db --help` 来获取子命令 `db` 的使用帮助。

用例：将数据库 `test` 备份到 s3 的名为 `backup-data` 的 bucket 下面的 `db-test/2022-01-30/` 前缀目录下。

{{< copyable "shell-regular" >}}

```shell
br backup db \
    --pd "${PDIP}:2379" \
    --db test \
    --storage "s3://backup-data/db-test/2022-01-30/" \
    --ratelimit 128 \
    --log-file backuptable.log
```

`db` 子命令的选项为 `--db`，用来指定数据库名。其他选项的含义与[备份 TiDB 集群快照](#备份-tidb-集群快照)相同。

### 备份单张表的数据

要备份集群中指定单张表的数据，可使用 `br backup table` 命令。同样可通过 `br backup table --help` 来获取子命令 `table` 的使用帮助。

用例：将表 `test.usertable` 备份到 s3 的名为 `backup-data` 的 bucket 下面的 `table-db-usertable/2022-01-30/` 前缀目录下。

{{< copyable "shell-regular" >}}

```shell
br backup table \
    --pd "${PDIP}:2379" \
    --db test \
    --table usertable \
    --storage "s3://backup-data/table-db-usertable/2022-01-30/" \
    --ratelimit 128 \
    --log-file backuptable.log
```

`table` 子命令有 `--db` 和 `--table` 两个选项，分别用来指定数据库名和表名。其他选项的含义与[备份 TiDB 集群快照](#备份-tidb-集群快照)相同。

### 使用表库过滤功能备份多张表的数据

如果你需要以更复杂的过滤条件来备份多个库/表，执行 `br backup full` 命令，并使用 `--filter` 或 `-f` 来指定[表库过滤](/table-filter.md)规则。

用例：以下命令将所有 `db*.tbl*` 形式的表格数据备份到 s3 的名为 `backup-data` 的 bucket 下面的 `table-filter/2022-01-30/` 前缀目录下。

{{< copyable "shell-regular" >}}

```shell
br backup full \
    --pd "${PDIP}:2379" \
    --filter 'db*.tbl*' \
    --storage "s3://backup-data/table-filter/2022-01-30/" \
    --ratelimit 128 \
    --log-file backupfull.log
```

## 备份数据加密

BR 支持在备份端，或备份到 Amazon S3 的时候在存储服务端，进行备份数据加密，用户可以根据自己情况选择其中一种使用。

### 备份端加密备份数据（实验性功能）

自 TiDB v5.3.0 起，你可配置下列参数在备份过程中到达加密数据的效果：

* `--crypter.method`：加密算法，支持 `aes128-ctr/aes192-ctr/aes256-ctr` 三种算法，缺省值为 `plaintext`，表示不加密
* `--crypter.key`：加密密钥，十六进制字符串格式，`aes128-ctr` 对应 128 位（16 字节）密钥长度，`aes192-ctr` 为 24 字节，`aes256-ctr` 为 32 字节
* `--crypter.key-file`：密钥文件，可直接将存放密钥的文件路径作为参数传入，此时 crypter.key 不需要传入

> **警告：**
>
> - 当前该功能为实验特性，不建议在生产环境中使用。
> - 密钥丢失，备份的数据将无法恢复到集群中。
> - 加密功能需在 br 工具和 TiDB 集群都不低于 v5.3.0 的版本上使用，且加密备份得到的数据无法在低于 v5.3.0 版本的集群上恢复。

备份加密的示例如下：

{{< copyable "shell-regular" >}}

```shell
br backup full\
    --pd ${PDIP}:2379 \
    --storage "s3://backup-data/2022-01-30/"  \
    --crypter.method aes128-ctr \
    --crypter.key 0123456789abcdef0123456789abcdef
```

### Amazon S3 储服务端加密备份数据

BR 支持对备份到 S3 的数据进行 S3 服务端加密 (SSE)。BR S3 服务端加密也支持使用用户自行创建的 AWS KMS 密钥进行加密，详细信息请参考 [BR S3 服务端加密](/encryption-at-rest.md#br-s3-服务端加密)。

## 备份数据到远端存储

BR 支持将数据备份到 Amazon S3/Google Cloud Storage/Azure Blob Storage/NFS，或者实现 s3 协议的其他文件存储服务。下面逐一介绍如何备份数据到对应的备份存储中。

- [使用 S3 存储备份数据](/br/backup-storage-S3.md)
- [使用 Google Cloud Storage 存储备份数据](/br/backup-storage-gcs.md)
- [使用 Azure Blob Storage 存储备份数据](/br/backup-storage-azblob.md)

## 备份性能和影响

TiDB 备份功能对集群性能（事务延迟和 QPS）有一定的影响，但是可以通过调整备份的线程数 [`backup.num-threads`](/tikv-configuration-file.md#num-threads-1) ，以及增加集群配置，来降低备份对集群性能的影响。 

为了更加具体说明备份对集群的影响，这里列举了多次快照备份测试结论来说明影响的范围：

- （使用 5.3 及之前版本）BR 在单 TiKV 存储节点上备份线程数量是节点 CPU 总数量的 75% 的时候，QPS 会下降到备份之前的 30% 左右；
- （使用 5.4 及以后版本）当 BR 在单 TiKV 存储节点上备份的线程数量不大于 `8`、集群总 CPU 利用率不超过 80% 时，BR 备份任务对集群（无论读写负载）影响最大在 20% 左右；
- （使用 5.4 及以后版本）当 BR 在单 TiKV 存储节点上备份的线程数量不大于 `8`、集群总 CPU 利用率不超过 75% 时，BR 备份任务对集群（无论读写负载）影响最大在 10% 左右；
- （使用 5.4 及以后版本）当 BR 在单 TiKV 存储节点上备份的线程数量不大于 `8`、集群总 CPU 利用率不超过 60% 时，BR 备份任务对集群（无论读写负载）几乎没有影响。

通过限制备份的线程数量可以降低备份对集群性能的形象，但是这会影响到备份的性能，以上的多次备份测试结果显示:（单 TiKV 存储节点上）备份速度和备份线程数量呈正比，在线程数量量较少的时候，速度大概是 20M/线程数。例如，单节点 5 个备份线程可达到 100M/s；

> **注意：**
>
> 备份的影响和速度，与集群配置、部署、运行的业务都有比较大的关系，以上结论，经过多个场景的仿真测试，并且在部分合作用户场景中，得到验证，具有一定的参考意义。 但是在不同用户场景中最大影响和性能，最好以用户自己的测试结论为准。

如果需要关于备份影响和性能的更多细节，可以参考以下文档：

- BR 在 5.3 版本引入自动调节备份线程数的功能（默认开启），它可以帮助用户将备份期间集群总 CPU 使用率尽量维持在 80% 以下，具体介绍可以参考 [备份线程自动调节](/br/br-auto-tune.md)。
