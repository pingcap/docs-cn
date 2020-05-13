---
title: TiDB Binlog 简介
category: reference
aliases: ['/docs-cn/dev/reference/tidb-binlog-overview/','/docs-cn/dev/reference/tools/tidb-binlog/overview/']
---

# TiDB Binlog 简介

TiDB Binlog 是一个用于收集 TiDB 的 binlog，并提供准实时备份和同步功能的商业工具。

TiDB Binlog 支持以下功能场景：

- **数据同步**：同步 TiDB 集群数据到其他数据库
- **实时备份和恢复**：备份 TiDB 集群数据，同时可以用于 TiDB 集群故障时恢复

## TiDB Binlog 整体架构

![TiDB Binlog 架构](/media/tidb_binlog_cluster_architecture.png)

TiDB Binlog 集群主要分为 Pump 和 Drainer 两个组件，以及 binlogctl 工具：

### Pump

[Pump](https://github.com/pingcap/tidb-binlog/blob/master/pump) 用于实时记录 TiDB 产生的 Binlog，并将 Binlog 按照事务的提交时间进行排序，再提供给 Drainer 进行消费。

### Drainer

[Drainer](https://github.com/pingcap/tidb-binlog/tree/master/drainer) 从各个 Pump 中收集 Binlog 进行归并，再将 Binlog 转化成 SQL 或者指定格式的数据，最终同步到下游。

### binlogctl 工具

[`binlogctl`](https://github.com/pingcap/tidb-binlog/tree/master/binlogctl) 是一个 TiDB Binlog 配套的运维工具，具有如下功能：

* 获取 TiDB 集群当前的 TSO
* 查看 Pump/Drainer 状态
* 修改 Pump/Drainer 状态
* 暂停/下线 Pump/Drainer

## 主要特性

* 多个 Pump 形成一个集群，可以水平扩容。
* TiDB 通过内置的 Pump Client 将 Binlog 分发到各个 Pump。
* Pump 负责存储 Binlog，并将 Binlog 按顺序提供给 Drainer。
* Drainer 负责读取各个 Pump 的 Binlog，归并排序后发送到下游。
* Drainer 支持 [relay log](/reference/tidb-binlog/relay-log.md) 功能，通过 relay log 保证下游集群的一致性状态。

## 注意事项

* 需要使用 TiDB v2.0.8-binlog、v2.1.0-rc.5 及以上版本，否则不兼容该版本的 TiDB Binlog。

* Drainer 支持将 Binlog 同步到 MySQL、TiDB、Kafka 或者本地文件。如果需要将 Binlog 同步到其他 Drainer 不支持的类型的系统中，可以设置 Drainer 将 Binlog 同步到 Kafka，然后根据 binlog slave protocol 进行定制处理，参考 [binlog slave client 用户文档](/reference/tidb-binlog/binlog-slave-client.md)。

* 如果 TiDB Binlog 用于增量恢复，可以设置配置项 `db-type="file"`，Drainer 会将 binlog 转化为指定的 [proto buffer 格式](https://github.com/pingcap/tidb-binlog/blob/master/proto/binlog.proto)的数据，再写入到本地文件中。这样就可以使用 [Reparo](/reference/tidb-binlog/reparo.md) 恢复增量数据。

    关于 `db-type` 的取值，应注意：

    - 如果 TiDB 版本 < 2.1.9，则 `db-type="pb"`。
    - 如果 TiDB 版本 > = 2.1.9，则 `db-type="file"` 或 `db-type="pb"`。

* 如果下游为 MySQL/TiDB，数据同步后可以使用 [sync-diff-inspector](/reference/tools/sync-diff-inspector/overview.md) 进行数据校验。
