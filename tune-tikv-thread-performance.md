---
title: TiKV 线程池性能调优
summary: 了解 TiKV 线程池性能调优。
aliases: ['/docs-cn/dev/tune-tikv-thread-performance/']
---

# TiKV 线程池性能调优

本文主要介绍 TiKV 线程池性能调优的主要手段，以及 TiKV 内部线程池的主要用途。

## 线程池介绍

在 TiKV 中，线程池主要由 gRPC、Scheduler、UnifyReadPool、Raftstore、Apply、RocksDB 以及其它一些占用 CPU 不多的定时任务与检测组件组成，这里主要介绍几个占用 CPU 比较多且会对用户读写请求的性能产生影响的线程池。

* gRPC 线程池：负责处理所有网络请求，它会把不同任务类型的请求转发给不同的线程池。
* Scheduler 线程池：负责检测写事务冲突，把事务的两阶段提交、悲观锁上锁、事务回滚等请求转化为 key-value 对数组，然后交给 Raftstore 线程进行 Raft 日志复制。
* Raftstore 线程池：负责处理所有的 Raft 消息以及添加新日志的提议 (Propose)、将日志写入到磁盘，当日志在多数副本中达成一致后，它就会把该日志发送给 Apply 线程。
* Apply 线程池：当收到从 Raftstore 线程池发来的已提交日志后，负责将其解析为 key-value 请求，然后写入 RocksDB 并且调用回调函数通知 gRPC 线程池中的写请求完成，返回结果给客户端。
* RocksDB 线程池：RocksDB 进行 Compact 和 Flush 任务的线程池，关于 RocksDB 的架构与 Compact 操作请参考 [RocksDB: A Persistent Key-Value Store for Flash and RAM Storage](https://github.com/facebook/rocksdb)。
* UnifyReadPool 线程池：由 Coprocessor 线程池与 Storage Read Pool 合并而来，所有的读取请求包括 kv get、kv batch get、raw kv get、coprocessor 等都会在这个线程池中执行。

## TiKV 的只读请求

TiKV 的读取请求分为两类：

- 一类是指定查询某一行或者某几行的简单查询，这类查询会运行在 Storage Read Pool 中。
- 另一类是复杂的聚合计算、范围查询，这类请求会运行在 Coprocessor Read Pool 中。

从 TiKV 5.0 版本起，默认所有的读取请求都通过统一的线程池进行查询。如果是从 TiKV 4.0 升级上来的 TiKV 集群且升级前未打开 `readpool.storage` 的 `use-unified-pool` 配置，则升级后所有的读取请求仍然继续使用独立的线程池进行查询，可以将 `readpool.storage.use-unified-pool` 设置为 `true` 使所有的读取请求通过统一的线程池进行查询。

## TiKV 线程池调优

* gRPC 线程池的大小默认配置 (`server.grpc-concurrency`) 是 4。由于 gRPC 线程池几乎不会有多少计算开销，它主要负责网络 IO、反序列化请求，因此该配置通常不需要调整。

    - 如果部署的机器 CPU 核数特别少（小于等于 8），可以考虑将该配置 (`server.grpc-concurrency`) 设置为 2。
    - 如果机器配置很高，并且 TiKV 承担了非常大量的读写请求，观察到 Grafana 上的监控 Thread CPU 的 gRPC poll CPU 的数值超过了 server.grpc-concurrency 大小的 80%，那么可以考虑适当调大 `server.grpc-concurrency` 以控制该线程池使用率在 80% 以下（即 Grafana 上的指标低于 `80% * server.grpc-concurrency` 的值）。

* Scheduler 线程池的大小配置 (`storage.scheduler-worker-pool-size`) 在 TiKV 检测到机器 CPU 核数大于等于 16 时默认为 8，小于 16 时默认为 4。它主要用于将复杂的事务请求转化为简单的 key-value 读写。但是 **scheduler 线程池本身不进行任何写操作**。

    - 如果检测到有事务冲突，那么它会提前返回冲突结果给客户端。
    - 如果未检测到事务冲突，那么它会把需要写入的 key-value 合并成一条 Raft 日志交给 Raftstore 线程进行 Raft 日志复制。
    
    通常来说为了避免过多的线程切换，最好确保 scheduler 线程池的利用率保持在 50%～75% 之间。（如果线程池大小为 8 的话，那么 Grafana 上的 TiKV-Details.Thread CPU.scheduler worker CPU 应当在 400%～600% 之间较为合理）

* Raftstore 线程池是 TiKV 最为复杂的一个线程池，默认大小 (`raftstore.store-pool-size`)为 2，所有的写请求都会先在 Raftstore 线程 fsync 的方式写入 RocksDB（除非手动将 `raftstore.sync-log` 设置为 false；而 `raftstore.sync-log` 设置为 false，可以提升一部分写性能，但也会增加在机器故障时数据丢失的风险）。

    由于存在 I/O，Raftstore 线程理论上不可能达到 100% 的 CPU。为了尽可能地减少写磁盘次数，将多个写请求攒在一起写入 RocksDB，最好控制其整体 CPU 使用在 60% 以下（按照线程数默认值 2，则 Grafana 监控上的 TiKV-Details.Thread CPU.Raft store CPU 上的数值控制在 120% 以内较为合理）。不要为了提升写性能盲目增大 Raftstore 线程池大小，这样可能会适得其反，增加了磁盘负担让性能变差。

* UnifyReadPool 负责处理所有的读取请求。默认配置 (`readpool.unified.max-thread-count`)大小为机器 CPU 数的 80% （如机器为 16 核，则默认线程池大小为 12）。

    通常建议根据业务负载特性调整其 CPU 使用率在线程池大小的 60%～90% 之间（如果用户 Grafana 上 TiKV-Details.Thread CPU.Unified read pool CPU 的峰值不超过 800%，那么建议用户将 `readpool.unified.max-thread-count` 设置为 10，过多的线程数会造成更频繁的线程切换，并且抢占其他线程池的资源）。

* RocksDB 线程池是 RocksDB 进行 Compact 和 Flush 任务的线程池，通常不需要配置。

    * 如果机器 CPU 核数较少，可将 `rocksdb.max-background-jobs` 与 `raftdb.max-background-jobs` 同时设置为 4。
    * 如果遇到了 Write Stall，可查看 Grafana 监控上 **RocksDB-kv** 中的 Write Stall Reason 有哪些指标不为 0。
        * 如果是由 pending compaction bytes 相关原因引起的，可将 `rocksdb.max-sub-compactions` 设置为 2 或者 3（该配置表示单次 compaction job 允许使用的子线程数量，TiKV 4.0 版本默认值为 3，3.0 版本默认值为 1）。
        * 如果原因是 memtable count 相关，建议调大所有列的 `max-write-buffer-number`（默认为 5）。
        * 如果原因是 level0 file limit 相关，建议调大如下参数为 64 或者更高：

            ```
            rocksdb.defaultcf.level0-slowdown-writes-trigger
            rocksdb.writecf.level0-slowdown-writes-trigger
            rocksdb.lockcf.level0-slowdown-writes-trigger
            rocksdb.defaultcf.level0-stop-writes-trigger
            rocksdb.writecf.level0-stop-writes-trigger
            rocksdb.lockcf.level0-stop-writes-trigger
            ```
