---
title: TiDB-Binlog Cluster简介
category: tools
aliases: ['/docs-cn/tools/tidb-binlog-cluster/']
---

# TiDB-Binlog Cluster 简介

本文档介绍 cluster 版本 TiDB-Binlog 的架构以及部署方案。

TiDB-Binlog 是一个用于收集 TiDB 的 Binlog，并提供实时备份和同步功能的商业工具。

TiDB-Binlog 支持以下功能场景：

* **数据同步**：同步 TiDB 集群数据到其他数据库
* **实时备份和恢复**：备份 TiDB 集群数据，同时可以用于 TiDB 集群故障时恢复

##TiDB-Binlog 的整体架构：

![TiDB-Binlog 架构](/media/tidb_binlog_cluster_architecture.png)

TiDB-Binlog 集群主要分为 Pump 和 Drainer 两个组件，以及 binlogctl 工具：

### Pump

Pump 用于实时记录 TiDB 产生的 Binlog，并将 Binlog 按照事务的提交时间进行排序，再提供给 Drainer 进行消费。

### Drainer

Drainer 从各个 Pump 中收集 Binlog 进行归并，再将 Binlog 转化成 SQL 或者指定格式的数据，最终同步到下游。

### binlogctl 工具

[binlogctl](https://github.com/pingcap/tidb-tools/tree/master/tidb-binlog/binlogctl) 是一个 TiDB-Binlog 配套的运维工具，具有如下功能：

* 获取 TiDB 集群当前的 TSO
* 查看 Pump/Drainer 状态
* 修改 Pump/Drainer 状态
* 暂停/下线 Pump/Drainer


## 主要特性

* 多个 Pump 形成一个集群，可以水平扩容；
* TiDB 通过内置的 Pump Client 将 Binlog 分发到各个 Pump；
* Pump 负责存储 Binlog，并将 Binlog 按顺序提供给 Drainer；
* Drainer 负责读取各个 Pump 的 Binlog，归并排序后发送到下游。

## 服务器要求

Pump 和 Drainer 都支持部署和运行在 Intel x86-64 架构的 64 位通用硬件服务器平台上。对于开发，测试以及生产环境的服务器硬件配置有以下要求和建议：

| 服务     | 部署数量       | CPU   | 磁盘          | 内存   |
| -------- | -------- | --------| --------------- | ------ |
| Pump | 3 | 8核+   | SSD, 200 GB+ | 16G |
| Drainer | 1 | 8核+ | SAS, 100 GB+ （如果输出为本地文件，则使用 SSD，并增加磁盘大小） | 16G |

## 注意

* 需要使用 TiDB v2.0.8-binlog、v2.1.0-rc.5 及以上版本，否则不兼容该版本的 TiDB-Binlog。
* 在运行 TiDB 时，需要保证至少一个 Pump 正常运行。
* 通过给 TiDB 增加启动参数 `enable-binlog` 来开启 binlog 服务。尽量保证同一集群的所有 TiDB 都开启了 binlog 服务，否则在同步数据时可能会导致上下游数据不一致。如果要临时运行一个不开启 binlog 服务的 TiDB 实例，需要在 TiDB 的配置文件中设置 `run_ddl= false`。
* Drainer 不支持对 ignore schemas（在过滤列表中的 schemas）的 table 进行 rename DDL 操作。
* 在已有的 TiDB 集群中启动 Drainer，一般需要全量备份并且获取 savepoint，然后导入全量备份，最后启动 Drainer 从 savepoint 开始同步增量数据。
* Drainer 支持将 Binlog 同步到 MySQL、TiDB、Kafka 或者本地文件。如果需要将 Binlog 同步到其他 Drainer 不支持的类型的系统中，可以设置 Drainer 将 Binlog 同步到 Kafka，然后根据 binlog slave protocol 进行定制处理，参考 [binlog slave client 用户文档](../binlog/binlog-slave-client.md)。
* 如果 TiDB-Binlog 用于增量恢复，可以设置配置项 `db-type="file"`，Drainer 会将 binlog 转化为指定的 [proto buffer 格式](https://github.com/pingcap/tidb-binlog/blob/master/proto/binlog.proto)的数据，再写入到本地文件中。这样就可以使用 [Reparo](../../tools/reparo.md) 恢复增量数据。
* Pump/Drainer 的状态需要区分已暂停（paused）和下线（offline），Ctrl + C 或者 kill 进程，Pump 和 Drainer 的状态会变为 pausing，最终变为 paused。进入 paused 状态前 Pump 不需要将已保存的 Binlog 数据全部发送到 Drainer，进入 offline 状态前 pump 需要将已保存的 Binlog 数据全部发送到 Drainer；如果需要较长时间退出 Pump（或不再使用该 Pump），需要使用 binlogctl 工具来下线 Pump。Drainer 同理。
* 如果下游为 MySQL/TiDB，数据同步后可以使用 [sync-diff-inspector](../../tools/sync-diff-inspector.md) 进行数据校验。

