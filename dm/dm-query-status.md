---
title: Query Task Status in TiDB Data Migration
summary: Learn how to query the status of a data replication task.
aliases: ['/docs/tidb-data-migration/dev/query-status/']
---

# Query Task Status in TiDB Data Migration

This document introduces how to use the `query-status` command to query the task status, and the subtask status of DM.

## Query result

{{< copyable "" >}}

```bash
» query-status
```

```
{
    "result": true,     # Whether the query is successful.
    "msg": "",          # Describes the reason for the unsuccessful query.
    "tasks": [          # Migration task list.
        {
            "taskName": "test",         # The task name.
            "taskStatus": "Running",    # The status of the task.
            "sources": [                # The upstream MySQL list.
                "mysql-replica-01",
                "mysql-replica-02"
            ]
        },
        {
            "taskName": "test2",
            "taskStatus": "Paused",
            "sources": [
                "mysql-replica-01",
                "mysql-replica-02"
            ]
        }
    ]
}
```

For detailed descriptions of `taskStatus` under the `tasks` section, refer to [Task status](#task-status).

It is recommended that you use `query-status` by the following steps:

1. Use `query-status` to check whether each on-going task is in the normal state.
2. If any error occurs in a task, use the `query-status <taskName>` command to see detailed error information. `<taskName>` in this command indicates the name of the task that encounters the error.

## Task status

The status of a DM migration task depends on the status of each subtask assigned to DM-worker. For detailed descriptions of subtask status, see [Subtask status](#subtask-status). The table below shows how the subtask status is related to task status.

|  Subtask status in a task | Task status |
| :--- | :--- |
| One subtask is in the `paused` state and error information is returned. | `Error - Some error occurred in subtask` |
| One subtask in the Sync phase is in the `Running` state but its Relay processing unit is not running (in the `Error`/`Paused`/`Stopped` state). | `Error - Relay status is Error/Paused/Stopped` |
| One subtask is in the `Paused` state and no error information is returned. | `Paused` |
| All subtasks are in the `New` state. | `New` |
| All subtasks are in the `Finished` state. | `Finished` |
| All subtasks are in the `Stopped` state. | `Stopped` |
| Other situations | `Running` |

## Detailed query result

{{< copyable "" >}}

```bash
» query-status test
```

```
» query-status
{
    "result": true,     # Whether the query is successful.
    "msg": "",          # Describes the cause for the unsuccessful query.
    "sources": [                            # The upstream MySQL list.
        {
            "result": true,
            "msg": "",
            "sourceStatus": {                   # The information of the upstream MySQL databases.
                "source": "mysql-replica-01",
                "worker": "worker1",
                "result": null,
                "relayStatus": null
            },
            "subTaskStatus": [              # The information of all subtasks of upstream MySQL databases.
                {
                    "name": "test",         # The name of the subtask.
                    "stage": "Running",     # The running status of the subtask, including "New", "Running", "Paused", "Stopped", and "Finished".
                    "unit": "Sync",         # The processing unit of DM, including "Check", "Dump", "Load", and "Sync".
                    "result": null,         # Displays the error information if a subtask fails.
                    "unresolvedDDLLockID": "test-`test`.`t_target`",    # The sharding DDL lock ID, used for manually handling the sharding DDL
                                                                        # lock in the abnormal condition.
                    "sync": {                   # The replication information of the `Sync` processing unit. This information is about the
                                                # same component with the current processing unit.
                        "masterBinlog": "(bin.000001, 3234)",                               # The binlog position in the upstream database.
                        "masterBinlogGtid": "c0149e17-dff1-11e8-b6a8-0242ac110004:1-14",    # The GTID information in the upstream database.
                        "syncerBinlog": "(bin.000001, 2525)",                               # The position of the binlog that has been replicated
                                                                                            # in the `Sync` processing unit.
                        "syncerBinlogGtid": "",                                             # The binlog position replicated using GTID.
                        "blockingDDLs": [       # The DDL list that is blocked currently. It is not empty only when all the upstream tables of this
                                                # DM-worker are in the "synced" status. In this case, it indicates the sharding DDL statements to be executed or that are skipped.
                            "USE `test`; ALTER TABLE `test`.`t_target` DROP COLUMN `age`;"
                        ],
                        "unresolvedGroups": [   # The sharding group that is not resolved.
                            {
                                "target": "`test`.`t_target`",                  # The downstream database table to be replicated.
                                "DDLs": [
                                    "USE `test`; ALTER TABLE `test`.`t_target` DROP COLUMN `age`;"
                                ],
                                "firstPos": "(bin|000001.000001, 3130)",        # The starting position of the sharding DDL statement.
                                "synced": [                                     # The upstream sharded table whose executed sharding DDL statement has been read by the `Sync` unit.
                                    "`test`.`t2`"
                                    "`test`.`t3`"
                                    "`test`.`t1`"
                                ],
                                "unsynced": [                                   # The upstream table that has not executed this sharding DDL
                                                                                # statement. If any upstream tables have not finished replication,
                                                                                # `blockingDDLs` is empty.
                                ]
                            }
                        ],
                        "synced": false         # Whether the incremental replication catches up with the upstream and has the same binlog position as that in the
                                                # upstream. The save point is not refreshed in real time in the `Sync` background, so `false` of `synced`
                                                # does not always mean a replication delay exits.
                        "totalRows": "12",      # The total number of rows that are replicated in this subtask.
                        "totalRps": "1",        # The number of rows that are replicated in this subtask per second.
                        "recentRps": "1"        # The number of rows that are replicated in this subtask in the last second.
                    }
                }
            ]
        },
        {
            "result": true,
            "msg": "",
            "sourceStatus": {
                "source": "mysql-replica-02",
                "worker": "worker2",
                "result": null,
                "relayStatus": null
            },
            "subTaskStatus": [
                {
                    "name": "test",
                    "stage": "Running",
                    "unit": "Load",
                    "result": null,
                    "unresolvedDDLLockID": "",
                    "load": {                   # The replication information of the `Load` processing unit.
                        "finishedBytes": "115",          # The number of bytes that have been loaded.
                        "totalBytes": "452",               # The total number of bytes that need to be loaded.
                        "progress": "25.44 %",         # The progress of the loading process.
                        "bps": "2734"                        # The speed of the full loading.
                    }
                }
            ]
        },
        {
            "result": true,
            "sourceStatus": {
                "source": "mysql-replica-03",
                "worker": "worker3",
                "result": null,
                "relayStatus": null
            },
            "subTaskStatus": [
                {
                    "name": "test",
                    "stage": "Paused",
                    "unit": "Load",
                    "result": {                 # The error example.
                        "isCanceled": false,
                        "errors": [
                            {
                                "Type": "ExecSQL",
                                "msg": "Error 1062: Duplicate entry '1155173304420532225' for key 'PRIMARY'\n/home/jenkins/workspace/build_dm/go/src/github.com/pingcap/tidb-enterprise-tools/loader/db.go:160: \n/home/jenkins/workspace/build_dm/go/src/github.com/pingcap/tidb-enterprise-tools/loader/db.go:105: \n/home/jenkins/workspace/build_dm/go/src/github.com/pingcap/tidb-enterprise-tools/loader/loader.go:138: file test.t1.sql"
                            }
                        ],
                        "detail": null
                    },
                    "unresolvedDDLLockID": "",
                    "load": {
                        "finishedBytes": "0",
                        "totalBytes": "156",
                        "progress": "0.00 %",
                        "bps": "0"
                    }
                }
            ]
        },
        {
            "result": true,
            "msg": "",
            "sourceStatus": {
                "source": "mysql-replica-04",
                "worker": "worker4",
                "result": null,
                "relayStatus": null
            },
            "subTaskStatus": [
                {
                    "name": "test",
                    "stage": "Running",
                    "unit": "Dump",
                    "result": null,
                    "unresolvedDDLLockID": "",
                    "dump": {                        # The replication information of the `Dump` processing unit.
                        "totalTables": "10",         # The number of tables to be dumped.
                        "completedTables": "3",      # The number of tables that have been dumped.
                        "finishedBytes": "2542",     # The number of bytes that have been dumped.
                        "finishedRows": "32",        # The number of rows that have been dumped.
                        "estimateTotalRows": "563",  # The estimated number of rows to be dumped.
                        "progress": "30.52 %",       # The progress of the dumping process.
                        "bps": "445"                 # The dumping speed.
                    }
                }
            ]
        },
    ]
}

```

For the status description and status switch relationship of "stage" of "subTaskStatus" of "sources", see the [subtask status](#subtask-status).

For operation details of "unresolvedDDLLockID" of "subTaskStatus" of "sources", see [Handle Sharding DDL Locks Manually](/dm/manually-handling-sharding-ddl-locks.md).

## Subtask status

### Status description

- `New`:

    - The initial status.
    - If the subtask does not encounter an error, it is switched to `Running`; otherwise it is switched to `Paused`.

- `Running`: The normal running status.

- `Paused`:

    - The paused status.
    - If the subtask encounters an error, it is switched to `Paused`.
    - If you run `pause-task` when the subtask is in the `Running` status, the task is switched to `Paused`.
    - When the subtask is in this status, you can run the `resume-task` command to resume the task.

- `Stopped`:

    - The stopped status.
    - If you run `stop-task` when the subtask is in the `Running` or `Paused` status, the task is switched to `Stopped`.
    - When the subtask is in this status, you cannot use `resume-task` to resume the task.

- `Finished`:

    - The finished subtask status.
    - Only when the full replication subtask is finished normally, the task is switched to this status.

### Status switch diagram

```
                                         error occurs
                            New --------------------------------|
                             |                                  |
                             |           resume-task            |
                             |  |----------------------------|  |
                             |  |                            |  |
                             |  |                            |  |
                             v  v        error occurs        |  v
  Finished <-------------- Running -----------------------> Paused
                             ^  |        or pause-task       |
                             |  |                            |
                  start task |  | stop task                  |
                             |  |                            |
                             |  v        stop task           |
                           Stopped <-------------------------|
```
