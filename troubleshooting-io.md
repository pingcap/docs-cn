---
title TiDB 磁盘 IO 过高
---
# TiDB 磁盘 IO 过高
作为需要持久化数据的组件，数据库在追求 IO 资源的道路上没有尽头。

随着基础工艺的不断发展，存储从 SATA 的磁盘，发展到 SATA 接口 SSD，再到 nvme 接口的 SSD，磁盘的 iops 性能，从几百向着数十万快速发展。TiDB 所使用的 TiKV 引擎，也随着时代发展的趋势，在 SSD 的数据存储优化上做着不断的努力。

当我们在使用 TiDB 数据库时，磁盘 IO 瓶颈是绕不开的问题，但同时由于线性扩展，也给了我们更多的解决方案和手段，本文会介绍我们如何定位和处理 TiDB 存储 IO 过高的问题。

## 确认当前 IO 指标 
当出现系统响应变慢的时候，根据之前的章节，如果已经排查了 cpu 的瓶颈，数据事务冲突的瓶颈后，这边就还需要从 IO 来入手来辅助判断目前的系统瓶颈点。

### 从监控定位

最快速的定位手段是从监控来查看整体的 IO 情况，可以从集群部署工具(TiDB-Ansible, TiUP) 默认会部署的监控组件 Grafana 来查看对应的 IO 监控：
#### 面板 ：
`Overview` &rarr; `System Info` &rarr; `IO Util`  中

可以看到集群中每个机器的 IO 情况，该指标和 linux iostat 监控中的 util 类似，百分比越高代表磁盘 IO 占用越高：
1. 如果监控中只有一台机器的 IO 高，那么可以辅助判断当前有读写热点
2. 如果监控中大部分机器的 IO 都高，那么集群现在是有高 IO 负载存在

TiDB 集群主要的持久化组件是 TiKV 集群，一个 TiKV 包含两个 RocksDB 实例，一个用于存储 raft 日志，位于 data/raft，一个用于存储真正的数据，位于data/db

#### 面板：
`TiKV-Details` &rarr; `Raft IO` 中，有更多的一些信息可以看到这两个实例当前的状态

- `Apply log duration`: 该监控表明了存储 raft 日志的 RocksDB 写入的响应时间，.99 响应应该在 100ms 以内。
- `Append log duration`: 该监控表明了存储真正数据的 RocksDB 写入的响应时间，.99 响应应该在 50ms 以内。

这两个监控还有 `.. per server` 的监控面板来提供辅助查看热点写入的情况。

#### 面板：
`TiKV-Details` &rarr; `Storage` 中，有关于 storage 相关情况监控

- `Storage command total`: 可以看到相关的 IO 操作次数统计
- `Storage async write duration`: 可以观察相关的磁盘 sync duration，这边应该是和 `Raft IO` 监控面板有强相关性，如果没有的话，可能需要通过 log 来检查相关组件的工作状态是否正常。

#### 同时，这边还需要配合其他的一些内容确认是否是 IO 的瓶颈，并可以尝试调整一些参数

  通过查看 TiKV gRPC 的 prewrite/commit/raw-put(仅限 raw kv 集群) duration 确认确实是 TiKV 写入慢了。下面列出集中常见的情况

- scheduler CPU 繁忙（仅限 transaction kv）。prewrite/commit 的 scheduler command duration 比 scheduler latch wait duration + storage async write duartion 更长，并且 scheduler worker CPU 比较高，例如超过 scheduler-worker-pool-size * 100% 的 80%，并且或者整个机器的 CPU 资源比较紧张。如果写入量很大，确认下是否 [storage] scheduler-worker-pool-size 配置得太小。其他情况请报 bug
- append log 慢。TiKV grafana 的 Raft IO/append log duration 比较高，通常情况下是由于写盘慢了，可以检查 RocksDB - raft 的 WAL Sync Duration max 值来确认，否则可能需要报 bug
- raftstore 线程繁忙。TiKV grafana 的 Raft Propose/propose wait duration 明显高于 append log duration。请查看
  - 1）[raftstore] store-pool-size 配置是否过小（该值建议在[1,5] 之间，不建议太大）。
  - 2）机器的 CPU 是不是不够了
- apply 慢了。TiKV grafana 的 Raft IO/apply log duration 比较高，通常会伴随着 Raft Propose/apply wait duration 比较高。可能是
  - 1） [raftstore] apply-pool-size 配置过小（建议在 [1, 5] 之间，不建议太大），Thread CPU/apply cpu 比较高；
  - 2）机器的 CPU 资源不够了；
  - 3）region 写入热点问题，单个 apply 线程 CPU 使用率比较高（通过修改 grafana 表达式，加上 by (instance, name) 来看各个线程的 cpu 使用情况），暂时对于单个 region 的热点写入没有很好的方式，最近在优化该场景；
  - 4）写 RocksDB 比较慢，RocksDB kv/max write duration 比较高（单个 raft log 可能包含很多个 kv，写 rocksdb 的时候会把 128 个 kv 放在一个 write batch 写入到 rocksdb，所以一次 apply log 可能涉及到多次 RocksDB 的 write）；
  - 5）其他情况，需要报 bug
- raft commit log 慢了。TiKV grafana 的 Raft IO/commit log duration 比较高（4.x 版本的 grafana 才有该 metric）。每个 region 对应一个独立的 raft group，raft 本身是有流控机制的，类似 TCP 的滑动窗口机制，通过参数 [raftstore] raft-max-inflight-msgs = 256 来控制滑动窗口的大小，如果有热点写入并且 commit log duration 比较高可以适度调大改参数，比如 1024

### 从 log 定位

客户端报 `server is busy` 错误。通过查看监控: grafana -> TiKV -> errors 监控确认具体 busy 原因。`server is busy` 是 TiKV 自身的流控机制，TiKV 通过这种方式告知 `tidb/ti-client` 当前 TiKV 的压力过大，等会再尝试

TiKV RocksDB 出现 `write stall`

`level0 sst` 太多导致 stall，添加参数 `[rocksdb] max-sub-compactions = 2（或者 3）` 加快 level0 sst 往下 compact 的速度，该参数的意思是将 从 level0 到 level1 的 compaction 任务最多切成 `max-sub-compactions` 个子任务交给多线程并发执行。

- `pending compaction bytes` 太多导致 stall，磁盘 IO 能力在业务高峰跟不上写入，可以通过调大对应 cf 的 `soft-pending-compaction-bytes-limit` 和 `hard-pending-compaction-bytes-limit` 参数来缓解。

- 如果 pending compaction bytes 达到该阈值，RocksDB 会放慢写入速度。默认值 64GB，`[rocksdb.defaultcf] soft-pending-compaction-bytes-limit = "128GB"`
  - 如果 pending compaction bytes 达到该阈值，RocksDB 会 stop 写入，通常不太可能触发该情况，因为在达到 soft-pending-compaction-bytes-limit 的阈值之后会放慢写入速度。默认值 256GB，`hard-pending-compaction-bytes-limit = "512GB"` 见案例 [case-275](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case275.md)；
  - 如果磁盘 IO 能力持续跟不上写入，建议扩容。如果磁盘的吞吐达到了上限（例如 SATA SSD 的吞吐相对 NVME SSD 会低很多）导致 write stall，但是 CPU 资源又比较充足，可以尝试采用压缩率更高的压缩算法来缓解磁盘的压力，用 CPU 资源换磁盘资源。
    - 比如 default cf compaction 压力比较大，调整参数 `[rocksdb.defaultcf] compression-per-level = ["no", "no", "lz4", "lz4", "lz4", "zstd", "zstd"]` 改成 `compression-per-level = ["no", "no", "zstd", "zstd", "zstd", "zstd", "zstd"]`

### 从告警获取
集群部署工具(TiDB-Ansible, TiUP) 默认部署的告警组件，官方已经预置了相关的告警项目和阈值，IO 相关包括：

- TiKV_write_stall
- TiKV_raft_log_lag
- TiKV_async_request_snapshot_duration_seconds
- TiKV_async_request_write_duration_seconds
- TiKV_raft_append_log_duration_secs
- TiKV_raft_apply_log_duration_secs

## 处理方案

1. 当确认为热点 IO 问题的时候，需要参考《热点问题处理》来消除相关的热点 IO 情况。
2. 当确认整体 IO 已经到达瓶颈的时候，且从业务侧能够判断 IO 的能力会持续的跟不上，那么就可以利用分布式数据库的 scale 的能力，采用扩容 TiKV 节点数量的方案来获取更大的整体 IO 吞吐量。
3. 调整上述说明中的一些参数，使用计算/内存资源来换取磁盘的存储资源。