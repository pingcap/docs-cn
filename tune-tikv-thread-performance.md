---
title: Tune TiKV Thread Pool Performance
summary: Learn how to tune TiKV thread pools for optimal performance.
aliases: ['/docs/dev/tune-tikv-thread-performance/']
---

# Tune TiKV Thread Pool Performance

This document introduces TiKV internal thread pools and how to tune their performance.

## Thread pool introduction

The TiKV thread pool is mainly composed of gRPC, Scheduler, UnifyReadPool, Raftstore, Apply, RocksDB, and some scheduled tasks and detection components that do not consume much CPU. This document mainly introduces a few CPU-intensive thread pools that affect the performance of read and write requests.

* The gRPC thread pool: it handles all network requests and forwards requests of different task types to different thread pools.

* The Scheduler thread pool: it detects write transaction conflicts, converts requests like the two-phase commit, pessimistic locking, and transaction rollbacks into key-value pair arrays, and then sends them to the Raftstore thread for Raft log replication.

* The Raftstore thread pool: it processes all Raft messages and the proposal to add a new log, and writing the log to a disk. When the logs in the majority of replicas are consistent, this thread pool sends the log to the Apply thread.

* The Apply thread pool: it receives the submitted log sent from the Raftstore thread pool, parses it as a key-value request, then writes it to RocksDB, calls the callback function to notify the gRPC thread pool that the write request is complete, and returns the result to the client.

* The RocksDB thread pool: it is a thread pool for RocksDB to compact and flush tasks. For RocksDB's architecture and `Compact` operation, refer to [RocksDB: A Persistent Key-Value Store for Flash and RAM Storage](https://github.com/facebook/rocksdb).

* The UnifyReadPool thread pool: it is a combination of the Coprocessor thread pool and Storage Read Pool. All read requests such as kv get, kv batch get, raw kv get, and coprocessor are executed in this thread pool.

## TiKV read-only requests

TiKV's read requests are divided into the following types:

- Simple queries that specify a certain row or several rows, running in the Storage Read Pool.
- Complex aggregate calculation and range queries, running in the Coprocessor Read Pool.

Starting from TiKV v5.0, all read requests use the unified thread pool for queries by default. If your TiKV cluster is upgraded from TiKV v4.0 and the `use-unified-pool` configuration of `readpool.storage` was set to `false` before the upgrade, all read requests continue using different thread pools after the upgrade. In this scenario, to make all read requests use the unified thread pool for queries, you can set the value of `readpool.storage.use-unified-pool` to `true`.

## Performance tuning for TiKV thread pools

* The gRPC thread pool.

    The default size (configured by `server.grpc-concurrency`) of the gRPC thread pool is `5`. This thread pool has almost no computing overhead and is mainly responsible for network I/O and deserialization requests, so generally you do not need to adjust the default configuration.

    - If the machine deployed with TiKV has a small number (less than or equal to 8) of CPU cores, consider setting the `server.grpc-concurrency` configuration item to `2`.
    - If the machine deployed with TiKV has very high configuration, TiKV undertakes a large number of read and write requests, and the value of `gRPC poll CPU` that monitors Thread CPU on Grafana exceeds 80% of `server.grpc-concurrency`, then consider increasing the value of `server.grpc-concurrency` to keep the thread pool usage rate below 80% (that is, the metric on Grafana is lower than `80% * server.grpc-concurrency`).

* The Scheduler thread pool.

    When TiKV detects that the number of machine CPU cores is larger than or equal to 16, the default size (configured by `storage.scheduler-worker-pool-size`) of the Scheduler thread pool is `8`; when TiKV detects that the number of machine CPU cores is smaller than 16, the default size is `4`.

    This thread pool is mainly used to convert complex transaction requests into simple key-value read and write requests. However, **the Scheduler thread pool itself does not perform any write operation**.

    - If it detects a transaction conflict, then this thread pool returns the conflict result to the client in advance.
    - If no conflict is detected, then this thread pool merges the key-value requests that perform write operations into a Raft log and sends it to the Raftstore thread for Raft log replication.

    Generally speaking, to avoid excessive thread switching, it is best to ensure that the utilization rate of the Scheduler thread pool is between 50% and 75%. If the thread pool size is `8`, then it is recommended to keep `TiKV-Details.Thread CPU.scheduler worker CPU` on Grafana between 400% and 600%.

* The Raftstore thread pool.

    The Raftstore thread pool is the most complex thread pool in TiKV. The default size (configured by `raftstore.store-pool-size`) is `2`. All write requests are written into RocksDB in the way of `fsync` from the Raftstore thread, unless you manually set `raftstore.sync-log` to `false`. Setting `raftstore.sync-log` to `false` improves write performance to a certain degree, but increases the risk of data loss in the case of machine failure).

    Due to I/O, Raftstore threads cannot reach 100% CPU usage theoretically. To reduce disk writes as much as possible, you can put together multiple write requests and write them to RocksDB. It is recommended to keep the overall CPU usage below 60% (If the default number of threads is `2`, it is recommended to keep `TiKV-Details.Thread CPU.Raft store CPU` on Grafana within 120%). Do not increase the size of the Raftstore thread pool to improve write performance without thinking, because this might increase the disk burden and degrade performance.

* The UnifyReadPool thread pool.

    The UnifyReadPool is responsible for handling all read requests. The default size (configured by `readpool.unified.max-thread-count`) is 80% of the number of the machine's CPU cores. For example, if the machine CPU has 16 cores, the default thread pool size is 12. It is recommended to adjust the CPU usage rate according to the application workloads and keep it between 60% and 90% of the thread pool size.

    If the peak value of the `TiKV-Details.Thread CPU.Unified read pool CPU` on Grafana does not exceed 800%, then it is recommended to set `readpool.unified.max-thread-count` to `10`. Too many threads can cause more frequent thread switching, and take up resources of other thread pools.

* The RocksDB thread pool.

    The RocksDB thread pool is a thread pool for RocksDB to compact and flush tasks. Usually, you do not need to configure it.

    * If the machine has a small number of CPU cores, set both `rocksdb.max-background-jobs` and `raftdb.max-background-jobs` to `4`.
    * If you encounter write stall, go to Write Stall Reason in **RocksDB-kv** on Grafana and check on the metrics that are not `0`.

        * If it is caused by reasons related to pending compaction bytes, set `rocksdb.max-sub-compactions` to `2` or `3`. This configuration item indicates the number of sub-threads allowed for a single compaction job. Its default value is `3` in TiKV 4.0 and `1` in TiKV 3.0.
        * If the reason is related to memtable count, it is recommended to increase the `max-write-buffer-number` of all columns (`5` by default).
        * If the reason is related to the level0 file limit, it is recommended to increase values of the following parameters to `64` or a larger number:

            ```
            rocksdb.defaultcf.level0-slowdown-writes-trigger
            rocksdb.writecf.level0-slowdown-writes-trigger
            rocksdb.lockcf.level0-slowdown-writes-trigger
            rocksdb.defaultcf.level0-stop-writes-trigger
            rocksdb.writecf.level0-stop-writes-trigger
            rocksdb.lockcf.level0-stop-writes-trigger
            ```
