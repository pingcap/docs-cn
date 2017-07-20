---
title: TiKV Performance Tuning
category: advanced
---

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
# The listening address
# addr = "127.0.0.1:20160"

# The data catalogue
# store-dir = "/tmp/tikv/store"

# You can lable a TiKV instance to schedule replicas.
# labels = "zone=cn-east-1,host=118"

# The log level: trace, debug, info, warn, error, off
log-level = "info"

# It is recommended to use the default value.
# notify-capacity = 40960
# messages-per-tick = 4096

# The size of the send / receive buffer of socket.
# send-buffer-size = "128KB"
# recv-buffer-size = "128KB"

# Most of the requests from TiDB will be sent to TiKV's coprocessor for processing. This parameter is used for configuring the number of coprocessor threads. If your business has more read requests than write, add more coprocessor threads but make sure it's less than the CPU core number in the system. For example, if the machine in which TiKV resides has 32 cores and it can be set to 30. By default, TiKV automatically sets this number as the total core number of CPU * 0.8.
# end-point-concurrency = 8

[metric]
# The time interval of pushing metrics to the Prometheus pushgateway
interval = "15s"
# The Prometheus pushgateway address
address = ""
job = "tikv"

[raftstore]
region-max-size = "80MB"
# The region split threshold
region-split-size = "64MB"
# Set the value to 64MB when exporting data. In other scenarios, use the default value. 
region-split-check-diff = "8MB"

[pd]
# The PD address
# endpoints = "127.0.0.1:2379"

[rocksdb]
# The maximum number of threads for RocksDB to conduct compaction. For more information about RocksDB compaction, see the RocksDB documents. When the write traffic is large (such as importing data), it is recommended to enable more compaction threads, but it should be smaller than the CPU core number. For example, when importing data, for a machine of 32-core CPU, max-background-compactions and max-background-flushes can be set to be 28.
max-background-compactions = 6
max-background-flushes = 2

# The maximum number of file handle that RocksDB can open
# max-open-files = 40960

# The size limit of RocksDB MANIFEST file.
# For more information, see https://github.com/facebook/rocksdb/wiki/MANIFEST
max-manifest-file-size = "20MB"

# The catalogue for RocksDB write-ahead logs. If the machine has two disks, you can store RocksDB data and WAL log in different disks to improve the TiKV performance.
# wal-dir = "/tmp/tikv/store"

# The following two parameters are used for RocksDB archiving WAL.
# For more information, see https://github.com/facebook/rocksdb/wiki/How-to-persist-in-memory-RocksDB-database
# wal-ttl-seconds = 0
# wal-size-limit = 0

# The maximum total size of RocksDB WAL log. Generally, you can use the default value.
# max-total-wal-size = "4GB"

# You can enable or disable the RocksDB statistics by using the enable-statistics parameter.
# enable-statistics = true

# You can enable the read-ahead function in the process of RocksDB compaction. If you use a mechanical disk, it is recommended to set the value to be at least 2MB.
# compaction-readahead-size = "2MB"

[rocksdb.defaultcf]
# The size of data block. RocksDB compresses data in block and at the same time, block is the smallest unit in block-cache (similar to the page concept of other databases).
block-size = "64KB"
# The compression level of data on each layer: no,snappy,zlib,bzip2,lz4,lz4hc.
# no:no:lz4:lz4:lz4:lz4:lz4 means level0 and level1 do not compress and level2 to level6 adopt the lz4 compression algorithm.
# "no" means there is no compression; lz4 is a compression algorithm with moderate velocity and compression ratio; zlib has a high compression ratio and is good for the storage space. However, the compression speed is slow and it takes up too much CPU resource when compressing. Different machines need to configure the compression method according to the situation of CPU and IO resource. For example, when the compression method is "no:no:lz4:lz4:lz4:lz4:lz4", if the system faces heavy IO pressure while the CPU resource is adequate when writing a large amount of data (importing data, for example), use level0 and level1 to compress, sacrificing CPU resource for IO resource. If the IO pressure is small but the CPU resource has run up, whose symptom is that top -H has found a large amount of threads started with bg (the compaction thread of RocksDB) are running, you can sacrifice IO resource for CPU resource by changing the compression method to "no:no:no:lz4:lz4:lz4:lz4". In a word, the purpose is to utilize the existing resource to the utmost extent so that TiKV can play the best performance.
compression-per-level = "no:no:no:lz4:lz4:lz4:lz4"

# the size of RocksDB memtable
write-buffer-size = "128MB"

# Several memtable is accepted at most. Data written to RocksDB will first be recorded to a WAL log and inserted to memtable. When the size of the memtable reaches the specified size of write-buffer-size, the current memtable will become read-only and then a new memtable will receive new write. The read-only memtable will be flushed to disk by the flush thread of RocksDB (the maximum number that the max-background-flushes parameter can control) and becomes an sst file of level0. When the flush thread is too busy and causes the number of memtable in the disk waiting for flush reaches the number specified by max-write-buffer-number, RocksDB will stall the new writes. Stall is a flow-control mechanism. When importing data, the value of max-write-buffer-number can be set to be bigger, 10 for example.
max-write-buffer-number = 5

# When the sst file of level0 reaches the limitation specified by level0-slowdown-writes-trigger, RocksDB will try to slow down the writing speed as too much sst of level0 will increase RocksDB read.
# level0-slowdown-writes-trigger and level0-stop-writes-trigger is another manifestation of RocksDB's flow-control. When the number of sst file of level0 reaches 4 (the default value), the overlapping sst file in level0 and level1 will conduct compaction, in order to solve the read amplification problem.
level0-slowdown-writes-trigger = 20
# When the number of sst file of level0 reaches the limitation specified by level0-stop-writes-trigger, RocksDB will stall new writing.
level0-stop-writes-trigger = 36
# When the data size of level1 reaches the limitation specified by max-bytes-for-level-base, the overlap sst in level1 and level2 will be compacted.
# Golden rule: the first principle of setting max-bytes-for-level-base is to ensure that the data size of level0 is roughly the same to reduce the unnecessary compaction. For example, if the compression method is "no:no:lz4:lz4:lz4:lz4:lz4", the value of max-bytes-for-level-base should be the size of write-buffer-size * 4. The reason is that level0 and level1 do not compress and the condition for level0 to enable compaction is that the sst number reaches 4 (the default value). If level0 and level1 has been compressed, you need to analyze the RocksDB log and check the size of memtable compressed to a sst file. If the size is 32MB, the recommended value of max-bytes-for-level-base should be 32MB * 4 = 128MB.
max-bytes-for-level-base = "512MB"
# The size of the sst file. The size of the sst file of level0 is influenced by the compression algorithm of write-buffer-size and level0. The target-file-size-base parameter is used for controlling the size of each sst file of level1 to level6.
target-file-size-base = "32MB"

# If this parameter has not been configured, TiKV will set the value as 40% of the total memory of the system. If you need to deploy multiple TiKV nodes on a standalone physical machine, configure this parameter explicitly configure, otherwise, there might be an OOM problem.
# block-cache-size = "1GB"

[rocksdb.writecf]
# Be consistent with rocksdb.defaultcf.compression-per-level.
compression-per-level = "no:no:lz4:lz4:lz4:lz4:lz4"
# Be consistent with rocksdb.defaultcf.write-buffer-size.
write-buffer-size = "128MB"
max-write-buffer-number = 5
min-write-buffer-number-to-merge = 1
# Be consistent with rocksdb.defaultcf.max-bytes-for-level-base.
max-bytes-for-level-base = "512MB"
target-file-size-base = "32MB"
# If this parameter has not been configured, TiKV will set the value as 15% of the total memory of the system. If you need to deploy multiple TiKV nodes on a standalone physical machine, you should explicitly configure this parameter. Information related to MVCC and data related to index will be recorded in this c. If there are many single table indexes in the scenarion of business, set this parameter to be bigger.
# block-cache-size = "256MB"

[rocksdb.raftcf]
# Be consistent with rocksdb.defaultcf.compression-per-level.
compression-per-level = "no:no:no:lz4:lz4:lz4:lz4"
# Be consistent with rocksdb.defaultcf.write-buffer-size.
write-buffer-size = "128MB"
max-write-buffer-number = 5
min-write-buffer-number-to-merge = 1
# Be consistent with rocksdb.defaultcf.max-bytes-for-level-base.
max-bytes-for-level-base = "512MB"
target-file-size-base = "32MB"
# Generally, it is configured between 256MB to 2GB and use the default value. But if the system has ample resource, you can make it larger.
block-cache-size = "256MB"

[storage]
# Generally, use the default value. When importing data, it is recommended to set the parameter as 1024000.
# scheduler-concurrency = 102400
# This parameter controls the number of writing threads. When the write operation are in batches, set the value to be bigger. Use top -H -p tikv-pid to find that the threads with the name of sched-worker-pool are busy. At this time, the scheduler-worker-pool-size parameter should be set to be bigger and add more threads.
# scheduler-worker-pool-size = 4
```
## 2.TiKV memory usage

Besides `block cache` and `write buffer`, the system memory is also occupied in the following scenarios:

+ Some of the memory need to be set aside as the system's page cache.

+ When TiKV processes large queries such as `select * from ...`, it reads data and generate corresponding data structure in the memory and returns to TiDB. During the process, some of the memory are also occupied.


## 3. Recommended configuration of TiKV

+ In production environments, it is not recommended to deploy TiKV on the machine whose CPU core is less than 8 or the memory is less than 32GB.

+ If you demand a high write throughput, it is recommended to use a disk with good throughput capacity.

+ If you demand a good read-write latency, it is recommended to use SSD with high IOPS.
