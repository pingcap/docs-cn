---
title: TiCDC 新架构介绍
summary: 介绍 TiCDC 新架构的主要特性，架构特点，升级部署指南以及其他注意事项。
---

# TiCDC 新架构介绍

TiCDC 新架构通过重新设计核心组件和优化数据处理流程，显著提升了实时数据同步的性能、扩展性和稳定性，同时降低了资源成本。新架构的主要优势包括：

- **更高的单节点性能**：单节点最高可支持 50 万张表的同步任务，宽表场景下的同步流量最高可达 200MiB/s。
- **更强的扩展能力**：集群同步能力接近线性扩展，单集群可扩展至超过 100 个节点，支持超 1 万个 Changefeed；单个 Changefeed 可支持百万级表的同步任务。
- **更高的稳定性**：在高流量、频繁 DDL 操作及集群扩缩容等场景下，Changefeed 的延迟更低且更加稳定。通过资源隔离和优先级调度，减少了多个 Changefeed 任务之间的相互干扰。
- **更低的资源成本**：通过改进资源利用率，减少冗余开销，在典型场景下，CPU 和内存等资源的利用效率提升高达一个数量级。

> **警告：**
>
> TiCDC 新架构目前为实验特性，不建议在生产环境中使用。该功能可能会在未事先通知的情况下发生变化或删除。如果发现 bug，请在 GitHub 上提 [issue](https://github.com/pingcap/tidb/issues) 反馈。

## 架构设计

![TiCDC New Architecture](/media/ticdc/ticdc-new-arch-1.jpg)

TiCDC 新架构由 Log Service 和 Downstream Adapter 两大核心组件构成。

- Log Service：作为核心数据服务层，Log Service 负责实时拉取上游 TiDB 集群的行变更和 DDL 变更等信息，并将变更数据临时存储在本地磁盘上。此外，它还负责响应 Downstream Adapter 的数据请求，定时将 DML 和 DDL 数据合并排序并推送至 Downstream Adapter。
- Downstream Adapter：作为下游数据同步适配层，Downstream Adapter 负责处理用户发起的 Changefeed 运维操作，调度生成相关同步任务，从 Log Service 获取数据并同步至下游系统。

TiCDC 新架构通过将整体架构拆分成有状态和无状态的两部分，显著提升了系统的可扩展性、可靠性和灵活性。Log Service 作为有状态组件，专注于数据的获取、排序和存储，通过与 Changefeed 业务逻辑的解耦，实现了数据在多个 Changefeed 间的共享，有效提高了资源利用率，降低了系统开销。 Downstream Adapter 作为无状态组件，采用轻量级调度机制，支持任务在不同实例间的快速迁移，并根据负载变化灵活调整同步任务的拆分与合并，确保在各种场景下都能实现低延迟的数据同步。

## 新老架构对比

新架构旨在解决系统规模持续扩展过程中用户普遍面临的性能瓶颈、稳定性不足及扩展性受限等核心问题。相较于传统架构，新架构在以下关键维度实现了显著优化：

| 特性                     | TiCDC 老架构                             | TiCDC 新架构                             |
| ------------------------ | ---------------------------------------- | ---------------------------------------- |
| **处理逻辑驱动方式**      | Timer Driven（定时器驱动）               | Event Driven（事件驱动）                 |
| **任务触发机制**          | 定时器触发的大循环，每隔 50ms 检查任务，处理性能有限    | 由事件驱动，包括 DML、DDL 变更及 Changefeed 操作，队列中的事件会被尽快处理，无需等待 50ms 的固定间隔，从而减少了额外的延迟 |
| **任务调度方式**          | 每个 Changefeed 运行一个主循环，轮询检查任务 | 事件被放入队列后，由多个线程并发消费处理   |
| **任务处理效率**          | 每个任务需要经过多个周期，存在性能瓶颈    | 事件可以立即处理，无需等待固定间隔，减少延迟 |
| **资源消耗**              | 对不活跃表进行频繁检查，浪费 CPU 资源    | 消费线程仅处理队列中的事件，无需检查不活跃任务 |
| **复杂度**                | O(n)，表数量增多时性能下降               | O(1)，不受表数量影响，效率更高           |
| **CPU 利用率**            | 每个 Changefeed 只能利用一个逻辑 CPU     | 能充分利用多核 CPU 的并行处理能力        |
| **扩展能力**              | 受限于 CPU 数量，扩展性差                | 通过多线程消费和事件队列，可扩展性强     |
| **Changefeed 干扰问题**   | 中央控制节点（Owner）会造成 Changefeed 之间的干扰 | 事件驱动模式避免了 Changefeed 之间的干扰 |

![TiCDC New Architecture](/media/ticdc/ticdc-new-arch-2.jpg)

## 部署指南

TiCDC 新架构仅支持 v7.5 或者以上版本的 TiDB 集群，使用之前需要确保 TiDB 集群版本满足要求。

### 使用 TiUP 部署启用新架构 TiCDC 的全新 TiDB 集群

在使用 TiUP 部署 v9.0.0 或者以上版本的全新 TiDB 集群时，支持同时部署启用新架构的 TiCDC 组件。你需要在 TiUP 启动 TiDB 集群时的配置文件中加入 TiCDC 组件相关的部分并启用新架构，以下是一个示例：

```shell
cdc_servers:
  - host: 10.0.1.20
    config:
      newarch: true
  - host: 10.0.1.21
    config:
      newarch: true
```

> **注意：**
> 
> `newarch`  配置项仅用于新架构，不添加 `newarch` 配置项则默认使用老架构。在使用 TiCDC 老架构时，请勿在配置文件中添加 `newarch` 配置项，否则可能会导致解析失败。

其他详细操作，请参考[使用 TiUP 部署包含 TiCDC 组件的全新 TiDB 集群](/ticdc/deploy-ticdc.md#使用-tiup-部署包含-ticdc-组件的全新-tidb-集群)。

### 使用 TiUP 在原有 TiDB 集群全新部署启用新架构的 TiCDC 组件

1. 参考[扩容 TiCDC 节点](/scale-tidb-using-tiup.md#扩容-ticdc-节点)在集群中扩容新的 TiCDC 节点。

2. 参考下一节启用 TiCDC 新架构。

### 使用 TiUP 将原有 TiDB 集群中的 TiCDC 升级为新架构

如果 TiDB 集群为 v9.0.0 之前版本，请通过以下方式将集群中 TiCDC 组件版本升级到 v9.0.0 或者以上版本，然后再启用新架构：

> **注意：**
> 
> 升级至 TiCDC 新架构后，将不再支持回退至旧架构。

1. 下载 v9.0.0 或者以上版本的 TiCDC 二进制文件。

    该文件下载链接格式为 `https://tiup-mirrors.pingcap.com/cdc-${version}-${os}-${arch}.tar.gz`，其中，{version} 为 TiCDC 版本号，${os} 为你的操作系统，{arch} 为组件运行的平台（`amd64` 或 `arm64`）。

    例如，可以使用以下命令下载 Linux 系统 x86-64 架构的 TiCDC v9.0.0 的二进制文件：

   ```shell
   wget https://tiup-mirrors.pingcap.com/cdc-v9.0.0-linux-amd64.tar.gz
   ```

2. 将下载的 TiCDC 二进制文件 Patch 到你的 TiDB 集群中：

    ```shell
    tiup cluster patch <cluster-name> ./cdc-v9.0.0-linux-amd64.tar.gz -R cdc
    ```

当 TiDB 集群中 TiCDC 组件版本已经升级到 v9.0.0 或者以上版本后，可以通过以下步骤启用 TiCDC 新架构。

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

## 使用指南

在 TiCDC 新架构的节点部署完成后，即可使用相应的命令进行操作。新架构沿用了旧架构的 TiCDC 使用方式，因此无需额外学习新的命令，也无需修改旧架构中使用到的命令。

例如，要在新架构的 TiCDC 节点中创建同步任务，可执行以下命令：

```
cdc cli changefeed create --server=http://127.0.0.1:8300 --sink-uri="mysql://root:123456@127.0.0.1:3306/" --changefeed-id="simple-replication-task" 
```

若需查询特定同步任务的信息，可执行：

```
cdc cli changefeed query -s --server=http://127.0.0.1:8300 --changefeed-id=simple-replication-task
```

更多命令的使用方法和细节，可以参考[管理 Changefeed](/ticdc/ticdc-manage-changefeed.md)。

## 注意事项

- 在 TiCDC 的老架构中，DDL 的同步是完全串行进行的，因此同步进度仅需通过 Changefeed 的 `CheckpointTs` 来标识。然而，在新架构中，为了提高 DDL 同步效率，TiCDC 会尽可能并行同步不同表的 DDL 变更。为了在下游 MySQL 兼容数据库中准确记录各表的 DDL 同步进度，TiCDC 新架构会在下游数据库中创建一张名为 `tidb_cdc.ddl_ts_v1` 的表，专门用于存储 Changefeed 的 DDL 同步进度信息。

- 作为实验性特性，TiCDC v9.0 的新架构尚未完全实现旧架构中的所有功能，这些功能将在后续的 GA 版本中完整实现，具体包括：

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