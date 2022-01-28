---
title: 从备份数据恢复 TiDB 集群
summary: 了解如何使用 BR 命令行从备份恢复恢复。
---

# 从 TiDB 备份数据恢复

下面介绍各种 TiDB 备份数据恢复功能的使用方式，

## 恢复快照备份数据

BR 支持在一个空集群上执行快照备份恢复，将该集群恢复到快照备份时刻点的集群最新状态。

用例：将 s3 的名为 `backup-data` bucket 下的 `2022-01-30/` 前缀目录中属于 '2022-01-30 07:42:23' 时刻点的快照数据恢复到目标肌群 。

{{< copyable "shell-regular" >}}

```shell
br restore full \
    --pd "${PDIP}:2379" \
    --storage "s3://backup-data/2022-01-30/" \
    --ratelimit 128 \
    --log-file restorefull.log
```

以上命令中，

- `--ratelimit` 选项限制了**每个 TiKV** 执行恢复任务的速度上限（单位 MiB/s）；
- `--log-file` 选项指定把 BR 的 log 写到 `restorefull.log` 文件中。

恢复期间还有进度条会在终端中显示，当进度条前进到 100% 时，说明恢复已完成。在完成恢复后，BR 为了确保数据安全性，还会校验恢复数据。进度条效果如下：

```shell
br restore full \
    --pd "${PDIP}:2379" \
    --storage "local:///tmp/backup" \
    --ratelimit 128 \
    --log-file restorefull.log
Full Restore <---------/...............................................> 17.12%.
```

## 恢复增量备份数据

增量恢复的方法和使用 BR 进行快照恢复的方法并无差别。需要注意，恢复增量数据的时候，需要保证备份时指定的 `last backup ts` 之前备份的数据已经全部恢复到目标集群。

```shell
br restore full \
    --pd "${PDIP}:2379" \
    --storage "s3://backup-data/2022-01-30/incr"  \
    --ratelimit 128 \
    --log-file restorefull.log
```

## 恢复备份数据中指定库表的数据

BR 支持只恢复备份数据中指定库/表的局部数据。该功能在恢复过程中过滤掉不需要的数据，可以用于往 TiDB 集群上恢复指定库/表的数据。

### 恢复单个数据库的数据

要将备份数据中的某个数据库恢复到集群中，可以使用 `br restore db` 命令。该命令的使用帮助可以通过 `br restore db --help` 来获取。

用例：将 s3 中名为 `backup-data` 的 bucket 下的 `db-test/2022-01-30/` 中的 `test` 库的相关的数据恢复的集群中。

{{< copyable "shell-regular" >}}

```shell
br restore db \
    --pd "${PDIP}:2379" \
    --db "test" \
    --ratelimit 128 \
    --storage "s3://backup-data/db-test/2022-01-30/" \
    --log-file restorefull.log
```

以上命令中 `--db` 选项指定了需要恢复的数据库名字。其余选项的含义与[恢复快照备份数据](#恢快照部备份数据)相同。

> **注意**：
>
> 恢复备份数据的时候，`--db` 选项指定的数据库名必须与执行备份时候 `--db`选项指定的数据库名相同，否则无法恢复成功。由于备份数据的元文件`backupmeta` 记录了该数据库名，因此只能将数据恢复到同名的数据库。推荐做法是把备份文件恢复到另一个集群的同名数据库中。

### 恢复单张表的数据

要将备份数据中的某张数据表恢复到集群中，可以使用 `br restore table` 命令。该命令的使用帮助可通过 `br restore table --help` 来获取。

用例：将 s3 中名为 `backup-data` 的 bucket 下的 `table-db-usertable/2022-01-30/` 中的 `test`.`usertable` 表的相关的数据恢复的集群中。

{{< copyable "shell-regular" >}}

```shell
br restore table \
    --pd "${PDIP}:2379" \
    --db "test" \
    --table "usertable" \
    --ratelimit 128 \
    --storage "s3://backup-data/table-db-usertable/2022-01-30/" \
    --log-file restorefull.log
```

以上命令中 `--table` 选项指定了需要恢复的表名。其余选项的含义与[恢复单个数据库](#恢复单个数据库的数据)相同。

### 使用表库功能过滤恢复数据

如果你需要用复杂的过滤条件来恢复多个表，执行 `br restore full` 命令，并用 `--filter` 或 `-f` 指定使用[表库过滤](/table-filter.md)。

用例：将 s3 中名为 `backup-data` 的 bucket 下的 `table-filter/2022-01-30/` 中能匹配上 `db*.tbl*`的表的相关的数据恢复的集群中。

{{< copyable "shell-regular" >}}

```shell
br restore full \
    --pd "${PDIP}:2379" \
    --filter 'db*.tbl*' \
    --storage "s3://backup-data/table-filter/2022-01-30/"  \
    --log-file restorefull.log
```

## 恢复加密的备份数据

> **警告：**
>
> - 当前该功能为实验特性，不建议在生产环境中使用。

在对数据做加密备份后，恢复操作需传入相应的解密参数，解密算法或密钥不正确则无法恢复，解密参数和加密参数一致即可。解密恢复的示例如下：

{{< copyable "shell-regular" >}}

```shell
br restore full\
    --pd ${PDIP}:2379 \
    --storage "s3://backup-data/2022-01-30/" \
    --crypter.method aes128-ctr \
    --crypter.key 0123456789abcdef0123456789abcdef
```

## 从远端存储恢复备份数据

BR 支持将数据备份到 Amazon S3/Google Cloud Storage/Azure Blob Storage/NFS，或者实现 s3 协议的其他文件存储服务。下面逐一介绍如何从对应的备份存储中恢复备份数据。

- [使用 S3 存储备份数据](/br/backup-storage-S3.md)
- [使用 Google Cloud Storage 存储备份数据](/br/backup-storage-gcs.md)
- [使用 Azure Blob Storage 存储备份数据](/br/backup-storage-azblob.md)

## 恢复性能和影响

- TiDB 恢复的时候会尽可能打满 TiKV CPU、磁盘 IO、网络带宽等资源，所以推荐在空的集群上执行备份数据的恢复，避免对正在运行的业务产生影响；
- 备份数据恢复速度，能够达到（单台 TiKV 节点） 100 MB/s。 

> **注意：**
>
> 备份数据的恢复速度，与集群配置、部署、运行的业务都有比较大的关系，以上结论，经过多个场景的仿真测试，并且在部分合作用户场景中，得到验证，具有一定的参考意义。 但是在不同用户场景中恢复速度，最好以用户自己的测试结论为准。

## 恢复创建在 `mysql` 数据库下的表（实验性功能）

BR 会默认备份 `mysql` 数据库下的表。在执行恢复时，`mysql` 下的表默认不会被恢复。如果需要恢复 `mysql` 下的用户创建的表，可以通过 [table filter](/table-filter.md#表库过滤语法) 来显式地包含目标表。以下示例中要恢复目标用户表为 `mysql.usertable`；该命令会在执行正常的恢复的同时恢复 `mysql.usertable`。

{{< copyable "shell-regular" >}}

```shell
br restore full -f '*.*' -f '!mysql.*' -f 'mysql.usertable' -s $external_storage_url --ratelimit 128
```

在如上的命令中，`-f '*.*'` 用于覆盖掉默认的规则，`-f '!mysql.*'` 指示 BR 不要恢复 `mysql` 中的表，除非另有指定。`-f 'mysql.usertable'` 则指定需要恢复 `mysql.usertable`。具体原理请参考 [table filter 的文档](/table-filter.md#表库过滤语法)。

如果只需要恢复 `mysql.usertable`，而无需恢复其他表，可以使用以下命令：

{{< copyable "shell-regular" >}}

```shell
br restore full -f 'mysql.usertable' -s $external_storage_url --ratelimit 128
```

> **警告：**
>
> 虽然系统表（例如 `mysql.tidb` 等）可以通过 BR 进行备份和恢复，但是部分系统表在恢复之后可能会出现非预期的状况，已知的异常如下：
>
> - 统计信息表（`mysql.stat_*`）无法被恢复。
> - 系统变量表（`mysql.tidb`，`mysql.global_variables`）无法被恢复。
> - 用户信息表（`mysql.user`，`mysql.columns_priv`，`tables_priv`, `global_grants`, `global_priv`）无法被恢复。
> - GC 数据等系统表。
> 
> 恢复系统表可能还存在更多兼容性问题。为了防止意外发生，请避免在生产环境中恢复系统表。
