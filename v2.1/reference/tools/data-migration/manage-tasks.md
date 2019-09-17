---
title: Manage the Data Replication Task
summary: Use dmctl to manage the data replication task.
category: reference
---

# Manage the Data Replication Task

This document describes how to manage and maintain the data replication task using the [dmctl](/v2.1/reference/tools/data-migration/overview.md#dmctl) component. For the Data Migration cluster deployed using DM-Ansible, the dmctl binary file is in `dm-ansible/dmctl`.

## dmctl basic usage

This section shows the basic usage of dmctl commands.

### dmctl help

```bash
$ ./dmctl --help
Usage of dmctl:
 # Prints the version information.
 -V prints version and exit
 # Encrypts the database password according to the encryption method provided by DM; used in DM configuration files.
 -encrypt string
       encrypt plaintext to ciphertext
 # The dm-master access address. dmctl interacts with dm-master to complete task management operations.
 -master-addr string
       master API server addr
```

### Database password encryption

In DM configuration files, you need to use the password encrypted using dmctl, otherwise an error occurs. For a same original password, the password is different after each encryption.

```bash
$ ./dmctl -encrypt 123456
VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU=
```

### Task management overview

```bash
# Enters the command line mode to interact with DM-master.
$ ./dmctl -master-addr 172.16.30.14:8261
Welcome to dmctl
Release Version: v1.0.0-100-g2bef6f8b
Git Commit Hash: 2bef6f8beda34c0dff57377005c71589b48aa3c5
Git Branch: dm-master
UTC Build Time: 2018-11-02 10:03:18
Go Version: go version go1.11 linux/amd64

» help
DM control

Usage:
  dmctl [command]

Available Commands:
  break-ddl-lock       force to break DM-worker's DDL lock
  generate-task-config generate a task config with config file
  help                 Help about any command
  pause-relay          pause DM-worker's relay unit
  pause-task           pause a running task with name
  query-status         query task's status
  refresh-worker-tasks refresh worker -> tasks mapper
  resume-relay         resume DM-worker's relay unit
  resume-task          resume a paused task with name
  show-ddl-locks       show un-resolved DDL locks
  sql-inject           sql-inject injects (limited) sqls into syncer as binlog event
  sql-replace          sql-replace replaces sql in specific binlog_pos with other sqls, each sql must ends with semicolon;
  sql-skip             sql-skip skips specified binlog position
  start-task           start a task with config file
  stop-task            stop a task with name
  switch-relay-master  switch master server of DM-worker's relay unit
  unlock-ddl-lock      force to unlock DDL lock
  update-master-config update configure of DM-master
  update-task          update a task's config for routes, filters, column-mappings, black-white-list

Flags:
  -h, --help             help for dmctl
  -w, --worker strings   DM-worker ID

# Use "dmctl [command] --help" for more information about a command.
```

## Manage the data replication task

This section describes how to use the task management commands to execute the following operations:

- [Create the data replication task](#create-the-data-replication-task)
- [Check the data replication task status](#check-the-data-replication-task-status)
- [Pause the data replication task](#pause-the-data-replication-task)
- [Restart the data replication task](#restart-the-data-replication-task)
- [Stop the data replication task](#stop-the-data-replication-task)
- [Update the data replication task](#update-the-data-replication-task)

### Create the data replication task

You can use the task management command to create the data replication task. Data Migration [prechecks the corresponding privileges and configuration automatically](/v2.1/reference/tools/data-migration/precheck.md) while starting the data replication.

```bash
» help start-task
start a task with config file

Usage:
 dmctl start-task [-w worker ...] <config_file> [flags]

Flags:
 -h, --help   help for start-task

Global Flags:
 -w, --worker strings   dm-worker ID
```

#### Command usage example

```bash
start-task [ -w "172.16.30.15:10081"] ./task.yaml
```

#### Flags description

- `-w`: (Optional) This flag specifies the group of DM-workers to execute `task.yaml`. If it is set, only subtasks of the specified task on these DM-workers are started.
- `config_file`: (Required) This flag specifies the file path of `task.yaml`.

#### Returned results

```bash
{
​    "result": true,
​    "msg": "",
​    "workers": [
​        {
​            "result": true,
​            "worker": "172.16.30.15:10081",
​            "msg": ""
​        },
​        {
​            "result": true,
​            "worker": "172.16.30.16:10081",
​            "msg": ""
​        }
​    ]
}
```

### Check the data replication task status

You can use the `query-status` task management command to check the status of the data replication task. For details about the query result and subtask status, see [Query Status](/v2.1/reference/tools/data-migration/query-status.md).

```bash
» help query-status
query task's status

Usage:
 dmctl query-status [-w worker ...] [task_name] [flags]

Flags:
 -h, --help   help for query-status

Global Flags:
 -w, --worker strings   dm-worker ID
```

#### Command usage example

```bash
query-status
```

#### Flags description

- `-w`: (Optional) This flag specifies the group of DM-workers where the subtasks of the replication task (that you want to query) run.
- `task_name`: (Optional) This flag specifies the task name. If it is not set, the results of all data replication tasks are returned.

#### Returned results

```bash
» query-status
{
​    "result": true,
​    "msg": "",
​    "workers": [
​        {
​            "result": true,
​            "worker": "172.16.30.15:10081",
​            "msg": "",
​            "subTaskStatus": [
​                {
​                    "name": "test",
​                    "stage": "Running",
​                    "unit": "Sync",
​                    "result": null,
​                    "unresolvedDDLLockID": "",
​                    "sync": {
​                        "TotalEvents": "0",
​                        "TotalTps": "0",
​                        "RecentTps": "0",
​                        "MasterBinlog": "(mysql-bin.000004, 484)",
​                        "MasterBinlogGtid": "",
​                        "SyncerBinlog": "(mysql-bin.000004, 484)",
​                        "SyncerBinlogGtid": "",
                        "blockingDDLs": [
                        ],
                        "unresolvedGroups": [
                        ]
​                    }
​                }
​            ],
​            "relayStatus": {
​                "MasterBinlog": "(mysql-bin.000004, 484)",
​                "MasterBinlogGtid": "",
                "relaySubDir": "0-1.000001",
​                "RelayBinlog": "(mysql-bin.000004, 484)",
​                "RelayBinlogGtid": "",
                "relayCatchUpMaster": true,
                "stage": "Running",
                "result": null
​            }
​        },
​        {
​            "result": true,
​            "worker": "172.16.30.16:10081",
​            "msg": "",
​            "subTaskStatus": [
​                {
​                    "name": "test",
​                    "stage": "Running",
​                    "unit": "Sync",
​                    "result": null,
​                    "unresolvedDDLLockID": "",
​                    "sync": {
​                        "TotalEvents": "0",
​                        "TotalTps": "0",
​                        "RecentTps": "0",
​                        "MasterBinlog": "(mysql-bin.000004, 4809)",
​                        "MasterBinlogGtid": "",
​                        "SyncerBinlog": "(mysql-bin.000004, 4809)",
​                        "SyncerBinlogGtid": "",
                        "blockingDDLs": [
                        ],
                        "unresolvedGroups": [
                        ]
​                    }
​                }
​            ],
​            "relayStatus": {
​                "MasterBinlog": "(mysql-bin.000004, 4809)",
​                "MasterBinlogGtid": "",
                "relaySubDir": "0-1.000001",
​                "RelayBinlog": "(mysql-bin.000004, 4809)",
​                "RelayBinlogGtid": "",
                "relayCatchUpMaster": true,
                "stage": "Running",
                "result": null
​            }
​        }
​    ]
}
```

### Pause the data replication task

You can use the task management command to pause the data replication task.

```bash
» help pause-task
pause a running task with name

Usage:
 dmctl pause-task [-w worker ...] <task_name> [flags]

Flags:
 -h, --help   help for pause-task

Global Flags:
 -w, --worker strings   DM-worker ID
```

#### Command usage example

```bash
pause-task [-w "127.0.0.1:10181"] task-name
```

#### Flags description

- `-w`: (Optional) This flag specifies the group of DM-workers where the subtasks of the replication task (that you want to pause) run. If it is set, only subtasks on the specified DM-workers are paused.
- `task_name`: (Required) This flag specifies the task name.

#### Returned results

```bash
» pause-task test
{
​    "op": "Pause",
​    "result": true,
​    "msg": "",
​    "workers": [
​        {
​            "op": "Pause",
​            "result": true,
​            "worker": "172.16.30.15:10081",
​            "msg": ""
​        },
​        {
​            "op": "Pause",
​            "result": true,
​            "worker": "172.16.30.16:10081",
​            "msg": ""
​        }
​    ]
}
```

### Restart the data replication task

You can use the task management command to restart the data replication task.

```bash
» help resume-task
resume a paused task with name

Usage:
 dmctl resume-task [-w worker ...] <task_name> [flags]

Flags:
 -h, --help   help for resume-task

Global Flags:
 -w, --worker strings   dm-worker ID
```

#### Command usage example

```bash
resume-task [-w "127.0.0.1:10181"] task-name
```

#### Flags description

- `-w`: (Optional) This flag specifies the group of DM-workers where the subtasks of the replication task (that you want to restart) run. If it is set, only subtasks on the specified DM-workers are restarted.
- `task_name`: (Required) This flag specifies the task name.

#### Returned results

```bash
» resume-task test
{
​    "op": "Resume",
​    "result": true,
​    "msg": "",
​    "workers": [
​        {
​            "op": "Resume",
​            "result": true,
​            "worker": "172.16.30.15:10081",
​            "msg": ""
​        },
​        {
​            "op": "Resume",
​            "result": true,
​            "worker": "172.16.30.16:10081",
​            "msg": ""
​        }
​    ]
}
```

### Stop the data replication task

You can use the task management command to stop the data replication task.

```bash
» help stop-task
stop a task with name

Usage:
 dmctl stop-task [-w worker ...] <task_name> [flags]

Flags:
 -h, --help   help for stop-task

Global Flags:
 -w, --worker strings   dm-worker ID
```

#### Command usage example

```bash
stop-task [-w "127.0.0.1:10181"]  task-name
```

#### Flags description

- `-w`: (Optional) This flag specifies the group of DM-workers where the subtasks of the replication task (that you want to stop) run. If it is set, only subtasks on the specified DM-workers are stopped.
- `task_name`: (Required) This flag specifies the task name.

#### Returned results

```bash
» stop-task test
{
​    "op": "Stop",
​    "result": true,
​    "msg": "",
​    "workers": [
​        {
​            "op": "Stop",
​            "result": true,
​            "worker": "172.16.30.15:10081",
​            "msg": ""
​        },
​        {
​            "op": "Stop",
​            "result": true,
​            "worker": "172.16.30.16:10081",
​            "msg": ""
​        }
​    ]
}
```

### Update the data replication task

You can use the task management command to update the data replication task. The following items support online update, while all other items do not support online update.

- table route rules
- black white list
- binlog filter rules
- column mapping  rules

#### Update items that support online update

1. Check the status of the corresponding data replication task using `query-status <task-name>`.

    If `stage` is not `Paused`, use `pause-task <task-name>` to pause the task.

2. Edit the `task.yaml` file to update the custom configuration that you need to modify and the incorrect configuration.

3. Update the task configuration using `update-task task.yaml`.

4. Restart the task using `resume-task <task-name>`.

#### Update items that do not support online update

1. Check the status of the corresponding data replication task using `query-status <task-name>`.

    If the task exists, use `stop-task <task-name>` to stop the task.

2. Edit the `task.yaml` file to update the custom configuration that you need to modify and the incorrect configuration.

3. Restart the task using `start-task <task-name>`.

#### Command usage help

```bash
» help update-task
update a task's config for routes, filters, column-mappings, black-white-list

Usage:
  dmctl update-task [-w worker ...] <config_file> [flags]

Flags:
  -h, --help   help for update-task

Global Flags:
  -w, --worker strings   dm-worker ID
```

#### Command usage example

```bash
update-task [-w "127.0.0.1:10181"] ./task.yaml
```

#### Flags description

- `-w`: (Optional) This flag specifies the group of DM-workers where the subtasks of the replication task (that you want to update) run. If it is set, only subtasks on the specified DM-workers are updated.
- `config_file`: (Required) This flag specifies the file path of `task.yaml`.

#### Returned results

```bash
» update-task task_all_black.yaml
{
​    "result": true,
​    "msg": "",
​    "workers": [
​        {
​            "result": true,
​            "worker": "172.16.30.15:10081",
​            "msg": ""
​        },
​        {
​            "result": true,
​            "worker": "172.16.30.16:10081",
​            "msg": ""
​        }
​    ]
}
```

## Manage the DDL locks

See [Handle Sharding DDL Locks Manually](/v2.1/reference/tools/data-migration/features/manually-handling-sharding-ddl-locks.md).

## Refresh worker tasks

You can use the `refresh-worker-tasks` command to forcefully refresh the `task => DM-workers` mapping maintained in the DM-master memory.

> **Note:**
>
> Generally, you do not need to use it. You can use it only when you are ensured that the `task => DM-workers` mapping exists, but you are still prompted to refresh while you are executing other commands.
