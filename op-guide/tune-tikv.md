---
title: TiKV 性能参数调优
category: advanced
---

# TiKV 性能参数调优

本文档用于描述如何根据机器配置情况来调整 TiKV 的参数，使 TiKV 的性能达到最优。

TiKV 最底层使用的是 RocksDB 做为持久化存储，所以 TiKV 的很多性能相关的参数都是与 RocksDB 相关的。TiKV 使用了两个 RocksDB 实例，默认 RocksDB 实例存储 KV 数据，Raft RocksDB 实例（简称 RaftDB）存储 Raft 数据。

TiKV 使用了 RocksDB 的 `Column Families` (CF) 特性。

- 默认 RocksDB 实例将 KV 数据存储在内部的 `default`、`write` 和 `lock` 3 个 CF 内。

    - `default` CF 存储的是真正的数据，与其对应的参数位于 `[rocksdb.defaultcf]` 项中；
    - `write` CF 存储的是数据的版本信息 (MVCC) 以及索引相关的数据，相关的参数位于 `[rocksdb.writecf]` 项中；
    - `lock` CF 存储的是锁信息，系统使用默认参数。

- Raft RocksDB 实例存储 Raft log。
    
    - `default` CF 主要存储的是 Raft log，与其对应的参数位于 `[raftdb.defaultcf]` 项中。

默认情况下，所有的 CF 共同使用一个 block cache 实例。通过在 `[storage.block-cache]` 下设置 `capacity` 参数，你可以配置该 block cache 的大小。block cache 越大，能够缓存的热点数据越多，读取数据越容易，同时占用的系统内存也越多。如果要为每个 CF 使用单独的 block cache 实例，需要在 `[storage.block-cache]` 下设置 `shared = false`，并为每个 CF 配置单独的 block cache 大小。例如，可以在 `[rocksdb.writecf]` 下设置 `block-cache-size` 参数来配置 `write` CF 的大小。

每个 CF 有各自的 `write-buffer`，大小通过 `write-buffer-size` 控制。

## 参数说明

```toml
# 日志级别，可选值为：trace，debug，info，warn，error，off
log-level = "info"

[server]
# 监听地址
# addr = "127.0.0.1:20160"

# gRPC 线程池大小
# grpc-concurrency = 4
# TiKV 每个实例之间的 gRPC 连接数
# grpc-raft-conn-num = 10

# TiDB 过来的大部分读请求都会发送到 TiKV 的 Coprocessor 进行处理，该参数用于设置
# coprocessor 线程的个数，如果业务是读请求比较多，增加 coprocessor 的线程数，但应比系统的
# CPU 核数小。例如：TiKV 所在的机器有 32 core，在重读的场景下甚至可以将该参数设置为 30。在没有
# 设置该参数的情况下，TiKV 会自动将该值设置为 CPU 总核数乘以 0.8。
# end-point-concurrency = 8

# 可以给 TiKV 实例打标签，用于副本的调度
# labels = {zone = "cn-east-1", host = "118", disk = "ssd"}

[storage]
# 数据目录
# data-dir = "/tmp/tikv/store"

# 通常情况下使用默认值就可以了。在导数据的情况下建议将该参数设置为 1024000。
# scheduler-concurrency = 102400
# 该参数控制写入线程的个数，当写入操作比较频繁的时候，需要把该参数调大。使用 top -H -p tikv-pid
# 发现名称为 sched-worker-pool 的线程都特别忙，这个时候就需要将 scheduler-worker-pool-size
# 参数调大，增加写线程的个数。
# scheduler-worker-pool-size = 4

[storage.block-cache]
## 是否为 RocksDB 的所有 CF 都创建一个 shared block cache。
##
## RocksDB 使用 block cache 来缓存未压缩的数据块。较大的 block cache 可以加快读取速度。
## 推荐开启 `shared block cache` 参数。这样只需要设置全部缓存大小，使配置过程更加方便。
## 在大多数情况下，可以通过 LRU 算法在各 CF 间自动平衡缓存用量。
##
## `storage.block-cache` 会话中的其余配置仅在开启 `shared block cache` 时起作用。
# shared = true
## shared block cache 的大小。正常情况下应设置为系统全部内存的 30%-50%。
## 如果未设置该参数，则由以下字段或其默认值的总和决定。
##
##   * rocksdb.defaultcf.block-cache-size 或系统全部内存的 25%
##   * rocksdb.writecf.block-cache-size 或系统全部内存的 15% 
##   * rocksdb.lockcf.block-cache-size 或系统全部内存的 2% 
##   * raftdb.defaultcf.block-cache-size 或系统全部内存的 2% 
##
## 要在单个物理机上部署多个 TiKV 节点，需要显式配置该参数。
## 否则，TiKV 中可能会出现 OOM 错误。
# capacity = "1GB"

[pd]
# pd 的地址
# endpoints = ["127.0.0.1:2379","127.0.0.2:2379","127.0.0.3:2379"]

[metric]
# 将 metrics 推送给 Prometheus pushgateway 的时间间隔
interval = "15s"
# Prometheus pushgateway 的地址
address = ""
job = "tikv"

[raftstore]
# 默认为 true，表示强制将数据刷到磁盘上。如果是非金融安全级别的业务场景，建议设置成 false，
# 以便获得更高的性能。
sync-log = true

# Raft RocksDB 目录。默认值是 [storage.data-dir] 的 raft 子目录。
# 如果机器上有多块磁盘，可以将 Raft RocksDB 的数据放在不同的盘上，提高 TiKV 的性能。
# raftdb-dir = "/tmp/tikv/store/raft"

region-max-size = "384MB"
# Region 分裂阈值
region-split-size = "256MB"
# 当 Region 写入的数据量超过该阈值的时候，TiKV 会检查该 Region 是否需要分裂。为了减少检查过程
# 中扫描数据的成本，数据过程中可以将该值设置为32MB，正常运行状态下使用默认值即可。
region-split-check-diff = "32MB"

[rocksdb]
# RocksDB 进行后台任务的最大线程数，后台任务包括 compaction 和 flush。具体 RocksDB 为什么需要进行 compaction，
# 请参考 RocksDB 的相关资料。在写流量比较大的时候（例如导数据），建议开启更多的线程，
# 但应小于 CPU 的核数。例如在导数据的时候，32 核 CPU 的机器，可以设置成 28。
# max-background-jobs = 8

# RocksDB 能够打开的最大文件句柄数。
# max-open-files = 40960

# RocksDB MANIFEST 文件的大小限制. # 更详细的信息请参考：https://github.com/facebook/rocksdb/wiki/MANIFEST
max-manifest-file-size = "20MB"

# RocksDB write-ahead logs 目录。如果机器上有两块盘，可以将 RocksDB 的数据和 WAL 日志放在
# 不同的盘上，提高 TiKV 的性能。
# wal-dir = "/tmp/tikv/store"

# 下面两个参数用于怎样处理 RocksDB 归档 WAL。
# 更多详细信息请参考：https://github.com/facebook/rocksdb/wiki/How-to-persist-in-memory-RocksDB-database%3F
# wal-ttl-seconds = 0
# wal-size-limit = 0

# RocksDB WAL 日志的最大总大小，通常情况下使用默认值就可以了。
# max-total-wal-size = "4GB"

# 可以通过该参数打开或者关闭 RocksDB 的统计信息。
# enable-statistics = true

# 开启 RocksDB compaction 过程中的预读功能，如果使用的是机械磁盘，建议该值至少为2MB。
# compaction-readahead-size = "2MB"

[rocksdb.defaultcf]
# 数据块大小。RocksDB 是按照 block 为单元对数据进行压缩的，同时 block 也是缓存在 block-cache
# 中的最小单元（类似其他数据库的 page 概念）。
block-size = "64KB"

# RocksDB 每一层数据的压缩方式，可选的值为：no,snappy,zlib,bzip2,lz4,lz4hc,zstd。
# no:no:lz4:lz4:lz4:zstd:zstd 表示 level0 和 level1 不压缩，level2 到 level4 采用 lz4 压缩算法,
# level5 和 level6 采用 zstd 压缩算法,。
# no 表示没有压缩，lz4 是速度和压缩比较为中庸的压缩算法，zlib 的压缩比很高，对存储空间比较友
# 好，但是压缩速度比较慢，压缩的时候需要占用较多的 CPU 资源。不同的机器需要根据 CPU 以及 I/O 资
# 源情况来配置怎样的压缩方式。例如：如果采用的压缩方式为"no:no:lz4:lz4:lz4:zstd:zstd"，在大量
# 写入数据的情况下（导数据），发现系统的 I/O 压力很大（使用 iostat 发现 %util 持续 100% 或者使
# 用 top 命令发现 iowait 特别多），而 CPU 的资源还比较充裕，这个时候可以考虑将 level0 和
# level1 开启压缩，用 CPU 资源换取 I/O 资源。如果采用的压缩方式
# 为"no:no:lz4:lz4:lz4:zstd:zstd"，在大量写入数据的情况下，发现系统的 I/O 压力不大，但是 CPU
# 资源已经吃光了，top -H 发现有大量的 bg 开头的线程（RocksDB 的 compaction 线程）在运行，这
# 个时候可以考虑用 I/O 资源换取 CPU 资源，将压缩方式改成"no:no:no:lz4:lz4:zstd:zstd"。总之，目
# 的是为了最大限度地利用系统的现有资源，使 TiKV 的性能在现有的资源情况下充分发挥。
compression-per-level = ["no", "no", "lz4", "lz4", "lz4", "zstd", "zstd"]

# RocksDB memtable 的大小。
write-buffer-size = "128MB"

# 最多允许几个 memtable 存在。写入到 RocksDB 的数据首先会记录到 WAL 日志里面，然后会插入到
# memtable 里面，当 memtable 的大小到达了 write-buffer-size 限定的大小的时候，当前的
# memtable 会变成只读的，然后生成一个新的 memtable 接收新的写入。只读的 memtable 会被
# RocksDB 的 flush 线程（max-background-flushes 参数能够控制 flush 线程的最大个数）
# flush 到磁盘，成为 level0 的一个 sst 文件。当 flush 线程忙不过来，导致等待 flush 到磁盘的
# memtable 的数量到达 max-write-buffer-number 限定的个数的时候，RocksDB 会将新的写入
# stall 住，stall 是 RocksDB 的一种流控机制。在导数据的时候可以将 max-write-buffer-number
# 的值设置的更大一点，例如 10。
max-write-buffer-number = 5

# 当 level0 的 sst 文件个数到达 level0-slowdown-writes-trigger 指定的限度的时候，
# RocksDB 会尝试减慢写入的速度。因为 level0 的 sst 太多会导致 RocksDB 的读放大上升。
# level0-slowdown-writes-trigger 和 level0-stop-writes-trigger 是 RocksDB 进行流控的
# 另一个表现。当 level0 的 sst 的文件个数到达 4（默认值），level0 的 sst 文件会和 level1 中
# 有 overlap 的 sst 文件进行 compaction，缓解读放大的问题。
level0-slowdown-writes-trigger = 20

# 当 level0 的 sst 文件个数到达 level0-stop-writes-trigger 指定的限度的时候，RocksDB 会
# stall 住新的写入。
level0-stop-writes-trigger = 36

# 当 level1 的数据量大小达到 max-bytes-for-level-base 限定的值的时候，会触发 level1 的
# sst 和 level2 种有 overlap 的 sst 进行 compaction。
# 黄金定律：max-bytes-for-level-base 的设置的第一参考原则就是保证和 level0 的数据量大致相
# 等，这样能够减少不必要的 compaction。例如压缩方式为"no:no:lz4:lz4:lz4:lz4:lz4"，那么
# max-bytes-for-level-base 的值应该是 write-buffer-size 的大小乘以 4，因为 level0 和
# level1 都没有压缩，而且 level0 触发 compaction 的条件是 sst 的个数到达 4（默认值）。在
# level0 和 level1 都采取了压缩的情况下，就需要分析下 RocksDB 的日志，看一个 memtable 的压
# 缩成一个 sst 文件的大小大概是多少，例如 32MB，那么 max-bytes-for-level-base 的建议值就应
# 该是 32MB * 4 = 128MB。
max-bytes-for-level-base = "512MB"

# sst 文件的大小。level0 的 sst 文件的大小受 write-buffer-size 和 level0 采用的压缩算法的
# 影响，target-file-size-base 参数用于控制 level1-level6 单个 sst 文件的大小。
target-file-size-base = "32MB"

[rocksdb.writecf]
# 保持和 rocksdb.defaultcf.compression-per-level 一致。
compression-per-level = ["no", "no", "lz4", "lz4", "lz4", "zstd", "zstd"]

# 保持和 rocksdb.defaultcf.write-buffer-size 一致。
write-buffer-size = "128MB"
max-write-buffer-number = 5
min-write-buffer-number-to-merge = 1

# 保持和 rocksdb.defaultcf.max-bytes-for-level-base 一致。
max-bytes-for-level-base = "512MB"
target-file-size-base = "32MB"

[raftdb]
# RaftDB 能够打开的最大文件句柄数。
# max-open-files = 40960

# 可以通过该参数打开或者关闭 RaftDB 的统计信息。
# enable-statistics = true

# 开启 RaftDB compaction 过程中的预读功能，如果使用的是机械磁盘，建议该值至少为2MB。
# compaction-readahead-size = "2MB"

[raftdb.defaultcf]
# 保持和 rocksdb.defaultcf.compression-per-level 一致。
compression-per-level = ["no", "no", "lz4", "lz4", "lz4", "zstd", "zstd"]

# 保持和 rocksdb.defaultcf.write-buffer-size 一致。
write-buffer-size = "128MB"
max-write-buffer-number = 5
min-write-buffer-number-to-merge = 1

# 保持和 rocksdb.defaultcf.max-bytes-for-level-base 一致。
max-bytes-for-level-base = "512MB"
target-file-size-base = "32MB"
```

## TiKV 内存使用情况

除了以上列出的 `block-cache` 以及 `write-buffer` 会占用系统内存外：

1.  需预留一些内存作为系统的 page cache
2.  TiKV 在处理大的查询的时候（例如 `select * from ...`）会读取数据然后在内存中生成对应的数据结构返回给 TiDB，这个过程中 TiKV 会占用一部分内存


## TiKV 机器配置推荐

1.  生产环境中，不建议将 TiKV 部署在 CPU 核数小于 8 或内存低于 32GB 的机器上
2.  如果对写入吞吐要求比较高，建议使用吞吐能力比较好的磁盘
3.  如果对读写的延迟要求非常高，建议使用 IOPS 比较高的 SSD 盘


