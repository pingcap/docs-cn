---
title: Data Migration Error Message Description
summary: Learn the system and description of error messages in Data Migration.
category: reference
---

# Data Migration Error Message Description

This document describes the error messages in Data Migration (DM) and offers solutions to some common error messages.

## DM error system

A new error system has been introduced in DM 1.0.0-GA, which has the following features:

+ Add the error code mechanism
+ Add the error fields such as `class`, `scope` or `level`
+ Improve the error description, error call chain information and stack trace information

For the design and implementation of this error system, refer to [Proposal: Improve Error System](https://github.com/pingcap/dm/blob/master/docs/RFCS/20190722_error_handling.md).

## Error message reference

The following is an actual error message in DM. Taking this message as a sample, this document explains each field of an error message in detail.

```
[code=38008:class=dm-master:scope=internal:level=high] grpc request error: rpc error: code = Unavailable desc = all SubConns are in TransientFailure, latest connection error: connection error: desc = "transport: Error while dialing dial tcp 172.17.0.2:8262: connect: connection refused"
github.com/pingcap/dm/pkg/terror.(*Error).Delegate
        /root/code/gopath/src/github.com/pingcap/dm/pkg/terror/terror.go:267
github.com/pingcap/dm/dm/master/workerrpc.callRPC
        /root/code/gopath/src/github.com/pingcap/dm/dm/master/workerrpc/rawgrpc.go:124
github.com/pingcap/dm/dm/master/workerrpc.(*GRPCClient).SendRequest
        /root/code/gopath/src/github.com/pingcap/dm/dm/master/workerrpc/rawgrpc.go:64
github.com/pingcap/dm/dm/master.(*Server).getStatusFromWorkers.func2
        /root/code/gopath/src/github.com/pingcap/dm/dm/master/server.go:1125
github.com/pingcap/dm/dm/master.(*AgentPool).Emit
        /root/code/gopath/src/github.com/pingcap/dm/dm/master/agent_pool.go:117
runtime.goexit
        /root/.gvm/gos/go1.12/src/runtime/asm_amd64.s:1337
```

All error messages in DM have the following three components:

+ [basic error information]
+ Error message description
+ Error stack information (optional)

### Basic error information

- `code`: error code, which is unique for each error type.

    DM uses the same error code for the same error type. An error code does not change as DM version changes.

    Some errors might be removed during the DM iteration, but the error code will not be removed. DM uses a new error code instead of an existing one for a new error.

- `class`: error type

    It is used to mark the component where an error occurs (error source).

    The table below displays all error types, the corresponding sources and error samples.

    |  Error type    |   Error source            | Error sample                                                     |
    | :-------------- | :------------------------------ | :------------------------------------------------------------ |
    | `database`       |  Database operations         | `[code=10003:class=database:scope=downstream:level=medium] database driver: invalid connection` |
    | `functional`     |  Underlying functions of DM           | `[code=11005:class=functional:scope=internal:level=high] not allowed operation: alter multiple tables in one statement` |
    | `config`         |  Incorrect configuration                      | `[code=20005:class=config:scope=internal:level=medium] empty source-id not valid` |
    | `binlog-op`      |  Binlog operations          | `[code=22001:class=binlog-op:scope=internal:level=high] empty UUIDs not valid` |
    | `checkpoint`     |  Checkpoint operations  | `[code=24002:class=checkpoint:scope=internal:level=high] save point bin.1234 is older than current pos bin.1371` |
    | `task-check`     |  Performing task check       | `[code=26003:class=task-check:scope=internal:level=medium] new table router error` |
    | `relay-event-lib`|  Executing the basic functions of the relay module | `[code=28001:class=relay-event-lib:scope=internal:level=high] parse server-uuid.index` |
    | `relay-unit`     |  Relay processing unit    | `[code=30015:class=relay-unit:scope=upstream:level=high] TCPReader get event: ERROR 1236 (HY000): Could not open log file` |
    | `dump-unit`      |   Dump processing unit    | `[code=32001:class=dump-unit:scope=internal:level=high] mydumper runs with error: CRITICAL **: 15:12:17.559: Error connecting to database: Access denied for user 'root'@'172.17.0.1' (using password: NO)` |
    | `load-unit`      |  Load processing unit    | `[code=34002:class=load-unit:scope=internal:level=high] corresponding ending of sql: ')' not found` |
    | `sync-unit`      |  sync processing unit     | `[code=36027:class=sync-unit:scope=internal:level=high] Column count doesn't match value count: 9 (columns) vs 10 (values)` |
    | `dm-master`      |   DM-master service | `[code=38008:class=dm-master:scope=internal:level=high] grpc request error: rpc error: code = Unavailable desc = all SubConns are in TransientFailure, latest connection error: connection error: desc = "transport: Error while dialing dial tcp 172.17.0.2:8262: connect: connection refused"` |
    | `dm-worker`      |  DM-worker service  | `[code=40066:class=dm-worker:scope=internal:level=high] ExecuteDDL timeout, try use query-status to query whether the DDL is still blocking` |
    | `dm-tracer`      |  DM-tracer service  | `[code=42004:class=dm-tracer:scope=internal:level=medium] trace event test.1 not found` |

- `scope`: Error scope

    It is used to identify the scope and source of DM objects when an error occurs, including these four types: `not-set`, `upstream`, `downstream`, and `internal`.

    If the logic of the error directly involves requests between upstream and downstream databases, the scope is set to `upstream` or `downstream`. Other error scenarios are currently set to `internal`.

- `level`: Error level

    The severity level of the error, which includes `low`, `medium`, and `high`.

    The low-level error usually relates to user operation and incorrect input, which does not affect normal replication tasks. The medium-level error usually relates to user configuration, which affects some newly started services but does not affect the existing DM replication status. The high-level error usually needs your solution, otherwise there might be such risks as interrupting replication tasks.

For the [above error sample](#error-message-reference):

- `code=38008` is the error code indicating that the error occurs in the gRPC communication.
- `class=dm-master` indicates that the error occurs when DM-master sends gRPC requests to DM-worker.
- `scope=interal` indicates that the error occurs in DM.
- `level=high` indicates that it is a high-level error that needs your solution. Find out more details of it according to the error message and error stack.

### Error message description

DM uses the descriptive language to indicate the error details in an error message. The [errors.Wrap](https://godoc.org/github.com/pkg/errors#hdr-Adding_context_to_an_error) mode is adopted to wrap and store every additional layer of error message description on the error call chain. The message description wrapped at the outermost layer indicates the error in DM and the message description wrapped at the innermost layer indicates the error from the bottommost error location.

Taking the [above error message](#error-message-reference) as an example:

- The error message description of the outermost layer is `grpc request error`, which describes the error in DM.
- The error message description of the innermost layer is `connection error: desc = "transport: Error while dialing dial tcp 172.17.0.2:8262: connect: connection refused"`. It is the error returned when DM-master fails to established the gRPC connection at the bottom layer.

After analyzing the basic error information and the error message descriptions, you can determine that this error occurs when DM-master sends gRPC requests to DM-worker but it fails to establish the gRPC connection. This error occurs often because DM-worker is not working normally.

### Error stack information

DM decides whether to output the error stack information according to the severity of the error. The error stack records the complete stack trace information when the error occurs. If you cannot figure out the error cause based on the basic information and the error message descriptions, use the error stack information to further check the running path of the error code.

## Published error code

You can find out a complete list of error codes from the [published error codes](https://github.com/pingcap/dm/blob/master/_utils/terror_gen/errors_release.txt) in the DM code warehouse.

## Common error description and handling method

| Error code       | Error description                                                     |  Handling method                                                    |
| :----------- | :------------------------------------------------------------ | :----------------------------------------------------------- |
| `code=10001` |  Abnormal database operation.                                              |  Further analyze the error message and error stack.                                |
| `code=10002` | The `bad connection` error from the underlying database. It usually indicates that the connection between DM and the downstream TiDB instance is abnormal (possibly caused by network failure, TiDB restart and so on) and the currently requested data is not sent to TiDB. |  DM provides automatic recovery for such error. If the recovery is not successful for a long time, check the network or TiDB status. |
| `code=10003` | The `invalid connection` error from the underlying database. It usually indicates that the connection between DM and the downstream TiDB instance is abnormal (possibly caused by network failure, TiDB restart and so on) and the currently requested data is partly sent to TiDB.  | DM provides automatic recovery for such error. If the recovery is not successful for a long time, further check the error message and analyze the information based on the actual situation. |
| `code=10005` |  Occurs when performing the `QUERY` type SQL statements.                                         |                                                              |
| `code=10006` |  Occurs when performing the `EXECUTE` type SQL statements, including DDL statements and DML statements of the `INSERT`, `UPDATE`or `DELETE` type. For more detailed error information, check the error message which usually includes the error code and error information returned for database operations.
|                                                              |
| `code=11006` |  Occurs when the built-in parser of DM parses the incompatible DDL statements.          |  Refer to [Data Migration - incompatible DDL statements](/dev/how-to/troubleshoot/data-migration.md#incompatible-ddl-statements) for solution. |
| `code=20010` |   Occurs when decrypting the database password that is provided in task configuration.                   |  Check whether the downstream database password provided in the configuration task is [correctly encrypted using dmctl](/dev/how-to/deploy/data-migration-with-ansible.md#encrypt-the-upstream-mysql-user-password-using-dmctl). |
| `code=26002` |  The task check fails to establish database connection. For more detailed error information, check the error message which usually includes the error code and error information returned for database operations. |  Check whether the machine where DM-master is located has permission to access the upstream. |
| `code=32001` |   Abnormal dump processing unit                                            |  If the error message contains `mydumper: argument list too long.`, configure the table to be exported by manually adding the `--regex` regular expression in the Mydumper argument `extra-args` in the `task.yaml` file according to the black-white list. For example, to export all tables named `hello`, add `--regex '.*\\.hello$'`; to export all tables, add `--regex '.*'`. |
| `code=38008` |  An error occurs in the gRPC communication among DM components.                                     |   Check `class`. Find out the error occurs in the interaction of which components. Determine the type of communication error. If the error occurs when establishing gRPC connection, check whether the communication server is working normally. |
