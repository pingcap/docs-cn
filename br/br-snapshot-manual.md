---
title: 快照备份和恢复命令行手册
summary: 介绍快照备份和恢复的命令行
aliases: ['/zh/tidb/dev/br-usage-backup/','/zh/tidb/dev/br-usage-restore/','/zh/tidb/dev/br-usage-restore-for-maintain/', '/zh/tidb/dev/br-usage-backup-for-maintain/']
---

# 快照备份和恢复命令行手册

本文介绍快照备份和恢复的命令行，包括：

- [备份 TiDB 集群快照](#备份-tidb-集群快照)
- [备份单个数据库的数据](#备份单个数据库的数据)
- [备份单张表的数据](#备份单张表的数据)
- [使用表库过滤功能备份多张表的数据](#使用表库过滤功能备份多张表的数据)
- [备份数据加密](#备份数据加密)
- [恢复快照备份数据](#恢复快照备份数据)
- [恢复单个数据库的数据](#恢复单个数据库的数据)
- [恢复单张表的数据](#恢复单张表的数据)
- [使用表库功能过滤恢复数据](#使用表库功能过滤恢复数据)
- [恢复加密的备份数据](#恢复加密的备份数据)

如果你想了解如何进行备份和恢复，可以参考以下教程

- [全量备份恢复 —— 快照备份和恢复功能使用指南](/br/br-snapshot-guide.md)
- [TiDB 集群备份和恢复实践示例](/br/backup-and-restore-use-cases.md)

## 备份 TiDB 集群快照

使用 `br backup full` 可以备份 TiDB 最新的或者指定时间点的快照数据。执行 `br backup full --help` 可获取该命令的使用帮助。

{{< copyable "shell-regular" >}}

```shell
br backup full \
    --pd "${PD_IP}:2379" \
    --backupts '2022-09-08 13:30:00' \
    --storage "s3://${backup_collection_addr}/snapshot-${date}?access_key=${access_key}&secret_access_key=${secret_access_key}" \
    --ratelimit 128 \
    --log-file backupfull.log
```

以上命令中：

- `--backupts`：快照对应的物理时间点。如果该快照的数据被 GC 了，那么 `br backup` 命令会报错退出；如果你没有指定该参数，那么 BR 会选取备份开始的时间点所对应的快照。
- `--ratelimit`：**每个 TiKV** 执行备份任务的速度上限（单位 MiB/s）。
- `--log-file`：BR log 写入的目标文件。

备份期间有进度条在终端中显示，显示效果如下。当进度条前进到 100% 时，说明备份已完成。

```shell
Full Backup <---------/................................................> 17.12%.
```

## 备份 TiDB 集群的指定库表的数据

BR 支持只备份集群快照和增量数据中指定库/表的局部数据。该功能在快照备份和增量数据备份的基础上，过滤掉不需要的数据，帮助用户备份实现只备份关键业务的数据。

### 备份单个数据库的数据

使用 `br backup db` 命令备份集群中指定单个数据库的数据。

示例：将单个数据库 `test` 备份到 s3。

{{< copyable "shell-regular" >}}

```shell
br backup db \
    --pd "${PD_IP}:2379" \
    --db test \
    --storage "s3://${backup_collection_addr}/snapshot-${date}?access_key=${access_key}&secret_access_key=${secret_access_key}" \
    --ratelimit 128 \
    --log-file backuptable.log
```

`db` 子命令的选项为 `--db`，用来指定数据库名。其他选项的含义与[备份 TiDB 集群快照](#备份-tidb-集群快照)相同。

### 备份单张表的数据

使用 `br backup table` 命令。

用例：将表 `test.usertable` 备份到 s3。

{{< copyable "shell-regular" >}}

```shell
br backup table \
    --pd "${PD_IP}:2379" \
    --db test \
    --table usertable \
    --storage "s3://${backup_collection_addr}/snapshot-${date}?access_key=${access_key}&secret_access_key=${secret_access_key}" \
    --ratelimit 128 \
    --log-file backuptable.log
```

`table` 子命令有 `--db` 和 `--table` 两个选项，分别用来指定数据库名和表名。其他选项的含义与[备份 TiDB 集群快照](#备份-tidb-集群快照)相同。

### 使用表库过滤功能备份多张表的数据

如果你需要以更复杂的过滤条件来备份多个库/表，执行 `br backup full` 命令，并使用 `--filter` 或 `-f` 来指定[表库过滤](/table-filter.md)规则。

示例：以下命令将所有 `db*.tbl*` 形式的表格数据备份到 s3。

{{< copyable "shell-regular" >}}

```shell
br backup full \
    --pd "${PD_IP}:2379" \
    --filter 'db*.tbl*' \
    --storage "s3://${backup_collection_addr}/snapshot-${date}?access_key=${access_key}&secret_access_key=${secret_access_key}" \
    --ratelimit 128 \
    --log-file backupfull.log
```

## 备份数据加密

> **警告：**
>
> 当前该功能为实验特性，不建议在生产环境中使用。

BR 支持在备份端，或备份到 Amazon S3 的时候在存储服务端，进行备份数据加密，用户可以根据自己情况选择其中一种使用。

### 备份端加密备份数据

自 TiDB v5.3.0 起，你可配置下列参数在备份过程中到达加密数据的效果：

- `--crypter.method`：加密算法，支持 `aes128-ctr/aes192-ctr/aes256-ctr` 三种算法，缺省值为 `plaintext`，表示不加密
- `--crypter.key`：加密密钥，十六进制字符串格式，`aes128-ctr` 对应 128 位（16 字节）密钥长度，`aes192-ctr` 为 24 字节，`aes256-ctr` 为 32 字节
- `--crypter.key-file`：密钥文件，可直接将存放密钥的文件路径作为参数传入，此时 crypter.key 不需要传入

备份加密的示例如下：

{{< copyable "shell-regular" >}}

```shell
br backup full\
    --pd ${PD_IP}:2379 \
    --storage "s3://${backup_collection_addr}/snapshot-${date}?access_key=${access_key}&secret_access_key=${secret_access_key}" \
    --crypter.method aes128-ctr \
    --crypter.key 0123456789abcdef0123456789abcdef
```

> **注意：**
>
> - 密钥丢失，备份的数据将无法恢复到集群中。
> - 加密功能需在 br 工具和 TiDB 集群都不低于 v5.3.0 的版本上使用，且加密备份得到的数据无法在低于 v5.3.0 版本的集群上恢复。

### Amazon S3 存储服务端加密备份数据

BR 支持对备份到 S3 的数据进行 S3 服务端加密 (SSE)。BR S3 服务端加密也支持使用用户自行创建的 AWS KMS 密钥进行加密，详细信息请参考 [BR S3 服务端加密](/encryption-at-rest.md#br-s3-服务端加密)。

## 恢复快照备份数据

使用 `br restore full` 恢复一个快照备份恢复，将该集群恢复到快照备份对应的数据状态。

{{< copyable "shell-regular" >}}

```shell
br restore full \
    --pd "${PD_IP}:2379" \
    --storage "s3://${backup_collection_addr}/snapshot-${date}?access_key=${access_key}&secret_access_key=${secret_access_key}" \
    --ratelimit 128 \
    --log-file restorefull.log
```

以上命令中，

- `--ratelimit`：**每个 TiKV** 执行恢复任务的速度上限（单位 MiB/s）
- `--log-file`：BR log 写入的目标文件

恢复期间还有进度条会在终端中显示，进度条效果如下。当进度条前进到 100% 时，说明恢复已完成。在完成恢复后，BR 为了确保数据安全性，还会校验恢复数据。

```shell
Full Restore <---------/...............................................> 17.12%.
```

## 恢复备份数据中指定库表的数据

BR 支持只恢复备份数据中指定库/表的局部数据。该功能在恢复过程中过滤掉不需要的数据，可以用于往 TiDB 集群上恢复指定库/表的数据。

### 恢复单个数据库的数据

使用 `br restore db` 命令

用例：将 s3 中的 `test` 库的相关数据恢复到集群中。

{{< copyable "shell-regular" >}}

```shell
br restore db \
    --pd "${PD_IP}:2379" \
    --db "test" \
    --ratelimit 128 \
    --storage "s3://${backup_collection_addr}/snapshot-${date}?access_key=${access_key}&secret_access_key=${secret_access_key}" \
    --log-file restore_db.log
```

以上命令中 `--db` 选项指定了需要恢复的数据库名字。其余选项的含义与[恢复快照备份数据](#恢复快照备份数据)相同。

> **注意**：
>
> 恢复备份数据的时候，`--db` 选项指定的数据库名必须与执行备份时候 `--db`选项指定的数据库名相同，否则无法恢复成功。由于备份数据的元文件`backupmeta` 记录了该数据库名，因此只能将数据恢复到同名的数据库。推荐做法是把备份文件恢复到另一个集群的同名数据库中。

### 恢复单张表的数据

使用 `br restore table` 命令。

用例：将 s3 中 `test`.`usertable` 表的相关的数据恢复的集群中。

{{< copyable "shell-regular" >}}

```shell
br restore table \
    --pd "${PD_IP}:2379" \
    --db "test" \
    --table "usertable" \
    --ratelimit 128 \
    --storage "s3://${backup_collection_addr}/snapshot-${date}?access_key=${access_key}&secret_access_key=${secret_access_key}" \
    --log-file restore_table.log
```

以上命令中 `--table` 选项指定了需要恢复的表名。其余选项的含义与[恢复单个数据库](#恢复单个数据库的数据)相同。

### 使用表库功能过滤恢复数据

如果你需要用复杂的过滤条件来恢复多个表，执行 `br restore full` 命令，并用 `--filter` 或 `-f` 指定使用[表库过滤](/table-filter.md)。

用例：将 s3 中能匹配上 `db*.tbl*`的表的相关的数据恢复的集群中。

{{< copyable "shell-regular" >}}

```shell
br restore full \
    --pd "${PD_IP}:2379" \
    --filter 'db*.tbl*' \
    --storage "s3://${backup_collection_addr}/snapshot-${date}?access_key=${access_key}&secret_access_key=${secret_access_key}" \
    --log-file restorefull.log
```

## 恢复加密的备份数据

> **警告：**
>
> 当前该功能为实验特性，不建议在生产环境中使用。

在对数据做加密备份后，恢复操作需传入相应的解密参数，解密算法或密钥不正确则无法恢复，解密参数和加密参数一致即可。解密恢复的示例如下：

{{< copyable "shell-regular" >}}

```shell
br restore full\
    --pd ${PD_IP}:2379 \
    --storage "s3://${backup_collection_addr}/snapshot-${date}?access_key=${access_key}&secret_access_key=${secret_access_key}" \
    --crypter.method aes128-ctr \
    --crypter.key 0123456789abcdef0123456789abcdef
```
