---
title: 管理数据同步任务
category: reference
---

# 管理数据同步任务

本文介绍了如何使用 [dmctl](/reference/tools/data-migration/overview.md#dmctl) 组件来进行数据同步任务的管理和维护。对于用 DM-Ansible 部署的 DM 集群，dmctl 二进制文件路径为 `dm-ansible/dmctl`。

## dmctl 基本用法

本部分描述了一些 dmctl 命令的基本用法。

### dmctl 使用帮助

```bash
$ ./dmctl --help
Usage of dmctl:
 # 打印版本信息
 -V prints version and exit
 # 按照 DM 提供的加密方法加密数据库密码，用于 DM 的配置文件
 -encrypt string
       encrypt plaintext to ciphertext
 # DM-master 访问地址，dmctl 与 DM-master 交互以完成任务管理操作
 -master-addr string
       master API server addr
```

### 加密数据库密码

在 DM 相关配置文件中，要求必须使用经 dmctl 加密后的密码，否则会报错。对于同一个原始密码，每次加密后密码不同。

```bash
$ ./dmctl -encrypt 123456
VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU=
```

### 任务管理概览

```bash
# 进入命令行模式，与 DM-master 进行交互
$ ./dmctl -master-addr 172.16.30.14
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

# 使用 `dmctl [command] --help` 来获取某个命令的更多信息
```

## 管理数据同步任务

本部分描述了如何使用不同的任务管理命令来执行以下操作：

- [创建数据同步任务](#创建数据同步任务)
- [查询数据同步任务状态](#查询数据同步任务状态)
- [暂停数据同步任务](#暂停数据同步任务)
- [恢复数据同步任务](#恢复数据同步任务)
- [停止数据同步任务](#停止数据同步任务)
- [更新数据同步任务](#更新数据同步任务)

### 创建数据同步任务

`start-task` 命令用于创建数据同步任务。 当数据同步任务启动时，DM 将[自动对相应权限和配置进行前置检查](/reference/tools/data-migration/precheck.md)。

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

#### 命令用法示例

```bash
start-task [ -w "172.16.30.15:10081"] ./task.yaml
```

#### 参数解释

+ `-w`：
    - 可选
    - 指定在特定的一组 DM-workers 上执行 `task.yaml`
    - 如果设置，则只启动指定任务在该组 DM-workers 上的子任务
+ `config_file`：
    - 必选
    - 指定 `task.yaml` 的文件路径

#### 返回结果示例

```bash
» start-task task.yaml
{
     "result": true,
     "msg": "",
     "workers": [
         {
             "result": true,
             "worker": "172.16.30.15:10081",
             "msg": ""
         },
         {
             "result": true,
             "worker": "172.16.30.16:10081",
             "msg": ""
         }
     ]
}
```

### 查询数据同步任务状态

`query-status` 命令用于查询数据同步任务状态。有关查询结果及子任务状态，详见[查询状态](/reference/tools/data-migration/query-status.md)。

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

#### 命令用法示例

```bash
query-status
```

#### 参数解释

- `-w`：
    - 可选
    - 查询在指定的一组 DM-workers 上运行的数据同步任务的子任务
- `task_name`：
    - 可选 
    - 指定任务名称 
    - 如果未设置，则返回全部数据同步任务的查询结果

#### 返回结果示例

有关查询结果中各参数的意义，详见[查询状态结果](/reference/tools/data-migration/query-status.md#查询结果)。

```bash
» query-status
{
     "result": true,
     "msg": "",
     "workers": [
         {
             "result": true,
             "worker": "172.16.30.15:10081",
             "msg": "",
             "subTaskStatus": [
                 {
                     "name": "test",
                     "stage": "Running",
                     "unit": "Sync",
                     "result": null,
                     "unresolvedDDLLockID": "",
                     "sync": {
                         "TotalEvents": "0",
                         "TotalTps": "0",
                         "RecentTps": "0",
                         "MasterBinlog": "(mysql-bin.000004, 484)",
                         "MasterBinlogGtid": "",
                         "SyncerBinlog": "(mysql-bin.000004, 484)",
                         "SyncerBinlogGtid": "",
                        "blockingDDLs": [
                        ],
                        "unresolvedGroups": [
                        ]
                     }
                 }
             ],
             "relayStatus": {
                 "MasterBinlog": "(mysql-bin.000004, 484)",
                 "MasterBinlogGtid": "",
                "relaySubDir": "0-1.000001",
                 "RelayBinlog": "(mysql-bin.000004, 484)",
                 "RelayBinlogGtid": "",
                "relayCatchUpMaster": true,
                "stage": "Running",
                "result": null
             }
         },
         {
             "result": true,
             "worker": "172.16.30.16:10081",
             "msg": "",
             "subTaskStatus": [
                 {
                     "name": "test",
                     "stage": "Running",
                     "unit": "Sync",
                     "result": null,
                     "unresolvedDDLLockID": "",
                     "sync": {
                         "TotalEvents": "0",
                         "TotalTps": "0",
                         "RecentTps": "0",
                         "MasterBinlog": "(mysql-bin.000004, 4809)",
                         "MasterBinlogGtid": "",
                         "SyncerBinlog": "(mysql-bin.000004, 4809)",
                         "SyncerBinlogGtid": "",
                        "blockingDDLs": [
                        ],
                        "unresolvedGroups": [
                        ]
                     }
                 }
             ],
             "relayStatus": {
                 "MasterBinlog": "(mysql-bin.000004, 4809)",
                 "MasterBinlogGtid": "",
                "relaySubDir": "0-1.000001",
                 "RelayBinlog": "(mysql-bin.000004, 4809)",
                 "RelayBinlogGtid": "",
                "relayCatchUpMaster": true,
                "stage": "Running",
                "result": null
             }
         }
     ]
}
```

### 暂停数据同步任务

`pause-task` 命令用于暂停数据同步任务。

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

#### 命令用法示例

```bash
pause-task [-w "127.0.0.1:10181"] task-name
```

#### 参数解释

- `-w`：
    - 可选
    - 指定在特定的一组 DM-workers 上暂停数据同步任务的子任务
    - 如果设置，则只暂停该任务在指定 DM-workers 上的子任务
- `task_name`：
    - 必选
    - 指定任务名称

#### 返回结果示例

```bash
» pause-task test
{
     "op": "Pause",
     "result": true,
     "msg": "",
     "workers": [
         {
             "op": "Pause",
             "result": true,
             "worker": "172.16.30.15:10081",
             "msg": ""
         },
         {
             "op": "Pause",
             "result": true,
             "worker": "172.16.30.16:10081",
             "msg": ""
         }
     ]
}
```

### 恢复数据同步任务

`resume-task` 命令用于恢复数据同步任务。

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

#### 命令用法示例

```bash
resume-task [-w "127.0.0.1:10181"] task-name
```

#### 参数解释

- `-w`：
    - 可选
    - 指定在特定的一组 DM-workers 上恢复数据同步任务的子任务 
    - 如果设置，则只恢复该任务在指定 DM-workers 上的子任务
- `task_name`：
    - 必选
    - 指定任务名称

#### 返回结果示例

```bash
» resume-task test
{
     "op": "Resume",
     "result": true,
     "msg": "",
     "workers": [
         {
             "op": "Resume",
             "result": true,
             "worker": "172.16.30.15:10081",
             "msg": ""
         },
         {
             "op": "Resume",
             "result": true,
             "worker": "172.16.30.16:10081",
             "msg": ""
         }
     ]
}
```

### 停止数据同步任务

`stop-task` 命令用于停止数据同步任务。

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

#### 命令用法示例

```bash
stop-task [-w "127.0.0.1:10181"]  task-name
```

#### 参数解释

- `-w`：
    - 可选
    - 指定在特定的一组 DM-workers 上停止数据同步任务的子任务
    - 如果设置，则只停止该任务在指定 DM-workers 上的子任务
- `task_name`：
    - 必选
    - 指定任务名称

#### 返回结果示例

```bash
» stop-task test
{
     "op": "Stop",
     "result": true,
     "msg": "",
     "workers": [
         {
             "op": "Stop",
             "result": true,
             "worker": "172.16.30.15:10081",
             "msg": ""
         },
         {
             "op": "Stop",
             "result": true,
             "worker": "172.16.30.16:10081",
             "msg": ""
         }
     ]
}
```

### 更新数据同步任务

`update-task` 命令用于更新数据同步任务。

支持的更新项包括：

- 表路由规则
- 表黑白名单规则
- binlog 过滤规则
- 列值转换规则

其余项均不支持更新。

#### 支持更新项的更新步骤

1. 使用 `query-status <task-name>` 查询对应数据同步任务的状态。

    - 若 `stage` 不为 `Paused`，则先使用 `pause-task <task-name>` 暂停任务。

2. 在 `task.yaml` 文件中更新需要修改的自定义配置或者错误配置。

3. 使用 `update-task task.yaml` 更新任务配置。

4. 使用 `resume-task <task-name>` 恢复任务。

#### 不支持更新项的更新步骤

1. 使用 `query-status <task-name>` 查询对应数据同步任务的状态。

    - 若任务存在，则通过 `stop-task <task-name>` 停止任务。

2. 在 `task.yaml` 文件中更新需要修改的自定义配置或者错误配置。

3. 使用 `start-task <task-name>` 恢复任务。

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

#### 命令用法示例

```bash
update-task [-w "127.0.0.1:10181"] ./task.yaml
```

#### 参数解释

- `-w`：
    - 可选
    - 指定在特定的一组 DM-workers 上更新数据同步任务的子任务
    - 如果设置，则只更新指定 DM-workers 上的子任务配置
- `config_file`：
    - 必选
    - 指定 `task.yaml` 的文件路径

#### 返回结果示例

```bash
» update-task task_all_black.yaml
{
     "result": true,
     "msg": "",
     "workers": [
         {
             "result": true,
             "worker": "172.16.30.15:10081",
             "msg": ""
         },
         {
             "result": true,
             "worker": "172.16.30.16:10081",
             "msg": ""
         }
     ]
}
```

## 管理 DDL lock

详见[手动处理 sharding DDL lock](/reference/tools/data-migration/features/manually-handling-sharding-ddl-locks.md)。

## 强制刷新 `task => DM-workers` 映射关系

`refresh-worker-tasks` 命令用于强制刷新 DM-master 内存中维护的 `task => DM-workers` 映射关系。

> **注意：**
>
> 一般不需要使用此命令。仅当已确定 `task => DM-workers` 映射关系存在，但执行其它命令时仍提示必须刷新它时，你才需要使用此命令。
