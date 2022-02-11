---
title: 使用 dmctl 运维集群
summary: 了解如何使用 dmctl 运维 DM 集群。
---

# 使用 dmctl 运维集群

> **注意：**
>
> 对于用 TiUP 部署的 DM 集群，推荐直接使用 [`tiup dmctl` 命令](/dm/maintain-dm-using-tiup.md#集群控制工具-dmctl)。

dmctl 是用来运维 DM 集群的命令行工具，支持交互模式和命令模式。

## dmctl 交互模式

进入交互模式，与 DM-master 进行交互：

> **注意：**
>
> 交互模式下不具有 bash 的特性，比如不需要通过引号传递字符串参数而应当直接传递。

{{< copyable "shell-regular" >}}

```bash
./dmctl --master-addr 172.16.30.14:8261
```

```
Welcome to dmctl
Release Version: ${version}
Git Commit Hash: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
Git Branch: release-x.x
UTC Build Time: yyyy-mm-dd hh:mm:ss
Go Version: go version gox.xx linux/amd64

» help
DM control

Usage:
  dmctl [command]

Available Commands:
  check-task      Checks the configuration file of the task.
  config          Commands to import/export config.
  get-config      Gets the configuration.
  handle-error    `skip`/`replace`/`revert` the current error event or a specific binlog position (binlog-pos) event.
  help            Help about any command
  list-member     Lists member information.
  offline-member  Offlines member which has been closed.
  operate-leader  `evict`/`cancel-evict` the leader.
  operate-schema  `get`/`set`/`remove` the schema for an upstream table.
  operate-source  `create`/`update`/`stop`/`show` upstream MySQL/MariaDB source.
  pause-relay     Pauses DM-worker's relay unit.
  pause-task      Pauses a specified running task.
  purge-relay     Purges relay log files of the DM-worker according to the specified filename.
  query-status    Queries task status.
  resume-relay    Resumes DM-worker's relay unit.
  resume-task     Resumes a specified paused task.
  show-ddl-locks  Shows un-resolved DDL locks.
  start-task      Starts a task as defined in the configuration file.
  stop-task       Stops a specified task.
  unlock-ddl-lock Unlocks DDL lock forcefully.

Flags:
  -h, --help             help for dmctl
  -s, --source strings   MySQL Source ID.

Use "dmctl [command] --help" for more information about a command.
```

## dmctl 命令模式

命令模式跟交互模式的区别是，执行命令时只需要在 dmctl 命令后紧接着执行任务操作，任务操作同交互模式的参数一致。

> **注意：**
>
> + 一条 dmctl 命令只能跟一个任务操作
> + 从 v2.0.4 版本开始，支持从环境变量 (DM_MASTER_ADDR) 里读取 `-master-addr` 参数

{{< copyable "shell-regular" >}}

```bash
./dmctl --master-addr 172.16.30.14:8261 start-task task.yaml
./dmctl --master-addr 172.16.30.14:8261 stop-task task
./dmctl --master-addr 172.16.30.14:8261 query-status

export DM_MASTER_ADDR="172.16.30.14:8261"
./dmctl query-status
```

```
Available Commands:
  check-task            check-task <config-file> [--error count] [--warn count]
  config                commands to import/export config
  get-config            get-config <task | master | worker | source> <name> [--file filename]
  handle-error          handle-error <task-name | task-file> [-s source ...] [-b binlog-pos] <skip/replace/revert> [replace-sql1;replace-sql2;]
  list-member           list-member [--leader] [--master] [--worker] [--name master-name/worker-name ...]
  offline-member        offline-member <--master/--worker> <--name master-name/worker-name>
  operate-leader        operate-leader <operate-type>
  operate-schema        operate-schema <operate-type> <-s source ...> <task-name | task-file> <-d database> <-t table> [schema-file]
  operate-source        operate-source <operate-type> [config-file ...] [--print-sample-config]
  pause-relay           pause-relay <-s source ...>
  pause-task            pause-task [-s source ...] <task-name | task-file>
  purge-relay           purge-relay <-s source> <-f filename> [--sub-dir directory]
  query-status          query-status [-s source ...] [task-name | task-file] [--more]
  resume-relay          resume-relay <-s source ...>
  resume-task           resume-task [-s source ...] <task-name | task-file>
  show-ddl-locks        show-ddl-locks [-s source ...] [task-name | task-file]
  start-task            start-task [-s source ...] [--remove-meta] <config-file>
  stop-task             stop-task [-s source ...] <task-name | task-file>
  unlock-ddl-lock       unlock-ddl-lock [-s source ...] <lock-ID>

Special Commands:
  --encrypt Encrypts plaintext to ciphertext.
  --decrypt Decrypts ciphertext to plaintext.

Global Options:
  --V Prints version and exit.
  --config Path to configuration file.
  --master-addr Master API server address.
  --rpc-timeout RPC timeout, default is 10m.
  --ssl-ca Path of file that contains list of trusted SSL CAs for connection.
  --ssl-cert Path of file that contains X509 certificate in PEM format for connection.
  --ssl-key Path of file that contains X509 key in PEM format for connection.
```
