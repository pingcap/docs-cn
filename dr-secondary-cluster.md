---
title: TiDB 主备集群容灾
summary: 介绍在容灾场景下，如何使用 TiCDC 构建主备容灾集群
---

# TiDB 主备集群容灾

使用主、备数据库进行容灾是一种常用的容灾方式。在这种方案下，系统会有一个主集群用于处理用户的请求，并有一个备用集群负责备份主数据库的数据。当主集群发生故障时，系统可以切换到备用集群，使用备份的数据继续提供服务。这样，系统就可以在主数据库发生故障的情况下继续正常运行，避免因为故障而导致的服务中断。使用主、备数据库进行容灾具有如下优势：

- 高可用性：主、备集群的架构可以有效提高系统的可用性，使得系统在遇到故障时能够快速恢复。
- 快速切换：在主集群发生故障的情况下，系统可以快速切换到备用集群，继续提供服务。
- 数据一致性：备用集群会近实时备份主集群的数据，因此在故障发生后切换到从集群时，数据基本是最新的。

## 基于 TiCDC 的构建 TiDB 主备集群

![TiCDC secondary cluster architecture](/media/dr/dr-ticdc-secondary-cluster.png)

在上述架构中，包含了两个 TiDB 集群：Primary Cluster 和 Secondary Cluster。Primary Cluster 运行在 Region 1 中，是一个三副本的集群，用于处理读写业务。Secondary Cluster 运行在 Region 2 中，是一个备用集群，通过 TiCDC 从 Primary Cluster 同步数据。这种容灾架构简洁易用，可以容忍 Region 级别的故障，并且在保证 Primary Cluster 的写入性能不会下降的同时，备用集群还可以用于处理一些延迟不敏感的只读业务。它的 Recovery Point Objective（RPO）在秒级别，Recovery Time Objective（RTO）可以做到分钟级别甚至更低。这是许多数据库厂商推荐的方案，适用于重要的生产系统。

### 搭建主备集群

我们将主备集群分别部署在两个不同的区域，TiCDC 与 TiDB 备用集群部署在一起。当主备集群之间的网络存在延迟，这种架构会实现最好的数据同步性能。 本教程示例的部署拓扑如下，其中的服务器配置可以参考
- [TiDB 软件和硬件环境建议配置](/hardware-and-software-requirements.md)。
- [TiCDC 软件和硬件环境推荐配置](/ticdc/deploy-ticdc.md#软件和硬件环境推荐配置)

|**区域** | **Host** | **集群** | **组件** |
| --- | --- | --- | --- |
| Region 1 | 10.0.1.1/10.0.1.2/10.0.1.3 | Primary | PD |
| Region 1 | 10.0.1.4/10.0.1.5 | Primary| TiDB |
| Region 1 | 10.0.1.6/10.0.1.7/10.0.1.8 | Primary | TiKV |
| Region 2 | 10.1.1.9/10.1.1.10 | Primary | TiCDC |
| Region 2 | 10.1.1.1/10.1.1.2/10.1.1.3 | Secondary | PD |
| Region 2 | 10.1.1.4/10.1.1.5 | Secondary | TiDB |
| Region 2 | 10.1.1.6/10.1.1.7/10.1.1.8 | Secondary | TiKV |


使用 TiUP [部署 TiDB 集群](/production-deployment-using-tiup.md)

并且确保 TiCDC 能访问


### 从主集群复制数据到备用数据

#### 全量数据迁移

#### 实时数据变更复制

### 主备集群状态监控

## 在主备集群之间进行双向复制

## 常见问题处理

- [TiCDC 常见问题处理]

