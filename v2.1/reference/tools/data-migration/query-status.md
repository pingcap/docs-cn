---
title: DM 查询状态
category: reference
---

# DM 查询状态

本文介绍 DM（Data Migration）`query-status` 命令的查询结果以及子任务状态。

## 查询结果

```
» query-status
{
    "result": true,     # 查询是否成功。
    "msg": "",          # 查询失败原因描述。
    "workers": [                            # DM-worker 列表。
        {
            "result": true,
            "worker": "172.17.0.2:10081",   # DM-worker ID。
            "msg": "",
            "subTaskStatus": [              # DM-worker 所有子任务的信息。
                {
                    "name": "test",         # 子任务名称。
                    "stage": "Running",     # 子任务运行状态，包括 “New”，“Running”，“Paused”，“Stopped” 以及 “Finished”。
                    "unit": "Sync",         # DM 的处理单元，包括 “Check”，“Dump“，“Load” 以及 “Sync”。
                    "result": null,         # 子任务失败时显示错误信息。
                    "unresolvedDDLLockID": "test-`test`.`t_target`",    # sharding DDL lock ID，可用于异常情况下手动处理 sharding DDL lock。
                    "sync": {                   # 当前 `Sync` 处理单元的同步信息。
                        "totalEvents": "12",    # 该子任务中同步的 binlog event 总数。
                        "totalTps": "1",        # 该子任务中每秒同步的 binlog event 数量。
                        "recentTps": "1",       # 该子任务中最后一秒同步的 binlog event 数量。
                        "masterBinlog": "(bin.000001, 3234)",                               # 上游数据库当前的 binlog position。
                        "masterBinlogGtid": "c0149e17-dff1-11e8-b6a8-0242ac110004:1-14",    # 上游数据库当前的 GTID 信息。
                        "syncerBinlog": "(bin.000001, 2525)",                               # 已被 `Sync` 处理单元同步的 binlog position。
                        "syncerBinlogGtid": "",                                             # 当前版本总是为空（因为 `Sync` 处理单元暂不使用 GTID 同步数据）。
                        "blockingDDLs": [       # 当前被阻塞的 DDL 列表。该项仅在当前 DM-worker 所有上游表都处于 “synced“ 状态时才有数值，此时该列表包含的是待执行或待跳过的 sharding DDL 语句.
                            "USE `test`; ALTER TABLE `test`.`t_target` DROP COLUMN `age`;"
                        ],
                        "unresolvedGroups": [   # 没有被解决的 sharding group 信息。
                            {
                                "target": "`test`.`t_target`",                  # 待同步的下游表。
                                "DDLs": [
                                    "USE `test`; ALTER TABLE `test`.`t_target` DROP COLUMN `age`;"
                                ],
                                "firstPos": "(bin|000001.000001, 3130)",        # sharding DDL 语句起始 binlog position。
                                "synced": [                                     # `Sync` 处理单元已经读到该 sharding DDL 的上游分表。
                                    "`test`.`t2`"
                                    "`test`.`t3`"
                                    "`test`.`t1`"
                                ],
                                "unsynced": [                                   # `Sync` 处理单元未读到该 sharding DDL 的上游分表。如有上游分表未完成同步，`blockingDDLs` 为空。
                                ]
                            }
                        ],
                        "synced": false         # 增量同步是否已追上上游。由于后台 `Sync` 单元并不会实时刷新保存点，当前值为 “false“ 并不一定代表发生了同步延迟。
                    }
                }
            ],
            "relayStatus": {    # relay 单元的同步状态.
                "masterBinlog": "(bin.000001, 3234)",                               # 上游数据库的 binlog position。
                "masterBinlogGtid": "c0149e17-dff1-11e8-b6a8-0242ac110004:1-14",    # 上游数据库的 binlog GTID 信息。
                "relaySubDir": "c0149e17-dff1-11e8-b6a8-0242ac110004.000001",       # 当前使用的 relay log 子目录。
                "relayBinlog": "(bin.000001, 3234)",                                # 已被拉取至本地存储的 binlog position。
                "relayBinlogGtid": "c0149e17-dff1-11e8-b6a8-0242ac110004:1-14",     # 已被拉取至本地存储的 binlog GTID 信息。
                "relayCatchUpMaster": true,     # 本地 relay log 同步进度是否与上游一致。
                "stage": "Running",             # relay 处理单元状态
                "result": null
            }
        },
        {
            "result": true,
            "worker": "172.17.0.3:10081",
            "msg": "",
            "subTaskStatus": [
                {
                    "name": "test",
                    "stage": "Running",
                    "unit": "Load",
                    "result": null,
                    "unresolvedDDLLockID": "",
                    "load": {                   # `Load` 处理单元的同步信息。
                        "finishedBytes": "115", # 已全量导入字节数。
                        "totalBytes": "452",    # 总计需要导入的字节数。
                        "progress": "25.44 %"   # 全量导入进度。
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
            }
        },
        {
            "result": true,
            "worker": "172.17.0.6:10081",
            "msg": "",
            "subTaskStatus": [
                {
                    "name": "test",
                    "stage": "Paused",
                    "unit": "Load",
                    "result": {                 # 错误示例
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
                "result": null
            }
        }
    ]
}

```

关于 `workers` 下 `subTaskStatus` 中 `stage` 状态和状态转换关系的详细信息，请参阅[子任务状态](#子任务状态)。

关于 `workers` 下 `subTaskStatus` 中 `unresolvedDDLLockID`的操作细节，请参阅[手动处理 Sharding DDL Lock](/v2.1/reference/tools/data-migration/features/manually-handling-sharding-ddl-locks.md)。

## 子任务状态

### 状态描述

- `New`：

    - 初始状态。
    - 如果子任务没有发生错误，状态切换为 `Running`，其他情况则切换为 `Paused`。

- `Running`：正常运行状态。

- `Paused`：

    - 暂停状态。
    - 子任务发生错误，状态切换为 `Paused`。
    - 如在子任务为 `Running` 状态下执行 `pause-task` 命令，任务状态会切换为 `Paused`。
    - 如子任务处于该状态，可以使用 `resume-task` 命令恢复任务。

- `Stopped`：

    - 停止状态。
    - 如在子任务为 `Running` 或 `Paused` 状态下执行 `stop-task` 命令，任务状态会切换为 `Stopped`。
    - 如子任务处于该状态，不可使用 `resume-task` 命令恢复任务。

- `Finished`：

    - 任务完成状态。
    - 只有 `task-mode` 为 `full` 的任务正常完成后，任务才会切换为该状态。

### 状态转换图

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
