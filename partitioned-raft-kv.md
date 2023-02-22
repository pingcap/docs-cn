---
title: Partitioned Raft KV
summary: Learn about the partitioned Raft KV feature of TiKV.
---

# Partitioned Raft KV

> **Warning:**
>
> Partitioned Raft KV is an experimental feature. It is not recommended that you use it in the production environment. This feature might be changed or removed without prior notice. If you find a bug, you can report an [issue](https://github.com/pingcap/tidb/issues) on GitHub.

Before v6.6.0, TiKV's Raft-based storage engine used a single RocksDB instance to store the data of all Regions of the TiKV instance.

To support larger clusters more stably, starting from TiDB v6.6.0, a new TiKV storage engine is introduced, which uses multiple RocksDB instances to store TiKV Region data, and the data of each Region is independently stored in a separate RocksDB instance.

The new engine can better control the number and level of files in each RocksDB instance, achieve physical isolation of data operations between Regions, and support stably managing more data. You can see it as TiKV managing multiple RocksDB instances through partitioning, which is why the feature is named Partitioned Raft KV.

## Application scenarios

You can use this feature if your TiKV cluster has the following characteristics:

* A single TiKV instance needs to support more data.
* There are many write requests.
* Scale-in and scale-out operations are frequent.
* The workload has a serious read and write amplification.
* TiKV has sufficient memory.

Advantages of this feature are better write performance, faster scaling speed, and larger volume of data supported with the same hardware. It can also support larger cluster scale.

## Usage

To enable Partitioned Raft KV, set the configuration item [`storage.engine`](/tikv-configuration-file.md#engine-new-in-v660) to `"partitioned-raft-kv"` when creating a cluster. At the same time, you can use the configuration items [`rocksdb.write-buffer-flush-oldest-first`](/tikv-configuration-file.md#write-buffer-flush-oldest-first-new-in-v660) and [`rocksdb.write-buffer-limit`](/tikv-configuration-file.md#write-buffer-limit-new-in-v660) to control the memory usage of RocksDB when using Raft KV.

## Restrictions

Partitioned Raft KV has the following restrictions:

* It does not support data import, replication, and backup tools, such as TiDB Lightning, TiCDC, BR, and Dumping.
* It does not support the tikv-ctl command-line tool.
* It cannot be used together with TiFlash.
* You can only enable Partitioned Raft KV when creating a cluster and cannot change the type of engine after the cluster is created.
