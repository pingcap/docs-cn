---
title: TiCDC 新架构介绍
summary: 介绍 TiCDC 新架构的主要特性、架构设计、升级部署指南以及其他注意事项。
---

# TiCDC 新架构介绍

自 v8.5.4-release.1 版本起，TiCDC 引入新架构，显著提升了实时数据复制的性能、可扩展性与稳定性，同时降低了资源成本。新架构重新设计了 TiCDC 的核心组件并优化了数据处理流程，具有以下优势：

- **更高的单节点性能**：单节点最高可支持 50 万张表的同步任务，宽表场景下单节点同步流量最高可达 190 MB/s。
- **更强的扩展能力**：集群同步能力接近线性扩展，单集群可扩展至超过 100 个节点，支持超 1 万个 Changefeed；单个 Changefeed 可支持百万级表的同步任务。
- **更高的稳定性**：在高流量、频繁 DDL 操作及集群扩缩容等场景下，Changefeed 的延迟更低且更加稳定。通过资源隔离和优先级调度，减少了多个 Changefeed 任务之间的相互干扰。
- **更低的资源成本**：通过改进资源利用率，减少冗余开销。在典型场景下，CPU 和内存等资源的使用量降低高达 50%。

## 架构设计

![TiCDC 新架构](/media/ticdc/ticdc-new-arch-1.png)

TiCDC 新架构由 Log Service 和 Downstream Adapter 两大核心组件构成。

- Log Service：作为核心数据服务层，Log Service 负责实时拉取上游 TiDB 集群的行变更和 DDL 变更等信息，并将变更数据临时存储在本地磁盘上。此外，它还负责响应 Downstream Adapter 的数据请求，定时将 DML 和 DDL 数据合并排序并推送至 Downstream Adapter。
- Downstream Adapter：作为下游数据同步适配层，Downstream Adapter 负责处理用户发起的 Changefeed 运维操作，调度生成相关同步任务，从 Log Service 获取数据并同步至下游系统。

TiCDC 新架构通过将整体架构拆分成有状态和无状态的两部分，显著提升了系统的可扩展性、可靠性和灵活性。Log Service 作为有状态组件，专注于数据的获取、排序和存储，通过与 Changefeed 业务逻辑的解耦，实现了数据在多个 Changefeed 间的共享，有效提高了资源利用率，降低了系统开销。Downstream Adapter 作为无状态组件，采用轻量级调度机制，支持任务在不同实例间的快速迁移，并根据负载变化灵活调整同步任务的拆分与合并，确保在各种场景下都能实现低延迟的数据同步。

## 新老架构对比

新架构旨在解决系统规模持续扩展过程中常见的性能瓶颈、稳定性不足及扩展性受限等核心问题。相较于传统架构，新架构在以下关键维度实现了显著优化：

| 特性                     | TiCDC 老架构                             | TiCDC 新架构                             |
| ------------------------ | ---------------------------------------- | ---------------------------------------- |
| **处理逻辑驱动方式**      | Timer Driven（定时器驱动）               | Event Driven（事件驱动）                 |
| **任务触发机制**          | 定时器触发的大循环，每隔 50 ms 检查任务，处理性能有限    | 由事件驱动，包括 DML、DDL 变更及 Changefeed 操作，队列中的事件会被尽快处理，无需等待 50 ms 的固定间隔，从而减少了额外的延迟 |
| **任务调度方式**          | 每个 Changefeed 运行一个主循环，轮询检查任务 | 事件被放入队列后，由多个线程并发消费处理   |
| **任务处理效率**          | 每个任务需要经过多个周期，存在性能瓶颈    | 事件可以立即处理，无需等待固定间隔，减少延迟 |
| **资源消耗**              | 频繁检查不活跃表，浪费 CPU 资源    | 消费线程仅处理队列中的事件，无需检查不活跃任务 |
| **复杂度**                | O(n)，表数量增多时性能下降               | O(1)，不受表数量影响，效率更高           |
| **CPU 利用率**            | 每个 Changefeed 只能利用一个逻辑 CPU     | 能充分利用多核 CPU 的并行处理能力        |
| **扩展能力**              | 受限于 CPU 数量，扩展性差                | 通过多线程消费和事件队列，可扩展性强     |
| **Changefeed 干扰问题**   | 中央控制节点 (Owner) 会造成 Changefeed 之间的干扰 | 事件驱动模式避免了 Changefeed 之间的干扰 |

![TiCDC 新老架构对比](/media/ticdc/ticdc-new-arch-2.png)

## 新老架构选择

如果您的业务存在以下任一情况，我们建议您从老架构切换至新架构，以获得更优的性能与稳定性：

- 增量扫性能瓶颈：增量扫任务长期无法完成，据同步延迟持续升高。
- MySQL Sink 写入超大流量单表：目标表结构满足“有且仅有一个主键或非空唯一键”。
- 海量表同步场景：同步的表数量超过 10 万张。
- 高频 DDL 操作引发延迟：频繁执行 DDL 语句导致同步延迟显著上升。

## 新功能介绍

新架构支持在 MySQL sink 中启用表级任务拆分。您可以通过在 changefeed 配置中设置 `scheduler.enable-table-across-nodes = true` 来开启此功能。开启后，所有有且仅有一个主键或非空唯一键的表，当超过配置的 region 个数阈值 （默认为`100000`）或者写流量阈值（默认未开启）时，会对表会进行拆分，并分发到多个不同节点上执行，从而提升同步效率与资源利用率。Region 个数阈值可以通过 `scheduler.region-threshold` 配置。写流量阈值可以通过 `scheduler.write-key-threshold` 配置。

## 兼容性介绍

### Server 级别错误的处理机制

在 TiCDC 的老架构中，如果 CDC 出现 Server 级别的错误，比如 ErrEtcdSessionDone，CDC 会自动重启主线程，进程不会退出。

而在新架构中，如果出现 CDC Server 级别的错误，进程会直接退出，需要借助外部运维工具（如 TiUP 或 TiDB Operator）来重新启动 TiCDC 进程。

### DDL 进度表

在 TiCDC 的老架构中，DDL 的同步是完全串行进行的，因此同步进度仅需通过 Changefeed 的 CheckpointTs 来标识。然而，在新架构中，为了提高 DDL 同步效率，TiCDC 会尽可能并行同步不同表的 DDL 变更。为了在下游 MySQL 兼容数据库中准确记录各表的 DDL 同步进度，TiCDC 新架构会在下游数据库中创建一张名为 tidb_cdc.ddl_ts_v1 的表，专门用于存储 Changefeed 的 DDL 同步进度信息。

### DDL 同步行为变更

1. TiCDC 老架构不支持同步对表名进行交换的 rename table DDL（例如：RENAME TABLE a TO c, b TO a, c TO b;） ，TiCDC 新架构已支持同步该类型的 DDL。
2. TiCDC 新架构统一并简化了 Rename DDL 的过滤规则。
  1. 在老架构中，单表与多表 Rename 操作的过滤逻辑不一致： 
    1. 单表 RENAME：仅需旧表名符合过滤规则，即会同步。 
    2. 多表 RENAME：则要求所有表的旧表名与新表名均符合规则，才会同步。 
  2. 新架构将此行为统一：无论单表还是多表 Rename，只要语句中涉及的旧表名符合过滤规则，整个 DDL 语句就会被同步。
  3. 例如：changefeed 的配置文件如下时
    ```
    [filter]
    rules = ['test.t*']
    ```
    1. 在老架构中，对于一条语句内 rename 单个表的 DDL，如 `RENAME TABLE test.t1 TO ignore.t1`，因旧表库名 `test.t1` 符合 filter 过滤规则，该 DDL 会被同步。
    2. 在老架构中，对于一条语句内 rename 多个表的 DDL，如 `RENAME TABLE test.t1 TO ignore.t1, test.t2 TO test.t22;`，由于新的表库名 `ignore.t1` 不符合 filter 过滤规则，该 DDL 不会被同步。
    3. 在新架构中，由于旧表库名（如 `test.t1`，`test.t2`）符合 filter 过滤规则，上述两条 DDL 均会被同步。

## 使用限制

目前，TiCDC 新架构已完整实现了旧架构的全部功能，但其中部分功能尚未通过全面的测试验证。因此，我们建议您在非核心生产环境中谨慎使用以下功能：

- [Redo Log](/ticdc/ticdc-sink-to-mysql.md#灾难场景的最终一致性复制)
- [Pulsar Sink](/ticdc/ticdc-sink-to-pulsar.md)
- [Storage Sink](/ticdc/ticdc-sink-to-cloud-storage.md)

此外，TiCDC 新架构目前暂不支持将大事务拆分为多个批次同步至下游，因此在处理超大事务时仍存在 OOM 风险，请在实际使用中注意评估相关影响。

# 部署指南

TiCDC 新架构仅支持 v7.5.0 或者以上版本的 TiDB 集群，使用之前需要确保 TiDB 集群版本满足要求。

## TiUP

1. 如果你的 TiDB 集群中尚无 TiCDC 节点，参考[扩容 TiCDC 节点](/scale-tidb-using-tiup.md#扩容-ticdc-节点)在集群中扩容新的 TiCDC 节点，否则跳过该步骤。

2. 手动下载 TiCDC 新架构离线包。文件下载链接格式为 `https://tiup-mirrors.pingcap.com/cdc-${version}-${os}-${arch}.tar.gz`。其中，`${version}` 为 TiCDC 版本号，`${os}` 为你的操作系统，`${arch}` 为组件运行的平台（`amd64` 或 `arm64`）。。

    例如，可以使用以下命令下载 Linux 系统 x86-64 架构的 TiCDC v9.0.0-beta.1 的二进制文件：

    ```shell
    wget https://tiup-mirrors.pingcap.com/cdc-v8.5.4-release.1-linux-amd64.tar.gz
    ```

3. 如果集群中已经有 Changefeed，请参考[停止同步任务](/ticdc/ticdc-manage-changefeed.md#停止同步任务)暂停所有的 Changefeed 同步任务。例如：
    
    ```shell
    # cdc 默认服务端口为 8300
    cdc cli changefeed pause --server=http://<ticdc-host>:8300 --changefeed-id <changefeed-name>
    ```

2. 使用 [`tiup cluster patch`](/tiup/tiup-component-cluster-patch.md) 命令将下载的 TiCDC 二进制文件动态替换到你的 TiDB 集群中：

    ```shell
    tiup cluster patch <cluster-name> ./cdc-v8.5.4-release.1-linux-amd64.tar.gz -R cdc
    ```

4. 通过 [`tiup cluster edit-config`](/tiup/tiup-component-cluster-edit-config.md) 命令更新 TiCDC 配置：

    ```shell
    tiup cluster edit-config <cluster-name>
    ```

    ```yaml
    server_configs:
      cdc:
        newarch: true
    ```

5. 参考[恢复同步任务](/ticdc/ticdc-manage-changefeed.md#恢复同步任务)恢复所有的 Changefeed 同步任务。例如：
    
    ```shell
    # cdc 默认服务端口为 8300
    cdc cli changefeed resume --server=http://<ticdc-host>:8300 --changefeed-id <changefeed-name>
    ```

## TiDB Operator

1. 如果现有 TiDB 集群中没有 TiCDC 组件，参考在现有 TiDB 集群上新增 TiCDC 组件在集群中扩容新的 TiCDC 节点，操作时，只需在集群配置文件中将 TiCDC 的镜像版本指定为新架构版本即可。以下是一个示例：

```
spec:
  ticdc:
    baseImage: pingcap/ticdc
    version: v8.5.4-release.1
    replicas: 3
    config:
      newarch = true
```

2. 如果现有 TiDB 集群中已有 TiCDC 组件，
    1. 如果集群中已经有 Changefeed，暂停所有的 Changefeed 同步任务。
    
    ```shell
    kubectl exec -it ${pod_name} -n ${namespace} -- sh
    ```

    ```shell
    # 通过 TiDB operator 部署的 TiCDC 服务器的默认端口为 8301 
    /cdc cli changefeed pause --server=http://127.0.0.1:8301 --changefeed-id <changefeed-name>
    ```

    2. 修改集群配置文件中 TiCDC 组件的镜像版本为新架构版本。
    ```shell
    kubectl edit tc ${cluster_name} -n ${namespace}
    ```

    ```
    spec:
      ticdc:
        baseImage: pingcap/ticdc
        version: v8.5.4-release.1
        replicas: 3
    ```

    ```shell
    kubectl apply -f ${cluster_name} -n ${namespace}
    ```

    3. 恢复所有的 Changefeed 同步任务。

    ```shell
    kubectl exec -it ${pod_name} -n ${namespace} -- sh
    ```

    ```shell
    # 通过 TiDB operator 部署的 TiCDC 服务器的默认端口为 8301 
    /cdc cli changefeed resume --server=http://127.0.0.1:8301 --changefeed-id <changefeed-name>
    ```

# 使用指南

在 TiCDC 新架构的节点部署完成后，即可使用相应的命令进行操作。新架构沿用了旧架构的 TiCDC 使用方式，因此无需额外学习新的命令，也无需修改旧架构中使用到的命令。

例如，要在新架构的 TiCDC 节点中创建同步任务，可执行以下命令：

```shell
cdc cli changefeed create --server=http://127.0.0.1:8300 --sink-uri="mysql://root:123456@127.0.0.1:3306/" --changefeed-id="simple-replication-task"
```

若需查询特定同步任务的信息，可执行：

```shell
cdc cli changefeed query -s --server=http://127.0.0.1:8300 --changefeed-id=simple-replication-task
```

更多命令的使用方法和细节，可以参考[管理 Changefeed](/ticdc/ticdc-manage-changefeed.md)。

# 监控

TiCDC 新架构监控面板已集成到 Grafana 面板中，其名称为 **TiCDC-New-Arch**，可以通过该面板查看新架构相关监控指标。

## Summary

![Summary](/media/ticdc/ticdc-new-arch-metric-1.png)

- Changefeed Checkpoint Lag：同步任务在下游与上游之间的时序差距。
- Changefeed ResolvedTs Lag：TiCDC 节点内部处理进度与上游数据库的时序差距。
- Upstream Write Bytes/s：上游数据库的写入吞吐量。
- TiCDC Input Bytes/s：TiCDC 从上游接收数据的写入吞吐量。
- Sink Event Row Count/s：TiCDC 向下游每秒写入的数据行数。
- Sink Write Bytes/s：TiCDC 向下游每秒写入的数据量。
- The Status of Changefeeds：Changefeed 的状态。
- Table Dispatcher Count：不同 Changefeed 对应的 Dispatcher 数量。
- Memory Quota：Event Collector 内存配额及使用量，使用量过大会导致限流。

## Server

![Server](/media/ticdc/ticdc-new-arch-metric-2.png)

- Uptime：TiKV 节点和 TiCDC 节点已经运行的时间
- Goroutine Count：TiCDC 节点 Goroutine 的个数
- Open FD Count：TiCDC 节点打开的文件句柄个数
- CPU Usage：TiCDC 节点使用的 CPU
- Memory Usage：TiCDC 节点使用的内存
- Ownership History：TiCDC 集群中 Owner 节点的历史记录
- PD Leader History：上游 TiDB 集群中 PD Leader 节点的历史记录

## Log Puller

![Log Puller](/media/ticdc/ticdc-new-arch-metric-3.png)

- Input Events/s: TiCDC 每秒收到的事件数
- Unresolved Region Request Count: TiCDC 已经发送但是没有结束的 region 增量扫请求数量，该监控会动态变化。
- Region Request Finish Scan Duration: region 增量扫的耗时。
- Subscribed Region Count: 订阅的 Region 总数
- Memory Quota: Log Puller 内存配额及使用量，使用量过大会导致限流。
- Resolved Ts Batch Size (Regions): 单个 Resolved Ts 事件包含的 Region 数量

## Event Store

![Event Store](/media/ticdc/ticdc-new-arch-metric-4.png)

- Resolved Ts Lag: Event Store 处理进度与上游数据库的时序差距。
- Register Dispatcher StartTs Lag: Dispatcher 注册请求的 StartTs 与当前时间点之间的时序差距。
- Subscriptions Resolved Ts Lag: Subscription 处理进度与上游数据库的时序差距。
- Subscriptions Data GC Lag: Subscription 数据 GC 进度与当前时间点的时序差距。
- Input Event Count/s: Event Store 每秒处理的事件数。
- Input Bytes/s: Event Store 每秒处理的数据量大小。
- Write Requests/s: Event Store 每秒执行的写入操作数。
- Write Worker Busy Ratio: Event Store 写线程的 IO 时间占总运行时间的比例。
- Compressed Rows/s:  Event Store 每秒压缩的数据行数（仅当行大小超过设定阈值时触发压缩）。
- Write Duration: Event Store 写入操作耗时。
- Write Batch Size: 单次写入操作的批量数据大小。
- Write Batch Event Count: 单次写入批次中包含的数据行数。
- Data Size On Disk: Event Store 占用的磁盘数据总量。
- Data Size In Memory: Event Store 占用的内存数据总量。
- Scan Requests/s: Event Store 每秒处理的扫描操作数。
- Scan Bytes/s: Event Store 每秒扫描的数据量。

## Sink

![Sink](/media/ticdc/ticdc-new-arch-metric-5.png)

- Output Row Batch Count: Sink 每批次写入 DML 的平均行数。
- Output Row Count(per second): 每秒钟往下游写的 DML 总行数
- Output DDL Executing Duration: 当前节点上对应 Changefeed 执行 DDL Event 的耗时
- Sink Error Count / m: Sink 模块该分钟报错信息的数目
- Output DDL Count / Minutes: 当前节点上对应 Changefeed 每分钟执行的 DDL 个数
