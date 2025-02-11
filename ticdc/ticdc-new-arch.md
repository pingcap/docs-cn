---
title: TiCDC 新架构介绍
summary: 介绍 TiCDC 新架构的主要特性，架构特点，升级部署指南以及其他注意事项。
---

# TiCDC 新架构介绍

## 概述

TiCDC 新架构通过重新设计核心组件和优化数据处理流程，显著提升了实时数据同步的性能、扩展性和稳定性，同时降低了资源成本。新架构的主要优势包括：
1. 更高的单节点性能：单节点最高支持 50 万张表的同步任务；宽表场景下最高同步流量可达 200MiB/s。
2. 更强的扩展能力：集群同步能力接近线性扩展，单集群预计可扩展至 100 个节点以上，支持超 1万个 Changefeed；单个 Changefeed 可支持百万级表的同步任务。
3. 更高的稳定性：在高流量、频繁 DDL 操作及集群扩缩容等场景下，Changefeed 延迟更小且更稳定；通过资源隔离和优先级调度，减少多 Changefeed 任务间的相互干扰。
4. 更低的资源成本：改进资源利用率，减少冗余开销，典型场景下 CPU、内存等资源利用效率提升最多一个数量级。

## 架构设计

![TiCDC New Architecture](/media/ticdc/ticdc-new-architecture-1.jpg)

TiCDC 新架构由两个主要部分组成，分别是 Log Service 和 Downstream Adapter，其中 Log Service 负责拉取上游集群的行变更和 DDL 信息并存储在本地，Downstream Adapter 则根据用户创建的 Changefeed 信息产生相关的同步任务从 Log Service 拉取相关数据并同步到下游。

### 核心组件

![TiCDC New Architecture](/media/ticdc/ticdc-new-architecture-2.jpg)

Log Service 作为 TiCDC 新架构的核心数据服务层，主要负责处理 Dispatcher 的注册请求，从上游集群拉取行变更和 DDL 信息存储到本地并推送给对应的 Dispatcher。Log Service 内部包括以下组件：
- Log Coordinator：在一个 TiCDC 集群中仅有一个实例，主要负责定时收集 Log Service 各节点的数据拉取和 GC 进度，并为 Dispatcher 提供数据访问路由服务：Dispatcher 在从 Log Service 请求数据时，会首先向 Log Coordinator 请求可用的 Event Service 节点列表，Log Coordinator 可以根据收集到的不同节点的统计信息返回可能可以复用数据的 Event Service 节点地址列表，Dispatcher 可以根据返回的列表决定请求的 Event Service 地址。
其余组件在每个 TiCDC 节点上都有一个实例，
- Log Puller：负责与上游集群建立连接，拉取相关数据并分发至 Event Store 和 Schema Store。
- Event Store：负责 DML 数据的排序、存储和管理。
- Schema Store：负责 DDL 数据的排序、存储和管理。
- Event Service：负责处理 Dispatcher 的注册请求，并从 Event Store 和 Schema Store 中拉取对应的数据排序后定期推送给 Dispatcher。

![TiCDC New Architecture](/media/ticdc/ticdc-new-architecture-3.jpg)

Downstream Adapter 作为 TiCDC 的下游数据同步适配层，负责处理用户发起的 Changefeed 运维操作，创建和管理相关同步任务，从 Log Service 拉取数据并同步到下游。Downstream Adapter 内部包括以下组件：
- Coordinator：TiCDC 新架构集群中的核心调度组件，一个 TiCDC 集群只会有一个 Coordinator 实例，负责统一管理所有 Changefeed 任务，其职责包括处理用户发起的 Changefeed 运维操作，协调调度各个 Changefeed 的 Maintainer，以及将 Changefeed 相关信息定期持久化到 Etcd。
- Maintainer：Changefeed 任务的核心调度组件，每个 Changefeed 任务对应一个 Maintainer 实例，其职责包括调度对应 Changefeed 的所有 Dispatcher 实例，协调 Changefeed 内部的 DDL 同步进度，以及计算对应 Changefeed 的各项同步延迟。
- Dispatcher：每个 Changefeed 任务会创建多个 Dispatcher 实例，每个 Dispatcher 实例负责单个表的同步任务，包括 DML 数据和 DDL 数据的同步。对于涉及多表的 DDL 操作，Maintainer 会协调相关表的 Dispatcher 实例，通过选举机制确定一个主 Dispatcher 来执行该 DDL 的同步。

## 使用指南

TiCDC 新架构仅支持 v7.5 或者以上版本的 TiDB 集群，使用之前需要确保 TiDB 集群版本满足要求。

### 使用 TiUP 部署启用新架构 TiCDC 的全新 TiDB 集群

在使用 TiUP 部署 v9.0 或者以上版本的全新 TiDB 集群时，支持同时部署启用新架构的 TiCDC 组件。你需要在 TiUP 启动 TiDB 集群时的配置文件中加入 TiCDC 组件相关的部分并启用新架构，以下是一个示例：

```shell
cdc_servers:
  - host: 10.0.1.20
    config:
      newarch: true
  - host: 10.0.1.21
    config:
      newarch: true
```

其他详细操作，请参考[使用 TiUP 部署包含 TiCDC 组件的全新 TiDB 集群](/ticdc/deploy-ticdc.md#使用-tiup-部署包含-ticdc-组件的全新-tidb-集群)

### 使用 TiUP 在原有 TiDB 集群全新部署启用新架构的 TiCDC 组件

1. 参考[扩容 TiCDC 节点](/scale-tidb-using-tiup.md#扩容-ticdc-节点)在集群中扩容新的 TiCDC 节点。

2. 参考下一节启用 TiCDC 新架构。

### 使用 TiUP 将原有 TiDB 集群中的 TiCDC 升级为新架构

如果 TiDB 集群为 v9.0 以下版本，需要手动下载 v9.0 或者以上版本的 TiCDC 二进制文件，并 Patch 到集群中。

> **注意：**
> 
> 升级至TiCDC新架构后，将不再支持回退至旧架构。


1. TiCDC 二进制文件下载链接格式为 `https://tiup-mirrors.pingcap.com/${component}-${version}-${os}-${arch}.tar.gz`，例如可以用以下命令下载 Linux 系统 x86-64 架构的 TiCDC v9.0.0 版本的二进制文件（更多信息参考[tiup cluster patch](/tiup/tiup-component-cluster-patch.md)）：

```shell
wget https://tiup-mirrors.pingcap.com/cdc-v9.0.0-linux-amd64.tar.gz
```

2. 将下载的 TiCDC 二进制文件 Patch 到集群中：

```shell
tiup cluster patch <cluster-name> ./cdc-v9.0.0-linux-amd64.tar.gz -R cdc
```

当 TiDB 集群中 TiCDC 组件版本已经升级到 v9.0 或者以上版本后，可以通过以下步骤启用 TiCDC 新架构。

1. 如果集群中已经有 Changefeed，需要参考[停止同步任务](/ticdc/ticdc-manage-changefeed.md#停止同步任务) 暂停所有的 Changefeed 同步任务；

2. 通过 TiUP 更新 TiCDC 配置：

```shell
tiup cluster edit-config <cluster-name>
```

```shell
server_configs:
  cdc:
    newarch: true
```

3. 参考[恢复同步任务](/ticdc/ticdc-manage-changefeed.md#恢复同步任务)恢复所有的 Changefeed 同步任务；

## 注意事项

1. TiCDC 老架构中，DDL 同步采用完全串行的方式，因此 DDL 的同步进度可以用 Changefeed 的 `CheckpointTs` 标识。但是在新架构中为了提高 DDL 同步效率，会尽可能并行同步不同表的 DDL，为了在下游为 MySQL 兼容数据库时准确记录各表的 DDL 同步进度，TiCDC 会在下游数据库中创建一张名为 `tidb_cdc.ddl_ts_v1` 的表，专门用于存储 Changefeed 的 DDL 同步进度信息。

2. 作为实验性特性，TiCDC v9.0 的新架构尚未完全实现旧架构中的所有功能，这些功能将在后续的 GA 版本中完整实现，具体包括：
    - [拆分 Update 事件](/ticdc/ticdc-split-update-behavior.md)
    - [灾难场景的最终一致性复制](/ticdc/ticdc-sink-to-mysql.md#灾难场景的最终一致性复制)
    - 拆分大事务
    - [TiCDC Avro Protocol](/ticdc/ticdc-avro-protocol.md)
    - [TiCDC CSV Protocol](/ticdc/ticdc-csv.md)
    - [TiCDC Debezium Protocol](/ticdc/ticdc-debezium.md)
    - [TiCDC Simple Protocol](/ticdc/ticdc-simple-protocol.md)
    - [Event Filter 事件过滤器](/ticdc/ticdc-filter.md#event-filter-事件过滤器-从-v620-版本开始引入)
    - [TiCDC 单行数据正确性校验](/ticdc/ticdc-integrity-check.md)
    - [TiCDC 双向复制](/ticdc/ticdc-bidirectional-replication.md)
    - [同步数据到 Pulsar](/ticdc/ticdc-sink-to-pulsar.md)
    - [同步数据到存储服务](/ticdc/ticdc-sink-to-cloud-storage.md)
    