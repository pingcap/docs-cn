---
title: Troubleshoot Log Backup
summary: Learn about common problems of log backup and how to fix them.
---

# Troubleshoot Log Backup

This document summarizes common problems during log backup and the solutions.

## After restoring a downstream cluster using the `br restore point` command, data cannot be accessed from TiFlash. What should I do?

In v6.2.0, PITR does not support restoring the TiFlash replicas of a cluster. After restoring data, you need to execute the following statement to set the TiFlash replica of the schema or table.

```sql
ALTER TABLE table_name SET TIFLASH REPLICA @count;
```

In v6.3.0 and later versions, after PITR completes data restore, BR automatically executes the `ALTER TABLE SET TIFLASH REPLICA` DDL statement according to the number of TiFlash replicas in the upstream cluster at the corresponding time. You can check the TiFlash replica setting using the following SQL statement:

``` sql
SELECT * FROM INFORMATION_SCHEMA.tiflash_replica;
```

> **Note:**
>
> Currently, PITR does not support writing data directly to TiFlash during the restore phase. Therefore, TiFlash replicas are not available immediately after PITR completes data restore. Instead, you need to wait for a certain period of time for the data to be replicated from TiKV nodes. To check the replication progress, check the `progress` information in the `INFORMATION_SCHEMA.tiflash_replica` table.

## What should I do if the `status` of a log backup task becomes `ERROR`?

During a log backup task, the task status becomes `ERROR` if it fails and cannot be recovered after retrying. The following is an example:

```shell
br log status --pd x.x.x.x:2379

● Total 1 Tasks.
> #1 <
                    name: task1
                  status: ○ ERROR
                   start: 2022-07-25 13:49:02.868 +0000
                     end: 2090-11-18 14:07:45.624 +0000
                 storage: s3://tmp/br-log-backup0ef49055-5198-4be3-beab-d382a2189efb/Log
             speed(est.): 0.00 ops/s
      checkpoint[global]: 2022-07-25 14:46:50.118 +0000; gap=11h31m29s
          error[store=1]: KV:LogBackup:RaftReq
error-happen-at[store=1]: 2022-07-25 14:54:44.467 +0000; gap=11h23m35s
  error-message[store=1]: retry time exceeds: and error failed to get initial snapshot: failed to get the snapshot (region_id = 94812): Error during requesting raftstore: message: "read index not ready, reason can not read index due to merge, region 94812" read_index_not_ready { reason: "can not read index due to merge" region_id: 94812 }: failed to get initial snapshot: failed to get the snapshot (region_id = 94812): Error during requesting raftstore: message: "read index not ready, reason can not read index due to merge, region 94812" read_index_not_ready { reason: "can not read index due to merge" region_id: 94812 }: failed to get initial snapshot: failed to get the snapshot (region_id = 94812): Error during requesting raftstore: message: "read index not ready, reason can not read index due to merge, region 94812" read_index_not_ready { reason: "can not read index due to merge" region_id: 94812 }
```

To address this problem, check the error message for the cause and perform as instructed. After the problem is addressed, run the following command to resume the task:

```shell
br log resume --task-name=task1 --pd x.x.x.x:2379
```

After the backup task is resumed, you can check the status using `br log status`. The backup task continues when the task status becomes `NORMAL`.

```shell
● Total 1 Tasks.
> #1 <
              name: task1
            status: ● NORMAL
             start: 2022-07-25 13:49:02.868 +0000
               end: 2090-11-18 14:07:45.624 +0000
           storage: s3://tmp/br-log-backup0ef49055-5198-4be3-beab-d382a2189efb/Log
       speed(est.): 15509.75 ops/s
checkpoint[global]: 2022-07-25 14:46:50.118 +0000; gap=6m28s
```

> **Note:**
>
> This feature backs up multiple versions of data. When a long backup task fails and the status becomes `ERROR`, the checkpoint data of this task is set as a `safe point`, and the data of the `safe point` will not be garbage collected within 24 hours. Therefore, the backup task continues from the last checkpoint after resuming the error. If the task fails for more than 24 hours and the last checkpoint data has been garbage collected, an error will be reported when you resume the task. In this case, you can only run the `br log stop` command to stop the task first and then start a new backup task.

## What should I do if the error message `ErrBackupGCSafepointExceeded` is returned when using the `br log resume` command to resume the suspended task?

```shell
Error: failed to check gc safePoint, checkpoint ts 433177834291200000: GC safepoint 433193092308795392 exceed TS 433177834291200000: [BR:Backup:ErrBackupGCSafepointExceeded]backup GC safepoint exceeded
```

After you pause a log backup task, to prevent the MVCC data from being garbage collected, the pausing task program sets the current checkpoint as the service safepoint automatically. This ensures that the MVCC data generated within 24 hours can remain. If the MVCC data of the backup checkpoint has been generated for more than 24 hours, the data of the checkpoint will be garbage collected, and the backup task is unable to resume.

To address this problem, delete the current task using `br log stop`, and then create a log backup task using `br log start`. At the same time, you can perform a full backup for subsequent PITR.
