---
title: 使用 BR 命令行进行备份恢复
summary: 了解如何使用 BR 命令行进行集群数据备份和恢复。
---

# 使用 BR 命令行进行备份恢复

本文介绍如何 BR 命令行进行 TiDB 集群数据的备份和恢复。

在阅读本文前，请确保你已通读[备份与恢复工具 BR 简介](/br/backup-and-restore-tool.md)，尤其是[使用限制](/br/backup-and-restore-tool.md#使用限制)和[最佳实践](/br/backup-and-restore-tool.md#最佳实践)这两节。

## BR 命令行描述

一条 `br` 命令是由子命令、选项和参数组成的。子命令即不带 `-` 或者 `--` 的字符。选项即以 `-` 或者 `--` 开头的字符。参数即子命令或选项字符后紧跟的、并传递给命令和选项的字符。

以下是一条完整的 `br` 命令行：

`br backup full --pd "${PDIP}:2379" -s "local:///tmp/backup"`

命令行各部分的解释如下：

* `backup`：`br` 的子命令
* `full`：`backup` 的子命令
* `-s` 或 `--storage`：备份保存的路径
* `"local:///tmp/backup"`：`-s` 的参数，保存的路径为各个 TiKV 节点本地磁盘的 `/tmp/backup`
* `--pd`：PD 服务地址
* `"${PDIP}:2379"`：`--pd` 的参数

> **注意：**
>
> 在使用 `local` storage 的时候，备份数据会分散在各个节点的本地文件系统中。
>
> **不建议**在生产环境中备份到本地磁盘，因为在日后恢复的时候，**必须**手动聚集这些数据才能完成恢复工作（见[恢复集群数据](#使用-br-命令行恢复集群数据)）。
>
> 聚集这些备份数据可能会造成数据冗余和运维上的麻烦，而且在不聚集这些数据便直接恢复的时候会遇到颇为迷惑的 `SST file not found` 报错。
>
> 建议在各个节点挂载 NFS 网盘，或者直接备份到 `S3` 对象存储中。

### 命令和子命令

BR 由多层命令组成。目前，BR 包含 `backup`、`restore` 和 `version` 三个子命令:

* `br backup` 用于备份 TiDB 集群
* `br restore` 用于恢复 TiDB 集群

以上三个子命令可能还包含这些子命令：

* `full`：可用于备份或恢复全部数据。
* `db`：可用于备份或恢复集群中的指定数据库。
* `table`：可用于备份或恢复集群指定数据库中的单张表。

### 常用选项

* `--pd`：用于连接的选项，表示 PD 服务地址，例如 `"${PDIP}:2379"`。
* `-h`/`--help`：获取所有命令和子命令的使用帮助。例如 `br backup --help`。
* `-V` (或 `--version`)：检查 BR 版本。
* `--ca`：指定 PEM 格式的受信任 CA 的证书文件路径。
* `--cert`：指定 PEM 格式的 SSL 证书文件路径。
* `--key`：指定 PEM 格式的 SSL 证书密钥文件路径。
* `--status-addr`：BR 向 Prometheus 提供统计数据的监听地址。

## 使用 BR 命令行备份集群数据

使用 `br backup` 命令来备份集群数据。可选择添加 `full` 或 `table` 子命令来指定备份的范围：全部集群数据或单张表的数据。

如果 BR 的版本低于 v4.0.8，而且备份时间可能超过设定的 [`tikv_gc_life_time`](/garbage-collection-configuration.md#tikv_gc_life_time)（默认 `10m0s`，即表示 10 分钟），需要手动将该参数调大。

例如，将 `tikv_gc_life_time` 调整为 `720h`：

{{< copyable "sql" >}}

```sql
mysql -h${TiDBIP} -P4000 -u${TIDB_USER} ${password_str} -Nse \
    "update mysql.tidb set variable_value='720h' where variable_name='tikv_gc_life_time'";
```

自 v4.0.8 起 BR 已经支持自适应 GC，无需手动调整 `tikv_gc_life_time`。

### 备份全部集群数据

要备份全部集群数据，可使用 `br backup full` 命令。该命令的使用帮助可以通过 `br backup full -h` 或 `br backup full --help` 来获取。

用例：将所有集群数据备份到各个 TiKV 节点的 `/tmp/backup` 路径，同时也会将备份的元信息文件 `backupmeta` 写到该路径下。

> **注意：**
>
> + 经测试，在全速备份的情况下，如果备份盘和服务盘不同，在线备份会让只读线上服务的 QPS 下降 15%~25% 左右。如果希望降低影响，请参考 `--ratelimit` 进行限速。
>
> + 假如备份盘和服务盘相同，备份将会和服务争夺 I/O 资源，这可能会让只读线上服务的 QPS 骤降一半以上。请尽量禁止将在线服务的数据备份到 TiKV 的数据盘。

{{< copyable "shell-regular" >}}

```shell
br backup full \
    --pd "${PDIP}:2379" \
    --storage "local:///tmp/backup" \
    --ratelimit 128 \
    --log-file backupfull.log
```

以上命令中，`--ratelimit` 选项限制了**每个 TiKV** 执行备份任务的速度上限（单位 MiB/s）。`--log-file` 选项指定把 BR 的 log 写到 `backupfull.log` 文件中。

备份期间有进度条在终端中显示。当进度条前进到 100% 时，说明备份已完成。在完成备份后，BR 为了确保数据安全性，还会校验备份数据。进度条效果如下：

```shell
br backup full \
    --pd "${PDIP}:2379" \
    --storage "local:///tmp/backup" \
    --ratelimit 128 \
    --log-file backupfull.log
Full Backup <---------/................................................> 17.12%.
```

### 备份单个数据库的数据

要备份集群中指定单个数据库的数据，可使用 `br backup db` 命令。同样可通过 `br backup db -h` 或 `br backup db --help` 来获取子命令 `db` 的使用帮助。

用例：将数据库 `test` 备份到各个 TiKV 节点的 `/tmp/backup` 路径，同时也会将备份的元信息文件 `backupmeta` 写到该路径下。

{{< copyable "shell-regular" >}}

```shell
br backup db \
    --pd "${PDIP}:2379" \
    --db test \
    --storage "local:///tmp/backup" \
    --ratelimit 128 \
    --log-file backuptable.log
```

`db` 子命令的选项为 `--db`，用来指定数据库名。其他选项的含义与[备份全部集群数据](#备份全部集群数据)相同。

备份期间有进度条在终端中显示。当进度条前进到 100% 时，说明备份已完成。在完成备份后，BR 为了确保数据安全性，还会校验备份数据。

### 备份单张表的数据

要备份集群中指定单张表的数据，可使用 `br backup table` 命令。同样可通过 `br backup table -h` 或 `br backup table --help` 来获取子命令 `table` 的使用帮助。

用例：将表 `test.usertable` 备份到各个 TiKV 节点的 `/tmp/backup` 路径，同时也会将备份的元信息文件 `backupmeta` 写到该路径下。

{{< copyable "shell-regular" >}}

```shell
br backup table \
    --pd "${PDIP}:2379" \
    --db test \
    --table usertable \
    --storage "local:///tmp/backup" \
    --ratelimit 128 \
    --log-file backuptable.log
```

`table` 子命令有 `--db` 和 `--table` 两个选项，分别用来指定数据库名和表名。其他选项的含义与[备份全部集群数据](#备份全部集群数据)相同。

备份期间有进度条在终端中显示。当进度条前进到 100% 时，说明备份已完成。在完成备份后，BR 为了确保数据安全性，还会校验备份数据。

### 使用表库过滤功能备份多张表的数据

如果你需要以更复杂的过滤条件来备份多个表，执行 `br backup full` 命令，并使用 `--filter` 或 `-f` 来指定[表库过滤](/table-filter.md)规则。

用例：以下命令将所有 `db*.tbl*` 形式的表格数据备份到每个 TiKV 节点上的 `/tmp/backup` 路径，并将 `backupmeta` 文件写入该路径。

{{< copyable "shell-regular" >}}

```shell
br backup full \
    --pd "${PDIP}:2379" \
    --filter 'db*.tbl*' \
    --storage "local:///tmp/backup" \
    --ratelimit 128 \
    --log-file backupfull.log
```

### 备份数据到 Amazon S3 后端存储

如果备份的存储并不是在本地，而是在 Amazon 的 S3 后端存储，那么需要在 `storage` 子命令中指定 S3 的存储路径，并且赋予 BR 节点和 TiKV 节点访问 Amazon S3 的权限。

这里可以参照 [AWS 官方文档](https://docs.aws.amazon.com/zh_cn/AmazonS3/latest/user-guide/create-bucket.html)在指定的 `Region` 区域中创建一个 S3 桶 `Bucket`，如果有需要，还可以参照 [AWS 官方文档](https://docs.aws.amazon.com/zh_cn/AmazonS3/latest/user-guide/create-folder.html) 在 Bucket 中创建一个文件夹 `Folder`。

> **注意：**
>
> 要完成一次备份，通常 TiKV 和 BR 需要的最小权限为 `s3:ListBucket`，`s3:PutObject` 和 `s3:AbortMultipartUpload`。

将有权限访问该 S3 后端存储的账号的 `SecretKey` 和 `AccessKey` 作为环境变量传入 BR 节点，并且通过 BR 将权限传给 TiKV 节点。

{{< copyable "shell-regular" >}}

```shell
export AWS_ACCESS_KEY_ID=${AccessKey}
export AWS_SECRET_ACCESS_KEY=${SecretKey}
```

在进行 BR 备份时，显示指定参数 `--s3.region` 和 `--send-credentials-to-tikv`, `--s3.region` 表示 S3 存储所在的区域，`--send-credentials-to-tikv` 表示将 S3 的访问权限传递给 TiKV 节点。

{{< copyable "shell-regular" >}}

```shell
br backup full \
    --pd "${PDIP}:2379" \
    --storage "s3://${Bucket}/${Folder}" \
    --s3.region "${region}" \
    --send-credentials-to-tikv=true \
    --ratelimit 128 \
    --log-file backuptable.log
```

### 增量备份

如果想要备份增量，只需要在备份的时候指定**上一次的备份时间戳** `--lastbackupts` 即可。

注意增量备份有以下限制：

- 增量备份需要与前一次全量备份在不同的路径下
- GC safepoint 必须在 `lastbackupts` 之前

{{< copyable "shell-regular" >}}

```shell
br backup full\
    --pd ${PDIP}:2379 \
    --ratelimit 128 \
    -s local:///home/tidb/backupdata/incr \
    --lastbackupts ${LAST_BACKUP_TS}
```

以上命令会备份 `(LAST_BACKUP_TS, current PD timestamp]` 之间的增量数据。

你可以使用 `validate` 指令获取上一次备份的时间戳，示例如下：

{{< copyable "shell-regular" >}}

```shell
LAST_BACKUP_TS=`br validate decode --field="end-version" -s local:///home/tidb/backupdata | tail -n1`
```

示例备份的增量数据记录 `(LAST_BACKUP_TS, current PD timestamp]` 之间的数据变更，以及这段时间内的 DDL。在恢复的时候，BR 会先把所有 DDL 恢复，而后才会恢复数据。

### Raw KV 备份（实验性功能）

> **警告：**
>
> Raw KV 备份功能还在实验中，没有经过完备的测试。暂时请避免在生产环境中使用该功能。

在某些使用场景下，TiKV 可能会独立于 TiDB 运行。考虑到这点，BR 也提供跳过 TiDB 层，直接备份 TiKV 中数据的功能：

{{< copyable "shell-regular" >}}

```shell
br backup raw --pd $PD_ADDR \
    -s "local://$BACKUP_DIR" \
    --start 31 \
    --ratelimit 128 \
    --end 3130303030303030 \
    --format hex \
    --cf default
```

以上命令会备份 default CF 上 `[0x31, 0x3130303030303030)` 之间的所有键到 `$BACKUP_DIR` 去。

这里，`--start` 和 `--end` 的参数会先依照 `--format` 指定的方式解码，再被送到 TiKV 上去，目前支持以下解码方式：

- "raw"：不进行任何操作，将输入的字符串直接编码为二进制格式的键。
- "hex"：将输入的字符串视作十六进制数字。这是默认的编码方式。
- "escape"：对输入的字符串进行转义之后，再编码为二进制格式。

## 使用 BR 命令行恢复集群数据

使用 `br restore` 命令来恢复备份数据。可选择添加 `full`、`db` 或 `table` 子命令来指定恢复操作的范围：全部集群数据、某个数据库或某张数据表。

> **注意：**
>
> 如果使用本地存储，在恢复前**必须**将所有备份的 SST 文件复制到各个 TiKV 节点上 `--storage` 指定的目录下。
>
> 即使每个 TiKV 节点最后只需要读取部分 SST 文件，这些节点也需要有所有 SST 文件的完全访问权限。原因如下：
>
> * 数据被复制到了多个 Peer 中。在读取 SST 文件时，这些文件必须要存在于所有 Peer 中。这与数据的备份不同，在备份时，只需从单个节点读取。
> * 在数据恢复的时候，每个 Peer 分布的位置是随机的，事先并不知道哪个节点将读取哪个文件。
>
> 使用共享存储可以避免这些情况。例如，在本地路径上安装 NFS，或使用 S3。利用这些网络存储，各个节点都可以自动读取每个 SST 文件，此时上述注意事项不再适用。

### 恢复全部备份数据

要将全部备份数据恢复到集群中来，可使用 `br restore full` 命令。该命令的使用帮助可以通过 `br restore full -h` 或 `br restore full --help` 来获取。

用例：将 `/tmp/backup` 路径中的全部备份数据恢复到集群中。

{{< copyable "shell-regular" >}}

```shell
br restore full \
    --pd "${PDIP}:2379" \
    --storage "local:///tmp/backup" \
    --ratelimit 128 \
    --log-file restorefull.log
```

以上命令中，`--ratelimit` 选项限制了**每个 TiKV** 执行恢复任务的速度上限（单位 MiB/s）。`--log-file` 选项指定把 BR 的 log 写到 `restorefull.log` 文件中。

恢复期间还有进度条会在终端中显示，当进度条前进到 100% 时，说明恢复已完成。在完成恢复后，BR 为了确保数据安全性，还会校验恢复数据。进度条效果如下：

```shell
br restore full \
    --pd "${PDIP}:2379" \
    --storage "local:///tmp/backup" \
    --ratelimit 128 \
    --log-file restorefull.log
Full Restore <---------/...............................................> 17.12%.
```

### 恢复单个数据库的数据

要将备份数据中的某个数据库恢复到集群中，可以使用 `br restore db` 命令。该命令的使用帮助可以通过 `br restore db -h` 或 `br restore db --help` 来获取。

用例：将 `/tmp/backup` 路径中备份数据中的某个数据库恢复到集群中。

{{< copyable "shell-regular" >}}

```shell
br restore db \
    --pd "${PDIP}:2379" \
    --db "test" \
    --ratelimit 128 \
    --storage "local:///tmp/backup" \
    --log-file restorefull.log
```

以上命令中 `--db` 选项指定了需要恢复的数据库名字。其余选项的含义与[恢复全部备份数据](#恢复全部备份数据)相同。

> **注意**：
>
> 恢复备份数据的时候，`--db` 选项指定的数据库名必须与执行备份时候 `--db`选项指定的数据库名相同，否则无法恢复成功。由于备份数据的元文件`backupmeta` 记录了该数据库名，因此只能将数据恢复到同名的数据库。推荐做法是把备份文件恢复到另一个集群的同名数据库中。

### 恢复单张表的数据

要将备份数据中的某张数据表恢复到集群中，可以使用 `br restore table` 命令。该命令的使用帮助可通过 `br restore table -h` 或 `br restore table --help` 来获取。

用例：将 `/tmp/backup` 路径下的备份数据中的某个数据表恢复到集群中。

{{< copyable "shell-regular" >}}

```shell
br restore table \
    --pd "${PDIP}:2379" \
    --db "test" \
    --table "usertable" \
    --ratelimit 128 \
    --storage "local:///tmp/backup" \
    --log-file restorefull.log
```

### 使用表库功能过滤恢复数据

如果你需要用复杂的过滤条件来恢复多个表，执行 `br restore full` 命令，并用 `--filter` 或 `-f` 指定使用[表库过滤](/table-filter.md)。

用例：以下命令将备份在 `/tmp/backup` 路径的表的子集恢复到集群中。

{{< copyable "shell-regular" >}}

```shell
br restore full \
    --pd "${PDIP}:2379" \
    --filter 'db*.tbl*' \
    --storage "local:///tmp/backup" \
    --log-file restorefull.log
```

### 从 Amazon S3 后端存储恢复数据

如果需要恢复的数据并不是存储在本地，而是在 Amazon 的 S3 后端，那么需要在 `storage` 子命令中指定 S3 的存储路径，并且赋予 BR 节点和 TiKV 节点访问 Amazon S3 的权限。

> **注意：**
>
> 要完成一次恢复，通常 TiKV 和 BR 需要的最小权限为 `s3:ListBucket` 和 `s3:GetObject`。

将有权限访问该 S3 后端存储的账号的 `SecretKey` 和 `AccessKey` 作为环境变量传入 BR 节点，并且通过 BR 将权限传给 TiKV 节点。

{{< copyable "shell-regular" >}}

```shell
export AWS_ACCESS_KEY_ID=${AccessKey}
export AWS_SECRET_ACCESS_KEY=${SecretKey}
```

在进行 BR 恢复时，显示指定参数 `--s3.region` 和 `--send-credentials-to-tikv`, `--s3.region` 表示 S3 存储所在的区域，`--send-credentials-to-tikv` 表示将 S3 的访问权限传递给 TiKV 节点。`--storage`参数中的 `Bucket` 和 `Folder` 分别代表需要恢复的数据所在的 S3 存储桶和文件夹。

{{< copyable "shell-regular" >}}

```shell
br restore full \
    --pd "${PDIP}:2379" \
    --storage "s3://${Bucket}/${Folder}" \
    --s3.region "${region}" \
    --ratelimit 128 \
    --send-credentials-to-tikv=true \
    --log-file restorefull.log
```

以上命令中 `--table` 选项指定了需要恢复的表名。其余选项的含义与[恢复单个数据库](#恢复单个数据库的数据)相同。

### 增量恢复

增量恢复的方法和使用 BR 进行全量恢复的方法并无差别。需要注意，恢复增量数据的时候，需要保证备份时指定的 `last backup ts` 之前备份的数据已经全部恢复到目标集群。

### 恢复创建在 `mysql` 数据库下的表（实验性功能）

BR 可以并且会默认备份 `mysql` 数据库下的表。

在执行恢复时，`mysql` 下的表默认不会被恢复。如果需要恢复 `mysql` 下的用户创建的表，可以通过 [table filter](/table-filter.md#表库过滤语法) 来显式地包含目标表。以下示例中要恢复目标用户表为 `mysql.usertable`；该命令会在执行正常的恢复的同时恢复 `mysql.usertable`。

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
> - 用户信息表（`mysql.user`，`mysql.columns_priv`，等等）无法被恢复。
> - GC 数据无法被恢复。
> 
> 恢复系统表可能还存在更多兼容性问题。为了防止意外发生，请避免在生产环境中恢复系统表。

### Raw KV 恢复（实验性功能）

> **警告：**
>
> Raw KV 恢复功能还在实验中，没有经过完备的测试。暂时请避免在生产环境中使用该功能。

和 [Raw KV 备份](#raw-kv-备份实验性功能)相似地，恢复 Raw KV 的命令如下：

{{< copyable "shell-regular" >}}

```shell
br restore raw --pd $PD_ADDR \
    -s "local://$BACKUP_DIR" \
    --start 31 \
    --end 3130303030303030 \
    --ratelimit 128 \
    --format hex \
    --cf default
```

以上命令会将范围在 `[0x31, 0x3130303030303030)` 的已备份键恢复到 TiKV 集群中。这里键的编码方式和备份时相同。

### 在线恢复（实验性功能）

> **警告：**
>
> 在线恢复功能还在实验中，没有经过完备的测试，同时还依赖 PD 的不稳定特性 Placement Rules。暂时请避免在生产环境中使用该功能。

在恢复的时候，写入过多的数据会影响在线集群的性能。为了尽量避免影响线上业务，BR 支持通过 [Placement rules](/configure-placement-rules.md) 隔离资源。让下载、导入 SST 的工作仅仅在指定的几个节点（下称“恢复节点”）上进行，具体操作如下：

1. 配置 PD，启动 Placement rules：

    {{< copyable "shell-regular" >}}

    ```shell
    echo "config set enable-placement-rules true" | pd-ctl
    ```

2. 编辑恢复节点 TiKV 的配置文件，在 `server` 一项中指定：

    {{< copyable "" >}}

    ```
    [server]
    labels = { exclusive = "restore" }
    ```

3. 启动恢复节点的 TiKV，使用 BR 恢复备份的文件，和非在线恢复相比，这里只需要加上 `--online` 标志即可：

    {{< copyable "shell-regular" >}}

    ```shell
    br restore full \
        -s "local://$BACKUP_DIR" \
        --ratelimit 128 \
        --pd $PD_ADDR \
        --online
    ```
