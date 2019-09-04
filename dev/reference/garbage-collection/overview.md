---
title: GC Overview
summary: Learn about Garbage Collection in TiDB.
category: reference
---

# GC Overview

TiDB uses MVCC to control transaction concurrency. When you update the data, the original data is not deleted immediately but is kept together with the new data, with a timestamp to distinguish the version. The goal of Garbage Collection (GC) is to clear the obsolete data.

## GC process

Each TiDB cluster contains a TiDB instance that is selected as the GC leader, which controls the GC process.

GC runs periodically on TiDB. The default frequency is once every 10 minutes. For each GC, TiDB firstly calculates a timestamp called "safe point" (defaults to the current time minus 10 minutes). Then, TiDB clears the obsolete data under the premise that all the snapshots after the safe point retain the integrity of the data. Specifically, there are three steps involved in the GC process:

1. Resolve Locks
2. Delete Ranges
3. Do GC

### Resolve Locks

The TiDB transaction model is implemented based on [Google's Percolator](https://ai.google/research/pubs/pub36726). It's mainly a two-phase commit protocol with some practical optimizations. When the first phase is finished, all the related keys are locked. Among these locks, one is the primary lock and the others are secondary locks which contain a pointer to the primary lock; in the second phase, the key with the primary lock gets a write record and its lock is removed. The write record indicates the write or delete operation in the history or the transactional rollback record of this key. The type of write record that replaces the primary lock indicates whether the corresponding transaction is committed successfully. Then all the secondary locks are replaced successively. If the threads fail to replace the secondary locks, these locks are retained.

The Resolve Locks step rolls back or commits the locks before the safe point, depending on whether their primary key has been committed or not. If the primary key is also retained, the transaction times out and is rolled back.
This step is required. Once GC has cleared the write record of the primary lock, you can never know whether this transaction is successful or not. Also, if the transaction contains retained secondary keys, it's important to know whether it should be rolled back or committed. As a result, data consistency cannot be guaranteed.

In the Resolve Lock step, the GC leader processes requests from all Regions. From TiDB 3.0, this process runs concurrently by default, with the default concurrency identical to the number of TiKV nodes in the cluster. For more details on how to configure, see [GC Configuration](/dev/reference/garbage-collection/configuration.md#tikv-gc-auto-concurrency).

### Delete Ranges

A great amount of data with consecutive keys is removed during operations such as `DROP TABLE/INDEX`. Removing each key and performing GC later for them can result in low execution efficiency on storage reclaiming. In such scenarios, TiDB actually does not delete each key. Instead, it only records the range to be removed and the timestamp of the deletion. Then the Delete Ranges step performs a fast physical deletion on the ranges whose timestamp is before the safe point.

### Do GC

The Do GC step clears the outdated versions for all keys. To guarantee that all timestamps after the safe point have consistent snapshots, this step deletes the data committed before the safe point, but retains the last write before the safe point as long as it is not a deletion.

In the previous GC mechanism for TiDB 2.1 and earlier versions, the GC leader sends GC requests to all Regions. From TiDB 3.0, the GC leader only uploads the safe point to PD for each TiKV node to obtain. When the TiKV node detects a change on the safe point, it performs GC on all leader Regions on the current node. In the meantime, the GC leader can trigger the next round of GC.

> **Note:**
>
> You can modify the `tikv_gc_mode` to use the previous GC mechanism. For more details, refer to [GC Configuration](/dev/reference/garbage-collection/configuration.md).
