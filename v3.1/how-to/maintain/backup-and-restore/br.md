---
title: 使用 BR 进行备份与恢复
summary: 了解如何使用 BR 工具进行集群数据备份和恢复。
category: how-to
---

# 使用 BR 进行备份与恢复

Backup & Restore（以下简称 BR）是 TiDB 分布式备份恢复的命令行工具，用于对 TiDB 集群进行数据备份和恢复。相比 [`mydumper`/`loader`](/v3.1/how-to/maintain/backup-and-restore/mydumper-loader.md)，BR 更适合大数据量的场景。本文档介绍了 BR 的使用限制、工作原理、命令行描述、备份恢复用例以及最佳实践。

## 使用限制

- BR 只支持 TiDB v3.1 及以上版本。
- 目前只支持在全新的集群上执行恢复操作。
- BR 备份最好串行执行，否则不同备份任务之间会相互影响。

## 推荐部署配置

- 推荐 BR 部署在 PD 节点上。
- 推荐使用一块高性能 SSD 网盘，挂载到 BR 节点和所有 TiKV 节点上，网盘推荐万兆网卡，否则带宽有可能成为备份恢复时的性能瓶颈。

## 下载 Binary

详见[下载链接](/v3.1/reference/tools/download.md#快速备份和恢复br)。

## 工作原理

BR 是分布式备份恢复的工具，它将备份或恢复操作命令下发到各个 TiKV 节点。TiKV 收到命令后执行相应的备份或恢复操作。在一次备份或恢复中，各个 TiKV 节点都会有一个对应的备份路径，TiKV 备份时产生的备份文件将会保存在该路径下，恢复时也会从该路径读取相应的备份文件。

### 备份原理

BR 执行备份操作时，会先从 PD 获取到以下信息：

- 当前的 TS 作为备份快照的时间点
- 当前集群的 TiKV 节点信息

然后 BR 根据这些信息，在内部启动一个 TiDB 实例，获取对应 TS 的数据库或表信息，同时过滤掉系统库 (`information_schema`，`performance_schema`，`mysql`)。

此时根据备份子命令，会有两种备份逻辑：

- 全量备份：BR 遍历全部库表，并且根据每一张表构建需要备份的 KV Range
- 单表备份：BR 根据该表构建需要备份的 KV Range

最后，BR 将需要备份的 KV Range 收集后，构造完整的备份请求分发给集群内的 TiKV 节点。

该请求的主要结构如下：

```
BackupRequest{
    ClusterId,      // 集群 ID
    StartKey,       // 备份起始点，startKey 会被备份
    EndKey,         // 备份结束点，endKey 不会被备份
    EndVersion,     // 备份快照时间点
    StorageBackend, // 备份文件存储地址
    RateLimit,      // 备份速度 (MB/s)
    Concurrency,    // 执行备份操作的线程数（默认为 4）
}
```

TiKV 节点收到备份请求后，会遍历节点上所有的 Region Leader，找到和请求中 KV Range 有重叠范围的 Region，将该范围下的部分或者全部数据进行备份，在备份路径下生成对应的 SST 文件。

TiKV 节点在备份完对应 Region Leader 的数据后将元信息返回给 BR。BR 将这些元信息收集并存储进 `backupmeta` 文件中，等待恢复时使用。

如果执行命令时开启了 checksum，那么 BR 在最后会对备份的每一张表计算 checksum 用于校验。

#### 备份文件类型

备份路径下会生成以下两种类型文件：

- SST 文件：存储 TiKV 备份下来的数据信息
- `backupmeta` 文件：存储本次备份的元信息，包括备份文件数、备份文件的 Key 区间、备份文件大小和备份文件 Hash (sha256) 值

#### SST 文件命名格式

SST 文件以 `storeID_regionID_regionEpoch_keyHash_cf` 的格式命名。格式名的解释如下：

- storeID：TiKV 节点编号
- regionID：Region 编号
- regionEpoch：Region 版本号
- keyHash：Range startKey 的 Hash (sha256) 值，确保唯一性
- cf：RocksDB 的 ColumnFamily（默认为 `default` 或 `write`）

### 恢复原理

BR 执行恢复操作时，会按顺序执行以下任务：

1. 解析备份路径下的 backupMeta 文件，根据解析出来的库表信息，在内部启动一个 TiDB 实例在新集群创建对应的库表。

2. 把解析出来的 SST 文件，根据表进行聚合。

3. 根据 SST 文件的 Key Range 进行预切分 Region，使得每个 Region 至少对应一个 SST 文件。

4. 遍历要恢复的每一张表，以及这个表对应的 SST 文件。

5. 找到该文件对应的 Region，发送下载文件的请求到对应的 TiKV 节点，并在下载成功后，发送加载请求。

TiKV 收到加载 SST 文件的请求后，利用 Raft 机制保证加载 SST 数据的强一致性。在加载成功后，下载下来的 SST 文件会被异步删除。

在执行完恢复操作后，BR 会对恢复后的数据进行 checksum 计算，用于和备份下来的数据进行对比。

![br-arch](/media/br-arch.png)

## BR 命令行描述

一条 `br` 命令是由子命令、选项和参数组成的。子命令即不带 `-` 或者 `--` 的字符。选项即以 `-` 或者 `--` 开头的字符。参数即子命令或选项字符后紧跟的、并传递给命令和选项的字符。

以下是一条完整的 `br` 命令行：

`br backup full --pd "${PDIP}:2379" -s "local:///tmp/backup"`

命令行各部分的解释如下：

* `backup`：`br` 的子命令
* `full`：`backup` 的子命令
* `-s` 或 `--storage`：备份保存的路径
* `"local:///tmp/backup"`：`-s` 的参数，保存的路径为本地磁盘的 `/tmp/backup`
* `--pd`：PD 服务地址
* `"${PDIP}:2379"`：`--pd` 的参数

### 命令和子命令

BR 由多层命令组成。目前，BR 包含 `backup`、`restore` 和 `version` 三个子命令:

* `br backup` 用于备份 TiDB 集群
* `br restore` 用于恢复 TiDB 集群
* `br version` 用于查看 BR 工具版本信息

以上三个子命令可能还包含这些子命令：

* `full`：可用于备份或恢复全部数据。
* `db`：可用于备份或恢复集群中的指定数据库。
* `table`：可用于备份或恢复集群指定数据库中的单张表。

### 常用选项

* `--pd`：用于连接的选项，表示 PD 服务地址，例如 `"${PDIP}:2379"`。
* `-h`/`--help`：获取所有命令和子命令的使用帮助。例如 `br backup --help`。
* `--ca`：指定 PEM 格式的受信任 CA 的证书文件路径。
* `--cert`：指定 PEM 格式的 SSL 证书文件路径。
* `--key`：指定 PEM 格式的 SSL 证书密钥文件路径。
* `--status-addr`：BR 向 Prometheus 提供统计数据的监听地址。

## 备份集群数据

使用 `br backup` 命令来备份集群数据。可选择添加 `full` 或 `table` 子命令来指定备份的范围：全部集群数据或单张表的数据。

如果备份时间可能超过设定的 [`tikv_gc_life_time`](/v3.1/reference/garbage-collection/configuration.md#tikv_gc_life_time)（默认 `10m0s`），则需要将该参数调大。

例如，将 `tikv_gc_life_time` 调整为 `720h`：

{{< copyable "sql" >}}

```sql
mysql -h${TiDBIP} -P4000 -u${TIDB_USER} ${password_str} -Nse \
    "update mysql.tidb set variable_value='720h' where variable_name='tikv_gc_life_time'";
```

### 备份全部集群数据

要备份全部集群数据，可使用 `br backup full` 命令。该命令的使用帮助可以通过 `br backup full -h` 或 `br backup full --help` 来获取。

用例：将所有集群数据备份到各个 TiKV 节点的 `/tmp/backup` 路径，同时也会将备份的元信息文件 `backupmeta` 写到该路径下。

{{< copyable "shell-regular" >}}

```shell
br backup full \
    --pd "${PDIP}:2379" \
    --storage "local:///tmp/backup" \
    --ratelimit 120 \
    --concurrency 4 \
    --log-file backupfull.log
```

以上命令中，`--ratelimit` 和 `--concurrency` 选项限制了**每个 TiKV** 执行备份任务的速度上限（单位 MiB/s）和并发数上限。`--log-file` 选项指定把 BR 的 log 写到 `backupfull.log` 文件中。

备份期间有进度条在终端中显示。当进度条前进到 100% 时，说明备份已完成。在完成备份后，BR 为了确保数据安全性，还会校验备份数据。进度条效果如下：

```shell
br backup full \
    --pd "${PDIP}:2379" \
    --storage "local:///tmp/backup" \
    --ratelimit 120 \
    --concurrency 4 \
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
    --ratelimit 120 \
    --concurrency 4 \
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
    --ratelimit 120 \
    --concurrency 4 \
    --log-file backuptable.log
```

`table` 子命令有 `--db` 和 `--table` 两个选项，分别用来指定数据库名和表名。其他选项的含义与[备份全部集群数据](#备份全部集群数据)相同。

备份期间有进度条在终端中显示。当进度条前进到 100% 时，说明备份已完成。在完成备份后，BR 为了确保数据安全性，还会校验备份数据。

## 恢复集群数据

使用 `br restore` 命令来恢复备份数据。可选择添加 `full`、`db` 或 `table` 子命令来指定恢复操作的范围：全部集群数据、某个数据库或某张数据表。

> **注意：**
>
> 如果备份的集群没有网络存储，在恢复前需要将所有备份的 SST 文件拷贝到各个 TiKV 节点上 `--storage` 指定的目录下。

### 恢复全部备份数据

要将全部备份数据恢复到集群中来，可使用 `br restore full` 命令。该命令的使用帮助可以通过 `br restore full -h` 或 `br restore full --help` 来获取。

用例：将 `/tmp/backup` 路径中的全部备份数据恢复到集群中。

{{< copyable "shell-regular" >}}

```shell
br restore full \
    --pd "${PDIP}:2379" \
    --storage "local:///tmp/backup" \
    --concurrency 128 \
    --log-file restorefull.log
```

`--concurrency` 指定了该恢复任务内部的子任务的并发数。`--log-file` 选项指定把 BR 的 log 写到 `restorefull.log` 文件中。

恢复期间还有进度条会在终端中显示，当进度条前进到 100% 时，说明恢复已完成。在完成恢复后，BR 为了确保数据安全性，还会校验恢复数据。进度条效果如下：

```shell
br restore full \
    --pd "${PDIP}:2379" \
    --storage "local:///tmp/backup" \
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
    --storage "local:///tmp/backup" \
    --log-file restorefull.log
```

以上命令中 `--db` 选项指定了需要恢复的数据库名字。其余选项的含义与[恢复全部备份数据](#恢复全部备份数据)相同。

### 恢复单张表的数据

要将备份数据中的某张数据表恢复到集群中，可以使用 `br restore table` 命令。该命令的使用帮助可通过 `br restore table -h` 或 `br restore table --help` 来获取。

用例：将 `/tmp/backup` 路径下的备份数据中的某个数据表恢复到集群中。

{{< copyable "shell-regular" >}}

```shell
br restore table \
    --pd "${PDIP}:2379" \
    --db "test" \
    --table "usertable" \
    --storage "local:///tmp/backup" \
    --log-file restorefull.log
```

以上命令中 `--table` 选项指定了需要恢复的表名。其余选项的含义与[恢复某个数据库](#恢复某个数据库)相同。

## 最佳实践

- 推荐在 `-s` 指定的备份路径上挂载一个共享存储，例如 NFS。这样能方便收集和管理备份文件。
- 在使用共享存储时，推荐使用高吞吐的存储硬件，因为存储的吞吐会限制备份或恢复的速度。
- 推荐在业务低峰时执行备份操作，这样能最大程度地减少对业务的影响。

更多最佳实践内容，参见 [BR 最佳实践文档](/v3.1/how-to/maintain/backup-and-restore/br-best-practices.md)。

## 备份和恢复示例

本示例展示如何对已有的集群数据进行备份和恢复操作。可以根据机器性能、配置、数据规模来预估一下备份和恢复的性能。

### 数据规模和机器配置

假设对 TiKV 集群中的 10 张表进行备份和恢复。每张表有 500 万行数据，数据总量为 35 GB。

```sql
MySQL [sbtest]> show tables;
+------------------+
| Tables_in_sbtest |
+------------------+
| sbtest1          |
| sbtest10         |
| sbtest2          |
| sbtest3          |
| sbtest4          |
| sbtest5          |
| sbtest6          |
| sbtest7          |
| sbtest8          |
| sbtest9          |
+------------------+

MySQL [sbtest]> select count(*) from sbtest1;
+----------+
| count(*) |
+----------+
|  5000000 |
+----------+
1 row in set (1.04 sec)
```

表结构如下：

```sql
CREATE TABLE `sbtest1` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `k` int(11) NOT NULL DEFAULT '0',
  `c` char(120) NOT NULL DEFAULT '',
  `pad` char(60) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `k_1` (`k`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin AUTO_INCREMENT=5138499
```

示例假设有 4 个 TiKV 节点，每个节点配置如下：

| CPU | 内存 | 磁盘 | 副本数 |
| :--- | :--- | :--- | :--- |
| 16 核 | 32 GB | SSD | 3 |

### 备份示例

- 备份前需确认已将 GC 时间调长，确保备份期间不会因为数据丢失导致中断
- 备份前需确认 TiDB 集群没有执行 DDL 操作

执行以下命令对集群中的全部数据进行备份：

{{< copyable "shell-regular" >}}

```
bin/br backup full -s local:///tmp/backup --pd "${PDIP}:2379" --log-file backup.log
```

```
[INFO] [collector.go:165] ["Full backup summary: total backup ranges: 2, total success: 2, total failed: 0, total take(s): 0.00, total kv: 4, total size(Byte): 133, avg speed(Byte/s): 27293.78"] ["backup total regions"=2] ["backup checksum"=1.640969ms] ["backup fast checksum"=227.885µs]
```

### 恢复示例

恢复操作前，需确认待恢复的 TiKV 集群是全新的集群。

执行以下命令对全部数据进行恢复：

{{< copyable "shell-regular" >}}

```
bin/br restore full -s local:///tmp/backup --pd "${PDIP}:2379" --log-file restore.log
```

```
[INFO] [collector.go:165] ["Full Restore summary: total restore tables: 1, total success: 1, total failed: 0, total take(s): 0.26, total kv: 20000, total size(MB): 10.98, avg speed(MB/s): 41.95"] ["restore files"=3] ["restore ranges"=2] ["split region"=0.562369381s] ["restore checksum"=36.072769ms]
```
