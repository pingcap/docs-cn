# TiKV 性能参数调优
本文档用于描述如何根据机器配置情况来调整 TiKV 的参数，使 TiKV 的性能达到最优。

TiKV 最底层使用的是 RocksDB 做为持久化存储，所以 TiKV 的很多性能相关的参数都是与 RocksDB 相关的。

TiKV 使用了 RocksDB 的 `Column Falimies` 特性，数据最终存储在 RocksDB 内部的 `raft`、`default`、`lock` 和 `write` 4 个 CF 内。

`raft` CF 主要存储的是 raft log，与其对应的参数位于 `[rocksdb.raftcf]` 项中；
`default` CF 存储的是真正的数据，与其对应的参数位于 `[rocksdb.defaultcf]` 项中；
`write` CF 存储的是数据的版本信息（MVCC），与其对应的参数位于 `[rocksdb.write]` 项中
`lock` CF 存储的是锁信息，系统使用默认参数。

每个 CF 都有单独的 `block-cache`，用于缓存数据块，加速 RocksDB 的读取速度，block-cache 的大小通过参数 `block-cache-size` 控制，block-cache-size 越大，能够缓存的热点数据越多，对读取操作越有利，同时占用的系统内存也会越多。

每个 CF 有各自的 `write-buffer`，大小通过 `write-buffer-size` 控制。

## 1.参数说明
```toml
[server]
# 通常情况下使用默认值。在复杂的查询比较多的情况下，例如 join 操作，聚合操作等等，
# 可以稍微调大点，但应比系统的 CPU 核数小。
end-point-concurrency = 8

[raftstore]
region-max-size = "80MB"
region-split-size = "64MB"
# 导数据过程中可以将该值设置为64MB，正常运行状态下使用默认值。
region-split-check-diff = "8MB"

[rocksdb]
# 通常情况下使用默认值就可以了，应小于CPU的核数。
max-background-compactions = 6
max-open-files = 40960

[rocksdb.defaultcf]
block-size = "64KB"
compression-per-level = "no:no:no:lz4:lz4:lz4:lz4"
write-buffer-size = "64MB"
max-write-buffer-number = 5
min-write-buffer-number-to-merge = 1
max-bytes-for-level-base = "256MB"
target-file-size-base = "32MB"
# 通常配置为系统内存的30-40%左右。
block-cache-size = "1GB"

[rocksdb.writecf]
compression-per-level = "no:no:no:lz4:lz4:lz4:lz4"
write-buffer-size = "64MB"
max-write-buffer-number = 5
min-write-buffer-number-to-merge = 1
max-bytes-for-level-base = "256MB"
target-file-size-base = "32MB"
# 通常为 defaultcf.block-cache-size 的 1/n。如果一行数据很大，
# n 通常比较大，如果一行数据比较短，n 比较小。n 通常在 4 到 16 之间。
block-cache-size = "256MB"

[rocksdb.raftcf]
compression-per-level = "no:no:no:lz4:lz4:lz4:lz4"
write-buffer-size = "64MB"
max-write-buffer-number = 5
min-write-buffer-number-to-merge = 1
max-bytes-for-level-base = "256MB"
target-file-size-base = "32MB"
# 通常配置在 256MB 到 2GB 之间，通常情况下使用默认值就可以了，
# 但如果系统资源比较充足可以适当调大点。
block-cache-size = "256MB"

[storage]
# 使用默认值就可以了。
scheduler-concurrency = 102400
# 通常情况下使用默认值就可以了。如果写入操作基本是批量写入的或者写入的行比较大，
# 可以适当调大点。
scheduler-worker-pool-size = 4
```
## 2.TiKV 内存使用情况

除了以上列出的 `block-cache` 以及 `write-buffer` 会占用系统内存外：

1）需预留一些内存作为系统的 page cache;

2）TiKV 在处理大的查询的时候（例如 `select * from ...`）会读取数据然后在内存中生成对应的数据结构返回给 TiDB，这个过程中 TiKV 会占用一部分内存。

## 3.导数据推荐配置
block-cache-size的大小根据机器的内存情况进行调整。
```toml
[raftstore]
# 该参数的含义是如果一个region的写入超过该值就会检查是否需要分裂，
# 在导数据的情况因为只有insert操作，所以为了减少检查一般配大点，一般为region-split-size的一半。
region-split-check-diff = "32MB"

[rocksdb]
# 该参数主要影响rocksdb compaction的线程数，在导数据的情况下因为有大量的写入，
# 所以应该开大点，但应小于CPU的核数。
max-background-compactions = 6

[rocksdb.defaultcf]
compression-per-level = "no:no:no:lz4:lz4:lz4:lz4"
block-size = "16KB"
write-buffer-size = "64MB"
max-write-buffer-number = 5
min-write-buffer-number-to-merge = 1
max-bytes-for-level-base = "256MB"
target-file-size-base = "32MB"
# 通常配置为系统内存的30-40%左右。
block-cache-size = "1GB"

[rocksdb.writecf]
compression-per-level = "no:no:no:lz4:lz4:lz4:lz4"
block-size = "16KB"
write-buffer-size = "64MB"
max-write-buffer-number = 5
min-write-buffer-number-to-merge = 1
max-bytes-for-level-base = "256MB"
target-file-size-base = "32MB"
# 通常为 defaultcf.block-cache-size 的 1/n。如果一行数据很大，n 通常比较大，
# 如果一行数据比较短，n 比较小。n 通常在 4 到 16 之间。
block-cache-size = "256MB"

[rocksdb.raftcf]
compression-per-level = "no:no:no:lz4:lz4:lz4:lz4"
block-size = "16KB"
write-buffer-size = "64MB"
max-write-buffer-number = 5
min-write-buffer-number-to-merge = 1
max-bytes-for-level-base = "256MB"
target-file-size-base = "32MB"
# 如果系统内存比较充足，建议配置为2GB。
block-cache-size = "256MB"

[storage]
# 由于导数据过程中每次都是insert一批数据，为了同时能够处理更多的请求，配置为默认配置的10倍。
scheduler-concurrency = 1024000
# 如果CPU核数大于8，建议修改该参数为8
scheduler-worker-pool-size = 4
```

