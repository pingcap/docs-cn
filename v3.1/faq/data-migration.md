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

## What can I do when the relay unit throws error `event from * in * diff from passed-in event *` or a replication task is interrupted with failing to get or parse binlog errors like `get binlog error ERROR 1236 (HY000)` and `binlog checksum mismatch, data may be corrupted` returned?

During the DM process of relay log pulling or incremental replication, this two errors might occur if the size of the upstream binlog file exceeds **4 GB**.

**Cause:** When writing relay logs, DM needs to perform event verification based on binlog positions and the size of the binlog file, and store the replicated binlog positions as checkpoints. However, the official MySQL uses `uint32` to store binlog positions. This means the binlog position for a binlog file over 4 GB overflows, and then the errors above occur.

For relay units, manually recover replication using the following solution:

1. Identify in the upstream that the size of the corresponding binlog file has exceeded 4GB when the error occurs.

2. Stop the DM-worker.

3. Copy the corresponding binlog file in the upstream to the relay log directory as the relay log file.

4. In the relay log directory, update the corresponding `relay.meta` file to pull from the next binlog file.

    Example: when the error occurs, `binlog-name = "mysql-bin.004451"` and `binlog-pos = 2453`. Update them respectively to `binlog-name = "mysql-bin.004452"` and `binlog-pos = 4`.

5. Restart the DM-worker.

For binlog replication processing units, manually recover replication using the following solution:

1. Identify in the upstream that the size of the corresponding binlog file has exceeded 4GB when the error occurs.

2. Stop the replication task using `stop-task`.

3. Update the `binlog_name` in the global checkpoints and in each table checkpoint of the downstream `dm_meta` database to the name of the binlog file in error; update `binlog_pos` to a valid position value for which replication has completed, for example, 4.

    Example: the name of the task in error is `dm_test`, the corresponding s`source-id` is `replica-1`, and the corresponding binlog file is `mysql-bin|000001.004451`. Execute the following command:

    {{< copyable "sql" >}}

    ```sql
    UPDATE dm_test_syncer_checkpoint SET binlog_name='mysql-bin|000001.004451', binlog_pos = 4 WHERE id='replica-1';
    ```

4. Specify `safe-mode: true` in the `syncers` section of the replication task configuration to ensure re-entrant.

5. Start the replication task using `start-task`.

6. View the status of the replication task using `query-status`. You can restore `safe-mode` to the original value and restart the replication task when replication is done for the original error-triggering relay log files.