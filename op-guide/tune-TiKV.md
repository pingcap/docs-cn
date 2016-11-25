
# TiKV Performance Tuning
This document describes how to tune the TiKV parameters for optimal performance.

TiKV uses RocksDB for persistent storage at the bottom level of the TiKV architecture. Therefore, many of the performance parameters are related to RocksDB.

TiKV implements `Column Families` (CF) from RocksDB and the data is ultimately stored in the `raft`, `default`, `lock` and `write` CFs inside RocksDB.
+ The `raft` CF stores the Raft log. The corresponding parameters are in `[rocksdb.raftcf]`.
+ The `default` CF stores the actual data. The corresponding parameters are in  `[rocksdb.defaultcf]`.
+ The `write` CF stores the version information in Multi-Version Concurrency Control (MVCC). The corresponding parameters are in `[rocksdb.write]`.
+ The `lock` CF stores the lock information. The system uses the default parameters.

Each CF has a separate `block cache` to cache data blocks to accelerate the data reading speed in RocksDB. You can configure the size of the `block cache` by setting the `block-cache-size` parameter. The bigger the `block-cache-size`, the more hot data can be cached, and the easier to read data, in the meantime, the more system memory will be occupied.

Each CF also has a separate `write buffer`. You can configure the size by setting the `write-buffer-size` parameter.

## 1. Parameter Specification
```toml
[server]
# Generally, use the default value. For complex queries, such as Join, Aggregation, and so on, the value can be bigger, but it must be smaller than the CPU number of the system.

end-point-concurrency = 8

[raftstore]
region-max-size = "80MB"
region-split-size = "64MB"
# Set the value to 64MB when exporting data. In other scenarios, use the default value.
region-split-check-diff = "8MB"

[rocksdb]
# Generally, use the default value and the value must be smaller than the CPU number of the system. 
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
# Generally, set the value to be 30% to 40% of the system memory size.
block-cache-size = "1GB"

[rocksdb.writecf]
compression-per-level = "no:no:no:lz4:lz4:lz4:lz4"
write-buffer-size = "64MB"
max-write-buffer-number = 5
min-write-buffer-number-to-merge = 1
max-bytes-for-level-base = "256MB"
target-file-size-base = "32MB"
# Generally, set the value to be 1/n of the `defaultcf.block-cache-size`. If the data in a row is very big, then n is big, too. And if the data in a row is short, then n is small. The range of n is from 4 to 16.

block-cache-size = "256MB"

[rocksdb.raftcf]
compression-per-level = "no:no:no:lz4:lz4:lz4:lz4"
write-buffer-size = "64MB"
max-write-buffer-number = 5
min-write-buffer-number-to-merge = 1
max-bytes-for-level-base = "256MB"
target-file-size-base = "32MB"
# Generally, set the value range to be from 256MB to 2GB. Usually, use the default value. But the value can be set to be bigger if there are ample system resources.
block-cache-size = "256MB"

[storage]
# Use the default value.
scheduler-concurrency = 102400
# Generally, use the default value. But the value can be set to be bigger if the write operation are in batches or the row is very big.
scheduler-worker-pool-size = 4
```
## 2.TiKV memory usage

Besides `block cache` and `write buffer`, the system memory is also occupied in the following scenarios:

+ Some of the memory need to be set aside as the system's cache page.

+ When TiKV processes large queries such as `select * from ...`, it reads data and generate corresponding data structure in the memory and returns to TiDB. During the process, some of the memory are also occupied.


## 3. Recommended configuration to export data
The value of `block-cache-size` is adjusted according to the system memory.

```toml
[raftstore]
# If the data written to a region is bigger than the value of this parameter, the region needs to be checked whether it needs to split. When exporting data, there are only `insert` operations, so the value can be set to be larger to reduce the check frequency, which can be half of the size of `region-split-size`. 
region-split-check-diff = "32MB"

[rocksdb]
# This parameter impacts the thread number of `rocksdb compaction`, so the value must be as big as possible but must be smaller than the CPU number of the system.
max-background-compactions = 6

[rocksdb.defaultcf]
compression-per-level = "no:no:no:lz4:lz4:lz4:lz4"
block-size = "16KB"
write-buffer-size = "64MB"
max-write-buffer-number = 5
min-write-buffer-number-to-merge = 1
max-bytes-for-level-base = "256MB"
target-file-size-base = "32MB"
# Generally, the value is 30% to 40% of the system memory size.
block-cache-size = "1GB"

[rocksdb.writecf]
compression-per-level = "no:no:no:lz4:lz4:lz4:lz4"
block-size = "16KB"
write-buffer-size = "64MB"
max-write-buffer-number = 5
min-write-buffer-number-to-merge = 1
max-bytes-for-level-base = "256MB"
target-file-size-base = "32MB"
# Generally, set the value to be 1/n of the `defaultcf.block-cache-size`. If the data in a row is very big, then n is big, too. And if the data in a row is short, then n is small. The range of n is from 4 to 16.
block-cache-size = "256MB"

[rocksdb.raftcf]
compression-per-level = "no:no:no:lz4:lz4:lz4:lz4"
block-size = "16KB"
write-buffer-size = "64MB"
max-write-buffer-number = 5
min-write-buffer-number-to-merge = 1
max-bytes-for-level-base = "256MB"
target-file-size-base = "32MB"
# If the system memory is big enough, it is recommended to set the value to 2GB. 
block-cache-size = "256MB"

[storage]
# Data are inserted in batches during the importing, so process more requests simultaneously, it is recommended to set the value to be 10 times of the default configuration.
scheduler-concurrency = 1024000
# If the CPU number is bigger than 8, it is recommended to set the value to 8.
scheduler-worker-pool-size = 4
```

