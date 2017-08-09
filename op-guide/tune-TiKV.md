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

[TiKV Configuration](https://github.com/pingcap/tikv/blob/master/etc/config-template.toml)

## 2.TiKV memory usage

Besides `block cache` and `write buffer`, the system memory is also occupied in the following scenarios:

+ Some of the memory need to be set aside as the system's page cache.

+ When TiKV processes large queries such as `select * from ...`, it reads data and generate corresponding data structure in the memory and returns to TiDB. During the process, some of the memory are also occupied.


## 3. Recommended configuration of TiKV

+ In production environments, it is not recommended to deploy TiKV on the machine whose CPU core is less than 8 or the memory is less than 32GB.

+ If you demand a high write throughput, it is recommended to use a disk with good throughput capacity.

+ If you demand a good read-write latency, it is recommended to use SSD with high IOPS.
