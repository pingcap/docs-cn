---
title: 数据迁移工具概览
summary: 介绍 TiDB 的数据迁移工具。
---

# 数据迁移工具概览

TiDB 提供了丰富的数据迁移相关的工具，用于全量迁移、增量迁移、备份恢复、数据同步等多种场景。

本文介绍了使用这些工具的场景、优势和相关限制等信息。请根据你的需求选择合适的工具。

下图显示了各迁移工具的使用场景。

![TiDB Migration Tools](/media/migration-tools.png)

下表介绍了迁移工具的使用场景、支持的上下游等信息。

| 名称 | 使用场景 | 上游（或输入源文件） | 下游（或输出文件） |主要优势 | 使用限制 |
|:---|:---|:---|:---|:---|:---|
|  [TiDB DM](/dm/dm-overview.md)|用于将数据从与 MySQL 协议兼容的数据库迁移到 TiDB。  |  MySQL，MariaDB，Aurora，MySQL| TiDB   | 一体化的数据迁移任务管理工具，支持全量迁移和增量同步；支持对表与操作进行过滤；支持分库分表的合并迁移。 |  建议用于 1TB 以内的存量数据迁移。|
| [Dumpling](/dumpling-overview.md) | 用于将数据从 MySQL/TiDB 进行全量导出。| MySQL，TiDB| SQL，CSV  | 支持全新的 table-filter，筛选数据更加方便；支持导出到 Amazon S3 云盘|如果导出后计划往非 TiDB 的数据库恢复，建议使用 Dumpling；如果是往另一个 TiDB 恢复，建议使用 BR。 |
| [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)| 用于将数据全量导入到 TiDB。|Dumpling 输出的文件；CSV 文件；从本地盘或 Amazon S3 云盘读取数据。 | TiDB | 支持迅速导入大量新数据，实现快速初始化 TiDB 集群的指定表；支持断点续传；支持数据过滤。| 如果使用 Local-backend 进行数据导入，TiDB Lightning 运行后，TiDB 集群将无法正常对外提供服务。如果你不希望 TiDB 集群的对外服务受到影响，可以参考 TiDB Lightning TiDB-backend 中的硬件需求与部署方式进行数据导入。|
|[Backup & Restore (BR)](/br/backup-and-restore-tool.md) |用于对大数据量的 TiDB 集群进行数据备份和恢复。 | TiDB| SST；backup.meta 文件；backup.lock 文件|适用于向另一个 TiDB 恢复数据。支持数据冷备份到外部存储，可以用于灾备恢复。 | BR 恢复到 TiCDC / Drainer 的上游集群时，恢复数据无法由 TiCDC / Drainer 同步到下游。BR 只支持在 new_collations_enabled_on_first_bootstrap 开关值相同的集群之间进行操作。|
| [TiCDC](/ticdc/ticdc-overview.md)| 通过拉取 TiKV 变更日志实现的 TiDB 增量数据同步工具，具有将数据还原到与上游任意 TSO 一致状态的能力，支持其他系统订阅数据变更。|TiDB | TiDB，MySQL，Apache Pulsar，Kafka，Confluent|提供开放数据协议 (TiCDC Open Protocol)。 | TiCDC 只能同步至少存在一个有效索引的表。暂不支持以下场景：暂不支持单独使用 RawKV 的 TiKV 集群。暂不支持在 TiDB 中创建 SEQUENCE 的 DDL 操作和 SEQUENCE 函数。|
|[TiDB Binlog](/tidb-binlog/tidb-binlog-overview.md) | 用于 TiDB 集群间的增量数据同步，如将其中一个 TiDB 集群作为另一个 TiDB 集群的从集群。| TiDB | TiDB，MySQL，Kafka，增量备份文件|支持实时备份和恢复。备份 TiDB 集群数据，同时可以用于 TiDB 集群故障时恢复。 |与部分 TiDB 版本不兼容，不能一起使用。|
|[sync-diff-inspector](/sync-diff-inspector/sync-diff-inspector-overview.md) | 用于校验 MySQL/TiDB 中两份数据的一致性。|TiDB，MySQL | TiDB，MySQL| 提供了修复数据的功能，适用于修复少量不一致的数据。|对于 MySQL 和 TiDB 之间的数据同步不支持在线校验。不支持 JSON、BIT、BINARY、BLOB 等类型的数据。 |

## 使用 TiUP 快速安装

从 TiDB 4.0 开始，TiUP 作为软件包管理器，帮助你轻松管理 TiDB 生态系统中的不同集群组件。现在你可以只用一个 TiUP 命令行来管理任何组件。

### 第 1 步： 安装 TiUP

{{< copyable "shell-regular" >}}

```shell
curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
```

重新声明全局环境变量

{{< copyable "shell-regular" >}}

```shell
source ~/.bash_profile
```

### 第 2 步： 安装组件

你可以通过以下命令查看所有可用组件:

{{< copyable "shell-regular" >}}

```shell
tiup list
```

以下输出为所有可用组件：

```bash
Available components:
Name            Owner    Description
----            -----    -----------
bench           pingcap  Benchmark database with different workloads
br              pingcap  TiDB/TiKV cluster backup restore tool
cdc             pingcap  CDC is a change data capture tool for TiDB
client          pingcap  Client to connect playground
cluster         pingcap  Deploy a TiDB cluster for production
ctl             pingcap  TiDB controller suite
dm              pingcap  Data Migration Platform manager
dmctl           pingcap  dmctl component of Data Migration Platform
errdoc          pingcap  Document about TiDB errors
pd-recover      pingcap  PD Recover is a disaster recovery tool of PD, used to recover the PD cluster which cannot start or provide services normally
playground      pingcap  Bootstrap a local TiDB cluster for fun
tidb            pingcap  TiDB is an open source distributed HTAP database compatible with the MySQL protocol
tidb-lightning  pingcap  TiDB Lightning is a tool used for fast full import of large amounts of data into a TiDB cluster
tiup            pingcap  TiUP is a command-line component management tool that can help to download and install TiDB platform components to the local system
```

选择所需要的组件进行安装

{{< copyable "shell-regular" >}}

```shell
tiup install dumpling tidb-lightning
```

> **Note:**
>
> 如果需要安装特定版本，可以使用 `tiup install <component>[:version]` 命令.

### 第 3 步： 更新 TiUP 及组件 (可选)

建议先查看新版本的更新日志及兼容性说明

{{< copyable "shell-regular" >}}

```shell
tiup update --self && tiup update dm
```

## 探索更多

- [离线方式安装 TiUP](/production-deployment-using-tiup.md)
- [以二进制包形式安装各工具](/download-ecosystem-tools.md)