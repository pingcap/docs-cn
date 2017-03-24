# TiKV 性能参数调优

本文档用于描述如何根据机器配置情况来调整 TiKV 的参数，使 TiKV 的性能达到最优。

TiKV 最底层使用的是 RocksDB 做为持久化存储，所以 TiKV 的很多性能相关的参数都是与 RocksDB 相关的。

TiKV 使用了 RocksDB 的 `Column Falimies` 特性，数据最终存储在 RocksDB 内部的 `raft`、`default`、`lock` 和 `write` 4 个 CF 内。

`raft` CF 主要存储的是 raft log，与其对应的参数位于 `[rocksdb.raftcf]` 项中；
`default` CF 存储的是真正的数据，与其对应的参数位于 `[rocksdb.defaultcf]` 项中；
`write` CF 存储的是数据的版本信息（MVCC）以及索引相关的数据，相关的参数位于 `[rocksdb.write]` 项中
`lock` CF 存储的是锁信息，系统使用默认参数。

每个 CF 都有单独的 `block-cache`，用于缓存数据块，加速 RocksDB 的读取速度，block-cache 的大小通过参数 `block-cache-size` 控制，block-cache-size 越大，能够缓存的热点数据越多，对读取操作越有利，同时占用的系统内存也会越多。

每个 CF 有各自的 `write-buffer`，大小通过 `write-buffer-size` 控制。

## 参数说明

```toml
[server]
# 监听地址
# addr = "127.0.0.1:20160"

# 数据目录
# store = "/tmp/tikv/store"

# 可以给 TiKV 实例打标签，用于副本的调度
# labels = "zone=cn-east-1,host=118"

# 日志级别，可选值为：trace，debug，info，warn，error，off
log-level = "info"

# 建议使用默认值
# notify-capacity = 40960
# message-per-tick = 4996

# socket 的发送／接收缓冲区大小
# send-buffer-size = "128KB"
# recv-buffer-size = "128KB"

# TiDB 过来的大部分读请求都会发送到 TiKV 的 coprocessor 进行处理，该参数用于设置 coprocessor 线程的个数，如果业务是读请求比较多，增加 coprocessor 的线程数，但应比系统的 CPU 核数小。例如：TiKV 所在的机器有 32 core，在重读的场景下甚至可以将该参数设置为 30。在没有设置该参数的情况下，TiKV 会自动将该值设置为 CPU 总核数乘以 0.8。
# end-point-concurrency = 8

[metric]
# 将 metrics 推送给 Prometheus pushgateway 的时间间隔
interval = "15s"
# Prometheus pushgateway 的地址
address = ""
job = "TiKV"

[raftstore]
region-max-size = "80MB"
# region 分裂阈值
region-split-size = "64MB"
# 当 region 写入的数据量超过该阈值的时候，TiKV 会检查该 region 是否需要分裂。为了减少检查过程中扫描数据的成本，数据过程中可以将该值设置为32MB，正常运行状态下使用默认值即可。
region-split-check-diff = "8MB"

[pd]
# pd 的地址
# endpoints = "127.0.0.1:2379"

[rocksdb]
# RocksDB 进行 compaction 的最大线程数。具体 RocksDB 为什么需要进行 compaction，请参考 RocksDB 的相关资料。在写流量比较大的时候（例如导数据），建议开启更多的 compaction 线程，但应小于CPU的核数。例如在导数据的时候，32 核 CPU 的机器，可以把 max-background-compactions 和 max-background-flushes 设置成 28。
max-background-compactions = 6
max-background-flushes = 2

# RocksDB 能够打开的最大文件句柄数。
# max-open-files = 40960

# RocksDB MANIFEST 文件的大小限制. # 更详细的信息请参考：https://github.com/facebook/rocksdb/wiki/MANIFEST
max-manifest-file-size = "20MB"

# RocksDB write-ahead logs 目录。如果机器上有两块盘，可以将 RocksDB 的数据和 WAL 日志放在不同的盘上，提高 TiKV 的性能。
# wal-dir = "/tmp/tikv/store"

# 下面两个参数用于怎样处理 RocksDB 归档 WAL。
# 更多详细信息请参考：https://github.com/facebook/rocksdb/wiki/How-to-persist-in-memory-RocksDB-database
# wal-ttl-seconds = 0
# wal-size-limit = 0

# RocksDB WAL 日志的最大总大小，通常情况下使用默认值就可以了。
# max-total-wal-size = "4GB"

# 可以通过该参数打开或者关闭 RocksDB 的统计信息。
# enable-statistics = true

# 开启 RocksDB compaction 过程中的预读功能，如果使用的是机械磁盘，建议该值至少为2MB。
# compaction-readahead-size = "2MB"

[rocksdb.defaultcf]
# 数据块大小。RocksDB 是按照 block 为单元对数据进行压缩的，同时 block 也是缓存在 block-cache 中的最小单元（类似其他数据库的 page 概念）。
block-size = "64KB"
# RocksDB 每一层数据的压缩方式，可选的值为：no,snappy,zlib,bzip2,lz4,lz4hc。
# no:no:lz4:lz4:lz4:lz4:lz4 表示 level0 和 level1 不压缩，level2 到 level6 采用 lz4 压缩算法。
# no 表示没有压缩，lz4 是速度和压缩比较为中庸的压缩算法，zlib 的压缩比很高，对存储空间比较友好，但是压缩速度比较慢，压缩的时候需要占用较多的 CPU 资源。不同的机器需要根据 CPU 以及 IO 资源情况来配置怎样的压缩方式。例如：如果采用的压缩方式为"no:no:lz4:lz4:lz4:lz4:lz4"，在大量写入数据的情况下（导数据），发现系统的 IO 压力很大（使用 iostat 发现 %util 持续 100% 或者使用 top 命令发现 iowait 特别多），而 CPU 的资源还比较充裕，这个时候可以考虑将 level0 和 level1 开启压缩，用 CPU 资源换取 IO 资源。如果采用的压缩方式为"no:no:lz4:lz4:lz4:lz4:lz4"，在大量写入数据的情况下，发现系统的 IO 压力不大，但是 CPU 资源已经吃光了，top -H 发现有大量的 bg 开头的线程（RocksDB 的 compaction 线程）在运行，这个时候可以考虑用 IO 资源换取 CPU 资源，将压缩方式改成"no:no:no:lz4:lz4:lz4:lz4"。总之，目的是为了最大限度地利用系统的现有资源，使 TiKV 的性能在现有的资源情况下充分发挥。
compression-per-level = "no:no:lz4:lz4:lz4:lz4:lz4"
# RocksDB memtable 的大小。
write-buffer-size = "128MB"
# 最多允许几个 memtable 存在。写入到 RocksDB 的数据首先会记录到 WAL 日志里面，然后会插入到 memtable 里面，当 memtable 的大小到达了 write-buffer-size 限定的大小的时候，当前的 memtable 会变成只读的，然后生成一个新的 memtable 接收新的写入。只读的 memtable 会被 RocksDB 的 flush 线程（max-background-flushes 参数能够控制 flush 线程的最大个数） flush 到磁盘，成为 level0 的一个 sst 文件。当 flush 线程忙不过来，导致等待 flush 到磁盘的 memtable 的数量到达 max-write-buffer-number 限定的个数的时候，RocksDB 会将新的写入 stall 住，stall 是 RocksDB 的一种流控机制。在导数据的时候可以将 max-write-buffer-number 的值设置的更大一点，例如 10。
max-write-buffer-number = 5

# 当 level0 的 sst 文件个数到达 level0-slowdown-writes-trigger 指定的限度的时候，RocksDB 会尝试减慢写入的速度。因为 level0 的 sst 太多会导致 RocksDB 的读放大上升。level0-slowdown-writes-trigger 和 level0-stop-writes-trigger 是 RocksDB 进行流控的另一个表现。当 level0 的 sst 的文件个数到达 4（默认值），level0 的 sst 文件会和 level1 中有 overlap 的 sst 文件进行 compaction，缓解读放大的问题。
level0-slowdown-writes-trigger = 20
# 当 level0 的 sst 文件个数到达 level0-stop-writes-trigger 指定的限度的时候，RocksDB 会stall 住新的写入。
level0-stop-writes-trigger = 36
# 当 level1 的数据量大小达到 max-bytes-for-level-base 限定的值的时候，会触发 level1 的 sst 和 level2 种有 overlap 的 sst 进行 compaction。
# 黄金定律：max-bytes-for-level-base 的设置的第一参考原则就是保证和 level0 的数据量大致相等，这样能够减少不必要的 compaction。例如压缩方式为"no:no:lz4:lz4:lz4:lz4:lz4"，那么 max-bytes-for-level-base 的值应该是 write-buffer-size 的大小乘以 4，因为 level0 和 level1 都没有压缩，而且 level0 触发 compaction 的条件是 sst 的个数到达 4（默认值）。在 level0 和 level1 都采取了压缩的情况下，就需要分析下 RocksDB 的日志，看一个 memtable 的压缩成一个 sst 文件的大小大概是多少，例如 32MB，那么 max-bytes-for-level-base 的建议值就应该是 32MB * 4 = 128MB。
max-bytes-for-level-base = "512MB"
# sst 文件的大小。level0 的 sst 文件的大小受 write-buffer-size 和 level0 采用的压缩算法的影响，target-file-size-base 参数用于控制 level1-level6 单个 sst 文件的大小。
target-file-size-base = "32MB"
# 在不配置该参数的情况下，TiKV 会将该值设置为系统总内存量的 40%。如果需要在单个物理机上部署多个 TiKV 节点，需要显式配置该参数，否则 TiKV 容易出现 OOM 的问题。
# block-cache-size = "1GB"

[rocksdb.writecf]
compression-per-level = "no:no:lz4:lz4:lz4:lz4:lz4"
write-buffer-size = "128MB"
max-write-buffer-number = 5
min-write-buffer-number-to-merge = 1
max-bytes-for-level-base = "512MB"
target-file-size-base = "32MB"
# 在不配置该参数的情况下，TiKV 会将该值设置为系统总内存量的 15%。如果需要在单个物理机上部署多个 TiKV 节点，需要显式配置该参数。版本信息（MVCC）相关的数据以及索引相关的数据都记录在 write 这个 cf 里面，如果业务的场景下单表索引较多，可以将该参数设置的更大一点。
# block-cache-size = "256MB"

[rocksdb.raftcf]
compression-per-level = "no:no:lz4:lz4:lz4:lz4:lz4"
write-buffer-size = "128MB"
max-write-buffer-number = 5
min-write-buffer-number-to-merge = 1
max-bytes-for-level-base = "512MB"
target-file-size-base = "32MB"
# 通常配置在 256MB 到 2GB 之间，通常情况下使用默认值就可以了，但如果系统资源比较充足可以适当调大点。
block-cache-size = "256MB"

[storage]
# 通常情况下使用默认值就可以了。在导数据的情况下建议将改参数设置为 1024000。
# scheduler-concurrency = 102400
# 该参数控制写入线程的个数，当写入操作比较频繁的时候，需要把该参数调大。使用 top -H -p tikv-pid 发现名称为 sched-worker-pool 的线程都特别忙，这个时候就需要将 scheduler-worker-pool-size 参数调大，增加写线程的个数。
# scheduler-worker-pool-size = 4
```
## TiKV 内存使用情况

除了以上列出的 `block-cache` 以及 `write-buffer` 会占用系统内存外：

1）需预留一些内存作为系统的 page cache;

2）TiKV 在处理大的查询的时候（例如 `select * from ...`）会读取数据然后在内存中生成对应的数据结构返回给 TiDB，这个过程中 TiKV 会占用一部分内存。


## TiKV 机器配置推荐

1）生产环境中，不建议将 TiKV 部署在 CPU 核数小于 8 或内存低于 32GB 的机器上。

2）如果对写入吞吐要求比较高，建议使用吞吐能力比较好的磁盘。

3）如果对读写的延迟要求非常高，建议使用 IOPS 比较高的 SSD 盘。


