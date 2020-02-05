---
title: A guide for choosing TiDB Ecosystem Tools
category: reference
---

# A guide for choosing TiDB Ecosystem Tools

目前 TiDB Ecosystem Tools 较多，有些工具之间有功能重叠，也有些属于版本迭代关系。本文档将对各个工具进行介绍，说明各个工具之间的关系，并且说明各个版本、场景下应该使用哪些工具。

## Tools 概览

### 数据导入类

#### 全量导入

##### Loader (Deprecated)

- 概述：轻量级的全量数据导入工具，以 SQL 的形式进行导入。目前这个工具正在逐步被 Lightning 替换掉，参见[文档](https://pingcap.com/docs/stable/reference/tools/tidb-lightning/tidb-backend/#migrating-from-loader-to-tidb-lightning-tidb-back-end)。

- 输入： Mydumper 输出文件

- 输出：以 SQL 形式写入 TiDB

- 适用 TiDB 版本：all versions

- 相关文档：[Loader](https://pingcap.com/docs/stable/reference/tools/loader/)

- K8s 支持：[backup and restore](https://pingcap.com/docs/stable/tidb-in-kubernetes/maintain/backup-and-restore/)

##### TiDB-Lightning

- 概述：将全量数据快速导入到一个新的 TiDB 集群的工具。注意用 TiDB-Lightning 导入数据的时候，有两种模式，默认的是以 `tikv-importer` 为后端，这种模式下导入数据过程中集群无法提供正常的服务，用于导入大量的数据（TB 级别）。第二种模式是以 `TiDB` 为后端（相当于 Loader 的功能），导入速度较慢，但是可以在线导入。

- 输入

    - Mydumper 输出文件

    - CSV 格式文件

- 适用 TiDB 版本：v2.1 及以上

- 相关文档：[TiDB-Lightning](https://pingcap.com/docs/stable/reference/tools/tidb-lightning/overview/)

- K8s 支持：[TiDB-Lightning](https://pingcap.com/docs/stable/tidb-in-kubernetes/maintain/lightning/)

#### 备份和恢复

##### BR

- 概述：TiDB 分布式备份恢复的命令行工具，用于对 TiDB 集群进行数据备份和恢复。相比 Mydumper/Loader，BR 更适合大数据量的场景。

- 备份输出和恢复输入：SST  + backupmeta 文件

- 适用 TiDB 版本：v3.1 及 v4.0

- 相关文档：[br](https://pingcap.com/docs/v3.1/how-to/maintain/backup-and-restore/br/)

- K8s 支持：已支持，文档撰写中

#### 增量导入

##### Syncer (Deprecated)

- 概述：将 MySQL/MariaDB 增量 binlog 数据实时复制导入到 TiDB 的工具。目前推荐使用 DM 替换该工具。

- 输入：MySQL/MariaDB 的 binlog

- 输出：以 SQL 形式写入 TiDB

- 适用 TiDB 版本：all version

- 相关文档：[Syncer](https://pingcap.com/docs/stable/reference/tools/syncer/)

- K8s 支持：不支持

##### DM

- 概述：将 MySQL/MariaDB 数据迁移到 TiDB 的工具，支持全量数据和增量数据的同步。

- 输入：MySQL/MariaDB 的全量数据以及 binlog

- 输出：以 SQL 形式写入 TiDB

- 适用 TiDB 版本：all version

- 相关文档： [Data Migration](https://pingcap.com/docs/stable/reference/tools/data-migration/overview/)

- k8s 支持：开发中

### 数据导出类

#### 全量导出

##### Mydumper

- 概述：用于对 MySQL/TiDB 进行全量逻辑备份。

- 输入：MySQL/TiDB 集群

- 输出：SQL 文件

- 适用 TiDB 版本：all version

- 相关文档：[Mydumper](https://pingcap.com/docs/stable/reference/tools/mydumper/)

- K8s 支持：[backup and restore](https://pingcap.com/docs/stable/tidb-in-kubernetes/maintain/backup-and-restore/)

#### 增量导出

##### TiDB-Binlog

- 概述：收集 TiDB 的 binlog，并提供准实时同步和备份的工具。

- 输入：TiDB 集群

- 输出：MySQL、TiDB、Kafka 或者增量备份文件

- 适用 TiDB 版本：v2.1 及以上

- 相关文档：[TiDB-Binlog](https://pingcap.com/docs/stable/reference/tidb-binlog/overview/)

- K8s 支持：[TiDB-Binlog](https://pingcap.com/docs/stable/tidb-in-kubernetes/maintain/tidb-binlog/)，[Drainer](
https://pingcap.com/docs/stable/tidb-in-kubernetes/reference/configuration/tidb-drainer/)

## 工具演进路线

### TiDB 备份与恢复

- Mydumper，Loader -> BR：Mydumper 和 Loader 都是在逻辑层面进行备份和恢复，备份效率低；BR 使用 TiDB 的特性进行备份和恢复，适合数据量比较大的场景，备份效率大大提升。

### TiDB 全量恢复

- Loader -> TiDB-Lightning：Loader 使用 SQL 的方式进行全量数据恢复，效率较低。TiDB-Lightning 将数据直接导入 TiKV，大大提升了全量数据恢复的效率，适合将大量数据（T 级别以上数据）快速导入到一个全新的 TiDB 集群中；且 TiDB-Lightning 集成了 Loader 的逻辑导入数据功能，参见[文档](https://pingcap.com/docs/stable/reference/tools/tidb-lightning/tidb-backend/#migrating-from-loader-to-tidb-lightning-tidb-back-end) ，支持在线导入数据。

### MySQL 数据迁移

- Mydumper，Loader，Syncer -> DM：使用 Mydumper、Loader、Syncer 将 MySQL 数据迁移到 TiDB，迁移过程比较繁琐。DM 提供了一体化的数据迁移方案，提高了易用性，而且 DM 还支持分库分表的合并。

- Loader -> TiDB-Lightning：TiDB-Lightning 集成了 Loader 的逻辑导入数据功能，参见[文档](https://pingcap.com/docs/stable/reference/tools/tidb-lightning/tidb-backend/#migrating-from-loader-to-tidb-lightning-tidb-back-end) ，由 Lightning 统一提供全量数据恢复功能。

## 数据迁移解决方案

针对 TiDB 的 2.1，3.0 以及 3.1 版本，下面给出典型业务场景下的数据迁移方案。

### TiDB 2.1 全链路数据迁移方案

#### MySQL 数据迁移到 TiDB

- MySQL 数据量在 T 级别以上

    - 使用 Mydumper 导出 MySQL 全量数据

    - 使用 TiDB-Lightning 将 MySQL 全量备份数据导入 TiDB 集群

    - 使用 DM 同步 MySQL 增量数据到 TiDB

- MySQL 数据量在 T 级别以下

    - 使用 DM 迁移 MySQL 数据到 TiDB，包括全量导入和增量的恢复

#### TiDB 集群数据的同步

- 使用 TiDB-Binlog 将 TiDB 数据同步到下游 TiDB/MySQL

#### TiDB 集群数据的全量备份及恢复

- 使用 Mydumper 进行全量数据的备份

- 使用 TiDB-Lightning 将全量数据恢复到 TiDB/MySQL

### TiDB 3.0 全链路数据迁移方案

#### MySQL 数据迁移到 TiDB

- MySQL 数据量在 T 级别以上

    - 使用 Mydumper 导出 MySQL 全量数据

    - 使用 TiDB-Lightning 将 MySQL 全量备份数据导入 TiDB 集群

    - 使用 DM 同步 MySQL 增量数据到 TiDB

- MySQL 数据量在 T 级别以下

    - 使用 DM 迁移 MySQL 数据到 TiDB，包括全量导入和增量的恢复

#### TiDB 集群数据的同步

- 使用 TiDB-Binlog 将 TiDB 数据同步到下游 TiDB/MySQL

#### TiDB 集群数据的全量备份及恢复

- 使用 Mydumper 进行全量数据的备份

- 使用 TiDB-Lightning 将全量数据恢复到 TiDB/MySQL

### TiDB 3.1 全链路数据迁移方案

#### MySQL 数据迁移到 TiDB

- MySQL 数据量在 T 级别以上

    - 使用 Mydumper 导出 MySQL 全量数据

    - 使用 TiDB-Lightning 将 MySQL 全量备份数据导入 TiDB 集群

    - 使用 DM 同步 MySQL 增量数据到 TiDB

- MySQL 数据量在 T 级别以下

    - 使用 DM 迁移 MySQL 数据到 TiDB，包括全量导入和增量的恢复

#### TiDB 集群数据的同步

- 使用 TiDB-Binlog 将 TiDB 数据同步到下游 TiDB/MySQL

#### TiDB 集群数据的全量备份及恢复

- 恢复到 TiDB

    - 使用 BR 进行全量数据的备份

    - 使用 BR 进行全量数据的恢复

- 恢复到 MySQL

    - 使用 Mydumper 进行全量数据的备份

    - 使用 TiDB-Lightning 进行全量数据的恢复
