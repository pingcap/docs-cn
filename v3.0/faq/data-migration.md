---
title: TiDB Data Migration FAQ
summary: Learn about frequently asked questions (FAQs) about TiDB Data Migration (DM).
category: FAQ
---

# TiDB Data Migration FAQ

This document collects the frequently asked questions (FAQs) about TiDB Data Migration (DM).

## What can I do when a replication task is interrupted with the `invalid connection` error returned?

The `invalid connection` error indicates that anomalies have occurred in the connection between DM and the downstream TiDB database (such as network failure, TiDB restart, TiKV busy and so on) and that a part of the data for the current request has been sent to TiDB.

Because DM has the feature of concurrently replicating data to the downstream in replication tasks, several errors might occur when a task is interrupted. You can check these errors by using `query-status` or `query-error`.

- If only the `invalid connection` error occurs during the incremental replication process, DM retries the task automatically.
- If DM does not or fails to retry automatically because of version problems, use `stop-task` to stop the task and then use `start-task` to restart the task.

## What can I do when a replication task is interrupted with the `driver: bad connection` error returned?

The `driver: bad connection` error indicates that anomalies have occurred in the connection between DM and the upstream TiDB database (such as network failure, TiDB restart and so on) and that the data of the current request has not yet been sent to TiDB at that moment.

When this type of error occurs in the current version, use `stop-task` to stop the task and then use `start-task` to restart the task. The automatic retry mechanism of DM will be improved later.

## What can I do when a replication task is interrupted with failing to get or parse binlog errors like `get binlog error ERROR 1236 (HY000)` and `binlog checksum mismatch, data may be corrupted` returned?

During the DM incremental replication process, this error might occur if the binlog file in the upstream exceeds **4 GB**, and DM encounters a replication interruption when processing this binlog file (including interruption caused by anomalies in ordinary pause or stop tasks).

**Cause:** DM needs to store the replicated binlog position, and MySQL officially uses `uint32` to store it, so the binlog position of the file with offset exceeding **4 GB** overflows and an incorrect binlog position is stored. After the task or DM-worker is restarted, this incorrect binlog position is used to re-parse the binlog or relay log.

In this case, manually recover replication using the following solution:

1. Determine whether the error occurs during the write of the relay log or replication of Binlog replication/Syncer unit (according to the component information in the log error message).

2. Take the following step according to the place where the error occurs.

    - If the error occurs in the relay log module and the checkpoints saved by the Binlog replication/Syncer unit are correct, you can first stop the task and the DM-worker, then manually adjust the binlog position of the relay meta to `4`, and restart the DM-worker to re-pull the relay log. If the relay log is written without error, the replication automatically resumes from the checkpoint after the task is restarted.
    - If the relay log is written well and has been rotated to the next file, the error occurs in an invalid binlog position when the Binlog replication/Syncer unit reads a relay log file exceeding **4 GB**. In this situation, you can stop the task and manually set the binlog position of the relay log to a valid one such as `4`. Note that you also need to adjust the binlog position of both the global checkpoint and each table checkpoint. Set the safe-mode of the task to `true` to ensure reentrant execution. Then, you can restart the replication task and observe the status. The task resumes after the oversized (larger than **4 GB**) file is replicated.
