---
title: TiDB Data Migration 性能问题及处理方法
summary: 了解 DM 可能存在的常见性能问题及其处理方法。
---

# TiDB Data Migration 性能问题及处理方法

本文档介绍 TiDB Data Migration (DM) 中可能存在的、常见的性能问题及其处理方法。

在诊断与处理性能问题时，请确保已经正确配置并安装 DM 的监控组件，并能在 Grafana 监控面板查看 [DM 的监控指标](/dm/monitor-a-dm-cluster.md#task)。

在诊断性能问题时，请先确保对应组件正在正常运行，否则可能出现监控指标异常的情况，对性能问题的诊断造成干扰。

在诊断问题前，也可以先了解 DM 的[性能测试报告](https://github.com/pingcap/docs-dm/blob/release-5.3/zh/dm-benchmark-v5.3.0.md)。

当数据迁移过程存在较大延迟时，若需快速定位瓶颈是在 DM 组件内部还是在 TiDB 集群，可先排查[写入 SQL 到下游](#写入-sql-到下游)部分的 `DML queue remain length`。

## relay log 模块的性能问题及处理方法

在 [relay log 的监控部分](/dm/monitor-a-dm-cluster.md#relay-log)，可以主要通过 `binlog file gap between master and relay` 监控项确认是否存在性能问题。如果该指标长时间大于 1，通常表明存在性能问题；如果该指标基本为 0，一般表明没有性能问题。

如果 `binlog file gap between master and relay` 基本为 0，但仍怀疑存在性能问题，则可以继续查看 `binlog pos`，如果该指标中 `master` 远大于 `relay`，则表明可能存在性能问题。

如果存在性能问题，则继续根据 relay log 模块的主要处理流程分别进行诊断与处理。

### 读取 binlog 数据

与 relay log 模块从上游读取 binlog 数据相关的主要性能指标是 `read binlog event duration`，该指标表示从上游 MySQL/MariaDB 读取到单个 binlog event 所需要的时间，理想情况下应接近于 DM-worker 与 MySQL/MariaDB 实例间的网络延迟。

对于同机房的数据迁移，这部分一般不会成为性能瓶颈；如果该值过大，请排查 DM-worker 与 MySQL/MariaDB 间的网络连通情况。

对于跨机房的数据迁移，可尝试将 DM-worker 与 MySQL/MariaDB 部署在同一机房，而仍将 TiDB 集群部署在目标机房。

从上游读取 binlog 数据这一流程细分后包括以下三个子流程：

- 上游 MySQL/MariaDB 从本地读取 binlog 数据并通过网络进行发送。上游 MySQL/MariaDB 负载无异常时，该子流程通常不会成为瓶颈。
- binlog 数据通过网络从 MySQL/MariaDB 所在机器传输到 DM-worker 所在机器。该子流程主要由 DM-worker 与上游 MySQL/MariaDB 的网络连通情况决定。
- DM-worker 从网络数据流中读取 binlog 数据，并构造成 binlog event。当 DM-worker 负载无异常时，该子流程通常不会成为瓶颈。

> **注意：**
>
> 如果 `read binlog event duration` 的值较大，另一个可能的原因是上游 MySQL/MariaDB 负载较低，一段时间内暂时没有需要发送给 DM 的 binlog event，relay log 模块处于等待状态，导致该值包含了额外的等待时间。

### binlog 数据解码与验证

将 binlog event 读取到 DM 内存后，会进行必要的数据解码与验证，这部分通常不会存在性能瓶颈，因此监控面板上默认无对应性能指标。如果需要查看相应指标，可手动为 Prometheus 中的 `dm_relay_read_transform_duration` 添加相应的监控。

### 写入 relay log 文件

在将 binlog event 写入 relay log 文件时，相关的主要性能指标是 `write relay log duration`，该指标在 `binlog event size` 不是特别大时，值应在微秒级别。如果该值过大，需排查磁盘写入性能，如尽量优先为 DM-worker 使用本地 SSD 等。

## Load 模块的性能问题及处理方法

Load 模块主要操作为从本地读取 SQL 文件数据并写入到下游，对应的主要性能指标是 `transaction execution latency`，如果该值过大，则通常需要根据下游数据库的监控对下游性能进行排查。

另外，也可以查看是否 DM 到下游数据库间的网络存在较大的延迟。

## Binlog replication 模块的性能问题及处理方法

在 [Binlog replication 的监控部分](/dm/monitor-a-dm-cluster.md#binlog-replication)，可以主要通过 `binlog file gap between master and syncer` 监控项确认是否存在性能问题，如果该指标长时间大于 1，则通常表明存在性能问题；如果该指标基本为 0，则一般表明没有性能问题。

如果 `binlog file gap between master and syncer` 长时间大于 1，则可以再通过 `binlog file gap between relay and syncer` 判断延迟主要存在于哪个模块，如果该值基本为 0，则延迟可能存在于 relay log 模块，请先参考 [relay log 模块的性能问题及处理方法](#relay-log-模块的性能问题及处理方法)进行处理；否则继续对 Binlog replication 进行排查。

### 读取 binlog 数据

Binlog replication 模块会根据配置选择从上游 MySQL/MariaDB 或 relay log 文件中读取 binlog event，对应的主要性能指标是 `read binlog event duration`，该值的范围一般是几微秒至几十微秒。

- 如果是从上游 MySQL/MariaDB 读取 binlog event，则可参考 relay log 模块下的[读取 binlog 数据](#读取-binlog-数据)进行排查与处理。

- 如果是从 relay log 文件中读取，则在 `binlog event size` 不是特别大时，`read binlog event duration` 的值应在微秒级别。如果 `read binlog event duration` 过大，则需排查磁盘读取性能，如尽量优先为 DM-worker 使用本地 SSD 等。

### binlog event 转换

Binlog replication 模块从 binlog event 数据中尝试构造 DML、解析 DDL 以及进行 [table router](/dm/dm-table-routing.md) 转换等，主要的性能指标是 `transform binlog event duration`。

这部分的耗时受上游写入的业务特点影响较大，如对于 `INSERT INTO` 语句，转换单个 `VALUES` 的时间和转换大量 `VALUES` 的时间差距很多，其波动范围可能从几十微秒至上百微秒，但一般不会成为系统的瓶颈。

### 写入 SQL 到下游

Binlog replication 模块将转换后的 SQL 写入到下游时，涉及到的性能指标主要包括 `DML queue remain length` 与 `transaction execution latency`。

DM 在从 binlog event 构造出 SQL 后，会使用 `worker-count` 个队列尝试并发写入到下游。但为了避免监控条目过多，会将并发队列编号按 `8` 取模，即所有并发队列在监控上会对应到 `q_0` 到 `q_7` 的某一项。

`DML queue remain length` 用于表示并发处理队列中尚未取出并开始用于向下游写入的 DML 语句数，理想情况下，各 `q_*` 对应的曲线应该基本一致，如果极不一致则表明并发的负载极不均衡。

如果负载不均衡，请确认需要迁移的所有表结构中都有主键或唯一键，如没有主键或唯一键则请尝试为其添加主键或唯一键；如果存在主键或唯一键时仍存在该问题，可尝试升级 DM 到 v1.0.5 及以上的版本。

当整个数据迁移链路无明显延迟时，`DML queue remain length` 对应曲线应基本为 0，且最大通常应不超过任务配置文件中的 `batch` 值。

如果确认数据迁移链路存在明显延迟，且 `DML queue remain length` 中各 `q_*` 对应的曲线基本一致且基本为 0，则表明 DM 未能及时地从上游读取数据、进行转换或进行并行分发（如瓶颈存在于 relay log 模块等），请参考本文档前述各节进行排查。

如果 `DML queue remain length` 对应曲线不为 0（最大一般不超过 1024），则通常表明向下游写入 SQL 时存在瓶颈，可通过 `transaction execution latency` 查看向下游执行单个事务的耗时情况。

`transaction execution latency` 一般应在几十毫秒。如果该值过高，则通常需要根据下游数据库的监控对下游性能进行排查，另外也可以关注是否 DM 到下游数据库间的网络存在较大的延迟。

此外，也可通过 `statement execution latency` 查看向下游写入 `BEGIN`、`INSERT`/`UPDATE`/`DELETE`、`COMMIT` 等单条语句的耗时情况。
