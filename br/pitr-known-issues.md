---
title: Known Issues in Log Backup
summary: Learn known issues in log backup.
---

# Known Issues in Log Backup

This document lists the known issues and corresponding workarounds when you use the log backup feature.

## BR encounters the OOM problem after you run the `br log truncate` command

Issue: [#36648](https://github.com/pingcap/tidb/issues/36648)

Consider the following possible causes:

- The range of logs to be deleted is too large.

    To resolve this issue, reduce the range of logs to be deleted first and delete the target logs in several batches instead of deleting them once.

- The memory allocation of the node where the BR process is located is too low.

    It is recommended to scale up the node memory configuration to at least 16 GB to ensure that PITR has sufficient memory resources for recovery.

## The upstream database imports data using TiDB Lightning in the physical import mode, which makes it impossible to use the log backup feature

Currently, the log backup feature is not fully adapted to TiDB Lightning. Therefore, data imported in the physical mode of TiDB Lightning cannot be backed up to logs.

In upstream clusters where you create log backup tasks, avoid using the TiDB Lightning physical mode to import data. Instead, you can use TiDB Lightning logical mode. If you do need to use the physical mode, perform a snapshot backup after the import is complete, so that PITR can be restored to the time point after the snapshot backup.

## The cluster has recovered from the network partition failure, but the checkpoint of the log backup task progress still does not resume

Issue: [#13126](https://github.com/tikv/tikv/issues/13126)

After a network partition failure in the cluster, the backup task cannot continue backing up logs. After a certain retry time, the task will be set to `ERROR` state. At this point, the backup task has stopped.

To resolve this issue, you need to manually execute the `br log resume` command to resume the log backup task.

## The error `execute over region id` is returned when you perform PITR

Issue: [#37207](https://github.com/pingcap/tidb/issues/37207)

This issue usually occurs when you enable log backup during a full data import and afterwards perform a PITR to restore data at a time point during the data import.

Specifically, there is a probability that this issue occurs if there are a large number of hotspot writes for a long time (such as 24 hours) and if the OPS of each TiKV node is larger than 50k/s (you can view the metrics in Grafana: **TiKV-Details** -> **Backup Log** -> **Handle Event Rate**).

For the current version, it is recommended that you perform a snapshot backup after the data import and perform PITR based on this snapshot backup.

## The commit time of a large transaction affects the checkpoint lag of log backup

Issue: [#13304](https://github.com/tikv/tikv/issues/13304)

When there is a large transaction, the log checkpoint lag is not updated before the transaction is committed. Therefore, the checkpoint lag is increased by a period of time close to the commit time of the transaction.

## The acceleration of adding indexes feature is not compatible with PITR

Issue: [#38045](https://github.com/pingcap/tidb/issues/38045)

Currently, the [acceleration of adding indexes](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630) feature is not compatible with PITR. When using index acceleration, you need to ensure that there are no PITR log backup tasks running in the background. Otherwise, unexpected behaviors might occur, including:

- If you start a log backup task first, and then add an index. The adding index process is not accelerated even if index acceleration is enabled. But the index is added in a slow way.
- If you start an index acceleration task first, and then start a log backup task. The log backup task returns an error. But the index acceleration is not affected.
- If you start a log backup task and an index acceleration task at the same time, the two tasks might not be aware of each other. This might result in PITR failing to back up the newly added index.
