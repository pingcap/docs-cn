---
title: Known Issues in Log Backup
summary: Learn known issues in log backup.
---

# Known Issues in Log Backup

This document lists the known issues and corresponding workarounds when you use the log backup feature.

## BR encounters the OOM problem during a PITR or after you run the `br log truncate` command

Issue: [#36648](https://github.com/pingcap/tidb/issues/36648)

Consider the following possible causes:

- PITR experiences OOM because the log range to be recovered is too large.

    It is recommended that you recover logs of no more than two days, and one week to maximum. That is, perform a full backup operation at least once in two days or once in up to one week during PITR backup process.

- OOM occurs when you delete logs because the range of logs to be deleted is too large.

    To resolve this issue, reduce the range of logs to be deleted first and delete the target logs in several batches instead of deleting them once.

- The memory allocation of the node where the BR process is located is too low.

    It is recommended to scale up the node memory configuration to at least 16 GB to ensure that PITR has sufficient memory resources for recovery.

## The upstream database imports data using TiDB Lightning in the physical import mode, which makes it impossible to use the log backup feature

Currently, the log backup feature is not fully adapted to TiDB Lightning. Therefore, data imported in the physical mode of TiDB Lightning cannot be backed up to logs.

In upstream clusters where you create log backup tasks, avoid using the TiDB Lightning physical mode to import data. Instead, you can use TiDB Lightning logical mode. If you do need to use the physical mode, perform a full backup after the import is complete, so that PITR can be restored to the time point after the full backup.

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
