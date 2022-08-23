---
title: Known Issues in Log Backup
summary: Learn known issues in log backup.
---

# Known Issues in Log Backup

This document lists the known issues and corresponding workarounds when you use the log backup feature.

## BR encounters the OOM problem during a PITR or after you run the `br log truncate` command

Issue: [#36648](https://github.com/pingcap/tidb/issues/36648)

Consider the following possible causes:

- PITR experiences OOM because the log data to be recovered is too much. The following are two typical causes:

    - The log range to be recovered is too large.

        It is recommended that you recover logs of no more than two days, and one week to maximum. That is, perform a full backup operation at least once in two days during PITR backup process.

    - There are a large number of writes for a long time during the log backup process.

        A large number of writes for a long time usually occur when you perform a full data import to initialize the cluster. It is recommended that you perform a snapshot backup after the initial import and use that backup to restore the cluster.

- OOM occurs when you delete logs because the range of logs to be deleted is too large.

    To resolve this issue, reduce the range of logs to be deleted first and delete the target logs in several batches instead of deleting them once.

- The memory allocation of the node where the BR process is located is too low.

    It is recommended to scale up the node memory configuration to at least 16 GB to ensure that PITR has sufficient memory resources for recovery.

## The upstream database imports data using TiDB Lightning in the physical import mode, which makes it impossible to use the log backup feature

Currently, the log backup feature is not fully adapted to TiDB Lightning. Therefore, data imported in the physical mode of TiDB Lightning cannot be backed up to logs.

In upstream clusters where you create log backup tasks, avoid using the TiDB Lightning physical mode to import data. Instead, you can use TiDB Lightning logical mode. If you do need to use the physical mode, perform a snapshot backup after the import is complete, so that PITR can be restored to the time point after the snapshot backup.

## When you use the self-built Minio system as the storage for log backups, running `br restore point` or `br log truncate` returns a `RequestCanceled` error

Issue: [#36515](https://github.com/pingcap/tidb/issues/36515)

```shell
[error="RequestCanceled: request context canceled\ncaused by: context canceled"]
```

This error occurs because the current log backup generates a large number of small files. The self-built Minio storage system fails to store all these files.

To resolve this issue, you need to upgrade your Minio system to a large distributed cluster, or use the Amazon S3 storage system as the storage for log backups.

## If the cluster load is too high, there are too many Regions, and the storage has reached a performance bottleneck (for example, a self-built Minio system is used as storage for log backups), the backup progress checkpoint delay may exceed 10 minutes

Issue: [#13030](https://github.com/tikv/tikv/issues/13030)

Because the current log backup generates a large number of small files, the self-built Minio system is not able to support the writing requirements, which results in slow backup progress.

To resolve this issue, you need to upgrade your Minio system to a large distributed cluster, or use the Amazon S3 storage system as the storage for log backups.

## The cluster has recovered from the network partition failure, but the checkpoint of the log backup task progress still does not resume

Issue: [#13126](https://github.com/tikv/tikv/issues/13126)

After a network partition failure in the cluster, the backup task cannot continue backing up logs. After a certain retry time, the task will be set to `ERROR` state. At this point, the backup task has stopped.

To resolve this issue, you need to manually execute the `br log resume` command to resume the log backup task.

## The actual storage space used by log backup is 2~3 times the volume of the incremental data displayed in the cluster monitoring metrics

Issue: [#13306](https://github.com/tikv/tikv/issues/13306)

This issue occurs because log backup data use a customized encoding format. The different format leads to different data compression ratios, the difference of which is 2~3 times.

Log backup does not store data the way RocksDB generates SST files, because the data generated during log backup might have a large range and a small content. In such cases, restoring data by ingesting SST files cannot improve the restoration performance.

## The error `execute over region id` is returned when you perform PITR

Issue: [#37207](https://github.com/pingcap/tidb/issues/37207)

This issue usually occurs when you enable log backup during a full data import and afterwards perform a PITR to restore data at a time point during the data import.

Specifically, there is a probability that this issue occurs if there are a large number of hotspot writes for a long time (such as 24 hours) and if the OPS of each TiKV node is larger than 50k/s (you can view the metrics in Grafana: **TiKV-Details** -> **Backup Log** -> **Handle Event Rate**).

For the current version, it is recommended that you perform a snapshot backup after the data import and perform PITR based on this snapshot backup.

## The commit time of a large transaction affects the checkpoint lag of log backup

Issue: [#13304](https://github.com/tikv/tikv/issues/13304)

When there is a large transaction, the log checkpoint lag is not updated before the transaction is committed. Therefore, the checkpoint lag is increased by a period of time close to the commit time of the transaction.
