---
title: 分库分表合并导入到 TiDB（大于 1 TiB）
summary: 使用 Dumpling 和 TiDB Lightning 合并导入分表数据到 TiDB。本文介绍的方法适用于导入数据总量大于 1 TiB 的场景。
---

# 分库分表合并导入到 TiDB（大于 1 TiB）

如果分表数据总规模特别大（例如大于 1 TiB），并且允许 TiDB 集群在迁移期间无其他业务写入，那么你可以使用 TiDB Lightning 对分表数据进行快速合并导入，然后根据业务需要选择是否使用 TiDB DM 进行增量数据的分表同步。本文档举例介绍了导入数据的操作步骤。

如果分库分表合并迁移在 1 TiB 以内，请参考[使用 DM 进行分表合并迁移](https://docs.pingcap.com/zh/tidb-data-migration/stable/usage-scenario-shard-merge)，支持全量和增量更为简单。

使用 TiDB Lightning 快速合并导入的原理如下图所示。

![使用 Dumpling 和 TiDB Lightning 合并导入分表数据](/media/shard-merge-using-lightning.png)

在这个示例中，假设有两个数据库 my_db1 和 my_db2 ，使用 Dumpling 分别从 my_db1 中导出 table1 和 table2 两个表，从 my_db2 中导出 table3 和 table4 两个表，然后再用 TiDB Lighting 把导出的 4 个表合并导入到下游 TiDB 中的同一个库 my_db 的同一个表格 table5 中。虽然 Dumpling 可以导出 MySQL 实例中的所有数据库，本文仅导出部分数据作为示例。

关于 Dumpling 和 TiDB Lightning 的更多介绍，请参考：

* [Dumpling](/dumpling-overview.md)
* [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)

**说明**：目前无法精确计算 Dumpling 从 MySQL 导出的数据大小，但你可以用下面 SQL 语句统计信息表的 data_length 字段估算数据量：

{{< copyable "sql" >}}

```sql
select table_schema,sum(data_length)/1024/1024 as data_length,sum(index_length)/1024/1024 as index_length,sum(data_length+index_length)/1024/1024 as sum from information_schema.tables group by table_schema;
```

## 前提条件

### TiDB Lightning 的资源要求

**操作系统**：本文档示例使用的是若干新的、纯净版 CentOS 7 实例，你可以在本地虚拟化或在供应商提供的平台上部署一台小型的云虚拟主机。TiDB Lightning 运行过程默认会占满 CPU，建议单独部署。如果条件不允许，可以和其他组件（比如 `tikv-server`）部署在同一台机器上，然后通过配置 `region-concurrency` 限制 TiDB Lightning 使用 CPU 资源。混合部署的情况下可以将其大小配置为逻辑 CPU 数的 75%，以限制 CPU 的使用。

**内存和 CPU**：因为 TiDB Lightning 对计算机资源消耗较高，是资源密集型工具，建议分配 64 GB 以上的内存以及 32 核以上的 CPU，而且确保 CPU 核数和内存（GB）比为 1:2 以上，以获取最佳性能。

**磁盘空间**：足够储存整个数据源的 SSD 硬盘，读取速度越快越好。

### 目标 TiKV 集群的磁盘空间要求

**磁盘空间**：目标 TiKV 集群必须有足够空间接收新导入的数据。除了[标准硬件配置](/hardware-and-software-requirements.md)以外，目标 TiKV 集群的总存储空间必须大于 **数据源大小 × [副本数量](/faq/deploy-and-maintain-faq.md#每个-region-的-replica-数量可配置吗调整的方法是) × 2**。例如集群默认使用 3 副本，那么总存储空间需为数据源大小的 6 倍以上。公式中的 2 倍可能难以理解，其依据是以下因素的估算空间占用：

* 索引会占据额外的空间
* RocksDB 的空间放大效应

### 上游 MySQL 权限

使用 Dumpling 从 MySQL 导出数据，需要下列权限：

* SELECT
* RELOAD
* LOCK TABLES
* REPLICATION CLIENT
* PROCESS

### 下游 TiDB 权限

本文档示例中使用的后端模式为 Local-backend，所以 TiDB Lightning 需要下游 TiDB 下列权限：

* SELECT
* UPDATE
* ALTER
* CREATE
* DROP

一般情况下，推荐使用配置项 `checksum = true`，所以 TiDB Lightning 还需要有下游 TiDB admin 用户权限。

更多相关权限的说明，请参考[TiDB Lightning 对下游数据库的账号权限要求是怎样的？](/tidb-lightning/tidb-lightning-faq.md#TiDB Lightning 对下游数据库的账号权限要求是怎样的？)

<!--
### 部署 Dumpling 和 TiDB Lightning

* [使用 TiUP 部署 TiDB Lighting](https://github.com/pingcap/docs/pull/6144/files#diff-53a937b1281c0fcb1ca972172e4c1b31a97af54bc5414e3186a648ea9eef6e23)
* [使用 TiUP 部署 Dumping](https://github.com/pingcap/docs/pull/6144/files#diff-53a937b1281c0fcb1ca972172e4c1b31a97af54bc5414e3186a648ea9eef6e23)
-->

## 数据导入流程

导入流程如下：

1. 用 Dumpling 导出全量数据备份。在本文档示例中，分别从 2 个源数据库中各导出 2 个表：
    - 从 my_db1 导出 table1、table2
    - 从 my_db2 导出 table3、table4
2. 启动 TiDB Lightning 执行导入操作
3. 导入成功
4. （可选）使用 TiDB DM 进行增量数据迁移

下面详细介绍每一步的操作流程。

### 第 1 步：用 Dumpling 导出全量数据备份

如果需要导出的多个分表属于同一个上游 MySQL 实例，可以直接使用 Dumpling 的 `-f` 参数一次导出多个分表的结果。如果多个分表分布在不同的 MySQL 实例，可以使用 Dumpling 分两次导出，并将两次导出的结果放置在相同的父目录下即可。下面的例子中同时用到了上述两种方式，然后将导出的数据存放在同一父目录下。

首先使用 Dumpling 从 my_db1 中导出表 table1 和 table2，如下：

```
tiup dumpling -h <ip> -P <port> -u root -t 16 -r 200000 -F 256MB -B my_db1 -f 'my_db1.table[12]' -o /data/my_database/
```

以上命令中，各参数解释如下：

- `-h`、`-P`、`-u` 分别代表地址、端口、用户。如果需要密码验证，可以使用 `-p $YOUR_SECRET_PASSWORD` 将密码传给 Dumpling。
- `-o` 用于选择存储导出文件的目录，支持本地文件路径或[外部存储 URL](/br/backup-and-restore-storages.md) 格式。
- `-t` 用于指定导出的线程数。增加线程数会增加 Dumpling 并发度提高导出速度，但也会加大数据库内存消耗，因此不宜设置过大。
- `-r` 用于指定单个文件的最大行数，指定该参数后 Dumpling 会开启表内并发加速导出，同时减少内存使用。
- `-F` 选项用于指定单个文件的最大大小（单位为 `MiB`，可接受类似 `5GiB` 或 `8KB` 的输入）。如果你想使用 TiDB Lightning 将该文件加载到 TiDB 实例中，建议将 `-F` 选项的值保持在 256 MiB 或以下。

> **注意：**
>
> 如果导出的单表大小超过 10 GiB，**强烈建议**使用`-r` 和 `-F` 参数。

然后使用 Dumpling 从 my_db2 中导出表 table3 和 table4，如下：

{{< copyable "shell-regular" >}}

```shell
tiup dumpling -h <ip> -P <port> -u root -t 16 -r 200000 -F 256MB -B my_db2 -f 'my_db2.table[34]' -o /data/my_database/
```

这样所需的全量备份数据就全部导出到了 `/data/my_database` 目录中。将所有源数据表格存储在一个目录中，是为了后续方便用 TiDB Lightning 导入。

### 第 2 步：启动 TiDB Lightning 进行导入

在启动 TiDB Lightning 进行导入之前，建议先了解如何选择后端模式、选择断点续传的处理方式，然后根据你的实际情况选择合适的方式进行。

#### 后端模式

在启动 TiDB Lightning 的时候请选择合适的后端模式。

* 如果导入的目标集群为 v4.0 或更新版本，请优先考虑使用 Local-backend 模式。Local-backend 部署更简单并且性能高于其他模式。
* 如果目标集群为 v3.x 或更旧版本，则建议使用 Importer-backend 模式。
* 如果需要导入的集群为生产环境线上集群，或需要导入的表中已包含有数据，则可以使用 TiDB-backend 模式。但由于该模式导入速度较慢，不适合本文介绍的大量数据迁移场景。

默认使用 Local-backend 模式。本文档的示例中采用了 Local-backend 模式。更多信息请参考 [TiDB Lightning 后端](/tidb-lightning/tidb-lightning-backends.md)。

下表展示了各后端模式的特点。

| 后端 | Local-backend | Importer-backend | TiDB-backend |
|:---|:---|:---|:---|
| 速度 | 快 (~500 GB/小时) | 快 (~400 GB/小时) | 慢 (~50 GB/小时) |
| 资源使用率 | 高 | 高 | 低 |
| 占用网络带宽 | 高 | 中  | 低 |
| 导入时是否满足 ACID | 否 | 否 | 是 |
| 目标表 | 必须为空 | 必须为空 | 可以不为空 |
| 额外组件 | 无 | `tikv-importer` | 无 |
| 支持 TiDB 集群版本 | >= v4.0.0 | 全部 | 全部 |
| 是否影响 TiDB 对外提供服务 | 是 | 是 | 否 |

#### 断点续传

大量数据导入一般耗时数小时甚至数天，长时间运行的进程会有一定机率发生非正常中断。如果每次重启都从头开始，之前已成功导入的数据就会前功尽弃。为此，TiDB Lightning 提供了断点续传的功能，即使 TiDB Lightning 崩溃，在重启时仍然从断点开始继续工作。

若 TiDB Lightning 因不可恢复的错误而退出，例如数据出错，在重启时不会使用断点，而是直接报错离开。为保证已导入的数据安全，必须先解决掉这些错误才能继续。你可以使用`tidb-lightning-ctl` 命令控制导入出错后的行为。该命令的选项有：

* --checkpoint-error-destroy：出现错误后，让失败的表从头开始整个导入过程。
* --checkpoint-error-ignore：如果导入表曾经出错，该命令会清除出错状态，如同错误没有发生过一样。
* --checkpoint-remove：无论是否有出错，把表的断点清除。

关于断点续传的更多信息，请参考 [TiDB Lightning 断点续传](/tidb-lightning/tidb-lightning-checkpoints.md)。

#### 执行导入操作

启动 tidb-lightning 的步骤如下：

1. 将数据源上传到部署了 TiDB Lightning 的服务器。
2. 参考下面例子配置 `tidb-lightning.toml`。

    ```toml
    [lightning]
    # 日志
    level = "info"
    file = "tidb-lightning.log"

    [tikv-importer]
    # 选择使用 local 后端
    backend = "local"
    # 设置排序的键值对的临时存放地址，目标路径需要是一个空目录
    sorted-kv-dir = "/mnt/ssd/sorted-kv-dir"
    # 设置分库分表合并规则，将 my_db1 中的 table1、table2 两个表,以及 my_db2 中的 table3、table4 两个表，共计 2 个数据库中的 4 个表都导入到目的数据库 my_db 中的 table5 表中。

    [[routes]]
    schema-pattern = "my_db1"
    table-pattern = "table[1-2]"
    target-schema = "my_db"
    target-table = "table5"

    [[routes]]
    schema-pattern = "my_db2"
    table-pattern = "table[3-4]"
    target-schema = "my_db"
    target-table = "table5"

    [mydumper]
    # 源数据目录。设置为 Dumpling 导出数据的路径，如果 Dumpling 执行了多次并分属不同的目录，请将多次导出的数据置放在相同的父目录下并指定此父目录即可。
    data-source-dir = "/data/my_database/"
    # 配置通配符规则，默认规则会过滤 mysql、sys、INFORMATION_SCHEMA、PERFORMANCE_SCHEMA、METRICS_SCHEMA、INSPECTION_SCHEMA 系统数据库下的所有表
    # 若不配置该项，导入系统表时会出现“找不到 schema”的异常
    filter = ['*.*', '!mysql.*', '!sys.*', '!INFORMATION_SCHEMA.*', '!PERFORMANCE_SCHEMA.*', '!METRICS_SCHEMA.*', '!INSPECTION_SCHEMA.*']

    [tidb]
    # 目标集群的信息，示例仅供参考。请把 IP 地址等信息替换成真实的信息。
    host = "172.16.31.2"
    port = 4000
    user = "root"
    password = "rootroot"
    # 表架构信息在从 TiDB 的“状态端口”获取。
    status-port = 10080
    # 集群 pd 的地址。示例仅供参考。请把 IP 地址等信息替换成真实的信息。
    pd-addr = "172.16.31.3:2379"
    ```

3. 配置合适的参数运行 `tidb-lightning`。如果直接在命令行中用 `nohup` 启动程序，可能会因为 SIGHUP 信号而退出，建议把 `nohup` 放到脚本里面，如：

  {{<copyable "shell-regular">}}

  ```shell
  tiup tidb-lightning -config tidb-lightning.toml > nohup.out &
  ```
   
导入开始后，可以采用以下任意方式查看进度：

- 通过 `grep` 日志关键字 `progress` 查看进度，默认 5 分钟更新一次。
- 通过监控面板查看进度，请参见 [TiDB Lightning 监控](/tidb-lightning/monitor-tidb-lightning.md)。

等待 TiDB Lightning 运行结束，则整个导入完成。

### 第 3 步：导入成功

导入完毕后，TiDB Lightning 会自动退出。查看日志的最后 5 行中会有 `the whole procedure completed`，则表示导入成功。

> **注意：**
>
> 无论导入成功与否，最后一行都会显示 `tidb lightning exit`。它只是表示 TiDB Lightning  正常退出，不代表任务完成。

如果导入过程中遇到问题，请参见 [TiDB Lightning 常见问题](/tidb-lightning/tidb-lightning-faq.md)。

### 第 4 步（可选）：增量数据的迁移

如果要将源数据库从指定位置开始的 Binlog 迁移到 TiDB，可以使用 TiDB DM 进行增量数据迁移。请参考 [Data Migration 增量数据迁移场景](https://docs.pingcap.com/zh/tidb-data-migration/stable/usage-scenario-incremental-migration)。