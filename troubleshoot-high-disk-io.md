---
title: TiDB 磁盘 I/O 过高的处理办法
summary: 了解如何定位和处理 TiDB 存储 I/O 过高的问题。
---

# TiDB 磁盘 I/O 过高的处理办法

本文主要介绍如何定位和处理 TiDB 存储 I/O 过高的问题。

## 确认当前 I/O 指标

当出现系统响应变慢的时候，如果已经排查了 CPU 的瓶颈、数据事务冲突的瓶颈后，就需要从 I/O 来入手来辅助判断目前的系统瓶颈点。

### 从监控定位 I/O 问题

最快速的定位手段是从监控来查看整体的 I/O 情况，可以从集群部署工具 (TiUP) 默认会部署的监控组件 Grafana 来查看对应的 I/O 监控，跟 I/O 相关的 Dashboard 有 `Overview`，`Node_exporter`，`Disk-Performance`。

#### 第一类面板

在 `Overview` > `System Info` > `IO Util` 中，可以看到集群中每个机器的 I/O 情况，该指标和 Linux iostat 监控中的 util 类似，百分比越高代表磁盘 I/O 占用越高：

- 如果监控中只有一台机器的 I/O 高，那么可以辅助判断当前有读写热点。
- 如果监控中大部分机器的 I/O 都高，那么集群现在有高 I/O 负载存在。

如果发现某台机器的 I/O 比较高，可以从监控 `Disk-Performance Dashboard` 进一步观察 I/O 的使用情况，结合 `Disk Latency`，`Disk Load` 等 metric 判断是否存在异常，必要时可以使用 fio 工具对磁盘进行检测。

#### 第二类面板

TiDB 集群主要的持久化组件是 TiKV 集群，一个 TiKV 包含两个 RocksDB 实例：一个用于存储 Raft 日志，位于 data/raft，一个用于存储真正的数据，位于 data/db。

在 `TiKV-Details` > `Raft IO` 中，可以看到这两个实例磁盘写入的相关 metric：

- `Append log duration`：该监控表明了存储 Raft 日志的 RocksDB 写入的响应时间，.99 响应应该在 50ms 以内。
- `Apply log duration`：该监控表明了存储真正数据的 RocksDB 写入的响应时间，.99 响应应该在 100ms 以内。

这两个监控还有 `.. per server` 的监控面板来提供辅助查看热点写入的情况。

#### 第三类面板

在 `TiKV-Details` > `Storage` 中，有关于 storage 相关情况的监控：

- `Storage command total`：收到的不同命令的个数。
- `Storage async write duration`：包括了磁盘 sync duration 等监控项，可能和 Raft IO 有关。如遇到异常情况，需要通过 log 来检查相关组件的工作状态是否正常。

#### 其他面板

此外，可能还需要一些其它内容来辅助确认瓶颈是否为 I/O，并可以尝试调整一些参数。通过查看 TiKV gRPC 的 prewrite/commit/raw-put（仅限 raw kv 集群）duration，确认确实是 TiKV 写入慢了。常见的几种情况如下：

- append log 慢。TiKV Grafana 的 Raft I/O 和 append log duration 比较高，通常情况下是由于写盘慢了，可以检查 RocksDB - raft 的 WAL Sync Duration max 值来确认，否则可能需要报 bug。
- raftstore 线程繁忙。TiKV grafana 的 Raft Propose/propose wait duration 明显高于 append log duration。请查看以下两点：

    - `[raftstore]` 的 `store-pool-size` 配置是否过小（该值建议在[1,5] 之间，不建议太大）。
    - 机器的 CPU 是不是不够了。

- apply log 慢。TiKV Grafana 的 Raft I/O 和 apply log duration 比较高，通常会伴随着 Raft Propose/apply wait duration 比较高。可能的情况如下：
  
    - `[raftstore]` 的 `apply-pool-size` 配置过小（建议在 [1, 5] 之间，不建议太大），Thread CPU/apply cpu 比较高；
    - 机器的 CPU 资源不够了。
    - Region 写入热点问题，单个 apply 线程 CPU 使用率比较高（通过修改 Grafana 表达式，加上 by (instance, name) 来看各个线程的 cpu 使用情况），暂时对于单个 Region 的热点写入没有很好的方式，最近在优化该场景。
    - 写 RocksDB 比较慢，RocksDB kv/max write duration 比较高（单个 Raft log 可能包含很多个 kv，写 RocksDB 的时候会把 128 个 kv 放在一个 write batch 写入到 RocksDB，所以一次 apply log 可能涉及到多次 RocksDB 的 write）。
    - 其他情况，需要报 bug。

- raft commit log 慢。TiKV Grafana 的 Raft I/O 和 commit log duration 比较高（4.x 版本的 Grafana 才有该 metric）。每个 Region 对应一个独立的 Raft group，Raft 本身是有流控机制的，类似 TCP 的滑动窗口机制，通过参数 [raftstore] raft-max-inflight-msgs = 256 来控制滑动窗口的大小，如果有热点写入并且 commit log duration 比较高可以适度调大改参数，比如 1024。

### 从 log 定位 I/O 问题

- 如果客户端报 `server is busy` 错误，特别是 `raftstore is busy` 的错误信息，会和 I/O 有相关性。

    可以通过查看监控：grafana -> TiKV -> errors 监控确认具体 busy 原因。其中，`server is busy` 是 TiKV 自身的流控机制，TiKV 通过这种方式告知 `tidb/ti-client` 当前 TiKV 的压力过大，过一会儿再尝试。

- TiKV RocksDB 日志出现 `write stall`。

    可能是 `level0 sst` 太多导致 stall。可以添加参数 `[rocksdb] max-sub-compactI/Ons = 2（或者 3）` 加快 level0 sst 往下 compact 的速度，该参数的意思是将从 level0 到 level1 的 compaction 任务最多切成 `max-sub-compactions` 个子任务交给多线程并发执行。

    如果磁盘 I/O 能力持续跟不上写入，建议扩容。如果磁盘的吞吐达到了上限（例如 SATA SSD 的吞吐相对 NVME SSD 会低很多）导致 write stall，但是 CPU 资源又比较充足，可以尝试采用压缩率更高的压缩算法来缓解磁盘的压力，用 CPU 资源换磁盘资源。
    
    比如 `default cf compaction` 压力比较大时，可以调整参数 `[rocksdb.defaultcf] compression-per-level = ["no", "no", "lz4", "lz4", "lz4", "zstd", "zstd"]` 改成 `compression-per-level = ["no", "no", "zstd", "zstd", "zstd", "zstd", "zstd"]` 。

### 从告警发现 I/O 问题

集群部署工具 (TiUP) 默认部署的告警组件，官方已经预置了相关的告警项目和阈值，I/O 相关项包括：

- TiKV_write_stall
- TiKV_raft_log_lag
- TiKV_async_request_snapshot_duration_seconds
- TiKV_async_request_write_duration_seconds
- TiKV_raft_append_log_duration_secs
- TiKV_raft_apply_log_duration_secs

## I/O 问题处理方案

1. 当确认为热点 I/O 问题的时候，需要参考 [TiDB 热点问题处理](/troubleshoot-hot-spot-issues.md)来消除相关的热点 I/O 情况。
2. 当确认整体 I/O 已经到达瓶颈的时候，且从业务侧能够判断 I/O 的能力会持续的跟不上，那么就可以利用分布式数据库的 scale 的能力，采用扩容 TiKV 节点数量的方案来获取更大的整体 I/O 吞吐量。
3. 调整上述说明中的一些参数，使用计算/内存资源来换取磁盘的存储资源。
