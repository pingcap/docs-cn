---
title: TiDB Data Migration 查询状态
summary: 深入了解 TiDB Data Migration 如何查询数据迁移任务状态
aliases: ['/docs-cn/tidb-data-migration/dev/query-status/','/docs-cn/tidb-data-migration/dev/query-error/','/tidb-data-migration/dev/query-error/']
---

# TiDB Data Migration 查询状态

本文介绍 TiDB Data Migration (DM) `query-status` 命令的查询结果、任务状态与子任务状态。

## 查询结果

{{< copyable "" >}}

```bash
» query-status
```

```
{
    "result": true,     # 查询是否成功
    "msg": "",          # 查询失败原因描述
    "tasks": [          # 迁移 task 列表
        {
            "taskName": "test",         # 任务名称
            "taskStatus": "Running",    # 任务运行状态
            "sources": [                # 该任务的上游 MySQL 列表
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

关于 tasks 下的 taskStatus 状态的详细定义，请参阅[任务状态](#任务状态)。

推荐的 `query-status` 使用方法是：

1. 首先使用 query-status 查看各个 task 的运行状态是否正常。
2. 如果发现其中某一 task 状态有问题，通过 `query-status <出错任务的 taskName>` 来得到更详细的错误信息。

## 任务状态

DM 的迁移任务状态取决于其分配到 DM-worker 上的[子任务状态](#子任务状态)，定义见下表：

| 任务对应的所有子任务的状态 | 任务状态 |
| :--- | :--- |
| 任一子任务处于 “Paused” 状态且返回结果有错误信息 | Error - Some error occurred in subtask |
| 任一处于 Sync 阶段的子任务处于 “Running” 状态但其 Relay 处理单元未运行（处于 Error/Paused/Stopped 状态） | Error - Relay status is Error/Paused/Stopped |
| 任一子任务处于 “Paused” 状态且返回结果没有错误信息 | Paused |
| 所有子任务处于 “New” 状态 | New |
| 所有子任务处于 “Finished” 状态 | Finished |
| 所有子任务处于 “Stopped” 状态 | Stopped |
| 其他情况 | Running |

## 详情查询结果

{{< copyable "" >}}

```bash
» query-status test
```

```
{
    "result": true,     # 查询是否成功
    "msg": "",          # 查询失败原因描述
    "sources": [        # 上游 MySQL 列表
        {
            "result": true,
            "msg": "",
            "sourceStatus": {                   # 上游 MySQL 的信息
                "source": "mysql-replica-01",
                "worker": "worker1",
                "result": null,
                "relayStatus": null
            },
            "subTaskStatus": [              # 上游 MySQL 所有子任务的信息
                {
                    "name": "test",         # 子任务名称
                    "stage": "Running",     # 子任务运行状态，包括 “New”，“Running”，“Paused”，“Stopped” 以及 “Finished”
                    "unit": "Sync",         # DM 的处理单元，包括 “Check”，“Dump“，“Load” 以及 “Sync”
                    "result": null,         # 子任务失败时显示错误信息
                    "unresolvedDDLLockID": "test-`test`.`t_target`",    # sharding DDL lock ID，可用于异常情况下手动处理 sharding DDL lock
                    "sync": {                   # 当前 `Sync` 处理单元的迁移信息
                        "totalEvents": "12",    # 该子任务中迁移的 binlog event 总数
                        "totalTps": "1",        # 该子任务中每秒迁移的 binlog event 数量
                        "recentTps": "1",       # 该子任务中最后一秒迁移的 binlog event 数量
                        "masterBinlog": "(bin.000001, 3234)",                               # 上游数据库当前的 binlog position
                        "masterBinlogGtid": "c0149e17-dff1-11e8-b6a8-0242ac110004:1-14",    # 上游数据库当前的 GTID 信息
                        "syncerBinlog": "(bin.000001, 2525)",                               # 已被 `Sync` 处理单元迁移的 binlog position
                        "syncerBinlogGtid": "",                                             # 使用 GTID 迁移的 binlog position
                        "blockingDDLs": [       # 当前被阻塞的 DDL 列表。该项仅在当前 DM-worker 所有上游表都处于 “synced“ 状态时才有数值，此时该列表包含的是待执行或待跳过的 sharding DDL 语句
                            "USE `test`; ALTER TABLE `test`.`t_target` DROP COLUMN `age`;"
                        ],
                        "unresolvedGroups": [   # 没有被解决的 sharding group 信息
                            {
                                "target": "`test`.`t_target`",                  # 待迁移的下游表
                                "DDLs": [
                                    "USE `test`; ALTER TABLE `test`.`t_target` DROP COLUMN `age`;"
                                ],
                                "firstPos": "(bin|000001.000001, 3130)",        # sharding DDL 语句起始 binlog position
                                "synced": [                                     # `Sync` 处理单元已经读到该 sharding DDL 的上游分表
                                    "`test`.`t2`"
                                    "`test`.`t3`"
                                    "`test`.`t1`"
                                ],
                                "unsynced": [                                   # `Sync` 处理单元未读到该 sharding DDL 的上游分表。如有上游分表未完成同步，`blockingDDLs` 为空
                                ]
                            }
                        ],
                        "synced": false         # 增量复制是否已追上上游。由于后台 `Sync` 单元并不会实时刷新保存点，当前值为 “false“ 并不一定代表发生了迁移延迟
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
                    "load": {                   # `Load` 处理单元的迁移信息
                        "finishedBytes": "115", # 已全量导入字节数
                        "totalBytes": "452",    # 总计需要导入的字节数
                        "progress": "25.44 %"   # 全量导入进度
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
            ]
        }
    ]
}
```

关于 `sources` 下 `subTaskStatus` 中 `stage` 状态和状态转换关系的详细信息，请参阅[子任务状态](#子任务状态)。

关于 `sources` 下 `subTaskStatus` 中 `unresolvedDDLLockID`的操作细节，请参阅[手动处理 Sharding DDL Lock](/dm/manually-handling-sharding-ddl-locks.md)。

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
