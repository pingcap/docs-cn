---
title: Data Migration Error Handling
summary: Learn how to deal with errors when you use TiDB Data Migration.
category: reference
---

# Data Migration Error Handling

This document introduces common errors that you might encounter and solutions to these errors when you use TiDB Data Migration.

## Common error description and handling method

| Error code       | Error description                                                     |  Handling method                                                    |
| :----------- | :------------------------------------------------------------ | :----------------------------------------------------------- |
| `code=10001` |  Abnormal database operation.                                              |  Further analyze the error message and error stack.                                |
| `code=10002` | The `bad connection` error from the underlying database. It usually indicates that the connection between DM and the downstream TiDB instance is abnormal (possibly caused by network failure, TiDB restart and so on) and the currently requested data is not sent to TiDB. |  DM provides automatic recovery for such error. If the recovery is not successful for a long time, check the network or TiDB status. |
| `code=10003` | The `invalid connection` error from the underlying database. It usually indicates that the connection between DM and the downstream TiDB instance is abnormal (possibly caused by network failure, TiDB restart and so on) and the currently requested data is partly sent to TiDB.  | DM provides automatic recovery for such error. If the recovery is not successful for a long time, further check the error message and analyze the information based on the actual situation. |
| `code=10005` |  Occurs when performing the `QUERY` type SQL statements.                                         |                                                              |
| `code=10006` |  Occurs when performing the `EXECUTE` type SQL statements, including DDL statements and DML statements of the `INSERT`, `UPDATE`or `DELETE` type. For more detailed error information, check the error message which usually includes the error code and error information returned for database operations.
|                                                              |
| `code=11006` |  Occurs when the built-in parser of DM parses the incompatible DDL statements.          |  Refer to [Data Migration - incompatible DDL statements](/reference/tools/data-migration/faq.md#how-to-handle-incompatible-ddl-statements) for solution. |
| `code=20010` |   Occurs when decrypting the database password that is provided in task configuration.                   |  Check whether the downstream database password provided in the configuration task is [correctly encrypted using dmctl](/how-to/deploy/data-migration-with-ansible.md#encrypt-the-upstream-mysql-user-password-using-dmctl). |
| `code=26002` |  The task check fails to establish database connection. For more detailed error information, check the error message which usually includes the error code and error information returned for database operations. |  Check whether the machine where DM-master is located has permission to access the upstream. |
| `code=32001` |   Abnormal dump processing unit                                            |  If the error message contains `mydumper: argument list too long.`, configure the table to be exported by manually adding the `--regex` regular expression in the Mydumper argument `extra-args` in the `task.yaml` file according to the black-white list. For example, to export all tables named `hello`, add `--regex '.*\\.hello$'`; to export all tables, add `--regex '.*'`. |
| `code=38008` |  An error occurs in the gRPC communication among DM components.                                     |   Check `class`. Find out the error occurs in the interaction of which components. Determine the type of communication error. If the error occurs when establishing gRPC connection, check whether the communication server is working normally. |

## What can I do when a replication task is interrupted with the `invalid connection` error returned?

The `invalid connection` error indicates that anomalies have occurred in the connection between DM and the downstream TiDB database (such as network failure, TiDB restart, TiKV busy and so on) and that a part of the data for the current request has been sent to TiDB.

Because DM has the feature of concurrently replicating data to the downstream in replication tasks, several errors might occur when a task is interrupted. You can check these errors by using `query-status` or `query-error`.

- If only the `invalid connection` error occurs during the incremental replication process, DM retries the task automatically.
- If DM does not or fails to retry automatically because of version problems, use `stop-task` to stop the task and then use `start-task` to restart the task.

## A replication task is interrupted with the `driver: bad connection` error returned

The `driver: bad connection` error indicates that anomalies have occurred in the connection between DM and the upstream TiDB database (such as network failure, TiDB restart and so on) and that the data of the current request has not yet been sent to TiDB at that moment.

When this type of error occurs in the current version, use `stop-task` to stop the task and then use `start-task` to restart the task. The automatic retry mechanism of DM will be improved later.

## The relay unit throws error `event from * in * diff from passed-in event *` or a replication task is interrupted with failing to get or parse binlog errors like `get binlog error ERROR 1236 (HY000)` and `binlog checksum mismatch, data may be corrupted` returned

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

### `Access denied for user 'root'@'172.31.43.27' (using password: YES)` shows when you query the task or check the log

For database related passwords in all the DM configuration files, use the passwords encrypted by `dmctl`. If a database password is empty, it is unnecessary to encrypt it. For how to encrypt the plaintext password, see [Encrypt the upstream MySQL user password using dmctl](/how-to/deploy/data-migration-with-ansible.md#encrypt-the-upstream-mysql-user-password-using-dmctl).

In addition, the user of the upstream and downstream databases must have the corresponding read and write privileges. Data Migration also [prechecks the corresponding privileges automatically](/reference/tools/data-migration/precheck.md) while starting the data replication task.
