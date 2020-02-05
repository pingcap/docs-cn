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

数据导出类
全量导出

Mydumper
概述：用于对 TiDB 进行全量逻辑备份。
输入/输出
输入：TiDB 集群
输出：SQL 文件
适用 TiDB 版本：all version
相关文档：https://pingcap.com/docs/stable/reference/tools/mydumper/
K8s 支持：https://pingcap.com/docs/stable/tidb-in-kubernetes/maintain/backup-and-restore/
Dumpling
概述：用于对 TiDB 进行全量逻辑备份。（可以理解为 golang 版本的 Mydumper）
输入/输出
输入：TiDB 集群
输出：SQL 文件
适用 TiDB 版本：all version
相关文档：暂无
是否支持 k8s：否
BR
概述：TiDB 分布式备份恢复的命令行工具，用于对 TiDB 集群进行数据备份和恢复。相比 Mydumper/Loader，BR 更适合大数据量的场景。
输入/输出
输入：TiDB 集群
输出：全量备份文件
适用 TiDB 版本：v3.1 及 v4.0
相关文档：https://pingcap.com/docs/v3.1/how-to/maintain/backup-and-restore/br/
K8s 支持：支持，文档撰写中
增量导出
TiDB-Binlog
概述：收集 TiDB 的 binlog，并提供准实时同步和备份的工具。
输入/输出：
输入：TiDB 集群
输出：MySQL、TiDB、Kafka 或者增量备份文件
适用 TiDB 版本：v2.1 及以上
相关文档：https://pingcap.com/docs/stable/reference/tidb-binlog/overview/
K8s 支持：
https://pingcap.com/docs/stable/tidb-in-kubernetes/maintain/tidb-binlog/
https://pingcap.com/docs/stable/tidb-in-kubernetes/reference/configuration/tidb-drainer/
CDC
概述：收集 TiKV 的 kv change log，还原事务后同步到下游的工具。可以理解为 TiDB-Binlog 的升级版本。（开发中）
输出/输出：
输入：TiDB 集群
输出：MySQL、TiDB、Kafka 或者增量备份文件
适用 TiDB 版本：v4.0
相关文档：暂无，文档撰写中
是否支持 k8s：暂无，正在规划中
	

工具版本适配和演进路线
版本适配
TiDB 2.1 and before：
MySQL 全量数据备份：使用 Mydumper
MySQL 全量数据导入 TiDB：
数据量 T 级别：使用 Lightning
数据量在 T 级别以下：使用 DM
MySQL 增量数据同步：使用 DM
TiDB 全量数据备份：使用 Mydumper
TiDB 全量数据恢复：
数据量 T 级别：使用 Lightning(>=TiDB 2.1)
数据量在 T 级别以下：使用 DM
TiDB 增量数据备份/恢复：使用 TiDB-Binlog

TiDB 3.0:
MySQL 全量数据备份：使用 Mydumper
MySQL 全量数据导入 TiDB：
数据量 T 级别：使用 Lightning
数据量在 T 级别以下：使用 DM
MySQL 增量数据同步：使用 DM
TiDB 全量数据备份：使用 Mydumper
TiDB 全量数据恢复：
数据量 T 级别：使用 Lightning
数据量在 T 级别以下：使用 DM
TiDB 增量数据备份/恢复：使用 TiDB-Binlog


TiDB 3.1:
MySQL 全量数据备份：使用 Mydumper
MySQL 全量数据导入 TiDB：
数据量 T 级别：使用 Lightning
数据量在 T 级别以下：使用 DM
MySQL 增量数据同步：使用 DM
TiDB 全量数据备份：使用 BR
TiDB 全量数据恢复：使用 BR
TiDB 增量数据备份/恢复：使用 TiDB-Binlog

TiDB 4.0
MySQL 全量数据备份：使用 Mydumper
MySQL 全量数据导入 TiDB：
数据量 T 级别：使用 Lightning
数据量在 T 级别以下：使用 DM
MySQL 增量数据同步：使用 DM
TiDB 全量数据备份：使用 BR
TiDB 全量数据恢复：使用 BR
TiDB 增量数据备份/恢复：使用 CDC
演进路线
TiDB 全量备份：
Mydumper -> BR，使用 TiDB 的特性进行备份和恢复，适合数据量比较大的场景，备份效率大大提升
，Mydumper -> dumpling，使用 golang 实现，方便维护，且易于集成到 DM 中
TiDB 全量恢复
：Loader -> Lightning -> BR：由 Lightning 统一提供全量数据恢复功能
Lightning -> BR：importer 逻辑和 BR 接近，把 importer 合并到 TiKV 中，TiKV 提供统一的数据导入接口
MySQL 数据迁移：
Mydumper，Loader，Syncer -> DM：，提供一体化的数据迁移方案，提高易用性
Loader -> Lightning：由 Lightning 统一提供全量数据恢复功能
TiDB 增量备份同步：
TiDB-Binlog -> CDC：
从 TiKV 层获取增量数据变更，解决 TiDB-Binlog 的 binlog 数据无高可用的问题
具有扩展性，支持扩展到任何 tikv 集群规模

数据迁移解决方案
目前 TiDB 主推以及使用最广泛的的版本是 3.0，另外今年会发布 TiDB 3.1 和 4.0，这里会针对这三个版本，给出典型业务场景下的数据迁移方案。
TiDB 3.0 全链路数据迁移方案

MySQL 数据迁移到 TiDB

MySQL 数据量在 T 级别以上：
使用 Mydumper 导出 MySQL 全量数据
使用 Lightning 将 MySQL 全量备份数据导入 TiDB 集群
使用 DM 同步 MySQL 增量数据到 TiDB
MySQL 数据量在 T 级别以下：
使用 DM 迁移 MySQL 数据到 TiDB，包括全量导入和增量的恢复

TiDB 集群数据的同步
使用 TiDB-Binlog 将 TiDB 数据同步到下游 TiDB/MySQL。

TiDB 集群数据的全量备份及恢复
使用 Mydumper 进行全量数据的备份
使用 Lightning 将全量数据恢复到 TiDB/MySQL。如果数据量在 T 级别以上，且恢复到新的 TiDB 集群，则可以使用 Lightning。


TiDB 3.1 全链路数据迁移方案
MySQL 数据迁移到 TiDB

MySQL 数据量在 T 级别以上：
使用 Mydumper 导出 MySQL 全量数据
使用 Lightning 将 MySQL 全量备份数据导入 TiDB 集群
使用 DM 同步 MySQL 增量数据到 TiDB
MySQL 数据量在 T 级别以下：
使用 DM 迁移 MySQL 数据到 TiDB，包括全量导入和增量的恢复

TiDB 集群数据的同步
使用 TiDB-Binlog 将 TiDB 数据同步到下游 TiDB/MySQL。

TiDB 集群数据的全量备份及恢复
恢复到 TiDB：
使用 BR 进行全量数据的备份
使用 BR 进行全量数据的恢复
恢复到 MySQL：
使用 Mydumper 进行全量数据的备份
使用 Lightning 进行全量数据的恢复


TiDB 4.0 全链路数据迁移方案
MySQL 数据迁移到 TiDB

MySQL 数据量在 T 级别以上：
使用 Mydumper 导出 MySQL 全量数据
使用 Lightning 将 MySQL 全量备份数据导入 TiDB 集群
使用 DM 同步 MySQL 增量数据到 TiDB
MySQL 数据量在 T 级别以下：
使用 DM 迁移 MySQL 数据到 TiDB，包括全量导入和增量的恢复

TiDB 集群数据的同步
使用 CDC 将 TiDB 数据同步到下游 TiDB/MySQL。

TiDB 集群数据的全量备份及恢复
恢复到 TiDB：
使用 BR 进行全量数据的备份
使用 BR 进行全量数据的恢复
恢复到 MySQL：
使用 Mydumper 进行全量数据的备份
使用 Lightning 进行全量数据的恢复
