---
title: Handle Errors in TiDB Data Migration
summary: Learn about the error system and how to handle common errors when you use DM.
aliases: ['/docs/tidb-data-migration/dev/error-handling/','/docs/tidb-data-migration/dev/troubleshoot-dm/','/docs/tidb-data-migration/dev/error-system/']
---

# Handle Errors in TiDB Data Migration

This document introduces the error system and how to handle common errors when you use DM.

## Error system

In the error system, usually, the information of a specific error is as follows:

- `code`: error code.

    DM uses the same error code for the same error type. An error code does not change as the DM version changes.

    Some errors might be removed during the DM iteration, while the error codes are not. DM uses a new error code instead of an existing one for a new error.

- `class`: error type.

    It is used to mark the component where an error occurs (error source).

    The following table displays all error types, error sources, and error samples.

    |  <div style="width: 100px;">Error Type</div>    |   Error Source            | Error Sample                                                     |
    | :-------------- | :------------------------------ | :------------------------------------------------------------ |
    | `database`       |  Database operations         | `[code=10003:class=database:scope=downstream:level=medium] database driver: invalid connection` |
    | `functional`     |  Underlying functions of DM           | `[code=11005:class=functional:scope=internal:level=high] not allowed operation: alter multiple tables in one statement` |
    | `config`         |  Incorrect configuration                      | `[code=20005:class=config:scope=internal:level=medium] empty source-id not valid` |
    | `binlog-op`      |  Binlog operations          | `[code=22001:class=binlog-op:scope=internal:level=high] empty UUIDs not valid` |
    | `checkpoint`     |  checkpoint operations  | `[code=24002:class=checkpoint:scope=internal:level=high] save point bin.1234 is older than current pos bin.1371` |
    | `task-check`     |  Performing task check       | `[code=26003:class=task-check:scope=internal:level=medium] new table router error` |
    | `relay-event-lib`|  Executing the basic functions of the relay module | `[code=28001:class=relay-event-lib:scope=internal:level=high] parse server-uuid.index` |
    | `relay-unit`     |  relay processing unit    | `[code=30015:class=relay-unit:scope=upstream:level=high] TCPReader get event: ERROR 1236 (HY000): Could not open log file` |
    | `dump-unit`      |   dump processing unit    | `[code=32001:class=dump-unit:scope=internal:level=high] mydumper runs with error: CRITICAL **: 15:12:17.559: Error connecting to database: Access denied for user 'root'@'172.17.0.1' (using password: NO)` |
    | `load-unit`      |  load processing unit    | `[code=34002:class=load-unit:scope=internal:level=high] corresponding ending of sql: ')' not found` |
    | `sync-unit`      |  sync processing unit     | `[code=36027:class=sync-unit:scope=internal:level=high] Column count doesn't match value count: 9 (columns) vs 10 (values)` |
    | `dm-master`      |   DM-master service | `[code=38008:class=dm-master:scope=internal:level=high] grpc request error: rpc error: code = Unavailable desc = all SubConns are in TransientFailure, latest connection error: connection error: desc = "transport: Error while dialing dial tcp 172.17.0.2:8262: connect: connection refused"` |
    | `dm-worker`      |  DM-worker service  | `[code=40066:class=dm-worker:scope=internal:level=high] ExecuteDDL timeout, try use query-status to query whether the DDL is still blocking` |
    | `dm-tracer`      |  DM-tracer service  | `[code=42004:class=dm-tracer:scope=internal:level=medium] trace event test.1 not found` |
    | `schema-tracker` | schema-tracker (during incremental data replication)   | `[code=44006:class=schema-tracker:scope=internal:level=high],"cannot track DDL: ALTER TABLE test DROP COLUMN col1"` |
    | `scheduler`      | Scheduling operations (of data migration tasks)   | `[code=46001:class=scheduler:scope=internal:level=high],"the scheduler has not started"` |
    | `dmctl`          | An error occurs within dmctl or when it interacts with other components | `[code=48001:class=dmctl:scope=internal:level=high],"can not create grpc connection"` |

- `scope`: Error scope.

    It is used to mark the scope and source of DM objects when an error occurs. `scope` includes four types: `not-set`, `upstream`, `downstream`, and `internal`.

    If the logic of the error directly involves requests between upstream and downstream databases, the scope is set to `upstream` or `downstream`; otherwise, it is currently set to `internal`.

- `level`: Error level.

    The severity level of the error, including `low`, `medium`, and `high`.

    - The `low` level error usually relates to user operations and incorrect inputs. It does not affect migration tasks.
    - The `medium` level error usually relates to user configurations. It affects some newly started services; however, it does not affect the existing DM migration status.
    - The `high` level error usually needs your attention, since you need to resolve it to avoid the possible interruption of a migration task.

- `message`: Error descriptions.

    Detailed descriptions of the error. To wrap and store every additional layer of error message on the error call chain, the [errors.Wrap](https://godoc.org/github.com/pkg/errors#hdr-Adding_context_to_an_error) mode is adopted. The message description wrapped at the outermost layer indicates the error in DM and the message description wrapped at the innermost layer indicates the error source.

- `workaround`: Error handling methods (optional)

    The handling methods for this error. For some confirmed errors (such as configuration errors), DM gives the corresponding manual handling methods in `workaround`.

- Error stack information (optional)

    Whether DM outputs the error stack information depends on the error severity and the necessity. The error stack records the complete stack call information when the error occurs. If you cannot figure out the error cause based on the basic information and the error message, you can trace the execution path of the code when the error occurs using the error stack.

For the complete list of error codes, refer to the [error code lists](https://github.com/pingcap/dm/blob/master/_utils/terror_gen/errors_release.txt).

## Troubleshooting

If you encounter an error while running DM, take the following steps to troubleshoot this error:

1. Execute the `query-status` command to check the task running status and the error output.

2. Check the log files related to the error. The log files are on the DM-master and DM-worker nodes. To get key information about the error, refer to the [error system](#error-system). Then check the [Handle Common Errors](#handle-common-errors) section to find the solution.

3. If the error is not covered in this document, and you cannot solve the problem by checking the log or monitoring metrics, [get support](/support.md) from PingCAP or the community.

4. After the error is resolved, restart the task using dmctl.

    {{< copyable "shell-regular" >}}

    ```bash
    resume-task ${task name}
    ```

However, you need to reset the data migration task in some cases. For details, refer to [Reset the Data Migration Task](/dm/dm-faq.md#how-to-reset-the-data-migration-task).

## Handle common errors

| <div style="width: 100px;">Error Code</div>       | Error Description                                                     |  How to Handle                                                    |
| :----------- | :------------------------------------------------------------ | :----------------------------------------------------------- |
| `code=10001` |  Abnormal database operation.                                              |  Further analyze the error message and error stack.                                |
| `code=10002` | The `bad connection` error from the underlying database. It usually indicates that the connection between DM and the downstream TiDB instance is abnormal (possibly caused by network failure or TiDB restart) and the currently requested data is not sent to TiDB. |  DM provides automatic recovery for such error. If the recovery is not successful for a long time, check the network or TiDB status. |
| `code=10003` | The `invalid connection` error from the underlying database. It usually indicates that the connection between DM and the downstream TiDB instance is abnormal (possibly caused by network failure or TiDB restart) and the currently requested data is partly sent to TiDB.  | DM provides automatic recovery for such error. If the recovery is not successful for a long time, further check the error message and analyze the information based on the actual situation. |
| `code=10005` |  Occurs when performing the `QUERY` type SQL statements.                                         |                                                              |
| `code=10006` |  Occurs when performing the `EXECUTE` type SQL statements, including DDL statements and DML statements of the `INSERT`, `UPDATE`or `DELETE` type. For more detailed error information, check the error message which usually includes the error code and error information returned for database operations.
|                                                              |
| `code=11006` |  Occurs when the built-in parser of DM parses the incompatible DDL statements.          |  Refer to [Data Migration - incompatible DDL statements](/dm/dm-faq.md#how-to-handle-incompatible-ddl-statements) for solution. |
| `code=20010` |   Occurs when decrypting the database password that is provided in task configuration.                   |  Check whether the downstream database password provided in the configuration task is [correctly encrypted using dmctl](/dm/dm-manage-source.md#encrypt-the-database-password). |
| `code=26002` |  The task check fails to establish database connection. For more detailed error information, check the error message which usually includes the error code and error information returned for database operations. |  Check whether the machine where DM-master is located has permission to access the upstream. |
| `code=32001` |   Abnormal dump processing unit                                            |  If the error message contains `mydumper: argument list too long.`, configure the table to be exported by manually adding the `--regex` regular expression in the Mydumper argument `extra-args` in the `task.yaml` file according to the block-allow list. For example, to export all tables named `hello`, add `--regex '.*\\.hello$'`; to export all tables, add `--regex '.*'`. |
| `code=38008` |  An error occurs in the gRPC communication among DM components.                                     |   Check `class`. Find out the error occurs in the interaction of which components. Determine the type of communication error. If the error occurs when establishing gRPC connection, check whether the communication server is working normally. |

### What can I do when a migration task is interrupted with the `invalid connection` error returned?

#### Reason

The `invalid connection` error indicates that anomalies have occurred in the connection between DM and the downstream TiDB database (such as network failure, TiDB restart, and TiKV busy) and that a part of the data for the current request has been sent to TiDB.

#### Solutions

Because DM has the feature of concurrently migrating data to the downstream in migration tasks, several errors might occur when a task is interrupted. You can check these errors by using `query-status`.

- If only the `invalid connection` error occurs during the incremental replication process, DM retries the task automatically.
- If DM does not or fails to retry automatically because of version problems, use `stop-task` to stop the task and then use `start-task` to restart the task.

### A migration task is interrupted with the `driver: bad connection` error returned

#### Reason

The `driver: bad connection` error indicates that anomalies have occurred in the connection between DM and the upstream TiDB database (such as network failure and TiDB restart) and that the data of the current request has not yet been sent to TiDB at that moment.

#### Solution

The current version of DM automatically retries on error. If you use the previous version which does not support automatically retry, you can execute the `stop-task` command to stop the task. Then execute `start-task` to restart the task.

### The relay unit throws error `event from * in * diff from passed-in event *` or a migration task is interrupted with failing to get or parse binlog errors like `get binlog error ERROR 1236 (HY000)` and `binlog checksum mismatch, data may be corrupted` returned

#### Reason

During the DM process of relay log pulling or incremental replication, this two errors might occur if the size of the upstream binlog file exceeds **4 GB**.

**Cause:** When writing relay logs, DM needs to perform event verification based on binlog positions and the size of the binlog file, and store the replicated binlog positions as checkpoints. However, the official MySQL uses `uint32` to store binlog positions. This means the binlog position for a binlog file over 4 GB overflows, and then the errors above occur.

#### Solutions

For relay units, manually recover migration using the following solution:

1. Identify in the upstream that the size of the corresponding binlog file has exceeded 4GB when the error occurs.

2. Stop the DM-worker.

3. Copy the corresponding binlog file in the upstream to the relay log directory as the relay log file.

4. In the relay log directory, update the corresponding `relay.meta` file to pull from the next binlog file. If you have specified `enable_gtid` to `true` for the DM-worker, you need to modify the GTID corresponding to the next binlog file when updating the `relay.meta` file. Otherwise, you don't need to modify the GTID.

    Example: when the error occurs, `binlog-name = "mysql-bin.004451"` and `binlog-pos = 2453`. Update them respectively to `binlog-name = "mysql-bin.004452"` and `binlog-pos = 4`, and update `binlog-gtid` to `f0e914ef-54cf-11e7-813d-6c92bf2fa791:1-138218058`.

5. Restart the DM-worker.

For binlog replication processing units, manually recover migration using the following solution:

1. Identify in the upstream that the size of the corresponding binlog file has exceeded 4GB when the error occurs.

2. Stop the migration task using `stop-task`.

3. Update the `binlog_name` in the global checkpoints and in each table checkpoint of the downstream `dm_meta` database to the name of the binlog file in error; update `binlog_pos` to a valid position value for which migration has completed, for example, 4.

    Example: the name of the task in error is `dm_test`, the corresponding s`source-id` is `replica-1`, and the corresponding binlog file is `mysql-bin|000001.004451`. Execute the following command:

    {{< copyable "sql" >}}

    ```sql
    UPDATE dm_test_syncer_checkpoint SET binlog_name='mysql-bin|000001.004451', binlog_pos = 4 WHERE id='replica-1';
    ```

4. Specify `safe-mode: true` in the `syncers` section of the migration task configuration to ensure re-entrant.

5. Start the migration task using `start-task`.

6. View the status of the migration task using `query-status`. You can restore `safe-mode` to the original value and restart the migration task when migration is done for the original error-triggering relay log files.

### `Access denied for user 'root'@'172.31.43.27' (using password: YES)` shows when you query the task or check the log

For database related passwords in all the DM configuration files, it is recommended to use the passwords encrypted by `dmctl`. If a database password is empty, it is unnecessary to encrypt it. For how to encrypt the plaintext password, see [Encrypt the database password using dmctl](/dm/dm-manage-source.md#encrypt-the-database-password).

In addition, the user of the upstream and downstream databases must have the corresponding read and write privileges. Data Migration also [prechecks the corresponding privileges automatically](/dm/dm-precheck.md) while starting the data migration task.

### The `load` processing unit reports the error `packet for query is too large. Try adjusting the 'max_allowed_packet' variable`

#### Reasons

* Both MySQL client and MySQL/TiDB server have the quota limits for `max_allowed_packet`. If any `max_allowed_packet` exceeds a limit, the client receives the error message. Currently, for the latest version of DM and TiDB server, the default value of `max_allowed_packet` is `64M`.

* The full data import processing unit in DM does not support splitting the SQL file exported by the Dump processing unit in DM.

#### Solutions

* It is recommended to set the `statement-size` option of `extra-args` for the Dump processing unit:

    According to the default `--statement-size` setting, the default size of `Insert Statement` generated by the Dump processing unit is about `1M`. With this default setting, the load processing unit does not report the error `packet for query is too large. Try adjusting the 'max_allowed_packet' variable` in most cases.

    Sometimes you might receive the following `WARN` log during the data dump. This `WARN` log does not affect the dump process. This only means that wide tables are dumped.

    ```
    Row bigger than statement_size for xxx
    ```

* If the single row of the wide table exceeds `64M`, you need to modify the following configurations and make sure the configurations take effect.

    * Execute `set @@global.max_allowed_packet=134217728` (`134217728` = 128 MB) in the TiDB server.

    * First add the `max-allowed-packet: 134217728` (128 MB) to the `target-database` section in the DM task configuration file. Then, execute the `stop-task` command and execute the `start-task` command.
