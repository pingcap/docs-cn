---
title: TiFlash 概述
summary: 了解 TiFlash 的架构和主要特性。
---

# TiFlash 概述

[TiFlash](https://github.com/pingcap/tiflash) 是使 TiDB 成为混合事务/分析处理 (HTAP) 数据库的关键组件。作为 TiKV 的列式存储扩展，TiFlash 提供了良好的隔离级别和强一致性保证。

在 TiFlash 中，列式副本根据 Raft Learner 共识算法进行异步复制。在读取这些副本时，通过验证 Raft 索引和多版本并发控制 (MVCC) 来实现快照隔离级别的一致性。

<CustomContent platform="tidb-cloud">

使用 TiDB Cloud，您可以根据 HTAP 工作负载轻松创建 HTAP 集群，只需指定一个或多个 TiFlash 节点即可。如果在创建集群时未指定 TiFlash 节点数量，或者您想添加更多 TiFlash 节点，可以通过[扩展集群](/tidb-cloud/scale-tidb-cluster.md)来更改节点数量。

</CustomContent>

## 架构

![TiFlash 架构](/media/tidb-storage-architecture-1.png)

上图是包含 TiFlash 节点的 TiDB HTAP 形态的架构。

TiFlash 提供列式存储，并通过 ClickHouse 高效实现了一层协处理器。与 TiKV 类似，TiFlash 也有一个多 Raft 系统，支持以 Region 为单位复制和分发数据（详情请参见[数据存储](https://www.pingcap.com/blog/tidb-internal-data-storage/)）。

TiFlash 以低成本实时复制 TiKV 节点中的数据，不会阻塞 TiKV 中的写入。同时，它提供与 TiKV 相同的读一致性，并确保读取最新数据。TiFlash 中的 Region 副本在逻辑上与 TiKV 中的副本相同，并与 TiKV 中的 Leader 副本同时进行分裂和合并。

要在 Linux AMD64 架构下部署 TiFlash，CPU 必须支持 AVX2 指令集。确保 `cat /proc/cpuinfo | grep avx2` 有输出。要在 Linux ARM64 架构下部署 TiFlash，CPU 必须支持 ARMv8 指令集架构。确保 `cat /proc/cpuinfo | grep 'crc32' | grep 'asimd'` 有输出。通过使用指令集扩展，TiFlash 的向量化引擎可以提供更好的性能。

<CustomContent platform="tidb">

TiFlash 同时兼容 TiDB 和 TiSpark，使您可以在这两个计算引擎之间自由选择。

</CustomContent>

建议将 TiFlash 部署在与 TiKV 不同的节点上，以确保工作负载隔离。如果不需要业务隔离，也可以将 TiFlash 和 TiKV 部署在同一节点上。

目前，数据不能直接写入 TiFlash。您需要先将数据写入 TiKV，然后复制到 TiFlash，因为它作为 Learner 角色连接到 TiDB 集群。TiFlash 支持以表为单位进行数据复制，但部署后默认不会复制任何数据。要复制指定表的数据，请参见[为表创建 TiFlash 副本](/tiflash/create-tiflash-replicas.md#为表创建-tiflash-副本)。

TiFlash 由两个主要组件组成：列式存储组件和 TiFlash 代理组件。TiFlash 代理组件负责使用多 Raft 共识算法进行通信。

在收到为表在 TiFlash 中创建副本的 DDL 命令后，TiDB 会自动在 PD 中创建相应的[放置规则](https://docs.pingcap.com/tidb/stable/configure-placement-rules)，然后 PD 根据这些规则执行相应的数据调度。

## 主要特性

TiFlash 具有以下主要特性：

- [异步复制](#异步复制)
- [一致性](#一致性)
- [智能选择](#智能选择)
- [计算加速](#计算加速)

### 异步复制

TiFlash 中的副本作为特殊角色 Raft Learner 进行异步复制。这意味着当 TiFlash 节点宕机或出现高网络延迟时，TiKV 中的应用程序仍可正常进行。

这种复制机制继承了 TiKV 的两个优点：自动负载均衡和高可用性。

- TiFlash 不依赖额外的复制通道，而是直接以多对多的方式从 TiKV 接收数据。
- 只要数据在 TiKV 中没有丢失，您随时都可以在 TiFlash 中恢复副本。

### 一致性

TiFlash 提供与 TiKV 相同的快照隔离级别一致性，并确保读取最新数据，这意味着您可以读取之前写入 TiKV 的数据。这种一致性是通过验证数据复制进度来实现的。

每次 TiFlash 收到读取请求时，Region 副本都会向 Leader 副本发送进度验证请求（一个轻量级的 RPC 请求）。只有在当前复制进度包含读取请求时间戳所覆盖的数据后，TiFlash 才会执行读取操作。

### 智能选择

TiDB 可以自动选择使用 TiFlash（列式）或 TiKV（行式），或在一个查询中同时使用两者，以确保最佳性能。

这种选择机制类似于 TiDB 选择不同索引来执行查询。TiDB 优化器根据读取成本的统计信息做出适当的选择。

### 计算加速

TiFlash 通过两种方式加速 TiDB 的计算：

- 列式存储引擎在执行读取操作时更高效。
- TiFlash 分担 TiDB 的部分计算工作负载。

TiFlash 以与 TiKV 协处理器相同的方式分担计算工作负载：TiDB 下推可以在存储层完成的计算。计算是否可以下推取决于 TiFlash 的支持情况。详情请参见[支持的下推计算](/tiflash/tiflash-supported-pushdown-calculations.md)。

## 使用 TiFlash

部署 TiFlash 后，数据复制不会自动开始。您需要手动指定要复制的表。

<CustomContent platform="tidb">

您可以根据自己的需求，使用 TiDB 读取 TiFlash 副本进行中等规模的分析处理，或使用 TiSpark 读取 TiFlash 副本进行大规模的分析处理。详情请参见以下章节：

</CustomContent>

<CustomContent platform="tidb-cloud">

您可以使用 TiDB 读取 TiFlash 副本进行分析处理。详情请参见以下章节：

</CustomContent>

- [创建 TiFlash 副本](/tiflash/create-tiflash-replicas.md)
- [使用 TiDB 读取 TiFlash 副本](/tiflash/use-tidb-to-read-tiflash.md)

<CustomContent platform="tidb">

- [使用 TiSpark 读取 TiFlash 副本](/tiflash/use-tispark-to-read-tiflash.md)

</CustomContent>

- [使用 MPP 模式](/tiflash/use-tiflash-mpp-mode.md)

<CustomContent platform="tidb">

要体验从导入数据到在 TPC-H 数据集中查询的完整过程，请参考 [TiDB HTAP 快速上手指南](/quick-start-with-htap.md)。

</CustomContent>

## 另请参阅

<CustomContent platform="tidb">

- 要部署带有 TiFlash 节点的新集群，请参见[使用 TiUP 部署 TiDB 集群](/production-deployment-using-tiup.md)。
- 要在已部署的集群中添加 TiFlash 节点，请参见[扩容 TiFlash 集群](/scale-tidb-using-tiup.md#扩容-tiflash-集群)。
- [维护 TiFlash 集群](/tiflash/maintain-tiflash.md)。
- [调优 TiFlash 性能](/tiflash/tune-tiflash-performance.md)。
- [配置 TiFlash](/tiflash/tiflash-configuration.md)。
- [监控 TiFlash 集群](/tiflash/monitor-tiflash.md)。
- 了解 [TiFlash 告警规则](/tiflash/tiflash-alert-rules.md)。
- [排查 TiFlash 集群问题](/tiflash/troubleshoot-tiflash.md)。
- [TiFlash 支持的下推计算](/tiflash/tiflash-supported-pushdown-calculations.md)
- [TiFlash 数据验证](/tiflash/tiflash-data-validation.md)
- [TiFlash 兼容性](/tiflash/tiflash-compatibility.md)

</CustomContent>

<CustomContent platform="tidb-cloud">

- [调优 TiFlash 性能](/tiflash/tune-tiflash-performance.md)。
- [TiFlash 支持的下推计算](/tiflash/tiflash-supported-pushdown-calculations.md)
- [TiFlash 兼容性](/tiflash/tiflash-compatibility.md)

</CustomContent>
