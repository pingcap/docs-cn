---
title: 管理数据同步任务
category: reference
aliases: ['/docs-cn/tools/dm/manage-task/']
---

# 管理数据同步任务

本文介绍了如何使用 [dmctl](/v3.0/reference/tools/data-migration/overview.md#dmctl) 组件来进行数据同步任务的管理和维护。对于用 DM-Ansible 部署的 DM 集群，dmctl 二进制文件路径为 `dm-ansible/dmctl`。

## dmctl 基本用法

本部分描述了一些 dmctl 命令的基本用法。

### dmctl 使用帮助

{{< copyable "shell-regular" >}}

```bash
./dmctl --help
./dmctl --help
```

```
Usage of dmctl:
 -V prints version and exit
 -config string
       path to config file
 # 按照 DM 提供的加密方法加密数据库密码，用于 DM 的配置文件
 -encrypt string
       encrypt plaintext to ciphertext
 # DM-master 访问地址，dmctl 与 DM-master 交互以完成任务管理操作
 -master-addr string
       master API server addr
 -rpc-timeout string
       rpc timeout, default is 10m (default "10m")
```

### 加密数据库密码

在 DM 相关配置文件中，要求必须使用经 dmctl 加密后的密码，否则会报错。对于同一个原始密码，每次加密后密码不同。

{{< copyable "shell-regular" >}}

```bash
./dmctl -encrypt 123456
```

```
VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU=
```

### 任务管理概览

进入命令行模式，与 DM-master 进行交互：

{{< copyable "shell-regular" >}}

```bash
./dmctl -master-addr 172.16.30.14:8261
```

```
Welcome to dmctl
Release Version: v1.0.1
Git Commit Hash: e63c6cdebea0edcf2ef8c91d84cff4aaa5fc2df7
Git Branch: release-1.0
UTC Build Time: 2019-09-10 06:15:05
Go Version: go version go1.12 linux/amd64

» help
DM control

Usage:
  dmctl [command]

Available Commands:
  break-ddl-lock       forcefully break DM-worker's DDL lock
  check-task           check the config file of the task
  help                 help about any command
  migrate-relay        migrate DM-worker's relay unit
  pause-relay          pause DM-worker's relay unit
  pause-task           pause a specified running task
  purge-relay          purge relay log files of the DM-worker according to the specified filename
  query-error          query task error
  query-status         query task status
  refresh-worker-tasks refresh worker -> tasks mapper
  resume-relay         resume DM-worker's relay unit
  resume-task          resume a specified paused task
  show-ddl-locks       show un-resolved DDL locks
  sql-inject           inject (limited) SQLs into binlog replication unit as binlog events
  sql-replace          replace SQLs matched by a specific binlog position (binlog-pos) or a SQL pattern (sql-pattern); each SQL must end with a semicolon
  sql-skip             skip the binlog event matched by a specific binlog position (binlog-pos) or a SQL pattern (sql-pattern)
  start-task           start a task as defined in the config file
  stop-task            stop a specified task
  switch-relay-master  switch the master server of the DM-worker's relay unit
  unlock-ddl-lock      forcefully unlock DDL lock
  update-master-config update the config of the DM-master
  update-relay         update the relay unit config of the DM-worker
  update-task          update a task's config for routes, filters, column-mappings, or black-white-list

Flags:
  -h, --help             help for dmctl
  -w, --worker strings   DM-worker ID

# 使用 `dmctl [command] --help` 来获取某个命令的更多信息
```

## 管理数据同步任务

本部分描述了如何使用不同的任务管理命令来执行相应操作。

### 创建数据同步任务

`start-task` 命令用于创建数据同步任务。 当数据同步任务启动时，DM 将[自动对相应权限和配置进行前置检查](/v3.0/reference/tools/data-migration/precheck.md)。

{{< copyable "" >}}

```bash
help start-task
```

```
start a task as defined in the config file

Usage:
 dmctl start-task [-w worker ...] <config_file> [flags]

Flags:
 -h, --help   help for start-task

Global Flags:
 -w, --worker strings   DM-worker ID
```

#### 命令用法示例

{{< copyable "" >}}

```bash
start-task [ -w "172.16.30.15:8262"] ./task.yaml
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

{{< copyable "" >}}

```bash
start-task task.yaml
```

```
{
     "result": true,
     "msg": "",
     "workers": [
         {
             "result": true,
             "worker": "172.16.30.15:8262",
             "msg": ""
         },
         {
             "result": true,
             "worker": "172.16.30.16:8262",
             "msg": ""
         }
     ]
}
```

### 查询数据同步任务状态

`query-status` 命令用于查询数据同步任务状态。有关查询结果及子任务状态，详见[查询状态](/v3.0/reference/tools/data-migration/query-status.md)。

{{< copyable "" >}}

```bash
help query-status
```

```
query task status

Usage:
 dmctl query-status [-w worker ...] [task-name] [flags]

Flags:
 -h, --help   help for query-status

Global Flags:
 -w, --worker strings   DM-worker ID
```

#### 命令用法示例

{{< copyable "" >}}

```bash
query-status
```

#### 参数解释

- `-w`：
    - 可选
    - 查询在指定的一组 DM-workers 上运行的数据同步任务的子任务
- `task-name`：
    - 可选
    - 指定任务名称
    - 如果未设置，则返回全部数据同步任务的查询结果

#### 返回结果示例

有关查询结果中各参数的意义，详见[查询状态结果](/v3.0/reference/tools/data-migration/query-status.md#查询结果)。

### 查询运行错误

`query-error` 可用于查询数据同步任务与 relay 处理单元的错误信息。相比于 `query-status`，`query-error` 一般不用于获取除错误信息之外的其他信息。

`query-error` 常用于获取 `sql-skip`/`sql-replace` 所需的 binlog position 信息，有关 `query-error` 的参数与结果解释，请参考 [跳过 (skip) 或替代执行 (replace) 异常的 SQL 语句 文档中的 query-error](/v3.0/reference/tools/data-migration/skip-replace-sqls.md#query-error)。

### 暂停数据同步任务

`pause-task` 命令用于暂停数据同步任务。

> **注意：**
>
> 有关 `pause-task` 与 `stop-task` 的区别如下：
>
> - 使用 `pause-task` 仅暂停同步任务的执行，但仍然会在内存中保留任务的状态信息等，且可通过 `query-status` 进行查询；使用 `stop-task` 会停止同步任务的执行，并移除内存中与该任务相关的信息，且不可再通过 `query-status` 进行查询，但不会移除已经写入到下游数据库中的数据以及其中的 checkpoint 等 `dm_meta` 信息。
> - 使用 `pause-task` 暂停同步任务期间，由于任务本身仍然存在，因此不能再启动同名的新任务，且会阻止对该任务所需 relay log 的清理；使用 `stop-task` 停止任务后，由于任务不再存在，因此可以再启动同名的新任务，且不会阻止对 relay log 的清理。
> - `pause-task` 一般用于临时暂停同步任务以排查问题等；`stop-task` 一般用于永久删除同步任务或通过与 `start-task` 配合以更新配置信息。

{{< copyable "" >}}

```bash
help pause-task
```

```
pause a specified running task

Usage:
 dmctl pause-task [-w worker ...] <task-name> [flags]

Flags:
 -h, --help   help for pause-task

Global Flags:
 -w, --worker strings   DM-worker ID
```

#### 命令用法示例

{{< copyable "" >}}

```bash
pause-task [-w "127.0.0.1:8262"] task-name
```

#### 参数解释

- `-w`：
    - 可选
    - 指定在特定的一组 DM-workers 上暂停数据同步任务的子任务
    - 如果设置，则只暂停该任务在指定 DM-workers 上的子任务
- `task-name`：
    - 必选
    - 指定任务名称

#### 返回结果示例

{{< copyable "" >}}

```bash
pause-task test
```

```
{
     "op": "Pause",
     "result": true,
     "msg": "",
     "workers": [
         {
            "meta": {
                "result": true,
                "worker": "172.16.30.15:8262",
                "msg": ""
            },
            "op": "Pause",
            "logID": "2"
         },
         {
            "meta": {
                "result": true,
                "worker": "172.16.30.16:8262",
                "msg": ""
            },
            "op": "Pause",
            "logID": "2"
         }
     ]
}
```

### 恢复数据同步任务

`resume-task` 命令用于恢复处于 `Paused` 状态的数据同步任务，通常用于在人为处理完造成同步任务暂停的故障后手动恢复同步任务。

{{< copyable "" >}}

```bash
help resume-task
```

```
resume a specified paused task

Usage:
 dmctl resume-task [-w worker ...] <task-name> [flags]

Flags:
 -h, --help   help for resume-task

Global Flags:
 -w, --worker strings   DM-worker ID
```

#### 命令用法示例

{{< copyable "" >}}

```bash
resume-task [-w "127.0.0.1:8262"] task-name
```

#### 参数解释

- `-w`：
    - 可选
    - 指定在特定的一组 DM-workers 上恢复数据同步任务的子任务
    - 如果设置，则只恢复该任务在指定 DM-workers 上的子任务
- `task-name`：
    - 必选
    - 指定任务名称

#### 返回结果示例

{{< copyable "" >}}

```bash
resume-task test
```

```
{
     "op": "Resume",
     "result": true,
     "msg": "",
     "workers": [
         {
             "meta": {
                 "result": true,
                 "worker": "172.16.30.15:8262",
                 "msg": ""
             },
             "op": "Resume",
             "logID": "3"
         },
         {
             "meta": {
                 "result": true,
                 "worker": "172.16.30.16:8262",
                 "msg": ""
             },
             "op": "Resume",
             "logID": "3"
         }
     ]
}
```

### 停止数据同步任务

`stop-task` 命令用于停止数据同步任务。有关 `stop-task` 与 `pause-task` 的区别，请参考[暂停数据同步任务](#暂停数据同步任务)中的相关说明。

{{< copyable "" >}}

```bash
help stop-task
```

```
stop a specified task

Usage:
 dmctl stop-task [-w worker ...] <task-name> [flags]

Flags:
 -h, --help   help for stop-task

Global Flags:
 -w, --worker strings   DM-worker ID
```

#### 命令用法示例

{{< copyable "" >}}

```bash
stop-task [-w "127.0.0.1:8262"]  task-name
```

#### 参数解释

- `-w`：
    - 可选
    - 指定在特定的一组 DM-workers 上停止数据同步任务的子任务
    - 如果设置，则只停止该任务在指定 DM-workers 上的子任务
- `task-name`：
    - 必选
    - 指定任务名称

#### 返回结果示例

{{< copyable "" >}}

```bash
stop-task test
```

```
{
     "op": "Stop",
     "result": true,
     "msg": "",
     "workers": [
         {
             "meta": {
                 "result": true,
                 "worker": "172.16.30.15:8262",
                 "msg": ""
             },
             "op": "Stop",
             "logID": "4"
         },
         {
             "meta": {
                 "result": true,
                 "worker": "172.16.30.16:8262",
                 "msg": ""
             },
             "op": "Stop",
             "logID": "4"
         }
     ]
}
```

### 更新数据同步任务

`update-task` 命令用于更新数据同步任务。

支持的更新项包括：

- Table routing 规则
- Black & white table lists 规则
- Binlog event filter 规则
- Column mapping 规则

其余项均不支持更新。

> **注意：**
>
> 如果能确保同步任务所需的 relay log 在任务停止期间不会被清理，则推荐使用[不支持更新项的更新步骤](#不支持更新项的更新步骤)来以统一的方式更新任务配置信息。

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

3. 使用 `start-task <task-name>` 重启恢复任务。

{{< copyable "" >}}

```bash
help update-task
```

```
update a task's config for routes, filters, column-mappings, or black-white-list

Usage:
  dmctl update-task [-w worker ...] <config-file> [flags]

Flags:
  -h, --help   help for update-task

Global Flags:
  -w, --worker strings   DM-worker ID
```

#### 命令用法示例

{{< copyable "" >}}

```bash
update-task [-w "127.0.0.1:8262"] ./task.yaml
```

#### 参数解释

- `-w`：
    - 可选
    - 指定在特定的一组 DM-workers 上更新数据同步任务的子任务
    - 如果设置，则只更新指定 DM-workers 上的子任务配置
- `config-file`：
    - 必选
    - 指定 `task.yaml` 的文件路径

#### 返回结果示例

{{< copyable "" >}}

```bash
update-task task_all_black.yaml
```

```
{
     "result": true,
     "msg": "",
     "workers": [
         {
             "result": true,
             "worker": "172.16.30.15:8262",
             "msg": ""
         },
         {
             "result": true,
             "worker": "172.16.30.16:8262",
             "msg": ""
         }
     ]
}
```

## 管理 DDL lock

目前与 DDL lock 相关的命令主要包括 `show-ddl-locks`、`unlock-ddl-lock`、`break-ddl-lock` 等。有关它们的功能、用法以及适用场景等，请参考[手动处理 sharding DDL lock](/v3.0/reference/tools/data-migration/features/manually-handling-sharding-ddl-locks.md)。

## 其他任务与集群管理命令

除上述常用的任务管理命令外，DM 还提供了其他一些命令用于管理数据同步任务或 DM 集群本身。

### 检查任务配置文件

`check-task` 命令用于检查指定的数据同步任务配置文件（`task.yaml`）是否合法以及上下游数据库的配置、权限、表结构等是否满足同步需要。具体可参考[上游 MySQL 实例配置前置检查](/v3.0/reference/tools/data-migration/precheck.md)。

在使用 `start-task` 启动同步任务时，DM 也会执行 `check-task` 所做的全部检查。

{{< copyable "" >}}

```bash
help check-task
```

```
check the config file of the task

Usage:
 dmctl check-task <config-file> [flags]

Flags:
 -h, --help   help for check-task

Global Flags:
 -w, --worker strings   DM-worker ID
```

#### 命令用法示例

{{< copyable "" >}}

```bash
check-task task.yaml
```

#### 参数解释

+ `config-file`：
    - 必选
    - 指定 `task.yaml` 的文件路径

#### 返回结果示例

{{< copyable "" >}}

```bash
check-task task-test.yaml
```

```
{
    "result": true,
    "msg": "check pass!!!"
}
```

### 暂停 relay 处理单元

relay 处理单元在 DM-worker 进程启动后即开始自动运行。通过使用 `pause-relay` 命令，我们可以暂停 relay 处理单元的运行。

当需要切换 DM-worker 通过虚拟 IP 连接的上游 MySQL 时，我们需要使用 `pause-relay` 对 DM 执行变更。具体变更步骤请参考[虚拟 IP 环境下的上游主从切换](/v3.0/reference/tools/data-migration/usage-scenarios/master-slave-switch.md#虚拟-IP-环境下的上游主从切换)。

{{< copyable "" >}}

```bash
help pause-relay
```

```
pause DM-worker's relay unit

Usage:
  dmctl pause-relay <-w worker ...> [flags]

Flags:
  -h, --help   help for pause-relay

Global Flags:
  -w, --worker strings   DM-worker ID
```

#### 命令用法示例

{{< copyable "" >}}

```bash
pause-relay -w "127.0.0.1:8262"
```

#### 参数解释

- `-w`：
    - 必选
    - 指定需要暂停 relay 处理单元的 DM-worker

#### 返回结果示例

{{< copyable "" >}}

```bash
pause-relay -w "172.16.30.15:8262"
```

```
{
    "op": "InvalidRelayOp",
    "result": true,
    "msg": "",
    "workers": [
        {
            "op": "PauseRelay",
            "result": true,
            "worker": "172.16.30.15:8262",
            "msg": ""
        }
    ]
}
```

### 恢复 relay 处理单元

`resume-relay` 用于恢复处于 `Paused` 状态的 relay 处理单元。

当需要切换 DM-worker 通过虚拟 IP 连接的上游 MySQL 时，我们需要使用 `resume-relay` 对 DM 执行变更。具体变更步骤请参考[虚拟 IP 环境下的上游主从切换](/v3.0/reference/tools/data-migration/usage-scenarios/master-slave-switch.md#虚拟-IP-环境下的上游主从切换)。

{{< copyable "" >}}

```bash
help resume-relay
```

```
resume DM-worker's relay unit

Usage:
  dmctl resume-relay <-w worker ...> [flags]

Flags:
  -h, --help   help for resume-relay

Global Flags:
  -w, --worker strings   DM-worker ID
```

#### 命令用法示例

{{< copyable "" >}}

```bash
resume-relay -w "127.0.0.1:8262"
```

#### 参数解释

- `-w`：
    - 必选
    - 指定需要恢复 relay 处理单元的 DM-worker

#### 返回结果示例

{{< copyable "" >}}

```bash
resume-relay -w "172.16.30.15:8262"
```

```
{
    "op": "InvalidRelayOp",
    "result": true,
    "msg": "",
    "workers": [
        {
            "op": "ResumeRelay",
            "result": true,
            "worker": "172.16.30.15:8262",
            "msg": ""
        }
    ]
}
```

### 切换 relay log 到新的子目录

relay 处理单元通过使用不同的子目录来存储来自上游不同 MySQL 实例的 binlog 数据。通过使用 `switch-relay-master` 命令，我们可以变更 relay 处理单元以开始使用一个新的子目录。

当需要切换 DM-worker 通过虚拟 IP 连接的上游 MySQL 时，我们需要使用 `switch-relay-master` 对 DM 执行变更。具体变更步骤请参考[虚拟 IP 环境下的上游主从切换](/v3.0/reference/tools/data-migration/usage-scenarios/master-slave-switch.md#虚拟-IP-环境下的上游主从切换)。

{{< copyable "" >}}

```bash
help switch-relay-master
```

```
switch the master server of the DM-worker's relay unit

Usage:
  dmctl switch-relay-master <-w worker ...> [flags]

Flags:
  -h, --help   help for switch-relay-master

Global Flags:
  -w, --worker strings   DM-worker ID
```

#### 命令用法示例

{{< copyable "" >}}

```bash
switch-relay-master -w "127.0.0.1:8262"
```

#### 参数解释

- `-w`：
    - 必选
    - 指定需要切换 relay 处理单元使用子目录的 DM-worker

#### 返回结果示例

{{< copyable "" >}}

```bash
switch-relay-master -w "172.16.30.15:8262"
```

```
{
    "result": true,
    "msg": "",
    "workers": [
        {
            "result": true,
            "worker": "172.16.30.15:8262",
            "msg": ""
        }
    ]
}
```

### 手动清理 relay log

DM 支持[自动清理 relay log](/v3.0/reference/tools/data-migration/relay-log.md#自动数据清理)，但同时 DM 也支持使用 `purge-relay` 命令[手动清理 relay log](/v3.0/reference/tools/data-migration/relay-log.md#手动数据清理)。

{{< copyable "" >}}

```bash
help purge-relay
```

```
purge relay log files of the DM-worker according to the specified filename

Usage:
  dmctl purge-relay <-w worker> [--filename] [--sub-dir] [flags]

Flags:
  -f, --filename string   name of the terminal file before which to purge relay log files. Sample format: "mysql-bin.000006"
  -h, --help              help for purge-relay
  -s, --sub-dir string    specify relay sub directory for --filename. If not specified, the latest one will be used. Sample format: "2ae76434-f79f-11e8-bde2-0242ac130008.000001"

Global Flags:
  -w, --worker strings   DM-worker ID
```

#### 命令用法示例

{{< copyable "" >}}

```bash
purge-relay -w "127.0.0.1:8262" --filename "mysql-bin.000003"
```

#### 参数解释

- `-w`：
    - 必选
    - 指定需要执行 relay log 清理操作的 DM-worker
- `--filename`：
    - 必选
    - 指定标识 relay log 将要停止清理的文件名。如指定为 `mysql-bin.000100`，则只尝试清理到 `mysql-bin.000099`
- `--sub-dir`：
    - 可选
    - 指定 `--filename` 对应的 relay log 子目录，如果不指定则会使用当前最新的子目录

#### 返回结果示例

{{< copyable "" >}}

```bash
purge-relay -w "127.0.0.1:8262" --filename "mysql-bin.000003"
```

```
[warn] no --sub-dir specified for --filename; the latest one will be used
{
    "result": true,
    "msg": "",
    "workers": [
        {
            "result": true,
            "worker": "127.0.0.1:8262",
            "msg": ""
        }
    ]
}
```

### 预设跳过 DDL 操作

`sql-skip` 命令用于预设一个跳过操作。当 binlog event 的 position 或 SQL 语句与指定的 `binlog-pos` 或 `sql-pattern` 匹配时，执行该跳过操作。相关参数与结果解释，请参考[`sql-skip`](/v3.0/reference/tools/data-migration/skip-replace-sqls.md#sql-skip)。

### 预设替换 DDL 操作

`sql-replace` 命令用于预设一个替换执行操作。当 binlog event 的 position 或 SQL 语句与指定的 `binlog-pos` 或 `sql-pattern` 匹配时，执行该替换执行操作。相关参数与结果解释，请参考[`sql-replace`](/v3.0/reference/tools/data-migration/skip-replace-sqls.md#sql-replace)。

### 强制刷新 `task => DM-workers` 映射关系

`refresh-worker-tasks` 命令用于强制刷新 DM-master 内存中维护的 `task => DM-workers` 映射关系。

> **注意：**
>
> 一般不需要使用此命令。仅当已确定 `task => DM-workers` 映射关系存在，但执行其它命令时仍提示必须刷新它时，你才需要使用此命令。

## 废弃或不推荐使用的命令

以下命令已经被废弃或仅用于 debug，在接下来的版本中可能会被移除或修改其语义，**强烈不推荐使用**。

- `migrate-relay`
- `sql-inject`
- `update-master-config`
- `update-relay`
