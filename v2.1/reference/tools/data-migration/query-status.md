---
title: Data Migration Query Status
summary: Learn the DM query result and subtask status.
category: reference
---

# Data Migration Query Status

This document introduces the query result and subtask status of Data Migration (DM).

## Query result

```
» query-status
{
    "result": true,     # Whether the query is successful.
    "msg": "",          # Describes the cause for the unsuccessful query.
    "workers": [                            # DM-worker list.
        {
            "result": true,
            "worker": "172.17.0.2:8262",   # The `host:port` information of the DM-worker.
            "msg": "",
            "subTaskStatus": [              # The information of all the subtasks of the DM-worker.
                {
                    "name": "test",         # The name of the subtask.
                    "stage": "Running",     # The running status of the subtask, including "New", "Running", "Paused", "Stopped", and "Finished".
                    "unit": "Sync",         # The processing unit of DM, including "Check", "Dump", "Load", and "Sync".
                    "result": null,         # Displays the error information if a subtask fails.
                    "unresolvedDDLLockID": "test-`test`.`t_target`",    # The sharding DDL lock ID, used for manually handling the sharding DDL
                                                                        # lock in the abnormal condition.
                    "sync": {                   # The replication information of the `Sync` processing unit. This information is about the
                                                # same component with the current processing unit.
                        "totalEvents": "12",    # The total number of binlog events that are replicated in this subtask.
                        "totalTps": "1",        # The number of binlog events that are replicated in this subtask per second.
                        "recentTps": "1",       # The number of binlog events that are replicated in this subtask in the last one second.
                        "masterBinlog": "(bin.000001, 3234)",                               # The binlog position in the upstream database.
                        "masterBinlogGtid": "c0149e17-dff1-11e8-b6a8-0242ac110004:1-14",    # The GTID information in the upstream database.
                        "syncerBinlog": "(bin.000001, 2525)",                               # The position of the binlog that has been replicated
                                                                                            # in the `Sync` processing unit.
                        "syncerBinlogGtid": "",                                             # It is always empty because `Sync` does not use GTID to
                                                                                            # replicate data.
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
                                                # upstream. The save point is not refreshed in real time in the `Sync` background, so "false" of "synced"
                                                # does not always mean a replication delay exits.
                    }
                }
            ],
            "relayStatus": {    # The replication status of the relay log.
                "masterBinlog": "(bin.000001, 3234)",                               # The binlog position of the upstream database.
                "masterBinlogGtid": "c0149e17-dff1-11e8-b6a8-0242ac110004:1-14",    # The binlog GTID information of the upstream database.
                "relaySubDir": "c0149e17-dff1-11e8-b6a8-0242ac110004.000001",       # The currently used subdirectory of the relay log.
                "relayBinlog": "(bin.000001, 3234)",                                # The position of the binlog that has been pulled to the local storage.
                "relayBinlogGtid": "c0149e17-dff1-11e8-b6a8-0242ac110004:1-14",     # The GTID information of the binlog that has been pulled to the local
                                                                                    # storage.
                "relayCatchUpMaster": true,     # Whether the progress of replicating the relay log in the local storage has been the same as that in
                                                # the upstream.
                "stage": "Running",             # The status of the `Sync` processing unit of the relay log.
                "result": null
            },
            "sourceID": "172.17.0.2:3306"        # ID of the upstream instance or replication group
        },
        {
            "result": true,
            "worker": "172.17.0.3:8262",
            "msg": "",
            "subTaskStatus": [
                {
                    "name": "test",
                    "stage": "Running",
                    "unit": "Load",
                    "result": null,
                    "unresolvedDDLLockID": "",
                    "load": {                   # The replication information of the `Load` processing unit.
                        "finishedBytes": "115", # The number of bytes that have been loaded.
                        "totalBytes": "452",    # The total number of bytes that need to be loaded.
                        "progress": "25.44 %"   # The progress of the loading process.
                    }
                }
            ],
            "relayStatus": {
                "masterBinlog": "(bin.000001, 28507)",
                "masterBinlogGtid": "c0149e17-dff1-11e8-b6a8-0242ac110004:1-96",
                "relaySubDir": "c0149e17-dff1-11e8-b6a8-0242ac110004.000001",
                "relayBinlog": "(bin.000001, 28507)",
                "relayBinlogGtid": "c0149e17-dff1-11e8-b6a8-0242ac110004:1-96",
                "relayCatchUpMaster": true,
                "stage": "Running",
                "result": null
            },
            "sourceID": "172.17.0.3:3306"
        },
        {
            "result": true,
            "worker": "172.17.0.6:8262",
            "msg": "",
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
                        "progress": "0.00 %"
                    }
                }
            ],
            "relayStatus": {
                "masterBinlog": "(bin.000001, 1691)",
                "masterBinlogGtid": "97b5142f-e19c-11e8-808c-0242ac110005:1-9",
                "relaySubDir": "97b5142f-e19c-11e8-808c-0242ac110005.000001",
                "relayBinlog": "(bin.000001, 1691)",
                "relayBinlogGtid": "97b5142f-e19c-11e8-808c-0242ac110005:1-9",
                "relayCatchUpMaster": true,
                "stage": "Running",
                "result": null,
                "sourceID": "172.17.0.6:3306"
            }
        }
    ]
}

```

For the status description and status switch relationship of "stage" of "subTaskStatus" of "workers", see [Subtask status](#subtask-status).

For operation details of "unresolvedDDLLockID" of "subTaskStatus" of "workers", see [Handle Sharding DDL Locks Manually](/v2.1/reference/tools/data-migration/features/manually-handling-sharding-ddl-locks.md).

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
